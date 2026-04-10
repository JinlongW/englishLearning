"""
检查题目数据完整性和正确性
- 检查重复题目
- 检查 question_type 是否合法
- 检查外键 grade_unit_id 是否存在
- 统计各题型分布
"""

import pyodbc
from collections import defaultdict

def get_db_connection():
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER=localhost;'
        f'DATABASE=EnglishLearning;'
        f'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def check_question_types(conn):
    """检查 question_type 是否都合法"""
    print("=" * 60)
    print("1. 检查 question_type 合法性")
    print("=" * 60)

    allowed_types = {'listening', 'match', 'spell_word', 'fill_blank',
                    'multiple_choice', 'single_choice', 'order_words'}

    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT question_type FROM tb_question")

    invalid = []
    all_types = []
    for row in cursor.fetchall():
        qtype = row[0]
        all_types.append(qtype)
        if qtype not in allowed_types:
            invalid.append(qtype)

    if invalid:
        print(f"[ERROR] 发现不合法的 question_type: {invalid}")
        return False
    else:
        print("[OK] 所有 question_type 都合法")
        print(f"    现有类型: {sorted(all_types)}")
        return True

def check_duplicate_questions(conn):
    """检查重复题目"""
    print("\n" + "=" * 60)
    print("2. 检查重复题目")
    print("=" * 60)

    cursor = conn.cursor()
    # 按 stem 分组查找重复
    cursor.execute("""
        SELECT question_stem, COUNT(*) as cnt
        FROM tb_question
        GROUP BY question_stem
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
    """)

    duplicates = cursor.fetchall()

    if duplicates:
        print(f"[WARNING] 发现 {len(duplicates)} 组重复题目:")
        for question_stem, cnt in duplicates:
            # 截断过长的标题
            short_stem = question_stem[:60] if len(question_stem) > 60 else question_stem
            print(f"    ({cnt}次) {short_stem}")
        total_dupl = sum(cnt for _, cnt in duplicates) - len(duplicates)
        print(f"\n    总计重复题目数: {total_dupl}")
    else:
        print("[OK] 没有发现重复题目")

    return len(duplicates) == 0

def check_foreign_keys(conn):
    """检查外键 grade_unit_id 是否存在于对应表"""
    print("\n" + "=" * 60)
    print("3. 检查外键 grade_unit_id 完整性")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.grade_unit_id
        FROM tb_question q
        LEFT JOIN tb_grade_unit gu ON q.grade_unit_id = gu.id
        WHERE gu.id IS NULL
    """)

    invalid = cursor.fetchall()

    if invalid:
        print(f"[ERROR] 发现 {len(invalid)} 道题目 grade_unit_id 不存在:")
        for qid, guid in invalid[:10]:
            print(f"    id={qid}, grade_unit_id={guid}")
        if len(invalid) > 10:
            print(f"    ... 还有 {len(invalid) - 10} 个")
        return False
    else:
        print("[OK] 所有题目 grade_unit_id 都有效")
        return True

def check_multiple_meanings(conn):
    """检查多释义 JSON 格式是否正确"""
    print("\n" + "=" * 60)
    print("4. 检查多释义 JSON 格式完整性")
    print("=" * 60)

    import json

    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, word, meaning_trans
        FROM tb_word
        WHERE LEN(ISNULL(meaning_trans, '')) > 0
    """)

    invalid_json = []
    empty_meanings = []

    for word_id, word, meaning_trans in cursor.fetchall():
        if not meaning_trans or meaning_trans.strip() == '':
            empty_meanings.append(word)
            continue

        try:
            data = json.loads(meaning_trans)
            if not isinstance(data, list):
                invalid_json.append((word, "不是数组"))
            elif len(data) == 0:
                empty_meanings.append(word)
        except json.JSONDecodeError as e:
            invalid_json.append((word, str(e)[:50]))

    if invalid_json:
        print(f"[ERROR] 发现 {len(invalid_json)} 个 JSON 格式错误:")
        for word, err in invalid_json[:10]:
            print(f"    {word}: {err}")
        if len(invalid_json) > 10:
            print(f"    ... 还有 {len(invalid_json) - 10} 个")
    else:
        print("[OK] 所有多释义 JSON 格式都正确")

    if empty_meanings:
        print(f"[WARNING] 发现 {len(empty_meanings)} 个多释义数组为空: {empty_meanings[:20]}")
    else:
        print("[OK] 所有多释义数组都非空")

    return len(invalid_json) == 0

