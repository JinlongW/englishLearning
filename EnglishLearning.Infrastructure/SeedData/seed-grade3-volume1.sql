-- =====================================================
-- 人教版小学英语三到六年级题库数据导入脚本
-- 包含：单词表、语法知识点、练习题目
-- =====================================================

-- =====================
-- 三年级上册 Unit 1 Hello!
-- =====================

-- 单词数据
INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'ruler', '/ˈruːlə/', '/ˈruːlər/', '尺子', 'n.', 'I have a ruler.', '我有一把尺子。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'pencil', '/ˈpensl/', '/ˈpensl/', '铅笔', 'n.', 'This is my pencil.', '这是我的铅笔。', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'eraser', '/ɪˈreɪzə/', '/ɪˈreɪsər/', '橡皮', 'n.', 'Can I use your eraser?', '我可以用你的橡皮吗？', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'crayon', '/ˈkreɪən/', '/ˈkreɪən/', '蜡笔', 'n.', 'She has a red crayon.', '她有一支红色的蜡笔。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'book', '/bʊk/', '/bʊk/', '书', 'n.', 'Open your book.', '打开你的书。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'pencil box', '/ˈpensl bɒks/', '/ˈpensl bɑːks/', '铅笔盒', 'n.', 'My pen is in the pencil box.', '我的钢笔在铅笔盒里。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'bag', '/bæɡ/', '/bæɡ/', '书包', 'n.', 'I put my books in the bag.', '我把书放进书包里。', 7);

-- 语法知识点
INSERT INTO tb_grammar (id, grade_unit_id, title, content_type, content_json, sort_order, passing_score, created_at)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), '问候语 Hello/Hi', 'lesson', '{"introduction":"Hello 和 Hi 是最常用的英语问候语，用于见面时打招呼。","examples":[{"en":"Hello! I am Mike.","cn":"你好！我是迈克。"},{"en":"Hi! I am Sarah.","cn":"嗨！我是莎拉。"}],"notes":"Hello 比较正式，Hi 比较随意，两者可以互换使用。"}', 1, 60, GETDATE());

-- 练习题目
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags, is_active, created_at, updated_at)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1), 'single_choice', 1, '当你想和别人打招呼时，你应该说：', 'A', 'Hello 和 Hi 都是常用的问候语，意思是"你好"。', '问候语', 'greeting,basic', 1, GETDATE(), GETDATE());

INSERT INTO tb_question_option (id, question_id, option_label, option_text, is_correct, sort_order)
VALUES
(NEWID(), (SELECT TOP 1 id FROM tb_question WHERE grade_unit_id=(SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1) ORDER BY created_at DESC), 'A', 'Hello!', 1, 1),
(NEWID(), (SELECT TOP 1 id FROM tb_question WHERE grade_unit_id=(SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1) ORDER BY created_at DESC), 'B', 'Goodbye!', 0, 2),
(NEWID(), (SELECT TOP 1 id FROM tb_question WHERE grade_unit_id=(SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=1) ORDER BY created_at DESC), 'C', 'Thank you!', 0, 3);

-- =====================
-- 三年级上册 Unit 2 Look at Me
-- =====================

INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'head', '/hed/', '/hed/', '头', 'n.', 'Touch your head.', '摸摸你的头。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'face', '/feɪs/', '/feɪs/', '脸', 'n.', 'She has a round face.', '她有一张圆脸。', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'nose', '/nəʊz/', '/noʊz/', '鼻子', 'n.', 'Point to your nose.', '指着你的鼻子。', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'eye', '/aɪ/', '/aɪ/', '眼睛', 'n.', 'I have two eyes.', '我有两只眼睛。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'ear', '/ɪə/', '/ɪr/', '耳朵', 'n.', 'Cover your ears.', '捂住你的耳朵。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'mouth', '/maʊθ/', '/maʊθ/', '嘴巴', 'n.', 'Open your mouth.', '张开你的嘴巴。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'arm', '/ɑːm/', '/ɑːrm/', '胳膊', 'n.', 'Raise your arm.', '举起你的胳膊。', 7),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'hand', '/hænd/', '/hænd/', '手', 'n.', 'Clap your hands.', '拍拍你的手。', 8),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'leg', '/leɡ/', '/leɡ/', '腿', 'n.', 'Stamp your foot.', '跺跺你的脚。', 9),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=2), 'foot', '/fʊt/', '/fʊt/', '脚', 'n.', 'My foot hurts.', '我的脚疼。', 10);

-- =====================
-- 三年级上册 Unit 3 Let's Paint (颜色)
-- =====================

INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'red', '/red/', '/red/', '红色', 'n./adj.', 'The apple is red.', '苹果是红色的。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'yellow', '/ˈjeləʊ/', '/ˈjeloʊ/', '黄色', 'n./adj.', 'The banana is yellow.', '香蕉是黄色的。', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'green', '/ɡriːn/', '/ɡriːn/', '绿色', 'n./adj.', 'The grass is green.', '草地是绿色的。', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'blue', '/bluː/', '/bluː/', '蓝色', 'n./adj.', 'The sky is blue.', '天空是蓝色的。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'black', '/blæk/', '/blæk/', '黑色', 'n./adj.', 'The cat is black.', '这只猫是黑色的。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'white', '/waɪt/', '/waɪt/', '白色', 'n./adj.', 'The snow is white.', '雪是白色的。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'orange', '/ˈɒrɪndʒ/', '/ˈɔːrɪndʒ/', '橙色', 'n./adj.', 'The orange is orange.', '橙子是橙色的。', 7),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=3), 'brown', '/braʊn/', '/braʊn/', '棕色', 'n./adj.', 'The bear is brown.', '熊是棕色的。', 8);

-- =====================
-- 三年级上册 Unit 4 We Love Animals
-- =====================

INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'pig', '/pɪɡ/', '/pɪɡ/', '猪', 'n.', 'The pig is fat.', '这头猪很胖。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'bear', '/beə/', '/ber/', '熊', 'n.', 'The bear is big.', '熊很大。', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'duck', '/dʌk/', '/dʌk/', '鸭子', 'n.', 'The duck can swim.', '鸭子会游泳。', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'elephant', '/ˈelɪfənt/', '/ˈelɪfənt/', '大象', 'n.', 'The elephant has a long nose.', '大象有一个长鼻子。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'monkey', '/ˈmʌŋki/', '/ˈmʌŋki/', '猴子', 'n.', 'The monkey is clever.', '猴子很聪明。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'bird', '/bɜːd/', '/bɜːrd/', '鸟', 'n.', 'The bird can fly.', '鸟会飞。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'tiger', '/ˈtaɪɡə/', '/ˈtaɪɡər/', '老虎', 'n.', 'The tiger is strong.', '老虎很强壮。', 7),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'panda', '/ˈpændə/', '/ˈpændə/', '熊猫', 'n.', 'The panda is cute.', '熊猫很可爱。', 8),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=4), 'zoo', '/zuː/', '/zuː/', '动物园', 'n.', 'Let''s go to the zoo.', '我们去动物园吧。', 9);

-- =====================
-- 三年级上册 Unit 5 Let's Eat (食物)
-- =====================

INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'bread', '/bred/', '/bred/', '面包', 'n.', 'I like bread.', '我喜欢面包。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'juice', '/dʒuːs/', '/dʒuːs/', '果汁', 'n.', 'Can I have some juice?', '我能喝点果汁吗？', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'egg', '/eɡ/', '/eɡ/', '鸡蛋', 'n.', 'I eat an egg for breakfast.', '我早餐吃了一个鸡蛋。', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'milk', '/mɪlk/', '/mɪlk/', '牛奶', 'n.', 'Drink some milk.', '喝点牛奶。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'water', '/ˈwɔːtə/', '/ˈwɔːtər/', '水', 'n.', 'I want some water.', '我想喝水。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'fish', '/fɪʃ/', '/fɪʃ/', '鱼', 'n.', 'The fish is delicious.', '鱼很美味。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=5), 'rice', '/raɪs/', '/raɪs/', '米饭', 'n.', 'I have rice for lunch.', '我午餐吃了米饭。', 7);

-- =====================
-- 三年级上册 Unit 6 Happy Birthday (数字)
-- =====================

INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'one', '/wʌn/', '/wʌn/', '一', 'num.', 'I have one book.', '我有一本书。', 1),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'two', '/tuː/', '/tuː/', '二', 'num.', 'I see two birds.', '我看到两只鸟。', 2),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'three', '/θriː/', '/θriː/', '三', 'num.', 'There are three apples.', '有三个苹果。', 3),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'four', '/fɔː/', '/fɔːr/', '四', 'num.', 'I have four pencils.', '我有四支铅笔。', 4),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'five', '/faɪv/', '/faɪv/', '五', 'num.', 'She has five fingers.', '她有五个手指。', 5),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'six', '/sɪks/', '/sɪks/', '六', 'num.', 'There are six days in a week.', '一周有六天。', 6),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'seven', '/ˈsevn/', '/ˈsevn/', '七', 'num.', 'I see seven stars.', '我看到七颗星星。', 7),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'eight', '/eɪt/', '/eɪt/', '八', 'num.', 'There are eight people.', '有八个人。', 8),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'nine', '/naɪn/', '/naɪn/', '九', 'num.', 'I have nine balls.', '我有九个球。', 9),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'ten', '/ten/', '/ten/', '十', 'num.', 'There are ten fingers.', '有十个手指。', 10),
(NEWID(), (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester='上' AND unit_no=6), 'cake', '/keɪk/', '/keɪk/', '蛋糕', 'n.', 'Happy birthday! Let''s eat cake.', '生日快乐！我们吃蛋糕吧。', 11);

PRINT '三年级上册数据导入完成！';
