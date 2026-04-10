#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 语法知识点和练习题目导入工具
为 3-6 年级每个单元导入 1 个语法知识点和 3 道练习题
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

# ========== 三年级上册语法和题目 ==========
GRADE3_VOL1_GRAMMAR = {
    1: {
        "title": "问候语 Hello/Hi",
        "content": {
            "introduction": "Hello 和 Hi 是最常用的英语问候语，用于见面时打招呼。",
            "examples": [
                {"en": "Hello! I am Mike.", "cn": "你好！我是迈克。"},
                {"en": "Hi! I am Sarah.", "cn": "嗨！我是莎拉。"}
            ],
            "notes": "Hello 比较正式，Hi 比较随意，两者可以互换使用。"
        }
    },
    2: {
        "title": "身体部位 this/that",
        "content": {
            "introduction": "This is...用于介绍近处的人或物，That is...用于介绍远处的人或物。",
            "examples": [
                {"en": "This is my face.", "cn": "这是我的脸。"},
                {"en": "That is my nose.", "cn": "那是我的鼻子。"}
            ],
            "notes": "this 指近处，that 指远处。"
        }
    },
    3: {
        "title": "颜色形容词",
        "content": {
            "introduction": "颜色词是形容词，用来描述物体的颜色。",
            "examples": [
                {"en": "The apple is red.", "cn": "苹果是红色的。"},
                {"en": "The sky is blue.", "cn": "天空是蓝色的。"}
            ],
            "notes": "颜色词放在 be 动词后面作表语。"
        }
    },
    4: {
        "title": "动物名词复数",
        "content": {
            "introduction": "英语中，表示多个动物时，名词要加 s 或 es 变成复数。",
            "examples": [
                {"en": "I see two pigs.", "cn": "我看见两头猪。"},
                {"en": "There are three ducks.", "cn": "有三只鸭子。"}
            ],
            "notes": "大多数名词直接加 s，以 s/x/ch/sh 结尾的加 es。"
        }
    },
    5: {
        "title": "请求句型 Can I have...",
        "content": {
            "introduction": "Can I have...?用于礼貌地请求要某物。",
            "examples": [
                {"en": "Can I have some juice?", "cn": "我能喝点果汁吗？"},
                {"en": "Can I have an egg?", "cn": "我能吃个鸡蛋吗？"}
            ],
            "notes": "some 用于肯定句，any 用于疑问句和否定句，但请求时可用 some 表示希望得到肯定回答。"
        }
    },
    6: {
        "title": "数字 1-10",
        "content": {
            "introduction": "学习用英语数数 1 到 10。",
            "examples": [
                {"en": "I have one book.", "cn": "我有一本书。"},
                {"en": "There are ten fingers.", "cn": "有十个手指。"}
            ],
            "notes": "数字后面接名词复数时，大于 1 的数字用复数名词。"
        }
    }
}

# ========== 三年级下册语法和题目 ==========
GRADE3_VOL2_GRAMMAR = {
    1: {
        "title": "国家与来源 I'm from...",
        "content": {
            "introduction": "I'm from...用于介绍自己来自哪里。",
            "examples": [
                {"en": "I'm from China.", "cn": "我来自中国。"},
                {"en": "She's from the USA.", "cn": "她来自美国。"}
            ],
            "notes": "from 是介词，后面接国家、城市等地点名词。"
        }
    },
    2: {
        "title": "家庭成员称呼",
        "content": {
            "introduction": "学习用英语称呼家庭成员。",
            "examples": [
                {"en": "This is my father.", "cn": "这是我的父亲。"},
                {"en": "She is my sister.", "cn": "她是我的姐姐/妹妹。"}
            ],
            "notes": "father 也可用 dad，mother 也可用 mom。"
        }
    },
    3: {
        "title": "形容词比较（大小高矮）",
        "content": {
            "introduction": "学习用形容词描述动物的特征。",
            "examples": [
                {"en": "The giraffe is tall.", "cn": "长颈鹿很高。"},
                {"en": "The monkey is small.", "cn": "猴子很小。"}
            ],
            "notes": "形容词放在 be 动词后面描述主语特征。"
        }
    },
    4: {
        "title": "方位介词 in/on/under",
        "content": {
            "introduction": "学习用介词描述物品的位置。",
            "examples": [
                {"en": "The pen is in the pencil box.", "cn": "钢笔在铅笔盒里。"},
                {"en": "The book is on the desk.", "cn": "书在桌子上。"}
            ],
            "notes": "in 表示在...里面，on 表示在...上面，under 表示在...下面。"
        }
    },
    5: {
        "title": "喜好表达 Do you like...?",
        "content": {
            "introduction": "Do you like...?用于询问对方是否喜欢某物。",
            "examples": [
                {"en": "Do you like pears?", "cn": "你喜欢梨吗？"},
                {"en": "Yes, I do.", "cn": "是的，我喜欢。"}
            ],
            "notes": "肯定回答 Yes, I do. 否定回答 No, I don't."
        }
    },
    6: {
        "title": "询问数量 How many...?",
        "content": {
            "introduction": "How many...?用于询问可数名词的数量。",
            "examples": [
                {"en": "How many kites can you see?", "cn": "你能看见多少只风筝？"},
                {"en": "I can see 12.", "cn": "我能看见 12 只。"}
            ],
            "notes": "How many 后面必须接名词复数。"
        }
    }
}

