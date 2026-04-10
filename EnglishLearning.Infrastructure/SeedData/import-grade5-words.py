#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 五年级单词表导入工具
"""

import pyodbc

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

# 五年级上册
GRADE5_VOLUME1 = {
    (5, "上", 1, "Unit 1 What's He Like"): [
        ("old", "/əʊld/", "/oʊld/", "老的", "adj.", "He is old.", "他很老。"),
        ("young", "/jʌŋ/", "/jʌŋ/", "年轻的", "adj.", "She is young.", "她很年轻。"),
        ("kind", "/kaɪnd/", "/kaɪnd/", "和蔼的", "adj.", "He is kind.", "他很和蔼。"),
        ("strict", "/strɪkt/", "/strɪkt/", "严格的", "adj.", "The teacher is strict.", "老师很严格。"),
        ("polite", "/pəˈlaɪt/", "/pəˈlaɪt/", "有礼貌的", "adj.", "She is polite.", "她很有礼貌。"),
        ("hard-working", "/ˌhɑːd ˈwɜːkɪŋ/", "/ˌhɑːrd ˈwɜːrkɪŋ/", "努力的", "adj.", "He is hard-working.", "他很努力。"),
        ("helpful", "/ˈhelpfl/", "/ˈhelpfl/", "有用的", "adj.", "She is helpful.", "她很有用。"),
        ("clever", "/ˈklevə/", "/ˈklevər/", "聪明的", "adj.", "The boy is clever.", "这个男孩很聪明。"),
        ("funny", "/ˈfʌni/", "/ˈfʌni/", "滑稽的", "adj.", "He is funny.", "他很滑稽。"),
    ],
    (5, "上", 2, "Unit 2 My Week"): [
        ("Monday", "/ˈmʌndeɪ/", "/ˈmʌndeɪ/", "星期一", "n.", "Today is Monday.", "今天是星期一。"),
        ("Tuesday", "/ˈtjuːzdeɪ/", "/ˈtuːzdeɪ/", "星期二", "n.", "Tomorrow is Tuesday.", "明天是星期二。"),
        ("Wednesday", "/ˈwenzdeɪ/", "/ˈwenzdeɪ/", "星期三", "n.", "It's Wednesday today.", "今天是星期三。"),
        ("Thursday", "/ˈθɜːzdeɪ/", "/ˈθɜːrzdeɪ/", "星期四", "n.", "Thursday is busy.", "星期四很忙。"),
        ("Friday", "/ˈfraɪdeɪ/", "/ˈfraɪdeɪ/", "星期五", "n.", "I like Friday.", "我喜欢星期五。"),
        ("Saturday", "/ˈsætədeɪ/", "/ˈsætərdeɪ/", "星期六", "n.", "Saturday is fun.", "星期六很有趣。"),
        ("Sunday", "/ˈsʌndeɪ/", "/ˈsʌndeɪ/", "星期日", "n.", "Sunday is relaxing.", "星期日很轻松。"),
        ("weekend", "/ˌwiːkˈend/", "/ˌwiːkˈend/", "周末", "n.", "I play on the weekend.", "我周末玩耍。"),
        ("wash", "/wɒʃ/", "/wɑːʃ/", "洗", "v.", "I wash my clothes.", "我洗我的衣服。"),
        ("read", "/riːd/", "/riːd/", "读", "v.", "I read books.", "我读书。"),
    ],
    (5, "上", 3, "Unit 3 What Would You Like"): [
        ("sandwich", "/ˈsænwɪtʃ/", "/ˈsænwɪtʃ/", "三明治", "n.", "I like sandwiches.", "我喜欢三明治。"),
        ("salad", "/ˈsæləd/", "/ˈsæləd/", "沙拉", "n.", "Salad is healthy.", "沙拉很健康。"),
        ("hamburger", "/ˈhæmbɜːɡə/", "/ˈhæmbɜːrɡər/", "汉堡包", "n.", "The hamburger is big.", "这个汉堡包很大。"),
        ("ice cream", "/ˌaɪs ˈkriːm/", "/ˌaɪs ˈkriːm/", "冰淇淋", "n.", "Ice cream is sweet.", "冰淇淋很甜。"),
        ("tea", "/tiː/", "/tiː/", "茶", "n.", "I drink tea.", "我喝茶。"),
        ("fresh", "/freʃ/", "/freʃ/", "新鲜的", "adj.", "The fruit is fresh.", "这水果很新鲜。"),
        ("healthy", "/ˈhelθi/", "/ˈhelθi/", "健康的", "adj.", "Vegetables are healthy.", "蔬菜很健康。"),
        ("delicious", "/dɪˈlɪʃəs/", "/dɪˈlɪʃəs/", "美味的", "adj.", "The food is delicious.", "食物很美味。"),
        ("sweet", "/swiːt/", "/swiːt/", "甜的", "adj.", "The cake is sweet.", "蛋糕很甜。"),
        ("hot", "/hɒt/", "/hɑːt/", "辣的", "adj.", "The food is hot.", "这食物很辣。"),
    ],
    (5, "上", 4, "Unit 4 What Can You Do"): [
        ("dance", "/dɑːns/", "/dæns/", "跳舞", "v.", "I can dance.", "我会跳舞。"),
        ("sing", "/sɪŋ/", "/sɪŋ/", "唱歌", "v.", "She can sing.", "她会唱歌。"),
        ("draw", "/drɔː/", "/drɔː/", "画画", "v.", "He can draw.", "他会画画。"),
        ("cook", "/kʊk/", "/kʊk/", "烹饪", "v.", "I can cook.", "我会做饭。"),
        ("swim", "/swɪm/", "/swɪm/", "游泳", "v.", "I can swim.", "我会游泳。"),
        ("speak", "/spiːk/", "/spiːk/", "说", "v.", "I can speak English.", "我会说英语。"),
        ("play", "/pleɪ/", "/pleɪ/", "玩", "v.", "I can play football.", "我会踢足球。"),
        ("do kung fu", "/duː kʌŋ fuː/", "/duː kʌŋ fuː/", "练武术", "v.", "He can do kung fu.", "他会练武术。"),
        ("cartoon", "/kɑːˈtuːn/", "/kɑːrˈtuːn/", "卡通", "n.", "I like cartoons.", "我喜欢卡通。"),
        ("wonderful", "/ˈwʌndəfl/", "/ˈwʌndərfl/", "精彩的", "adj.", "It's wonderful.", "它很精彩。"),
    ],
    (5, "上", 5, "Unit 5 There Is a Big Bed"): [
        ("clock", "/klɒk/", "/klɑːk/", "时钟", "n.", "The clock is on the wall.", "时钟在墙上。"),
        ("plant", "/plɑːnt/", "/plænt/", "植物", "n.", "The plant is green.", "植物是绿色的。"),
        ("bottle", "/ˈbɒtl/", "/ˈbɑːtl/", "瓶子", "n.", "The bottle is full.", "瓶子是满的。"),
        ("water bottle", "/ˈwɔːtə ˌbɒtl/", "/ˈwɔːtər ˌbɑːtl/", "水瓶", "n.", "This is my water bottle.", "这是我的水瓶。"),
        ("bike", "/baɪk/", "/baɪk/", "自行车", "n.", "I have a bike.", "我有一辆自行车。"),
        ("photo", "/ˈfəʊtəʊ/", "/ˈfoʊtoʊ/", "照片", "n.", "This is a photo.", "这是一张照片。"),
        ("front", "/frʌnt/", "/frʌnt/", "正面", "n.", "In front of the house.", "在房子前面。"),
        ("between", "/bɪˈtwiːn/", "/bɪˈtwiːn/", "在...中间", "prep.", "Between you and me.", "在你我之间。"),
        ("above", "/əˈbʌv/", "/əˈbʌv/", "在...上面", "prep.", "Above the tree.", "在树上面。"),
        ("beside", "/bɪˈsaɪd/", "/bɪˈsaɪd/", "在...旁边", "prep.", "Beside the window.", "在窗户旁边。"),
    ],
    (5, "上", 6, "Unit 6 In a Nature Park"): [
        ("forest", "/ˈfɒrɪst/", "/ˈfɔːrɪst/", "森林", "n.", "The forest is big.", "森林很大。"),
        ("river", "/ˈrɪvə/", "/ˈrɪvər/", "河流", "n.", "The river is long.", "河流很长。"),
        ("lake", "/leɪk/", "/leɪk/", "湖泊", "n.", "The lake is beautiful.", "湖泊很美丽。"),
        ("mountain", "/ˈmaʊntɪn/", "/ˈmaʊntn/", "高山", "n.", "The mountain is tall.", "高山很高。"),
        ("hill", "/hɪl/", "/hɪl/", "小山", "n.", "The hill is small.", "小山很小。"),
        ("tree", "/triː/", "/triː/", "树", "n.", "The tree is green.", "树是绿色的。"),
        ("bridge", "/brɪdʒ/", "/brɪdʒ/", "桥", "n.", "The bridge is long.", "桥很长。"),
        ("building", "/ˈbɪldɪŋ/", "/ˈbɪldɪŋ/", "建筑物", "n.", "The building is tall.", "建筑物很高。"),
        ("village", "/ˈvɪlɪdʒ/", "/ˈvɪlɪdʒ/", "村庄", "n.", "The village is small.", "村庄很小。"),
        ("house", "/haʊs/", "/haʊs/", "房屋", "n.", "The house is big.", "房屋很大。"),
    ],
}

# 五年级下册
GRADE5_VOLUME2 = {
    (5, "下", 1, "Unit 1 My Day"): [
        ("do morning exercises", "/duː ˈmɔːnɪŋ ˈeksəsaɪzɪz/", "/duː ˈmɔːrnɪŋ ˈeksərsaɪzɪz/", "做早操", "v.", "I do morning exercises.", "我做早操。"),
        ("have class", "/hæv klɑːs/", "/hæv klæs/", "上课", "v.", "I have class at 8.", "我 8 点上课。"),
        ("eat dinner", "/iːt ˈdɪnə/", "/iːt ˈdɪnər/", "吃晚饭", "v.", "I eat dinner at 6.", "我 6 点吃晚饭。"),
        ("exercise", "/ˈeksəsaɪz/", "/ˈeksərsaɪz/", "运动", "v.", "I exercise every day.", "我每天运动。"),
        ("play sports", "/pleɪ spɔːts/", "/pleɪ spɔːrts/", "进行体育运动", "v.", "I play sports.", "我进行体育运动。"),
        ("eat breakfast", "/iːt ˈbrekfəst/", "/iːt ˈbrekfəst/", "吃早饭", "v.", "I eat breakfast at 7.", "我 7 点吃早饭。"),
        ("clean", "/kliːn/", "/kliːn/", "打扫", "v.", "I clean my room.", "我打扫我的房间。"),
        ("go for a walk", "/ɡəʊ fɔːr ə wɔːk/", "/ɡoʊ fɔːr ə wɔːk/", "散步", "v.", "I go for a walk.", "我去散步。"),
        ("take", "/teɪk/", "/teɪk/", "上 (课)", "v.", "I take dancing class.", "我上舞蹈课。"),
        ("dance", "/dɑːns/", "/dæns/", "跳舞", "v.", "I dance on Saturday.", "我星期六跳舞。"),
    ],
    (5, "下", 2, "Unit 2 My Favourite Season"): [
        ("spring", "/sprɪŋ/", "/sprɪŋ/", "春天", "n.", "Spring is warm.", "春天很温暖。"),
        ("summer", "/ˈsʌmə/", "/ˈsʌmər/", "夏天", "n.", "Summer is hot.", "夏天很热。"),
        ("autumn", "/ˈɔːtəm/", "/ˈɔːtəm/", "秋天", "n.", "Autumn is cool.", "秋天很凉爽。"),
        ("winter", "/ˈwɪntə/", "/ˈwɪntər/", "冬天", "n.", "Winter is cold.", "冬天很冷。"),
        ("season", "/ˈsiːzn/", "/ˈsiːzn/", "季节", "n.", "My favourite season is spring.", "我最喜欢的季节是春天。"),
        ("picnic", "/ˈpɪknɪk/", "/ˈpɪknɪk/", "野餐", "n.", "We go for a picnic.", "我们去野餐。"),
        ("pick", "/pɪk/", "/pɪk/", "摘", "v.", "I pick apples.", "我摘苹果。"),
        ("snowman", "/ˈsnəʊmæn/", "/ˈsnoʊmæn/", "雪人", "n.", "I make a snowman.", "我堆雪人。"),
        ("vacation", "/vəˈkeɪʃn/", "/vəˈkeɪʃn/", "假期", "n.", "Summer vacation is long.", "暑假很长。"),
        ("leaf", "/liːf/", "/liːf/", "叶子", "n.", "The leaf is green.", "叶子是绿色的。"),
    ],
    (5, "下", 3, "Unit 3 My School Calendar"): [
        ("January", "/ˈdʒænjuəri/", "/ˈdʒænjueri/", "一月", "n.", "My birthday is in January.", "我的生日在一月。"),
        ("February", "/ˈfebruəri/", "/ˈfebrueri/", "二月", "n.", "It's cold in February.", "二月很冷。"),
        ("March", "/mɑːtʃ/", "/mɑːrtʃ/", "三月", "n.", "March is the third month.", "三月是第三个月。"),
        ("April", "/ˈeɪprəl/", "/ˈeɪprəl/", "四月", "n.", "April is warm.", "四月很温暖。"),
        ("May", "/meɪ/", "/meɪ/", "五月", "n.", "May is beautiful.", "五月很美丽。"),
        ("June", "/dʒuːn/", "/dʒuːn/", "六月", "n.", "Children's Day is in June.", "儿童节在六月。"),
        ("July", "/dʒuˈlaɪ/", "/dʒuˈlaɪ/", "七月", "n.", "July is hot.", "七月很热。"),
        ("August", "/ˈɔːɡəst/", "/ˈɔːɡəst/", "八月", "n.", "August is the eighth month.", "八月是第八个月。"),
        ("September", "/sepˈtembə/", "/sepˈtembər/", "九月", "n.", "School starts in September.", "学校九月开学。"),
        ("October", "/ɒkˈtəʊbə/", "/ɑːkˈtoʊbər/", "十月", "n.", "October is the tenth month.", "十月是第十个月。"),
        ("November", "/nəʊˈvembə/", "/noʊˈvembər/", "十一月", "n.", "November is cool.", "十一月很凉爽。"),
        ("December", "/dɪˈsembə/", "/dɪˈsembər/", "十二月", "n.", "Christmas is in December.", "圣诞节在十二月。"),
    ],
    (5, "下", 4, "Unit 4 When Is Easter"): [
        ("first", "/fɜːst/", "/fɜːrst/", "第一", "num.", "I am first.", "我是第一。"),
        ("second", "/ˈsekənd/", "/ˈsekənd/", "第二", "num.", "She is second.", "她是第二。"),
        ("third", "/θɜːd/", "/θɜːrd/", "第三", "num.", "He is third.", "他是第三。"),
        ("fourth", "/fɔːθ/", "/fɔːrθ/", "第四", "num.", "This is fourth.", "这是第四。"),
        ("fifth", "/fɪfθ/", "/fɪfθ/", "第五", "num.", "She is fifth.", "她是第五。"),
        ("twelfth", "/twelfθ/", "/twelfθ/", "第十二", "num.", "This is twelfth.", "这是第十二。"),
        ("twentieth", "/ˈtwentiəθ/", "/ˈtwentiəθ/", "第二十", "num.", "This is twentieth.", "这是第二十。"),
        ("thirtieth", "/ˈθɜːtiəθ/", "/ˈθɜːrtiəθ/", "第三十", "num.", "This is thirtieth.", "这是第三十。"),
        ("special", "/ˈspeʃl/", "/ˈspeʃl/", "特别的", "adj.", "It's a special day.", "这是特别的一天。"),
        ("fool", "/fuːl/", "/fuːl/", "愚人", "n.", "April Fool's Day.", "愚人节。"),
    ],
    (5, "下", 5, "Unit 5 Whose Dog Is It"): [
        ("mine", "/maɪn/", "/maɪn/", "我的", "pron.", "It's mine.", "它是我的。"),
        ("yours", "/jɔːz/", "/jɔːrz/", "你的", "pron.", "It's yours.", "它是你的。"),
        ("his", "/hɪz/", "/hɪz/", "他的", "pron.", "It's his.", "它是他的。"),
        ("hers", "/hɜːz/", "/hɜːrz/", "她的", "pron.", "It's hers.", "它是她的。"),
        ("theirs", "/ðeəz/", "/ðerz/", "他们的", "pron.", "It's theirs.", "它是他们的。"),
        ("ours", "/ˈaʊəz/", "/ˈaʊərz/", "我们的", "pron.", "It's ours.", "它是我们的。"),
        ("climb", "/klaɪm/", "/klaɪm/", "攀爬", "v.", "I can climb.", "我会攀爬。"),
        ("eat", "/iːt/", "/iːt/", "吃", "v.", "The dog is eating.", "狗正在吃。"),
        ("play", "/pleɪ/", "/pleɪ/", "玩", "v.", "The children are playing.", "孩子们正在玩。"),
        ("sleep", "/sliːp/", "/sliːp/", "睡觉", "v.", "The cat is sleeping.", "猫正在睡觉。"),
    ],
    (5, "下", 6, "Unit 6 Work Quietly"): [
        ("keep", "/kiːp/", "/kiːp/", "保持", "v.", "Keep quiet.", "保持安静。"),
        ("keep to the right", "/kiːp tuː ðə raɪt/", "/kiːp tuː ðə raɪt/", "靠右", "v.", "Keep to the right.", "靠右。"),
        ("talk", "/tɔːk/", "/tɔːk/", "说话", "v.", "Don't talk.", "不要说话。"),
        ("turn", "/tɜːn/", "/tɜːrn/", "顺序", "n.", "It's your turn.", "轮到你了。"),
        ("take turns", "/teɪk tɜːnz/", "/teɪk tɜːrnz/", "按顺序来", "v.", "Take turns.", "按顺序来。"),
        ("bamboo", "/bæmˈbuː/", "/bæmˈbuː/", "竹子", "n.", "Pandas eat bamboo.", "熊猫吃竹子。"),
        ("show", "/ʃəʊ/", "/ʃoʊ/", "展示", "v.", "Show me your book.", "给我看你的书。"),
        ("anything", "/ˈeniθɪŋ/", "/ˈeniθɪŋ/", "任何事物", "pron.", "Anything is OK.", "任何事物都可以。"),
        ("else", "/els/", "/els/", "另外", "adv.", "What else?", "还有什么？"),
        ("exhibition", "/ˌeksɪˈbɪʃn/", "/ˌeksɪˈbɪʃn/", "展览", "n.", "Go to the exhibition.", "去展览。"),
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

def import_grade5():
    print("=" * 60)
    print("人教版小学英语 (PEP) 五年级单词表导入工具")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_imported = 0

    all_units = {**GRADE5_VOLUME1, **GRADE5_VOLUME2}

    for (grade, semester, unit_no, unit_name), words in all_units.items():
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
    import_grade5()
