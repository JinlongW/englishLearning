USE EnglishLearning;
GO

-- 统计各年级数据
SELECT
    gu.grade AS 年级，
    gu.semester AS 学期，
    COUNT(DISTINCT gu.id) AS 单元数，
    COUNT(w.id) AS 单词数,
    COUNT(CASE WHEN w.meaning_trans LIKE '%,%' THEN 1 END) AS 多释义单词数
FROM tb_grade_unit gu
LEFT JOIN tb_word w ON gu.id = w.grade_unit_id
WHERE gu.grade BETWEEN 3 AND 6
GROUP BY gu.grade, gu.semester
ORDER BY gu.grade, gu.semester;
GO
