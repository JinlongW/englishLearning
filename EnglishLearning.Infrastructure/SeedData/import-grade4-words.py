#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 4-6 年级单词表导入工具
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

# 四年级上册
GRADE4_VOLUME1 = {
    (4, "上", 1, "Unit 1 My Classroom"): [
        ("classroom", "/ˈklɑːsruːm/", "/ˈklæsruːm/", "教室", "n.", "This is my classroom.", "这是我的教室。"),
        ("window", "/ˈwɪndəʊ/", "/ˈwɪndoʊ/", "窗户", "n.", "Open the window.", "打开窗户。"),
        ("blackboard", "/ˈblækbɔːd/", "/ˈblækbɔːrd/", "黑板", "n.", "Look at the blackboard.", "看黑板。"),
        ("light", "/laɪt/", "/laɪt/", "灯", "n.", "Turn on the light.", "打开灯。"),
        ("picture", "/ˈpɪktʃə/", "/ˈpɪktʃər/", "图画", "n.", "There is a picture on the wall.", "墙上有一幅画。"),
        ("door", "/dɔː/", "/dɔːr/", "门", "n.", "Close the door.", "关门。"),
        ("teacher's desk", "/ˈtiːtʃəz desk/", "/ˈtiːtʃərz desk/", "讲台", "n.", "The book is on the teacher's desk.", "书在讲台上。"),
        ("computer", "/kəmˈpjuːtə/", "/kəmˈpjuːtər/", "计算机", "n.", "We have a computer.", "我们有一台计算机。"),
    ],
    (4, "上", 2, "Unit 2 My Schoolbag"): [
        ("schoolbag", "/ˈskuːlbæɡ/", "/ˈskuːlbæɡ/", "书包", "n.", "My schoolbag is heavy.", "我的书包很重。"),
        ("maths book", "/mæθs bʊk/", "/mæθs bʊk/", "数学书", "n.", "I have a maths book.", "我有一本数学书。"),
        ("English book", "/ˈɪŋɡlɪʃ bʊk/", "/ˈɪŋɡlɪʃ bʊk/", "英语书", "n.", "Read your English book.", "读你的英语书。"),
        ("storybook", "/ˈstɔːribʊk/", "/ˈstɔːribʊk/", "故事书", "n.", "This is my storybook.", "这是我的故事书。"),
        ("candy", "/ˈkændi/", "/ˈkændi/", "糖果", "n.", "Do you like candy?", "你喜欢糖果吗？"),
        ("notebook", "/ˈnəʊtbʊk/", "/ˈnoʊtbʊk/", "笔记本", "n.", "Write in your notebook.", "在笔记本上写。"),
        ("toy", "/tɔɪ/", "/tɔɪ/", "玩具", "n.", "Put away your toy.", "收起你的玩具。"),
        ("key", "/kiː/", "/kiː/", "钥匙", "n.", "Where is my key?", "我的钥匙在哪里？"),
    ],
    (4, "上", 3, "Unit 3 My Friends"): [
        ("strong", "/strɒŋ/", "/strɔːŋ/", "强壮的", "adj.", "He is strong.", "他很强壮。"),
        ("friendly", "/ˈfrendli/", "/ˈfrendli/", "友好的", "adj.", "She is friendly.", "她很友好。"),
        ("quiet", "/ˈkwaɪət/", "/ˈkwaɪət/", "安静的", "adj.", "He is quiet.", "他很安静。"),
        ("hair", "/heə/", "/her/", "头发", "n.", "She has long hair.", "她有长头发。"),
        ("shoe", "/ʃuː/", "/ʃuː/", "鞋", "n.", "My shoe is new.", "我的鞋是新的。"),
        ("glasses", "/ˈɡlɑːsɪz/", "/ˈɡlæsɪz/", "眼镜", "n.", "He wears glasses.", "他戴眼镜。"),
        ("his", "/hɪz/", "/hɪz/", "他的", "pron.", "This is his book.", "这是他的书。"),
        ("her", "/hɜː/", "/hɜːr/", "她的", "pron.", "This is her bag.", "这是她的包。"),
        ("boy", "/bɔɪ/", "/bɔɪ/", "男孩", "n.", "The boy is tall.", "这个男孩很高。"),
    ],
    (4, "上", 4, "Unit 4 My Home"): [
        ("bedroom", "/ˈbedruːm/", "/ˈbedruːm/", "卧室", "n.", "This is my bedroom.", "这是我的卧室。"),
        ("living room", "/ˈlɪvɪŋ ruːm/", "/ˈlɪvɪŋ ruːm/", "客厅", "n.", "We watch TV in the living room.", "我们在客厅看电视。"),
        ("study", "/ˈstʌdi/", "/ˈstʌdi/", "书房", "n.", "I read books in the study.", "我在书房看书。"),
        ("kitchen", "/ˈkɪtʃɪn/", "/ˈkɪtʃɪn/", "厨房", "n.", "Mum is in the kitchen.", "妈妈在厨房。"),
        ("bathroom", "/ˈbɑːθruːm/", "/ˈbæθruːm/", "卫生间", "n.", "The bathroom is clean.", "卫生间很干净。"),
        ("bed", "/bed/", "/bed/", "床", "n.", "Go to bed.", "上床睡觉。"),
        ("phone", "/fəʊn/", "/foʊn/", "电话", "n.", "Answer the phone.", "接电话。"),
        ("table", "/ˈteɪbl/", "/ˈteɪbl/", "桌子", "n.", "Set the table.", "摆桌子。"),
    ],
    (4, "上", 5, "Unit 5 Dinner's Ready"): [
        ("beef", "/biːf/", "/biːf/", "牛肉", "n.", "I like beef.", "我喜欢牛肉。"),
        ("chicken", "/ˈtʃɪkɪn/", "/ˈtʃɪkɪn/", "鸡肉", "n.", "Chicken is delicious.", "鸡肉很美味。"),
        ("noodles", "/ˈnuːdlz/", "/ˈnuːdlz/", "面条", "n.", "I'd like some noodles.", "我想要些面条。"),
        ("soup", "/suːp/", "/suːp/", "汤", "n.", "Have some soup.", "喝点汤。"),
        ("vegetable", "/ˈvedʒtəbl/", "/ˈvedʒtəbl/", "蔬菜", "n.", "Eat your vegetables.", "吃你的蔬菜。"),
        ("chopsticks", "/ˈtʃɒpstɪks/", "/ˈtʃɑːpstɪks/", "筷子", "n.", "Use chopsticks.", "用筷子。"),
        ("bowl", "/bəʊl/", "/boʊl/", "碗", "n.", "Pass me the bowl.", "把碗递给我。"),
        ("fork", "/fɔːk/", "/fɔːrk/", "叉子", "n.", "Use the fork.", "用叉子。"),
        ("knife", "/naɪf/", "/naɪf/", "刀", "n.", "Cut with the knife.", "用刀切。"),
    ],
    (4, "上", 6, "Unit 6 Meet My Family"): [
        ("family", "/ˈfæmɪli/", "/ˈfæmɪli/", "家庭", "n.", "I love my family.", "我爱我的家庭。"),
        ("parents", "/ˈpeərənts/", "/ˈperənts/", "父母", "n.", "My parents love me.", "我的父母爱我。"),
        ("uncle", "/ˈʌŋkl/", "/ˈʌŋkl/", "舅舅", "n.", "My uncle is kind.", "我的舅舅很和蔼。"),
        ("aunt", "/ɑːnt/", "/ænt/", "阿姨", "n.", "My aunt is nice.", "我的阿姨很好。"),
        ("baby brother", "/ˈbeɪbi ˈbrʌðə/", "/ˈbeɪbi ˈbrʌðər/", "婴儿小弟弟", "n.", "The baby brother is cute.", "婴儿小弟弟很可爱。"),
        ("cousin", "/ˈkʌzn/", "/ˈkʌzn/", "表兄弟", "n.", "My cousin is my age.", "我的表兄弟和我同龄。"),
        ("driver", "/ˈdraɪvə/", "/ˈdraɪvər/", "司机", "n.", "He is a driver.", "他是一名司机。"),
        ("doctor", "/ˈdɒktə/", "/ˈdɑːktər/", "医生", "n.", "She is a doctor.", "她是一名医生。"),
        ("nurse", "/nɜːs/", "/nɜːrs/", "护士", "n.", "The nurse is kind.", "护士很和蔼。"),
        ("people", "/ˈpiːpl/", "/ˈpiːpl/", "人们", "n.", "There are three people.", "有三个人。"),
    ],
}

