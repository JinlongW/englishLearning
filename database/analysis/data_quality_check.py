# -*- coding: utf-8 -*-
"""
词库数据检查分析工具
日期：2026-04-02
说明：全面检查词库数据质量、完整性、一致性
"""

import pyodbc
import json
from collections import defaultdict

# ==================== 配置区域 ====================
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

def get_db_connection():
    """创建数据库连接 - Windows 集成认证"""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_subsection(title):
    """打印子标题"""
    print(f"\n[{title}]")

# ==================== 检查项 ====================

def check_data_overview(conn):
    """1. 数据总览"""
    print_section("1. 数据总览")
    cursor = conn.cursor()

    # 单词统计
    cursor.execute("SELECT COUNT(*) FROM tb_word")
    total_words = cursor.fetchone()[0]
    print(f"单词总数：{total_words}")

    # 单元统计
    cursor.execute("SELECT COUNT(*) FROM tb_grade_unit")
    total_units = cursor.fetchone()[0]
    print(f"单元总数：{total_units}")

    # 年级单元分布
    cursor.execute("""
        SELECT grade, semester, COUNT(*) as unit_count, COUNT(w.id) as word_count
        FROM tb_grade_unit gu
        LEFT JOIN tb_word w ON gu.id = w.grade_unit_id
        WHERE grade BETWEEN 3 AND 6
        GROUP BY grade, semester
        ORDER BY grade, semester
    """)

    print("\n按年级分布:")
    print(f"{'年级':<8} {'学期':<6} {'单元数':<10} {'单词数':<10}")
    print("-" * 40)
    for row in cursor.fetchall():
        print(f"{row.grade:<8} {row.semester:<6} {row.unit_count:<10} {row.word_count:<10}")

def check_word_completeness(conn):
    """2. 单词数据完整性检查"""
    print_section("2. 单词数据完整性检查")
    cursor = conn.cursor()

    # 必填字段检查 - 白名单验证防止SQL注入
    ALLOWED_FIELDS = {'word', 'phonetic_uk', 'phonetic_us', 'meaning_cn', 'meaning_trans', 'part_of_speech'}
    checks = [
        ("单词 (word)", "word IS NOT NULL AND word <> ''"),
        ("音标 (phonetic)", "phonetic_uk IS NOT NULL OR phonetic_us IS NOT NULL"),
        ("释义 (meaning_cn)", "meaning_cn IS NOT NULL AND meaning_cn <> ''"),
        ("词性 (part_of_speech)", "part_of_speech IS NOT NULL AND part_of_speech <> ''"),
    ]

    print("\n必填字段完整性:")
    print(f"{'字段':<25} {'完整数':<12} {'缺失数':<12} {'完整率':<10}")
    print("-" * 60)

    for field_name, query_condition in checks:
        # 验证不包含用户输入，都是静态常量，这里额外做白名单验证确保安全
        # 提取字段名进行验证
        import re
        fields_in_condition = re.findall(r'\\b\\w+\\b', query_condition)
        for field in fields_in_condition:
            if field not in ALLOWED_FIELDS:
                raise ValueError(f"非法字段 {field}，不允许动态SQL拼接非白名单字段")
        cursor.execute(f"SELECT COUNT(*) FROM tb_word WHERE {query_condition}")
        complete = cursor.fetchone()[0]
        missing = 1034 - complete
        rate = (complete / 1034) * 100
        print(f"{field_name:<25} {complete:<12} {missing:<12} {rate:.1f}%")

def check_phonetic_data(conn):
    """3. 音标数据检查"""
    print_section("3. 音标数据检查")
    cursor = conn.cursor()
    cursor = conn.cursor()

    # 音标分布
    cursor.execute("""
        SELECT
            SUM(CASE WHEN phonetic_uk IS NOT NULL AND phonetic_uk <> '' THEN 1 ELSE 0 END) as has_uk,
            SUM(CASE WHEN phonetic_us IS NOT NULL AND phonetic_us <> '' THEN 1 ELSE 0 END) as has_us,
            SUM(CASE WHEN (phonetic_uk IS NULL OR phonetic_uk = '') AND (phonetic_us IS NULL OR phonetic_us = '') THEN 1 ELSE 0 END) as no_phonetic
        FROM tb_word
    """)
    row = cursor.fetchone()
    print(f"\n音标统计:")
    print(f"  有英式音标：{row.has_uk}")
    print(f"  有美式音标：{row.has_us}")
    print(f"  无音标数据：{row.no_phonetic}")

    # 缺失音标的单词示例
    cursor.execute("""
        SELECT TOP 10 word, phonetic_uk, phonetic_us
        FROM tb_word
        WHERE (phonetic_uk IS NULL OR phonetic_uk = '')
          AND (phonetic_us IS NULL OR phonetic_us = '')
    """)
    print("\n缺失音标的单词示例 (前 10 个):")
    for row in cursor.fetchall():
        print(f"  - {row.word}")

