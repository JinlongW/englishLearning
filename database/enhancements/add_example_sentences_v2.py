# -*- coding: utf-8 -*-
"""
例句数据添加工具 v2 - 扩展至 350 条
日期：2026-04-02
"""

import pyodbc

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

def get_word_id(conn, word):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tb_word WHERE word = ?", word)
    row = cursor.fetchone()
    return row.id if row else None

def insert_example(conn, word_id, sentence, translation, difficulty=1):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tb_example_sentence (word_id, example_sentence, translation, difficulty)
            VALUES (?, ?, ?, ?)
        """, (word_id, sentence, translation, difficulty))
        conn.commit()
        return True
    except Exception as e:
        return False

# 三年级核心词汇例句
GRADE3_EXAMPLES = {
    "hello": [
        ("Hello! I'm Amy.", "你好！我是艾米。"),
        ("Hello, nice to meet you.", "你好，很高兴见到你。"),
    ],
    "hi": [
        ("Hi! How are you?", "嗨！你好吗？"),
        ("Hi! Let's play.", "嗨！我们一起玩吧。"),
    ],
    "goodbye": [
        ("Goodbye! See you tomorrow.", "再见！明天见。"),
        ("Say goodbye to your friends.", "和你的朋友们说再见。"),
    ],
    "name": [
        ("What's your name?", "你叫什么名字？"),
        ("My name is John.", "我叫约翰。"),
    ],
    "I": [
        ("I am a student.", "我是一名学生。"),
        ("I like English.", "我喜欢英语。"),
    ],
    "am": [
        ("I am happy.", "我很开心。"),
        ("I am from China.", "我来自中国。"),
    ],
    "you": [
        ("You are my friend.", "你是我的朋友。"),
        ("How are you?", "你好吗？"),
    ],
    "he": [
        ("He is my brother.", "他是我的兄弟。"),
        ("He is tall.", "他很高。"),
    ],
    "she": [
        ("She is my sister.", "她是我的姐妹。"),
        ("She is nice.", "她很好。"),
    ],
    "my": [
        ("This is my book.", "这是我的书。"),
        ("I love my family.", "我爱我的家人。"),
    ],
    "your": [
        ("What's your name?", "你叫什么名字？"),
        ("Is this your pen?", "这是你的钢笔吗？"),
    ],
    "pen": [
        ("I have a pen.", "我有一支钢笔。"),
        ("Can I use your pen?", "我可以用你的钢笔吗？"),
    ],
    "pencil": [
        ("This is my pencil.", "这是我的铅笔。"),
        ("I draw with a pencil.", "我用铅笔画画。"),
    ],
    "ruler": [
        ("I have a ruler.", "我有一把尺子。"),
        ("The ruler is long.", "这把尺子很长。"),
    ],
    "bag": [
        ("This is my bag.", "这是我的包。"),
        ("I put my books in the bag.", "我把书放进包里。"),
    ],
    "face": [
        ("Touch your face.", "摸摸你的脸。"),
        ("She has a round face.", "她有一张圆脸。"),
    ],
    "nose": [
        ("Touch your nose.", "摸摸你的鼻子。"),
        ("My nose is small.", "我的鼻子很小。"),
    ],
    "ear": [
        ("I have two ears.", "我有两只耳朵。"),
        ("She covers her ear.", "她捂住耳朵。"),
    ],
    "mouth": [
        ("Open your mouth.", "张开你的嘴。"),
        ("She has a small mouth.", "她有一张小嘴。"),
    ],
    "arm": [
        ("Raise your arm.", "举起你的手臂。"),
        ("My arm hurts.", "我的手臂疼。"),
    ],
    "hand": [
        ("Clap your hands.", "拍拍你的手。"),
        ("I write with my hand.", "我用手写字。"),
    ],
    "leg": [
        ("I have two legs.", "我有两条腿。"),
        ("My leg is long.", "我的腿很长。"),
    ],
    "foot": [
        ("Stamp your foot.", "跺跺你的脚。"),
        ("My foot is big.", "我的脚很大。"),
    ],
    "red": [
        ("I like red.", "我喜欢红色。"),
        ("The apple is red.", "苹果是红色的。"),
    ],
    "blue": [
        ("The sky is blue.", "天空是蓝色的。"),
        ("I have a blue pen.", "我有一支蓝色的钢笔。"),
    ],
    "yellow": [
        ("The banana is yellow.", "香蕉是黄色的。"),
        ("I like yellow flowers.", "我喜欢黄色的花。"),
    ],
    "green": [
        ("The grass is green.", "草是绿色的。"),
        ("I have a green bag.", "我有一个绿色的包。"),
    ],
    "white": [
        ("The snow is white.", "雪是白色的。"),
        ("She wears a white dress.", "她穿着一条白色的裙子。"),
    ],
    "black": [
        ("The cat is black.", "这只猫是黑色的。"),
        ("I have black hair.", "我有黑色的头发。"),
    ],
    "brown": [
        ("The bear is brown.", "这只熊是棕色的。"),
        ("My eyes are brown.", "我的眼睛是棕色的。"),
    ],
    "one": [
        ("I have one apple.", "我有一个苹果。"),
        ("One plus one is two.", "一加一等于二。"),
    ],
    "two": [
        ("I have two hands.", "我有两只手。"),
        ("Two and two is four.", "二加二等于四。"),
    ],
    "three": [
        ("I see three birds.", "我看见三只鸟。"),
        ("One two three, let's go!", "一二三，我们走吧！"),
    ],
    "four": [
        ("There are four seasons.", "有四个季节。"),
        ("I have four books.", "我有四本书。"),
    ],
    "five": [
        ("I have five fingers.", "我有五个手指。"),
        ("Count to five.", "数到五。"),
    ],
    "six": [
        ("I am six years old.", "我六岁了。"),
        ("Six is my lucky number.", "六是我的幸运数字。"),
    ],
    "seven": [
        ("There are seven days in a week.", "一周有七天。"),
        ("I wake up at seven.", "我七点起床。"),
    ],
    "eight": [
        ("An octopus has eight legs.", "章鱼有八条腿。"),
        ("Eight is a big number.", "八是个大数字。"),
    ],
    "nine": [
        ("I have nine apples.", "我有九个苹果。"),
        ("Nine plus one is ten.", "九加一等于十。"),
    ],
    "ten": [
        ("I have ten fingers.", "我有十个手指。"),
        ("Count from one to ten.", "从一数到十。"),
    ],
}

# 四年级核心词汇例句
GRADE4_EXAMPLES = {
    "computer": [
        ("I use the computer to study.", "我用电脑学习。"),
        ("The computer is on the desk.", "电脑在书桌上。"),
    ],
    "desk": [
        ("My desk is clean.", "我的书桌很干净。"),
        ("There is a book on the desk.", "书桌上有一本书。"),
    ],
    "chair": [
        ("Sit on the chair.", "坐在椅子上。"),
        ("This chair is comfortable.", "这把椅子很舒服。"),
    ],
    "blackboard": [
        ("The teacher writes on the blackboard.", "老师在黑板上写字。"),
        ("Clean the blackboard, please.", "请擦黑板。"),
    ],
    "light": [
        ("Turn on the light.", "打开灯。"),
        ("The light is bright.", "灯光很亮。"),
    ],
    "picture": [
        ("I draw a picture.", "我画了一幅画。"),
        ("There is a picture on the wall.", "墙上有一幅画。"),
    ],
    "door": [
        ("Close the door, please.", "请关门。"),
        ("The door is open.", "门开着。"),
    ],
    "window": [
        ("Open the window.", "打开窗户。"),
        ("The window is clean.", "窗户很干净。"),
    ],
    "floor": [
        ("The floor is clean.", "地板很干净。"),
        ("Don't sit on the floor.", "不要坐在地板上。"),
    ],
    "maths": [
        ("I like maths class.", "我喜欢数学课。"),
        ("Maths is my favourite subject.", "数学是我最喜欢的科目。"),
    ],
    "Chinese": [
        ("I speak Chinese.", "我说中文。"),
        ("Chinese class is fun.", "语文课很有趣。"),
    ],
    "storybook": [
        ("I read a storybook.", "我在读故事书。"),
        ("This is my favourite storybook.", "这是我最喜欢的故事书。"),
    ],
    "notebook": [
        ("I write in my notebook.", "我在笔记本上写字。"),
        ("I have a new notebook.", "我有一本新笔记本。"),
    ],
    "candy": [
        ("I like candy.", "我喜欢糖果。"),
        ("Don't eat too much candy.", "不要吃太多糖果。"),
    ],
    "key": [
        ("Where is my key?", "我的钥匙在哪里？"),
        ("I put the key in the bag.", "我把钥匙放在包里。"),
    ],
    "beef": [
        ("I like beef.", "我喜欢牛肉。"),
        ("The beef is delicious.", "牛肉很美味。"),
    ],
    "chicken": [
        ("We eat chicken for dinner.", "我们晚餐吃鸡肉。"),
        ("The chicken is yummy.", "鸡肉很好吃。"),
    ],
    "noodles": [
        ("I eat noodles for breakfast.", "我早餐吃面条。"),
        ("Chinese noodles are long.", "中国面条很长。"),
    ],
    "vegetable": [
        ("Eat your vegetables.", "吃你的蔬菜。"),
        ("Vegetables are healthy.", "蔬菜很健康。"),
    ],
    "juice": [
        ("I drink orange juice.", "我喝橙汁。"),
        ("Juice is sweet.", "果汁很甜。"),
    ],
    "milk": [
        ("I drink milk every day.", "我每天喝牛奶。"),
        ("Milk is good for you.", "牛奶对你有好处。"),
    ],
    "coffee": [
        ("My dad drinks coffee.", "我爸爸喝咖啡。"),
        ("Coffee is hot.", "咖啡很烫。"),
    ],
    "tea": [
        ("My grandma drinks tea.", "我奶奶喝茶。"),
        ("Chinese tea is famous.", "中国茶很有名。"),
    ],
    "water": [
        ("Drink more water.", "多喝水。"),
        ("Water is important.", "水很重要。"),
    ],
}

# 五六年级核心词汇例句
GRADE5_6_EXAMPLES = {
    "Monday": [
        ("Today is Monday.", "今天是星期一。"),
        ("I have maths on Monday.", "我星期一有数学课。"),
    ],
    "Tuesday": [
        ("Tomorrow is Tuesday.", "明天是星期二。"),
        ("We have PE on Tuesday.", "我们星期二有体育课。"),
    ],
    "Wednesday": [
        ("Wednesday is mid-week.", "星期三是一周的中间。"),
        ("I go to school on Wednesday.", "我星期三上学。"),
    ],
    "Thursday": [
        ("Thursday comes after Wednesday.", "星期四在星期三之后。"),
        ("I have art on Thursday.", "我星期四有美术课。"),
    ],
    "Friday": [
        ("Friday is my favourite day.", "星期五是我最喜欢的一天。"),
        ("We have no homework on Friday.", "我们星期五没有作业。"),
    ],
    "Saturday": [
        ("Saturday is the weekend.", "星期六是周末。"),
        ("I play games on Saturday.", "我星期六玩游戏。"),
    ],
    "Sunday": [
        ("Sunday is a rest day.", "星期日是休息日。"),
        ("We visit grandparents on Sunday.", "我们星期日去看望祖父母。"),
    ],
    "January": [
        ("My birthday is in January.", "我的生日在一月。"),
        ("January is cold.", "一月很冷。"),
    ],
    "February": [
        ("February has 28 days.", "二月有 28 天。"),
        ("Spring Festival is in February.", "春节在二月。"),
    ],
    "March": [
        ("Women's Day is in March.", "妇女节在三月。"),
        ("Trees grow in March.", "树木在三月生长。"),
    ],
    "April": [
        ("April is spring.", "四月是春天。"),
        ("We have a picnic in April.", "我们四月去野餐。"),
    ],
    "May": [
        ("May Day is in May.", "五一劳动节在五月。"),
        ("Flowers bloom in May.", "花朵在五月盛开。"),
    ],
    "June": [
        ("Children's Day is in June.", "儿童节在六月。"),
        ("Summer starts in June.", "夏天从六月开始。"),
    ],
    "July": [
        ("Summer vacation is in July.", "暑假在七月。"),
        ("July is hot.", "七月很热。"),
    ],
    "August": [
        ("August is the hottest month.", "八月是最热的月份。"),
        ("We swim in August.", "我们八月游泳。"),
    ],
    "always": [
        ("I always get up early.", "我总是早起。"),
        ("She always helps others.", "她总是帮助别人。"),
    ],
    "usually": [
        ("I usually walk to school.", "我通常步行上学。"),
        ("He usually comes at 8.", "他通常 8 点来。"),
    ],
    "often": [
        ("I often read books.", "我经常看书。"),
        ("We often play together.", "我们经常一起玩。"),
    ],
    "sometimes": [
        ("Sometimes I watch TV.", "有时我看电视。"),
        ("Sometimes it rains in summer.", "夏天有时会下雨。"),
    ],
    "never": [
        ("I never lie.", "我从不说谎。"),
        ("She never gives up.", "她从不放弃。"),
    ],
    "tall": [
        ("He is very tall.", "他很高。"),
        ("The building is tall.", "这栋楼很高。"),
    ],
    "short": [
        ("She has short hair.", "她留着短发。"),
        ("The pencil is short.", "这支铅笔很短。"),
    ],
    "long": [
        ("Her hair is long.", "她的头发很长。"),
        ("The river is long.", "这条河很长。"),
    ],
    "young": [
        ("She is young.", "她很年轻。"),
        ("Young people are active.", "年轻人很活跃。"),
    ],
    "old": [
        ("He is old.", "他老了。"),
        ("This is an old book.", "这是一本旧书。"),
    ],
    "strong": [
        ("He is strong.", "他很强壮。"),
        ("The rope is strong.", "这根绳子很结实。"),
    ],
    "weak": [
        ("She feels weak.", "她感到虚弱。"),
        ("The signal is weak.", "信号很弱。"),
    ],
    "clever": [
        ("She is clever.", "她很聪明。"),
        ("The boy is clever.", "这个男孩很聪明。"),
    ],
    "lazy": [
        ("Don't be lazy.", "不要懒惰。"),
        ("The cat is lazy.", "这只猫很懒。"),
    ],
    "active": [
        ("She is active in class.", "她在课堂上很活跃。"),
        ("Active kids are healthy.", "活跃的孩子很健康。"),
    ],
    "quiet": [
        ("Be quiet, please.", "请安静。"),
        ("She is a quiet girl.", "她是个安静的女孩。"),
    ],
    "polite": [
        ("He is polite.", "他很有礼貌。"),
        ("Be polite to others.", "对别人要有礼貌。"),
    ],
    "helpful": [
        ("She is helpful.", "她很乐于助人。"),
        ("Helpful people are nice.", "乐于助人的人很好。"),
    ],
    "kind": [
        ("My teacher is kind.", "我的老师很和蔼。"),
        ("Be kind to animals.", "善待动物。"),
    ],
    "strict": [
        ("My dad is strict.", "我爸爸很严格。"),
        ("The rules are strict.", "规则很严格。"),
    ],
    "funny": [
        ("He is funny.", "他很滑稽。"),
        ("The story is funny.", "这个故事很有趣。"),
    ],
    "delicious": [
        ("The food is delicious.", "食物很美味。"),
        ("This cake is delicious.", "这个蛋糕很好吃。"),
    ],
    "fresh": [
        ("The air is fresh.", "空气很清新。"),
        ("The fruit is fresh.", "水果很新鲜。"),
    ],
    "healthy": [
        ("Vegetables are healthy.", "蔬菜很健康。"),
        ("Exercise keeps you healthy.", "运动让你健康。"),
    ],
    "sweet": [
        ("The candy is sweet.", "糖果很甜。"),
        ("She has a sweet voice.", "她有甜美的嗓音。"),
    ],
    "hot": [
        ("The soup is hot.", "汤很烫。"),
        ("Summer is hot.", "夏天很热。"),
    ],
    "cold": [
        ("The water is cold.", "水很冷。"),
        ("Winter is cold.", "冬天很冷。"),
    ],
    "warm": [
        ("It's warm today.", "今天很暖和。"),
        ("The sun is warm.", "阳光很温暖。"),
    ],
    "cool": [
        ("The weather is cool.", "天气很凉爽。"),
        ("That's cool!", "太酷了！"),
    ],
    "windy": [
        ("It's windy today.", "今天有风。"),
        ("Windy days are good for flying kites.", "有风的日子适合放风筝。"),
    ],
    "cloudy": [
        ("The sky is cloudy.", "天空多云。"),
        ("Cloudy days are cool.", "多云天很凉爽。"),
    ],
    "rainy": [
        ("I don't like rainy days.", "我不喜欢雨天。"),
        ("It's rainy outside.", "外面在下雨。"),
    ],
    "snowy": [
        ("It's snowy in winter.", "冬天下雪。"),
        ("Snowy days are beautiful.", "下雪天很美。"),
    ],
}

def main():
    print("=" * 60)
    print("     例句数据添加工具 v2 - 扩展至 350 条")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    total = 0
    success = 0
    not_found = 0

    # 三年级
    print("正在添加三年级例句...")
    for word, examples in GRADE3_EXAMPLES.items():
        word_id = get_word_id(conn, word)
        if not word_id:
            not_found += 1
            continue
        for sentence, translation in examples:
            if insert_example(conn, word_id, sentence, translation):
                success += 1
            total += 1

    # 四年级
    print("正在添加四年级例句...")
    for word, examples in GRADE4_EXAMPLES.items():
        word_id = get_word_id(conn, word)
        if not word_id:
            not_found += 1
            continue
        for sentence, translation in examples:
            if insert_example(conn, word_id, sentence, translation):
                success += 1
            total += 1

    # 五六年级
    print("正在添加五六年级例句...")
    for word, examples in GRADE5_6_EXAMPLES.items():
        word_id = get_word_id(conn, word)
        if not word_id:
            not_found += 1
            continue
        for sentence, translation in examples:
            if insert_example(conn, word_id, sentence, translation):
                success += 1
            total += 1

    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  尝试插入：{total} 条")
    print(f"  成功：{success} 条")
    print(f"  单词未找到：{not_found} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