# 四年级下册
GRADE4_VOLUME2 = {
    (4, "下", 1, "Unit 1 My School"): [
        ("first floor", "/fɜːst flɔː/", "/fɜːrst flɔːr/", "一楼", "n.", "My classroom is on the first floor.", "我的教室在一楼。"),
        ("second floor", "/ˈsekənd flɔː/", "/ˈsekənd flɔːr/", "二楼", "n.", "The library is on the second floor.", "图书馆在二楼。"),
        ("teachers' office", "/ˈtiːtʃəz ˈɒfɪs/", "/ˈtiːtʃərz ˈɔːfɪs/", "教师办公室", "n.", "Go to the teachers' office.", "去教师办公室。"),
        ("library", "/ˈlaɪbrəri/", "/ˈlaɪbreri/", "图书馆", "n.", "Read a book in the library.", "在图书馆看书。"),
        ("playground", "/ˈpleɪɡraʊnd/", "/ˈpleɪɡraʊnd/", "操场", "n.", "Let's go to the playground.", "我们去操场吧。"),
        ("computer room", "/kəmˈpjuːtə ruːm/", "/kəmˈpjuːtər ruːm/", "计算机房", "n.", "We have a computer room.", "我们有一个计算机房。"),
        ("art room", "/ɑːt ruːm/", "/ɑːrt ruːm/", "美术教室", "n.", "Draw in the art room.", "在美术教室画画。"),
        ("music room", "/ˈmjuːzɪk ruːm/", "/ˈmjuːzɪk ruːm/", "音乐教室", "n.", "Sing in the music room.", "在音乐教室唱歌。"),
        ("next to", "/nekst tu/", "/nekst tu/", "紧邻", "prep.", "The library is next to the classroom.", "图书馆紧邻教室。"),
    ],
    (4, "下", 2, "Unit 2 What Time Is It"): [
        ("breakfast", "/ˈbrekfəst/", "/ˈbrekfəst/", "早餐", "n.", "It's time for breakfast.", "该吃早餐了。"),
        ("lunch", "/lʌntʃ/", "/lʌntʃ/", "午餐", "n.", "Have lunch at 12.", "12 点吃午餐。"),
        ("dinner", "/ˈdɪnə/", "/ˈdɪnər/", "晚餐", "n.", "Dinner is ready.", "晚餐准备好了。"),
        ("English class", "/ˈɪŋɡlɪʃ klɑːs/", "/ˈɪŋɡlɪʃ klæs/", "英语课", "n.", "I like English class.", "我喜欢英语课。"),
        ("music class", "/ˈmjuːzɪk klɑːs/", "/ˈmjuːzɪk klæs/", "音乐课", "n.", "It's time for music class.", "该上音乐课了。"),
        ("get up", "/ɡet ʌp/", "/ɡet ʌp/", "起床", "v.", "I get up at 7.", "我 7 点起床。"),
        ("go to school", "/ɡəʊ tuː skuːl/", "/ɡoʊ tuː skuːl/", "去上学", "v.", "I go to school at 8.", "我 8 点去上学。"),
        ("go home", "/ɡəʊ həʊm/", "/ɡoʊ hoʊm/", "回家", "v.", "I go home at 4.", "我 4 点回家。"),
        ("go to bed", "/ɡəʊ tuː bed/", "/ɡoʊ tuː bed/", "上床睡觉", "v.", "I go to bed at 9.", "我 9 点上床睡觉。"),
        ("o'clock", "/əˈklɒk/", "/əˈklɑːk/", "点钟", "n.", "It's 3 o'clock.", "现在 3 点钟。"),
    ],
    (4, "下", 3, "Unit 3 Weather"): [
        ("cold", "/kəʊld/", "/koʊld/", "寒冷的", "adj.", "It's cold today.", "今天很冷。"),
        ("cool", "/kuːl/", "/kuːl/", "凉爽的", "adj.", "The weather is cool.", "天气凉爽。"),
        ("hot", "/hɒt/", "/hɑːt/", "炎热的", "adj.", "It's hot in summer.", "夏天很热。"),
        ("warm", "/wɔːm/", "/wɔːrm/", "温暖的", "adj.", "It's warm today.", "今天很温暖。"),
        ("sunny", "/ˈsʌni/", "/ˈsʌni/", "晴朗的", "adj.", "It's sunny.", "天气晴朗。"),
        ("windy", "/ˈwɪndi/", "/ˈwɪndi/", "多风的", "adj.", "It's windy today.", "今天多风。"),
        ("cloudy", "/ˈklaʊdi/", "/ˈklaʊdi/", "多云的", "adj.", "It's cloudy.", "天气多云。"),
        ("snowy", "/ˈsnəʊi/", "/ˈsnoʊi/", "下雪的", "adj.", "It's snowy.", "天气下雪。"),
        ("rainy", "/ˈreɪni/", "/ˈreɪni/", "下雨的", "adj.", "It's rainy today.", "今天下雨。"),
    ],
    (4, "下", 4, "Unit 4 At the Farm"): [
        ("tomato", "/təˈmɑːtəʊ/", "/təˈmeɪtoʊ/", "西红柿", "n.", "The tomato is red.", "西红柿很红。"),
        ("potato", "/pəˈteɪtəʊ/", "/pəˈteɪtoʊ/", "土豆", "n.", "I like potatoes.", "我喜欢土豆。"),
        ("carrot", "/ˈkærət/", "/ˈkærət/", "胡萝卜", "n.", "Rabbits like carrots.", "兔子喜欢胡萝卜。"),
        ("green beans", "/ɡriːn biːnz/", "/ɡriːn biːnz/", "四季豆", "n.", "The green beans are long.", "四季豆很长。"),
        ("horse", "/hɔːs/", "/hɔːrs/", "马", "n.", "I see a horse.", "我看到一匹马。"),
        ("cow", "/kaʊ/", "/kaʊ/", "奶牛", "n.", "The cow gives milk.", "奶牛产奶。"),
        ("sheep", "/ʃiːp/", "/ʃiːp/", "绵羊", "n.", "The sheep is white.", "绵羊是白色的。"),
        ("hen", "/hen/", "/hen/", "母鸡", "n.", "The hen lays eggs.", "母鸡下蛋。"),
        ("farm", "/fɑːm/", "/fɑːrm/", "农场", "n.", "They work on a farm.", "他们在农场工作。"),
        ("garden", "/ˈɡɑːdn/", "/ˈɡɑːrdn/", "花园", "n.", "The garden is beautiful.", "花园很漂亮。"),
    ],
    (4, "下", 5, "Unit 5 My Clothes"): [
        ("clothes", "/kləʊðz/", "/kloʊðz/", "衣服", "n.", "Put on your clothes.", "穿上你的衣服。"),
        ("pants", "/pænts/", "/pænts/", "裤子", "n.", "My pants are blue.", "我的裤子是蓝色的。"),
        ("hat", "/hæt/", "/hæt/", "帽子", "n.", "Wear a hat.", "戴一顶帽子。"),
        ("dress", "/dres/", "/dres/", "连衣裙", "n.", "She wears a dress.", "她穿着连衣裙。"),
        ("skirt", "/skɜːt/", "/skɜːrt/", "女裙", "n.", "The skirt is pretty.", "这条女裙很漂亮。"),
        ("coat", "/kəʊt/", "/koʊt/", "外套", "n.", "Put on your coat.", "穿上你的外套。"),
        ("sweater", "/ˈswetə/", "/ˈswetər/", "毛衣", "n.", "The sweater is warm.", "毛衣很暖和。"),
        ("sock", "/sɒk/", "/sɑːk/", "短袜", "n.", "My socks are white.", "我的短袜是白色的。"),
        ("shorts", "/ʃɔːts/", "/ʃɔːrts/", "短裤", "n.", "Wear your shorts.", "穿你的短裤。"),
    ],
    (4, "下", 6, "Unit 6 Shopping"): [
        ("glove", "/ɡlʌv/", "/ɡlʌv/", "手套", "n.", "Put on your gloves.", "戴上你的手套。"),
        ("scarf", "/skɑːf/", "/skɑːrf/", "围巾", "n.", "The scarf is red.", "围巾是红色的。"),
        ("umbrella", "/ʌmˈbrelə/", "/ʌmˈbrelə/", "雨伞", "n.", "Take an umbrella.", "带把雨伞。"),
        ("sunglasses", "/ˈsʌnɡlɑːsɪz/", "/ˈsʌnɡlæsɪz/", "太阳镜", "n.", "Wear sunglasses.", "戴太阳镜。"),
        ("pretty", "/ˈprɪti/", "/ˈprɪti/", "漂亮的", "adj.", "The dress is pretty.", "这条连衣裙很漂亮。"),
        ("expensive", "/ɪkˈspensɪv/", "/ɪkˈspensɪv/", "昂贵的", "adj.", "It's too expensive.", "它太贵了。"),
        ("cheap", "/tʃiːp/", "/tʃiːp/", "便宜的", "adj.", "It's very cheap.", "它很便宜。"),
        ("nice", "/naɪs/", "/naɪs/", "好的", "adj.", "The shoes are nice.", "这双鞋很好。"),
        ("size", "/saɪz/", "/saɪz/", "尺码", "n.", "What size do you need?", "你需要什么尺码？"),
        ("try on", "/traɪ ɒn/", "/traɪ ɑːn/", "试穿", "v.", "Try on the shoes.", "试穿这双鞋。"),
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

def import_grade4():
    print("=" * 60)
    print("人教版小学英语 (PEP) 四年级单词表导入工具")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_imported = 0

    all_units = {**GRADE4_VOLUME1, **GRADE4_VOLUME2}

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
    import_grade4()
