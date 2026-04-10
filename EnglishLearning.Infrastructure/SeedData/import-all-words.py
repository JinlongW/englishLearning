#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 完整单词表导入工具
一次性导入 3-6 年级所有单词数据
"""

import pyodbc
import sys

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

# ========== 三年级上册 ==========
GRADE3_VOL1 = {
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
}

# ========== 三年级下册 ==========
GRADE3_VOL2 = {
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

# ========== 四年级上册 ==========
GRADE4_VOL1 = {
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

# ========== 四年级下册 ==========
GRADE4_VOL2 = {
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

# ========== 五年级上册 ==========
GRADE5_VOL1 = {
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

# ========== 五年级下册 ==========
GRADE5_VOL2 = {
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

# ========== 六年级上册 ==========
GRADE6_VOL1 = {
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

# ========== 六年级下册 ==========
GRADE6_VOL2 = {
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

# ========== 合并所有数据 ==========
ALL_DATA = {
    **GRADE3_VOL1, **GRADE3_VOL2,
    **GRADE4_VOL1, **GRADE4_VOL2,
    **GRADE5_VOL1, **GRADE5_VOL2,
    **GRADE6_VOL1, **GRADE6_VOL2,
}

def get_unit_id(conn, grade, semester, unit_no):
    """获取单元 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def insert_word(conn, grade_unit_id, word_data):
    """插入单个单词"""
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
    print("3-6 年级上下册 (共 48 个单元)")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_imported = 0
    skipped = 0

    for (grade, semester, unit_no, unit_name), words in ALL_DATA.items():
        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[SKIP] 单元不存在：{grade}年级{semester}册 {unit_name}")
            skipped += 1
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
    print(f"导入完成！")
    print(f"  成功导入：{total_imported} 个单词")
    print(f"  跳过单元：{skipped} 个")
    print("=" * 60)

if __name__ == '__main__':
    main()
