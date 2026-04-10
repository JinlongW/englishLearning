#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人教版小学英语 (PEP) 全单元练习题导入工具
为所有 48 个单元添加高质量题目（每单元 5 道，共 240 道）
"""

import pyodbc
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_CONFIG = {'server': 'localhost', 'database': 'EnglishLearning', 'trusted_connection': 'yes'}

def get_connection_string():
    return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection={DB_CONFIG['trusted_connection']};"

def get_unit_id(conn, grade, semester, unit_no):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tb_grade_unit WHERE grade=? AND semester=? AND unit_no=?", (grade, semester, unit_no))
    row = cursor.fetchone()
    return row.id if row else None

def insert_question(conn, grade_unit_id, q):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem,
                                stem_audio_url, correct_answer, answer_analysis, knowledge_point,
                                tags, is_active, created_at, updated_at)
        VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
    """, grade_unit_id, q['type'], q['difficulty'], q['stem'], None, q['answer'], q['analysis'], q['knowledge_point'], q['tags'])
    conn.commit()
    cursor.execute("SELECT TOP 1 id FROM tb_question WHERE grade_unit_id=? AND question_stem=? ORDER BY created_at DESC", (grade_unit_id, q['stem']))
    row = cursor.fetchone()
    return row.id if row else None

def insert_option(conn, question_id, key, text, order):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_question_option (id, question_id, option_key, option_content, sort_order) VALUES (NEWID(), ?, ?, ?, ?)", question_id, key, text, order)
    conn.commit()

