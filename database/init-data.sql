-- =============================================
-- 英语学习工具 - 初始化数据脚本
-- 用于插入基础测试数据
-- =============================================

USE EnglishLearning;
GO

-- =============================================
-- 1. 插入测试用户
-- =============================================
DECLARE @user1 UNIQUEIDENTIFIER = NEWID();
DECLARE @user2 UNIQUEIDENTIFIER = NEWID();

-- 用户 1 - 六年级
INSERT INTO tb_user (id, username, password_hash, student_name, grade_level, phone)
VALUES (@user1, 'xiaoming', '$2a$10$placeholder', '小明', 6, '13800138001');

INSERT INTO tb_user_profile (user_id, learning_style, difficulty_level, current_streak, max_streak, total_learning_days)
VALUES (@user1, 'visual', 2, 5, 12, 30);

INSERT INTO tb_user_level (user_id, current_level, level_name, current_exp, exp_to_next)
VALUES (@user1, 3, '进步之星', 450, 300);

-- 用户 2 - 三年级
INSERT INTO tb_user (id, username, password_hash, student_name, grade_level, phone)
VALUES (@user2, 'xiaohong', '$2a$10$placeholder', '小红', 3, '13800138002');

INSERT INTO tb_user_profile (user_id, learning_style, difficulty_level, current_streak, max_streak, total_learning_days)
VALUES (@user2, 'audio', 1, 3, 5, 15);

INSERT INTO tb_user_level (user_id, current_level, level_name, current_exp, exp_to_next)
VALUES (@user2, 2, '入门学徒', 150, 100);

PRINT '测试用户创建完成';
GO

-- =============================================
-- 2. 插入年级单元 (三年级到六年级)
-- =============================================
-- 三年级上
DECLARE @grade3_1 UNIQUEIDENTIFIER = NEWID();
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
VALUES (@grade3_1, 3, '上', 1, 'Unit 1 Hello!', 1);

INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (3, '上', 2, 'Unit 2 Look at Me', 2),
       (3, '上', 3, 'Unit 3 Let''s Paint', 3),
       (3, '上', 4, 'Unit 4 We Love Animals', 4),
       (3, '上', 5, 'Unit 5 Let''s Eat', 5),
       (3, '上', 6, 'Unit 6 Happy Birthday', 6);

-- 三年级下
INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (3, '下', 1, 'Unit 1 Welcome Back to School', 1),
       (3, '下', 2, 'Unit 2 My Family', 2),
       (3, '下', 3, 'Unit 3 At the Zoo', 3),
       (3, '下', 4, 'Unit 4 Where Is My Car', 4),
       (3, '下', 5, 'Unit 5 Do You Like Pears', 5),
       (3, '下', 6, 'Unit 6 How Many', 6);

-- 四年级上
INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (4, '上', 1, 'Unit 1 My Classroom', 1),
       (4, '上', 2, 'Unit 2 My Schoolbag', 2),
       (4, '上', 3, 'Unit 3 My Friends', 3),
       (4, '上', 4, 'Unit 4 My Home', 4),
       (4, '上', 5, 'Unit 5 Dinner''s Ready', 5),
       (4, '上', 6, 'Unit 6 Meet My Family', 6);

-- 五年级上 (示例)
INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (5, '上', 1, 'Unit 1 What''s He Like', 1),
       (5, '上', 2, 'Unit 2 My Week', 2),
       (5, '上', 3, 'Unit 3 What Would You Like', 3);

-- 六年级上 (示例 - 重点，因为用户有六年级孩子)
DECLARE @grade6_1 UNIQUEIDENTIFIER = NEWID();
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
VALUES (@grade6_1, 6, '上', 1, 'Unit 1 How Can I Get There', 1);

INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (6, '上', 2, 'Unit 2 Ways to Go to School', 2),
       (6, '上', 3, 'Unit 3 My Weekend Plan', 3),
       (6, '上', 4, 'Unit 4 Then and Now', 4),
       (6, '上', 5, 'Unit 5 Occupations', 5),
       (6, '上', 6, 'Unit 6 How Do You Feel', 6);

-- 六年级下
INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
VALUES (6, '下', 1, 'Unit 1 How Tall Are You', 1),
       (6, '下', 2, 'Unit 2 Last Weekend', 2),
       (6, '下', 3, 'Unit 3 Where Did You Go', 3),
       (6, '下', 4, 'Unit 4 Then and Now', 4);

PRINT '年级单元数据插入完成';
GO

