# -*- coding: utf-8 -*-
"""
补充剩余的拼写题、连词成句、匹配题
日期：2026-04-02
"""

import pyodbc
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def get_grade_unit_id(conn, grade, semester, unit_no):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))
    row = cursor.fetchone()
    return row.id if row else None

def insert_question(conn, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tb_question (
                id, grade_unit_id, question_type, difficulty,
                question_stem, correct_answer, answer_analysis, knowledge_point, is_active
            ) VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            grade_unit_id, question_type, difficulty,
            question_stem, correct_answer, answer_analysis, knowledge_point
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

# 补充拼写题 - 还需要 18 个
MORE_SPELLING = [
    ("苹果", "apple", 3, '上', 1),
    ("香蕉", "banana", 3, '上', 2),
    ("橙子", "orange", 3, '上', 3),
    ("书", "book", 3, '上', 4),
    ("笔", "pen", 3, '上', 5),
    ("朋友", "friend", 3, '上', 6),
    ("学校", "school", 3, '下', 1),
    ("家", "home", 3, '下', 2),
    ("桌子", "desk", 3, '下', 3),
    ("椅子", "chair", 3, '下', 4),
    ("窗户", "window", 3, '下', 5),
    ("门", "door", 3, '下', 6),
    ("星期一", "Monday", 4, '上', 1),
    ("星期二", "Tuesday", 4, '上', 2),
    ("星期三", "Wednesday", 4, '上', 3),
    ("星期四", "Thursday", 4, '上', 4),
    ("星期五", "Friday", 4, '上', 5),
    ("星期六", "Saturday", 4, '上', 6),
]

# 连词成句 - 需要 30 个
MORE_ORDERING = [
    ("I, a, have, apple", "I have an apple.", 3, '上', 1),
    ("This, is, banana, a", "This is a banana.", 3, '上', 2),
    ("is, what, your, name", "What is your name?", 3, '上', 3),
    ("old, how, you, are", "How old are you?", 3, '上', 4),
    ("from, where, you, are", "Where are you from?", 3, '上', 5),
    ("cat, the, where, is", "Where is the cat?", 3, '上', 6),
    ("like, you, do, apples", "Do you like apples?", 3, '下', 1),
    ("how, ducks, many, you, see", "How many ducks do you see?", 3, '下', 2),
    ("is, this, my, classroom", "This is my classroom.", 3, '下', 3),
    ("time, what, it, is", "What time is it?", 3, '下', 4),
    ("weather, what's, like, the", "What's the weather like?", 3, '下', 5),
    ("much, how, is, it", "How much is it?", 3, '下', 6),
    ("would, what, like, you", "What would you like?", 4, '上', 1),
    ("your, what's, favourite, food", "What's your favourite food?", 4, '上', 2),
    ("can, what, you, do", "What can you do?", 4, '上', 3),
    ("a, there, is, bed, room, the, in", "There is a bed in the room.", 4, '上', 4),
    ("when, get, do, up, you", "When do you get up?", 4, '上', 5),
    ("which, season, you, best, do, like", "Which season do you like best?", 4, '上', 6),
    ("when, birthday, your, is", "When is your birthday?", 4, '下', 1),
    ("what, doing, they, are", "What are they doing?", 4, '下', 2),
    ("how, I, can, to, get, museum, the", "How can I get to the museum?", 4, '下', 3),
    ("what, you, going, are, to, be", "What are you going to be?", 4, '下', 4),
    ("how, tall, are, you", "How tall are you?", 4, '下', 5),
    ("what, did, you, last, weekend, do", "What did you do last weekend?", 4, '下', 6),
    ("where, you, did, go", "Where did you go?", 5, '上', 1),
    ("what, your, is, hobby", "What is your hobby?", 5, '上', 2),
    ("when, is, Children's Day", "When is Children's Day?", 5, '上', 3),
    ("who, that, man, is", "Who is that man?", 5, '上', 4),
    ("how, you, did, it, do", "How did you do it?", 5, '上', 5),
    ("what, is, your, job", "What is your job?", 5, '上', 6),
]

# 匹配题 - 需要 30 个
MORE_MATCHING = [
    [("cat", "猫"), ("dog", "狗"), ("pig", "猪"), ("bird", "鸟")],
    [("teacher", "老师"), ("student", "学生"), ("friend", "朋友"), ("father", "父亲")],
    [("mother", "母亲"), ("sister", "姐妹"), ("brother", "兄弟"), ("farmer", "农民")],
    [("doctor", "医生"), ("driver", "司机"), ("nurse", "护士"), ("worker", "工人")],
    [("spring", "春天"), ("summer", "夏天"), ("autumn", "秋天"), ("winter", "冬天")],
    [("January", "一月"), ("February", "二月"), ("March", "三月"), ("April", "四月")],
    [("May", "五月"), ("June", "六月"), ("July", "七月"), ("August", "八月")],
    [("September", "九月"), ("October", "十月"), ("November", "十一月"), ("December", "十二月")],
    [("big", "大的"), ("small", "小的"), ("tall", "高的"), ("short", "矮的")],
    [("young", "年轻的"), ("old", "年老的"), ("strong", "强壮的"), ("thin", "瘦的")],
    [("red", "红色"), ("blue", "蓝色"), ("green", "绿色"), ("yellow", "黄色")],
    [("black", "黑色"), ("white", "白色"), ("brown", "棕色"), ("orange", "橙色")],
    [("long", "长的"), ("short", "短的"), ("new", "新的"), ("old", "旧的")],
    [("cold", "冷的"), ("hot", "热的"), ("warm", "温暖的"), ("cool", "凉爽的")],
    [("happy", "开心的"), ("sad", "伤心的"), ("angry", "生气的"), ("tired", "累的")],
    [("eat", "吃"), ("drink", "喝"), ("play", "玩"), ("run", "跑")],
    [("walk", "走"), ("jump", "跳"), ("sing", "唱"), ("dance", "跳舞")],
    [("book", "书"), ("pen", "钢笔"), ("pencil", "铅笔"), ("ruler", "尺子")],
    [("apple", "苹果"), ("banana", "香蕉"), ("orange", "橙子"), ("pear", "梨")],
    [("football", "足球"), ("basketball", "篮球"), ("ping-pong", "乒乓球"), ("tennis", "网球")],
    [("Monday", "周一"), ("Tuesday", "周二"), ("Wednesday", "周三"), ("Thursday", "周四")],
    [("Friday", "周五"), ("Saturday", "周六"), ("Sunday", "周日"), ("weekend", "周末")],
    [("China", "中国"), ("UK", "英国"), ("USA", "美国"), ("Canada", "加拿大")],
    [("east", "东"), ("south", "南"), ("west", "西"), ("north", "北")],
    [("one", "一"), ("two", "二"), ("three", "三"), ("four", "四")],
    [("five", "五"), ("six", "六"), ("seven", "七"), ("eight", "八")],
    [("nine", "九"), ("ten", "十"), ("eleven", "十一"), ("twelve", "十二")],
    [("thirteen", "十三"), ("fourteen", "十四"), ("fifteen", "十五"), ("sixteen", "十六")],
    [("seventeen", "十七"), ("eighteen", "十八"), ("nineteen", "十九"), ("twenty", "二十")],
    [("mother", "妈妈"), ("father", "爸爸"), ("sister", "姐妹"), ("brother", "兄弟")],
]

def main():
    print("=" * 60)
    print("     补充剩余练习题")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    # 当前统计
    cursor = conn.cursor()
    cursor.execute("""
        SELECT question_type, COUNT(*) FROM tb_question
        GROUP BY question_type
    """)
    print("当前题型分布：")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    print()

    success_total = 0
    failed_total = 0

    # 1. 添加拼写题
    print("正在添加拼写题...")
    for word_cn, word_en, grade, semester, unit in MORE_SPELLING:
        guid = get_grade_unit_id(conn, grade, semester, unit)
        if not guid:
            print(f"[NOT FOUND] {grade}年级{semester}册 Unit {unit}")
            failed_total += 1
            continue
        difficulty = 1 if grade < 5 else 2
        if insert_question(conn, guid, 'spell_word', difficulty,
                 f"根据汉语提示，拼写单词：{word_cn}", word_en,
                 f"记住 {word_en} 的拼写", "单词拼写"):
            print(f"[OK] {word_cn} → {word_en}")
            success_total += 1
        else:
            failed_total += 1
        time.sleep(0.8)

    # 2. 添加连词成句
    print("\n正在添加连词成句...")
    for words, answer, grade, semester, unit in MORE_ORDERING:
        guid = get_grade_unit_id(conn, grade, semester, unit)
        if not guid:
            print(f"[NOT FOUND] {grade}年级{semester}册 Unit {unit}")
            failed_total += 1
            continue
        difficulty = 1 if grade < 5 else 2
        if insert_question(conn, guid, 'order_words', difficulty,
                 f"将下列单词连成正确的句子：\n{words}", answer,
                 "注意语序和标点符号", "连词成句"):
            print(f"[OK] {words[:40]}... → {answer}")
            success_total += 1
        else:
            failed_total += 1
        time.sleep(0.8)

    # 3. 添加匹配题
    print("\\n正在添加匹配题...")
    idx = 0
    for grade in [5, 6]:
        for semester in ['上', '下']:
            for unit in range(1, 7):
                if idx >= len(MORE_MATCHING):
                    break
                pairs = MORE_MATCHING[idx]
                difficulty = 1 if grade < 5 else 2
                guid = get_grade_unit_id(conn, grade, semester, unit)
                if not guid:
                    print(f"[NOT FOUND] {grade}年级{semester}册 Unit {unit}")
                    failed_total += 1
                    idx += 1
                    continue

                stem = "将左边单词与右边汉语意思匹配：\n"
                answer = []
                for i, (word, cn) in enumerate(pairs):
                    stem += f"{chr(ord('1') + i)}. {word}     {cn}\n"
                for i, (word, cn) in enumerate(pairs):
                    answer.append(f"{chr(ord('A') + i)}-{chr(ord('1') + i)}")
                answer_str = ", ".join(answer)

                if insert_question(conn, guid, 'match', difficulty, stem, answer_str,
                         "考查单词词义匹配", "单词匹配"):
                    print(f"[OK] {len(pairs)} pairs → Unit {unit}")
                    success_total += 1
                else:
                    failed_total += 1

                idx += 1
                time.sleep(0.8)
                if idx >= 30:
                    break

    # 最终统计
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tb_question")
    total_after = cursor.fetchone()[0]

    cursor.execute("""
        SELECT question_type, COUNT(*) FROM tb_question
        GROUP BY question_type
        ORDER BY COUNT(*) DESC
    """)
    final_stats = list(cursor.fetchall())

    print("\\n" + "=" * 60)
    print("     添加完成!")
    print("=" * 60)
    print(f"  成功添加：{success_total} 道")
    print(f"  失败：{failed_total} 道")
    print(f"  题目总数：{584} → {total_after}")
    print()
    print("  最终题型分布：")
    for t, cnt in final_stats:
        print(f"    {t}: {cnt}")
    print()
    print("  目标检查：")
    for target, need in [('listening', 50), ('spell_word', 50), ('order_words', 30), ('match', 30)]:
        actual = next((cnt for t, cnt in final_stats if t == target), 0)
        done = 'OK' if actual >= need else '--'
        print(f"    {target}: 需要 {need}+ → 实际 {actual} → {done}")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    main()