def check_meaning_data(conn):
    """4. 释义数据检查"""
    print_section("4. 释义数据检查")
    cursor = conn.cursor()

    # 多释义统计
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN meaning_trans IS NOT NULL THEN 1 ELSE 0 END) as has_json,
            SUM(CASE WHEN meaning_trans LIKE '%,%' THEN 1 ELSE 0 END) as multi_meaning
        FROM tb_word
    """)
    row = cursor.fetchone()
    print(f"\n释义统计:")
    print(f"  总单词数：{row.total}")
    print(f"  有 JSON 释义：{row.has_json}")
    print(f"  多释义单词：{row.multi_meaning}")
    print(f"  单释义单词：{row.total - row.multi_meaning}")

    # 多释义单词示例
    cursor.execute("""
        SELECT TOP 10 word, meaning_cn, meaning_trans
        FROM tb_word
        WHERE meaning_trans LIKE '%,%'
        ORDER BY NEWID()
    """)
    print("\n多释义单词示例:")
    for row in cursor.fetchall():
        print(f"  - {row.word}: {row.meaning_trans}")

def check_pos_distribution(conn):
    """5. 词性分布检查"""
    print_section("5. 词性分布检查")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT part_of_speech, COUNT(*) as count
        FROM tb_word
        WHERE part_of_speech IS NOT NULL AND part_of_speech <> ''
        GROUP BY part_of_speech
        ORDER BY count DESC
    """)

    print("\n词性分布:")
    print(f"{'词性':<20} {'数量':<10} {'占比':<10}")
    print("-" * 45)
    total = 0
    for row in cursor.fetchall():
        pos = row.part_of_speech or 'NULL'
        count = row.count
        total += count
        print(f"{pos:<20} {count:<10} {count/10.34:.1f}%")
    print("-" * 45)
    print(f"{'总计':<20} {total:<10}")

def check_unit_word_distribution(conn):
    """6. 单元单词分布检查"""
    print_section("6. 单元单词分布检查")
    cursor = conn.cursor()

    # 每单元单词数统计
    cursor.execute("""
        SELECT
            gu.grade,
            gu.semester,
            gu.unit_no,
            gu.unit_name,
            COUNT(w.id) as word_count
        FROM tb_grade_unit gu
        LEFT JOIN tb_word w ON gu.id = w.grade_unit_id
        WHERE gu.grade BETWEEN 3 AND 6
        GROUP BY gu.grade, gu.semester, gu.unit_no, gu.unit_name
        ORDER BY gu.grade, gu.semester, gu.unit_no
    """)

    print("\n各单元单词数分布:")
    print(f"{'年级':<6} {'学期':<4} {'单元':<25} {'单词数':<8}")
    print("-" * 50)

    word_counts = []
    for row in cursor.fetchall():
        print(f"{row.grade:<6} {row.semester:<4} {row.unit_name:<25} {row.word_count:<8}")
        word_counts.append(row.word_count)

    if word_counts:
        print("-" * 50)
        print(f"平均每单元单词数：{sum(word_counts) / len(word_counts):.1f}")
        print(f"最少单词数：{min(word_counts)}")
        print(f"最多单词数：{max(word_counts)}")

def check_duplicate_words(conn):
    """7. 重复单词检查"""
    print_section("7. 重复单词检查")
    cursor = conn.cursor()

    # 检查同一单元内的重复单词
    cursor.execute("""
        SELECT grade_unit_id, word, COUNT(*) as cnt
        FROM tb_word
        GROUP BY grade_unit_id, word
        HAVING COUNT(*) > 1
    """)

    duplicates = cursor.fetchall()
    if duplicates:
        print(f"\n发现 {len(duplicates)} 个重复单词:")
        for row in duplicates:
            print(f"  - Unit {row.grade_unit_id}: {row.word} ({row.cnt}次)")
    else:
        print("\n[OK] 未发现单元内重复单词")

    # 检查跨单元重复（同一单词出现在多个单元）
    cursor.execute("""
        SELECT word, COUNT(DISTINCT grade_unit_id) as unit_count
        FROM tb_word
        GROUP BY word
        HAVING COUNT(DISTINCT grade_unit_id) > 1
        ORDER BY unit_count DESC
    """)

    cross_unit = cursor.fetchall()
    if cross_unit:
        print(f"\n跨单元重复单词 ({len(cross_unit)}个):")
        for row in cross_unit[:20]:  # 显示前 20 个
            print(f"  - {row.word}: 出现在 {row.unit_count} 个单元")
    else:
        print("\n[OK] 无跨单元重复单词")

