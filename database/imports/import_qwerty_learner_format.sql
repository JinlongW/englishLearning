-- =============================================
-- 数据导入脚本：从 qwerty-learner 格式导入单词
-- 日期：2026-04-02
-- 说明：导入人教版小学英语三年级上册 Unit 1 单词
-- =============================================

USE EnglishLearning;
GO

-- =============================================
-- 获取三年级上册 Unit 1 的 grade_unit_id
-- =============================================
DECLARE @grade3_1_unit1 UNIQUEIDENTIFIER = (
    SELECT id FROM tb_grade_unit
    WHERE grade = 3 AND semester = '上' AND unit_no = 1
);

IF @grade3_1_unit1 IS NULL
BEGIN
    -- 如果单元不存在，先创建
    INSERT INTO tb_grade_unit (grade, semester, unit_no, unit_name, sort_order)
    VALUES (3, '上', 1, 'Unit 1 Hello!', 1);

    SET @grade3_1_unit1 = SCOPE_IDENTITY();
    PRINT '已创建三年级上册 Unit 1';
END
ELSE
BEGIN
    PRINT '使用现有的三年级上册 Unit 1';
END
GO

-- =============================================
-- 导入单词数据 (qwerty-learner 格式转换)
-- =============================================
-- 使用 MERGE 语句实现存在则更新，不存在则插入
DECLARE @unit_id UNIQUEIDENTIFIER = (
    SELECT id FROM tb_grade_unit WHERE grade = 3 AND semester = '上' AND unit_no = 1
);

-- Unit 1 Hello! 单词列表
MERGE tb_word AS target
USING (
    VALUES
    -- 学习用品
    ('ruler', '/''ruːlə/', '/''rulɚ/', '尺子', JSON_QUERY('["尺子"]'), 'n.', '', '', 1),
    ('pencil', '/''pens(ə)l; -sɪl/', '/''pɛnsl/', '铅笔', JSON_QUERY('["铅笔"]'), 'n.', '', '', 2),
    ('eraser', 'ɪ''reɪzə/', 'ɪ''resɚ/', '橡皮', JSON_QUERY('["橡皮"]'), 'n.', '', '', 3),
    ('crayon', 'ˈkreɪən/', 'kreən/', '蜡笔', JSON_QUERY('["蜡笔"]'), 'n.', '', '', 4),
    ('bag', 'bæg/', 'bæɡ/', '包', JSON_QUERY('["包"]'), 'n.', '', '', 5),
    ('pen', 'pen/', 'pɛn/', '钢笔', JSON_QUERY('["钢笔"]'), 'n.', '', '', 6),
    ('pencil box', '/''pensl bɒks/', '/''pɛnsl bɑks/', '铅笔盒', JSON_QUERY('["铅笔盒"]'), 'n.', '', '', 7),
    ('book', 'bʊk/', 'bʊk/', '书', JSON_QUERY('["书"]'), 'n.', '', '', 8),

    -- 其他基础词汇
    ('no', 'nəʊ/', 'no/', '不', JSON_QUERY('["不"]'), 'adv./det.', '', '', 9),
    ('your', 'jɔ:(r)/', 'jʊər; jʊr/', '你（们）的', JSON_QUERY('["你（们）的"]'), 'pron.', '', '', 10),

    -- 颜色
    ('red', 'red/', 'rɛd/', '红色；红色的', JSON_QUERY('["红色", "红色的"]'), 'n./adj.', '', '', 11),
    ('green', 'griːn/', 'ɡrin/', '绿色；绿色的', JSON_QUERY('["绿色", "绿色的"]'), 'n./adj.', '', '', 12),
    ('yellow', '''jeləʊ/', '''jɛlo/', '黄色；黄色的', JSON_QUERY('["黄色", "黄色的"]'), 'n./adj.', '', '', 13),
    ('blue', 'bluː/', 'blu/', '蓝色；蓝色的', JSON_QUERY('["蓝色", "蓝色的"]'), 'n./adj.', '', '', 14),
    ('black', 'blæk/', 'blæk/', '黑色；黑色的', JSON_QUERY('["黑色", "黑色的"]'), 'n./adj.', '', '', 15),
    ('brown', 'braʊn/', 'braʊn/', '棕色；棕色的', JSON_QUERY('["棕色", "棕色的"]'), 'n./adj.', '', '', 16),
    ('white', 'waɪt/', 'hwaɪt/', '白色；白色的', JSON_QUERY('["白色", "白色的"]'), 'n./adj.', '', '', 17),
    ('orange', '''ɒrɪn(d)ʒ/', '''ɔrɪndʒ/', '橙色；橙色的', JSON_QUERY('["橙色", "橙色的"]'), 'n./adj.', '', '', 18),

    -- 其他
    ('OK', '', '', '好；行', JSON_QUERY('["好", "行"]'), 'adj./adv.', '', '', 19),
    ('mum', 'mʌm/', 'mʌm/', '妈妈', JSON_QUERY('["妈妈"]'), 'n.', '', '', 20)
) AS source (word, phonetic_uk, phonetic_us, meaning_cn, meaning_trans, part_of_speech, example_en, example_cn, sort_order)
ON target.word = source.word AND target.grade_unit_id = @unit_id
WHEN MATCHED THEN
    UPDATE SET
        target.phonetic_uk = source.phonetic_uk,
        target.phonetic_us = source.phonetic_us,
        target.meaning_cn = source.meaning_cn,
        target.meaning_trans = source.meaning_trans,
        target.part_of_speech = source.part_of_speech,
        target.sort_order = source.sort_order,
        target.updated_at = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, meaning_trans, part_of_speech, example_en, example_cn, sort_order)
    VALUES (@unit_id, source.word, source.phonetic_uk, source.phonetic_us, source.meaning_cn, source.meaning_trans, source.part_of_speech, source.example_en, source.example_cn, source.sort_order);

PRINT '三年级上册 Unit 1 单词导入完成';
GO

-- =============================================
-- 验证导入结果
-- =============================================
PRINT '========================================';
PRINT '单词导入验证';
PRINT '========================================';

SELECT
    w.word AS 单词，
    w.phonetic_uk AS 英音，
    w.phonetic_us AS 美音，
    w.meaning_cn AS 主释义，
    w.meaning_trans AS 多释义 JSON,
    w.part_of_speech AS 词性
FROM tb_word w
INNER JOIN tb_grade_unit gu ON w.grade_unit_id = gu.id
WHERE gu.grade = 3 AND gu.semester = '上' AND gu.unit_no = 1
ORDER BY w.sort_order;
GO
