"""
qwerty-learner 词库导入工具
日期：2026-04-02
说明：将 qwerty-learner 格式的 JSON 词库导入到 EnglishLearning 数据库
"""

import json
import pyodbc
import os
from pathlib import Path
from typing import List, Dict, Any

# ==================== 配置区域 ====================
# 数据库连接配置
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"
DB_USERNAME = ""  # 留空使用 Windows 集成认证
DB_PASSWORD = ""

# qwerty-learner 词库目录
DICTS_DIR = Path(__file__).parent.parent.parent / "qwerty-learner" / "public" / "dicts"

# ==================== 数据库连接 ====================
def get_db_connection():
    """创建数据库连接"""
    if DB_USERNAME and DB_PASSWORD:
        # SQL Server 认证
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD}"
        )
    else:
        # Windows 集成认证
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"Trusted_Connection=yes;"
        )
    return pyodbc.connect(conn_str)

# ==================== 数据转换 ====================
def parse_phonetic(phone: str) -> str:
    """
    处理音标格式
    qwerty-learner 的音标可能包含额外的空格或格式问题
    """
    if not phone:
        return ""
    # 去除多余空格，保持原有音标符号
    return phone.strip()

def create_meaning_trans(trans: List[str]) -> str:
    """
    将中文释义列表转换为 JSON 字符串
    """
    return json.dumps(trans, ensure_ascii=False)

def extract_main_meaning(trans: List[str]) -> str:
    """
    提取主要释义（第一个）
    """
    if not trans:
        return ""
    return trans[0] if trans else ""

# ==================== 文件解析 ====================
def load_dict_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    加载 qwerty-learner 格式的词典文件
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def parse_dict_filename(filename: str) -> Dict[str, str]:
    """
    解析词典文件名，提取教材信息
    格式：PEPXiaoXue3_1_T.json
    """
    result = {
        "publisher": "",
        "level": "",
        "grade": "",
        "semester": "",
        "version": ""
    }

    # 人教版小学
    if "PEPXiaoXue" in filename:
        result["publisher"] = "PEP"
        result["level"] = "小学"

        # 提取年级和学期
        parts = filename.replace("PEPXiaoXue", "").split("_")
        if len(parts) >= 2:
            result["grade"] = parts[0]
            semester_num = parts[1]
            result["semester"] = "上" if semester_num == "1" else "下"
            result["version"] = "T" if len(parts) > 2 and "T" in parts[2] else "S"

    return result

# ==================== 数据导入 ====================
def get_or_create_grade_unit(conn, grade: int, semester: str, unit_no: int, unit_name: str) -> str:
    """
    获取或创建年级单元记录
    """
    cursor = conn.cursor()

    # 查询是否存在
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))

    row = cursor.fetchone()
    if row:
        return row.id

    # 创建新单元
    cursor.execute("""
        INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
        VALUES (?, ?, ?, ?, ?)
    """, (grade, semester, unit_no, unit_name, unit_no))

    conn.commit()

    cursor.execute("SELECT TOP 1 id FROM tb_grade_unit ORDER BY created_at DESC")
    return cursor.fetchone().id

def get_unit_name_for_grade(grade: int, semester: str, unit_no: int) -> str:
    """
    根据年级、学期和单元号生成单元名称
    参考人教版小学英语教材结构
    """
    # 人教版小学英语每册 6 个单元
    unit_names = {
        (3, '上', 1): 'Unit 1 Hello!',
        (3, '上', 2): 'Unit 2 Look at Me',
        (3, '上', 3): 'Unit 3 Let\'s Paint',
        (3, '上', 4): 'Unit 4 We Love Animals',
        (3, '上', 5): 'Unit 5 Let\'s Eat',
        (3, '上', 6): 'Unit 6 Happy Birthday',
        (3, '下', 1): 'Unit 1 Welcome Back to School',
        (3, '下', 2): 'Unit 2 My Family',
        (3, '下', 3): 'Unit 3 At the Zoo',
        (3, '下', 4): 'Unit 4 Where Is My Car',
        (3, '下', 5): 'Unit 5 Do You Like Pears',
        (3, '下', 6): 'Unit 6 How Many',
        # 四年级
        (4, '上', 1): 'Unit 1 My Classroom',
        (4, '上', 2): 'Unit 2 My Schoolbag',
        (4, '上', 3): 'Unit 3 My Friends',
        (4, '上', 4): 'Unit 4 My Home',
        (4, '上', 5): 'Unit 5 Dinner\'s Ready',
        (4, '上', 6): 'Unit 6 Meet My Family',
        # 五年级
        (5, '上', 1): 'Unit 1 What\'s He Like',
        (5, '上', 2): 'Unit 2 My Week',
        (5, '上', 3): 'Unit 3 What Would You Like',
        # 六年级
        (6, '上', 1): 'Unit 1 How Can I Get There',
        (6, '上', 2): 'Unit 2 Ways to Go to School',
        (6, '上', 3): 'Unit 3 My Weekend Plan',
        (6, '上', 4): 'Unit 4 Then and Now',
        (6, '上', 5): 'Unit 5 Occupations',
        (6, '上', 6): 'Unit 6 How Do You Feel',
    }

    key = (grade, semester, unit_no)
    return unit_names.get(key, f'Unit {unit_no}')