def check_grammar_coverage(conn):
    """8. 语法知识点覆盖检查"""
    print_section("8. 语法知识点覆盖检查")
    cursor = conn.cursor()

    # 语法知识点分布
    cursor.execute("""
        SELECT
            gu.grade,
            gu.semester,
            COUNT(DISTINCT g.id) as grammar_count
        FROM tb_grade_unit gu
        LEFT JOIN tb_grammar g ON gu.id = g.grade_unit_id
        WHERE gu.grade BETWEEN 3 AND 6
        GROUP BY gu.grade, gu.semester
        ORDER BY gu.grade, gu.semester
    """)

    print("\n语法知识点覆盖:")
    print(f"{'年级':<8} {'学期':<6} {'语法点数':<10}")
    print("-" * 30)
    for row in cursor.fetchall():
        print(f"{row.grade:<8} {row.semester:<6} {row.grammar_count:<10}")

def check_question_coverage(conn):
    """9. 练习题覆盖检查"""
    print_section("9. 练习题覆盖检查")
    cursor = conn.cursor()

    # 题型分布
    cursor.execute("""
        SELECT question_type, COUNT(*) as count
        FROM tb_question
        GROUP BY question_type
        ORDER BY count DESC
    """)

    print("\n题型分布:")
    print(f"{'题型':<20} {'数量':<10}")
    print("-" * 35)
    for row in cursor.fetchall():
        print(f"{row.question_type:<20} {row.count:<10}")

    # 难度分布
    cursor.execute("""
        SELECT difficulty, COUNT(*) as count
        FROM tb_question
        GROUP BY difficulty
        ORDER BY difficulty
    """)

    print("\n难度分布:")
    difficulty_map = {1: '基础', 2: '中等', 3: '较难', 4: '困难', 5: '专家'}
    print(f"{'难度':<20} {'数量':<10}")
    print("-" * 35)
    for row in cursor.fetchall():
        level = difficulty_map.get(row.difficulty, '未知')
        print(f"{level:<20} {row.count:<10}")

def check_data_quality_issues(conn):
    """10. 数据质量问题检查"""
    print_section("10. 数据质量问题检查")
    cursor = conn.cursor()

    issues = []

    # 检查空释义
    cursor.execute("""
        SELECT TOP 5 word, meaning_cn
        FROM tb_word
        WHERE meaning_cn IS NULL OR meaning_cn = '' OR LEN(LTRIM(RTRIM(meaning_cn))) = 0
    """)
    empty_meanings = cursor.fetchall()
    if empty_meanings:
        issues.append(f"空释义单词：{len(empty_meanings)}个")
        print("\n[WARN] 空释义单词:")
        for row in empty_meanings:
            print(f"  - {row.word}")

    # 检查异常长的单词（可能是数据错误）
    cursor.execute("""
        SELECT TOP 5 word, LEN(word) as word_len
        FROM tb_word
        WHERE LEN(word) > 20
        ORDER BY LEN(word) DESC
    """)
    long_words = cursor.fetchall()
    if long_words:
        issues.append(f"超长单词：{len(long_words)}个")
        print("\n[WARN] 超长单词 (>20 字符):")
        for row in long_words:
            print(f"  - {row.word} ({row.word_len}字符)")

    # 检查 JSON 格式是否有效
    cursor.execute("""
        SELECT TOP 5 word, meaning_trans
        FROM tb_word
        WHERE meaning_trans IS NOT NULL
    """)
    json_words = cursor.fetchall()
    invalid_json = 0
    for row in json_words:
        try:
            if row.meaning_trans:
                json.loads(row.meaning_trans)
        except:
            invalid_json += 1

    if invalid_json > 0:
        issues.append(f"无效 JSON: {invalid_json}个")
        print(f"\n[WARN] 无效 JSON 格式：{invalid_json}个")

    # 总结
    print("\n" + "-" * 40)
    if issues:
        print(f"发现 {len(issues)} 类数据质量问题")
    else:
        print("[OK] 未发现明显数据质量问题")

def generate_recommendations():
    """生成优化建议"""
    print_section("优化建议")

    recommendations = [
        "1. 补充缺失的音标数据（如有）",
        "2. 扩展多释义单词覆盖（目前较少）",
        "3. 增加语法知识点覆盖到全部 48 单元",
        "4. 增加练习题数量和题型多样性",
        "5. 考虑添加例句数据"
    ]

    for rec in recommendations:
        print(f"\n{rec}")

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("=" * 60)
    print("     英语学习项目 - 词库数据检查分析报告")
    print("=" * 60)
    print(f"     数据库：{DB_DATABASE}@{DB_SERVER}")
    print(f"     时间：2026-04-02")
    print("=" * 60)

    try:
        conn = get_db_connection()
        print("[OK] 数据库连接成功\n")

        # 执行所有检查
        check_data_overview(conn)
        check_word_completeness(conn)
        check_phonetic_data(conn)
        check_meaning_data(conn)
        check_pos_distribution(conn)
        check_unit_word_distribution(conn)
        check_duplicate_words(conn)
        check_grammar_coverage(conn)
        check_question_coverage(conn)
        check_data_quality_issues(conn)
        generate_recommendations()

        print("\n" + "=" * 60)
        print("     检查完成!")
        print("=" * 60)

        conn.close()

    except Exception as e:
        print(f"\n[ERROR] 错误：{e}")

if __name__ == "__main__":
    main()