def show_statistics(conn):
    """显示详细统计信息"""
    print("\n" + "=" * 60)
    print("5. 详细数据统计")
    print("=" * 60)

    cursor = conn.cursor()

    # 题目统计
    cursor.execute("""
        SELECT question_type, COUNT(*)
        FROM tb_question
        GROUP BY question_type
        ORDER BY COUNT(*) DESC
    """)
    print("\n【题目类型分布】")
    print(f"{'题型':<15} {'数量':>6}")
    print("-" * 25)
    total = 0
    for qtype, cnt in cursor.fetchall():
        print(f"{qtype:<15} {cnt:>6}")
        total += cnt
    print("-" * 25)
    print(f"{'总计':<15} {total:>6}")

    # 多释义统计
    cursor.execute("""
        SELECT
            COUNT(*) as total_words,
            SUM(CASE WHEN LEN(ISNULL(meaning_trans, '')) > 0 THEN 1 ELSE 0 END) as with_multi,
            SUM(CASE WHEN LEN(ISNULL(phonetic_uk, '')) > 0 OR LEN(ISNULL(phonetic_us, '')) > 0 THEN 1 ELSE 0 END) as with_phonetic
        FROM tb_word
    """)
    row = cursor.fetchone()
    total_words, with_multi, with_phonetic = row

    print("\n【单词数据统计】")
    print(f"  总单词数: {total_words}")
    print(f"  有多释义: {with_multi} ({round(with_multi/total_words*100, 2)}%)")
    print(f"  有音标: {with_phonetic} ({round(with_phonetic/total_words*100, 2)}%)")
    print(f"  无多释义: {total_words - with_multi}")

    # 年级统计
    cursor.execute("""
        SELECT gu.grade, COUNT(DISTINCT w.id) as word_count
        FROM tb_grade_unit gu
        JOIN tb_word w ON gu.id = w.grade_unit_id
        GROUP BY gu.grade
        ORDER BY gu.grade
    """)
    print("\n【各年级单词分布】")
    print(f"{'年级':<10} {'单词数':>8}")
    print("-" * 20)
    for grade, cnt in cursor.fetchall():
        print(f"{grade:<10} {cnt:>8}")

def check_null_fields(conn):
    """检查关键字段是否为 NULL"""
    print("\n" + "=" * 60)
    print("6. 检查关键字段空值")
    print("=" * 60)

    cursor = conn.cursor()

    # 检查题目
    cursor.execute("""
        SELECT
            SUM(CASE WHEN question_stem IS NULL OR question_stem = '' THEN 1 ELSE 0 END) as null_stem,
            SUM(CASE WHEN correct_answer IS NULL OR correct_answer = '' THEN 1 ELSE 0 END) as null_answer,
            COUNT(*) as total
        FROM tb_question
    """)
    null_stem, null_answer, total = cursor.fetchone()[0:3]

    print(f"题目表 (tb_question):")
    print(f"    空 question_stem: {null_stem}/{total}")
    print(f"    空 correct_answer: {null_answer}/{total}")

    if null_stem > 0 or null_answer > 0:
        print("[WARNING] 存在空字段!")
    else:
        print("[OK] 关键字段无空值")

    # 检查单词
    cursor.execute("""
        SELECT
            SUM(CASE WHEN word IS NULL OR word = '' THEN 1 ELSE 0 END) as null_word,
            SUM(CASE WHEN meaning_cn IS NULL OR meaning_cn = '' THEN 1 ELSE 0 END) as null_meaning,
            COUNT(*) as total
        FROM tb_word
    """)
    null_word, null_meaning, total = cursor.fetchone()[0:3]

    print(f"\n单词表 (tb_word):")
    print(f"    空 word: {null_word}/{total}")
    print(f"    空 meaning_cn: {null_meaning}/{total}")

    if null_word > 0 or null_meaning > 0:
        print("[WARNING] 存在空字段!")
    else:
        print("[OK] 关键字段无空值")

    return null_stem == 0 and null_answer == 0 and null_word == 0 and null_meaning == 0

def main():
    conn = get_db_connection()

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 18 + "题库完整性检查" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n检查数据库: EnglishLearning@localhost\n")

    checks = [
        check_question_types(conn),
        check_foreign_keys(conn),
        check_duplicate_questions(conn),
        check_multiple_meanings(conn),
        check_null_fields(conn),
    ]

    show_statistics(conn)

    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)

    passed = sum(1 for c in checks if c)
    total = len(checks)

    print(f"\n通过: {passed}/{total}")

    if passed == total:
        print("\n[✓] 所有检查通过，数据完整性良好!")
    else:
        print("\n[!] 发现一些问题需要修复")

    conn.close()

if __name__ == "__main__":
    main()