# ========== 四年级上册语法和题目 ==========
GRADE4_VOL1_GRAMMAR = {
    1: {
        "title": "教室物品与 there be 句型",
        "content": {
            "introduction": "There is...表示某处有某物（单数）。",
            "examples": [
                {"en": "There is a computer in the classroom.", "cn": "教室里有一台电脑。"},
                {"en": "There is a blackboard.", "cn": "有一块黑板。"}
            ],
            "notes": "There is 接单数名词，There are 接复数名词。"
        }
    },
    2: {
        "title": "书包里的物品询问",
        "content": {
            "introduction": "What's in your schoolbag?用于询问书包里有什么。",
            "examples": [
                {"en": "What's in your schoolbag?", "cn": "你书包里有什么？"},
                {"en": "Three storybooks and a math book.", "cn": "三本故事书和一本数学书。"}
            ],
            "notes": "storybook 的复数形式是 storybooks。"
        }
    },
    3: {
        "title": "描述朋友的外貌特征",
        "content": {
            "introduction": "学习用形容词描述人的外貌。",
            "examples": [
                {"en": "He is tall and strong.", "cn": "他又高又壮。"},
                {"en": "She has long hair.", "cn": "她有长头发。"}
            ],
            "notes": "be 动词后接形容词，have/has 后接名词。"
        }
    },
    4: {
        "title": "询问物品位置 Where is...?",
        "content": {
            "introduction": "Where is...?用于询问某物在哪里。",
            "examples": [
                {"en": "Where is my cat?", "cn": "我的猫在哪里？"},
                {"en": "Is it on the bed?", "cn": "它在床上吗？"}
            ],
            "notes": "回答用 It's in/on/under..."
        }
    },
    5: {
        "title": "晚餐食物询问 What's for dinner?",
        "content": {
            "introduction": "What's for dinner?用于询问晚餐吃什么。",
            "examples": [
                {"en": "What's for dinner?", "cn": "晚餐吃什么？"},
                {"en": "Some fish and soup.", "cn": "一些鱼和汤。"}
            ],
            "notes": "some 可以接可数名词复数或不可数名词。"
        }
    },
    6: {
        "title": "介绍家人 How many people...?",
        "content": {
            "introduction": "How many people are there in your family?询问家里有几口人。",
            "examples": [
                {"en": "How many people are there in your family?", "cn": "你家有几口人？"},
                {"en": "Three.", "cn": "三口人。"}
            ],
            "notes": "这是 there be 句型的特殊疑问句形式。"
        }
    }
}

