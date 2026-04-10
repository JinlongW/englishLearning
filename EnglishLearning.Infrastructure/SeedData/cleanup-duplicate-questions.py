#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题库数据清理脚本
删除重复和模板化的题目数据
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
    print("题库数据清理工具")
    print("删除重复和模板化的题目")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    cursor = conn.cursor()

    # 统计清理前的数量
    cursor.execute('SELECT COUNT(*) FROM tb_question')
    questions_before = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tb_question_option')
    options_before = cursor.fetchone()[0]

    print(f"\n清理前：题目 {questions_before} 道，选项 {options_before} 条")

    # 1. 删除模板化题目（请选择正确的英语表达、选择与中文意思相符的英文句子）
    print("\n【1】删除模板化题目...")
    template_stems = [
        '请选择正确的英语表达：',
        '选择与中文意思相符的英文句子：',
        '关于本单元知识点%',
    ]

    deleted_options = 0
    deleted_questions = 0

    for stem in template_stems:
        # 先删除选项
        cursor.execute("""
            DELETE FROM tb_question_option
            WHERE question_id IN (
                SELECT id FROM tb_question WHERE question_stem LIKE ?
            )
        """, stem)
        deleted_options += cursor.rowcount

        # 再删除题目
        cursor.execute("DELETE FROM tb_question WHERE question_stem LIKE ?", stem)
        deleted_questions += cursor.rowcount
        print(f"  删除'{stem[:20]}...': {cursor.rowcount} 道题")

    # 2. 删除重复题目（保留每组的第一个）
    print("\n【2】删除重复题目（保留每组的第一个）...")

    cursor.execute("""
        SELECT question_stem
        FROM tb_question
        GROUP BY question_stem
        HAVING COUNT(*) > 1
    """)
    duplicate_stems = cursor.fetchall()

    for row in duplicate_stems:
        stem = row.question_stem
        # 获取该题干的所有题目 ID
        cursor.execute("""
            SELECT id FROM tb_question
            WHERE question_stem = ?
            ORDER BY created_at DESC
        """, stem)
        question_ids = cursor.fetchall()

        if len(question_ids) > 1:
            # 保留第一个，删除其余的
            for qid in question_ids[1:]:
                # 先删除选项
                cursor.execute("DELETE FROM tb_question_option WHERE question_id = ?", qid.id)
                deleted_options += cursor.rowcount
                # 再删除题目
                cursor.execute("DELETE FROM tb_question WHERE id = ?", qid.id)
                deleted_questions += cursor.rowcount

    print(f"  删除重复题目：{deleted_questions - 96} 道")  # 减去模板化题目

    conn.commit()

    # 统计清理后的数量
    cursor.execute('SELECT COUNT(*) FROM tb_question')
    questions_after = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tb_question_option')
    options_after = cursor.fetchone()[0]

    print(f"\n清理后：题目 {questions_after} 道，选项 {options_after} 条")
    print(f"\n共计删除：题目 {questions_before - questions_after} 道，选项 {options_before - options_after} 条")

    conn.close()

    print("\n" + "=" * 60)
    print("清理完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
