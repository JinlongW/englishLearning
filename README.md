# EnglishLearning

英语学习工具 - 基于 .NET 8 + Vue3 的单词学习、语法学习、每日挑战系统

## 项目概述

完整的英语学习工具，包含后端 API、前端小程序和数据库脚本。支持单词学习、语法学习、每日挑战、错题本等功能。

## 项目结构

```
englishLearning/
├── backend/                # 后端 .NET 8 Web API
│   ├── EnglishLearning.API/
│   ├── EnglishLearning.Domain/
│   ├── EnglishLearning.Infrastructure/
│   └── EnglishLearning.Shared/
├── frontend/               # 前端 Vue3 + TypeScript 小程序
│   ├── src/
│   ├── e2e/
│   └── package.json
└── database/               # 数据库脚本和初始化数据
    ├── database.sql        # 数据库结构
    ├── init-data.sql       # 初始化数据
    └── migrations/         # 数据库迁移
```

## 技术栈

### 后端
- **框架**: ASP.NET Core 8.0 Web API
- **数据库**: SQL Server 2016+
- **ORM**: Entity Framework Core 8.0
- **认证**: JWT Bearer Token
- **验证**: FluentValidation

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 组件**: Vant 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **测试**: Playwright

### 数据库
- **数据库**: SQL Server 2016+
- **迁移工具**: EF Core Migrations

## 快速开始

### 1.  prerequisites

- .NET 8.0 SDK
- SQL Server 2016+
- Visual Studio 2022 或 VS Code

### 2. 数据库设置

```sql
-- 执行数据库脚本
sqlcmd -S localhost -d master -i database.sql
sqlcmd -S localhost -d EnglishLearning -i init-data.sql
```

### 3. 配置连接字符串

编辑 `appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=EnglishLearning;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

### 4. 运行项目

```bash
cd EnglishLearning.API
dotnet restore
dotnet run
```

访问 `https://localhost:5001/swagger` 查看 API 文档。

## API 接口

### 认证模块
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/me` - 获取当前用户信息

### 用户模块
- `GET /api/user/stats` - 学习统计
- `GET /api/user/badges` - 徽章列表
- `GET /api/user/points` - 积分记录
- `POST /api/user/checkin` - 每日签到

### 单词学习
- `GET /api/words` - 单词列表
- `GET /api/words/{id}` - 单词详情
- `POST /api/words/{id}/progress` - 更新学习进度

### 语法学习
- `GET /api/grammar` - 语法列表
- `GET /api/grammar/{id}` - 语法详情
- `POST /api/grammar/{id}/quiz` - 提交测验

### 题目模块
- `GET /api/questions/{id}` - 题目详情
- `POST /api/questions/{id}/answer` - 提交答案

### 每日挑战
- `GET /api/challenge/today` - 今日挑战状态
- `POST /api/challenge/start` - 开始挑战
- `POST /api/challenge/{id}/submit` - 提交挑战结果

### 错题本
- `GET /api/wrong-questions` - 错题列表
- `GET /api/wrong-questions/review` - 复习推送
- `POST /api/wrong-questions/{id}/review` - 复习错题
- `POST /api/wrong-questions/{id}/master` - 标记已掌握

## 核心功能

### 1. 积分系统
- 每日签到 +5 积分
- 完成每日挑战 +50 积分
- 单词完成 +10 积分
- 语法完成 +20 积分
- 满分奖励 +20 积分

### 2. 等级系统
12 个等级，从"英语小白"到"英语学霸"，通过学习获得经验值升级。

### 3. 徽章系统
- 连续打卡徽章（3/7/15/30 天）
- 单词学习徽章（50/100/300 词）
- 语法学习徽章（5/10 课）
- 挑战徽章（7/30 天）
- 特殊成就（满分达人）

### 4. 艾宾浩斯记忆曲线
复习间隔：即时 → 5 分钟 → 1 天 → 3 天 → 7 天 → 15 天 → 30 天

## 测试账号

| 用户名 | 密码 | 年级 | 说明 |
|-------|------|------|------|
| xiaoming | 123456 | 6 年级 | 已有学习记录 |
| xiaohong | 123456 | 3 年级 | 新用户状态 |

## 开发计划

- [x] 数据库设计
- [x] 实体类和 DTO
- [x] 业务服务层
- [x] API 控制器
- [x] 单元测试
- [x] 集成测试
- [ ] Docker 部署配置
- [ ] 性能优化

## 注意事项

1. JWT Token 默认有效期 2 小时
2. 密码使用 BCrypt 加密存储
3. 所有 API 响应统一格式
4. 全局异常处理和日志记录

## 许可证

MIT License