# 所有题目数据 - 48 个单元 x 5 题 = 240 题
ALL_QUESTIONS = {
    # 三年级上册
    (3,"上",1): [("single_choice",1,"下列哪个单词的意思是尺子？","A","ruler 的意思是尺子。","文具词汇","vocabulary",[("A","ruler"),("B","pencil"),("C","eraser"),("D","crayon")]),
                ("single_choice",1,"当你第一次见到新同学时，你应该说：","A","Hello! I'm... 是初次见面的标准问候语。","问候语","greeting",[("A","Hello! I'm Mike."),("B","Goodbye!"),("C","Thank you!"),("D","Sorry.")]),
                ("single_choice",2,"— Hello! I'm Sarah.\n— _____________","B","当别人自我介绍时，你也应该自我介绍作为回应。","对话应答","dialogue",[("A","Goodbye!"),("B","Hi! I'm Chen Jie."),("C","OK!"),("D","Bye!")]),
                ("fill_blank",2,"根据中文提示，填写单词：I have a ______ (尺子).","ruler","尺子的英文是 ruler。","单词拼写","spelling",[]),
                ("single_choice",1,"— I have a book.\n— _____________","A","Me too! 表示'我也是'。","Me too 句型","dialogue",[("A","Me too!"),("B","OK!"),("C","Bye!"),("D","Hello!")])],
    (3,"上",2): [("single_choice",1,"Touch your ______ (头).","A","head 是头的意思。","身体部位","vocabulary",[("A","head"),("B","face"),("C","nose"),("D","eye")]),
                ("single_choice",1,"I have two ______ (眼睛).","A","eyes 是眼睛的复数形式。","身体部位","vocabulary",[("A","eyes"),("B","ears"),("C","hands"),("D","arms")]),
                ("fill_blank",2,"This is my ______ (脸).","face","脸的英文是 face。","身体部位","spelling",[]),
                ("single_choice",2,"— Point to your nose!\n— _____________","A","OK! 表示同意对方的指令。","指令应答","dialogue",[("A","OK!"),("B","Hello!"),("C","Bye!"),("D","Thank you!")]),
                ("single_choice",1,"Clap your ______ (手).","C","hands 是手的意思。","身体部位","vocabulary",[("A","legs"),("B","feet"),("C","hands"),("D","arms")])],
    (3,"上",3): [("single_choice",1,"苹果是什么颜色的？","A","苹果通常是红色的。","颜色","vocabulary",[("A","red"),("B","blue"),("C","green"),("D","yellow")]),
                ("single_choice",1,"天空是什么颜色的？","B","天空通常是蓝色的。","颜色","vocabulary",[("A","red"),("B","blue"),("C","yellow"),("D","black")]),
                ("fill_blank",2,"The grass is ______ (绿色的).","green","绿色的英文是 green。","颜色","spelling",[]),
                ("single_choice",2,"香蕉是什么颜色的？","D","香蕉是黄色的。","颜色","vocabulary",[("A","red"),("B","blue"),("C","green"),("D","yellow")]),
                ("single_choice",2,"— Let's paint!\n— OK! I have ______ (红色的蜡笔).","A","红色的英文是 red。","颜色","vocabulary",[("A","red crayon"),("B","blue crayon"),("C","green crayon"),("D","yellow crayon")])],
    (3,"上",4): [("single_choice",1,"The ______ (猪) is fat.","A","pig 是猪的意思。","动物词汇","vocabulary",[("A","pig"),("B","bear"),("C","duck"),("D","bird")]),
                ("single_choice",1,"The ______ (大象) has a long nose.","B","elephant 是大象的意思。","动物词汇","vocabulary",[("A","tiger"),("B","elephant"),("C","monkey"),("D","panda")]),
                ("fill_blank",2,"Look at the ______ (熊猫). It's cute.","panda","熊猫的英文是 panda。","动物词汇","spelling",[]),
                ("single_choice",2,"— What's this?\n— It's a ______ (鸭子).","A","duck 是鸭子的意思。","动物词汇","vocabulary",[("A","duck"),("B","bird"),("C","bear"),("D","pig")]),
                ("single_choice",1,"Let's go to the ______ (动物园).","C","zoo 是动物园的意思。","地点词汇","vocabulary",[("A","school"),("B","park"),("C","zoo"),("D","home")])],
    (3,"上",5): [("single_choice",1,"I like ______ (面包).","A","bread 是面包的意思。","食物词汇","vocabulary",[("A","bread"),("B","rice"),("C","fish"),("D","egg")]),
                ("single_choice",1,"— Can I have some ______ (果汁)?\n— Here you are.","A","juice 是果汁的意思。","食物词汇","vocabulary",[("A","juice"),("B","water"),("C","milk"),("D","Coke")]),
                ("fill_blank",2,"I eat an ______ (鸡蛋) for breakfast.","egg","鸡蛋的英文是 egg。","食物词汇","spelling",[]),
                ("single_choice",2,"— Have some ______ (鱼).\n— Thank you.","A","fish 是鱼的意思。","食物词汇","vocabulary",[("A","fish"),("B","rice"),("C","bread"),("D","egg")]),
                ("single_choice",1,"Drink some ______ (水).","C","water 是水的意思。","食物词汇","vocabulary",[("A","juice"),("B","milk"),("C","water"),("D","Coke")])],
    (3,"上",6): [("single_choice",1,"— How many ______ (蜡烛)?\n— Five.","A","candles 是蜡烛的复数形式。","数字","vocabulary",[("A","candles"),("B","plates"),("C","gifts"),("D","balloons")]),
                ("single_choice",1,"— Happy Birthday!\n— _____________","A","收到生日祝福时应说谢谢。","日常交际","dialogue",[("A","Thank you!"),("B","OK!"),("C","Bye!"),("D","Hello!")]),
                ("fill_blank",2,"I am ______ (六) years old.","six","六的英文是 six。","数字","spelling",[]),
                ("single_choice",2,"— How old are you?\n— I'm ______ (十).","D","十的英文是 ten。","数字","vocabulary",[("A","one"),("B","five"),("C","eight"),("D","ten")]),
                ("single_choice",1,"Let's eat the birthday ______ (蛋糕).","A","cake 是蛋糕的意思。","食物词汇","vocabulary",[("A","cake"),("B","bread"),("C","egg"),("D","rice")])],
    # 三年级下册
    (3,"下",1): [("single_choice",1,"— I'm from ______ (中国).\n— Me too!","A","China 是中国的意思。","国家名称","vocabulary",[("A","China"),("B","USA"),("C","UK"),("D","Canada")]),
                ("single_choice",1,"— Where are you from?\n— I'm from ______ (美国).","B","USA 是美国的意思。","国家名称","vocabulary",[("A","China"),("B","USA"),("C","UK"),("D","Canada")]),
                ("fill_blank",2,"She is a new ______ (学生).","student","学生的英文是 student。","人物称呼","spelling",[]),
                ("single_choice",2,"— This is my friend.\n— Nice ______ you.","A","Nice to meet you. 是初次见面的礼貌用语。","日常交际","dialogue",[("A","to meet"),("B","meet"),("C","meeting"),("D","met")]),
                ("single_choice",1,"The UK is short for ______ (英国).","C","UK 是英国的缩写。","国家名称","vocabulary",[("A","China"),("B","USA"),("C","UK"),("D","Canada")])],
    (3,"下",2): [("single_choice",1,"This is my ______ (父亲).","A","father 是父亲的意思。","家庭成员","vocabulary",[("A","father"),("B","mother"),("C","brother"),("D","sister")]),
                ("single_choice",1,"She is my ______ (母亲).","B","mother 是母亲的意思。","家庭成员","vocabulary",[("A","father"),("B","mother"),("C","grandpa"),("D","grandma")]),
                ("fill_blank",2,"He is my ______ (哥哥/弟弟).","brother","哥哥或弟弟的英文是 brother。","家庭成员","spelling",[]),
                ("single_choice",2,"— Who's that woman?\n— She's my ______ (姐姐/妹妹).","A","sister 是姐姐或妹妹的意思。","家庭成员","vocabulary",[("A","sister"),("B","brother"),("C","father"),("D","mother")]),
                ("single_choice",1,"My ______ (祖父) is old.","C","grandpa 是祖父/外祖父的意思。","家庭成员","vocabulary",[("A","father"),("B","brother"),("C","grandpa"),("D","uncle")])],
    (3,"下",3): [("single_choice",1,"The giraffe is ______ (高的).","A","tall 是高的意思。","形容词","vocabulary",[("A","tall"),("B","short"),("C","fat"),("D","thin")]),
                ("single_choice",1,"The monkey is ______ (聪明的).","B","clever 是聪明的意思。","形容词","vocabulary",[("A","tall"),("B","clever"),("C","fat"),("D","big")]),
                ("fill_blank",2,"The elephant has a ______ (长的) nose.","long","长的英文是 long。","形容词","spelling",[]),
                ("single_choice",2,"The panda is ______ (可爱的).","A","cute 是可爱的意思。","形容词","vocabulary",[("A","cute"),("B","big"),("C","fat"),("D","tall")]),
                ("single_choice",1,"Look at that ______ (熊). It's fat.","A","bear 是熊的意思。","动物词汇","vocabulary",[("A","bear"),("B","pig"),("C","tiger"),("D","lion")])],
    (3,"下",4): [("single_choice",1,"— Where is my car?\n— It's ______ (在...下面) the desk.","A","under 是在...下面的意思。","方位介词","vocabulary",[("A","under"),("B","on"),("C","in"),("D","near")]),
                ("single_choice",1,"The book is ______ (在...上面) the chair.","B","on 是在...上面的意思。","方位介词","vocabulary",[("A","under"),("B","on"),("C","in"),("D","at")]),
                ("fill_blank",2,"My ball is ______ (在...里面) the box.","in","在...里面的英文是 in。","方位介词","spelling",[]),
                ("single_choice",2,"— Is it in your bag?\n— No, ______.","A","否定回答用 it isn't。","一般疑问句","grammar",[("A","it isn't"),("B","it is"),("C","is it"),("D","isn't it")]),
                ("single_choice",1,"Look ______ my new cap!","A","look at 是看的意思。","动词短语","vocabulary",[("A","at"),("B","to"),("C","on"),("D","in")])],
    (3,"下",5): [("single_choice",1,"— Do you like ______ (梨)?\n— Yes, I do.","A","pear 是梨的意思。","水果词汇","vocabulary",[("A","pears"),("B","apple"),("C","orange"),("D","banana")]),
                ("single_choice",1,"— Do you like oranges?\n— No, I ______.","B","否定回答用 don't。","一般疑问句","grammar",[("A","do"),("B","don't"),("C","does"),("D","doesn't")]),
                ("fill_blank",2,"I like ______ (苹果). They are sweet.","apples","苹果的英文是 apple，此处用复数。","水果词汇","spelling",[]),
                ("single_choice",2,"— Have some fruit.\n— _____________","A","接受别人的招待要说谢谢。","日常交际","dialogue",[("A","Thank you."),("B","No."),("C","OK."),("D","Bye.")]),
                ("single_choice",1,"The banana is ______ (黄色的).","A","yellow 是黄色的意思。","颜色","vocabulary",[("A","yellow"),("B","red"),("C","green"),("D","blue")])],
    (3,"下",6): [("single_choice",1,"— How many ______ (风筝) can you see?\n— I can see 12.","A","kite 是风筝的意思。","玩具词汇","vocabulary",[("A","kites"),("B","balls"),("C","cars"),("D","dolls")]),
                ("single_choice",1,"— Let's fly it!\n— _____________","A","OK! Great! 表示同意。","日常交际","dialogue",[("A","OK!"),("B","Bye!"),("C","No!"),("D","Sorry!")]),
                ("fill_blank",2,"I can see ______ (十一) birds.","eleven","十一的英文是 eleven。","数字","spelling",[]),
                ("single_choice",2,"— How many books do you have?\n— I have ______ (十五).","C","十五的英文是 fifteen。","数字","vocabulary",[("A","twelve"),("B","thirteen"),("C","fifteen"),("D","twenty")]),
                ("single_choice",1,"The black one ______ a bird!","A","主语是 the black one，谓语用 is。","be 动词","grammar",[("A","is"),("B","are"),("C","am"),("D","be")])],
    # 四年级上册
    (4,"上",1): [("single_choice",1,"We study in the ______ (教室).","A","classroom 是教室的意思。","教室物品","vocabulary",[("A","classroom"),("B","window"),("C","door"),("D","light")]),
                ("single_choice",2,"— ______ is in the classroom?\n— A blackboard.","A","What's 用于询问有什么。","特殊疑问句","grammar",[("A","What's"),("B","Where's"),("C","Who's"),("D","How's")]),
                ("fill_blank",2,"There ______ a computer in my classroom.","is","There be 句型，单数用 is。","There be 句型","grammar",[]),
                ("single_choice",2,"— Let's clean the classroom!\n— _____________","A","Good idea! 表示同意。","建议句型","dialogue",[("A","Good idea!"),("B","Thank you!"),("C","Bye!"),("D","Sorry!")]),
                ("single_choice",1,"Open the ______ (门), please.","A","door 是门的意思。","教室物品","vocabulary",[("A","door"),("B","window"),("C","blackboard"),("D","picture")])],
    (4,"上",2): [("single_choice",1,"I have a new ______ (书包).","A","schoolbag 是书包的意思。","学习用品","vocabulary",[("A","schoolbag"),("B","bag"),("C","book"),("D","pen")]),
                ("single_choice",1,"— What's in your schoolbag?\n— Three ______ (故事书).","A","storybook 的复数是 storybooks。","名词复数","vocabulary",[("A","storybooks"),("B","storybook"),("C","story"),("D","books")]),
                ("fill_blank",2,"Put your ______ (数学书) in your desk.","math book","数学书的英文是 math book。","学习用品","spelling",[]),
                ("single_choice",2,"— Is this your pen?\n— No, it ______.","B","否定回答用 isn't。","一般疑问句","grammar",[("A","is"),("B","isn't"),("C","does"),("D","don't")]),
                ("single_choice",1,"I have an ______ (英语书).","A","English book 是英语书的意思。","学习用品","vocabulary",[("A","English book"),("B","math book"),("C","Chinese book"),("D","story book")])],
    (4,"上",3): [("single_choice",1,"He is tall and ______ (强壮的).","A","strong 是强壮的意思。","描述人物","vocabulary",[("A","strong"),("B","thin"),("C","short"),("D","small")]),
                ("single_choice",1,"She has ______ (长的) hair.","A","long 是长的意思。","描述人物","vocabulary",[("A","long"),("B","short"),("C","big"),("D","small")]),
                ("fill_blank",2,"My friend is very ______ (友好的).","friendly","友好的英文是 friendly。","描述人物","spelling",[]),
                ("single_choice",2,"— What's his name?\n— ______ name is Zhang Peng.","A","他的名字用 His name。","物主代词","grammar",[("A","His"),("B","Her"),("C","Its"),("D","He's")]),
                ("single_choice",1,"— A boy or ______ (女孩)?\n— A boy.","C","girl 是女孩的意思。","人物称呼","vocabulary",[("A","boy"),("B","man"),("C","girl"),("D","woman")])],
    (4,"上",4): [("single_choice",1,"— Is she in the ______ (卧室)?\n— Yes, she is.","A","bedroom 是卧室的意思。","房间词汇","vocabulary",[("A","bedroom"),("B","living room"),("C","kitchen"),("D","bathroom")]),
                ("single_choice",1,"Go to the ______ (客厅). Watch TV.","B","living room 是客厅的意思。","房间词汇","vocabulary",[("A","bedroom"),("B","living room"),("C","kitchen"),("D","study")]),
                ("fill_blank",2,"Take a shower in the ______ (浴室).","bathroom","浴室的英文是 bathroom。","房间词汇","spelling",[]),
                ("single_choice",2,"— Are they on the table?\n— Yes, ______ are.","A","肯定回答用 they are。","一般疑问句","grammar",[("A","they"),("B","there"),("C","it"),("D","we")]),
                ("single_choice",1,"I can see a sofa in the ______ (家).","A","home 是家的意思。","地点词汇","vocabulary",[("A","home"),("B","school"),("C","park"),("D","shop")])],
    (4,"上",5): [("single_choice",1,"What's ______ (晚餐) ready?","A","dinner 是晚餐的意思。","食物词汇","vocabulary",[("A","dinner"),("B","lunch"),("C","breakfast"),("D","meal")]),
                ("single_choice",1,"I'd like some ______ (牛肉), please.","A","beef 是牛肉的意思。","食物词汇","vocabulary",[("A","beef"),("B","chicken"),("C","fish"),("D","pork")]),
                ("fill_blank",2,"Pass me a ______ (盘子), please.","plate","盘子的英文是 plate。","餐具词汇","spelling",[]),
                ("single_choice",2,"— What would you like?\n— I'd like some ______ (汤).","A","soup 是汤的意思。","食物词汇","vocabulary",[("A","soup"),("B","water"),("C","juice"),("D","milk")]),
                ("single_choice",1,"Use the ______ (筷子) to eat rice.","C","chopsticks 是筷子的意思。","餐具词汇","vocabulary",[("A","knife"),("B","fork"),("C","chopsticks"),("D","spoon")])],
    (4,"上",6): [("single_choice",1,"My family has six ______ (人).","A","people 是人的意思，单复数同形。","家庭成员","vocabulary",[("A","people"),("B","person"),("C","man"),("D","woman")]),
                ("single_choice",1,"— Is this your ______ (叔叔)?\n— Yes, it is.","A","uncle 是叔叔的意思。","家庭成员","vocabulary",[("A","uncle"),("B","aunt"),("C","cousin"),("D","grandpa")]),
                ("fill_blank",2,"My ______ (表妹) is a student.","cousin","表妹/堂妹的英文是 cousin。","家庭成员","spelling",[]),
                ("single_choice",2,"— How many people are there in your family?\n— ______.","A","询问家庭人口数量的回答。","数量问答","dialogue",[("A","Three"),("B","Three years old"),("C","Three o'clock"),("D","Three meters")]),
                ("single_choice",1,"My ______ (父母) love me.","A","parents 是父母的意思。","家庭成员","vocabulary",[("A","parents"),("B","parent"),("C","father"),("D","mother")])],
    # 四年级下册
    (4,"下",1): [("single_choice",1,"— Where is the ______ (图书馆)?\n— It's on the first floor.","A","library 是图书馆的意思。","地点词汇","vocabulary",[("A","library"),("B","classroom"),("C","office"),("D","hall")]),
                ("single_choice",1,"The teachers' ______ (办公室) is big.","A","office 是办公室的意思。","地点词汇","vocabulary",[("A","office"),("B","classroom"),("C","library"),("D","gate")]),
                ("fill_blank",2,"Welcome to our ______ (学校)!","school","学校的英文是 school。","地点词汇","spelling",[]),
                ("single_choice",2,"— Is this the teachers' office?\n— No, it ______.","B","否定回答用 isn't。","一般疑问句","grammar",[("A","is"),("B","isn't"),("C","doesn't"),("D","don't")]),
                ("single_choice",1,"It's ______ (在...旁边) the office.","A","next to 是在...旁边的意思。","方位介词","vocabulary",[("A","next to"),("B","next"),("C","near to"),("D","near of")])],
    (4,"下",2): [("single_choice",1,"— What time is it?\n— It's ______ (九点) o'clock.","A","nine 是九的意思。","时间表达","vocabulary",[("A","nine"),("B","eight"),("C","seven"),("D","six")]),
                ("single_choice",1,"It's time ______ (该) get up.","A","It's time to... 表示该做...了。","时间句型","grammar",[("A","to"),("B","for"),("C","of"),("D","at")]),
                ("fill_blank",2,"It's time for ______ (早餐).","breakfast","早餐的英文是 breakfast。","食物词汇","spelling",[]),
                ("single_choice",2,"— It's 12 o'clock.\n— It's time for ______ (午餐).","A","lunch 是午餐的意思。","食物词汇","vocabulary",[("A","lunch"),("B","dinner"),("C","breakfast"),("D","meal")]),
                ("single_choice",1,"Hurry ______! It's time to go.","A","Hurry up! 表示快点。","日常交际","dialogue",[("A","up"),("B","on"),("C","in"),("D","at")])],
    (4,"下",3): [("single_choice",1,"It's ______ (晴朗的) today.","A","sunny 是晴朗的意思。","天气词汇","vocabulary",[("A","sunny"),("B","rainy"),("C","cloudy"),("D","windy")]),
                ("single_choice",1,"It's ______ (多雨的). Take an umbrella.","B","rainy 是多雨的意思。","天气词汇","vocabulary",[("A","sunny"),("B","rainy"),("C","snowy"),("D","windy")]),
                ("fill_blank",2,"It's ______ (多云的) today.","cloudy","多云的英文是 cloudy。","天气词汇","spelling",[]),
                ("single_choice",2,"— Can I go outside now?\n— No. It's ______ (冷的) outside.","A","cold 是冷的意思。","天气词汇","vocabulary",[("A","cold"),("B","hot"),("C","warm"),("D","cool")]),
                ("single_choice",1,"The weather is ______ (温暖的).","A","warm 是温暖的意思。","天气词汇","vocabulary",[("A","warm"),("B","cold"),("C","cool"),("D","hot")])],
    (4,"下",4): [("single_choice",1,"Are these ______ (胡萝卜)?","A","carrots 是胡萝卜的复数形式。","蔬菜词汇","vocabulary",[("A","carrots"),("B","potatoes"),("C","tomatoes"),("D","onions")]),
                ("single_choice",1,"Those are ______ (马铃薯).","A","potatoes 是马铃薯的复数形式。","蔬菜词汇","vocabulary",[("A","potatoes"),("B","tomatoes"),("C","carrots"),("D","beans")]),
                ("fill_blank",2,"Look at the ______ (西红柿). They are red.","tomatoes","西红柿的英文是 tomato，复数是 tomatoes。","蔬菜词汇","spelling",[]),
                ("single_choice",2,"— Are those sheep?\n— No, they ______.","B","否定回答用 aren't。","一般疑问句","grammar",[("A","are"),("B","aren't"),("C","isn't"),("D","don't")]),
                ("single_choice",1,"I can see many ______ (马) on the farm.","A","horse 的复数是 horses。","动物词汇","vocabulary",[("A","horses"),("B","horse"),("C","sheep"),("D","cow")])],
    (4,"下",5): [("single_choice",1,"These are my ______ (裤子).","A","pants 是裤子的意思。","衣物词汇","vocabulary",[("A","pants"),("B","shirt"),("C","coat"),("D","sweater")]),
                ("single_choice",1,"That's a ______ (连衣裙).","A","dress 是连衣裙的意思。","衣物词汇","vocabulary",[("A","dress"),("B","skirt"),("C","shirt"),("D","coat")]),
                ("fill_blank",2,"These are my ______ (短袜).","socks","短袜的英文是 socks。","衣物词汇","spelling",[]),
                ("single_choice",2,"— ______ hat is this?\n— It's mine.","A","Whose 用于询问是谁的。","特殊疑问词","grammar",[("A","Whose"),("B","Who's"),("C","What's"),("D","Where's")]),
                ("single_choice",1,"The shirt is too ______ (小的).","A","small 是小的意思。","形容词","vocabulary",[("A","small"),("B","big"),("C","long"),("D","fat")])],
    (4,"下",6): [("single_choice",1,"Can I help you? The shoes are very ______ (便宜的).","A","cheap 是便宜的意思。","购物用语","vocabulary",[("A","cheap"),("B","expensive"),("C","good"),("D","nice")]),
                ("single_choice",1,"This skirt is too ______ (贵的).","B","expensive 是贵的意思。","购物用语","vocabulary",[("A","cheap"),("B","expensive"),("C","small"),("D","big")]),
                ("fill_blank",2,"I'll take ______ (它们).","them","它们的宾格形式是 them。","人称代词","spelling",[]),
                ("single_choice",2,"— Can I try them on?\n— Yes. Of ______.","A","Of course. 表示当然可以。","购物用语","dialogue",[("A","course"),("B","OK"),("C","yes"),("D","good")]),
                ("single_choice",1,"The size is ______ (正好).","A","just right 表示正好。","购物用语","vocabulary",[("A","just right"),("B","too big"),("C","too small"),("D","OK")])],
    # 五年级上册
    (5,"上",1): [("single_choice",1,"— Is he ______ (年轻的)?\n— No, he's old.","A","young 是年轻的意思。","描述人物","vocabulary",[("A","young"),("B","old"),("C","tall"),("D","short")]),
                ("single_choice",1,"She is very ______ (和蔼的).","A","kind 是和蔼的、友好的意思。","描述人物","vocabulary",[("A","kind"),("B","strict"),("C","angry"),("D","sad")]),
                ("fill_blank",2,"Mr Jones is very ______ (严格的).","strict","严格的英文是 strict。","描述人物","spelling",[]),
                ("single_choice",2,"— What's he like?\n— He's ______ (风趣的).","A","funny 是风趣的意思。","描述人物","vocabulary",[("A","funny"),("B","strict"),("C","quiet"),("D","shy")]),
                ("single_choice",1,"— Who's your art teacher?\n— Miss ______ (怀特).","A","White 是怀特的音译。","人物称呼","vocabulary",[("A","White"),("B","Black"),("C","Green"),("D","Brown")])],
    (5,"上",2): [("single_choice",1,"— What do you have on ______ (星期一)?\n— I have Chinese and math.","A","Monday 是星期一的意思。","星期词汇","vocabulary",[("A","Mondays"),("B","Tuesdays"),("C","Fridays"),("D","Sundays")]),
                ("single_choice",1,"Today is ______ (星期二).","B","Tuesday 是星期二的意思。","星期词汇","vocabulary",[("A","Monday"),("B","Tuesday"),("C","Wednesday"),("D","Thursday")]),
                ("fill_blank",2,"I often ______ (读书) on the weekend.","read books","读书的英文是 read books。","日常活动","spelling",[]),
                ("single_choice",2,"— Do you often play football on weekends?\n— Yes, ______.","A","肯定回答用 I do。","一般疑问句","grammar",[("A","I do"),("B","I am"),("C","it is"),("D","they are")]),
                ("single_choice",1,"______ (星期六) is the last day of the week.","A","Saturday 是星期六的意思。","星期词汇","vocabulary",[("A","Saturday"),("B","Sunday"),("C","Friday"),("D","Monday")])],
    (5,"上",3): [("single_choice",1,"— What would you like to ______ (喝)?\n— Some water, please.","A","drink 是喝的意思。","食物词汇","vocabulary",[("A","drink"),("B","eat"),("C","have"),("D","like")]),
                ("single_choice",1,"I'd like a ______ (三明治), please.","A","sandwich 是三明治的意思。","食物词汇","vocabulary",[("A","sandwich"),("B","hamburger"),("C","hot dog"),("D","pizza")]),
                ("fill_blank",2,"The noodles are ______ (咸的).","salty","咸的英文是 salty。","食物口味","spelling",[]),
                ("single_choice",2,"— What's your favourite ______ (食物)?\n— Noodles.","A","food 是食物的意思。","食物词汇","vocabulary",[("A","food"),("B","drink"),("C","fruit"),("D","vegetable")]),
                ("single_choice",1,"The ice cream is ______ (甜的).","A","sweet 是甜的意思。","食物口味","vocabulary",[("A","sweet"),("B","salty"),("C","sour"),("D","bitter")])],
    (5,"上",4): [("single_choice",1,"— What can you do?\n— I can ______ (扫地).","A","sweep the floor 是扫地的意思。","家务活动","vocabulary",[("A","sweep the floor"),("B","clean the room"),("C","wash clothes"),("D","cook dinner")]),
                ("single_choice",1,"I can ______ (洗衣服).","A","wash clothes 是洗衣服的意思。","家务活动","vocabulary",[("A","wash clothes"),("B","sweep the floor"),("C","clean the room"),("D","do dishes")]),
                ("fill_blank",2,"Can you ______ (做饭)?","cook","做饭的英文是 cook。","家务活动","spelling",[]),
                ("single_choice",2,"— Can you play basketball?\n— No, I ______.","B","否定回答用 can't。","can 句型","grammar",[("A","can"),("B","can't"),("C","don't"),("D","doesn't")]),
                ("single_choice",1,"My mother can ______ (游泳).","A","swim 是游泳的意思。","运动词汇","vocabulary",[("A","swim"),("B","run"),("C","jump"),("D","fly")])],
    (5,"上",5): [("single_choice",1,"There ______ a big bed in my room.","A","There is 接单数名词。","There be 句型","grammar",[("A","is"),("B","are"),("C","am"),("D","be")]),
                ("single_choice",1,"There ______ many books on the desk.","B","There are 接复数名词。","There be 句型","grammar",[("A","is"),("B","are"),("C","am"),("D","be")]),
                ("fill_blank",2,"There is a ______ (植物) in my room.","plant","植物的英文是 plant。","植物词汇","spelling",[]),
                ("single_choice",2,"— Is there a river near your house?\n— Yes, ______ is.","A","肯定回答用 there is。","There be 句型","grammar",[("A","there"),("B","it"),("C","this"),("D","that")]),
                ("single_choice",1,"The ______ (时钟) is on the wall.","A","clock 是时钟的意思。","物品词汇","vocabulary",[("A","clock"),("B","photo"),("C","picture"),("D","map")])],
    (5,"上",6): [("single_choice",1,"There is a ______ (森林) in the park.","A","forest 是森林的意思。","自然词汇","vocabulary",[("A","forest"),("B","village"),("C","city"),("D","town")]),
                ("single_choice",1,"There is a ______ (湖) in the nature park.","A","lake 是湖的意思。","自然词汇","vocabulary",[("A","lake"),("B","river"),("C","sea"),("D","hill")]),
                ("fill_blank",2,"Are there any tall ______ (建筑物) in the city?","buildings","建筑物的英文是 building，复数是 buildings。","地点词汇","spelling",[]),
                ("single_choice",2,"— Are there any pandas in the zoo?\n— No, there ______.","B","否定回答用 aren't。","There be 句型","grammar",[("A","are"),("B","aren't"),("C","isn't"),("D","don't")]),
                ("single_choice",1,"There is a ______ (小山) near the lake.","A","hill 是小山的意思。","自然词汇","vocabulary",[("A","hill"),("B","mountain"),("C","island"),("D","beach")])],
    # 五年级下册
    (5,"下",1): [("single_choice",1,"I usually get ______ (起床) at 7 o'clock.","A","get up 是起床的意思。","日常活动","vocabulary",[("A","up"),("B","down"),("C","on"),("D","in")]),
                ("single_choice",1,"I often ______ (晨练) in the morning.","A","do morning exercises 是晨练的意思。","日常活动","vocabulary",[("A","do morning exercises"),("B","play sports"),("C","have class"),("D","go to bed")]),
                ("fill_blank",2,"We eat ______ (晚餐) at 6:30 p.m.","dinner","晚餐的英文是 dinner。","食物词汇","spelling",[]),
                ("single_choice",2,"— When do you go to school?\n— ______ 7:30.","A","在具体时间点前用 At。","时间介词","grammar",[("A","At"),("B","In"),("C","On"),("D","For")]),
                ("single_choice",1,"I ______ (步行) to school every day.","A","walk 是步行的意思。","交通方式","vocabulary",[("A","walk"),("B","run"),("C","drive"),("D","fly")])],
    (5,"下",2): [("single_choice",1,"— Which ______ (季节) do you like best?\n— Spring.","A","season 是季节的意思。","季节词汇","vocabulary",[("A","season"),("B","month"),("C","week"),("D","day")]),
                ("single_choice",1,"I like ______ (春天) best.","A","spring 是春天的意思。","季节词汇","vocabulary",[("A","spring"),("B","summer"),("C","fall"),("D","winter")]),
                ("fill_blank",2,"It's hot in ______ (夏天).","summer","夏天的英文是 summer。","季节词汇","spelling",[]),
                ("single_choice",2,"— Why do you like winter?\n— ______ I can make a snowman.","A","Because 用于回答 Why 的问题。","特殊疑问句","grammar",[("A","Because"),("B","So"),("C","But"),("D","And")]),
                ("single_choice",1,"It's ______ (凉爽的) in autumn.","A","cool 是凉爽的意思。","天气词汇","vocabulary",[("A","cool"),("B","warm"),("C","hot"),("D","cold")])],
    (5,"下",3): [("single_choice",1,"— When is your ______ (生日)?\n— It's in May.","A","birthday 是生日的意思。","日期词汇","vocabulary",[("A","birthday"),("B","party"),("C","holiday"),("D","festival")]),
                ("single_choice",1,"My birthday is in ______ (五月).","A","May 是五月的意思。","月份词汇","vocabulary",[("A","May"),("B","April"),("C","June"),("D","July")]),
                ("fill_blank",2,"New Year's Day is in ______ (一月).","January","一月的英文是 January。","月份词汇","spelling",[]),
                ("single_choice",2,"— Is your birthday in June?\n— Yes, ______.","A","肯定回答用 it is。","一般疑问句","grammar",[("A","it is"),("B","it's"),("C","is it"),("D","isn't it")]),
                ("single_choice",1,"Teachers' Day is in ______ (九月).","C","September 是九月的意思。","月份词汇","vocabulary",[("A","July"),("B","August"),("C","September"),("D","October")])],
    (5,"下",4): [("single_choice",1,"Easter is in ______ (三月) or April.","A","March 是三月的意思。","月份词汇","vocabulary",[("A","March"),("B","May"),("C","June"),("D","July")]),
                ("single_choice",1,"— When is Easter?\n— It's usually in ______.","A","Easter 通常在四月。","节日词汇","vocabulary",[("A","April"),("B","May"),("C","March"),("D","June")]),
                ("fill_blank",2,"My mother's birthday is on April ______ (第四).","4th","第四的英文是 4th 或 fourth。","序数词","spelling",[]),
                ("single_choice",2,"— What's the date today?\n— It's ______ 1st.","A","询问日期的回答。","日期问答","dialogue",[("A","April"),("B","Monday"),("C","morning"),("D","8 o'clock")]),
                ("single_choice",1,"The ______ (兔子) is cute.","A","rabbit 是兔子的意思。","动物词汇","vocabulary",[("A","rabbit"),("B","duck"),("C","chicken"),("D","dog")])],
    (5,"下",5): [("single_choice",1,"— ______ dog is this?\n— It's Zhang Peng's.","A","Whose 用于询问是谁的。","特殊疑问词","grammar",[("A","Whose"),("B","Who's"),("C","What's"),("D","Where's")]),
                ("single_choice",1,"The book is ______ (我的).","A","mine 是我的（东西），名词性物主代词。","物主代词","vocabulary",[("A","mine"),("B","my"),("C","me"),("D","I")]),
                ("fill_blank",2,"This is ______ (你的) pen.","your","你的英文是 your。","物主代词","spelling",[]),
                ("single_choice",2,"— Is this yours?\n— No, it's ______ (他的).","A","his 是他的，名词性物主代词。","物主代词","vocabulary",[("A","his"),("B","he's"),("C","him"),("D","he")]),
                ("single_choice",1,"These are ______ (他们的) books.","A","their 是他们的，形容词性物主代词。","物主代词","vocabulary",[("A","their"),("B","they're"),("C","them"),("D","they")])],
    (5,"下",6): [("single_choice",1,"— What are you ______ (正在做)?\n— I'm reading a book.","A","doing 是正在做的意思。","现在进行时","vocabulary",[("A","doing"),("B","do"),("C","did"),("D","does")]),
                ("single_choice",1,"I am ______ (正在吃) dinner now.","A","eating 是正在吃的意思。","现在进行时","vocabulary",[("A","eating"),("B","eat"),("C","ate"),("D","eats")]),
                ("fill_blank",2,"She is ______ (正在睡觉) in the bedroom.","sleeping","正在睡觉的英文是 sleeping。","现在进行时","spelling",[]),
                ("single_choice",2,"— What is he doing?\n— He ______ running.","A","现在进行时用 be + doing，he 用 is。","现在进行时","grammar",[("A","is"),("B","are"),("C","am"),("D","be")]),
                ("single_choice",1,"— Are you listening to music?\n— Yes, ______ are.","A","肯定回答用 we are。","现在进行时","grammar",[("A","we"),("B","you"),("C","they"),("D","I")])],
    # 六年级上册
    (6,"上",1): [("single_choice",1,"— Where is the museum ______ (商店)?\n— It's next to the museum.","A","shop 是商店的意思。","地点词汇","vocabulary",[("A","shop"),("B","store"),("C","park"),("D","zoo")]),
                ("single_choice",1,"Turn ______ (左) at the crossing.","A","left 是左边的意思。","方向词汇","vocabulary",[("A","left"),("B","right"),("C","straight"),("D","back")]),
                ("fill_blank",2,"Go ______ (直走) for 5 minutes.","straight","直走的英文是 straight。","方向词汇","spelling",[]),
                ("single_choice",2,"— How can I get to the post office?\n— Turn right ______ the crossing.","A","at the crossing 表示在十字路口。","介词用法","grammar",[("A","at"),("B","in"),("C","on"),("D","to")]),
                ("single_choice",1,"The cinema is ______ (在...后面) the school.","A","behind 是在...后面的意思。","方位介词","vocabulary",[("A","behind"),("B","next to"),("C","near"),("D","in front of")])],
    (6,"上",2): [("single_choice",1,"I go to school ______ (乘) bus.","A","by 表示乘坐交通工具。","交通方式","vocabulary",[("A","by"),("B","on"),("C","in"),("D","at")]),
                ("single_choice",1,"She goes to work ______ (骑自行车).","A","by bike 是骑自行车的意思。","交通方式","vocabulary",[("A","by bike"),("B","by bus"),("C","by car"),("D","on foot")]),
                ("fill_blank",2,"I usually go to school on ______ (步行).","foot","on foot 是步行的意思。","交通方式","spelling",[]),
                ("single_choice",2,"— How do you come to school?\n— I come ______ subway.","A","by subway 表示乘地铁。","交通方式","vocabulary",[("A","by"),("B","on"),("C","in"),("D","at")]),
                ("single_choice",1,"Wait at a ______ (红灯).","A","red light 是红灯的意思。","交通规则","vocabulary",[("A","red light"),("B","green light"),("C","yellow light"),("D","traffic light")])],
    (6,"上",3): [("single_choice",1,"— What are you going to do ______ (今晚)?\n— I'm going to see a film.","A","tonight 是今晚的意思。","时间词汇","vocabulary",[("A","tonight"),("B","tomorrow"),("C","today"),("D","tonight's")]),
                ("single_choice",1,"I'm going to the ______ (电影院) tonight.","A","cinema 是电影院的意思。","地点词汇","vocabulary",[("A","cinema"),("B","hospital"),("C","school"),("D","park")]),
                ("fill_blank",2,"I'm going to buy a ______ (字典).","dictionary","字典的英文是 dictionary。","学习用品","spelling",[]),
                ("single_choice",2,"— Where are you going?\n— I'm going to the ______ (超市).","A","supermarket 是超市的意思。","地点词汇","vocabulary",[("A","supermarket"),("B","school"),("C","hospital"),("D","museum")]),
                ("single_choice",1,"— When are you going?\n— This ______ (下午).","A","afternoon 是下午的意思。","时间词汇","vocabulary",[("A","afternoon"),("B","morning"),("C","evening"),("D","night")])],
    (6,"上",4): [("single_choice",1,"— What are Peter's ______ (爱好)?\n— He likes reading.","A","hobby 的复数是 hobbies。","爱好词汇","vocabulary",[("A","hobbies"),("B","hobby"),("C","sport"),("D","like")]),
                ("single_choice",1,"He likes ______ (读故事).","A","reading stories 是读故事的意思。","爱好词汇","vocabulary",[("A","reading stories"),("B","read stories"),("C","reads stories"),("D","to read stories")]),
                ("fill_blank",2,"She likes ______ (唱歌).","singing","唱歌的英文是 sing，like doing 表示喜欢做某事。","爱好词汇","spelling",[]),
                ("single_choice",2,"— Does he like doing word puzzles?\n— Yes, he ______.","A","肯定回答用 does。","一般疑问句","grammar",[("A","does"),("B","do"),("C","is"),("D","likes")]),
                ("single_choice",1,"My pen pal ______ (居住) in Australia.","A","live 的第三人称单数是 lives。","动词三单","vocabulary",[("A","lives"),("B","live"),("C","living"),("D","lived")])],
    (6,"上",5): [("single_choice",1,"— What ______ your mother do?\n— She is a teacher.","A","询问职业用 What does... do?","特殊疑问句","grammar",[("A","does"),("B","do"),("C","is"),("D","are")]),
                ("single_choice",1,"My father is a ______ (商人).","A","businessman 是商人的意思。","职业词汇","vocabulary",[("A","businessman"),("B","teacher"),("C","doctor"),("D","nurse")]),
                ("fill_blank",2,"My uncle is a ______ (渔民).","fisherman","渔民的英文是 fisherman。","职业词汇","spelling",[]),
                ("single_choice",2,"— Where does your father work?\n— He works at a ______ (大学).","A","university 是大学的意思。","地点词汇","vocabulary",[("A","university"),("B","school"),("C","hospital"),("D","factory")]),
                ("single_choice",1,"She goes to work ______ (乘地铁).","A","by subway 是乘地铁的意思。","交通方式","vocabulary",[("A","by subway"),("B","by bus"),("C","by bike"),("D","on foot")])],
    (6,"上",6): [("single_choice",1,"— How do you ______ (感觉)?\n— I feel happy.","A","feel 是感觉的意思。","情感词汇","vocabulary",[("A","feel"),("B","feels"),("C","feeling"),("D","felt")]),
                ("single_choice",1,"I am ______ (生气的) with him.","A","angry 是生气的意思。","情感词汇","vocabulary",[("A","angry"),("B","happy"),("C","sad"),("D","worried")]),
                ("fill_blank",2,"Don't be ______ (难过的).","sad","难过的英文是 sad。","情感词汇","spelling",[]),
                ("single_choice",2,"— What's wrong?\n— The cat is ______ (生病的).","A","ill 是生病的意思。","健康词汇","vocabulary",[("A","ill"),("B","happy"),("C","angry"),("D","well")]),
                ("single_choice",1,"You should see a ______ (医生).","A","doctor 是医生的意思。","职业词汇","vocabulary",[("A","doctor"),("B","teacher"),("C","nurse"),("D","driver")])],
    # 六年级下册
    (6,"下",1): [("single_choice",1,"I'm 1.6 ______ (米) tall.","A","meter 是米的意思。","度量单位","vocabulary",[("A","meters"),("B","meter"),("C","centimeters"),("D","kilometers")]),
                ("single_choice",1,"You are ______ (更高的) than me.","A","taller 是更高的意思。","形容词比较级","vocabulary",[("A","taller"),("B","tall"),("C","tallest"),("D","more tall")]),
                ("fill_blank",2,"I am ______ (更重的) than you.","heavier","更重的英文是 heavier。","形容词比较级","spelling",[]),
                ("single_choice",2,"— How ______ are you?\n— I'm 45 kilograms.","A","询问体重用 How heavy。","特殊疑问句","grammar",[("A","heavy"),("B","tall"),("C","old"),("D","long")]),
                ("single_choice",1,"My legs are ______ (更长的) than yours.","A","longer 是更长的意思。","形容词比较级","vocabulary",[("A","longer"),("B","long"),("C","longest"),("D","more long")])],
    (6,"下",2): [("single_choice",1,"I ______ (打扫) my room last weekend.","A","cleaned 是 clean 的过去式。","一般过去时","vocabulary",[("A","cleaned"),("B","clean"),("C","cleans"),("D","cleaning")]),
                ("single_choice",1,"She ______ (洗) her clothes yesterday.","A","washed 是 wash 的过去式。","一般过去时","vocabulary",[("A","washed"),("B","wash"),("C","washes"),("D","washing")]),
                ("fill_blank",2,"I ______ (待) at home last Sunday.","stayed","待在家里的英文是 stayed at home。","一般过去时","spelling",[]),
                ("single_choice",2,"— Did you do anything else?\n— Yes, I ______ my homework.","A","did 是 do 的过去式。","一般过去时","grammar",[("A","did"),("B","do"),("C","does"),("D","doing")]),
                ("single_choice",1,"We ______ (喝) tea last night.","A","drank 是 drink 的过去式。","一般过去时","vocabulary",[("A","drank"),("B","drink"),("C","drinks"),("D","drinking")])],
    (6,"下",3): [("single_choice",1,"I ______ (去) to Turpan last month.","A","went 是 go 的过去式。","一般过去时","vocabulary",[("A","went"),("B","go"),("C","goes"),("D","going")]),
                ("single_choice",1,"She ______ (骑) a horse yesterday.","A","rode 是 ride 的过去式。","一般过去时","vocabulary",[("A","rode"),("B","ride"),("C","rides"),("D","riding")]),
                ("fill_blank",2,"I ______ (看见) many beautiful flowers there.","saw","看见的过去式是 saw。","一般过去时","spelling",[]),
                ("single_choice",2,"— How did you go there?\n— I went there ______ (乘火车).","A","by train 是乘火车的意思。","交通方式","vocabulary",[("A","by train"),("B","by bus"),("C","by plane"),("D","on foot")]),
                ("single_choice",1,"I ______ (买) some gifts for my friends.","A","bought 是 buy 的过去式。","一般过去时","vocabulary",[("A","bought"),("B","buy"),("C","buys"),("D","buying")])],
    (6,"下",4): [("single_choice",1,"There was no ______ (图书馆) in my old school.","A","library 是图书馆的意思。","地点词汇","vocabulary",[("A","library"),("B","gym"),("C","dining hall"),("D","classroom")]),
                ("single_choice",1,"Tell ______ (我们) about your school.","A","us 是我们，宾格形式。","人称代词","vocabulary",[("A","us"),("B","we"),("C","our"),("D","ours")]),
                ("fill_blank",2,"There are many tall ______ (建筑物) now.","buildings","建筑物的英文是 building。","地点词汇","spelling",[]),
                ("single_choice",2,"— Was there a gym before?\n— No, there ______.","B","否定回答用 wasn't。","There be 过去时","grammar",[("A","was"),("B","wasn't"),("C","isn't"),("D","weren't")]),
                ("single_choice",1,"Now there ______ a new computer in my room.","A","现在时用 there is。","There be 句型","grammar",[("A","is"),("B","was"),("C","are"),("D","were")])],
    (6,"下",5): [("single_choice",1,"Let's ______ (玩) a game together.","A","play 是玩的意思。","动词用法","vocabulary",[("A","play"),("B","to play"),("C","playing"),("D","played")]),
                ("single_choice",1,"We are on the same ______ (队).","A","team 是队的意思。","运动词汇","vocabulary",[("A","team"),("B","group"),("C","class"),("D","school")]),
                ("fill_blank",2,"He is a good basketball ______ (运动员).","player","运动员的英文是 player。","运动词汇","spelling",[]),
                ("single_choice",2,"— Who won the game?\n— Class 1 ______.","A","win 的过去式是 won。","一般过去时","vocabulary",[("A","won"),("B","win"),("C","wins"),("D","winning")]),
                ("single_choice",1,"Please pass me the ______ (球).","A","ball 是球的意思。","运动词汇","vocabulary",[("A","ball"),("B","bat"),("C","racket"),("D","net")])],
    (6,"下",6): [("single_choice",1,"We are going to have a ______ (聚会) next week.","A","party 是聚会的意思。","活动词汇","vocabulary",[("A","party"),("B","meeting"),("C","game"),("D","match")]),
                ("single_choice",1,"I want to ______ (分享) my photos with you.","A","share 是分享的意思。","动词词汇","vocabulary",[("A","share"),("B","show"),("C","give"),("D","take")]),
                ("fill_blank",2,"I will ______ (想念) you.","miss","想念的英文是 miss。","情感词汇","spelling",[]),
                ("single_choice",2,"— Here's a gift ______ you.\n— Thank you!","A","for 表示给、为了。","介词用法","grammar",[("A","for"),("B","to"),("C","of"),("D","with")]),
                ("single_choice",1,"Let's take a ______ (照片) together.","A","photo 是照片的意思。","日常词汇","vocabulary",[("A","photo"),("B","book"),("C","card"),("D","letter")])],
}

