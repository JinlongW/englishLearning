#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于教材内容生成高质量题目
根据各单元的单词、语法点生成针对性练习
"""

import pyodbc
import sys
import json

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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def get_unit_words(conn, grade_unit_id):
    """获取单元的单词"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word, phonetic_uk, meaning_cn, part_of_speech, example_en, example_cn
        FROM tb_word WHERE grade_unit_id = ?
        ORDER BY sort_order
    """, grade_unit_id)
    return cursor.fetchall()

def get_unit_grammar(conn, grade_unit_id):
    """获取单元的语法点"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, content_json
        FROM tb_grammar WHERE grade_unit_id = ?
    """, grade_unit_id)
    return cursor.fetchall()

def insert_question(conn, grade_unit_id, q_type, difficulty, stem, answer, analysis, knowledge, tags, options=None):
    """插入题目和选项"""
    cursor = conn.cursor()

    # 插入题目
    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem,
                                stem_audio_url, correct_answer, answer_analysis, knowledge_point,
                                tags, is_active, created_at, updated_at)
        VALUES (NEWID(), ?, ?, ?, ?, NULL, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
    """, grade_unit_id, q_type, difficulty, stem, answer, analysis, knowledge, tags)

    # 获取题目 ID
    cursor.execute("""
        SELECT TOP 1 id FROM tb_question
        WHERE grade_unit_id = ? AND question_stem = ?
        ORDER BY created_at DESC
    """, (grade_unit_id, stem))
    row = cursor.fetchone()
    question_id = row.id if row else None

    # 插入选项
    if options and question_id:
        for idx, opt in enumerate(options, 1):
            cursor.execute("""
                INSERT INTO tb_question_option (id, question_id, option_key, option_content, sort_order)
                VALUES (NEWID(), ?, ?, ?, ?)
            """, question_id, opt['key'], opt['text'], idx)

    return question_id

# ========== 题目生成模板 ==========

def generate_word_meaning_question(words):
    """生成单词释义选择题"""
    if len(words) < 2:
        return None

    word = words[0]
    correct = word[0]  # word text
    answer = word[2]   # meaning

    # 从其他单词中选 3 个作为干扰项
    import random
    other_words = random.sample(list(words[1:]), min(3, len(words)-1))
    distractors = [w[2] for w in other_words]  # meanings

    options = [
        {"key": "A", "text": answer},
        {"key": "B", "text": distractors[0] if len(distractors) > 0 else "错误的"},
        {"key": "C", "text": distractors[1] if len(distractors) > 1 else "错误的"},
        {"key": "D", "text": distractors[2] if len(distractors) > 2 else "错误的"},
    ]

    return {
        "type": "single_choice",
        "difficulty": 1,
        "stem": f"单词\"{correct}\"的中文意思是：",
        "answer": "A",
        "analysis": f"{correct} 的意思是{answer}。",
        "knowledge": "词汇理解",
        "tags": "vocabulary,meaning",
        "options": options
    }

def generate_spelling_question(words):
    """生成单词拼写选择题"""
    if len(words) < 2:
        return None

    import random
    word = random.choice(list(words))
    correct = word[0]  # word text
    meaning = word[2]  # meaning

    # 从其他单词中选 3 个作为干扰项
    other_words = [w for w in words if w[0] != correct]
    if other_words:
        distractors = random.sample(other_words, min(3, len(other_words)))
        distractor_texts = [w[0] for w in distractors]
    else:
        distractor_texts = ["wrong1", "wrong2", "wrong3"]

    options = [
        {"key": "A", "text": correct},
        {"key": "B", "text": distractor_texts[0] if len(distractor_texts) > 0 else "wrong1"},
        {"key": "C", "text": distractor_texts[1] if len(distractor_texts) > 1 else "wrong2"},
        {"key": "D", "text": distractor_texts[2] if len(distractor_texts) > 2 else "wrong3"},
    ]

    # 随机打乱选项顺序
    random.shuffle(options)
    correct_key = [o["key"] for o in options if o["text"] == correct][0]

    return {
        "type": "single_choice",
        "difficulty": 2,
        "stem": f"根据中文\"{meaning}\"，选择正确的英文单词：",
        "answer": correct_key,
        "analysis": f"{meaning}的英文是{correct}。",
        "knowledge": "单词拼写",
        "tags": "vocabulary,spelling",
        "options": options
    }

def generate_example_sentence_question(words):
    """生成例句理解题"""
    if len(words) < 1:
        return None

    word = words[0]
    correct = word[0]
    example_en = word[4]
    example_cn = word[5]

    return {
        "type": "single_choice",
        "difficulty": 2,
        "stem": f"选择\"{example_en}\"的正确中文翻译：",
        "answer": "A",
        "analysis": example_cn,
        "knowledge": "句子理解",
        "tags": "sentence,translation",
        "options": [
            {"key": "A", "text": example_cn},
            {"key": "B", "text": "这是一个错误的翻译。"},
            {"key": "C", "text": "另一个错误的翻译。"},
            {"key": "D", "text": "以上都不对。"},
        ]
    }

