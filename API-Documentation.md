# 英语学习工具 - API 接口文档

## API 规范

### 基础信息

- **Base URL**: `http://localhost:5000/api`
- **认证方式**: JWT Bearer Token
- **请求格式**: `application/json`
- **响应格式**: `application/json`

### 统一响应格式

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": { },
  "timestamp": "2026-03-30T10:30:00Z"
}
```

### 错误码说明

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/Token 失效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 1001 | 业务异常 |
| 1002 | 用户名或密码错误 |
| 1003 | 用户已存在 |
| 1004 | 挑战已完成 |
| 1005 | 题目不存在 |

---

## 接口列表

### 1. 认证模块 (Auth)

#### 1.1 用户登录

```
POST /api/auth/login
```

**请求参数：**

```json
{
  "username": "xiaoming",
  "password": "123456"
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "username": "xiaoming",
      "studentName": "小明",
      "gradeLevel": 6,
      "avatarUrl": null,
      "currentStreak": 5,
      "currentLevel": 3,
      "levelName": "进步之星",
      "currentExp": 450,
      "totalPoints": 65,
      "totalCoins": 25
    },
    "expiresIn": 7200
  }
}
```

---

#### 1.2 用户注册

```
POST /api/auth/register
```

**请求参数：**

```json
{
  "username": "xiaohong",
  "password": "123456",
  "studentName": "小红",
  "gradeLevel": 3,
  "phone": "13800138002"
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "username": "xiaohong"
  }
}
```

---

#### 1.3 获取当前用户信息

```
GET /api/auth/me
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "username": "xiaoming",
    "studentName": "小明",
    "gradeLevel": 6,
    "avatarUrl": null,
    "currentStreak": 5,
    "currentLevel": 3,
    "levelName": "进步之星",
    "currentExp": 450,
    "totalPoints": 65,
    "totalCoins": 25
  }
}
```

---

### 2. 单词学习模块 (Word)

#### 2.1 获取单词列表

```
GET /api/words?gradeUnitId={unitId}&limit=10
Authorization: Bearer {token}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| gradeUnitId | guid | 是 | 年级单元 ID |
| limit | int | 否 | 每次获取数量，默认 10 |

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": "w1...",
        "wordText": "science",
        "phoneticUk": "/ˈsaɪəns/",
        "phoneticUs": "/ˈsaɪəns/",
        "audioUrl": "/audio/science.mp3",
        "meaningCn": "科学",
        "partOfSpeech": "n.",
        "exampleEn": "I like science class.",
        "exampleCn": "我喜欢科学课。",
        "imageUrl": null,
        "status": "not_started",
        "score": null
      }
    ],
    "total": 12
  }
}
```

---

#### 2.2 获取单词详情

```
GET /api/words/{id}
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "id": "w1...",
    "wordText": "science",
    "phoneticUk": "/ˈsaɪəns/",
    "phoneticUs": "/ˈsaɪəns/",
    "audioUrl": "/audio/science.mp3",
    "meaningCn": "科学",
    "partOfSpeech": "n.",
    "exampleEn": "I like science class.",
    "exampleCn": "我喜欢科学课。",
    "imageUrl": null,
    "status": "completed",
    "score": 100
  }
}
```

---

#### 2.3 更新单词学习进度

```
POST /api/words/{id}/progress
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "score": 100,
  "status": "completed"
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "message": "进度更新成功",
  "data": {
    "pointsEarned": 10,
    "expEarned": 5,
    "levelUp": false
  }
}
```

---

### 3. 语法学习模块 (Grammar)

#### 3.1 获取语法列表

```
GET /api/grammar?gradeUnitId={unitId}
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": "g1...",
        "title": "问路句型 - How can I get to...",
        "contentType": "article",
        "durationSeconds": null,
        "sortOrder": 1,
        "passingScore": 60,
        "status": "learning",
        "score": 60
      }
    ]
  }
}
```

---

#### 3.2 获取语法详情

```
GET /api/grammar/{id}
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "id": "g1...",
    "title": "问路句型 - How can I get to...",
    "contentType": "article",
    "contentJson": "{\"sections\":[...]}",
    "quizJson": "{\"questions\":[...]}",
    "passingScore": 60,
    "status": "learning",
    "score": 60
  }
}
```

---

#### 3.3 提交语法测验

```
POST /api/grammar/{id}/quiz
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "answers": [
    {
      "questionId": "q1...",
      "userAnswer": "A"
    }
  ]
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "score": 80,
    "isPassed": true,
    "correctCount": 4,
    "totalCount": 5,
    "pointsEarned": 20,
    "expEarned": 10
  }
}
```

---

### 4. 题目模块 (Question)

#### 4.1 获取题目详情

```
GET /api/questions/{id}
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "id": "q1...",
    "questionType": "single_choice",
    "difficulty": 1,
    "questionStem": "单词 \"museum\" 的中文意思是？",
    "stemAudioUrl": null,
    "options": [
      {
        "id": "o1...",
        "optionKey": "A",
        "optionContent": "博物馆",
        "imageUrl": null,
        "audioUrl": null
      },
      {
        "id": "o2...",
        "optionKey": "B",
        "optionContent": "美术馆",
        "imageUrl": null,
        "audioUrl": null
      }
    ]
  }
}
```

---

#### 4.2 提交答案

```
POST /api/questions/{id}/answer
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "userAnswer": "A",
  "isUncertain": false,
  "timeUsedSeconds": 15
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "isCorrect": true,
    "correctAnswer": "A",
    "analysis": "museum 意为\"博物馆\"，是六年级上册 Unit 1 的重点词汇。",
    "pointsEarned": 5,
    "expEarned": 2,
    "levelUp": false
  }
}
```

---

### 5. 每日挑战模块 (Challenge)

#### 5.1 获取今日挑战状态

```
GET /api/challenge/today
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "date": "2026-03-30",
    "status": "pending",
    "isCompleted": false,
    "totalQuestions": 10,
    "correctCount": 0,
    "score": 0,
    "pointsEarned": 0,
    "coinsEarned": 0
  }
}
```

---

#### 5.2 开始挑战

```
POST /api/challenge/start
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "challengeId": "c1...",
    "questions": [
      {
        "id": "q1...",
        "questionType": "single_choice",
        "questionStem": "单词 \"museum\" 的中文意思是？",
        "options": [...]
      }
    ]
  }
}
```

---

#### 5.3 提交挑战结果

```
POST /api/challenge/{id}/submit
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "answers": [
    {
      "questionId": "q1...",
      "userAnswer": "A",
      "isCorrect": true,
      "timeUsedSeconds": 15
    }
  ],
  "timeUsedSeconds": 270
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "id": "c1...",
    "totalQuestions": 10,
    "correctCount": 8,
    "score": 80,
    "timeUsedSeconds": 270,
    "pointsEarned": 50,
    "coinsEarned": 20,
    "questionResults": [
      {
        "questionId": "q1...",
        "questionStem": "单词 \"museum\" 的中文意思是？",
        "userAnswer": "A",
        "correctAnswer": "A",
        "isCorrect": true,
        "analysis": "museum 意为\"博物馆\"..."
      }
    ]
  }
}
```

---

### 6. 错题本模块 (Wrong Question)

#### 6.1 获取错题列表

```
GET /api/wrong-questions?page=1&pageSize=20&status=reviewing
Authorization: Bearer {token}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| page | int | 否 | 页码，默认 1 |
| pageSize | int | 否 | 每页数量，默认 20 |
| status | string | 否 | 复习状态 (new/reviewing/mastered) |

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": "wq1...",
        "questionId": "q1...",
        "questionStem": "选择正确形式：She ___ to school...",
        "questionType": "fill_blank",
        "knowledgePoint": "一般现在时",
        "userAnswer": "goed",
        "correctAnswer": "goes",
        "analysis": "主语是第三人称单数 She...",
        "reviewCount": 2,
        "nextReviewAt": "2026-04-02T10:00:00Z",
        "reviewStatus": "reviewing"
      }
    ],
    "total": 14,
    "page": 1,
    "pageSize": 20,
    "totalPages": 1
  }
}
```

---

#### 6.2 获取复习推送

```
GET /api/wrong-questions/review?limit=10
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": "wq1...",
        "questionId": "q1...",
        "questionStem": "选择正确形式：She ___ to school...",
        "questionType": "fill_blank",
        "reviewCount": 2
      }
    ],
    "totalCount": 8
  }
}
```

---

#### 6.3 更新错题状态

```
POST /api/wrong-questions/{id}/review
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "isCorrect": true,
  "userAnswer": "goes"
}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "message": "复习完成",
  "data": {
    "reviewCount": 3,
    "nextReviewAt": "2026-04-09T10:00:00Z",
    "reviewStatus": "mastered",
    "isMastered": true
  }
}
```

---

#### 6.4 标记已掌握

```
POST /api/wrong-questions/{id}/master
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "message": "已标记为掌握"
}
```

---

### 7. 用户模块 (User)

#### 7.1 获取学习统计

```
GET /api/user/stats
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "totalLearningDays": 30,
    "currentStreak": 5,
    "maxStreak": 12,
    "wordsLearned": 328,
    "grammarsCompleted": 18,
    "challengesCompleted": 25,
    "wrongQuestionCount": 14,
    "totalPoints": 2350,
    "totalCoins": 680,
    "currentLevel": 8,
    "levelName": "语法高手"
  }
}
```

---

#### 7.2 获取徽章列表

```
GET /api/user/badges
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": [
    {
      "id": "b1...",
      "badgeCode": "STREAK_7",
      "badgeName": "坚持 7 天",
      "badgeType": "streak",
      "description": "连续签到 7 天",
      "badgeIcon": "/icons/badge_streak_7.png",
      "earnedAt": "2026-03-25T10:00:00Z",
      "isEarned": true,
      "isNew": false
    },
    {
      "id": "b2...",
      "badgeCode": "WORD_100",
      "badgeName": "词汇达人",
      "badgeType": "word",
      "description": "掌握 100 个单词",
      "badgeIcon": "/icons/badge_word_100.png",
      "earnedAt": null,
      "isEarned": false,
      "isNew": false
    }
  ]
}
```

---

#### 7.3 获取积分记录

```
GET /api/user/points?page=1&pageSize=20
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [
      {
        "id": "p1...",
        "pointsType": "points",
        "changeType": "signin",
        "changeAmount": 5,
        "balanceAfter": 65,
        "description": "每日签到",
        "createdAt": "2026-03-30T08:00:00Z"
      },
      {
        "id": "p2...",
        "pointsType": "points",
        "changeType": "challenge",
        "changeAmount": 50,
        "balanceAfter": 60,
        "description": "完成每日挑战",
        "createdAt": "2026-03-29T19:00:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "pageSize": 20
  }
}
```

---

#### 7.4 每日签到

```
POST /api/user/checkin
Authorization: Bearer {token}
```

**响应：**

```json
{
  "success": true,
  "code": 200,
  "data": {
    "checkinDate": "2026-03-30",
    "pointsEarned": 5,
    "streakDays": 5,
    "bonusPoints": 0,
    "totalPoints": 5
  }
}
```

---

### 8. 管理后台模块 (Admin)

#### 8.1 获取用户列表

```
GET /api/admin/users?page=1&pageSize=20
Authorization: Bearer {token}
```

---

#### 8.2 获取用户详情

```
GET /api/admin/users/{id}
Authorization: Bearer {token}
```

---

#### 8.3 添加单词

```
POST /api/admin/words
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "gradeUnitId": "g1...",
  "wordText": "example",
  "phoneticUk": "/ɪɡˈzɑːmpl/",
  "phoneticUs": "/ɪɡˈzæmpl/",
  "meaningCn": "例子",
  "partOfSpeech": "n.",
  "exampleEn": "This is an example.",
  "exampleCn": "这是一个例子。",
  "sortOrder": 1
}
```

---

#### 8.4 添加题目

```
POST /api/admin/questions
Authorization: Bearer {token}
```

**请求参数：**

```json
{
  "gradeUnitId": "g1...",
  "questionType": "single_choice",
  "difficulty": 2,
  "questionStem": "选择正确的翻译",
  "correctAnswer": "B",
  "answerAnalysis": "解析内容...",
  "knowledgePoint": "词汇翻译",
  "tags": "word,translation",
  "options": [
    {
      "optionKey": "A",
      "optionContent": "例子 A",
      "sortOrder": 1
    },
    {
      "optionKey": "B",
      "optionContent": "例子 B",
      "sortOrder": 2
    }
  ]
}
```

---

## 附录

### A. JWT Token 生成规则

```csharp
var tokenHandler = new JwtSecurityTokenHandler();
var key = Encoding.UTF8.GetBytes(secretKey);

