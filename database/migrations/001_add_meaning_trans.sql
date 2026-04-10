-- =============================================
-- 迁移脚本 001: 为 tb_word 表增加多释义支持
-- 日期：2026-04-02
-- 说明：增加 meaning_trans 字段存储 JSON 格式的多释义
-- =============================================

USE EnglishLearning;
GO

-- =============================================
-- 1. 增加 meaning_trans 字段
-- =============================================
IF NOT EXISTS (SELECT 1 FROM sys.columns
               WHERE object_id = OBJECT_ID(N'[dbo].[tb_word]')
               AND name = 'meaning_trans')
BEGIN
    ALTER TABLE tb_word ADD meaning_trans NVARCHAR(MAX) NULL;
    PRINT '已添加 meaning_trans 字段';
END
ELSE
BEGIN
    PRINT 'meaning_trans 字段已存在，跳过';
END
GO

-- =============================================
-- 2. 数据迁移：将现有 meaning_cn 转换为 JSON 格式存入 meaning_trans
-- =============================================
-- 更新现有数据，将单个释义转换为数组格式
UPDATE tb_word
SET meaning_trans = JSON_QUERY('["' + REPLACE(meaning_cn, '"', '\"') + '"]')
WHERE meaning_trans IS NULL AND meaning_cn IS NOT NULL;

PRINT '已完成现有数据的 meaning_trans 转换';
GO

-- =============================================
-- 3. 创建计算列 main_meaning (可选，用于向后兼容)
-- =============================================
-- 从 meaning_trans JSON 数组中提取第一个释义作为主要释义
IF NOT EXISTS (SELECT 1 FROM sys.computed_columns
               WHERE object_id = OBJECT_ID(N'[dbo].[tb_word]')
               AND name = 'main_meaning')
BEGIN
    -- 注意：SQL Server 不支持直接添加从 JSON 提取的计算列，需要应用层处理
    -- 或者使用视图来提供这个功能
    PRINT '计算列需要通过视图或应用层处理';
END
GO

-- =============================================
-- 4. 创建视图 vw_word_with_meanings (方便查询多释义)
-- =============================================
IF EXISTS (SELECT 1 FROM sys.views WHERE name = 'vw_word_with_meanings')
    DROP VIEW vw_word_with_meanings;
GO

CREATE VIEW vw_word_with_meanings AS
SELECT
    w.*,
    -- 从 JSON 数组提取释义数量
    ISNULL(JSON_VALUE(w.meaning_trans, '$[0]'), w.meaning_cn) AS main_meaning,
    ISNULL(JSON_VALUE(w.meaning_trans, '$[1]'), '') AS meaning_2,
    ISNULL(JSON_VALUE(w.meaning_trans, '$[2]'), '') AS meaning_3,
    ISNULL(JSON_VALUE(w.meaning_trans, '$[3]'), '') AS meaning_4,
    ISNULL(JSON_VALUE(w.meaning_trans, '$[4]'), '') AS meaning_5
FROM tb_word w;
GO

PRINT '已创建视图 vw_word_with_meanings';
GO

-- =============================================
-- 5. 增加索引优化 JSON 查询性能
-- =============================================
-- 为经常查询的单词字段增加覆盖索引
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_tb_word_meaning_lookup')
BEGIN
    CREATE NONCLUSTERED INDEX IX_tb_word_meaning_lookup
    ON tb_word(word)
    INCLUDE (meaning_cn, meaning_trans, part_of_speech);

    PRINT '已创建索引 IX_tb_word_meaning_lookup';
END
GO

-- =============================================
-- 验证迁移结果
-- =============================================
PRINT '========================================';
PRINT '迁移脚本 001 执行完成！';
PRINT '========================================';
PRINT 'tb_word 表结构已更新:';
PRINT '  - 新增 meaning_trans 字段 (JSON 数组格式)';
PRINT '  - 现有数据已转换';
PRINT '  - 创建视图 vw_word_with_meanings';
PRINT '========================================';

-- 显示示例数据
SELECT TOP 5
    word,
    meaning_cn,
    meaning_trans,
    JSON_VALUE(meaning_trans, '$[0]') AS main_meaning_json
FROM tb_word;
GO
