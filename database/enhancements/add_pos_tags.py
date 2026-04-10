"""
词性标注工具 - 为小学英语单词添加词性
日期：2026-04-02
说明：基于常见词性规则为单词自动标注词性
"""

import json
import pyodbc
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 配置区域 ====================
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"
DB_USERNAME = ""  # Windows 集成认证
DB_PASSWORD = ""

# ==================== 词性规则库 ====================
# 常见名词后缀
NOUN_SUFFIXES = [
    'tion', 'sion', 'ment', 'ness', 'ity', 'ty', 'er', 'or', 'ist', 'ian',
    'ance', 'ence', 'ism', 'ist', 'ship', 'hood', 'th', 'ture', 'ure', 'age'
]

# 常见动词后缀
VERB_SUFFIXES = [
    'ize', 'ise', 'ify', 'ate', 'en', 'fy'
]

# 常见形容词后缀
ADJ_SUFFIXES = [
    'able', 'ible', 'al', 'ial', 'ed', 'ing', 'ful', 'less', 'ous', 'ious',
    'ive', 'ative', 'y', 'ly', 'ic', 'ical', 'ish', 'some'
]

# 常见副词后缀
ADV_SUFFIXES = ['ly', 'ward', 'wards']

# 小学英语常见单词词性映射（手动整理的特殊规则）
SPECIAL_WORDS = {
    # 三年级
    'ruler': 'n.', 'pencil': 'n.', 'eraser': 'n.', 'crayon': 'n.',
    'bag': 'n.', 'pen': 'n.', 'book': 'n.', 'no': 'adv./det.',
    'your': 'pron.', 'red': 'n./adj.', 'green': 'n./adj.',
    'yellow': 'n./adj.', 'blue': 'n./adj.', 'black': 'n./adj.',
    'brown': 'n./adj.', 'white': 'n./adj.', 'orange': 'n./adj.',
    'OK': 'adj./adv.', 'mum': 'n.', 'face': 'n.', 'ear': 'n.',
    'eye': 'n.', 'nose': 'n.', 'mouth': 'n.', 'arm': 'n.',
    'hand': 'n.', 'head': 'n.', 'body': 'n.', 'leg': 'n.',
    'foot': 'n.', 'school': 'n.', 'duck': 'n.', 'pig': 'n.',
    'cat': 'n.', 'bear': 'n.', 'dog': 'n.', 'elephant': 'n.',
    'monkey': 'n.', 'bird': 'n.', 'tiger': 'n.', 'panda': 'n.',
    'zoo': 'n.', 'funny': 'adj.', 'bread': 'n.', 'juice': 'n.',
    'egg': 'n.', 'milk': 'n.', 'water': 'n.', 'cake': 'n.',
    'fish': 'n.', 'rice': 'n.', 'one': 'num.', 'two': 'num.',
    'three': 'num.', 'four': 'num.', 'five': 'num.', 'six': 'num.',
    'seven': 'num.', 'eight': 'num.', 'nine': 'num.', 'ten': 'num.',
    'brother': 'n.', 'plate': 'n.',
    # 常用动词
    'is': 'v.', 'am': 'v.', 'are': 'v.', 'have': 'v.', 'has': 'v.',
    'do': 'v.', 'does': 'v.', 'can': 'v.aux', 'like': 'v.',
    'look': 'v.', 'see': 'v.', 'hear': 'v.', 'touch': 'v.',
    'turn': 'v.', 'go': 'v.', 'come': 'v.', 'eat': 'v.',
    'drink': 'v.', 'draw': 'v.', 'write': 'v.', 'read': 'v.',
    'open': 'v./adj.', 'close': 'v./adj.', 'show': 'v.',
    'welcome': 'v./adj.', 'meet': 'v.', 'let': 'v.',
    'make': 'v.', 'play': 'v./n.', 'help': 'v./n.',
    # 介词和代词
    'I': 'pron.', 'you': 'pron.', 'he': 'pron.', 'she': 'pron.',
    'it': 'pron.', 'we': 'pron.', 'they': 'pron.',
    'my': 'pron.', 'his': 'pron.', 'her': 'pron.', 'its': 'pron.',
    'our': 'pron.', 'their': 'pron.',
    'me': 'pron.', 'him': 'pron.', 'us': 'pron.', 'them': 'pron.',
    'in': 'prep.', 'on': 'prep./adv.', 'at': 'prep.', 'under': 'prep.',
    'near': 'prep./adj.', 'behind': 'prep.', 'next to': 'prep.',
    'to': 'prep.', 'for': 'prep.', 'of': 'prep.', 'with': 'prep.',
    'and': 'conj.', 'but': 'conj.', 'or': 'conj.',
    # 其他常用词
    'this': 'pron./adj.', 'that': 'pron./adj.',
    'these': 'pron./adj.', 'those': 'pron./adj.',
    'what': 'pron./adj.', 'where': 'adv.', 'who': 'pron.',
    'how': 'adv.', 'yes': 'adv.', 'please': 'adv.',
    'thank': 'v.', 'sorry': 'adj.', 'good': 'adj.',
    'great': 'adj.', 'nice': 'adj.', 'fine': 'adj./n.',
    'here': 'adv.', 'there': 'adv.', 'now': 'adv.',
    'today': 'n./adv.', 'welcome': 'v./adj./n.',
}

