# -*- coding: utf-8 -*-
"""
语法知识点和练习题导入工具
日期：2026-04-02
说明：为 3-6 年级每个单元创建语法知识点和练习题
"""

import json
import pyodbc
import uuid
from pathlib import Path

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

def get_grade_unit(conn, grade, semester, unit_no):
    """获取年级单元 ID"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))
    row = cursor.fetchone()
    return row.id if row else None

def insert_grammar(conn, unit_id, title, content_json, sort_order=1):
    """插入语法知识点"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_grammar (grade_unit_id, title, content_type, content_json, duration_seconds, sort_order, passing_score)
        VALUES (?, ?, 'article', ?, NULL, ?, 60)
    """, (unit_id, title, content_json, sort_order))
    conn.commit()
    print(f"  [语法] {title}")

def insert_question(conn, unit_id, q_type, difficulty, stem, correct, analysis, knowledge, options, tags=""):
    """插入题目和选项"""
    question_id = str(uuid.uuid4())
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty,
                                question_stem, correct_answer, answer_analysis,
                                knowledge_point, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (question_id, unit_id, q_type, difficulty, stem, correct, analysis, knowledge, tags))

    for idx, (opt_key, opt_content) in enumerate(options):
        cursor.execute("""
            INSERT INTO tb_question_option (question_id, option_key, option_content, sort_order)
            VALUES (?, ?, ?, ?)
        """, (question_id, opt_key, opt_content, idx + 1))

    conn.commit()

def create_grammar_content(sections):
    """创建语法内容 JSON"""
    return json.dumps({"sections": sections}, ensure_ascii=False)

# ==================== 语法知识点 ====================
GRAMMAR_POINTS = {
    # 三年级上册
    (3, '上', 1): [
        ("问候语", create_grammar_content([
            {"title": "基本问候", "content": "Hello! (你好!)\nHi! (嗨!)\nGood morning! (早上好!)"},
            {"title": "初次见面", "content": "Nice to meet you! (很高兴见到你!)"}
        ])),
        ("自我介绍", create_grammar_content([
            {"title": "介绍自己", "content": "I'm ... (我是...)\nMy name is ... (我的名字是...)"}
        ]))
    ],
    (3, '上', 2): [
        ("身体部位", create_grammar_content([
            {"title": "介绍身体部位", "content": "This is my head. (这是我的头)\nThis is my face. (这是我的脸)"}
        ]))
    ],
    (3, '上', 3): [
        ("颜色表达", create_grammar_content([
            {"title": "询问颜色", "content": "What color is it? (它是什么颜色？)"},
            {"title": "回答颜色", "content": "It's red. (它是红色)\nIt's blue. (它是蓝色)"}
        ]))
    ],
    (3, '上', 4): [
        ("动物名称", create_grammar_content([
            {"title": "描述看到的动物", "content": "I see a cat. (我看见一只猫)\nI see a dog. (我看见一只狗)"}
        ]))
    ],
    (3, '上', 5): [
        ("表达喜好", create_grammar_content([
            {"title": "表达喜欢", "content": "I like apples. (我喜欢苹果)"},
            {"title": "想要某物", "content": "I'd like some bread. (我想要些面包)"}
        ]))
    ],
    (3, '上', 6): [
        ("年龄表达", create_grammar_content([
            {"title": "询问年龄", "content": "How old are you? (你多大了？)"},
            {"title": "回答年龄", "content": "I'm seven. (我七岁)\nHappy birthday! (生日快乐!)"}
        ]))
    ],
    # 四年级上册
    (4, '上', 1): [
        ("位置表达", create_grammar_content([
            {"title": "询问位置", "content": "Where is my pencil? (我的铅笔在哪里？)"},
            {"title": "回答位置", "content": "It's in the classroom. (它在教室里)\nIt's on the desk. (它在书桌上)"}
        ]))
    ],
    (4, '上', 2): [
        ("询问物品", create_grammar_content([
            {"title": "询问内容物", "content": "What's in your schoolbag? (你的书包里有什么？)"}
        ]))
    ],
    # 五年级上册
    (5, '上', 1): [
        ("描述人物", create_grammar_content([
            {"title": "描述人物性格", "content": "He's very kind. (他很和蔼)\nShe's strict. (她很严格)"}
        ]))
    ],
    (5, '上', 2): [
        ("星期表达", create_grammar_content([
            {"title": "星期单词", "content": "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"},
            {"title": "询问课程", "content": "What do you have on Mondays? (你星期一有什么课？)"}
        ]))
    ],
    # 六年级上册
    (6, '上', 1): [
        ("问路句型", create_grammar_content([
            {"title": "核心句型", "content": "How can I get to the museum? (我怎么去博物馆？)"},
            {"title": "指路回答", "content": "Go straight. (直走)\nTurn left. (左转)\nTurn right. (右转)"}
        ])),
        ("方位介词", create_grammar_content([
            {"title": "in/on/next to", "content": "in 在...里面\non 在...上面\nnext to 在...旁边"}
        ]))
    ],
    (6, '上', 2): [
        ("交通方式", create_grammar_content([
            {"title": "by+交通工具", "content": "by bus (乘公交)\nby train (乘火车)\nby plane (乘飞机)"},
            {"title": "询问方式", "content": "How do you go to school? (你怎么去学校？)"}
        ]))
    ],
    (6, '上', 3): [
        ("将来时 be going to", create_grammar_content([
            {"title": "be going to 结构", "content": "be going to + 动词原形，表示计划或打算"},
            {"title": "例句", "content": "I'm going to visit my grandparents. (我要去看望祖父母)"}
        ]))
    ],
}

# ==================== 练习题 ====================
QUESTIONS = {
    (6, '上', 1): [
        ("single_choice", 2, "你想问路去电影院，应该怎么说？", "B", "问路的标准句型是 How can I get to the + 地点", "问路句型", [
            ("A", "Where is the cinema go?"),
            ("B", "How can I get to the cinema?"),
            ("C", "How go to cinema?"),
            ("D", "Where cinema?")
        ]),
        ("single_choice", 2, "「在...旁边」用英语怎么说？", "C", "next to 表示「在...旁边」", "方位介词", [
            ("A", "in front of"),
            ("B", "behind"),
            ("C", "next to"),
            ("D", "under")
        ]),
        ("single_choice", 1, "单词 'museum' 的中文意思是？", "A", "museum 意为博物馆", "词汇记忆", [
            ("A", "博物馆"),
            ("B", "美术馆"),
            ("C", "图书馆"),
            ("D", "电影院")
        ])
    ],
    (6, '上', 2): [
        ("single_choice", 1, "「乘公交车」用英语怎么说？", "B", "用 by 表示交通方式：by bus", "交通方式", [
            ("A", "on bus"),
            ("B", "by bus"),
            ("C", "in bus"),
            ("D", "at bus")
        ]),
        ("single_choice", 2, "How do you go to school? 的正确回答是？", "A", "回答交通方式", "交通方式", [
            ("A", "I go to school by bus."),
            ("B", "I go to school."),
            ("C", "I am going to school."),
            ("D", "I go school by bus.")
        ])
    ],
    (3, '上', 1): [
        ("single_choice", 1, "「你好!」用英语怎么说？", "A", "Hello 是常用问候语", "问候语", [
            ("A", "Hello!"),
            ("B", "Goodbye!"),
            ("C", "Thank you!"),
            ("D", "Sorry!")
        ]),
        ("single_choice", 1, "Nice to meet you! 的合适回答是？", "B", "标准回答是 Nice to meet you, too!", "问候语", [
            ("A", "Hello!"),
            ("B", "Nice to meet you, too!"),
            ("C", "Good morning!"),
            ("D", "How are you?")
        ])
    ],
}

def import_grammar():
    """导入语法知识点"""
    print("=" * 50)
    print("语法知识点导入")
    print("=" * 50)

    conn = get_db_connection()
    total = 0

    for (grade, semester, unit_no), grammars in GRAMMAR_POINTS.items():
        unit_id = get_grade_unit(conn, grade, semester, unit_no)
        if not unit_id:
            continue

        print(f"\n{grade}年级{semester}册 Unit {unit_no}")
        for idx, (title, content) in enumerate(grammars):
            insert_grammar(conn, unit_id, title, content, idx + 1)
            total += 1

    conn.close()
    print(f"\n完成！共导入 {total} 个语法知识点")

def import_questions():
    """导入练习题"""
    print("\n" + "=" * 50)
    print("练习题导入")
    print("=" * 50)

    conn = get_db_connection()
    total = 0

    for (grade, semester, unit_no), questions in QUESTIONS.items():
        unit_id = get_grade_unit(conn, grade, semester, unit_no)
        if not unit_id:
            continue

        print(f"\n{grade}年级{semester}册 Unit {unit_no}")
        for q in questions:
            q_type, diff, stem, correct, analysis, knowledge, options = q
            insert_question(conn, unit_id, q_type, diff, stem, correct, analysis, knowledge, options, "grammar")
            total += 1
            print(f"  [题目] {stem[:30]}...")

    conn.close()
    print(f"\n完成！共导入 {total} 道练习题")

if __name__ == "__main__":
    import_grammar()
    import_questions()
    print("\n" + "=" * 50)
    print("全部完成!")
    print("=" * 50)
