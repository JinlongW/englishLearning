#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 六年级单词表导入工具
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

# 六年级上册
GRADE6_VOLUME1 = {
    (6, "上", 1, "Unit 1 How Can I Get There"): [
        ("science", "/ˈsaɪəns/", "/ˈsaɪəns/", "科学", "n.", "I like science.", "我喜欢科学。"),
        ("museum", "/mjuːˈziːəm/", "/mjuːˈziːəm/", "博物馆", "n.", "We visit the museum.", "我们参观博物馆。"),
        ("post office", "/pəʊst ˈɒfɪs/", "/poʊst ˈɔːfɪs/", "邮局", "n.", "Go to the post office.", "去邮局。"),
        ("bookstore", "/ˈbʊkstɔː/", "/ˈbʊkstɔːr/", "书店", "n.", "I buy books at the bookstore.", "我在书店买书。"),
        ("cinema", "/ˈsɪnəmə/", "/ˈsɪnəmə/", "电影院", "n.", "Let's go to the cinema.", "我们去电影院吧。"),
        ("hospital", "/ˈhɒspɪtl/", "/ˈhɑːspɪtl/", "医院", "n.", "She works in a hospital.", "她在医院工作。"),
        ("crossing", "/ˈkrɒsɪŋ/", "/ˈkrɔːsɪŋ/", "十字路口", "n.", "Turn left at the crossing.", "在十字路口左转。"),
        ("turn", "/tɜːn/", "/tɜːrn/", "转弯", "v.", "Turn right here.", "在这里右转。"),
        ("left", "/left/", "/left/", "左边", "n.", "Turn left.", "左转。"),
        ("right", "/raɪt/", "/raɪt/", "右边", "n.", "Turn right.", "右转。"),
        ("straight", "/streɪt/", "/streɪt/", "直的", "adv.", "Go straight.", "直走。"),
    ],
    (6, "上", 2, "Unit 2 Ways to Go to School"): [
        ("on foot", "/ɒn fʊt/", "/ɑːn fʊt/", "步行", "prep.", "I go to school on foot.", "我步行去学校。"),
        ("by", "/baɪ/", "/baɪ/", "乘", "prep.", "I go by bus.", "我乘公交车去。"),
        ("bus", "/bʌs/", "/bʌs/", "公共汽车", "n.", "The bus is big.", "公共汽车很大。"),
        ("plane", "/pleɪn/", "/pleɪn/", "飞机", "n.", "I go by plane.", "我乘飞机去。"),
        ("taxi", "/ˈtæksi/", "/ˈtæksi/", "出租车", "n.", "Take a taxi.", "坐出租车。"),
        ("ship", "/ʃɪp/", "/ʃɪp/", "船", "n.", "Go by ship.", "乘船去。"),
        ("subway", "/ˈsʌbweɪ/", "/ˈsʌbweɪ/", "地铁", "n.", "Take the subway.", "坐地铁。"),
        ("train", "/treɪn/", "/treɪn/", "火车", "n.", "Go by train.", "乘火车去。"),
        ("slow", "/sləʊ/", "/sloʊ/", "慢的", "adj.", "Slow down.", "慢下来。"),
        ("down", "/daʊn/", "/daʊn/", "向下", "adv.", "Sit down.", "坐下。"),
        ("stop", "/stɒp/", "/stɑːp/", "停止", "v.", "Stop at the red light.", "红灯停。"),
    ],
    (6, "上", 3, "Unit 3 My Weekend Plan"): [
        ("visit", "/ˈvɪzɪt/", "/ˈvɪzɪt/", "拜访", "v.", "I visit my grandma.", "我拜访我的奶奶。"),
        ("film", "/fɪlm/", "/fɪlm/", "电影", "n.", "See a film.", "看电影。"),
        ("see a film", "/siː ə fɪlm/", "/siː ə fɪlm/", "看电影", "v.", "Let's see a film.", "我们看电影吧。"),
        ("trip", "/trɪp/", "/trɪp/", "旅行", "n.", "Take a trip.", "去旅行。"),
        ("supermarket", "/ˈsuːpəmɑːkɪt/", "/ˈsuːpərmɑːrkɪt/", "超市", "n.", "Go to the supermarket.", "去超市。"),
        ("evening", "/ˈiːvnɪŋ/", "/ˈiːvnɪŋ/", "晚上", "n.", "This evening.", "今天晚上。"),
        ("tonight", "/təˈnaɪt/", "/təˈnaɪt/", "今晚", "n.", "See you tonight.", "今晚见。"),
        ("tomorrow", "/təˈmɒrəʊ/", "/təˈmɔːroʊ/", "明天", "n.", "See you tomorrow.", "明天见。"),
        ("next week", "/nekst wiːk/", "/nekst wiːk/", "下周", "n.", "Next week is busy.", "下周很忙。"),
        ("dictionary", "/ˈdɪkʃənri/", "/ˈdɪkʃəneri/", "词典", "n.", "I have a dictionary.", "我有一本词典。"),
        ("comic", "/ˈkɒmɪk/", "/ˈkɑːmɪk/", "连环画", "n.", "Read a comic book.", "看连环画。"),
        ("word", "/wɜːd/", "/wɜːrd/", "单词", "n.", "Learn new words.", "学新单词。"),
    ],
    (6, "上", 4, "Unit 4 I Have a Pen Pal"): [
        ("pen pal", "/pen pæl/", "/pen pæl/", "笔友", "n.", "I have a pen pal.", "我有一个笔友。"),
        ("hobby", "/ˈhɒbi/", "/ˈhɑːbi/", "爱好", "n.", "My hobby is reading.", "我的爱好是阅读。"),
        ("jasmine", "/ˈdʒæzmɪn/", "/ˈdʒæzmɪn/", "茉莉", "n.", "I like jasmine.", "我喜欢茉莉。"),
        ("idea", "/aɪˈdɪə/", "/aɪˈdiːə/", "主意", "n.", "Good idea!", "好主意！"),
        ("can", "/kæn/", "/kæn/", "能", "v.", "I can swim.", "我会游泳。"),
        ("no", "/nəʊ/", "/noʊ/", "不", "int.", "No, I can't.", "不，我不会。"),
        ("not", "/nɒt/", "/nɑːt/", "不", "adv.", "I do not know.", "我不知道。"),
        ("Australia", "/ɒˈstreɪliə/", "/ɔːˈstreɪliə/", "澳大利亚", "n.", "He's from Australia.", "他来自澳大利亚。"),
        ("our", "/ˈaʊə/", "/ˈaʊər/", "我们的", "pron.", "This is our school.", "这是我们的学校。"),
        ("cook", "/kʊk/", "/kʊk/", "烹饪", "v.", "She cooks dinner.", "她做晚饭。"),
        ("go hiking", "/ɡəʊ ˈhaɪkɪŋ/", "/ɡoʊ ˈhaɪkɪŋ/", "去远足", "v.", "I go hiking.", "我去远足。"),
        ("puzzle", "/ˈpʌzl/", "/ˈpʌzl/", "谜", "n.", "Solve a puzzle.", "解谜。"),
    ],
    (6, "上", 5, "Unit 5 What Does He Do"): [
        ("factory", "/ˈfæktri/", "/ˈfæktri/", "工厂", "n.", "He works in a factory.", "他在工厂工作。"),
        ("worker", "/ˈwɜːkə/", "/ˈwɜːrkər/", "工人", "n.", "She is a worker.", "她是一名工人。"),
        ("postman", "/ˈpəʊstmən/", "/ˈpoʊstmən/", "邮递员", "n.", "He is a postman.", "他是一名邮递员。"),
        ("businessman", "/ˈbɪznəsmæn/", "/ˈbɪznəsmæn/", "商人", "n.", "He is a businessman.", "他是一名商人。"),
        ("police officer", "/pəˈliːs ˈɒfɪsə/", "/pəˈliːs ˈɔːfɪsər/", "警察", "n.", "She is a police officer.", "她是一名警察。"),
        ("fisherman", "/ˈfɪʃəmən/", "/ˈfɪʃərmən/", "渔民", "n.", "He is a fisherman.", "他是一名渔民。"),
        ("scientist", "/ˈsaɪəntɪst/", "/ˈsaɪəntɪst/", "科学家", "n.", "She is a scientist.", "她是一名科学家。"),
        ("pilot", "/ˈpaɪlət/", "/ˈpaɪlət/", "飞行员", "n.", "He is a pilot.", "他是一名飞行员。"),
        ("coach", "/kəʊtʃ/", "/koʊtʃ/", "教练", "n.", "She is a coach.", "她是一名教练。"),
        ("country", "/ˈkʌntri/", "/ˈkʌntri/", "国家", "n.", "I love my country.", "我爱我的国家。"),
        ("head teacher", "/hed ˈtiːtʃə/", "/hed ˈtiːtʃər/", "校长", "n.", "She is a head teacher.", "她是一名校长。"),
    ],
    (6, "上", 6, "Unit 6 How Do You Feel"): [
        ("angry", "/ˈæŋɡri/", "/ˈæŋɡri/", "生气的", "adj.", "He is angry.", "他很生气。"),
        ("afraid", "/əˈfreɪd/", "/əˈfreɪd/", "害怕的", "adj.", "She is afraid.", "她很害怕。"),
        ("sad", "/sæd/", "/sæd/", "难过的", "adj.", "I am sad.", "我很难过。"),
        ("worried", "/ˈwʌrid/", "/ˈwɜːrid/", "担心的", "adj.", "She is worried.", "她很担心。"),
        ("happy", "/ˈhæpi/", "/ˈhæpi/", "高兴的", "adj.", "I am happy.", "我很高兴。"),
        ("see", "/siː/", "/siː/", "看见", "v.", "I see a bird.", "我看见一只鸟。"),
        ("doctor", "/ˈdɒktə/", "/ˈdɑːktər/", "医生", "n.", "See a doctor.", "看医生。"),
        ("do", "/duː/", "/duː/", "做", "v.", "Do more exercise.", "多做运动。"),
        ("more", "/mɔː/", "/mɔːr/", "更多的", "adj.", "More water.", "更多的水。"),
        ("breath", "/breθ/", "/breθ/", "呼吸", "n.", "Take a deep breath.", "深呼吸。"),
        ("count", "/kaʊnt/", "/kaʊnt/", "数", "v.", "Count to ten.", "数到十。"),
        ("chase", "/tʃeɪs/", "/tʃeɪs/", "追赶", "v.", "The cat chases the mouse.", "猫追老鼠。"),
    ],
}

