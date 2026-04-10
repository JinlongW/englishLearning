# -*- coding: utf-8 -*-
"""
例句数据添加工具
日期：2026-04-02
说明：为核心单词和语法点添加例句数据
"""

import pyodbc
import json

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

def create_example_table(conn):
    """创建例句表"""
    cursor = conn.cursor()

    # 检查表是否存在
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tb_example_sentence' and xtype='U')
        BEGIN
            CREATE TABLE tb_example_sentence (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                word_id UNIQUEIDENTIFIER NULL,
                grammar_id UNIQUEIDENTIFIER NULL,
                example_sentence NVARCHAR(500) NOT NULL,
                translation NVARCHAR(300) NOT NULL,
                difficulty INT DEFAULT 1,
                sort_order INT DEFAULT 0,
                created_at DATETIME2 DEFAULT GETDATE(),
                FOREIGN KEY (word_id) REFERENCES tb_word(id),
                FOREIGN KEY (grammar_id) REFERENCES tb_grammar(id)
            )
            PRINT '例句表创建成功'
        END
        ELSE
        BEGIN
            -- 检查是否需要添加 grammar_id 字段
            IF NOT EXISTS (SELECT * FROM sys.columns WHERE name='grammar_id' AND object_id = OBJECT_ID('tb_example_sentence'))
            BEGIN
                ALTER TABLE tb_example_sentence ADD grammar_id UNIQUEIDENTIFIER NULL
                PRINT '已添加 grammar_id 字段'
            END
            PRINT '例句表已存在'
        END
    """)
    conn.commit()

def insert_example(conn, word_id, sentence, translation, difficulty=1):
    """插入例句"""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tb_example_sentence (word_id, example_sentence, translation, difficulty)
            VALUES (?, ?, ?, ?)
        """, (word_id, sentence, translation, difficulty))
        conn.commit()
        return True
    except Exception as e:
        print(f"插入失败：{e}")
        return False

