# 数据库迁移记录

## Migration 001: 增加多释义支持

**日期**: 2026-04-02
**影响范围**: `tb_word` 表

### 变更内容

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meaning_trans` | NVARCHAR(MAX) | 新增字段，JSON 数组格式存储多个中文释义 |

### 向后兼容性

- `meaning_cn` 字段保留，存储主要释义（第一个）
- 新增视图 `vw_word_with_meanings` 提供便捷的查询接口

### 执行步骤

1. 运行迁移脚本：
```sql
-- 在 SQL Server Management Studio 中执行
: .\migrations\001_add_meaning_trans.sql
```

2. 验证迁移结果：
```sql
-- 查看新增字段
SELECT TOP 5 word, meaning_cn, meaning_trans
FROM tb_word;

-- 测试视图
SELECT TOP 5 * FROM vw_word_with_meanings;
```

### 数据导入

**从 qwerty-learner 格式导入**:

1. 手动导入（少量数据）:
```sql
-- 使用示例脚本
: .\imports\import_qwerty_learner_format.sql
```

2. 批量导入（完整词库）:
```bash
# 1. 克隆 qwerty-learner 词库
git clone https://github.com/RealKai42/qwerty-learner.git
cp -r qwerty-learner/public/dicts ./qwerty-learner-dicts

# 2. 运行 Python 导入脚本
python imports/import_qwerty_learner.py
```

### qwerty-learner 数据格式

```json
{
  "name": "ruler",
  "trans": ["尺子"],
  "usphone": "'rulɚ",
  "ukphone": "'ruːlə"
}
```

### 导入后数据格式

| word | phonetic_uk | phonetic_us | meaning_cn | meaning_trans | part_of_speech |
|------|-------------|-------------|------------|---------------|----------------|
| ruler | 'ruːlə | 'rulɚ | 尺子 | `["尺子"]` | n. |
| red | red | rɛd | 红色；红色的 | `["红色", "红色的"]` | n./adj. |

---

## 未来迁移计划

| Migration | 内容 | 优先级 |
|-----------|------|--------|
| 002 | 增加单词音频 URL 批量导入 | 中 |
| 003 | 增加单词图片 URL 批量导入 | 中 |
| 004 | 语法知识点 JSON 结构优化 | 低 |
| 005 | 题库数据批量导入工具 | 高 |
