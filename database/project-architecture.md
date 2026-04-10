# 英语学习工具 - 项目架构文档

## 一、技术选型总览

```
┌─────────────────────────────────────────────────────────┐
│                    用户层                               │
│     微信小程序  ←→  Web 管理后台 (家长/管理)              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                    API 网关层                            │
│              ASP.NET Core Web API (.NET 8)              │
│         JWT 认证 | 限流 | 日志 | 全局异常处理            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层                             │
│    UserService | QuestionService | ChallengeService     │
│    LearningService | BadgeService | PointService        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   数据访问层                             │
│        Entity Framework Core 8 + SQL Server             │
│        Repository Pattern + Unit of Work                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                     数据库                               │
│              SQL Server 2016+ (EnglishLearning)         │
└─────────────────────────────────────────────────────────┘
```

---

## 二、项目目录结构

### 2.1 后端项目结构

```
EnglishLearning.API/
├── EnglishLearning.API/                  # API 主项目
│   ├── Controllers/                      # API 控制器
│   │   ├── AuthController.cs             # 认证注册
│   │   ├── UserController.cs             # 用户信息
│   │   ├── WordController.cs             # 单词学习
│   │   ├── GrammarController.cs          # 语法学习
│   │   ├── QuestionController.cs         # 题库
│   │   ├── ChallengeController.cs        # 每日挑战
│   │   ├── BadgeController.cs            # 徽章系统
│   │   └── ReportController.cs           # 学习报告
│   ├── Middleware/                       # 中间件
│   │   ├── ExceptionHandlerMiddleware.cs # 全局异常
│   │   └── RequestLoggingMiddleware.cs   # 请求日志
│   ├── Filters/                          # 过滤器
│   │   └── ValidateModelAttribute.cs     # 模型验证
│   ├── Extensions/                       # 扩展方法
│   │   ├── ServiceCollectionExtensions.cs
│   │   └── ApplicationBuilderExtensions.cs
│   ├── appsettings.json                  # 配置文件
│   ├── appsettings.Development.json      # 开发环境配置
│   └── Program.cs                        # 入口文件
│
├── EnglishLearning.Domain/               # 领域层
│   ├── Entities/                         # 实体类
│   │   ├── User.cs
│   │   ├── UserProfile.cs
│   │   ├── GradeUnit.cs
│   │   ├── Word.cs
│   │   ├── Grammar.cs
│   │   ├── Question.cs
│   │   ├── QuestionOption.cs
│   │   ├── LearningProgress.cs
│   │   ├── WrongQuestion.cs
│   │   ├── DailyChallenge.cs
│   │   ├── DailyChallengeDetail.cs
│   │   ├── UserLevel.cs
│   │   ├── Badge.cs
│   │   ├── UserBadge.cs
│   │   ├── UserPoints.cs
│   │   └── Checkin.cs
│   ├── Enums/                            # 枚举
│   │   ├── QuestionType.cs
│   │   ├── LearningStatus.cs
│   │   ├── ReviewStatus.cs
│   │   └── BadgeType.cs
│   ├── Interfaces/                       # 仓储接口
│   │   ├── IRepository.cs
│   │   ├── IUserRepository.cs
│   │   ├── IQuestionRepository.cs
│   │   └── ...
│   └── DTOs/                             # 数据传输对象
│       ├── Request/                      # 请求 DTO
│       │   ├── LoginRequest.cs
│       │   ├── CreateChallengeRequest.cs
│       │   └── SubmitAnswerRequest.cs
│       └── Response/                     # 响应 DTO
│           ├── ApiResponse.cs
│           ├── UserInfoResponse.cs
│           ├── WordDetailResponse.cs
│           └── ChallengeResultResponse.cs
│
├── EnglishLearning.Infrastructure/       # 基础设施层
│   ├── Data/                             # 数据访问
│   │   ├── AppDbContext.cs               # EF Core 上下文
│   │   ├── Repository.cs                 # 通用仓储
│   │   └── UnitOfWork.cs                 # 工作单元
│   ├── Configurations/                   # 实体配置
│   │   ├── UserConfiguration.cs
│   │   ├── QuestionConfiguration.cs
│   │   └── ...
│   ├── Services/                         # 业务服务
│   │   ├── AuthService.cs
│   │   ├── UserService.cs
│   │   ├── QuestionService.cs
│   │   ├── ChallengeService.cs
│   │   ├── BadgeService.cs
│   │   └── PointService.cs
│   └── Helpers/                          # 工具类
│       ├── JwtHelper.cs                  # JWT 生成
│       ├── PasswordHelper.cs             # 密码加密
│       └── EbbinghausHelper.cs           # 艾宾浩斯记忆计算
│
├── EnglishLearning.Shared/               # 共享层
│   ├── Constants/                        # 常量定义
│   │   ├── PointRules.cs
│   │   └── LevelConfig.cs
│   ├── Exceptions/                       # 自定义异常
│   │   └── BusinessException.cs
│   └── Utils/                            # 通用工具
│       ├── Result.cs                     # 统一返回结果
│       └── PageList.cs                   # 分页结果
│
└── EnglishLearning.sln                   # 解决方案文件
```

