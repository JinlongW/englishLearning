#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语单词表数据导入工具
支持从 Excel/CSV 文件导入单词数据到 SQL Server 数据库
"""

import json
import pyodbc
import pandas as pd
import sys
from pathlib import Path

# 配置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

# 数据库连接配置
DB_CONFIG = {
    'server': 'localhost',
    'database': 'EnglishLearning',
    'trusted_connection': 'yes'
}

def get_connection_string():
    """生成 SQL Server 连接字符串"""
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
    )

def load_words_from_json(json_path):
    """从 JSON 文件加载单词数据"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('data', {}).get('gradeUnits', [])

def load_words_from_excel(excel_path):
    """从 Excel 文件加载单词数据"""
    df = pd.read_excel(excel_path)
    # 期望的列名：grade, semester, unit_no, unit_name, word, phonetic_uk, phonetic_us,
    # meaning_cn, part_of_speech, example_en, example_cn
    return df.to_dict('records')

def load_words_from_csv(csv_path):
    """从 CSV 文件加载单词数据"""
    df = pd.read_csv(csv_path, encoding='utf-8')
    return df.to_dict('records')

def load_words(file_path):
    """根据文件类型自动选择加载方式"""
    ext = Path(file_path).suffix.lower()
    if ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('data', {}).get('gradeUnits', [])
    elif ext in ['.xlsx', '.xls']:
        return load_words_from_excel(file_path)
    elif ext == '.csv':
        return load_words_from_csv(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{ext}")

def get_unit_id(conn, grade, semester, unit_no):
    """根据年级、学期、单元号获取单元 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def insert_word(conn, grade_unit_id, word_data):
    """插入单个单词数据"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_word (
            id, grade_unit_id, word, phonetic_uk, phonetic_us,
            meaning_cn, part_of_speech, example_en, example_cn, sort_order
        ) VALUES (
            NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """,
        grade_unit_id,
        word_data.get('word', ''),
        word_data.get('phonetic_uk', ''),
        word_data.get('phonetic_us', ''),
        word_data.get('meaning_cn', ''),
        word_data.get('part_of_speech', ''),
        word_data.get('example_en', ''),
        word_data.get('example_cn', ''),
        word_data.get('sort_order', 1)
    )
    conn.commit()

def import_words(file_path):
    """主导入函数"""
    print("=" * 50)
    print("人教版小学英语单词表导入工具")
    print("=" * 50)

    # 连接数据库
    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    # 加载数据
    data = load_words(file_path)

    # 判断数据类型并统一处理
    if data and isinstance(data[0], dict) and 'words' in data[0]:
        # JSON 格式：包含 gradeUnits 数组
        units = data
        print(f"加载了 {len(units)} 个单元的数据")
    else:
        # CSV/Excel 格式：扁平数据，需要按单元分组
        print(f"加载了 {len(data)} 条单词记录")
        # 按单元分组
        unit_groups = {}
        for row in data:
            # 确保类型正确
            grade = int(row.get('grade', 0))
            unit_no = int(str(row.get('unit_no', '0')).strip())
            semester = str(row.get('semester', '')).strip()
            unit_name = str(row.get('unit_name', '')).strip()

            key = (grade, semester, unit_no, unit_name)
            if key not in unit_groups:
                unit_groups[key] = {
                    'grade': grade,
                    'semester': semester,
                    'unitNo': unit_no,
                    'unitName': unit_name,
                    'words': []
                }
            # 移除不需要的字段
            word_data = {k: v for k, v in row.items() if k not in ['grade', 'semester', 'unit_no', 'unit_name']}
            unit_groups[key]['words'].append(word_data)
        units = list(unit_groups.values())
        print(f"共 {len(units)} 个单元")

    total_imported = 0

    for unit in units:
        grade = unit.get('grade')
        semester = unit.get('semester')
        unit_no = unit.get('unitNo')
        unit_name = unit.get('unitName')
        words = unit.get('words', [])

        if not words:
            continue

        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[WARN] 单元不存在：{grade}年级{semester}册 Unit {unit_no}，跳过")
            continue

        print(f"正在导入 {grade}年级{semester}册 {unit_name} ({len(words)} 个单词)...")

        for idx, word in enumerate(words, 1):
            word['sort_order'] = idx
            insert_word(conn, unit_id, word)
            total_imported += 1

        print(f"  [OK] {unit_name} 导入完成")

    conn.close()
    print("=" * 50)
    print(f"导入完成！共导入 {total_imported} 个单词")
    print("=" * 50)

if __name__ == '__main__':
    import sys

    # 支持多种文件格式
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'textbook-words.json'

    if not Path(input_file).exists():
        print(f"错误：文件不存在 - {input_file}")
        sys.exit(1)

    print(f"使用文件：{input_file}")
    import_words(input_file)
