#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 题库数据校验工具
检查导入单词的正确性和完整性
"""

import pyodbc
import sys

# 配置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

DB_CONFIG = {
    'server': 'localhost',
    'database': 'EnglishLearning',
    'trusted_connection': 'yes'
}

def get_connection_string():
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
    )

# 预期的各年级单词数（根据教材大纲）
EXPECTED_WORD_COUNTS = {
    (3, "上"): 54, (3, "下"): 57,
    (4, "上"): 52, (4, "下"): 57,
    (5, "上"): 59, (5, "下"): 62,
    (6, "上"): 69, (6, "下"): 69,
}

def check_duplicate_words(conn):
    """检查重复单词"""
    print("\n" + "=" * 60)
    print("【1】检查重复单词")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.word, gu.grade, gu.semester, gu.unit_name, COUNT(*) as cnt
        FROM tb_word w
        JOIN tb_grade_unit gu ON w.grade_unit_id = gu.id
        GROUP BY w.word, gu.grade, gu.semester, gu.unit_name
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
    """)

    duplicates = cursor.fetchall()
    if duplicates:
        print(f"发现 {len(duplicates)} 个重复的单词记录:")
        for row in duplicates[:20]:  # 只显示前 20 个
            print(f"  - {row.word} ({row.grade}年级{row.semester}册 {row.unit_name}): {row.cnt} 次")
    else:
        print("✅ 没有发现重复单词")
    return len(duplicates)

def check_word_count(conn):
    """检查各年级单词数量"""
    print("\n" + "=" * 60)
    print("【2】检查各年级单词数量")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT gu.grade, gu.semester, COUNT(w.id) as word_count
        FROM tb_grade_unit gu
        LEFT JOIN tb_word w ON gu.id = w.grade_unit_id
        GROUP BY gu.grade, gu.semester
        ORDER BY gu.grade, gu.semester
    """)

    results = cursor.fetchall()

    print(f"{'年级':<8} {'学期':<6} {'实际数量':<10} {'预期数量':<10} {'状态'}")
    print("-" * 50)

    all_ok = True
    for row in results:
        grade = row.grade
        semester = row.semester
        actual = row.word_count
        expected = EXPECTED_WORD_COUNTS.get((grade, semester), 0)

        # 判断状态
        if expected == 0:
            status = "⚠️ 无预期数据"
        elif actual == expected:
            status = "✅ 正确"
        elif actual > expected:
            status = f"⚠️ 多出 {actual - expected} 个 (可能重复)"
            all_ok = False
        else:
            status = f"⚠️ 缺少 {expected - actual} 个"
            all_ok = False

        print(f"{grade:<8} {semester:<6} {actual:<10} {expected:<10} {status}")

    return all_ok

def check_empty_units(conn):
    """检查没有单词的单元"""
    print("\n" + "=" * 60)
    print("【3】检查没有单词的单元")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT gu.grade, gu.semester, gu.unit_no, gu.unit_name, COUNT(w.id) as word_count
        FROM tb_grade_unit gu
        LEFT JOIN tb_word w ON gu.id = w.grade_unit_id
        GROUP BY gu.grade, gu.semester, gu.unit_no, gu.unit_name
        HAVING COUNT(w.id) = 0
        ORDER BY gu.grade, gu.semester, gu.unit_no
    """)

    empty_units = cursor.fetchall()
    if empty_units:
        print(f"发现 {len(empty_units)} 个单元没有单词数据:")
        for row in empty_units:
            print(f"  - {row.grade}年级{row.semester}册 {row.unit_name}")
    else:
        print("✅ 所有单元都有单词数据")
    return len(empty_units)

def check_data_quality(conn):
    """检查数据质量（必填字段）"""
    print("\n" + "=" * 60)
    print("【4】检查数据质量（必填字段）")
    print("=" * 60)

    cursor = conn.cursor()

    # 检查缺少音标的单词
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE phonetic_uk IS NULL OR phonetic_uk = '' OR phonetic_us IS NULL OR phonetic_us = ''
    """)
    no_phonetic = cursor.fetchone()[0]

    # 检查缺少中文意思的单词
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_cn IS NULL OR meaning_cn = ''
    """)
    no_meaning = cursor.fetchone()[0]

    # 检查缺少例句的单词
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE example_en IS NULL OR example_en = ''
    """)
    no_example = cursor.fetchone()[0]

    print(f"缺少音标的单词：{no_phonetic} 个")
    print(f"缺少中文意思的单词：{no_meaning} 个")
    print(f"缺少英文例句的单词：{no_example} 个")

    issues = no_phonetic + no_meaning + no_example
    if issues == 0:
        print("✅ 所有单词数据完整")
    else:
        print(f"⚠️ 共有 {issues} 个单词缺少必填字段")

    return issues == 0

def sample_check(conn):
    """抽样检查"""
    print("\n" + "=" * 60)
    print("【5】抽样检查（每个年级随机抽查 3 个单词）")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 3 w.word, w.phonetic_uk, w.meaning_cn, w.part_of_speech,
               w.example_en, w.example_cn, gu.grade, gu.semester, gu.unit_name
        FROM tb_word w
        JOIN tb_grade_unit gu ON w.grade_unit_id = gu.id
        WHERE gu.grade = 3 AND gu.semester = '上'
        ORDER BY NEWID()
    """)

    print("\n三年级上册抽样:")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"单词：{row.word}")
        print(f"  音标：{row.phonetic_uk}")
        print(f"  意思：{row.meaning_cn} ({row.part_of_speech})")
        print(f"  例句：{row.example_en}")
        print(f"  翻译：{row.example_cn}")
        print()

def generate_report(conn):
    """生成完整报告"""
    print("\n" + "=" * 60)
    print("【数据校验总结报告】")
    print("=" * 60)

    cursor = conn.cursor()

    # 总统计
    cursor.execute("SELECT COUNT(*) FROM tb_grade_unit")
    unit_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tb_word")
    word_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT word) FROM tb_word")
    unique_words = cursor.fetchone()[0]

    print(f"年级单元总数：{unit_count} 个")
    print(f"单词记录总数：{word_count} 条")
    print(f"唯一单词数量：{unique_words} 个")
    print(f"预期单词总数：{sum(EXPECTED_WORD_COUNTS.values())} 个")

    if unique_words == sum(EXPECTED_WORD_COUNTS.values()):
        print("\n✅ 数据校验通过！")
    else:
        diff = word_count - sum(EXPECTED_WORD_COUNTS.values())
        if diff > 0:
            print(f"\n⚠️ 发现 {diff} 条重复记录，建议清理")
        else:
            print(f"\n⚠️ 缺少 {abs(diff)} 条记录")

def main():
    print("=" * 60)
    print("人教版小学英语 (PEP) 题库数据校验工具")
    print("=" * 60)

    try:
        conn = pyodbc.connect(get_connection_string())
        print("数据库连接成功！")
    except Exception as e:
        print(f"数据库连接失败：{e}")
        sys.exit(1)

    # 执行各项检查
    duplicate_count = check_duplicate_words(conn)
    check_word_count(conn)
    empty_units = check_empty_units(conn)
    data_quality = check_data_quality(conn)
    sample_check(conn)
    generate_report(conn)

    conn.close()

    print("\n" + "=" * 60)
    print("校验完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
