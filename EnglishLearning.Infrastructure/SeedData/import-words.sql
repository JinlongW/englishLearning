-- =====================================================
-- 人教版小学英语三到六年级题库数据导入脚本
-- =====================================================

SET NOCOUNT ON;
PRINT '========================================';
PRINT '人教版小学英语题库数据导入';
PRINT '========================================';
PRINT '';

-- 三年级上册 Unit 1 Hello!
PRINT '正在导入三年级上册 Unit 1 数据...';

DECLARE @Unit3_1 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=1);

-- 插入单词
INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_1, 'ruler', '/ru:l@/', '/ru:l@r/', N'尺子', N'n.', N'I have a ruler.', N'我有一把尺子。', 1),
(NEWID(), @Unit3_1, 'pencil', '/pensl/', '/pensl/', N'铅笔', N'n.', N'This is my pencil.', N'这是我的铅笔。', 2),
(NEWID(), @Unit3_1, 'eraser', '/I'reIz@/', '/I'reIs@r/', N'橡皮', N'n.', N'Can I use your eraser?', N'我可以用你的橡皮吗？', 3),
(NEWID(), @Unit3_1, 'crayon', '/'kreI@n/', '/'kreI@n/', N'蜡笔', N'n.', N'She has a red crayon.', N'她有一支红色的蜡笔。', 4),
(NEWID(), @Unit3_1, 'book', '/bUk/', '/bUk/', N'书', N'n.', N'Open your book.', N'打开你的书。', 5),
(NEWID(), @Unit3_1, 'pencil box', '/pensl bOks/', '/pensl bA:ks/', N'铅笔盒', N'n.', N'My pen is in the pencil box.', N'我的钢笔在铅笔盒里。', 6),
(NEWID(), @Unit3_1, 'bag', '/b[g/', '/b[g/', N'书包', N'n.', N'I put my books in the bag.', N'我把书放进书包里。', 7);

-- 插入语法
INSERT INTO tb_grammar (id, grade_unit_id, title, content_type, content_json, sort_order, passing_score, created_at)
VALUES
(NEWID(), @Unit3_1, N'问候语 Hello/Hi', N'lesson', N'{"introduction":"Hello 和 Hi 是最常用的英语问候语。","examples":[{"en":"Hello! I am Mike.","cn":"你好！我是迈克。"}]}', 1, 60, GETDATE());

-- 插入题目
DECLARE @Q1 UNIQUEIDENTIFIER = NEWID();
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags, is_active, created_at, updated_at)
VALUES (@Q1, @Unit3_1, N'single_choice', 1, N'当你想和别人打招呼时，你应该说：', N'A', N'Hello 是常用的问候语。', N'问候语', N'greeting', 1, GETDATE(), GETDATE());

INSERT INTO tb_question_option (id, question_id, option_key, option_content, sort_order)
VALUES (NEWID(), @Q1, N'A', N'Hello!', 1), (NEWID(), @Q1, N'B', N'Goodbye!', 2), (NEWID(), @Q1, N'C', N'Thank you!', 3);

PRINT '三年级上册 Unit 1 完成！';

-- 三年级上册 Unit 2 Look at Me
PRINT '正在导入三年级上册 Unit 2 数据...';

DECLARE @Unit3_2 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=2);

INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_2, 'head', '/hed/', '/hed/', N'头', N'n.', N'Touch your head.', N'摸摸你的头。', 1),
(NEWID(), @Unit3_2, 'face', '/feIs/', '/feIs/', N'脸', N'n.', N'She has a round face.', N'她有一张圆脸。', 2),
(NEWID(), @Unit3_2, 'nose', '/n@Uz/', '/noUz/', N'鼻子', N'n.', N'Point to your nose.', N'指着你的鼻子。', 3),
(NEWID(), @Unit3_2, 'eye', '/aI/', '/aI/', N'眼睛', N'n.', N'I have two eyes.', N'我有两只眼睛。', 4),
(NEWID(), @Unit3_2, 'ear', '/I@/', '/Ir/', N'耳朵', N'n.', N'Cover your ears.', N'捂住你的耳朵。', 5),
(NEWID(), @Unit3_2, 'mouth', '/maUT/', '/maUT/', N'嘴巴', N'n.', N'Open your mouth.', N'张开你的嘴巴。', 6),
(NEWID(), @Unit3_2, 'arm', '/A:m/', '/A:rm/', N'胳膊', N'n.', N'Raise your arm.', N'举起你的胳膊。', 7),
(NEWID(), @Unit3_2, 'hand', '/h[nd/', '/h[nd/', N'手', N'n.', N'Clap your hands.', N'拍拍你的手。', 8),
(NEWID(), @Unit3_2, 'leg', '/leɡ/', '/leɡ/', N'腿', N'n.', N'Stamp your foot.', N'跺跺你的脚。', 9),
(NEWID(), @Unit3_2, 'foot', '/fUt/', '/fUt/', N'脚', N'n.', N'My foot hurts.', N'我的脚疼。', 10);

