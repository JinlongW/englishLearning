-- 人教版小学英语题库数据库 - 索引和外键优化脚本
-- 执行日期：2026-04-01
-- 说明：添加缺失的索引和外键约束，提升查询性能和数据完整性

USE EnglishLearning;
GO

-- ==================== 一、外键约束 ====================

PRINT '========== 添加外键约束 ==========';

-- Word -> GradeUnit
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_word_grade_unit')
BEGIN
    ALTER TABLE tb_word ADD CONSTRAINT FK_word_grade_unit
    FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE;
    PRINT '已添加：FK_word_grade_unit';
END

-- Grammar -> GradeUnit
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_grammar_grade_unit')
BEGIN
    ALTER TABLE tb_grammar ADD CONSTRAINT FK_grammar_grade_unit
    FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE;
    PRINT '已添加：FK_grammar_grade_unit';
END

-- Question -> GradeUnit
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_question_grade_unit')
BEGIN
    ALTER TABLE tb_question ADD CONSTRAINT FK_question_grade_unit
    FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id) ON DELETE CASCADE;
    PRINT '已添加：FK_question_grade_unit';
END

-- QuestionOption -> Question
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_question_option_question')
BEGIN
    ALTER TABLE tb_question_option ADD CONSTRAINT FK_question_option_question
    FOREIGN KEY (question_id) REFERENCES tb_question(id) ON DELETE CASCADE;
    PRINT '已添加：FK_question_option_question';
END

-- LearningProgress -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_learning_progress_user')
BEGIN
    ALTER TABLE tb_learning_progress ADD CONSTRAINT FK_learning_progress_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id);
    PRINT '已添加：FK_learning_progress_user';
END

-- LearningProgress -> GradeUnit
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_learning_progress_grade_unit')
BEGIN
    ALTER TABLE tb_learning_progress ADD CONSTRAINT FK_learning_progress_grade_unit
    FOREIGN KEY (grade_unit_id) REFERENCES tb_grade_unit(id);
    PRINT '已添加：FK_learning_progress_grade_unit';
END

-- WrongQuestion -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_wrong_question_user')
BEGIN
    ALTER TABLE tb_wrong_question ADD CONSTRAINT FK_wrong_question_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id);
    PRINT '已添加：FK_wrong_question_user';
END

-- WrongQuestion -> Question
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_wrong_question_question')
BEGIN
    ALTER TABLE tb_wrong_question ADD CONSTRAINT FK_wrong_question_question
    FOREIGN KEY (question_id) REFERENCES tb_question(id);
    PRINT '已添加：FK_wrong_question_question';
END

-- DailyChallenge -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_daily_challenge_user')
BEGIN
    ALTER TABLE tb_daily_challenge ADD CONSTRAINT FK_daily_challenge_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_daily_challenge_user';
END

-- DailyChallengeDetail -> DailyChallenge
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_daily_challenge_detail_challenge')
BEGIN
    ALTER TABLE tb_daily_challenge_detail ADD CONSTRAINT FK_daily_challenge_detail_challenge
    FOREIGN KEY (daily_challenge_id) REFERENCES tb_daily_challenge(id) ON DELETE CASCADE;
    PRINT '已添加：FK_daily_challenge_detail_challenge';
END

-- DailyChallengeDetail -> Question
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_daily_challenge_detail_question')
BEGIN
    ALTER TABLE tb_daily_challenge_detail ADD CONSTRAINT FK_daily_challenge_detail_question
    FOREIGN KEY (question_id) REFERENCES tb_question(id);
    PRINT '已添加：FK_daily_challenge_detail_question';
END

-- UserProfile -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_user_profile_user')
BEGIN
    ALTER TABLE tb_user_profile ADD CONSTRAINT FK_user_profile_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_user_profile_user';
END

-- UserLevel -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_user_level_user')
BEGIN
    ALTER TABLE tb_user_level ADD CONSTRAINT FK_user_level_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_user_level_user';
END

-- UserBadge -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_user_badge_user')
BEGIN
    ALTER TABLE tb_user_badge ADD CONSTRAINT FK_user_badge_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_user_badge_user';
END

-- UserBadge -> Badge
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_user_badge_badge')
BEGIN
    ALTER TABLE tb_user_badge ADD CONSTRAINT FK_user_badge_badge
    FOREIGN KEY (badge_id) REFERENCES tb_badge(id);
    PRINT '已添加：FK_user_badge_badge';
END

-- UserPoints -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_user_points_user')
BEGIN
    ALTER TABLE tb_user_points ADD CONSTRAINT FK_user_points_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_user_points_user';
END

-- Checkin -> User
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_checkin_user')
BEGIN
    ALTER TABLE tb_checkin ADD CONSTRAINT FK_checkin_user
    FOREIGN KEY (user_id) REFERENCES tb_user(id) ON DELETE CASCADE;
    PRINT '已添加：FK_checkin_user';
END

-- ==================== 二、唯一索引 ====================

PRINT '========== 添加唯一索引 ==========';

-- Username 唯一索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_username')
BEGIN
    CREATE UNIQUE INDEX IX_user_username ON tb_user(username) WHERE is_active = 1;
    PRINT '已添加：IX_user_username';
END

-- Badge code 唯一索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_badge_code')
BEGIN
    CREATE UNIQUE INDEX IX_badge_code ON tb_badge(badge_code);
    PRINT '已添加：IX_badge_code';
END