### 2.2 小程序项目结构 (Uni-app)

```
english-learning-miniprogram/
├── src/
│   ├── pages/                            # 页面
│   │   ├── index/                        # 首页
│   │   │   └── index.vue
│   │   ├── word-challenge/               # 单词闯关
│   │   │   └── index.vue
│   │   ├── grammar-learn/                # 语法学习
│   │   │   └── index.vue
│   │   ├── daily-challenge/              # 每日挑战
│   │   │   ├── index.vue                 # 挑战首页
│   │   │   ├──答题页.vue
│   │   │   └── result.vue                # 结果页
│   │   ├── wrong-book/                   # 错题本
│   │   │   └── index.vue
│   │   ├── profile/                      # 个人中心
│   │   │   ├── index.vue
│   │   │   ├── badge.vue                 # 徽章墙
│   │   │   └── report.vue                # 学习报告
│   │   └── login/                        # 登录
│   │       └── index.vue
│   ├── components/                       # 组件
│   │   ├── WordCard.vue                  # 单词卡片
│   │   ├── QuestionItem.vue              # 题目组件
│   │   ├── ProgressBar.vue               # 进度条
│   │   ├── StarRating.vue                # 星级评价
│   │   ├── BadgeIcon.vue                 # 徽章图标
│   │   └── LoadingSpinner.vue            # 加载动画
│   ├── stores/                           # Pinia 状态管理
│   │   ├── user.js                       # 用户状态
│   │   ├── challenge.js                  # 挑战状态
│   │   └── app.js                        # 全局状态
│   ├── api/                              # API 封装
│   │   ├── request.js                    # Axios 封装
│   │   ├── auth.js                       # 认证 API
│   │   ├── word.js                       # 单词 API
│   │   ├── grammar.js                    # 语法 API
│   │   ├── challenge.js                  # 挑战 API
│   │   └── user.js                       # 用户 API
│   ├── utils/                            # 工具函数
│   │   ├── storage.js                    # 本地存储
│   │   ├── timer.js                      # 计时器
│   │   └── format.js                     # 格式化工具
│   ├── router/                           # 路由配置
│   │   └── index.js
│   ├── styles/                           # 全局样式
│   │   └── variables.scss
│   ├── App.vue
│   └── main.js
├── static/                               # 静态资源
│   ├── images/
│   └── audio/
├── pages.json                            # 页面配置
├── manifest.json                         # 应用配置
├── uni.scss
├── package.json
└── vite.config.js
```

### 2.3 Web 管理后台项目结构

```
english-learning-admin/
├── src/
│   ├── views/                            # 页面视图
│   │   ├── dashboard/                    # 数据看板
│   │   │   └── index.vue
│   │   ├── user/                         # 用户管理
│   │   │   ├── list.vue                  # 用户列表
│   │   │   └── detail.vue                # 用户详情
│   │   ├── content/                      # 内容管理
│   │   │   ├── word/                     # 单词管理
│   │   │   │   ├── list.vue
│   │   │   │   └── edit.vue
│   │   │   ├── grammar/                  # 语法管理
│   │   │   │   ├── list.vue
│   │   │   │   └── edit.vue
│   │   │   └── question/                 # 题库管理
│   │   │       ├── list.vue
│   │   │       └── edit.vue
│   │   ├── learning/                     # 学习数据
│   │   │   ├── progress.vue              # 进度查询
│   │   │   └── wrong-analysis.vue        # 错题分析
│   │   ├── system/                       # 系统设置
│   │   │   ├── config.vue                # 配置管理
│   │   │   └── badge.vue                 # 徽章管理
│   │   └── login/                        # 登录
│   │       └── index.vue
│   ├── components/                       # 公共组件
│   │   ├── Layout/                       # 布局组件
│   │   ├── Table/                        # 表格组件
│   │   ├── Form/                         # 表单组件
│   │   └── Chart/                        # 图表组件
│   ├── stores/                           # Pinia
│   │   ├── user.js
│   │   └── app.js
│   ├── api/                              # API 封装
│   │   ├── request.js
│   │   ├── user.js
│   │   ├── content.js
│   │   └── learning.js
│   ├── router/                           # 路由
│   │   └── index.js
│   ├── utils/                            # 工具
│   │   ├── auth.js                       # 认证
│   │   └── validate.js                   # 验证
│   ├── styles/
│   ├── App.vue
│   └── main.js
├── public/
├── package.json
├── vite.config.js
└── README.md
```

