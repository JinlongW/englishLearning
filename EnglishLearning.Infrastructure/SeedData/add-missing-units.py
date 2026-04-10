#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加缺失的年级单元数据 (4-6 年级)
"""

import pyodbc

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

# 缺失的单元列表
MISSING_UNITS = [
    # 四年级下册
    (4, "下", 1, "Unit 1 My School", 1),
    (4, "下", 2, "Unit 2 What Time Is It", 2),
    (4, "下", 3, "Unit 3 Weather", 3),
    (4, "下", 4, "Unit 4 At the Farm", 4),
    (4, "下", 5, "Unit 5 My Clothes", 5),
    (4, "下", 6, "Unit 6 Shopping", 6),
    # 五年级上册
    (5, "上", 1, "Unit 1 What's He Like", 1),
    (5, "上", 2, "Unit 2 My Week", 2),
    (5, "上", 3, "Unit 3 What Would You Like", 3),
    (5, "上", 4, "Unit 4 What Can You Do", 4),
    (5, "上", 5, "Unit 5 There Is a Big Bed", 5),
    (5, "上", 6, "Unit 6 In a Nature Park", 6),
    # 五年级下册
    (5, "下", 1, "Unit 1 My Day", 1),
    (5, "下", 2, "Unit 2 My Favourite Season", 2),
    (5, "下", 3, "Unit 3 My School Calendar", 3),
    (5, "下", 4, "Unit 4 When Is Easter", 4),
    (5, "下", 5, "Unit 5 Whose Dog Is It", 5),
    (5, "下", 6, "Unit 6 Work Quietly", 6),
    # 六年级上册
    (6, "上", 1, "Unit 1 How Can I Get There", 1),
    (6, "上", 2, "Unit 2 Ways to Go to School", 2),
    (6, "上", 3, "Unit 3 My Weekend Plan", 3),
    (6, "上", 4, "Unit 4 I Have a Pen Pal", 4),
    (6, "上", 5, "Unit 5 What Does He Do", 5),
    (6, "上", 6, "Unit 6 How Do You Feel", 6),
    # 六年级下册
    (6, "下", 1, "Unit 1 How Tall Are You", 1),
    (6, "下", 2, "Unit 2 Last Weekend", 2),
    (6, "下", 3, "Unit 3 Where Did You Go", 3),
    (6, "下", 4, "Unit 4 Then and Now", 4),
    (6, "下", 5, "Unit 5 Let's Play", 5),
    (6, "下", 6, "Unit 6 A Farewell Party", 6),
]

def unit_exists(conn, grade, semester, unit_no):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    return cursor.fetchone() is not None

def insert_unit(conn, grade, semester, unit_no, unit_name, sort_order):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
        VALUES (NEWID(), ?, ?, ?, ?, ?)
    """, (grade, semester, unit_no, unit_name, sort_order))
    conn.commit()

def main():
    print("=" * 60)
    print("添加缺失的年级单元数据 (4-6 年级)")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    added = 0
    skipped = 0

    for grade, semester, unit_no, unit_name, sort_order in MISSING_UNITS:
        if unit_exists(conn, grade, semester, unit_no):
            print(f"[SKIP] 已存在：{grade}年级{semester}册 {unit_name}")
            skipped += 1
        else:
            insert_unit(conn, grade, semester, unit_no, unit_name, sort_order)
            print(f"[OK] 已添加：{grade}年级{semester}册 {unit_name}")
            added += 1

    conn.close()

    print("=" * 60)
    print(f"完成！添加了 {added} 个单元，跳过了 {skipped} 个单元")
    print("=" * 60)

if __name__ == '__main__':
    main()
