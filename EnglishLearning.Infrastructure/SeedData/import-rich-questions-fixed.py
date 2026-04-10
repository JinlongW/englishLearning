#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 丰富练习题导入工具
为每个单元添加 10 道高质量题目，包含多种题型
"""

import pyodbc
import json
import sys
from datetime import datetime

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

def get_unit_id(conn, grade, semester, unit_no):
    """获取单元 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def insert_question(conn, grade_unit_id, question_type, difficulty, question_stem, correct_answer,
                   answer_analysis, knowledge_point, tags, stem_audio_url=None):
    """插入题目"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem,
                                stem_audio_url, correct_answer, answer_analysis, knowledge_point,
                                tags, is_active, created_at, updated_at)
        VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
    """, grade_unit_id, question_type, difficulty, question_stem, stem_audio_url,
        correct_answer, answer_analysis, knowledge_point, tags)
    conn.commit()

    cursor.execute("""
        SELECT TOP 1 id FROM tb_question
        WHERE grade_unit_id = ? AND question_stem = ?
        ORDER BY created_at DESC
    """, (grade_unit_id, question_stem))
    row = cursor.fetchone()
    return row.id if row else None

def insert_question_option(conn, question_id, option_key, option_content, sort_order):
    """插入题目选项"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_question_option (id, question_id, option_key, option_content, sort_order)
        VALUES (NEWID(), ?, ?, ?, ?)
    """, question_id, option_key, option_content, sort_order)
    conn.commit()

# ========== 三年级上册 Unit 1 完整题目 ==========
GRADE3_VOL1_UNIT1_QUESTIONS = [
    # 单选题 - 词汇
    {
        "type": "single_choice",
        "difficulty": 1,
        "stem": "下列哪个单词的意思是"尺子"？",
        "answer": "A",
        "analysis": "ruler 的意思是尺子。pencil 是铅笔，eraser 是橡皮，crayon 是蜡笔。",
        "knowledge_point": "文具词汇",
        "tags": "vocabulary,school_supplies",
        "options": [
            {"key": "A", "text": "ruler"},
            {"key": "B", "text": "pencil"},
            {"key": "C", "text": "eraser"},
            {"key": "D", "text": "crayon"}
        ]
    },
    # 单选题 - 问候语
    {
        "type": "single_choice",
        "difficulty": 1,
        "stem": "当你第一次见到新同学时，你应该说：",
        "answer": "A",
        "analysis": "Hello! I'm... 是初次见面的标准问候语。",
        "knowledge_point": "问候语",
        "tags": "greeting,speaking",
        "options": [
            {"key": "A", "text": "Hello! I'm Mike."},
            {"key": "B", "text": "Goodbye!"},
            {"key": "C", "text": "Thank you!"},
            {"key": "D", "text": "Sorry."}
        ]
    },
    # 单选题 - 情景对话
    {
        "type": "single_choice",
        "difficulty": 2,
        "stem": "— Hello! I'm Sarah.\n— _____________",
        "answer": "B",
        "analysis": "当别人自我介绍时，你也应该自我介绍作为回应。",
        "knowledge_point": "对话应答",
        "tags": "dialogue,responding",
        "options": [
            {"key": "A", "text": "Goodbye!"},
            {"key": "B", "text": "Hi! I'm Chen Jie."},
            {"key": "C", "text": "OK!"},
            {"key": "D", "text": "Bye!"}
        ]
    },
    # 填空题 - 单词拼写
    {
        "type": "fill_blank",
        "difficulty": 2,
        "stem": "根据中文提示，填写单词：I have a ______ (尺子).",
        "answer": "ruler",
        "analysis": "尺子的英文是 ruler。",
        "knowledge_point": "单词拼写",
        "tags": "spelling,vocabulary"
    },
    # 听力题（模拟）
    {
        "type": "listening",
        "difficulty": 2,
        "stem": "听录音，选择正确的单词：(录音内容：pencil)",
        "answer": "B",
        "analysis": "录音中说的是 pencil（铅笔）。",
        "knowledge_point": "听力理解",
        "tags": "listening,vocabulary",
        "stem_audio_url": "audio/unit1/pencil.mp3",
        "options": [
            {"key": "A", "text": "ruler"},
            {"key": "B", "text": "pencil"},
            {"key": "C", "text": "eraser"},
            {"key": "D", "text": "book"}
        ]
    },
]