var tokenDescriptor = new SecurityTokenDescriptor
{
    Subject = new ClaimsIdentity(new[]
    {
        new Claim(ClaimTypes.NameIdentifier, userId.ToString()),
        new Claim(ClaimTypes.Name, username),
        new Claim("studentName", studentName),
        new Claim("gradeLevel", gradeLevel.ToString())
    }),
    Expires = DateTime.UtcNow.AddMinutes(120),
    Issuer = "EnglishLearning",
    Audience = "EnglishLearning",
    SigningCredentials = new SigningCredentials(
        new SymmetricSecurityKey(key),
        SecurityAlgorithms.HmacSha256Signature)
};

var token = tokenHandler.CreateToken(tokenDescriptor);
return tokenHandler.WriteToken(token);
```

---

### B. 艾宾浩斯复习间隔配置

| 复习次数 | 间隔时间 | 说明 |
|---------|---------|------|
| 0 | 即时 | 首次做错立即复习 |
| 1 | 5 分钟 | 5 分钟后 |
| 2 | 1 天 | 24 小时后 |
| 3 | 3 天 | 72 小时后 |
| 4 | 7 天 | 168 小时后 |
| 5 | 15 天 | 360 小时后 |
| 6 | 30 天 | 720 小时后 |

---

### C. 积分规则

| 行为 | 积分 | 金币 |
|-----|-----|-----|
| 每日签到 | +5 | +5 |
| 完成每日挑战 | +50 | +20 |
| 单词闯关完成 | +10~30 | - |
| 语法课程完成 | +20 | - |
| 连续打卡 7 天奖励 | +10 | - |
| 连续打卡 30 天奖励 | +50 | - |
| 满分奖励 (100 分) | +20 | - |
