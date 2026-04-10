-- 导入缺失的年级单元数据 (4-6 年级)
-- 执行人教社小学英语 (PEP) 完整单元结构

USE EnglishLearning;
GO

-- 四年级下册 (如果不存在则插入)
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 1, 'Unit 1 My School', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=1);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 2, 'Unit 2 What Time Is It', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=2);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 3, 'Unit 3 Weather', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=3);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 4, 'Unit 4 At the Farm', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=4);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 5, 'Unit 5 My Clothes', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=5);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 4, '下', 6, 'Unit 6 Shopping', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=4 AND semester='下' AND unit_no=6);

-- 五年级上册
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 1, 'Unit 1 What''s He Like', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=1);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 2, 'Unit 2 My Week', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=2);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 3, 'Unit 3 What Would You Like', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=3);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 4, 'Unit 4 What Can You Do', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=4);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 5, 'Unit 5 There Is a Big Bed', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=5);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '上', 6, 'Unit 6 In a Nature Park', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='上' AND unit_no=6);

-- 五年级下册
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 1, 'Unit 1 My Day', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=1);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 2, 'Unit 2 My Favourite Season', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=2);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 3, 'Unit 3 My School Calendar', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=3);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 4, 'Unit 4 When Is Easter', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=4);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 5, 'Unit 5 Whose Dog Is It', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=5);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 5, '下', 6, 'Unit 6 Work Quietly', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=5 AND semester='下' AND unit_no=6);

-- 六年级上册
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 1, 'Unit 1 How Can I Get There', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=1);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 2, 'Unit 2 Ways to Go to School', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=2);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 3, 'Unit 3 My Weekend Plan', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=3);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 4, 'Unit 4 I Have a Pen Pal', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=4);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 5, 'Unit 5 What Does He Do', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=5);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '上', 6, 'Unit 6 How Do You Feel', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='上' AND unit_no=6);

-- 六年级下册
INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 1, 'Unit 1 How Tall Are You', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=1);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 2, 'Unit 2 Last Weekend', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=2);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 3, 'Unit 3 Where Did You Go', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=3);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 4, 'Unit 4 Then and Now', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=4);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 5, 'Unit 5 Let''s Play', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=5);

INSERT INTO tb_grade_unit (id, grade, semester, unit_no, unit_name, sort_order)
SELECT NEWID(), 6, '下', 6, 'Unit 6 A Farewell Party', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_grade_unit WHERE grade=6 AND semester='下' AND unit_no=6);

GO

PRINT '年级单元导入完成！';
GO
