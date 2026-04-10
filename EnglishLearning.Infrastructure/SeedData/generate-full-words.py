#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 完整单词表生成器
根据官方教材大纲生成 3-6 年级所有单词数据
"""

import json
import pyodbc
from pathlib import Path

# 数据库连接配置
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

# 人教版小学英语 (PEP) 完整单词表 - 根据官方教材整理
CURRICULUM_DATA = {
    # 三年级上册
    (3, "上", 1, "Unit 1 Hello!"): [
        ("ruler", "/ˈruːlə/", "/ˈruːlər/", "尺子", "n.", "I have a ruler.", "我有一把尺子。"),
        ("pencil", "/ˈpensl/", "/ˈpensl/", "铅笔", "n.", "This is my pencil.", "这是我的铅笔。"),
        ("eraser", "/ɪˈreɪzə/", "/ɪˈreɪsər/", "橡皮", "n.", "Can I use your eraser?", "我可以用你的橡皮吗？"),
        ("crayon", "/ˈkreɪən/", "/ˈkreɪən/", "蜡笔", "n.", "She has a red crayon.", "她有一支红色的蜡笔。"),
        ("book", "/bʊk/", "/bʊk/", "书", "n.", "Open your book.", "打开你的书。"),
        ("pencil box", "/ˈpensl bɒks/", "/ˈpensl bɑːks/", "铅笔盒", "n.", "My pen is in the pencil box.", "我的钢笔在铅笔盒里。"),
        ("bag", "/bæɡ/", "/bæɡ/", "书包", "n.", "I put my books in the bag.", "我把书放进书包里。"),
    ],
    (3, "上", 2, "Unit 2 Look at Me"): [
        ("head", "/hed/", "/hed/", "头", "n.", "Touch your head.", "摸摸你的头。"),
        ("face", "/feɪs/", "/feɪs/", "脸", "n.", "She has a round face.", "她有一张圆脸。"),
        ("nose", "/nəʊz/", "/noʊz/", "鼻子", "n.", "Point to your nose.", "指着你的鼻子。"),
        ("eye", "/aɪ/", "/aɪ/", "眼睛", "n.", "I have two eyes.", "我有两只眼睛。"),
        ("ear", "/ɪə/", "/ɪr/", "耳朵", "n.", "Cover your ears.", "捂住你的耳朵。"),
        ("mouth", "/maʊθ/", "/maʊθ/", "嘴巴", "n.", "Open your mouth.", "张开你的嘴巴。"),
        ("arm", "/ɑːm/", "/ɑːrm/", "胳膊", "n.", "Raise your arm.", "举起你的胳膊。"),
        ("hand", "/hænd/", "/hænd/", "手", "n.", "Clap your hands.", "拍拍你的手。"),
        ("leg", "/leɡ/", "/leɡ/", "腿", "n.", "Stamp your foot.", "跺跺你的脚。"),
        ("foot", "/fʊt/", "/fʊt/", "脚", "n.", "My foot hurts.", "我的脚疼。"),
    ],
    (3, "上", 3, "Unit 3 Let's Paint"): [
        ("red", "/red/", "/red/", "红色", "n./adj.", "The apple is red.", "苹果是红色的。"),
        ("yellow", "/ˈjeləʊ/", "/ˈjeloʊ/", "黄色", "n./adj.", "The banana is yellow.", "香蕉是黄色的。"),
        ("green", "/ɡriːn/", "/ɡriːn/", "绿色", "n./adj.", "The grass is green.", "草地是绿色的。"),
        ("blue", "/bluː/", "/bluː/", "蓝色", "n./adj.", "The sky is blue.", "天空是蓝色的。"),
        ("black", "/blæk/", "/blæk/", "黑色", "n./adj.", "The cat is black.", "这只猫是黑色的。"),
        ("white", "/waɪt/", "/waɪt/", "白色", "n./adj.", "The snow is white.", "雪是白色的。"),
        ("orange", "/ˈɒrɪndʒ/", "/ˈɔːrɪndʒ/", "橙色", "n./adj.", "The orange is orange.", "橙子是橙色的。"),
        ("brown", "/braʊn/", "/braʊn/", "棕色", "n./adj.", "The bear is brown.", "熊是棕色的。"),
    ],
    (3, "上", 4, "Unit 4 We Love Animals"): [
        ("pig", "/pɪɡ/", "/pɪɡ/", "猪", "n.", "The pig is fat.", "这头猪很胖。"),
        ("bear", "/beə/", "/ber/", "熊", "n.", "The bear is big.", "熊很大。"),
        ("duck", "/dʌk/", "/dʌk/", "鸭子", "n.", "The duck can swim.", "鸭子会游泳。"),
        ("elephant", "/ˈelɪfənt/", "/ˈelɪfənt/", "大象", "n.", "The elephant has a long nose.", "大象有一个长鼻子。"),
        ("monkey", "/ˈmʌŋki/", "/ˈmʌŋki/", "猴子", "n.", "The monkey is clever.", "猴子很聪明。"),
        ("bird", "/bɜːd/", "/bɜːrd/", "鸟", "n.", "The bird can fly.", "鸟会飞。"),
        ("tiger", "/ˈtaɪɡə/", "/ˈtaɪɡər/", "老虎", "n.", "The tiger is strong.", "老虎很强壮。"),
        ("panda", "/ˈpændə/", "/ˈpændə/", "熊猫", "n.", "The panda is cute.", "熊猫很可爱。"),
        ("zoo", "/zuː/", "/zuː/", "动物园", "n.", "Let's go to the zoo.", "我们去动物园吧。"),
    ],
    (3, "上", 5, "Unit 5 Let's Eat"): [
        ("bread", "/bred/", "/bred/", "面包", "n.", "I like bread.", "我喜欢面包。"),
        ("juice", "/dʒuːs/", "/dʒuːs/", "果汁", "n.", "Can I have some juice?", "我能喝点果汁吗？"),
        ("egg", "/eɡ/", "/eɡ/", "鸡蛋", "n.", "I eat an egg for breakfast.", "我早餐吃了一个鸡蛋。"),
        ("milk", "/mɪlk/", "/mɪlk/", "牛奶", "n.", "Drink some milk.", "喝点牛奶。"),
        ("water", "/ˈwɔːtə/", "/ˈwɔːtər/", "水", "n.", "I want some water.", "我想喝水。"),
        ("fish", "/fɪʃ/", "/fɪʃ/", "鱼", "n.", "The fish is delicious.", "鱼很美味。"),
        ("rice", "/raɪs/", "/raɪs/", "米饭", "n.", "I have rice for lunch.", "我午餐吃了米饭。"),
    ],
    (3, "上", 6, "Unit 6 Happy Birthday"): [
        ("one", "/wʌn/", "/wʌn/", "一", "num.", "I have one book.", "我有一本书。"),
        ("two", "/tuː/", "/tuː/", "二", "num.", "I see two birds.", "我看到两只鸟。"),
        ("three", "/θriː/", "/θriː/", "三", "num.", "There are three apples.", "有三个苹果。"),
        ("four", "/fɔː/", "/fɔːr/", "四", "num.", "I have four pencils.", "我有四支铅笔。"),
        ("five", "/faɪv/", "/faɪv/", "五", "num.", "She has five fingers.", "她有五个手指。"),
        ("six", "/sɪks/", "/sɪks/", "六", "num.", "There are six days in a week.", "一周有六天。"),
        ("seven", "/ˈsevn/", "/ˈsevn/", "七", "num.", "I see seven stars.", "我看到七颗星星。"),
        ("eight", "/eɪt/", "/eɪt/", "八", "num.", "There are eight people.", "有八个人。"),
        ("nine", "/naɪn/", "/naɪn/", "九", "num.", "I have nine balls.", "我有九个球。"),
        ("ten", "/ten/", "/ten/", "十", "num.", "There are ten fingers.", "有十个手指。"),
        ("cake", "/keɪk/", "/keɪk/", "蛋糕", "n.", "Happy birthday! Let's eat cake.", "生日快乐！我们吃蛋糕吧。"),
    ],
    # 三年级下册
    (3, "下", 1, "Unit 1 Welcome Back to School"): [
        ("UK", "/ˌjuː ˈkeɪ/", "/ˌjuː ˈkeɪ/", "英国", "n.", "I'm from the UK.", "我来自英国。"),
        ("USA", "/ˌjuː es ˈeɪ/", "/ˌjuː es ˈeɪ/", "美国", "n.", "She's from the USA.", "她来自美国。"),
        ("China", "/ˈtʃaɪnə/", "/ˈtʃaɪnə/", "中国", "n.", "I'm from China.", "我来自中国。"),
        ("Canada", "/ˈkænədə/", "/ˈkænədə/", "加拿大", "n.", "He's from Canada.", "他来自加拿大。"),
        ("student", "/ˈstjuːdnt/", "/ˈstuːdnt/", "学生", "n.", "I'm a student.", "我是一名学生。"),
        ("pupil", "/ˈpjuːpl/", "/ˈpjuːpl/", "小学生", "n.", "She's a pupil.", "她是个小学生。"),
        ("teacher", "/ˈtiːtʃə/", "/ˈtiːtʃər/", "教师", "n.", "He's a teacher.", "他是一名教师。"),
        ("new", "/njuː/", "/nuː/", "新的", "adj.", "I have a new bag.", "我有一个新书包。"),
        ("friend", "/frend/", "/frend/", "朋友", "n.", "She's my new friend.", "她是我的新朋友。"),
        ("today", "/təˈdeɪ/", "/təˈdeɪ/", "今天", "n.", "Welcome back today.", "今天欢迎回来。"),
    ],
    (3, "下", 2, "Unit 2 My Family"): [
        ("father", "/ˈfɑːðə/", "/ˈfɑːðər/", "父亲", "n.", "My father is tall.", "我的父亲很高。"),
        ("dad", "/dæd/", "/dæd/", "爸爸", "n.", "I love my dad.", "我爱我的爸爸。"),
        ("mother", "/ˈmʌðə/", "/ˈmʌðər/", "母亲", "n.", "My mother is kind.", "我的母亲很善良。"),
        ("mum", "/mʌm/", "/mʌm/", "妈妈", "n.", "Mum is cooking.", "妈妈在做饭。"),
        ("man", "/mæn/", "/mæn/", "男人", "n.", "He's a man.", "他是个男人。"),
        ("woman", "/ˈwʊmən/", "/ˈwʊmən/", "女人", "n.", "She's a woman.", "她是个女人。"),
        ("sister", "/ˈsɪstə/", "/ˈsɪstər/", "姐妹", "n.", "She's my sister.", "她是我的姐妹。"),
        ("brother", "/ˈbrʌðə/", "/ˈbrʌðər/", "兄弟", "n.", "He's my brother.", "他是我的兄弟。"),
        ("grandmother", "/ˈɡrænmʌðə/", "/ˈɡrænmʌðər/", "祖母", "n.", "My grandmother is old.", "我的祖母老了。"),
        ("grandpa", "/ˈɡrænpɑː/", "/ˈɡrænpɑː/", "爷爷", "n.", "Grandpa is reading.", "爷爷在看书。"),
    ],
    (3, "下", 3, "Unit 3 At the Zoo"): [
        ("thin", "/θɪn/", "/θɪn/", "瘦的", "adj.", "The monkey is thin.", "这只猴子很瘦。"),
        ("fat", "/fæt/", "/fæt/", "胖的", "adj.", "The pig is fat.", "这头猪很胖。"),
        ("tall", "/tɔːl/", "/tɔːl/", "高的", "adj.", "The giraffe is tall.", "长颈鹿很高。"),
        ("short", "/ʃɔːt/", "/ʃɔːrt/", "矮的", "adj.", "He is short.", "他很矮。"),
        ("long", "/lɒŋ/", "/lɔːŋ/", "长的", "adj.", "The snake is long.", "这条蛇很长。"),
        ("small", "/smɔːl/", "/smɔːl/", "小的", "adj.", "The ant is small.", "蚂蚁很小。"),
        ("big", "/bɪɡ/", "/bɪɡ/", "大的", "adj.", "The elephant is big.", "大象很大。"),
        ("giraffe", "/dʒəˈrɑːf/", "/dʒəˈræf/", "长颈鹿", "n.", "The giraffe has a long neck.", "长颈鹿有个长脖子。"),
    ],
    (3, "下", 4, "Unit 4 Where Is My Car"): [
        ("car", "/kɑː/", "/kɑːr/", "汽车", "n.", "This is my car.", "这是我的汽车。"),
        ("boat", "/bəʊt/", "/boʊt/", "船", "n.", "The boat is on the water.", "船在水上。"),
        ("map", "/mæp/", "/mæp/", "地图", "n.", "Look at the map.", "看地图。"),
        ("ball", "/bɔːl/", "/bɔːl/", "球", "n.", "Kick the ball.", "踢球。"),
        ("box", "/bɒks/", "/bɑːks/", "盒子", "n.", "It's in the box.", "它在盒子里。"),
        ("cap", "/kæp/", "/kæp/", "帽子", "n.", "Where is my cap?", "我的帽子在哪里？"),
        ("toy", "/tɔɪ/", "/tɔɪ/", "玩具", "n.", "I have a toy.", "我有一个玩具。"),
        ("under", "/ˈʌndə/", "/ˈʌndər/", "在...下面", "prep.", "The cat is under the table.", "猫在桌子下面。"),
        ("on", "/ɒn/", "/ɑːn/", "在...上面", "prep.", "The book is on the desk.", "书在桌子上。"),
    ],
    (3, "下", 5, "Unit 5 Do You Like Pears"): [
        ("pear", "/peə/", "/per/", "梨", "n.", "I like pears.", "我喜欢梨。"),
        ("apple", "/ˈæpl/", "/ˈæpl/", "苹果", "n.", "An apple a day.", "一天一个苹果。"),
        ("orange", "/ˈɒrɪndʒ/", "/ˈɔːrɪndʒ/", "橙子", "n.", "Do you like oranges?", "你喜欢橙子吗？"),
        ("banana", "/bəˈnɑːnə/", "/bəˈnænə/", "香蕉", "n.", "Monkeys like bananas.", "猴子喜欢香蕉。"),
        ("grape", "/ɡreɪp/", "/ɡreɪp/", "葡萄", "n.", "These grapes are sweet.", "这些葡萄很甜。"),
        ("like", "/laɪk/", "/laɪk/", "喜欢", "v.", "I like ice cream.", "我喜欢冰淇淋。"),
        ("some", "/sʌm/", "/sʌm/", "一些", "det.", "Have some fruit.", "吃点水果吧。"),
        ("fruit", "/fruːt/", "/fruːt/", "水果", "n.", "Fruit is healthy.", "水果很健康。"),
        ("buy", "/baɪ/", "/baɪ/", "买", "v.", "Let's buy some fruit.", "我们买点水果吧。"),
        ("child", "/tʃaɪld/", "/tʃaɪld/", "孩子", "n.", "The child is happy.", "孩子很高兴。"),
    ],
    (3, "下", 6, "Unit 6 How Many"): [
        ("eleven", "/ɪˈlevn/", "/ɪˈlevn/", "十一", "num.", "I see eleven birds.", "我看到十一只鸟。"),
        ("twelve", "/twelv/", "/twelv/", "十二", "num.", "There are twelve months.", "有十二个月。"),
        ("thirteen", "/ˌθɜːˈtiːn/", "/ˌθɜːrˈtiːn/", "十三", "num.", "She is thirteen.", "她十三岁。"),
        ("fourteen", "/ˌfɔːˈtiːn/", "/ˌfɔːrˈtiːn/", "十四", "num.", "I have fourteen pens.", "我有十四支钢笔。"),
        ("fifteen", "/ˌfɪfˈtiːn/", "/ˌfɪfˈtiːn/", "十五", "num.", "There are fifteen stars.", "有十五颗星星。"),
        ("sixteen", "/ˌsɪkˈstiːn/", "/ˌsɪkˈstiːn/", "十六", "num.", "I see sixteen fish.", "我看到十六条鱼。"),
        ("seventeen", "/ˌsevnˈtiːn/", "/ˌsevnˈtiːn/", "十七", "num.", "There are seventeen trees.", "有十七棵树。"),
        ("eighteen", "/ˌeɪˈtiːn/", "/ˌeɪˈtiːn/", "十八", "num.", "I have eighteen balls.", "我有十八个球。"),
        ("nineteen", "/ˌnaɪnˈtiːn/", "/ˌnaɪnˈtiːn/", "十九", "num.", "There are nineteen apples.", "有十九个苹果。"),
        ("twenty", "/ˈtwenti/", "/ˈtwenti/", "二十", "num.", "I have twenty fingers.", "我有二十个手指。"),
        ("kite", "/kaɪt/", "/kaɪt/", "风筝", "n.", "Fly a kite.", "放风筝。"),
        ("beautiful", "/ˈbjuːtɪfl/", "/ˈbjuːtɪfl/", "美丽的", "adj.", "The kite is beautiful.", "风筝很漂亮。"),
    ],
}

def get_unit_id(conn, grade, semester, unit_no):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def insert_word(conn, grade_unit_id, word_data):
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
        word_data['word'],
        word_data['phonetic_uk'],
        word_data['phonetic_us'],
        word_data['meaning_cn'],
        word_data['part_of_speech'],
        word_data['example_en'],
        word_data['example_cn'],
        word_data['sort_order']
    )
    conn.commit()

def main():
    print("=" * 60)
    print("人教版小学英语 (PEP) 完整单词表导入工具")
    print("数据源：根据官方教材大纲整理")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_imported = 0

    for (grade, semester, unit_no, unit_name), words in CURRICULUM_DATA.items():
        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[SKIP] 单元不存在：{grade}年级{semester}册 {unit_name}")
            continue

        print(f"导入 {grade}年级{semester}册 {unit_name} ({len(words)} 个单词)...")

        for idx, word in enumerate(words, 1):
            word_data = {
                'word': word[0],
                'phonetic_uk': word[1],
                'phonetic_us': word[2],
                'meaning_cn': word[3],
                'part_of_speech': word[4],
                'example_en': word[5],
                'example_cn': word[6],
                'sort_order': idx
            }
            insert_word(conn, unit_id, word_data)
            total_imported += 1

        print(f"  [OK] {unit_name} 完成")

    conn.close()

    print("=" * 60)
    print(f"导入完成！共导入 {total_imported} 个单词")
    print("=" * 60)

if __name__ == '__main__':
    main()
