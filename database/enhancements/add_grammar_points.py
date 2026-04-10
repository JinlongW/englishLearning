# -*- coding: utf-8 -*-
"""
语法知识点补充工具
日期：2026-04-02
说明：为语法知识点较少的单元补充语法内容
"""

import pyodbc
import json
import uuid

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

def get_unit_id(conn, grade, semester, unit_no):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))
    row = cursor.fetchone()
    return row.id if row else None

def get_grammar_count(conn, unit_id):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tb_grammar WHERE grade_unit_id = ?", unit_id)
    return cursor.fetchone()[0]

def insert_grammar(conn, unit_id, title, sections):
    content_json = json.dumps({"sections": sections}, ensure_ascii=False)
    cursor = conn.cursor()

    # 获取当前单元的最大 sort_order
    cursor.execute("SELECT ISNULL(MAX(sort_order), 0) + 1 FROM tb_grammar WHERE grade_unit_id = ?", unit_id)
    sort_order = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO tb_grammar (grade_unit_id, title, content_type, content_json, duration_seconds, sort_order, passing_score)
        VALUES (?, ?, 'article', ?, NULL, ?, 60)
    """, (unit_id, title, content_json, sort_order))
    conn.commit()
    return cursor.rowcount > 0

# 语法知识点数据 - 按单元组织
GRAMMAR_DATA = {
    # 三年级下册
    (3, '下', 1): [
        ("欢迎语 - Welcome back!", [
            {"title": "欢迎返回", "content": "Welcome back to school! (欢迎回到学校!)\nNice to see you again! (很高兴再次见到你!)"}
        ]),
        ("国家表达 - I'm from...", [
            {"title": "介绍来自哪里", "content": "I'm from China. (我来自中国)\nI'm from the UK. (我来自英国)\nI'm from the USA. (我来自美国)"}
        ])
    ],
    (3, '下', 2): [
        ("家庭成员 - This is my...", [
            {"title": "介绍家庭成员", "content": "This is my father. (这是我的父亲)\nThis is my mother. (这是我的母亲)\nThis is my family. (这是我的家人)"}
        ]),
        ("称呼语 - He's/She's...", [
            {"title": "称呼他人", "content": "He's my brother. (他是我的兄弟)\nShe's my sister. (她是我的姐妹)"}
        ])
    ],
    (3, '下', 3): [
        ("动物描述 - It's so...", [
            {"title": "描述动物特征", "content": "It's so tall! (它好高!)\nIt's so big! (它好大!)\nIt's so cute! (它好可爱!)"}
        ]),
        ("形容词 - big/small/long/short", [
            {"title": "形容词用法", "content": "big (大的) / small (小的)\nlong (长的) / short (短的)\nfat (胖的) / thin (瘦的)"}
        ])
    ],
    (3, '下', 4): [
        ("方位 - Where is...?", [
            {"title": "询问位置", "content": "Where is my car? (我的小汽车在哪里？)\nIt's in the desk. (它在书桌里)\nIt's under the chair. (它在椅子下面)"}
        ]),
        ("介词 - in/on/under", [
            {"title": "方位介词", "content": "in (在...里面)\non (在...上面)\nunder (在...下面)"}
        ])
    ],
    (3, '下', 5): [
        ("喜好询问 - Do you like...?", [
            {"title": "询问喜好", "content": "Do you like pears? (你喜欢梨吗？)\nYes, I do. (是的，我喜欢)\nNo, I don't. (不，我不喜欢)"}
        ]),
        ("水果名称", [
            {"title": "水果词汇", "content": "apple (苹果), pear (梨), banana (香蕉), orange (橙子)"}
        ])
    ],
    (3, '下', 6): [
        ("数字 11-20", [
            {"title": "数字表达", "content": "eleven (11), twelve (12), thirteen (13)\nfourteen (14), fifteen (15), sixteen (16)\nseventeen (17), eighteen (18), nineteen (19), twenty (20)"}
        ]),
        ("数量询问 - How many...?", [
            {"title": "询问数量", "content": "How many kites do you see? (你看见多少只风筝？)\nI see 12! (我看见 12 只!)"}
        ])
    ],
    # 四年级上册
    (4, '上', 3): [
        ("朋友描述 - He's/She's...", [
            {"title": "描述朋友", "content": "He's strong. (他很强壮)\nShe's thin. (她很瘦)\nHe's friendly. (他很友好)"}
        ]),
        ("姓名询问 - What's his/her name?", [
            {"title": "询问姓名", "content": "What's his name? (他叫什么名字？)\nHis name is Zhang Peng. (他的名字叫张鹏)\nHer name is Amy. (她的名字叫艾米)"}
        ])
    ],
    (4, '上', 4): [
        ("房间描述 - Is she in the...?", [
            {"title": "询问位置", "content": "Is she in the living room? (她在客厅吗？)\nYes, she is. (是的，她在)\nNo, she isn't. (不，她不在)"}
        ]),
        ("家居词汇", [
            {"title": "家居房间", "content": "living room (客厅), bedroom (卧室), kitchen (厨房), study (书房), bathroom (浴室)"}
        ])
    ],
    (4, '上', 5): [
        ("饮食喜好 - What would you like?", [
            {"title": "询问饮食需求", "content": "What would you like for dinner? (你晚餐想吃什么？)\nI'd like some fish, please. (我想要一些鱼)"}
        ]),
        ("餐具词汇", [
            {"title": "餐具名称", "content": "chopsticks (筷子), bowl (碗), fork (叉子), spoon (勺子), knife (刀)"}
        ])
    ],
    (4, '上', 6): [
        ("职业询问 - What's your uncle's job?", [
            {"title": "询问职业", "content": "What's your uncle's job? (你叔叔是做什么的？)\nHe's a driver. (他是司机)"}
        ]),
        ("职业词汇", [
            {"title": "职业名称", "content": "doctor (医生), nurse (护士), driver (司机), farmer (农民), cook (厨师)"}
        ])
    ],
    # 四年级下册
    (4, '下', 1): [
        ("学校设施 - This is the...", [
            {"title": "介绍学校设施", "content": "This is the library. (这是图书馆)\nThat is the playground. (那是操场)"}
        ]),
        ("位置询问 - Is this the...?", [
            {"title": "确认位置", "content": "Is this the teachers' office? (这是教师办公室吗？)\nYes, it is. (是的)\nNo, it isn't. (不是)"}
        ])
    ],
    (4, '下', 2): [
        ("时间询问 - What time is it?", [
            {"title": "询问时间", "content": "What time is it? (现在几点了？)\nIt's 7 o'clock. (现在 7 点)\nIt's time for breakfast. (是早餐时间了)"}
        ]),
        ("日常活动", [
            {"title": "日常活动表达", "content": "get up (起床), go to school (去上学), go home (回家), go to bed (上床睡觉)"}
        ])
    ],
    (4, '下', 3): [
        ("天气表达 - What's the weather like?", [
            {"title": "询问天气", "content": "What's the weather like in Beijing? (北京天气怎么样？)\nIt's sunny. (晴朗的)"}
        ]),
        ("天气词汇", [
            {"title": "天气形容词", "content": "sunny (晴朗的), cloudy (多云的), windy (有风的), rainy (下雨的), snowy (下雪的)"}
        ])
    ],
    (4, '下', 4): [
        ("农场动物 - Are these...?", [
            {"title": "确认复数", "content": "Are these carrots? (这些是胡萝卜吗？)\nYes, they are. (是的)\nNo, they aren't. (不是)"}
        ]),
        ("蔬菜词汇", [
            {"title": "蔬菜名称", "content": "tomato (西红柿), potato (土豆), carrot (胡萝卜), green beans (四季豆)"}
        ])
    ],
    (4, '下', 5): [
        ("衣物表达 - Whose coat is this?", [
            {"title": "询问所属", "content": "Whose coat is this? (这是谁的外套？)\nIt's mine. (是我的)\nIt's Amy's. (是艾米的)"}
        ]),
        ("衣物词汇", [
            {"title": "衣物名称", "content": "coat (外套), shirt (衬衫), skirt (裙子), dress (连衣裙), pants (裤子)"}
        ])
    ],
    (4, '下', 6): [
        ("价格询问 - How much is this?", [
            {"title": "询问价格", "content": "How much is this skirt? (这条裙子多少钱？)\nIt's 89 yuan. (89 元)"}
        ]),
        ("购物用语", [
            {"title": "购物表达", "content": "Can I help you? (需要帮忙吗？)\nI want to buy... (我想买...)"}
        ])
    ],
    # 五年级上册
    (5, '上', 3): [
        ("饮食偏好 - What's your favourite food?", [
            {"title": "询问最爱食物", "content": "What's your favourite food? (你最喜欢的食物是什么？)\nMy favourite food is noodles. (我最喜欢的食物是面条)"}
        ]),
        ("味道表达", [
            {"title": "味道形容词", "content": "delicious (美味的), healthy (健康的), sweet (甜的), hot (辣的)"}
        ])
    ],
    (5, '上', 4): [
        ("能力表达 - What can you do?", [
            {"title": "询问能力", "content": "What can you do? (你会做什么？)\nI can swim. (我会游泳)\nI can cook. (我会做饭)"}
        ]),
        ("家务活动", [
            {"title": "家务词汇", "content": "clean the room (打扫房间), wash clothes (洗衣服), cook dinner (做晚饭)"}
        ])
    ],
    (5, '上', 5): [
        ("存在句 - There is/are...", [
            {"title": "存在句用法", "content": "There is a bed in the room. (房间里有一张床)\nThere are two chairs. (有两把椅子)"}
        ]),
        ("房屋描述", [
            {"title": "房间物品", "content": "bed (床), sofa (沙发), table (桌子), chair (椅子), desk (书桌)"}
        ])
    ],
    (5, '上', 6): [
        ("自然景物 - Is there a...?", [
            {"title": "询问存在", "content": "Is there a river in the park? (公园里有河吗？)\nYes, there is. (是的)\nNo, there isn't. (没有)"}
        ]),
        ("自然词汇", [
            {"title": "自然景物", "content": "river (河), lake (湖), mountain (山), hill (小山), tree (树)"}
        ])
    ],
    # 五年级下册
    (5, '下', 1): [
        ("日常作息 - When do you...?", [
            {"title": "询问时间", "content": "When do you get up? (你什么时候起床？)\nI get up at 7 o'clock. (我 7 点起床)"}
        ]),
        ("频度副词", [
            {"title": "频度表达", "content": "always (总是), usually (通常), often (经常), sometimes (有时)"}
        ])
    ],
    (5, '下', 2): [
        ("季节偏好 - Which season do you like best?", [
            {"title": "询问最爱季节", "content": "Which season do you like best? (你最喜欢哪个季节？)\nI like spring best. (我最喜欢春天)"}
        ]),
        ("季节活动", [
            {"title": "季节活动", "content": "go on a picnic (去野餐), go swimming (去游泳), pick apples (摘苹果), make a snowman (堆雪人)"}
        ])
    ],
    (5, '下', 3): [
        ("月份表达 - When is...?", [
            {"title": "询问日期", "content": "When is your birthday? (你的生日是什么时候？)\nMy birthday is on May 2nd. (我的生日是 5 月 2 日)"}
        ]),
        ("序数词", [
            {"title": "序数词 (1-5)", "content": "first (第 1), second (第 2), third (第 3), fourth (第 4), fifth (第 5)"}
        ])
    ],
    (5, '下', 4): [
        ("日期表达 - When is Easter?", [
            {"title": "节日日期", "content": "When is Easter? (复活节是什么时候？)\nIt's in March or April. (在 3 月或 4 月)"}
        ]),
        ("节日词汇", [
            {"title": "节日名称", "content": "New Year's Day (元旦), Children's Day (儿童节), National Day (国庆节)"}
        ])
    ],
    (5, '下', 5): [
        ("所有格 - Whose dog is it?", [
            {"title": "名词所有格", "content": "It's Amy's dog. (这是艾米的狗)\nThe dog is hers. (这只狗是她的)"}
        ]),
        ("名词性物主代词", [
            {"title": "物主代词", "content": "mine (我的), yours (你的), his (他的), hers (她的), theirs (他们的)"}
        ])
    ],
    (5, '下', 6): [
        ("现在进行时 - What are they doing?", [
            {"title": "现在进行时", "content": "What are they doing? (他们在做什么？)\nThey are eating lunch. (他们在吃午饭)"}
        ]),
        ("动词-ing 形式", [
            {"title": "动词进行时", "content": "eating (正在吃), drinking (正在喝), reading (正在读), writing (正在写)"}
        ])
    ],
    # 六年级上册
    (6, '上', 4): [
        ("过去时 - There was/were...", [
            {"title": "一般过去时", "content": "There was no library before. (以前没有图书馆)\nNow there is a new one. (现在有一个新的)"}
        ]),
        ("今昔对比", [
            {"title": "对比表达", "content": "before (以前) / now (现在)\nold (旧的) / new (新的)"}
        ])
    ],
    (6, '上', 5): [
        ("职业梦想 - What are you going to be?", [
            {"title": "将来职业", "content": "What are you going to be? (你将来想做什么？)\nI'm going to be a scientist. (我想成为科学家)"}
        ]),
        ("职业词汇 2", [
            {"title": "职业名称", "content": "scientist (科学家), pilot (飞行员), coach (教练), police officer (警察)"}
        ])
    ],
    (6, '上', 6): [
        ("情感表达 - How do you feel?", [
            {"title": "询问感受", "content": "How do you feel? (你感觉怎么样？)\nI feel happy. (我感觉很开心)"}
        ]),
        ("情感词汇", [
            {"title": "情感形容词", "content": "happy (开心的), sad (难过的), angry (生气的), worried (担心的), afraid (害怕的)"}
        ])
    ],
    # 六年级下册
    (6, '下', 1): [
        ("比较级 - taller/shorter", [
            {"title": "形容词比较级", "content": "I'm taller than you. (我比你高)\nYou're shorter than me. (你比我矮)"}
        ]),
        ("身高体重询问", [
            {"title": "询问身高体重", "content": "How tall are you? (你多高？)\nI'm 1.65 meters. (我 1 米 65)"}
        ])
    ],
    (6, '下', 2): [
        ("过去时 - What did you do?", [
            {"title": "一般过去时", "content": "What did you do last weekend? (你上周末做了什么？)\nI cleaned my room. (我打扫了房间)"}
        ]),
        ("规则动词过去式", [
            {"title": "动词过去式", "content": "clean → cleaned, wash → washed, watch → watched, play → played"}
        ])
    ],
    (6, '下', 3): [
        ("假期活动 - Where did you go?", [
            {"title": "询问假期去向", "content": "Where did you go on your holiday? (你假期去了哪里？)\nI went to Turpan. (我去了吐鲁番)"}
        ]),
        ("不规则动词过去式", [
            {"title": "动词过去式", "content": "go → went, see → saw, buy → bought, eat → ate"}
        ])
    ],
    (6, '下', 4): [
        ("今昔对比 - Before/Now", [
            {"title": "过去与现在对比", "content": "Before, I was quiet. (以前我很安静)\nNow, I'm very active. (现在我很活跃)"}
        ]),
        ("变化表达", [
            {"title": "变化描述", "content": "I was... / Now I am... (我过去是.../现在我是...)"}
        ])
    ],
    (6, '下', 5): [
        ("告别聚会 - Let's have a party", [
            {"title": "聚会策划", "content": "Let's have a farewell party. (我们办个告别派对吧)\nThat's a good idea! (好主意!)"}
        ]),
        ("建议表达", [
            {"title": "提建议", "content": "Let's... (让我们...)\nHow about...? (...怎么样？)\nWhy not...? (为什么不...?)"}
        ])
    ],
    (6, '下', 6): [
        ("联系方式 - How can we stay in touch?", [
            {"title": "保持联系", "content": "How can we stay in touch? (我们怎么保持联系？)\nWe can write emails. (我们可以写邮件)"}
        ]),
        ("祝愿表达", [
            {"title": "美好祝愿", "content": "Wish you all the best! (祝你一切顺利!)\nGood luck! (祝好运!)"}
        ])
    ],
}

def main():
    print("=" * 60)
    print("     语法知识点补充工具")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    total = 0
    added = 0
    skipped = 0

    for (grade, semester, unit_no), grammars in GRAMMAR_DATA.items():
        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[NOT FOUND] {grade}年级{semester}册 Unit {unit_no}")
            continue

        current_count = get_grammar_count(conn, unit_id)
        print(f"\n{grade}年级{semester}册 Unit {unit_no} (现有：{current_count}个)")

        # 如果已有 2 个或以上语法点，跳过
        if current_count >= 2:
            print(f"  [SKIP] 已有足够的语法点")
            skipped += len(grammars)
            continue

        for title, sections in grammars:
            if insert_grammar(conn, unit_id, title, sections):
                print(f"  [OK] {title}")
                added += 1
                total += 1

    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  新增语法点：{added} 个")
    print(f"  跳过：{skipped} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