# ========== 四年级下册语法和题目 ==========
GRADE4_VOL2_GRAMMAR = {
    1: {
        "title": "询问地点 Where is the...?",
        "content": {
            "introduction": "Where is the library?询问图书馆在哪里。",
            "examples": [
                {"en": "Where is the library?", "cn": "图书馆在哪里？"},
                {"en": "It's on the first floor.", "cn": "它在一楼。"}
            ],
            "notes": "floor 表示楼层，first floor 是一楼，second floor 是二楼。"
        }
    },
    2: {
        "title": "询问时间 What time is it?",
        "content": {
            "introduction": "What time is it?用于询问现在几点。",
            "examples": [
                {"en": "What time is it?", "cn": "现在几点了？"},
                {"en": "It's 9 o'clock.", "cn": "现在 9 点。"}
            ],
            "notes": "o'clock 表示整点。"
        }
    },
    3: {
        "title": "天气表达 It's...",
        "content": {
            "introduction": "学习用英语描述天气。",
            "examples": [
                {"en": "It's sunny today.", "cn": "今天阳光明媚。"},
                {"en": "It's rainy outside.", "cn": "外面在下雨。"}
            ],
            "notes": "sunny, rainy, cloudy, windy 等是描述天气的形容词。"
        }
    },
    4: {
        "title": "农场动物和蔬菜",
        "content": {
            "introduction": "学习农场动物和蔬菜的英语名称。",
            "examples": [
                {"en": "Are these carrots?", "cn": "这些是胡萝卜吗？"},
                {"en": "Yes, they are.", "cn": "是的，它们是。"}
            ],
            "notes": "these 是 this 的复数形式，those 是 that 的复数形式。"
        }
    },
    5: {
        "title": "衣物所有格 Whose...?",
        "content": {
            "introduction": "Whose coat is this?询问这件外套是谁的。",
            "examples": [
                {"en": "Whose coat is this?", "cn": "这是谁的外套？"},
                {"en": "It's mine.", "cn": "它是我的。"}
            ],
            "notes": "mine 是名词性物主代词，相当于 my + 名词。"
        }
    },
    6: {
        "title": "购物询问 Can I help you?",
        "content": {
            "introduction": "Can I help you?是购物时店员的常用语。",
            "examples": [
                {"en": "Can I help you?", "cn": "我能帮您吗？"},
                {"en": "Yes. Can I try that skirt on?", "cn": "是的。我能试穿那条裙子吗？"}
            ],
            "notes": "try on 表示试穿，试穿衣服用 try on，试穿鞋子也用 try on。"
        }
    }
}

# ========== 五年级上册语法和题目 ==========
GRADE5_VOL1_GRAMMAR = {
    1: {
        "title": "描述人物性格特征",
        "content": {
            "introduction": "学习用形容词描述人的性格特点。",
            "examples": [
                {"en": "He is very friendly.", "cn": "他很友好。"},
                {"en": "She is strict but kind.", "cn": "她很严厉但很和蔼。"}
            ],
            "notes": "friendly 友好的，strict 严厉的，kind 和蔼的。"
        }
    },
    2: {
        "title": "星期表达与课程安排",
        "content": {
            "introduction": "学习星期的英文表达和询问课程安排。",
            "examples": [
                {"en": "What do you have on Mondays?", "cn": "你星期一有什么课？"},
                {"en": "I have math and English.", "cn": "我有数学和英语课。"}
            ],
            "notes": "星期一到星期日：Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday。"
        }
    },
    3: {
        "title": "点餐句型 What would you like?",
        "content": {
            "introduction": "What would you like to eat/drink?用于询问对方想吃什么/喝什么。",
            "examples": [
                {"en": "What would you like to eat?", "cn": "你想吃什么？"},
                {"en": "I'd like a sandwich, please.", "cn": "我想要一个三明治。"}
            ],
            "notes": "I'd like = I would like，表示想要。"
        }
    },
    4: {
        "title": "能力表达 I can...",
        "content": {
            "introduction": "I can...用于表达自己会做什么。",
            "examples": [
                {"en": "I can sweep the floor.", "cn": "我会扫地。"},
                {"en": "Can you cook?", "cn": "你会做饭吗？"}
            ],
            "notes": "can 是情态动词，后面接动词原形。"
        }
    },
    5: {
        "title": "There be 句型（复习与拓展）",
        "content": {
            "introduction": "There be 句型表示某处有某物。",
            "examples": [
                {"en": "There is a big bed in my room.", "cn": "我的房间里有一张大床。"},
                {"en": "There are two closets.", "cn": "有两个衣柜。"}
            ],
            "notes": "There is + 单数/不可数名词，There are + 复数名词。"
        }
    },
    6: {
        "title": "自然公园与 there be 疑问句",
        "content": {
            "introduction": "Is there...?用于询问某处是否有某物。",
            "examples": [
                {"en": "Is there a river near the park?", "cn": "公园附近有一条河吗？"},
                {"en": "Yes, there is.", "cn": "是的，有。"}
            ],
            "notes": "Are there...?用于询问复数名词。"
        }
    }
}