-- =============================================
-- 3. 插入单词数据 (示例 - 六年级 Unit 1)
-- =============================================
DECLARE @unit6_1 UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=1);

INSERT INTO tb_word (grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order)
VALUES
(@unit6_1, 'science', '/ˈsaɪəns/', '/ˈsaɪəns/', '科学', 'n.', 'I like science class.', '我喜欢科学课。', 1),
(@unit6_1, 'museum', '/mjuːˈziːəm/', '/mjuˈziəm/', '博物馆', 'n.', 'We visited the museum yesterday.', '我们昨天参观了博物馆。', 2),
(@unit6_1, 'post office', '/ˈpəʊst ˌɒfɪs/', '/ˈpoʊst ˌɔːfɪs/', '邮局', 'n.', 'The post office is near here.', '邮局就在这附近。', 3),
(@unit6_1, 'bookstore', '/ˈbʊkstɔː/', '/ˈbʊkstɔːr/', '书店', 'n.', 'I bought a book at the bookstore.', '我在书店买了一本书。', 4),
(@unit6_1, 'cinema', '/ˈsɪnəmə/', '/ˈsɪnəmə/', '电影院', 'n.', 'Let''s go to the cinema.', '我们去看电影吧。', 5),
(@unit6_1, 'hospital', '/ˈhɒspɪtl/', '/ˈhɑːspɪtl/', '医院', 'n.', 'She works in a hospital.', '她在医院工作。', 6),
(@unit6_1, 'crossing', '/ˈkrɒsɪŋ/', '/ˈkrɔːsɪŋ/', '十字路口', 'n.', 'Turn left at the crossing.', '在十字路口左转。', 7),
(@unit6_1, 'turn', '/tɜːn/', '/tɜːrn/', '转弯', 'v.', 'Turn right here.', '在这里右转。', 8),
(@unit6_1, 'left', '/left/', '/left/', '左边的', 'adj.', 'On the left side.', '在左边。', 9),
(@unit6_1, 'right', '/raɪt/', '/raɪt/', '右边的', 'adj.', 'On the right side.', '在右边。', 10),
(@unit6_1, 'straight', '/streɪt/', '/streɪt/', '直的', 'adv.', 'Go straight ahead.', '直走。', 11),
(@unit6_1, 'map', '/mæp/', '/mæp/', '地图', 'n.', 'Look at the map.', '看地图。', 12);

PRINT '六年级 Unit 1 单词插入完成';
GO

-- =============================================
-- 4. 插入语法知识点 (六年级重点语法)
-- =============================================
DECLARE @unit6_1_id UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=1);

-- 语法 1: 问路句型
INSERT INTO tb_grammar (grade_unit_id, title, content_type, content_json, duration_seconds, sort_order, passing_score)
VALUES
(@unit6_1_id, '问路句型 - How can I get to...', 'article', N'{
    "sections": [
        {
            "title": "基本句型",
            "content": "问路是日常生活中很实用的英语技能。我们来学习几个常用的问路句型。"
        },
        {
            "title": "核心句型",
            "content": "How can I get to the + 地点？\n\n例如：\n• How can I get to the museum? (我怎么去博物馆？)\n• How can I get to the post office? (我怎么去邮局？)"
        },
        {
            "title": "其他问路表达",
            "content": "1. Where is the...? (请问...在哪里？)\n2. Can you tell me the way to...? (你能告诉我去...的路吗？)\n3. Is there a... near here? (这附近有...吗？)"
        },
        {
            "title": "指路回答",
            "content": "• Go straight. (直走)\n• Turn left. (左转)\n• Turn right. (右转)\n• It''s on your left/right. (它在你的左边/右边)"
        }
    ]
}', NULL, 1, 60);

-- 语法 2: 方位介词
INSERT INTO tb_grammar (grade_unit_id, title, content_type, content_json, duration_seconds, sort_order, passing_score)
VALUES
(@unit6_1_id, '方位介词 - in, on, at, next to', 'article', N'{
    "sections": [
        {
            "title": "方位介词用法",
            "content": "方位介词用来描述物体或地点之间的位置关系。"
        },
        {
            "title": "in - 在...里面",
            "content": "in 表示在某个空间或范围的内部\n\n例句：\n• The book is in the bag. (书在包里。)\n• She lives in Beijing. (她住在北京。)"
        },
        {
            "title": "on - 在...上面",
            "content": "on 表示在某物体的表面上\n\n例句：\n• The cup is on the table. (杯子在桌子上。)\n• There is a picture on the wall. (墙上有一幅画。)"
        },
        {
            "title": "next to - 在...旁边",
            "content": "next to 表示紧挨着、靠近\n\n例句：\n• The bank is next to the supermarket. (银行在超市旁边。)\n• Sit next to me. (坐我旁边。)"
        }
    ]
}', NULL, 2, 60);

