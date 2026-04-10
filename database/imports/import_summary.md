# 词库导入总结报告

**日期**: 2026-04-02  
**数据来源**: qwerty-learner (https://github.com/RealKai42/qwerty-learner)

---

## 一、导入结果

### 1. 数据库变更

| 项目 | 数量 |
|------|------|
| 新增 `meaning_trans` 字段 | ✓ |
| 创建视图 `vw_word_with_meanings` | ✓ |
| 创建索引 `IX_tb_word_meaning_lookup` | ✓ |

### 2. 数据导入统计

| 年级 | 学期 | 单元数 | 单词数 |
|------|------|--------|--------|
| 3 年级 | 上册 | 6 | 85 |
| 3 年级 | 下册 | 6 | 83 |
| 4 年级 | 上册 | 6 | 95 |
| 4 年级 | 下册 | 6 | 123 |
| 5 年级 | 上册 | 6 | 138 |
| 5 年级 | 下册 | 6 | 170 |
| 6 年级 | 上册 | 6 | 174 |
| 6 年级 | 下册 | 6 | 166 |
| **合计** | | **48** | **1,034** |

---

## 二、数据格式对比

### qwerty-learner 格式

```json
{
  "name": "red",
  "trans": ["红色", "红色的"],
  "usphone": "'rɛd",
  "ukphone": "red"
}
```

### 导入后数据库格式

| 字段 | 值 |
|------|-----|
| word | red |
| phonetic_uk | red |
| phonetic_us | 'rɛd |
| meaning_cn | 红色；红色的 |
| meaning_trans | `["红色","红色的"]` |
| part_of_speech | NULL (qwerty-learner 无此字段) |

---

## 三、已完成的工作

### 1. 数据库迁移

- ✅ 运行 `migrations/001_add_meaning_trans.sql`
- ✅ 添加 `meaning_trans` 字段 (NVARCHAR(MAX))
- ✅ 创建视图 `vw_word_with_meanings`
- ✅ 创建索引 `IX_tb_word_meaning_lookup`

### 2. 导入工具开发

- ✅ 开发 Python 导入脚本 `imports/import_qwerty_learner.py`
- ✅ 支持 Windows 集成认证
- ✅ 按单元自动分配单词（每册 6 单元）
- ✅ 使用 MERGE 语句实现增量导入

### 3. 数据导入

- ✅ 导入人教版小学 3-6 年级（上下册）
- ✅ 共 48 个单元，1,034 个单词
- ✅ 多释义 JSON 格式存储

---

## 四、数据验证

### 查询示例

```sql
-- 查看多释义数据
SELECT TOP 10 
    word, 
    meaning_cn, 
    meaning_trans,
    JSON_VALUE(meaning_trans, '$[0]') AS main_meaning,
    JSON_VALUE(meaning_trans, '$[1]') AS meaning_2
FROM tb_word
WHERE JSON_VALUE(meaning_trans, '$[1]') IS NOT NULL;

-- 按年级统计
SELECT grade, semester, COUNT(*) as word_count
FROM tb_word w
JOIN tb_grade_unit gu ON w.grade_unit_id = gu.id
WHERE grade BETWEEN 3 AND 6
GROUP BY grade, semester
ORDER BY grade, semester;
```

---

## 五、后续建议

### 1. 数据增强（优先级：高）

- [ ] 补充词性信息（qwerty-learner 无此字段）
- [ ] 补充例句数据
- [ ] 添加单词音频 URL

### 2. 语法和题库（优先级：中）

- [ ] 参考 ChinaTextbook 补充语法知识点
- [ ] 按单元补充练习题

### 3. 其他教材版本（优先级：低）

- [ ] PEP_SL 系列（一年级起点）
- [ ] 初中、高中英语

---

## 六、文件清单

| 文件 | 用途 |
|------|------|
| `migrations/001_add_meaning_trans.sql` | 数据库迁移脚本 |
| `imports/import_qwerty_learner.py` | Python 导入工具 |
| `imports/import_qwerty_learner_format.sql` | SQL 示例脚本 |
| `migrations/README.md` | 迁移文档 |

---

## 七、技术要点

### 1. 多释义存储

使用 SQL Server 的 JSON 功能：
- `JSON_QUERY()` 创建 JSON 数组
- `JSON_VALUE()` 提取 JSON 值

### 2. 增量导入

使用 `MERGE` 语句：
```sql
MERGE tb_word AS target
USING (...) AS source
ON target.word = source.word AND target.grade_unit_id = ?
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

### 3. 单元自动分配

 qwerty-learner 词库不按单元分，脚本按以下规则分配：
- 每册教材 6 个单元
- 单词平均分配到各单元
- 单元名称参考人教版教材目录

---

**导入完成！** 🎉