# ========== 五年级下册语法和题目 ==========
GRADE5_VOL2_GRAMMAR = {
    1: {
        "title": "日常活动与频率副词",
        "content": {
            "introduction": "学习描述日常活动和频率副词的使用。",
            "examples": [
                {"en": "I usually get up at 7 o'clock.", "cn": "我通常 7 点起床。"},
                {"en": "I sometimes go hiking on weekends.", "cn": "我有时周末去远足。"}
            ],
            "notes": "频率副词：always 总是，usually 通常，often 经常，sometimes 有时，never 从不。"
        }
    },
    2: {
        "title": "季节与天气",
        "content": {
            "introduction": "学习描述季节和天气。",
            "examples": [
                {"en": "Which season do you like best?", "cn": "你最喜欢哪个季节？"},
                {"en": "I like spring best.", "cn": "我最喜欢春天。"}
            ],
            "notes": "四季：spring 春，summer 夏，fall/autumn 秋，winter 冬。"
        }
    },
    3: {
        "title": "月份与序数词",
        "content": {
            "introduction": "学习 12 个月份和序数词。",
            "examples": [
                {"en": "When is your birthday?", "cn": "你的生日是什么时候？"},
                {"en": "My birthday is on May 3rd.", "cn": "我的生日是 5 月 3 日。"}
            ],
            "notes": "序数词表示顺序：1st 第一，2nd 第二，3rd 第三，4th 第四..."
        }
    },
    4: {
        "title": "日期与节日",
        "content": {
            "introduction": "学习用英语表达日期和节日。",
            "examples": [
                {"en": "When is Easter?", "cn": "复活节是什么时候？"},
                {"en": "It's usually in April.", "cn": "通常在四月。"}
            ],
            "notes": "在月份前用介词 in，在具体日期前用 on。"
        }
    },
    5: {
        "title": "名词所有格",
        "content": {
            "introduction": "学习用名词所有格表示所属关系。",
            "examples": [
                {"en": "Whose dog is this?", "cn": "这是谁的狗？"},
                {"en": "It's Zhang Peng's.", "cn": "是张鹏的。"}
            ],
            "notes": "名词+'s 表示所有格，如 Mike's 表示 Mike 的。"
        }
    },
    6: {
        "title": "现在进行时",
        "content": {
            "introduction": "现在进行时表示正在进行的动作。",
            "examples": [
                {"en": "What are you doing?", "cn": "你在做什么？"},
                {"en": "I'm doing homework.", "cn": "我在做作业。"}
            ],
            "notes": "现在进行时：be(am/is/are) + 动词 ing 形式。"
        }
    }
}

# ========== 六年级上册语法和题目 ==========
GRADE6_VOL1_GRAMMAR = {
    1: {
        "title": "问路与指路",
        "content": {
            "introduction": "学习用英语问路和指路。",
            "examples": [
                {"en": "How can I get to the museum?", "cn": "我怎么去博物馆？"},
                {"en": "Turn left at the crossing.", "cn": "在十字路口左转。"}
            ],
            "notes": "turn left 左转，turn right 右转，go straight 直走。"
        }
    },
    2: {
        "title": "交通方式 by...",
        "content": {
            "introduction": "学习用 by 表达交通方式。",
            "examples": [
                {"en": "I go to school by bus.", "cn": "我乘公交车去学校。"},
                {"en": "She goes to work by bike.", "cn": "她骑自行车去上班。"}
            ],
            "notes": "by bus/plane/taxi/ship/subway/train，但 on foot 表示步行。"
        }
    },
    3: {
        "title": "将来计划 be going to",
        "content": {
            "introduction": "be going to 表示计划或打算做某事。",
            "examples": [
                {"en": "What are you going to do tonight?", "cn": "你今晚打算做什么？"},
                {"en": "I'm going to see a film.", "cn": "我打算看电影。"}
            ],
            "notes": "be going to + 动词原形，表示将来计划。"
        }
    },
    4: {
        "title": "一般现在时第三人称单数",
        "content": {
            "introduction": "一般现在时中，第三人称单数动词要加 s 或 es。",
            "examples": [
                {"en": "He likes reading books.", "cn": "他喜欢读书。"},
                {"en": "She goes hiking every weekend.", "cn": "她每个周末去远足。"}
            ],
            "notes": "动词后加 s，以 s/x/ch/sh/o 结尾的加 es。"
        }
    },
    5: {
        "title": "职业名称与询问",
        "content": {
            "introduction": "学习各种职业的英文名称。",
            "examples": [
                {"en": "What does your father do?", "cn": "你父亲是做什么的？"},
                {"en": "He is a doctor.", "cn": "他是一名医生。"}
            ],
            "notes": "询问职业：What does he/she do? 回答：He/She is a..."
        }
    },
    6: {
        "title": "情感表达 How do you feel?",
        "content": {
            "introduction": "学习用英语表达情感和感受。",
            "examples": [
                {"en": "How do you feel?", "cn": "你感觉怎么样？"},
                {"en": "I feel happy.", "cn": "我感到高兴。"}
            ],
            "notes": "情感形容词：happy 高兴，sad 难过，angry 生气，afraid 害怕，worried 担心。"
        }
    }
}

