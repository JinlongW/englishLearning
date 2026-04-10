#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理所有单词数据，为重新导入做准备
"""

import pyodbc
import sys

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

def main():
    print("=" * 60)
    print("清理单词数据")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    # 统计当前数据
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tb_word")
    word_count = cursor.fetchone()[0]
    print(f"当前单词总数：{word_count} 条")

    # 删除所有单词数据
    cursor.execute("DELETE FROM tb_word")
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM tb_word")
    new_count = cursor.fetchone()[0]

    print(f"删除后单词总数：{new_count} 条")
    print(f"已删除 {word_count - new_count} 条记录")

    # 保留年级单元数据
    cursor.execute("SELECT COUNT(*) FROM tb_grade_unit")
    unit_count = cursor.fetchone()[0]
    print(f"年级单元数量：{unit_count} 个 (已保留)")

    conn.close()

    print("=" * 60)
    print("清理完成！可以重新导入数据了")
    print("=" * 60)

if __name__ == '__main__':
    main()