# 六年级下册
GRADE6_VOLUME2 = {
    (6, "下", 1, "Unit 1 How Tall Are You"): [
        ("tall", "/tɔːl/", "/tɔːl/", "高的", "adj.", "I am tall.", "我很高。"),
        ("short", "/ʃɔːt/", "/ʃɔːrt/", "矮的", "adj.", "He is short.", "他很矮。"),
        ("long", "/lɒŋ/", "/lɔːŋ/", "长的", "adj.", "My hair is long.", "我的头发很长。"),
        ("thin", "/θɪn/", "/θɪn/", "瘦的", "adj.", "She is thin.", "她很瘦。"),
        ("heavy", "/ˈhevi/", "/ˈhevi/", "重的", "adj.", "I am heavy.", "我很重。"),
        ("big", "/bɪɡ/", "/bɪɡ/", "大的", "adj.", "My bag is big.", "我的包很大。"),
        ("small", "/smɔːl/", "/smɔːl/", "小的", "adj.", "My room is small.", "我的房间很小。"),
        ("strong", "/strɒŋ/", "/strɔːŋ/", "强壮的", "adj.", "He is strong.", "他很强壮。"),
        ("old", "/əʊld/", "/oʊld/", "年老的", "adj.", "She is old.", "她很老。"),
        ("young", "/jʌŋ/", "/jʌŋ/", "年轻的", "adj.", "He is young.", "他很年轻。"),
        ("meter", "/ˈmiːtə/", "/ˈmiːtər/", "米", "n.", "I am 1.5 meters tall.", "我 1.5 米高。"),
        ("kilogram", "/ˈkɪləɡræm/", "/ˈkɪləɡræm/", "千克", "n.", "I weigh 50 kilograms.", "我重 50 千克。"),
    ],
    (6, "下", 2, "Unit 2 Last Weekend"): [
        ("clean", "/kliːn/", "/kliːn/", "打扫", "v.", "I cleaned my room.", "我打扫了我的房间。"),
        ("stay", "/steɪ/", "/steɪ/", "待", "v.", "I stayed at home.", "我待在家里。"),
        ("home", "/həʊm/", "/hoʊm/", "家", "n.", "Stay at home.", "待在家里。"),
        ("wash", "/wɒʃ/", "/wɑːʃ/", "洗", "v.", "I washed my clothes.", "我洗了我的衣服。"),
        ("watch", "/wɒtʃ/", "/wɑːtʃ/", "看", "v.", "I watched TV.", "我看了电视。"),
        ("read", "/riːd/", "/riːd/", "读", "v.", "I read a book.", "我读了一本书。"),
        ("see", "/siː/", "/siː/", "看见", "v.", "I saw a film.", "我看了一部电影。"),
        ("last", "/lɑːst/", "/læst/", "上一个的", "adj.", "Last weekend.", "上个周末。"),
        ("yesterday", "/ˈjestədeɪ/", "/ˈjestərdeɪ/", "昨天", "n.", "Yesterday was Sunday.", "昨天是星期日。"),
        ("before", "/bɪˈfɔː/", "/bɪˈfɔːr/", "在...之前", "prep.", "Before yesterday.", "在昨天之前。"),
        ("sleep", "/sliːp/", "/sliːp/", "睡觉", "v.", "I slept well.", "我睡得很好。"),
    ],
    (6, "下", 3, "Unit 3 Where Did You Go"): [
        ("go", "/ɡəʊ/", "/ɡoʊ/", "去", "v.", "I went to Beijing.", "我去了北京。"),
        ("camp", "/kæmp/", "/kæmp/", "露营", "v.", "I went camping.", "我去露营了。"),
        ("fish", "/fɪʃ/", "/fɪʃ/", "钓鱼", "v.", "I went fishing.", "我去钓鱼了。"),
        ("ride", "/raɪd/", "/raɪd/", "骑", "v.", "I rode a horse.", "我骑了一匹马。"),
        ("horse", "/hɔːs/", "/hɔːrs/", "马", "n.", "The horse is big.", "这匹马很大。"),
        ("hurt", "/hɜːt/", "/hɜːrt/", "受伤", "v.", "I hurt my foot.", "我的脚受伤了。"),
        ("eat", "/iːt/", "/iːt/", "吃", "v.", "I ate fresh food.", "我吃了新鲜食物。"),
        ("take", "/teɪk/", "/teɪk/", "拍照", "v.", "I took pictures.", "我拍了照片。"),
        ("buy", "/baɪ/", "/baɪ/", "买", "v.", "I bought a gift.", "我买了一份礼物。"),
        ("gift", "/ɡɪft/", "/ɡɪft/", "礼物", "n.", "This is a gift.", "这是一份礼物。"),
        ("fall", "/fɔːl/", "/fɔːl/", "摔倒", "v.", "I fell off the bike.", "我从自行车上摔下来了。"),
        ("off", "/ɒf/", "/ɔːf/", "从...落下", "prep.", "Fall off.", "从...落下。"),
    ],
    (6, "下", 4, "Unit 4 Then and Now"): [
        ("dining hall", "/ˈdaɪnɪŋ hɔːl/", "/ˈdaɪnɪŋ hɔːl/", "食堂", "n.", "There was no dining hall before.", "以前没有食堂。"),
        ("grass", "/ɡrɑːs/", "/ɡræs/", "草坪", "n.", "The grass is green.", "草坪是绿色的。"),
        ("gym", "/dʒɪm/", "/dʒɪm/", "体育馆", "n.", "We play in the gym.", "我们在体育馆玩。"),
        ("ago", "/əˈɡəʊ/", "/əˈɡoʊ/", "以前", "adv.", "Years ago.", "多年前。"),
        ("years ago", "/ˈjɪəz əɡəʊ/", "/ˈjɪrz əɡoʊ/", "几年前", "n.", "Three years ago.", "三年前。"),
        ("months ago", "/mʌnθs əɡəʊ/", "/mʌnθs əɡoʊ/", "几个月前", "n.", "Two months ago.", "两个月前。"),
        ("office", "/ˈɒfɪs/", "/ˈɔːfɪs/", "办公室", "n.", "This is my office.", "这是我的办公室。"),
        ("building", "/ˈbɪldɪŋ/", "/ˈbɪldɪŋ/", "建筑物", "n.", "The building is tall.", "建筑物很高。"),
        ("then", "/ðen/", "/ðen/", "那时", "adv.", "Then and now.", "那时和现在。"),
        ("change", "/tʃeɪndʒ/", "/tʃeɪndʒ/", "改变", "v.", "Things change.", "事情在改变。"),
        ("become", "/bɪˈkʌm/", "/bɪˈkʌm/", "变成", "v.", "I become taller.", "我变得更高了。"),
        ("feel", "/fiːl/", "/fiːl/", "感觉", "v.", "I feel happy.", "我感到高兴。"),
    ],
    (6, "下", 5, "Unit 5 Let's Play"): [
        ("children", "/ˈtʃɪldrən/", "/ˈtʃɪldrən/", "儿童", "n.", "The children are playing.", "孩子们在玩耍。"),
        ("game", "/ɡeɪm/", "/ɡeɪm/", "游戏", "n.", "Let's play a game.", "我们玩游戏吧。"),
        ("play", "/pleɪ/", "/pleɪ/", "玩", "v.", "I play with my friends.", "我和我的朋友们玩。"),
        ("together", "/təˈɡeðə/", "/təˈɡeðər/", "一起", "adv.", "Play together.", "一起玩。"),
        ("fun", "/fʌn/", "/fʌn/", "乐趣", "n.", "It's fun.", "它很有趣。"),
        ("exciting", "/ɪkˈsaɪtɪŋ/", "/ɪkˈsaɪtɪŋ/", "令人兴奋的", "adj.", "It's exciting.", "它令人兴奋。"),
        ("win", "/wɪn/", "/wɪn/", "赢", "v.", "I want to win.", "我想赢。"),
        ("lose", "/luːz/", "/luːz/", "输", "v.", "I don't want to lose.", "我不想输。"),
        ("team", "/tiːm/", "/tiːm/", "队", "n.", "We are a team.", "我们是一个队。"),
        ("player", "/ˈpleɪə/", "/ˈpleɪər/", "运动员", "n.", "He is a good player.", "他是一名好运动员。"),
    ],
    (6, "下", 6, "Unit 6 A Farewell Party"): [
        ("farewell", "/ˌfeəˈwel/", "/ˌferˈwel/", "告别", "n.", "A farewell party.", "一个告别派对。"),
        ("party", "/ˈpɑːti/", "/ˈpɑːrti/", "派对", "n.", "Have a party.", "举办派对。"),
        ("bring", "/brɪŋ/", "/brɪŋ/", "带来", "v.", "Bring some food.", "带些食物来。"),
        ("share", "/ʃeə/", "/ʃer/", "分享", "v.", "Share with friends.", "与朋友分享。"),
        ("say goodbye", "/seɪ ˌɡʊdˈbaɪ/", "/seɪ ˌɡʊdˈbaɪ/", "说再见", "v.", "Say goodbye to friends.", "向朋友说再见。"),
        ("write", "/raɪt/", "/raɪt/", "写", "v.", "Write a letter.", "写一封信。"),
        ("letter", "/ˈletə/", "/ˈletər/", "信", "n.", "I write a letter.", "我写了一封信。"),
        ("email", "/ˈiːmeɪl/", "/ˈiːmeɪl/", "电子邮件", "n.", "Send an email.", "发送电子邮件。"),
        ("address", "/əˈdres/", "/əˈdres/", "地址", "n.", "What's your address?", "你的地址是什么？"),
        ("phone", "/fəʊn/", "/foʊn/", "电话", "n.", "My phone number is...", "我的电话号码是..."),
        ("number", "/ˈnʌmbə/", "/ˈnʌmbər/", "号码", "n.", "Call my number.", "打我的号码。"),
        ("miss", "/mɪs/", "/mɪs/", "想念", "v.", "I will miss you.", "我会想念你。"),
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

def import_grade6():
    print("=" * 60)
    print("人教版小学英语 (PEP) 六年级单词表导入工具")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_imported = 0

    all_units = {**GRADE6_VOLUME1, **GRADE6_VOLUME2}

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
    import_grade6()