# ========== 各单元题目模板 ==========

def generate_vocabulary_questions(unit_words, knowledge_point):
    """生成词汇类题目"""
    questions = []

    # 单词释义选择题
    if len(unit_words) >= 2:
        questions.append({
            "type": "single_choice",
            "difficulty": 1,
            "stem": f"单词\"{unit_words[0][0]}\"的中文意思是：",
            "answer": "A",
            "analysis": f"{unit_words[0][0]} 的意思是{unit_words[0][2]}。",
            "knowledge_point": knowledge_point,
            "tags": "vocabulary,meaning",
            "options": [
                {"key": "A", "text": unit_words[0][2]},
                {"key": "B", "text": unit_words[1][2] if len(unit_words) > 1 else "错误选项"},
                {"key": "C", "text": "以上都不是"},
                {"key": "D", "text": "以上都是"}
            ]
        })

    return questions

def generate_dialogue_questions(topic, examples):
    """生成情景对话题目"""
    questions = []

    questions.append({
        "type": "single_choice",
        "difficulty": 2,
        "stem": f"— {examples[0]}\n— _____________",
        "answer": "A",
        "analysis": "这是关于" + topic + "的标准对话。",
        "knowledge_point": topic,
        "tags": "dialogue,speaking",
        "options": [
            {"key": "A", "text": examples[1] if len(examples) > 1 else "回答示例"},
            {"key": "B", "text": "Goodbye!"},
            {"key": "C", "text": "Thank you!"},
            {"key": "D", "text": "OK!"}
        ]
    })

    return questions

def generate_grammar_questions(grammar_point, examples):
    """生成语法类题目"""
    questions = []

    questions.append({
        "type": "single_choice",
        "difficulty": 2,
        "stem": f"选择正确的句子：",
        "answer": "A",
        "analysis": examples[0] if examples else "语法要点说明。",
        "knowledge_point": grammar_point,
        "tags": "grammar,application",
        "options": [
            {"key": "A", "text": examples[0] if examples else "正确句子示例"},
            {"key": "B", "text": "错误句子示例 1"},
            {"key": "C", "text": "错误句子示例 2"},
            {"key": "D", "text": "错误句子示例 3"}
        ]
    })

    return questions

# ========== 各年级典型单元题目数据 ==========