def generate_fill_blank_question(words):
    """生成填空题"""
    if len(words) < 1:
        return None

    import random
    word = random.choice(list(words))
    correct = word[0]
    example_en = word[4]

    # 从例句中挖空
    if example_en and correct.lower() in example_en.lower():
        stem = example_en.replace(correct, "______")
        stem = stem.replace(correct.lower(), "______")
    else:
        stem = f"I have a ______ ({word[2]})."

    return {
        "type": "fill_blank",
        "difficulty": 2,
        "stem": f"根据句意和中文提示，填写单词：{stem}",
        "answer": correct,
        "analysis": f"{correct} 的意思是{word[2]}。",
        "knowledge": "单词拼写",
        "tags": "spelling,vocabulary",
        "options": []
    }

def generate_grammar_question(grammar_list):
    """生成语法题"""
    if not grammar_list:
        return None

    grammar = grammar_list[0]
    title = grammar[0]
    content_json = grammar[1]

    # 尝试从 JSON 中获取例句
    examples = []
    if content_json:
        try:
            content = json.loads(content_json)
            if isinstance(content, dict) and "examples" in content:
                examples = content["examples"]
        except:
            pass

    if examples:
        ex = examples[0]
        en = ex.get("en", "") if isinstance(ex, dict) else ""
        cn = ex.get("cn", "") if isinstance(ex, dict) else ""

        return {
            "type": "single_choice",
            "difficulty": 2,
            "stem": f"关于\"{title}\"，下列句子正确的是：",
            "answer": "A",
            "analysis": en + " 意思是：" + cn,
            "knowledge": title,
            "tags": "grammar,application",
            "options": [
                {"key": "A", "text": en},
                {"key": "B", "text": "这是一个语法错误的句子。"},
                {"key": "C", "text": "这是另一个错误的句子。"},
                {"key": "D", "text": "以上都不对。"},
            ]
        }
    else:
        return {
            "type": "single_choice",
            "difficulty": 1,
            "stem": f"本单元的语法知识点\"{title}\"主要用于：",
            "answer": "A",
            "analysis": f"{title} 是本单元的核心语法点，需要重点掌握。",
            "knowledge": title,
            "tags": "grammar,basic",
            "options": [
                {"key": "A", "text": "描述事物或进行日常交流"},
                {"key": "B", "text": "表达过去发生的动作"},
                {"key": "C", "text": "表示将来的计划"},
                {"key": "D", "text": "进行比较和最高级"},
            ]
        }

# ========== 主程序 ==========

def main():
    print("=" * 60)
    print("基于教材内容生成高质量题目")
    print("根据各单元的单词、语法点生成针对性练习")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_questions = 0

    # 遍历所有 48 个单元
    all_units = [
        (3, "上"), (3, "下"),
        (4, "上"), (4, "下"),
        (5, "上"), (5, "下"),
        (6, "上"), (6, "下")
    ]

    for grade, semester in all_units:
        for unit_no in range(1, 7):
            unit_id = get_unit_id(conn, grade, semester, unit_no)
            if not unit_id:
                print(f"[SKIP] 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
                continue

            # 获取单元的单词和语法
            words = get_unit_words(conn, unit_id)
            grammar = get_unit_grammar(conn, unit_id)

            if not words:
                print(f"[SKIP] {grade}年级{semester}册 Unit {unit_no}: 没有单词数据")
                continue

            # 为每个单元生成 5 道题目
            questions = []

            # 1. 单词释义题
            q = generate_word_meaning_question(words)
            if q:
                questions.append(q)

            # 2. 单词拼写题
            q = generate_spelling_question(words)
            if q:
                questions.append(q)

            # 3. 填空题
            q = generate_fill_blank_question(words)
            if q:
                questions.append(q)

            # 4. 例句理解题
            q = generate_example_sentence_question(words)
            if q:
                questions.append(q)

            # 5. 语法题
            q = generate_grammar_question(grammar)
            if q:
                questions.append(q)

            # 插入题目
            print(f"导入 {grade}年级{semester}册 Unit {unit_no} 题目...", end=" ")
            unit_count = 0
            for q in questions:
                insert_question(
                    conn, unit_id, q['type'], q['difficulty'], q['stem'],
                    q['answer'], q['analysis'], q['knowledge'], q['tags'], q.get('options')
                )
                unit_count += 1
                total_questions += 1

            print(f"[OK] {unit_count} 道题")

    conn.commit()
    conn.close()

    print("=" * 60)
    print("生成完成！")
    print(f"  新增题目：{total_questions} 道")
    print("=" * 60)

if __name__ == '__main__':
    main()