def get_word_id(conn, word):
    """获取单词 ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tb_word WHERE word = ?", word)
    row = cursor.fetchone()
    return row.id if row else None

# 例句数据 - 按年级组织
EXAMPLE_SENTENCES = {
    # 三年级 - 基础词汇
    3: {
        "hello": [
            ("Hello! My name is Amy.", "你好！我叫艾米。"),
            ("Hello, how are you?", "你好，你好吗？"),
        ],
        "teacher": [
            ("This is my teacher.", "这是我的老师。"),
            ("My teacher is very kind.", "我的老师很和蔼。"),
        ],
        "friend": [
            ("She is my good friend.", "她是我的好朋友。"),
            ("I play with my friend.", "我和朋友一起玩。"),
        ],
        "apple": [
            ("I like apples.", "我喜欢苹果。"),
            ("This apple is red.", "这个苹果是红色的。"),
            ("An apple a day keeps the doctor away.", "一天一苹果，医生远离我。"),
        ],
        "book": [
            ("Open your book.", "打开你的书。"),
            ("I have a new book.", "我有一本新书。"),
        ],
        "cat": [
            ("I have a cat.", "我有一只猫。"),
            ("The cat is cute.", "这只猫很可爱。"),
        ],
        "dog": [
            ("I have a dog.", "我有一只狗。"),
            ("My dog is black.", "我的狗是黑色的。"),
        ],
        "school": [
            ("I go to school.", "我去上学。"),
            ("My school is big.", "我的学校很大。"),
        ],
        "head": [
            ("Touch your head.", "摸摸你的头。"),
            ("My head hurts.", "我的头疼。"),
        ],
        "eye": [
            ("Close your eyes.", "闭上眼睛。"),
            ("I have two eyes.", "我有两只眼睛。"),
        ],
    },
    # 四年级 - 进阶词汇
    4: {
        "classroom": [
            ("Our classroom is clean.", "我们的教室很干净。"),
            ("There are 40 students in our classroom.", "我们教室有 40 个学生。"),
        ],
        "library": [
            ("I read books in the library.", "我在图书馆看书。"),
            ("The library is quiet.", "图书馆很安静。"),
        ],
        "playground": [
            ("We play on the playground.", "我们在操场上玩。"),
            ("The playground is big.", "操场很大。"),
        ],
        "breakfast": [
            ("I have breakfast at 7.", "我 7 点吃早餐。"),
            ("Breakfast is ready.", "早餐准备好了。"),
        ],
        "lunch": [
            ("I have lunch at school.", "我在学校吃午餐。"),
            ("Lunch time is 12 o'clock.", "午餐时间是 12 点。"),
        ],
        "dinner": [
            ("We have dinner together.", "我们一起吃晚餐。"),
            ("Dinner is delicious.", "晚餐很美味。"),
        ],
        "weather": [
            ("What's the weather like?", "天气怎么样？"),
            ("The weather is sunny.", "天气晴朗。"),
        ],
        "sunny": [
            ("It's sunny today.", "今天天气晴朗。"),
            ("I like sunny days.", "我喜欢晴天。"),
        ],
        "rainy": [
            ("It's rainy today.", "今天下雨。"),
            ("I don't like rainy days.", "我不喜欢雨天。"),
        ],
        "clothes": [
            ("I like these clothes.", "我喜欢这些衣服。"),
            ("Put on your clothes.", "穿上你的衣服。"),
        ],
    },
    # 五年级 - 提高词汇
    5: {
        "kind": [
            ("She is very kind.", "她很善良。"),
            ("He is a kind teacher.", "他是一位和蔼的老师。"),
        ],
        "strict": [
            ("My maths teacher is strict.", "我的数学老师很严格。"),
            ("Don't be too strict.", "不要太严格。"),
        ],
        "favourite": [
            ("What's your favourite food?", "你最喜欢的食物是什么？"),
            ("My favourite color is blue.", "我最喜欢的颜色是蓝色。"),
        ],
        "season": [
            ("Which season do you like best?", "你最喜欢哪个季节？"),
            ("Spring is my favourite season.", "春天是我最喜欢的季节。"),
        ],
        "birthday": [
            ("When is your birthday?", "你的生日是什么时候？"),
            ("My birthday is in May.", "我的生日在五月。"),
        ],
        "weekend": [
            ("What do you do on the weekend?", "你周末做什么？"),
            ("I visit my grandparents on the weekend.", "我周末去看望祖父母。"),
        ],
        "morning": [
            ("Good morning!", "早上好！"),
            ("I exercise in the morning.", "我早上锻炼。"),
        ],
        "afternoon": [
            ("Good afternoon!", "下午好！"),
            ("I sleep in the afternoon.", "我下午睡觉。"),
        ],
        "evening": [
            ("Good evening!", "晚上好！"),
            ("I watch TV in the evening.", "我晚上看电视。"),
        ],
        "homework": [
            ("I do my homework.", "我做作业。"),
            ("Have you finished your homework?", "你完成作业了吗？"),
        ],
    },
    # 六年级 - 拓展词汇
    6: {
        "science": [
            ("I like science class.", "我喜欢科学课。"),
            ("Science is interesting.", "科学很有趣。"),
        ],
        "museum": [
            ("We visited the museum.", "我们参观了博物馆。"),
            ("The museum is big.", "博物馆很大。"),
        ],
        "post office": [
            ("Where is the post office?", "邮局在哪里？"),
            ("I send a letter at the post office.", "我在邮局寄信。"),
        ],
        "hospital": [
            ("He works in a hospital.", "他在医院工作。"),
            ("The hospital is near.", "医院很近。"),
        ],
        "scientist": [
            ("I want to be a scientist.", "我想成为科学家。"),
            ("The scientist is smart.", "这位科学家很聪明。"),
        ],
        "pilot": [
            ("My uncle is a pilot.", "我的叔叔是飞行员。"),
            ("The pilot flies the plane.", "飞行员驾驶飞机。"),
        ],
        "happy": [
            ("I'm very happy.", "我很开心。"),
            ("She looks happy.", "她看起来很开心。"),
        ],
        "sad": [
            ("Don't be sad.", "不要难过。"),
            ("He looks sad.", "他看起来很伤心。"),
        ],
        "angry": [
            ("Why are you angry?", "你为什么生气？"),
            ("Don't be angry with me.", "不要生我的气。"),
        ],
        "worried": [
            ("I'm worried about you.", "我担心你。"),
            ("She looks worried.", "她看起来很担心。"),
        ],
    },
}

# 语法点例句
GRAMMAR_EXAMPLES = {
    # 三年级语法
    (3, '下', 1): [
        ("Welcome back to school!", "欢迎回到学校！"),
        ("Nice to see you again!", "很高兴再次见到你！"),
        ("I'm from China.", "我来自中国。"),
        ("Where are you from?", "你来自哪里？"),
    ],
    (3, '下', 2): [
        ("This is my father.", "这是我的父亲。"),
        ("She's my sister.", "她是我的姐妹。"),
        ("He's my brother.", "他是我的兄弟。"),
    ],
    (3, '下', 3): [
        ("It's so tall!", "它好高！"),
        ("The elephant is big.", "大象很大。"),
        ("The mouse is small.", "老鼠很小。"),
    ],
    (3, '下', 4): [
        ("Where is my car?", "我的小汽车在哪里？"),
        ("It's in the desk.", "它在书桌里。"),
        ("It's under the chair.", "它在椅子下面。"),
    ],
    (3, '下', 5): [
        ("Do you like pears?", "你喜欢梨吗？"),
        ("Yes, I do.", "是的，我喜欢。"),
        ("No, I don't.", "不，我不喜欢。"),
    ],
    (3, '下', 6): [
        ("How many kites do you see?", "你看见多少只风筝？"),
        ("I see 12!", "我看见 12 只！"),
    ],
    # 四年级语法
    (4, '下', 1): [
        ("This is the library.", "这是图书馆。"),
        ("Is this the teachers' office?", "这是教师办公室吗？"),
        ("Yes, it is.", "是的，它是。"),
    ],
    (4, '下', 2): [
        ("What time is it?", "现在几点了？"),
        ("It's 7 o'clock.", "现在 7 点。"),
        ("It's time for breakfast.", "是早餐时间了。"),
    ],
    (4, '下', 3): [
        ("What's the weather like?", "天气怎么样？"),
        ("It's sunny.", "天气晴朗。"),
        ("It's cloudy.", "天气多云。"),
    ],
    (4, '下', 4): [
        ("Are these carrots?", "这些是胡萝卜吗？"),
        ("Yes, they are.", "是的，它们是。"),
    ],
    (4, '下', 5): [
        ("Whose coat is this?", "这是谁的外套？"),
        ("It's mine.", "是我的。"),
    ],
    (4, '下', 6): [
        ("How much is this?", "这个多少钱？"),
        ("It's 89 yuan.", "89 元。"),
    ],
    # 五年级语法
    (5, '上', 3): [
        ("What's your favourite food?", "你最喜欢的食物是什么？"),
        ("My favourite food is noodles.", "我最喜欢的食物是面条。"),
    ],
    (5, '上', 4): [
        ("What can you do?", "你会做什么？"),
        ("I can swim.", "我会游泳。"),
        ("I can cook.", "我会做饭。"),
    ],
    (5, '上', 5): [
        ("There is a bed in the room.", "房间里有一张床。"),
        ("There are two chairs.", "有两把椅子。"),
    ],
    (5, '下', 1): [
        ("When do you get up?", "你什么时候起床？"),
        ("I get up at 7 o'clock.", "我 7 点起床。"),
    ],
    (5, '下', 2): [
        ("Which season do you like best?", "你最喜欢哪个季节？"),
        ("I like spring best.", "我最喜欢春天。"),
    ],
    (5, '下', 3): [
        ("When is your birthday?", "你的生日是什么时候？"),
        ("My birthday is on May 2nd.", "我的生日是 5 月 2 日。"),
    ],
    (5, '下', 6): [
        ("What are they doing?", "他们在做什么？"),
        ("They are eating lunch.", "他们在吃午饭。"),
    ],
    # 六年级语法
    (6, '上', 1): [
        ("How can I get to the museum?", "我怎么去博物馆？"),
        ("Turn left at the school.", "在学校左转。"),
    ],
    (6, '上', 5): [
        ("What are you going to be?", "你将来想做什么？"),
        ("I'm going to be a scientist.", "我想成为科学家。"),
    ],
    (6, '下', 1): [
        ("How tall are you?", "你多高？"),
        ("I'm 1.65 meters.", "我 1 米 65。"),
        ("I'm taller than you.", "我比你高。"),
    ],
    (6, '下', 2): [
        ("What did you do last weekend?", "你上周末做了什么？"),
        ("I cleaned my room.", "我打扫了房间。"),
    ],
    (6, '下', 3): [
        ("Where did you go?", "你去了哪里？"),
        ("I went to Turpan.", "我去了吐鲁番。"),
    ],
    (6, '下', 6): [
        ("How can we stay in touch?", "我们怎么保持联系？"),
        ("We can write emails.", "我们可以写邮件。"),
        ("Wish you all the best!", "祝你一切顺利！"),
    ],
}

def main():
    print("=" * 60)
    print("     例句数据添加工具")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    # 创建例句表
    create_example_table(conn)
    print("[OK] 例句表创建/确认完成\n")

    # 统计
    total_inserted = 0
    total_skipped = 0

    # 1. 添加单词例句
    print("正在添加单词例句...")
    for grade, words in EXAMPLE_SENTENCES.items():
        for word, examples in words.items():
            word_id = get_word_id(conn, word)
            if not word_id:
                print(f"  [NOT FOUND] {word}")
                continue

            for sentence, translation in examples:
                if insert_example(conn, word_id, sentence, translation):
                    total_inserted += 1
                    print(f"  [OK] {word}: {sentence[:30]}...")
                else:
                    total_skipped += 1

    # 2. 添加语法例句 (关联到语法点)
    print("\n正在添加语法例句...")
    for (grade, semester, unit_no), examples in GRAMMAR_EXAMPLES.items():
        # 获取单元 ID
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM tb_grade_unit
            WHERE grade = ? AND semester = ? AND unit_no = ?
        """, (grade, semester, unit_no))
        unit = cursor.fetchone()

        if not unit:
            print(f"  [NOT FOUND] {grade}年级{semester}册 Unit {unit_no}")
            continue

        # 获取该单元的语法点 ID
        cursor.execute("""
            SELECT TOP 1 id FROM tb_grammar
            WHERE grade_unit_id = ?
        """, (unit.id,))
        grammar = cursor.fetchone()

        if not grammar:
            print(f"  [NO GRAMMAR] {grade}年级{semester}册 Unit {unit_no}")
            continue

        for sentence, translation in examples:
            # 语法例句关联到语法点
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO tb_example_sentence (grammar_id, example_sentence, translation, difficulty)
                    VALUES (?, ?, ?, 1)
                """, (grammar.id, sentence, translation))
                conn.commit()
                total_inserted += 1
                print(f"  [OK] Unit {unit_no}: {sentence[:30]}...")
            except Exception as e:
                total_skipped += 1
                print(f"  [ERROR] 插入失败：{e}")

    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  成功插入：{total_inserted} 条")
    print(f"  跳过/失败：{total_skipped} 条")
    print("=" * 60)

if __name__ == "__main__":
    main()
