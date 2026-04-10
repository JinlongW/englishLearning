"""
语法知识点和练习题导入工具
日期：2026-04-02
说明：为 3-6 年级每个单元创建语法知识点和练习题
"""

import json
import pyodbc
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# ==================== 配置区域 ====================
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"
DB_USERNAME = ""  # Windows 集成认证
DB_PASSWORD = ""

# ==================== 语法知识点库 ====================
# 按年级和单元的语法知识点
GRAMMAR_POINTS = {
    # 三年级上册
    (3, '上', 1): [
        {
            "title": "问候语 - Hello! Hi! Good morning!",
            "content_json": json.dumps({
                "sections": [
                    {"title": "基本问候", "content": "英语中常用的问候语有：\n• Hello! (你好!)\n• Hi! (嗨!)\n• Good morning! (早上好!)\n• Good afternoon! (下午好!)\n• Good evening! (晚上好!)"},
                    {"title": "初次见面", "content": "初次见面时可以说：\n• Nice to meet you! (很高兴见到你!)\n• Glad to meet you! (很高兴认识你!)"},
                    {"title": "回答问候", "content": "回应问候时可以说：\n• Hello! / Hi!\n• Nice to meet you, too! (我也很高兴见到你!)"}
                ]
            }, ensure_ascii=False),
            "sort_order": 1
        },
        {
            "title": "自我介绍 - I'm... My name is...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "介绍自己", "content": "介绍自己时可以说：\n• I'm ... (我是...)\n• My name is ... (我的名字是...)"},
                    {"title": "询问对方", "content": "询问对方名字可以说：\n• What's your name? (你叫什么名字？)"}
                ]
            }, ensure_ascii=False),
            "sort_order": 2
        }
    ],
    (3, '上', 2): [
        {
            "title": "身体部位 - This is my...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "介绍身体部位", "content": "介绍身体部位：\n• This is my head. (这是我的头)\n• This is my face. (这是我的脸)\n• These are my eyes. (这些是我的眼睛)"},
                    {"title": "Touch 游戏", "content": "听指令做动作：\n• Touch your nose! (摸摸你的鼻子!)\n• Touch your ear! (摸摸你的耳朵!)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (3, '上', 3): [
        {
            "title": "颜色表达 - It's red/blue/green...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "询问颜色", "content": "询问颜色：\n• What color is it? (它是什么颜色？)"},
                    {"title": "回答颜色", "content": "回答颜色：\n• It's red. (它是红色)\n• It's blue. (它是蓝色)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (3, '上', 4): [
        {
            "title": "动物名称 - I see a...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "描述看到的动物", "content": "描述看到的动物：\n• I see a cat. (我看见一只猫)\n• I see a dog. (我看见一只狗)"},
                    {"title": "模仿动物声音", "content": "模仿动物：\n• It goes 'meow meow' (喵喵叫)\n• It goes 'woof woof' (汪汪叫)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (3, '上', 5): [
        {
            "title": "表达喜好 - I like... / I'd like...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "表达喜欢", "content": "表达喜欢的食物：\n• I like apples. (我喜欢苹果)\n• I like rice. (我喜欢米饭)"},
                    {"title": "想要某物", "content": "表达想要：\n• I'd like some bread, please. (我想要些面包)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (3, '上', 6): [
        {
            "title": "年龄表达 - How old are you? I'm...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "询问年龄", "content": "询问年龄：\n• How old are you? (你多大了？)"},
                    {"title": "回答年龄", "content": "回答年龄：\n• I'm seven. (我七岁)\n• I'm eight years old. (我八岁)"},
                    {"title": "生日祝福", "content": "生日祝福：\n• Happy birthday! (生日快乐!)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    # 四年级上册
    (4, '上', 1): [
        {
            "title": "教室物品 - Where is...? It's in/on/under...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "询问位置", "content": "询问物品位置：\n• Where is my pencil? (我的铅笔在哪里？)"},
                    {"title": "回答位置", "content": "用介词回答：\n• It's in the classroom. (它在教室里)\n• It's on the desk. (它在书桌上)\n• It's under the chair. (它在椅子下面)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (4, '上', 2): [
        {
            "title": "询问物品 - What's in your schoolbag?",
            "content_json": json.dumps({
                "sections": [
                    {"title": "询问内容物", "content": "询问包里有什么：\n• What's in your schoolbag? (你的书包里有什么？)"},
                    {"title": "回答内容物", "content": "回答：\n• I have a book and two pens. (我有一本书和两支钢笔)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    # 五年级上册
    (5, '上', 1): [
        {
            "title": "描述人物性格 - He's/She's kind/strict/funny...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "描述人物", "content": "用形容词描述人物：\n• He's very kind. (他很和蔼)\n• She's strict. (她很严格)\n• He's funny. (他很滑稽)"},
                    {"title": "询问人物特征", "content": "询问：\n• What's he like? (他是什么样的人？)\n• Is she strict? (她严格吗？)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (5, '上', 2): [
        {
            "title": "星期表达 - What do you have on Mondays?",
            "content_json": json.dumps({
                "sections": [
                    {"title": "星期单词", "content": "星期的表达：\n• Monday (星期一)\n• Tuesday (星期二)\n• Wednesday (星期三)\n• Thursday (星期四)\n• Friday (星期五)\n• Saturday (星期六)\n• Sunday (星期日)"},
                    {"title": "询问课程", "content": "询问课程安排：\n• What do you have on Mondays? (你星期一有什么课？)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    # 六年级上册
    (6, '上', 1): [
        {
            "title": "问路句型 - How can I get to...?",
            "content_json": json.dumps({
                "sections": [
                    {"title": "基本句型", "content": "问路是日常生活中很实用的英语技能。我们来学习几个常用的问路句型。"},
                    {"title": "核心句型", "content": "How can I get to the + 地点？\n\n例如：\n• How can I get to the museum? (我怎么去博物馆？)\n• How can I get to the post office? (我怎么去邮局？)"},
                    {"title": "其他问路表达", "content": "1. Where is the...? (请问...在哪里？)\n2. Can you tell me the way to...? (你能告诉我去...的路吗？)\n3. Is there a... near here? (这附近有...吗？)"},
                    {"title": "指路回答", "content": "• Go straight. (直走)\n• Turn left. (左转)\n• Turn right. (右转)\n• It's on your left/right. (它在你的左边/右边)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        },
        {
            "title": "方位介词 - in, on, at, next to, behind",
            "content_json": json.dumps({
                "sections": [
                    {"title": "方位介词用法", "content": "方位介词用来描述物体或地点之间的位置关系。"},
                    {"title": "in - 在...里面", "content": "in 表示在某个空间或范围的内部\n\n例句：\n• The book is in the bag. (书在包里。)\n• She lives in Beijing. (她住在北京。)"},
                    {"title": "on - 在...上面", "content": "on 表示在某物体的表面上\n\n例句：\n• The cup is on the table. (杯子在桌子上。)\n• There is a picture on the wall. (墙上有一幅画。)"},
                    {"title": "next to - 在...旁边", "content": "next to 表示紧挨着、靠近\n\n例句：\n• The bank is next to the supermarket. (银行在超市旁边。)\n• Sit next to me. (坐我旁边。)"},
                    {"title": "behind - 在...后面", "content": "behind 表示在某物后面\n\n例句：\n• The cat is behind the door. (猫在门后面。)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 2
        }
    ],
    (6, '上', 2): [
        {
            "title": "交通方式 - by bus/train/plane...",
            "content_json": json.dumps({
                "sections": [
                    {"title": "交通方式表达", "content": "用 by 表示交通方式：\n• by bus (乘公交车)\n• by train (乘火车)\n• by plane (乘飞机)\n• by ship (乘船)\n• by subway (乘地铁)"},
                    {"title": "步行", "content": "步行用 on foot：\n• I go to school on foot. (我步行去学校)"},
                    {"title": "询问交通方式", "content": "询问：\n• How do you go to school? (你怎么去学校？)"},
                    {"title": "回答交通方式", "content": "回答：\n• I go to school by bus. (我乘公交车去学校)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
    (6, '上', 3): [
        {
            "title": "将来时 be going to - 计划和打算",
            "content_json": json.dumps({
                "sections": [
                    {"title": "be going to 结构", "content": "be going to + 动词原形，表示计划或打算做某事"},
                    {"title": "肯定句", "content": "• I'm going to visit my grandparents. (我要去看望我的祖父母)\n• She's going to buy a book. (她打算买一本书)"},
                    {"title": "否定句", "content": "• I'm not going to go out. (我不打算出去)"},
                    {"title": "疑问句", "content": "• Are you going to watch TV? (你打算看电视吗？)\n• What are you going to do? (你打算做什么？)"}
                ]
            }, ensure_ascii=False)),
            "sort_order": 1
        }
    ],
}

# ==================== 练习题题库 ====================
QUESTION_TEMPLATES = {
    # 词汇题模板
    "vocabulary_choice": {
        "type": "single_choice",
        "difficulty": 1,
        "stem_template": '单词 "{word}" 的中文意思是？',
        "options_generator": "generate_vocab_options",
        "knowledge_point": "词汇记忆"
    },
    # 选择题 - 中文选英文
    "chinese_to_english": {
        "type": "single_choice",
        "difficulty": 2,
        "stem_template": "{meaning_cn} 用英语怎么说？",
        "options_generator": "generate_meaning_options",
        "knowledge_point": "词汇运用"
    },
    # 听力题（模拟）
    "listening_choice": {
        "type": "listening",
        "difficulty": 2,
        "stem_template": '听录音，选择正确的答案：(播放 "{word}" 的录音)',
        "options_generator": "generate_vocab_options",
        "knowledge_point": "听力理解"
    },
    # 语法选择题
    "grammar_choice": {
        "type": "single_choice",
        "difficulty": 2,
        "stem_template": "{stem}",
        "options_generator": "generate_grammar_options",
        "knowledge_point": "语法运用"
    },
}

# 语法练习题
GRAMMAR_QUESTIONS = {
    (6, '上', 1): [
        {
            "question_type": "single_choice",
            "difficulty": 2,
            "question_stem": "你想问路去电影院，应该怎么说？",
            "options": [
                ("A", "Where is the cinema go?"),
                ("B", "How can I get to the cinema?"),
                ("C", "How go to cinema?"),
                ("D", "Where cinema?")
            ],
            "correct_answer": "B",
            "analysis": "问路的标准句型是 \"How can I get to the + 地点？\""
        },
        {
            "question_type": "single_choice",
            "difficulty": 2,
            "question_stem": "「在...旁边」用英语怎么说？",
            "options": [
                ("A", "in front of"),
                ("B", "behind"),
                ("C", "next to"),
                ("D", "under")
            ],
            "correct_answer": "C",
            "analysis": "next to 表示「在...旁边」"
        }
    ],
    (6, '上', 2): [
        {
            "question_type": "single_choice",
            "difficulty": 1,
            "question_stem": "「乘公交车」用英语怎么说？",
            "options": [
                ("A", "on bus"),
                ("B", "by bus"),
                ("C", "in bus"),
                ("D", "at bus")
            ],
            "correct_answer": "B",
            "analysis": "用 by 表示交通方式：by bus"
        }
    ],
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

def get_grade_unit(conn, grade: int, semester: str, unit_no: int):
    """获取年级单元 ID"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))
    row = cursor.fetchone()
    return row.id if row else None

def insert_grammar(conn, unit_id: str, title: str, content_json: str, sort_order: int = 1):
    """插入语法知识点"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_grammar (grade_unit_id, title, content_type, content_json, duration_seconds, sort_order, passing_score)
        VALUES (?, 'article', ?, ?, NULL, ?, 60)
    """, (unit_id, title, content_json, sort_order))
    conn.commit()
    print(f"  ✓ 已插入语法：{title}")

def insert_question(conn, unit_id: str, q_type: str, difficulty: int, stem: str,
                   correct: str, analysis: str, knowledge: str,
                   options: List[tuple], tags: str = ""):
    """插入题目和选项"""
    question_id = str(uuid.uuid4())
    cursor = conn.cursor()

    # 插入题目
    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty,
                                question_stem, correct_answer, answer_analysis,
                                knowledge_point, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (question_id, unit_id, q_type, difficulty, stem, correct, analysis, knowledge, tags))

    # 插入选项
    for idx, (opt_key, opt_content) in enumerate(options):
        cursor.execute("""
            INSERT INTO tb_question_option (question_id, option_key, option_content, sort_order)
            VALUES (?, ?, ?, ?)
        """, (question_id, opt_key, opt_content, idx + 1))

    conn.commit()

def import_grammar_points():
    """导入语法知识点"""
    print("=" * 50)
    print("语法知识点导入工具")
    print("=" * 50)

    conn = get_db_connection()
    total = 0

    for (grade, semester, unit_no), grammars in GRAMMAR_POINTS.items():
        unit_id = get_grade_unit(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"⚠ 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
            continue

        print(f"\n处理：{grade}年级{semester}册 Unit {unit_no}")
        for grammar in grammars:
            insert_grammar(
                conn,
                unit_id,
                grammar["title"],
                grammar["content_json"],
                grammar["sort_order"]
            )
            total += 1

    conn.close()
    print(f"\n完成！共导入 {total} 个语法知识点")
    print("=" * 50)

def import_questions():
    """导入练习题"""
    print("=" * 50)
    print("练习题导入工具")
    print("=" * 50)

    conn = get_db_connection()
    total = 0

    for (grade, semester, unit_no), questions in GRAMMAR_QUESTIONS.items():
        unit_id = get_grade_unit(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"⚠ 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
            continue

        print(f"\n处理：{grade}年级{semester}册 Unit {unit_no}")
        for q in questions:
            insert_question(
                conn,
                unit_id,
                q["question_type"],
                q["difficulty"],
                q["question_stem"],
                q["correct_answer"],
                q["analysis"],
                q["knowledge_point"],
                q["options"],
                "grammar"
            )
            total += 1
            print(f"  ✓ 已插入题目：{q['question_stem'][:30]}...")

    conn.close()
    print(f"\n完成！共导入 {total} 道练习题")
    print("=" * 50)

if __name__ == "__main__":
    import_grammar_points()
    print("\n")
    import_questions()
