# 人教版小学英语题库数据导入指南

## 概述

本指南介绍如何从官方渠道获取人教版 (PEP) 小学英语教材资源，并导入到系统中生成完整的题库数据。

---

## 官方数据获取渠道

### 1. 人民教育出版社官网
- **网址**: https://www.pep.com.cn/
- **资源**: 电子课本、教师用书、配套练习
- **获取方式**: 
  1. 访问人教社官网
  2. 进入"产品中心" → "数字教材"
  3. 选择小学英语 (PEP) 对应年级
  4. 下载电子课本或在线阅读

### 2. 人教社数字教材中心
- **网址**: https://jczx.pep.com.cn/
- **资源**: 正版数字教材、教学资源包
- **获取方式**: 注册账号后可下载官方数字资源

### 3. 国家中小学智慧教育平台
- **网址**: https://www.zxx.edu.cn/
- **资源**: 课程教材、教学资源
- **获取方式**: 免费注册后可访问教材资源

### 4. 地方教育局资源平台
部分省市教育局也有官方教材资源：
- 北京市数字学校：https://www.bdschool.cn/
- 上海微校：https://www.shweixiao.com/

---

## 数据整理方法

### 方法一：手动录入（推荐用于校验）

1. 打开电子课本 PDF 或网页版
2. 找到每个单元的单词表（通常在单元末尾）
3. 将数据填入 `textbook-words.json` 文件
4. 按以下格式组织：

```json
{
  "grade": 3,
  "semester": "上",
  "unitNo": 1,
  "unitName": "Unit 1 Hello!",
  "words": [
    {
      "word": "ruler",
      "phonetic_uk": "/ˈruːlə/",
      "phonetic_us": "/ˈruːlər/",
      "meaning_cn": "尺子",
      "part_of_speech": "n.",
      "example_en": "I have a ruler.",
      "example_cn": "我有一把尺子。"
    }
  ]
}
```

### 方法二：Excel 整理后转换

1. 创建 Excel 表格，包含以下列：
   - grade (年级：3/4/5/6)
   - semester (学期：上/下)
   - unit_no (单元号：1-6)
   - unit_name (单元名称)
   - word (单词)
   - phonetic_uk (英式音标)
   - phonetic_us (美式音标)
   - meaning_cn (中文意思)
   - part_of_speech (词性)
   - example_en (英文例句)
   - example_cn (中文例句)

2. 从电子课本复制单词表数据到 Excel
3. 使用 Python 脚本转换为 JSON：

```python
import pandas as pd
import json

df = pd.read_excel('单词表整理.xlsx')
units = df.groupby(['grade', 'semester', 'unit_no', 'unit_name'])

data = {'gradeUnits': []}
for name, group in units:
    unit_data = {
        'grade': name[0],
        'semester': name[1],
        'unitNo': name[2],
        'unitName': name[3],
        'words': group.drop(columns=['grade', 'semester', 'unit_no', 'unit_name']).to_dict('records')
    }
    data['gradeUnits'].append(unit_data)

with open('textbook-words.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 方法三：使用 OCR 识别（适用于纸质教材）

1. 使用手机扫描 App（如扫描全能王）扫描教材单词表
2. 使用 OCR 识别文字
3. 校对识别结果
4. 整理为 Excel 或 JSON 格式

---

## 数据导入步骤

### 前置条件
- SQL Server 数据库已运行
- 数据库 `EnglishLearning` 已创建
- 年级单元数据 (tb_grade_unit) 已存在

### 方式一：使用 Python 脚本导入

```bash
# 安装依赖
pip install pyodbc pandas openpyxl

# 运行导入脚本
python import_words.py textbook-words.json
```

### 方式二：使用 .NET API 导入

1. 确保 API 服务正在运行：
```bash
dotnet run --project EnglishLearning.API
```

2. 调用导入接口：
```bash
curl -X POST http://localhost:5000/api/seed/import-textbook-data
```

3. 查看导入统计：
```bash
curl http://localhost:5000/api/seed/stats
```

---

## 完整单词表参考（3-6 年级）

### 三年级上册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | Hello! | 7 |
| Unit 2 | Look at Me | 10 |
| Unit 3 | Let's Paint | 8 |
| Unit 4 | We Love Animals | 9 |
| Unit 5 | Let's Eat | 7 |
| Unit 6 | Happy Birthday | 11 |

### 三年级下册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | Welcome Back to School | 8 |
| Unit 2 | My Family | 10 |
| Unit 3 | At the Zoo | 8 |
| Unit 4 | Where Is My Car | 9 |
| Unit 5 | Do You Like Pears | 10 |
| Unit 6 | How Many | 11 |

### 四年级上册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | My Classroom | 8 |
| Unit 2 | My Schoolbag | 8 |
| Unit 3 | My Friends | 9 |
| Unit 4 | My Home | 8 |
| Unit 5 | Dinner's Ready | 9 |
| Unit 6 | Meet My Family | 10 |

### 四年级下册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | My School | 9 |
| Unit 2 | What Time Is It | 10 |
| Unit 3 | Weather | 9 |
| Unit 4 | At the Farm | 10 |
| Unit 5 | My Clothes | 9 |
| Unit 6 | Shopping | 10 |

### 五年级上册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | What's He Like | 9 |
| Unit 2 | My Week | 10 |
| Unit 3 | What Would You Like | 9 |
| Unit 4 | What Can You Do | 10 |
| Unit 5 | There Is a Big Bed | 9 |
| Unit 6 | In a Nature Park | 10 |

### 五年级下册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | My Day | 9 |
| Unit 2 | My Favourite Season | 10 |
| Unit 3 | My School Calendar | 9 |
| Unit 4 | When Is Easter | 10 |
| Unit 5 | Whose Dog Is It | 9 |
| Unit 6 | Work Quietly | 10 |

### 六年级上册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | How Can I Get There | 9 |
| Unit 2 | Ways to Go to School | 10 |
| Unit 3 | My Weekend Plan | 9 |
| Unit 4 | I Have a Pen Pal | 10 |
| Unit 5 | What Does He Do | 9 |
| Unit 6 | How Do You Feel | 10 |

### 六年级下册
| 单元 | 主题 | 单词数 |
|------|------|--------|
| Unit 1 | How Tall Are You | 10 |
| Unit 2 | Last Weekend | 10 |
| Unit 3 | Where Did You Go | 10 |
| Unit 4 | Then and Now | 10 |
| Unit 5 | Let's Play | 9 |
| Unit 6 | A Farewell Party | 10 |

---

## 语法知识点和练习题目

除单词外，还可以整理：

### 语法知识点
- 每个单元的核心语法
- 句型结构
- 用法说明
- 示例句子

### 练习题目
- 选择题（单词拼写、词义理解、语法应用）
- 填空题（句子补全、单词填空）
- 连线题（单词与图片/释义匹配）
- 听力题（如有音频资源）

---

## 注意事项

1. **版权说明**: 教材内容版权归人民教育出版社所有，请仅用于个人学习或教学用途
2. **数据校验**: 导入前请仔细校对单词、音标、释义的准确性
3. **备份数据**: 导入前备份数据库，防止数据丢失
4. **分批导入**: 建议按年级或学期分批导入，便于校验

---

## 技术支持

如有问题，请检查：
1. 数据库连接是否正常
2. JSON 文件格式是否正确
3. 年级单元数据是否已存在于数据库中
4. 查看日志输出定位错误