PRINT '语法知识点插入完成';
GO

-- =============================================
-- 5. 插入题库数据 (示例)
-- =============================================
DECLARE @unit6_1_q UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=1);
DECLARE @q1 UNIQUEIDENTIFIER = NEWID();
DECLARE @q2 UNIQUEIDENTIFIER = NEWID();
DECLARE @q3 UNIQUEIDENTIFIER = NEWID();
DECLARE @q4 UNIQUEIDENTIFIER = NEWID();
DECLARE @q5 UNIQUEIDENTIFIER = NEWID();

-- 题目 1: 单选题 - 单词意思
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags)
VALUES
(@q1, @unit6_1_q, 'single_choice', 1,
'单词 "museum" 的中文意思是？',
'A',
'museum 意为"博物馆"，是六年级上册 Unit 1 的重点词汇。',
'词汇记忆',
'word,vocabulary');

INSERT INTO tb_question_option (question_id, option_key, option_content, sort_order)
VALUES
(@q1, 'A', '博物馆', 1),
(@q1, 'B', '美术馆', 2),
(@q1, 'C', '图书馆', 3),
(@q1, 'D', '电影院', 4);

-- 题目 2: 单选题 - 句型
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags)
VALUES
(@q2, @unit6_1_q, 'single_choice', 2,
'你想问路去电影院，应该怎么说？',
'B',
'问路的标准句型是 "How can I get to the + 地点？"',
'问路句型',
'grammar,speaking');

INSERT INTO tb_question_option (question_id, option_key, option_content, sort_order)
VALUES
(@q2, 'A', 'Where is the cinema go?', 1),
(@q2, 'B', 'How can I get to the cinema?', 2),
(@q2, 'C', 'How go to cinema?', 3),
(@q2, 'D', 'Where cinema?', 4);

-- 题目 3: 填空题 - 方位介词
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags)
VALUES
(@q3, @unit6_1_q, 'fill_blank', 2,
'The bookstore is ________ (在...旁边) the post office.',
'next to',
'next to 表示"在...旁边"，是描述位置关系的常用介词短语。',
'方位介词',
'grammar,preposition');

-- 题目 4: 拼写题
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags)
VALUES
(@q4, @unit6_1_q, 'spell_word', 2,
'根据音标和中文写单词：/hɒspɪtl/ 医院',
'hospital',
'hospital 医院，注意发音和拼写的对应关系。',
'单词拼写',
'spelling,vocabulary');

-- 题目 5: 听力题 (模拟)
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, stem_audio_url, correct_answer, answer_analysis, knowledge_point, tags)
VALUES
(@q5, @unit6_1_q, 'listening', 3,
'听录音，选择正确的地点：(播放音频)',
'/audio/unit1_listening_1.mp3',
'C',
'听力原文：Turn left at the cinema, then go straight. The bookstore is on your right.',
'听力理解',
'listening');

INSERT INTO tb_question_option (question_id, option_key, option_content, sort_order)
VALUES
(@q5, 'A', 'museum', 1),
(@q5, 'B', 'post office', 2),
(@q5, 'C', 'bookstore', 3),
(@q5, 'D', 'hospital', 4);

PRINT '题库数据插入完成';
GO

-- =============================================
-- 6. 插入徽章数据
-- =============================================
INSERT INTO tb_badge (badge_code, badge_name, badge_type, description, requirement_json, sort_order)
VALUES
('STREAK_3', '坚持 3 天', 'streak', '连续签到 3 天', '{"type": "streak", "value": 3}', 1),
('STREAK_7', '坚持 7 天', 'streak', '连续签到 7 天', '{"type": "streak", "value": 7}', 2),
('STREAK_15', '坚持 15 天', 'streak', '连续签到 15 天', '{"type": "streak", "value": 15}', 3),
('STREAK_30', '坚持 30 天', 'streak', '连续签到 30 天', '{"type": "streak", "value": 30}', 4),
('WORD_50', '词汇小新', 'word', '掌握 50 个单词', '{"type": "word_count", "value": 50}', 10),
('WORD_100', '词汇达人', 'word', '掌握 100 个单词', '{"type": "word_count", "value": 100}', 11),
('WORD_300', '词汇大师', 'word', '掌握 300 个单词', '{"type": "word_count", "value": 300}', 12),
('GRAMMAR_5', '语法新手', 'grammar', '完成 5 课语法学习', '{"type": "grammar_count", "value": 5}', 20),
('GRAMMAR_10', '语法能手', 'grammar', '完成 10 课语法学习', '{"type": "grammar_count", "value": 10}', 21),
('CHALLENGE_7', '挑战 7 天', 'challenge', '完成 7 次每日挑战', '{"type": "challenge_count", "value": 7}', 30),
('CHALLENGE_30', '挑战 30 天', 'challenge', '完成 30 次每日挑战', '{"type": "challenge_count", "value": 30}', 31),
('PERFECT_100', '满分达人', 'special', '每日挑战获得 100 分', '{"type": "perfect_score", "value": 1}', 40);