PRINT '三年级上册 Unit 2 完成！';

-- 三年级上册 Unit 3 Let's Paint
PRINT '正在导入三年级上册 Unit 3 数据...';

DECLARE @Unit3_3 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=3);

INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_3, 'red', '/red/', '/red/', N'红色', N'n./adj.', N'The apple is red.', N'苹果是红色的。', 1),
(NEWID(), @Unit3_3, 'yellow', '/'jel@U/', '/'jeloU/', N'黄色', N'n./adj.', N'The banana is yellow.', N'香蕉是黄色的。', 2),
(NEWID(), @Unit3_3, 'green', '/ɡri:n/', '/ɡri:n/', N'绿色', N'n./adj.', N'The grass is green.', N'草地是绿色的。', 3),
(NEWID(), @Unit3_3, 'blue', '/blu:/', '/blu:/', N'蓝色', N'n./adj.', N'The sky is blue.', N'天空是蓝色的。', 4),
(NEWID(), @Unit3_3, 'black', '/blk/', '/blk/', N'黑色', N'n./adj.', N'The cat is black.', N'这只猫是黑色的。', 5),
(NEWID(), @Unit3_3, 'white', '/waIt/', '/waIt/', N'白色', N'n./adj.', N'The snow is white.', N'雪是白色的。', 6),
(NEWID(), @Unit3_3, 'orange', '/'OrIndZ/', '/'O:rIndZ/', N'橙色', N'n./adj.', N'The orange is orange.', N'橙子是橙色的。', 7),
(NEWID(), @Unit3_3, 'brown', '/braUn/', '/braUn/', N'棕色', N'n./adj.', N'The bear is brown.', N'熊是棕色的。', 8);

PRINT '三年级上册 Unit 3 完成！';

-- 三年级上册 Unit 4 We Love Animals
PRINT '正在导入三年级上册 Unit 4 数据...';

DECLARE @Unit3_4 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=4);

INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_4, 'pig', '/pIɡ/', '/pIɡ/', N'猪', N'n.', N'The pig is fat.', N'这头猪很胖。', 1),
(NEWID(), @Unit3_4, 'bear', '/be@/', '/ber/', N'熊', N'n.', N'The bear is big.', N'熊很大。', 2),
(NEWID(), @Unit3_4, 'duck', '/dVk/', '/dVk/', N'鸭子', N'n.', N'The duck can swim.', N'鸭子会游泳。', 3),
(NEWID(), @Unit3_4, 'elephant', '/'elIf@nt/', '/elIf@nt/', N'大象', N'n.', N'The elephant has a long nose.', N'大象有一个长鼻子。', 4),
(NEWID(), @Unit3_4, 'monkey', '/'mVNki/', '/'mVNki/', N'猴子', N'n.', N'The monkey is clever.', N'猴子很聪明。', 5),
(NEWID(), @Unit3_4, 'bird', '/b3:d/', '/b3:rd/', N'鸟', N'n.', N'The bird can fly.', N'鸟会飞。', 6),
(NEWID(), @Unit3_4, 'tiger', '/'taIɡ@/', '/taIɡ@r/', N'老虎', N'n.', N'The tiger is strong.', N'老虎很强壮。', 7),
(NEWID(), @Unit3_4, 'panda', '/'p[nd@/', '/p[nd@/', N'熊猫', N'n.', N'The panda is cute.', N'熊猫很可爱。', 8),
(NEWID(), @Unit3_4, 'zoo', '/zu:/', '/zu:/', N'动物园', N'n.', N'Let''s go to the zoo.', N'我们去动物园吧。', 9);

PRINT '三年级上册 Unit 4 完成！';

-- 三年级上册 Unit 5 Let's Eat
PRINT '正在导入三年级上册 Unit 5 数据...';

DECLARE @Unit3_5 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=5);

INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_5, 'bread', '/bred/', '/bred/', N'面包', N'n.', N'I like bread.', N'我喜欢面包。', 1),
(NEWID(), @Unit3_5, 'juice', '/dZu:s/', '/dZu:s/', N'果汁', N'n.', N'Can I have some juice?', N'我能喝点果汁吗？', 2),
(NEWID(), @Unit3_5, 'egg', '/eɡ/', '/eɡ/', N'鸡蛋', N'n.', N'I eat an egg for breakfast.', N'我早餐吃了一个鸡蛋。', 3),
(NEWID(), @Unit3_5, 'milk', '/mIlk/', '/mIlk/', N'牛奶', N'n.', N'Drink some milk.', N'喝点牛奶。', 4),
(NEWID(), @Unit3_5, 'water', '/'wO:t@/', '/wO:t@r/', N'水', N'n.', N'I want some water.', N'我想喝水。', 5),
(NEWID(), @Unit3_5, 'fish', '/fIS/', '/fIS/', N'鱼', N'n.', N'The fish is delicious.', N'鱼很美味。', 6),
(NEWID(), @Unit3_5, 'rice', '/raIs/', '/raIs/', N'米饭', N'n.', N'I have rice for lunch.', N'我午餐吃了米饭。', 7);

PRINT '三年级上册 Unit 5 完成！';

-- 三年级上册 Unit 6 Happy Birthday
PRINT '正在导入三年级上册 Unit 6 数据...';

DECLARE @Unit3_6 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=3 AND semester=N'上' AND unit_no=6);

INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(NEWID(), @Unit3_6, 'one', '/wVn/', '/wVn/', N'一', N'num.', N'I have one book.', N'我有一本书。', 1),
(NEWID(), @Unit3_6, 'two', '/tu:/', '/tu:/', N'二', N'num.', N'I see two birds.', N'我看到两只鸟。', 2),
(NEWID(), @Unit3_6, 'three', '/Tri:/', '/Tri:/', N'三', N'num.', N'There are three apples.', N'有三个苹果。', 3),
(NEWID(), @Unit3_6, 'four', '/fO:/', '/fO:r/', N'四', N'num.', N'I have four pencils.', N'我有四支铅笔。', 4),
(NEWID(), @Unit3_6, 'five', '/faIv/', '/faIv/', N'五', N'num.', N'She has five fingers.', N'她有五个手指。', 5),
(NEWID(), @Unit3_6, 'six', '/sIks/', '/sIks/', N'六', N'num.', N'There are six days in a week.', N'一周有六天。', 6),
(NEWID(), @Unit3_6, 'seven', '/'sevn/', '/'sevn/', N'七', N'num.', N'I see seven stars.', N'我看到七颗星星。', 7),
(NEWID(), @Unit3_6, 'eight', '/eIt/', '/eIt/', N'八', N'num.', N'There are eight people.', N'有八个人。', 8),
(NEWID(), @Unit3_6, 'nine', '/naIn/', '/naIn/', N'九', N'num.', N'I have nine balls.', N'我有九个球。', 9),
(NEWID(), @Unit3_6, 'ten', '/ten/', '/ten/', N'十', N'num.', N'There are ten fingers.', N'有十个手指。', 10),
(NEWID(), @Unit3_6, 'cake', '/keIk/', '/keIk/', N'蛋糕', N'n.', N'Happy birthday! Let''s eat cake.', N'生日快乐！我们吃蛋糕吧。', 11);

PRINT '三年级上册 Unit 6 完成！';
PRINT '';
PRINT '========================================';
PRINT '数据导入完成！';
PRINT '========================================';