def main():
    print("=" * 60)
    print("人教版小学英语 (PEP) 全单元练习题导入工具")
    print("为所有 48 个单元添加高质量题目（每单元 5 道）")
    print("=" * 60)

    conn = pyodbc.connect(get_connection_string())
    print("数据库连接成功！")

    total_questions = 0
    total_options = 0

    for (grade, semester, unit_no), questions in ALL_QUESTIONS.items():
        unit_id = get_unit_id(conn, grade, semester, unit_no)
        if not unit_id:
            print(f"[SKIP] 单元不存在：{grade}年级{semester}册 Unit {unit_no}")
            continue

        print(f"导入 {grade}年级{semester}册 Unit {unit_no} 题目...", end=" ")
        unit_q_count = 0
        unit_opt_count = 0

        for q in questions:
            q_data = {'type': q[0], 'difficulty': q[1], 'stem': q[2], 'answer': q[3],
                      'analysis': q[4], 'knowledge_point': q[5], 'tags': q[6]}
            question_id = insert_question(conn, unit_id, q_data)
            if question_id and q[7]:
                for idx, opt in enumerate(q[7], 1):
                    insert_option(conn, question_id, opt[0], opt[1], idx)
                    unit_opt_count += 1
            unit_q_count += 1
            total_questions += 1

        print(f"[OK] {unit_q_count} 道题，{unit_opt_count} 个选项")

    conn.close()
    print("=" * 60)
    print(f"导入完成！")
    print(f"  新增题目：{total_questions} 道")
    print(f"  新增选项：{total_options} 条")
    print("=" * 60)

if __name__ == '__main__':
    main()