# ========== 六年级下册语法和题目 ==========
GRADE6_VOL2_GRAMMAR = {
    1: {
        "title": "形容词比较级",
        "content": {
            "introduction": "学习用比较级比较两者的差异。",
            "examples": [
                {"en": "I am taller than you.", "cn": "我比你高。"},
                {"en": "She is thinner than me.", "cn": "她比我瘦。"}
            ],
            "notes": "单音节词直接加 er：tall→taller，thin→thinner。"
        }
    },
    2: {
        "title": "一般过去时（规则动词）",
        "content": {
            "introduction": "一般过去时表示过去发生的动作。",
            "examples": [
                {"en": "I cleaned my room yesterday.", "cn": "我昨天打扫了房间。"},
                {"en": "She watched TV last night.", "cn": "她昨晚看电视了。"}
            ],
            "notes": "规则动词过去式加 ed：clean→cleaned，watch→watched。"
        }
    },
    3: {
        "title": "一般过去时（不规则动词）",
        "content": {
            "introduction": "不规则动词的过去式需要特别记忆。",
            "examples": [
                {"en": "I went to Beijing last week.", "cn": "我上周去了北京。"},
                {"en": "She ate fresh food yesterday.", "cn": "她昨天吃了新鲜食物。"}
            ],
            "notes": "go→went，eat→ate，take→took，buy→bought，see→saw。"
        }
    },
    4: {
        "title": "There be 句型过去式",
        "content": {
            "introduction": "There be 句型的过去式表示过去某处有某物。",
            "examples": [
                {"en": "There was no dining hall before.", "cn": "以前没有食堂。"},
                {"en": "There are many buildings now.", "cn": "现在有很多建筑物。"}
            ],
            "notes": "There was 接单数，There were 接复数。"
        }
    },
    5: {
        "title": "游戏活动表达",
        "content": {
            "introduction": "学习描述游戏和活动的英语表达。",
            "examples": [
                {"en": "Let's play a game.", "cn": "我们玩游戏吧。"},
                {"en": "We are on the same team.", "cn": "我们在同一个队。"}
            ],
            "notes": "team 队，player 运动员，win 赢，lose 输。"
        }
    },
    6: {
        "title": "告别与祝福",
        "content": {
            "introduction": "学习用英语告别和表达祝福。",
            "examples": [
                {"en": "Say goodbye to your friends.", "cn": "向你的朋友们说再见。"},
                {"en": "I will miss you.", "cn": "我会想念你。"}
            ],
            "notes": "farewell 告别，party 派对，share 分享，miss 想念。"
        }
    }
}

# ========== 练习题数据（每个单元 3 道题） ==========
QUESTIONS_TEMPLATE = {
    "single_choice": {
        "question_type": "single_choice",
        "difficulty": 1,
        "options": [
            {"key": "A", "text": "", "is_correct": True},
            {"key": "B", "text": "", "is_correct": False},
            {"key": "C", "text": "", "is_correct": False}
        ]
    }
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

def get_unit_id_by_no(conn, unit_no):
    """根据单元编号获取单元 ID（用于 4-6 年级）"""
    cursor = conn.cursor()
    # 计算年级和学期
    if unit_no <= 6:
        grade, semester = 3, "上"
    elif unit_no <= 12:
        grade, semester = 3, "下"
    elif unit_no <= 18:
        grade, semester = 4, "上"
    elif unit_no <= 24:
        grade, semester = 4, "下"
    elif unit_no <= 30:
        grade, semester = 5, "上"
    elif unit_no <= 36:
        grade, semester = 5, "下"
    elif unit_no <= 42:
        grade, semester = 6, "上"
    else:
        grade, semester = 6, "下"

    actual_unit_no = ((unit_no - 1) % 6) + 1

    cursor.execute(
        "SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?",
        (grade, semester, actual_unit_no)
    )
    row = cursor.fetchone()
    return row.id if row else None

def insert_grammar(conn, grade_unit_id, title, content_json, sort_order):
    """插入语法知识点"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_grammar (id, grade_unit_id, title, content_type, content_json, sort_order, passing_score, created_at)
        VALUES (NEWID(), ?, ?, 'article', ?, ?, 60, GETDATE())
    """, grade_unit_id, title, json.dumps(content_json, ensure_ascii=False), sort_order)
    conn.commit()