ALL_QUESTIONS_DATA = {
    # 三年级上册
    (3, "上", 1): {
        "words": [("ruler", "尺子"), ("pencil", "铅笔"), ("eraser", "橡皮"), ("crayon", "蜡笔"), ("book", "书")],
        "questions": [
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "下列哪个单词的意思是"尺子"？",
                "answer": "A",
                "analysis": "ruler 的意思是尺子。pencil 是铅笔，eraser 是橡皮，crayon 是蜡笔。",
                "knowledge_point": "文具词汇",
                "tags": "vocabulary,school_supplies",
                "options": [
                    {"key": "A", "text": "ruler"},
                    {"key": "B", "text": "pencil"},
                    {"key": "C", "text": "eraser"},
                    {"key": "D", "text": "crayon"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "— Hello! I'm Mike.\n— _____________",
                "answer": "B",
                "analysis": "当别人说 Hello 自我介绍时，你也应该回应 Hi/Hello 并自我介绍。",
                "knowledge_point": "问候语 Hello/Hi",
                "tags": "greeting,dialogue",
                "options": [
                    {"key": "A", "text": "Goodbye!"},
                    {"key": "B", "text": "Hi! I'm Sarah."},
                    {"key": "C", "text": "Thank you!"},
                    {"key": "D", "text": "OK!"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "当你想让别人看你的新书包时，你应该说：",
                "answer": "A",
                "analysis": "Look at my... 用于让别人看自己的东西。",
                "knowledge_point": "Look at 句型",
                "tags": "speaking,application",
                "options": [
                    {"key": "A", "text": "Look at my new bag!"},
                    {"key": "B", "text": "This is my bag."},
                    {"key": "C", "text": "I have a bag."},
                    {"key": "D", "text": "Where is my bag?"}
                ]
            },
            {
                "type": "fill_blank",
                "difficulty": 2,
                "stem": "根据中文提示，填写单词：I have a ______ (尺子).",
                "answer": "ruler",
                "analysis": "尺子的英文是 ruler。",
                "knowledge_point": "单词拼写",
                "tags": "spelling,vocabulary"
            },
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "— I have a book.\n— _____________",
                "answer": "A",
                "analysis": "Me too! 表示"我也是"，用于回应别人说自己有的东西自己也有。",
                "knowledge_point": "Me too 句型",
                "tags": "dialogue,responding",
                "options": [
                    {"key": "A", "text": "Me too!"},
                    {"key": "B", "text": "OK!"},
                    {"key": "C", "text": "Bye!"},
                    {"key": "D", "text": "Hello!"}
                ]
            },
        ]
    },
    # 三年级上册 Unit 3 颜色
    (3, "上", 3): {
        "words": [("red", "红色"), ("yellow", "黄色"), ("green", "绿色"), ("blue", "蓝色"), ("black", "黑色")],
        "questions": [
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "苹果是什么颜色的？",
                "answer": "A",
                "analysis": "苹果通常是红色的 (red)。",
                "knowledge_point": "颜色形容词",
                "tags": "vocabulary,colors",
                "options": [
                    {"key": "A", "text": "red"},
                    {"key": "B", "text": "blue"},
                    {"key": "C", "text": "green"},
                    {"key": "D", "text": "yellow"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "天空是什么颜色的？",
                "answer": "B",
                "analysis": "天空通常是蓝色的 (blue)。",
                "knowledge_point": "颜色形容词",
                "tags": "vocabulary,colors",
                "options": [
                    {"key": "A", "text": "red"},
                    {"key": "B", "text": "blue"},
                    {"key": "C", "text": "yellow"},
                    {"key": "D", "text": "black"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— Let's paint! \n— OK! I have ______ (红色的蜡笔).",
                "answer": "A",
                "analysis": "红色的英文是 red。",
                "knowledge_point": "颜色词汇",
                "tags": "vocabulary,application",
                "options": [
                    {"key": "A", "text": "red crayon"},
                    {"key": "B", "text": "blue crayon"},
                    {"key": "C", "text": "green crayon"},
                    {"key": "D", "text": "yellow crayon"}
                ]
            },
            {
                "type": "fill_blank",
                "difficulty": 2,
                "stem": "The grass (草地) is ______ (绿色的).",
                "answer": "green",
                "analysis": "绿色的英文是 green。",
                "knowledge_point": "颜色词汇",
                "tags": "spelling,colors"
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "香蕉 (banana) 是什么颜色的？",
                "answer": "D",
                "analysis": "香蕉是黄色的 (yellow)。",
                "knowledge_point": "颜色形容词",
                "tags": "vocabulary,colors",
                "options": [
                    {"key": "A", "text": "red"},
                    {"key": "B", "text": "blue"},
                    {"key": "C", "text": "green"},
                    {"key": "D", "text": "yellow"}
                ]
            },
        ]
    },
    # 四年级上册 Unit 1 教室
    (4, "上", 1): {
        "words": [("classroom", "教室"), ("window", "窗户"), ("blackboard", "黑板"), ("light", "灯"), ("picture", "图画")],
        "questions": [
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "We study (学习) in the ______.",
                "answer": "A",
                "analysis": "classroom 是教室的意思。",
                "knowledge_point": "教室物品词汇",
                "tags": "vocabulary,school",
                "options": [
                    {"key": "A", "text": "classroom"},
                    {"key": "B", "text": "window"},
                    {"key": "C", "text": "blackboard"},
                    {"key": "D", "text": "light"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— ______ is in the classroom?\n— A blackboard, many desks and chairs.",
                "answer": "A",
                "analysis": "What's 是 What is 的缩写，用于询问"有什么"。",
                "knowledge_point": "There be 句型",
                "tags": "grammar,question",
                "options": [
                    {"key": "A", "text": "What's"},
                    {"key": "B", "text": "Where's"},
                    {"key": "C", "text": "Who's"},
                    {"key": "D", "text": "How's"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— Let's clean the classroom!\n— _____________",
                "answer": "A",
                "analysis": "Good idea! 表示同意对方的建议。",
                "knowledge_point": "建议句型",
                "tags": "dialogue,responding",
                "options": [
                    {"key": "A", "text": "Good idea!"},
                    {"key": "B", "text": "Thank you!"},
                    {"key": "C", "text": "You're welcome."},
                    {"key": "D", "text": "Excuse me."}
                ]
            },
            {
                "type": "fill_blank",
                "difficulty": 2,
                "stem": "There ______ (be) a computer in my classroom.",
                "answer": "is",
                "analysis": "There be 句型中，a computer 是单数，所以用 is。",
                "knowledge_point": "There be 句型",
                "tags": "grammar,be_verbs"
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "The ______ (灯) is on the ceiling (天花板).",
                "answer": "B",
                "analysis": "light 是灯的意思。",
                "knowledge_point": "教室物品词汇",
                "tags": "vocabulary,school",
                "options": [
                    {"key": "A", "text": "window"},
                    {"key": "B", "text": "light"},
                    {"key": "C", "text": "picture"},
                    {"key": "D", "text": "door"}
                ]
            },
        ]
    },
    # 五年级上册 Unit 1 描述人物
    (5, "上", 1): {
        "words": [("old", "老的"), ("young", "年轻的"), ("funny", "滑稽的"), ("kind", "和蔼的"), ("strict", "严厉的")],
        "questions": [
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "— Is your teacher young?\n— Yes, ______ is.",
                "answer": "A",
                "analysis": "teacher 可以用 he 或 she 来指代，根据上下文选择。",
                "knowledge_point": "人称代词",
                "tags": "grammar,pronouns",
                "options": [
                    {"key": "A", "text": "he"},
                    {"key": "B", "text": "she"},
                    {"key": "C", "text": "it"},
                    {"key": "D", "text": "they"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "Miss White is very ______. She always smiles (微笑).",
                "answer": "A",
                "analysis": "总是微笑的老师是和蔼的 (kind)。",
                "knowledge_point": "描述人物性格",
                "tags": "vocabulary,description",
                "options": [
                    {"key": "A", "text": "kind"},
                    {"key": "B", "text": "strict"},
                    {"key": "C", "text": "angry"},
                    {"key": "D", "text": "sad"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— What's he like?\n— _____________",
                "answer": "A",
                "analysis": "What's he like? 询问人的性格或特点，回答用形容词。",
                "knowledge_point": "What's ... like 句型",
                "tags": "grammar,question",
                "options": [
                    {"key": "A", "text": "He's tall and strong."},
                    {"key": "B", "text": "He likes apples."},
                    {"key": "C", "text": "He is a teacher."},
                    {"key": "D", "text": "He has short hair."}
                ]
            },
            {
                "type": "fill_blank",
                "difficulty": 2,
                "stem": "Mr Jones is very ______ (严格的).",
                "answer": "strict",
                "analysis": "严格的英文是 strict。",
                "knowledge_point": "形容词词汇",
                "tags": "spelling,description"
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— Who is your math teacher?\n— Mr Zhang. He is ______ (很风趣).",
                "answer": "A",
                "analysis": "funny 是风趣、滑稽的意思。",
                "knowledge_point": "描述人物性格",
                "tags": "vocabulary,description",
                "options": [
                    {"key": "A", "text": "funny"},
                    {"key": "B", "text": "strict"},
                    {"key": "C", "text": "quiet"},
                    {"key": "D", "text": "shy"}
                ]
            },
        ]
    },
    # 六年级上册 Unit 1 问路指路
    (6, "上", 1): {
        "words": [("museum", "博物馆"), ("post office", "邮局"), ("bookstore", "书店"), ("cinema", "电影院"), ("hospital", "医院")],
        "questions": [
            {
                "type": "single_choice",
                "difficulty": 1,
                "stem": "— Where is the museum shop?\n— It's ______ (在旁边) the museum.",
                "answer": "A",
                "analysis": "next to 是在...旁边的意思。",
                "knowledge_point": "方位介词",
                "tags": "vocabulary,location",
                "options": [
                    {"key": "A", "text": "next to"},
                    {"key": "B", "text": "near to"},
                    {"key": "C", "text": "next"},
                    {"key": "D", "text": "near of"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— How can I get to the post office?\n— Turn right ______ the crossing.",
                "answer": "A",
                "analysis": "at the crossing 表示在十字路口。",
                "knowledge_point": "问路指路",
                "tags": "grammar,preposition",
                "options": [
                    {"key": "A", "text": "at"},
                    {"key": "B", "text": "in"},
                    {"key": "C", "text": "on"},
                    {"key": "D", "text": "to"}
                ]
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "如果你想问路，你应该先说：",
                "answer": "A",
                "analysis": "Excuse me 是礼貌地打断别人或引起注意的用语。",
                "knowledge_point": "礼貌用语",
                "tags": "speaking,politeness",
                "options": [
                    {"key": "A", "text": "Excuse me."},
                    {"key": "B", "text": "Sorry."},
                    {"key": "C", "text": "Thank you."},
                    {"key": "D", "text": "Hello."}
                ]
            },
            {
                "type": "fill_blank",
                "difficulty": 2,
                "stem": "Go ______ (直走) for 5 minutes.",
                "answer": "straight",
                "analysis": "直走的英文是 go straight。",
                "knowledge_point": "指路用语",
                "tags": "spelling,directions"
            },
            {
                "type": "single_choice",
                "difficulty": 2,
                "stem": "— Is it far from here?\n— No, it's ______ (近的).",
                "answer": "A",
                "analysis": "near 是近的意思。",
                "knowledge_point": "距离表达",
                "tags": "vocabulary,distance",
                "options": [
                    {"key": "A", "text": "near"},
                    {"key": "B", "text": "far"},
                    {"key": "C", "text": "long"},
                    {"key": "D", "text": "short"}
                ]
            },
        ]
    },
}

def main():
    print("=" * 60)
    print("人教版小学英语 (PEP) 丰富练习题导入工具")
    print("为每个单元添加 5-10 道高质量题目")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_questions = 0
    total_options = 0

    # 预定义的单元题目数据
    predefined_units = ALL_QUESTIONS_DATA

    for (grade, semester, unit_no), unit_data in predefined_units.items():
        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[SKIP] 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
            continue

        print(f"导入 {grade}年级{semester}册 Unit {unit_no} 题目...")

        for q_data in unit_data["questions"]:
            question_id = insert_question(
                conn,
                unit_id,
                q_data["type"],
                q_data["difficulty"],
                q_data["stem"],
                q_data["answer"],
                q_data["analysis"],
                q_data["knowledge_point"],
                q_data["tags"],
                q_data.get("stem_audio_url")
            )

            if question_id and "options" in q_data:
                for idx, opt in enumerate(q_data["options"], 1):
                    insert_question_option(conn, question_id, opt["key"], opt["text"], idx)
                    total_options += 1

            total_questions += 1

        print(f"  [OK] 完成，导入 {len(unit_data['questions'])} 道题")

    conn.close()

    print("=" * 60)
    print(f"导入完成！")
    print(f"  新增题目：{total_questions} 道")
    print(f"  新增选项：{total_options} 条")
    print("=" * 60)

if __name__ == '__main__':
    main()
