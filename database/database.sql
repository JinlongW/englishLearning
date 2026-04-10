-- =============================================
-- 英语学习工具 - SQL Server 数据库脚本
-- 创建日期：2026-03-30
-- 数据库：SQL Server 2016+
-- =============================================

-- 创建数据库
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'EnglishLearning')
BEGIN
    CREATE DATABASE EnglishLearning;
END
GO

-- 设置数据库排序规则
ALTER DATABASE EnglishLearning COLLATE Chinese_PRC_CI_AS;
GO

USE EnglishLearning;
GO

-- =============================================
-- 1. 用户表 tb_user
-- =============================================
CREATE TABLE tb_user (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    username NVARCHAR(50) NOT NULL,
    password_hash NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20) NULL,
    student_name NVARCHAR(50) NOT NULL,
    grade_level INT NOT NULL CHECK (grade_level BETWEEN 1 AND 12),
    avatar_url NVARCHAR(200) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

CREATE INDEX IX_tb_user_phone ON tb_user(phone);
CREATE INDEX IX_tb_user_grade_level ON tb_user(grade_level);
GO

-- =============================================
-- 2. 用户画像表 tb_user_profile
-- =============================================
CREATE TABLE tb_user_profile (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    learning_style NVARCHAR(20) NULL,
    difficulty_level INT NOT NULL DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
    preferred_study_time TIME NULL,
    parent_notify_enabled BIT NOT NULL DEFAULT 1,
    total_learning_days INT NOT NULL DEFAULT 0,
    current_streak INT NOT NULL DEFAULT 0,
    max_streak INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_tb_user_profile_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_user_profile_user_id ON tb_user_profile(user_id);
GO

-- =============================================
-- 3. 年级单元表 tb_grade_unit
-- =============================================
CREATE TABLE tb_grade_unit (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 12),
    semester NVARCHAR(10) NOT NULL CHECK (semester IN ('上', '下')),
    unit_no INT NOT NULL,
    unit_name NVARCHAR(100) NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    is_locked BIT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

CREATE UNIQUE INDEX IX_tb_grade_unit_grade_semester_unit
ON tb_grade_unit(grade, semester, unit_no);
GO

-- =============================================
-- 4. 单词表 tb_word
-- =============================================
CREATE TABLE tb_word (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    grade_unit_id UNIQUEIDENTIFIER NOT NULL,
    word NVARCHAR(50) NOT NULL,
    phonetic_uk NVARCHAR(50) NULL,
    phonetic_us NVARCHAR(50) NULL,
    audio_url NVARCHAR(200) NULL,
    meaning_cn NVARCHAR(500) NOT NULL,
    meaning_trans NVARCHAR(MAX) NULL,
    part_of_speech NVARCHAR(20) NULL,
    example_en NVARCHAR(MAX) NULL,
    example_cn NVARCHAR(MAX) NULL,
    image_url NVARCHAR(200) NULL,
    sort_order INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_tb_word_grade_unit FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_word_grade_unit ON tb_word(grade_unit_id);
CREATE INDEX IX_tb_word_word ON tb_word(word);
GO

-- =============================================
-- 5. 语法知识点表 tb_grammar
-- =============================================
CREATE TABLE tb_grammar (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    grade_unit_id UNIQUEIDENTIFIER NOT NULL,
    title NVARCHAR(100) NOT NULL,
    content_type NVARCHAR(20) NOT NULL CHECK (content_type IN ('video', 'article')),
    video_url NVARCHAR(200) NULL,
    content_json NVARCHAR(MAX) NULL,
    duration_seconds INT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    quiz_json NVARCHAR(MAX) NULL,
    passing_score INT NOT NULL DEFAULT 60,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_grammar_grade_unit FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_grammar_grade_unit ON tb_grammar(grade_unit_id);
GO

-- =============================================
-- 6. 题库表 tb_question
-- =============================================
CREATE TABLE tb_question (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    grade_unit_id UNIQUEIDENTIFIER NOT NULL,
    question_type NVARCHAR(20) NOT NULL CHECK (question_type IN (
        'single_choice', 'multiple_choice', 'fill_blank',
        'spell_word', 'match', 'listening'
    )),
    difficulty INT NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
    question_stem NVARCHAR(MAX) NOT NULL,
    stem_audio_url NVARCHAR(200) NULL,
    correct_answer NVARCHAR(MAX) NOT NULL,
    answer_analysis NVARCHAR(MAX) NULL,
    knowledge_point NVARCHAR(100) NULL,
    tags NVARCHAR(200) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_question_grade_unit FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_question_grade_unit ON tb_question(grade_unit_id);
CREATE INDEX IX_tb_question_type ON tb_question(question_type);
CREATE INDEX IX_tb_question_difficulty ON tb_question(difficulty);
CREATE INDEX IX_tb_question_knowledge_point ON tb_question(knowledge_point);
GO

-- =============================================
-- 7. 题目选项表 tb_question_option
-- =============================================
CREATE TABLE tb_question_option (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    question_id UNIQUEIDENTIFIER NOT NULL,
    option_key NVARCHAR(5) NOT NULL,
    option_content NVARCHAR(500) NOT NULL,
    image_url NVARCHAR(200) NULL,
    audio_url NVARCHAR(200) NULL,
    sort_order INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_tb_question_option_question FOREIGN KEY (question_id) REFERENCES tb_question(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_question_option_question ON tb_question_option(question_id);
GO

-- =============================================
-- 8. 学习进度表 tb_learning_progress
-- =============================================
CREATE TABLE tb_learning_progress (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    grade_unit_id UNIQUEIDENTIFIER NOT NULL,
    content_type NVARCHAR(20) NOT NULL CHECK (content_type IN ('word', 'grammar', 'question')),
    content_id UNIQUEIDENTIFIER NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'not_started'
        CHECK (status IN ('not_started', 'learning', 'completed', 'mastered')),
    score INT NULL,
    attempts_count INT NOT NULL DEFAULT 0,
    last_attempt_at DATETIME2 NULL,
    completed_at DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_learning_progress_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE,
    CONSTRAINT FK_tb_learning_progress_grade_unit FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_learning_progress_unique
ON tb_learning_progress(user_id, content_type, content_id);
CREATE INDEX IX_tb_learning_progress_user_status ON tb_learning_progress(user_id, status);
GO

-- =============================================
-- 9. 错题本表 tb_wrong_question
-- =============================================
CREATE TABLE tb_wrong_question (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    question_id UNIQUEIDENTIFIER NOT NULL,
    user_answer NVARCHAR(MAX) NOT NULL,
    correct_answer NVARCHAR(MAX) NOT NULL,
    error_type NVARCHAR(50) NULL,
    review_status NVARCHAR(20) NOT NULL DEFAULT 'new'
        CHECK (review_status IN ('new', 'reviewing', 'mastered')),
    review_count INT NOT NULL DEFAULT 0,
    next_review_at DATETIME2 NULL,
    first_wrong_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    last_review_at DATETIME2 NULL,
    mastered_at DATETIME2 NULL,
    is_deleted BIT NOT NULL DEFAULT 0,
    CONSTRAINT FK_tb_wrong_question_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE,
    CONSTRAINT FK_tb_wrong_question_question FOREIGN KEY (question_id) REFERENCES tb_question(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_wrong_question_user_review
ON tb_wrong_question(user_id, review_status, next_review_at)
WHERE is_deleted = 0;
CREATE INDEX IX_tb_wrong_question_next_review
ON tb_wrong_question(next_review_at)
WHERE review_status = 'reviewing' AND is_deleted = 0;
GO

-- =============================================
-- 10. 每日挑战主表 tb_daily_challenge
-- =============================================
CREATE TABLE tb_daily_challenge (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    challenge_date DATE NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_progress', 'completed')),
    total_questions INT NOT NULL DEFAULT 10,
    correct_count INT NOT NULL DEFAULT 0,
    score INT NOT NULL DEFAULT 0,
    time_used_seconds INT NOT NULL DEFAULT 0,
    points_earned INT NOT NULL DEFAULT 0,
    coins_earned INT NOT NULL DEFAULT 0,
    started_at DATETIME2 NULL,
    completed_at DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_daily_challenge_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_daily_challenge_unique
ON tb_daily_challenge(user_id, challenge_date);
CREATE INDEX IX_tb_daily_challenge_date ON tb_daily_challenge(challenge_date);
GO

-- =============================================
-- 11. 每日挑战详情表 tb_daily_challenge_detail
-- =============================================
CREATE TABLE tb_daily_challenge_detail (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    daily_challenge_id UNIQUEIDENTIFIER NOT NULL,
    question_id UNIQUEIDENTIFIER NOT NULL,
    question_order INT NOT NULL,
    user_answer NVARCHAR(MAX) NOT NULL,
    is_correct BIT NOT NULL DEFAULT 0,
    time_used_seconds INT NOT NULL DEFAULT 0,
    is_uncertain BIT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_daily_challenge_detail_challenge
        FOREIGN KEY (daily_challenge_id) REFERENCES tb_daily_challenge(id) ON DELETE CASCADE,
    CONSTRAINT FK_tb_daily_challenge_detail_question
        FOREIGN KEY (question_id) REFERENCES tb_question(id)
);
GO

CREATE INDEX IX_tb_daily_challenge_detail_challenge
ON tb_daily_challenge_detail(daily_challenge_id);
GO

-- =============================================
-- 12. 用户等级表 tb_user_level
-- =============================================
CREATE TABLE tb_user_level (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    current_level INT NOT NULL DEFAULT 1,
    level_name NVARCHAR(50) NOT NULL DEFAULT '英语小白',
    current_exp INT NOT NULL DEFAULT 0,
    exp_to_next INT NOT NULL DEFAULT 100,
    level_up_at DATETIME2 NULL,
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_user_level_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_user_level_user ON tb_user_level(user_id);
GO

-- =============================================
-- 13. 徽章表 tb_badge
-- =============================================
CREATE TABLE tb_badge (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    badge_code NVARCHAR(50) NOT NULL UNIQUE,
    badge_name NVARCHAR(100) NOT NULL,
    badge_icon NVARCHAR(200) NULL,
    badge_type NVARCHAR(50) NOT NULL CHECK (badge_type IN ('streak', 'word', 'grammar', 'challenge', 'special')),
    description NVARCHAR(500) NOT NULL,
    requirement_json NVARCHAR(MAX) NULL,
    sort_order INT NOT NULL DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

CREATE INDEX IX_tb_badge_type ON tb_badge(badge_type);
GO

-- =============================================
-- 14. 用户徽章表 tb_user_badge
-- =============================================
CREATE TABLE tb_user_badge (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    badge_id UNIQUEIDENTIFIER NOT NULL,
    earned_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    is_new BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_tb_user_badge_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE,
    CONSTRAINT FK_tb_user_badge_badge FOREIGN KEY (badge_id) REFERENCES tb_badge(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_user_badge_unique ON tb_user_badge(user_id, badge_id);
CREATE INDEX IX_tb_user_badge_user_new ON tb_user_badge(user_id) WHERE is_new = 1;
GO

-- =============================================
-- 15. 积分记录表 tb_user_points
-- =============================================
CREATE TABLE tb_user_points (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    points_type NVARCHAR(20) NOT NULL CHECK (points_type IN ('points', 'coins')),
    change_type NVARCHAR(50) NOT NULL,
    change_amount INT NOT NULL,
    balance_after INT NOT NULL,
    description NVARCHAR(200) NOT NULL,
    reference_id UNIQUEIDENTIFIER NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_user_points_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE
);
GO

CREATE INDEX IX_tb_user_points_user ON tb_user_points(user_id);
CREATE INDEX IX_tb_user_points_created ON tb_user_points(created_at);
GO

-- =============================================
-- 16. 签到记录表 tb_checkin
-- =============================================
CREATE TABLE tb_checkin (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER NOT NULL,
    checkin_date DATE NOT NULL,
    points_earned INT NOT NULL DEFAULT 5,
    streak_days INT NOT NULL DEFAULT 1,
    bonus_points INT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_tb_checkin_user FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX IX_tb_checkin_unique ON tb_checkin(user_id, checkin_date);
GO

-- =============================================
-- 17. 系统配置表 tb_system_config
-- =============================================
CREATE TABLE tb_system_config (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    config_key NVARCHAR(100) NOT NULL UNIQUE,
    config_value NVARCHAR(MAX) NOT NULL,
    config_type NVARCHAR(50) NOT NULL DEFAULT 'json'
        CHECK (config_type IN ('json', 'text', 'number', 'boolean')),
    description NVARCHAR(200) NULL,
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- =============================================
-- 初始化系统配置数据
-- =============================================
INSERT INTO tb_system_config (config_key, config_value, config_type, description) VALUES
('level_config', N'{
    "levels": [
        {"level": 1, "name": "英语小白", "exp_required": 0},
        {"level": 2, "name": "入门学徒", "exp_required": 100},
        {"level": 3, "name": "进步之星", "exp_required": 300},
        {"level": 4, "name": "勤奋少年", "exp_required": 600},
        {"level": 5, "name": "英语新星", "exp_required": 1000},
        {"level": 6, "name": "学习能手", "exp_required": 1500},
        {"level": 7, "name": "词汇达人", "exp_required": 2200},
        {"level": 8, "name": "语法高手", "exp_required": 3000},
        {"level": 9, "name": "英语达人", "exp_required": 4000},
        {"level": 10, "name": "英语大师", "exp_required": 5500},
        {"level": 11, "name": "单词王者", "exp_required": 7500},
        {"level": 12, "name": "英语学霸", "exp_required": 10000}
    ]
}', 'json', '等级配置'),
('points_rules', N'{
    "signin": 5,
    "daily_challenge_complete": 50,
    "word_level_complete": 10,
    "grammar_level_complete": 20,
    "streak_bonus_7days": 10,
    "streak_bonus_30days": 50,
    "perfect_score_bonus": 20
}', 'json', '积分规则'),
('review_intervals', N'[0, 5, 1440, 4320, 10080, 21600, 43200]', 'json', '艾宾浩斯复习间隔 (分钟): 即时，5 分钟，1 天，3 天，7 天，15 天，30 天'),
('badge_rules', N'{
    "streak_7days": {"badge_code": "STREAK_7", "requirement": {"type": "streak", "value": 7}},
    "streak_30days": {"badge_code": "STREAK_30", "requirement": {"type": "streak", "value": 30}},
    "word_100": {"badge_code": "WORD_100", "requirement": {"type": "word_count", "value": 100}},
    "perfect_challenge": {"badge_code": "PERFECT_CHALLENGE", "requirement": {"type": "perfect_score", "value": 1}}
}', 'json', '徽章规则');
GO

-- =============================================
-- 创建更新时间触发器
-- =============================================
-- tb_user 更新时间触发器
CREATE TRIGGER trg_tb_user_update ON tb_user
AFTER UPDATE AS
BEGIN
    UPDATE tb_user SET updated_at = GETDATE()
    FROM tb_user u INNER JOIN inserted i ON u.id = i.id;
END
GO

-- tb_question 更新时间触发器
CREATE TRIGGER trg_tb_question_update ON tb_question
AFTER UPDATE AS
BEGIN
    UPDATE tb_question SET updated_at = GETDATE()
    FROM tb_question q INNER JOIN inserted i ON q.id = i.id;
END
GO

-- tb_learning_progress 更新时间触发器
CREATE TRIGGER trg_tb_learning_progress_update ON tb_learning_progress
AFTER UPDATE AS
BEGIN
    UPDATE tb_learning_progress SET updated_at = GETDATE()
    FROM tb_learning_progress lp INNER JOIN inserted i ON lp.id = i.id;
END
GO

-- tb_user_level 更新时间触发器
CREATE TRIGGER trg_tb_user_level_update ON tb_user_level
AFTER UPDATE AS
BEGIN
    UPDATE tb_user_level SET updated_at = GETDATE()
    FROM tb_user_level ul INNER JOIN inserted i ON ul.id = i.id;
END
GO

-- tb_system_config 更新时间触发器
CREATE TRIGGER trg_tb_system_config_update ON tb_system_config
AFTER UPDATE AS
BEGIN
    UPDATE tb_system_config SET updated_at = GETDATE()
    FROM tb_system_config sc INNER JOIN inserted i ON sc.id = i.id;
END
GO

-- =============================================
-- 视图：用户学习统计
-- =============================================
CREATE VIEW vw_user_learning_summary AS
SELECT
    u.id AS user_id,
    u.student_name,
    u.grade_level,
    up.current_streak,
    up.max_streak,
    up.total_learning_days,
    ul.current_level,
    ul.level_name,
    ul.current_exp,
    (SELECT COUNT(*) FROM tb_wrong_question wq WHERE wq.user_id = u.id AND wq.is_deleted = 0) AS wrong_question_count,
    (SELECT SUM(change_amount) FROM tb_user_points up2 WHERE up2.user_id = u.id AND up2.points_type = 'points') AS total_points,
    (SELECT SUM(change_amount) FROM tb_user_points up3 WHERE up3.user_id = u.id AND up3.points_type = 'coins') AS total_coins,
    (SELECT COUNT(*) FROM tb_checkin c WHERE c.user_id = u.id) AS total_checkin_days
FROM tb_user u
LEFT JOIN tb_user_profile up ON u.id = up.user_id
LEFT JOIN tb_user_level ul ON u.id = ul.user_id;
GO

-- =============================================
-- 视图：错题复习推送
-- =============================================
CREATE VIEW vw_wrong_question_review AS
SELECT
    wq.id,
    wq.user_id,
    wq.question_id,
    q.question_stem,
    q.question_type,
    q.knowledge_point,
    wq.user_answer,
    wq.correct_answer,
    wq.review_count,
    wq.next_review_at,
    DATEDIFF(MINUTE, GETDATE(), wq.next_review_at) AS minutes_until_review
FROM tb_wrong_question wq
INNER JOIN tb_question q ON wq.question_id = q.id
WHERE wq.is_deleted = 0
  AND wq.review_status IN ('new', 'reviewing')
  AND (wq.next_review_at IS NULL OR wq.next_review_at <= GETDATE());
GO

PRINT '数据库创建完成！';
PRINT '共创建 17 张表，4 个触发器，2 个视图';
GO