def insert_question(conn, grade_unit_id, question_type, difficulty, question_stem, correct_answer,
                   answer_analysis, knowledge_point, tags):
    """插入题目"""
    cursor = conn.cursor()
    question_id = str(json.dumps({}))  # 获取刚插入的 question ID
    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem,
                                correct_answer, answer_analysis, knowledge_point, tags, is_active, created_at, updated_at)
        VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
    """, grade_unit_id, question_type, difficulty, question_stem, correct_answer,
        answer_analysis, knowledge_point, tags)
    conn.commit()

    # 获取刚插入的题目 ID
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

def create_sample_questions(grade_unit_id, unit_name, knowledge_point):
    """为单元创建示例题目"""
    questions = [
        {
            "type": "single_choice",
            "difficulty": 1,
            "stem": f"关于本单元知识点\"{knowledge_point}\"，下列说法正确的是：",
            "answer": "A",
            "analysis": "这是本单元的核心知识点，需要重点掌握。",
            "tags": f"{knowledge_point},basic",
            "options": [
                {"key": "A", "text": "正确选项示例", "correct": True},
                {"key": "B", "text": "错误选项示例 1", "correct": False},
                {"key": "C", "text": "错误选项示例 2", "correct": False}
            ]
        },
        {
            "type": "single_choice",
            "difficulty": 2,
            "stem": "请选择正确的英语表达：",
            "answer": "A",
            "analysis": "注意英语表达的习惯用法。",
            "tags": f"{knowledge_point},application",
            "options": [
                {"key": "A", "text": "Hello! How are you?", "correct": True},
                {"key": "B", "text": "Hello! How is you?", "correct": False},
                {"key": "C", "text": "Hi! How are your?", "correct": False}
            ]
        },
        {
            "type": "single_choice",
            "difficulty": 2,
            "stem": "选择与中文意思相符的英文句子：",
            "answer": "A",
            "analysis": "理解句子的含义是学习外语的关键。",
            "tags": f"{knowledge_point},translation",
            "options": [
                {"key": "A", "text": "Good morning!", "correct": True},
                {"key": "B", "text": "Good afternoon!", "correct": False},
                {"key": "C", "text": "Good evening!", "correct": False}
            ]
        }
    ]
    return questions

def main():
    print("=" * 60)
    print("人教版小学英语 (PEP) 语法和练习题目导入工具")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    grammar_imported = 0
    questions_imported = 0

    # 各年级语法数据
    all_grammar = {
        (3, "上"): GRADE3_VOL1_GRAMMAR,
        (3, "下"): GRADE3_VOL2_GRAMMAR,
        (4, "上"): GRADE4_VOL1_GRAMMAR,
        (4, "下"): GRADE4_VOL2_GRAMMAR,
        (5, "上"): GRADE5_VOL1_GRAMMAR,
        (5, "下"): GRADE5_VOL2_GRAMMAR,
        (6, "上"): GRADE6_VOL1_GRAMMAR,
        (6, "下"): GRADE6_VOL2_GRAMMAR
    }

    for (grade, semester), grammar_data in all_grammar.items():
        for unit_no, grammar_info in grammar_data.items():
            unit_id = get_unit_id(conn, grade, semester, unit_no)
            if not unit_id:
                print(f"[SKIP] 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
                continue

            # 插入语法知识点
            insert_grammar(conn, unit_id, grammar_info["title"], grammar_info["content"], unit_no)
            grammar_imported += 1

            # 插入 3 道练习题
            sample_questions = create_sample_questions(unit_id, grammar_info["title"], grammar_info["title"])

            for q in sample_questions:
                question_id = insert_question(
                    conn, unit_id, q["type"], q["difficulty"], q["stem"],
                    q["answer"], q["analysis"], grammar_info["title"], q["tags"]
                )

                if question_id:
                    for idx, opt in enumerate(q["options"], 1):
                        insert_question_option(conn, question_id, opt["key"], opt["text"], idx)
                    questions_imported += 1

    conn.close()

    print("=" * 60)
    print(f"导入完成！")
    print(f"  语法知识点：{grammar_imported} 个")
    print(f"  练习题目：{questions_imported} 道")
    print("=" * 60)

if __name__ == '__main__':
    main()
