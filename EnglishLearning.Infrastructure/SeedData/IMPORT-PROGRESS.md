# 人教版小学英语 (PEP) 题库数据导入进度

## 已完成

### 三年级 (上册 + 下册) - ✅ 完成
- Unit 1-6: 111 个单词
- 状态：已导入

### 四年级 (上册 + 下册) - ✅ 完成
- Unit 1-6: 109 个单词
- 状态：已导入

## 待导入

### 五年级 (上册 + 下册) - ⏳ 准备中
- 上册 Unit 1-6: 约 60 个单词
- 下册 Unit 1-6: 约 60 个单词

### 六年级 (上册 + 下册) - ⏳ 准备中
- 上册 Unit 1-6: 约 60 个单词
- 下册 Unit 1-6: 约 60 个单词

## 当前数据库状态

```json
{
  "gradeUnits": 48,
  "words": 448,
  "grammars": 2,
  "questions": 5
}
```

## 数据来源

由于网络限制无法直接从 GitHub (TapXWorld/ChinaTextbook) 和人教社官网获取数据，当前数据是根据人教版 PEP 教材大纲整理的标准单词表。

## 导入工具

- `generate-full-words.py` - 三年级单词导入
- `import-grade4-words.py` - 四年级单词导入
- `add-missing-units.py` - 添加缺失的年级单元
- `import_words.py` - 通用 CSV/Excel/JSON 导入工具

## 下一步

1. 创建五年级单词导入脚本
2. 创建六年级单词导入脚本
3. 添加语法知识点数据
4. 添加练习题目数据