PRINT '徽章数据插入完成';
GO

-- =============================================
-- 7. 插入测试学习记录
-- =============================================
DECLARE @test_user UNIQUEIDENTIFIER = (SELECT id FROM tb_user WHERE username = 'xiaoming');
DECLARE @test_unit UNIQUEIDENTIFIER = (SELECT id FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=1);

-- 学习进度记录
INSERT INTO tb_learning_progress (user_id, grade_unit_id, content_type, content_id, status, score, attempts_count, last_attempt_at, completed_at)
SELECT TOP 5
    @test_user,
    @test_unit,
    'word',
    id,
    CASE WHEN id % 3 = 0 THEN 'completed' WHEN id % 3 = 1 THEN 'learning' ELSE 'not_started' END,
    CASE WHEN id % 3 = 0 THEN 100 WHEN id % 3 = 1 THEN 60 ELSE NULL END,
    CASE WHEN id % 3 = 0 THEN 2 WHEN id % 3 = 1 THEN 1 ELSE 0 END,
    GETDATE(),
    CASE WHEN id % 3 = 0 THEN GETDATE() ELSE NULL END
FROM tb_word WHERE grade_unit_id = @test_unit;

-- 错题记录
DECLARE @wrong_q1 UNIQUEIDENTIFIER = (SELECT id FROM tb_question WHERE question_type = 'single_choice' ORDER BY NEWID() OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY);

INSERT INTO tb_wrong_question (user_id, question_id, user_answer, correct_answer, error_type, review_status, review_count, next_review_at, first_wrong_at)
VALUES
(@test_user, @wrong_q1, 'B', 'A', '理解偏差', 'reviewing', 2, DATEADD(DAY, 3, GETDATE()), DATEADD(DAY, -5, GETDATE()));

-- 签到记录
INSERT INTO tb_checkin (user_id, checkin_date, points_earned, streak_days, bonus_points)
SELECT TOP 10
    @test_user,
    DATEADD(DAY, -10 + ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), CAST(GETDATE() AS DATE)),
    5,
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)),
    CASE WHEN ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) = 7 THEN 10 ELSE 0 END
FROM sys.objects;

-- 积分记录
INSERT INTO tb_user_points (user_id, points_type, change_type, change_amount, balance_after, description)
VALUES
(@test_user, 'points', 'signin', 5, 5, '每日签到'),
(@test_user, 'points', 'challenge', 50, 55, '完成每日挑战'),
(@test_user, 'points', 'word', 10, 65, '单词闯关'),
(@test_user, 'coins', 'signin', 5, 5, '每日签到奖励'),
(@test_user, 'coins', 'challenge', 20, 25, '完成每日挑战奖励');

PRINT '测试学习记录插入完成';
GO

-- =============================================
-- 验证数据
-- =============================================
PRINT '========================================';
PRINT '数据初始化完成！';
PRINT '========================================';
PRINT '用户数：' + CAST((SELECT COUNT(*) FROM tb_user) AS NVARCHAR);
PRINT '年级单元数：' + CAST((SELECT COUNT(*) FROM tb_grade_unit) AS NVARCHAR);
PRINT '单词数：' + CAST((SELECT COUNT(*) FROM tb_word) AS NVARCHAR);
PRINT '语法知识点数：' + CAST((SELECT COUNT(*) FROM tb_grammar) AS NVARCHAR);
PRINT '题目数：' + CAST((SELECT COUNT(*) FROM tb_question) AS NVARCHAR);
PRINT '徽章数：' + CAST((SELECT COUNT(*) FROM tb_badge) AS NVARCHAR);
PRINT '========================================';
GO