---

## 三、开发环境要求

### 后端

| 工具 | 版本 | 用途 |
|-----|------|------|
| .NET SDK | 8.0+ | 开发框架 |
| Visual Studio 2022 / VS Code | - | IDE |
| SQL Server Management Studio | - | 数据库管理 |
| Postman / Swagger UI | - | API 测试 |

### 前端 (小程序)

| 工具 | 版本 | 用途 |
|-----|------|------|
| Node.js | 18+ | 运行环境 |
| HBuilderX | 最新版 | Uni-app 开发工具 |
| 微信开发者工具 | 最新版 | 小程序调试 |
| pnpm / npm | 9+/10+ | 包管理 |

### 前端 (Web 管理台)

| 工具 | 版本 | 用途 |
|-----|------|------|
| Node.js | 18+ | 运行环境 |
| VS Code | - | IDE |
| pnpm / npm | 9+/10+ | 包管理 |

---

## 四、关键技术实现

### 4.1 JWT 认证流程

```
1. 用户登录 → 后端验证 → 返回 JWT Token
2. 小程序存储 Token (localStorage)
3. 后续请求携带 Token (Authorization: Bearer xxx)
4. 后端中间件验证 Token → 解析用户信息 → 放行请求
```

### 4.2 艾宾浩斯复习算法

```csharp
// 复习间隔配置 (分钟)
public static int[] ReviewIntervals = { 0, 5, 1440, 4320, 10080, 21600, 43200 };
//                        即时  5 分钟  1 天   3 天    7 天   15 天   30 天

public DateTime CalculateNextReviewTime(int reviewCount)
{
    if (reviewCount >= ReviewIntervals.Length)
        return DateTime.MaxValue; // 已掌握

    int minutesToAdd = ReviewIntervals[reviewCount];
    return DateTime.Now.AddMinutes(minutesToAdd);
}
```

### 4.3 积分系统

```csharp
public class PointRules
{
    public static readonly int SignIn = 5;
    public static readonly int DailyChallengeComplete = 50;
    public static readonly int WordLevelComplete = 10;
    public static readonly int GrammarLevelComplete = 20;
    public static readonly int StreakBonus7Days = 10;
    public static readonly int StreakBonus30Days = 50;
    public static readonly int PerfectScoreBonus = 20;
}
```

### 4.4 徽章解锁机制

```csharp
// 监听用户行为 → 检查徽章条件 → 解锁徽章
public async Task UnlockBadgesAsync(Guid userId, string eventType, object eventData)
{
    var allBadges = await _badgeRepository.GetAllActiveAsync();

    foreach (var badge in allBadges)
    {
        var requirement = JsonSerializer.Deserialize<BadgeRequirement>(badge.RequirementJson);

        if (await CheckRequirementAsync(userId, requirement, eventData))
        {
            await AwardBadgeAsync(userId, badge.Id);
        }
    }
}
```

---

## 五、API 接口规范

### 5.1 统一响应格式

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": { ... },
  "timestamp": "2026-03-30T10:30:00Z"
}
```

### 5.2 错误码定义

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证/Token 失效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 1001 | 业务异常 |

---

## 六、部署架构

```
                    ┌─────────────┐
                    │   小程序    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  微信 API   │
                    └──────┬──────┘
                           │
┌─────────────┐     ┌──────▼──────┐     ┌─────────────┐
│  Web 管理台  │────→│  .NET API   │────→│ SQL Server  │
└─────────────┘     │  (IIS/Docker)│     │             │
                    └─────────────┘     └─────────────┘
```

### 部署方式 (推荐)

| 组件 | 部署方式 |
|-----|---------|
| .NET API | IIS 或 Docker |
| SQL Server | 本地/云服务器 |
| 小程序 | 微信平台 |
| Web 管理台 | IIS / Nginx |

---

## 七、开发计划

| 阶段 | 内容 | 周期 |
|-----|------|------|
| 第 1 周 | 后端基础框架 + 数据库对接 | 5-7 天 |
| 第 2 周 | 核心 API 开发 (用户/单词/题库) | 5-7 天 |
| 第 3 周 | 小程序前端开发 | 5-7 天 |
| 第 4 周 | Web 管理后台 + 联调测试 | 5-7 天 |