def import_words_to_unit(conn, unit_id: str, words: List[Dict[str, Any]], start_order: int = 1):
    """
    导入单词到指定单元
    """
    cursor = conn.cursor()

    for idx, word_data in enumerate(words):
        word = word_data.get("name", "")
        trans = word_data.get("trans", [])
        uk_phone = parse_phonetic(word_data.get("ukphone", ""))
        us_phone = parse_phonetic(word_data.get("usphone", ""))

        if not word:
            continue

        meaning_cn = extract_main_meaning(trans)
        meaning_trans = create_meaning_trans(trans)

        # 使用 MERGE 语句实现存在则更新，不存在则插入
        cursor.execute("""
            MERGE tb_word AS target
            USING (SELECT ? AS word) AS source
            ON target.word = source.word AND target.grade_unit_id = ?
            WHEN MATCHED THEN
                UPDATE SET
                    target.phonetic_uk = ?,
                    target.phonetic_us = ?,
                    target.meaning_cn = ?,
                    target.meaning_trans = ?,
                    target.sort_order = ?
            WHEN NOT MATCHED THEN
                INSERT (grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, meaning_trans, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            word, unit_id,
            uk_phone, us_phone,
            meaning_cn, meaning_trans,
            start_order + idx,
            unit_id, word, uk_phone, us_phone, meaning_cn, meaning_trans, start_order + idx
        ))

    conn.commit()
    print(f"  已导入 {len(words)} 个单词")

# ==================== 主流程 ====================
def process_dict_file(conn, dict_file: Path):
    """
    处理单个词典文件 - 按单元导入
    """
    print(f"\n处理文件：{dict_file.name}")

    # 解析文件名获取教材信息
    meta = parse_dict_filename(dict_file.name)
    print(f"  教材信息：{meta}")

    # 加载词典数据
    words = load_dict_file(dict_file)
    print(f"  单词数量：{len(words)}")

    # 根据文件名获取年级和学期
    if not meta["grade"]:
        print(f"  跳过：无法解析年级信息")
        return

    grade = int(meta["grade"])
    semester = meta["semester"]

    # 人教版小学英语每册 6 个单元，将单词平均分配到 6 个单元
    unit_count = 6
    total_words = len(words)
    words_per_unit = (total_words + unit_count - 1) // unit_count

    for unit_idx in range(unit_count):
        start = unit_idx * words_per_unit
        end = min((unit_idx + 1) * words_per_unit, total_words)

        if start >= total_words:
            break

        unit_words = words[start:end]
        unit_no = unit_idx + 1
        unit_name = get_unit_name_for_grade(grade, semester, unit_no)

        # 获取或创建单元
        unit_id = get_or_create_grade_unit(conn, grade, semester, unit_no, unit_name)
        print(f"  处理单元 {unit_no}: {unit_name} ({start+1}-{end} 词，共{len(unit_words)}个)")

        # 导入单词
        import_words_to_unit(conn, unit_id, unit_words, start + 1)

def main():
    """
    主函数
    """
    print("=" * 50)
    print("qwerty-learner 词库导入工具")
    print("=" * 50)

    # 检查词典目录
    if not DICTS_DIR.exists():
        print(f"错误：词典目录不存在：{DICTS_DIR}")
        print("请将 qwerty-learner 的 public/dicts 目录复制到此处")
        return

    # 获取所有 JSON 文件
    dict_files = list(DICTS_DIR.glob("PEP*.json"))
    if not dict_files:
        print(f"错误：未找到 PEP 开头的词典文件")
        return

    print(f"找到 {len(dict_files)} 个词典文件")

    # 连接数据库
    try:
        conn = get_db_connection()
        print("数据库连接成功")
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return

    # 处理每个词典文件
    for dict_file in dict_files:
        try:
            process_dict_file(conn, dict_file)
        except Exception as e:
            print(f"处理文件 {dict_file.name} 时出错：{e}")

    conn.close()
    print("\n" + "=" * 50)
    print("导入完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