-- GradeUnit 唯一索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_grade_unit_unique')
BEGIN
    CREATE UNIQUE INDEX IX_grade_unit_unique ON tb_grade_unit(grade, semester, unit_no);
    PRINT '已添加：IX_grade_unit_unique';
END

-- UserProfile 唯一索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_profile_user')
BEGIN
    CREATE UNIQUE INDEX IX_user_profile_user ON tb_user_profile(user_id);
    PRINT '已添加：IX_user_profile_user';
END

-- UserLevel 唯一索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_level_user')
BEGIN
    CREATE UNIQUE INDEX IX_user_level_user ON tb_user_level(user_id);
    PRINT '已添加：IX_user_level_user';
END

-- DailyChallenge 唯一索引 (每用户每天一个挑战)
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_daily_challenge_user_date')
BEGIN
    CREATE UNIQUE INDEX IX_daily_challenge_user_date ON tb_daily_challenge(user_id, challenge_date);
    PRINT '已添加：IX_daily_challenge_user_date';
END

-- Checkin 唯一索引 (每用户每天签到一次)
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_checkin_user_date')
BEGIN
    CREATE UNIQUE INDEX IX_checkin_user_date ON tb_checkin(user_id, checkin_date);
    PRINT '已添加：IX_checkin_user_date';
END

-- ==================== 三、普通索引 ====================

PRINT '========== 添加普通索引 ==========';

-- Word 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_word_grade_unit_id')
BEGIN
    CREATE INDEX IX_word_grade_unit_id ON tb_word(grade_unit_id);
    PRINT '已添加：IX_word_grade_unit_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_word_grade_unit_sort')
BEGIN
    CREATE INDEX IX_word_grade_unit_sort ON tb_word(grade_unit_id, sort_order);
    PRINT '已添加：IX_word_grade_unit_sort';
END

-- Grammar 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_grammar_grade_unit_id')
BEGIN
    CREATE INDEX IX_grammar_grade_unit_id ON tb_grammar(grade_unit_id);
    PRINT '已添加：IX_grammar_grade_unit_id';
END

-- Question 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_question_grade_unit_id')
BEGIN
    CREATE INDEX IX_question_grade_unit_id ON tb_question(grade_unit_id);
    PRINT '已添加：IX_question_grade_unit_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_question_active_difficulty')
BEGIN
    CREATE INDEX IX_question_active_difficulty ON tb_question(grade_unit_id, is_active, difficulty);
    PRINT '已添加：IX_question_active_difficulty';
END

-- QuestionOption 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_question_option_question_id')
BEGIN
    CREATE INDEX IX_question_option_question_id ON tb_question_option(question_id);
    PRINT '已添加：IX_question_option_question_id';
END

-- LearningProgress 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_learning_progress_user_id')
BEGIN
    CREATE INDEX IX_learning_progress_user_id ON tb_learning_progress(user_id);
    PRINT '已添加：IX_learning_progress_user_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_learning_progress_grade_unit_id')
BEGIN
    CREATE INDEX IX_learning_progress_grade_unit_id ON tb_learning_progress(grade_unit_id);
    PRINT '已添加：IX_learning_progress_grade_unit_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_learning_progress_content')
BEGIN
    CREATE INDEX IX_learning_progress_content ON tb_learning_progress(user_id, content_type, content_id);
    PRINT '已添加：IX_learning_progress_content';
END

-- WrongQuestion 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_wrong_question_user_id')
BEGIN
    CREATE INDEX IX_wrong_question_user_id ON tb_wrong_question(user_id);
    PRINT '已添加：IX_wrong_question_user_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_wrong_question_review')
BEGIN
    CREATE INDEX IX_wrong_question_review ON tb_wrong_question(user_id, review_status) WHERE is_deleted = 0;
    PRINT '已添加：IX_wrong_question_review';
END

-- DailyChallenge 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_daily_challenge_user_id')
BEGIN
    CREATE INDEX IX_daily_challenge_user_id ON tb_daily_challenge(user_id);
    PRINT '已添加：IX_daily_challenge_user_id';
END

-- DailyChallengeDetail 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_daily_challenge_detail_challenge_id')
BEGIN
    CREATE INDEX IX_daily_challenge_detail_challenge_id ON tb_daily_challenge_detail(daily_challenge_id);
    PRINT '已添加：IX_daily_challenge_detail_challenge_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_daily_challenge_detail_question_id')
BEGIN
    CREATE INDEX IX_daily_challenge_detail_question_id ON tb_daily_challenge_detail(question_id);
    PRINT '已添加：IX_daily_challenge_detail_question_id';
END

-- UserBadge 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_badge_user_id')
BEGIN
    CREATE INDEX IX_user_badge_user_id ON tb_user_badge(user_id);
    PRINT '已添加：IX_user_badge_user_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_badge_badge_id')
BEGIN
    CREATE INDEX IX_user_badge_badge_id ON tb_user_badge(badge_id);
    PRINT '已添加：IX_user_badge_badge_id';
END

-- UserPoints 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_points_user_id')
BEGIN
    CREATE INDEX IX_user_points_user_id ON tb_user_points(user_id);
    PRINT '已添加：IX_user_points_user_id';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_user_points_type')
BEGIN
    CREATE INDEX IX_user_points_type ON tb_user_points(user_id, points_type);
    PRINT '已添加：IX_user_points_type';
END

-- Checkin 表索引
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_checkin_user_id')
BEGIN
    CREATE INDEX IX_checkin_user_id ON tb_checkin(user_id);
    PRINT '已添加：IX_checkin_user_id';
END

PRINT '========== 优化脚本执行完成 ==========';
GO
