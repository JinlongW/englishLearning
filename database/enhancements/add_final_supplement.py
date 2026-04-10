"""
补充删除重复后缺失的题目
拼写题: 需要 50+，现有 32 → 需要补充 18 道
匹配题: 需要 30+，现有 24 → 需要补充 6 道
"""

import pyodbc
import uuid
import time

def get_db_connection():
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER=localhost;'
        f'DATABASE=EnglishLearning;'
        f'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def get_grade_unit_id(conn, grade: int, semester: str, unit: int):
    """根据年级、学期、单元获取 grade_unit_id"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, grade, semester, unit)
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def insert_question(conn, grade_unit_id, question_type, difficulty, stem, answer, analysis, title):
    """插入一道新题目"""
    question_id = str(uuid.uuid4())
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO tb_question (
                id, grade_unit_id, question_type, difficulty,
                question_stem, correct_answer, answer_analysis, knowledge_point,
                is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
        """
        cursor.execute(sql, (
            question_id, grade_unit_id, question_type, difficulty,
            stem, answer, analysis, title
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"  [ERROR] {stem[:30]}: {e}")
        conn.rollback()
        return False

# 补充拼写题 - 18 道
SPELL_WORDS = [
    # 三年级上册
    (3, '上', 2, "apple", "苹果"),
    (3, '上', 2, "banana", "香蕉"),
    (3, '上', 2, "orange", "橙子"),
    (3, '上', 3, "book", "书"),
    (3, '上', 3, "pen", "钢笔"),
    (3, '上', 3, "friend", "朋友"),
    (3, '上', 4, "school", "学校"),
    (3, '上', 4, "home", "家"),
    (3, '上', 4, "desk", "书桌"),
    (3, '上', 4, "chair", "椅子"),
    (3, '上', 5, "window", "窗户"),
    (3, '上', 5, "door", "门"),
    (3, '上', 6, "Monday", "星期一"),
    (3, '上', 6, "Tuesday", "星期二"),
    (3, '上', 6, "Wednesday", "星期三"),
    (3, '上', 6, "Thursday", "星期四"),
    (3, '上', 6, "Friday", "星期五"),
    (3, '上', 6, "Saturday", "星期六"),
]

# 补充匹配题 - 6 组
MATCHING_SUPPLY = [
    # 三年级下册
    3, '下', [
        [("one", "一"), ("two", "二"), ("three", "三"), ("four", "四")],
        [("five", "五"), ("six", "六"), ("seven", "七"), ("eight", "八")],
        [("nine", "九"), ("ten", "十"), ("eleven", "十一"), ("twelve", "十二")],
        [("thirteen", "十三"), ("fourteen", "十四"), ("fifteen", "十五"), ("sixteen", "十六")],
        [("seventeen", "十七"), ("eighteen", "十八"), ("nineteen", "十九"), ("twenty", "二十")],
        [("mother", "妈妈"), ("father", "爸爸"), ("sister", "姐妹"), ("brother", "兄弟")],
    ]
]

def main():
    conn = get_db_connection()
    print("=" * 60)
    print("补充删除重复后缺失的题目")
    print("=" * 60)

    success = 0
    total = 0

    # 添加拼写题
    print("\n补充拼写题...")
    for grade, semester, unit, word, meaning in SPELL_WORDS:
        guid = get_grade_unit_id(conn, grade, semester, unit)
        if not guid:
            print(f"  [SKIP] 找不到单元: {grade}{semester} 单元{unit}")
            continue
        stem = f"根据汉语写出英语单词：\n{meaning}"
        if insert_question(conn, guid, 'spell_word', 2, stem, word,
                         f"正确拼写是 {word}", "单词拼写"):
            print(f"  [OK] {meaning} - {word}")
            success += 1
        total += 1
        time.sleep(0.2)

    # 添加匹配题
    print("\n补充匹配题...")
    grade = MATCHING_SUPPLY[0]
    semester = MATCHING_SUPPLY[1]
    match_list = MATCHING_SUPPLY[2]
    unit_no = 1
    for pairs in match_list:
        guid = get_grade_unit_id(conn, grade, semester, unit_no)
        if not guid:
            print(f"  [SKIP] 找不到单元: {grade}{semester} 单元{unit_no}")
            unit_no += 1
            continue
        stem = "将左边的单词与右边的汉语意思匹配：\n"
        answer = []
        for idx, (word, cn) in enumerate(pairs, 1):
            stem += f"{idx}. {word}     {cn}\n"
            answer.append(f"{word}-{cn}")
        answer_str = "\n".join(answer)
        if insert_question(conn, guid, 'match', 2, stem, answer_str,
                         "考查单词词义匹配", "单词匹配"):
            print(f"  [OK] {len(pairs)} pairs - Unit {unit_no}")
            success += 1
        total += 1
        unit_no += 1
        time.sleep(0.2)

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
    print(f"  成功: {success} / {total}")

    # 最终统计
    cursor = conn.cursor()
    print("\n  当前题型分布：")
    cursor.execute("SELECT question_type, COUNT(*) FROM tb_question GROUP BY question_type")
    for qtype, cnt in cursor.fetchall():
        print(f"    {qtype}: {cnt}")

    conn.close()

if __name__ == "__main__":
    main()