# 按年级和单元的词性映射（更精确的）
UNIT_SPECIFIC_POS = {
    # 六年级上册 Unit 1 - 问路主题
    (6, '上', 1): {
        'science': 'n.', 'museum': 'n.', 'post office': 'n.',
        'bookstore': 'n.', 'cinema': 'n.', 'hospital': 'n.',
        'crossing': 'n.', 'turn': 'v.', 'left': 'n./adj./adv.',
        'right': 'n./adj./adv.', 'straight': 'adv./adj.',
        'map': 'n.', 'ask': 'v.', 'sir': 'n.', 'interesting': 'adj.',
        'Italian': 'adj./n.', 'restaurant': 'n.', 'pizza': 'n.',
        'street': 'n.', 'get': 'v.', 'BDS': 'abbr.', 'gave': 'v.',
        'feature': 'n.', 'follow': 'v.', 'far': 'adj./adv.',
        'tell': 'v.',
    },
    # 六年级上册 Unit 2 - 交通方式
    (6, '上', 2): {
        'on foot': 'prep.phrase', 'walk': 'v./n.', 'run': 'v.',
        'slow': 'adj.', 'down': 'adv./prep.', 'stop': 'v./n.',
        'train': 'n.', 'bus': 'n.', 'plane': 'n.', 'ship': 'n.',
        'subway': 'n.', 'taxi': 'n.', 'traffic': 'n.', 'light': 'n.',
    },
}

def get_db_connection():
    """创建数据库连接"""
    if DB_USERNAME and DB_PASSWORD:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD}"
        )
    else:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"Trusted_Connection=yes;"
        )
    return pyodbc.connect(conn_str)

def guess_pos_by_suffix(word: str) -> str:
    """根据后缀猜测词性"""
    word_lower = word.lower()

    # 检查动词后缀
    for suffix in VERB_SUFFIXES:
        if word_lower.endswith(suffix):
            return 'v.'

    # 检查名词后缀
    for suffix in NOUN_SUFFIXES:
        if word_lower.endswith(suffix):
            return 'n.'

    # 检查形容词后缀
    for suffix in ADJ_SUFFIXES:
        if word_lower.endswith(suffix):
            return 'adj.'

    # 检查副词后缀
    for suffix in ADV_SUFFIXES:
        if word_lower.endswith(suffix):
            return 'adv.'

    # 默认返回名词（小学英语大部分是名词）
    return 'n.'

def get_pos_for_word(word: str, grade: int = None, semester: str = None, unit_no: int = None) -> str:
    """
    获取单词的词性
    优先级：特殊单词映射 > 单元特定映射 > 后缀规则
    """
    word_lower = word.lower()

    # 1. 检查单元特定映射
    if grade and semester and unit_no:
        unit_key = (grade, semester, unit_no)
        if unit_key in UNIT_SPECIFIC_POS:
            if word_lower in UNIT_SPECIFIC_POS[unit_key]:
                return UNIT_SPECIFIC_POS[unit_key][word_lower]

    # 2. 检查特殊单词映射
    if word_lower in SPECIAL_WORDS:
        return SPECIAL_WORDS[word_lower]
    if word in SPECIAL_WORDS:  # 大写形式
        return SPECIAL_WORDS[word]

    # 3. 根据后缀规则猜测
    return guess_pos_by_suffix(word)

def update_word_pos(conn, word_id: str, pos: str):
    """更新单词的词性"""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_word SET part_of_speech = ? WHERE id = ?
    """, (pos, word_id))
    conn.commit()

def batch_update_pos():
    """批量更新词性"""
    print("=" * 50)
    print("批量词性标注工具")
    print("=" * 50)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询所有需要更新词性的单词
    cursor.execute("""
        SELECT w.id, w.word, gu.grade, gu.semester, gu.unit_no
        FROM tb_word w
        JOIN tb_grade_unit gu ON w.grade_unit_id = gu.id
        WHERE w.part_of_speech IS NULL OR w.part_of_speech = ''
        ORDER BY gu.grade, gu.semester, gu.unit_no, w.sort_order
    """)

    rows = cursor.fetchall()
    total = len(rows)
    print(f"需要更新词性的单词数：{total}")

    updated = 0
    for idx, row in enumerate(rows):
        word_id, word, grade, semester, unit_no = row

        # 获取词性
        pos = get_pos_for_word(word, grade, semester, unit_no)

        # 更新数据库
        update_word_pos(conn, word_id, pos)
        updated += 1

        if (idx + 1) % 100 == 0 or (idx + 1) == total:
            print(f"进度：{idx + 1}/{total} ({(idx + 1) / total * 100:.1f}%)")

    conn.close()
    print(f"\n完成！已更新 {updated} 个单词的词性")
    print("=" * 50)

if __name__ == "__main__":
    batch_update_pos()
