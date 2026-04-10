# 英语学习工具 - 测试指南

## 测试状态

### 后端集成测试

**当前状态**: ✅ 所有测试通过

- ✅ AuthIntegrationTests - 认证模块测试（3 通过，1 跳过）
- ✅ UserIntegrationTests - 用户模块测试（4 通过）

**测试结果**:
```
Passed:  7
Skipped: 1 (Login_WithInvalidCredentials - 需要数据库配置)
Total:   8
```

**跳过的测试**:
- `Login_WithInvalidCredentials_ReturnsUnauthorized` - 需要配置数据库连接验证逻辑

### 前端 E2E 测试

**当前状态**: ✅ Playwright 框架已配置

- ✅ playwright.config.ts - 配置文件
- ✅ e2e/auth.spec.ts - 认证流程测试
- ✅ e2e/home.spec.ts - 首页功能测试

**运行 E2E 测试**:
```bash
cd english-learning-frontend/miniapp
npm run test:e2e
```

## 目录结构

```
english-learning-api/
└── tests/
    └── EnglishLearning.Tests/
        ├── IntegrationTests/
        │   ├── AuthIntegrationTests.cs    # 认证模块集成测试
        │   └── UserIntegrationTests.cs    # 用户模块集成测试
        └── EnglishLearning.Tests.csproj
```

```
english-learning-frontend/miniapp/
├── e2e/
│   ├── auth.spec.ts                      # 认证流程 E2E 测试
│   └── home.spec.ts                      # 首页功能 E2E 测试
└── playwright.config.ts                  # Playwright 配置
```

## 运行测试

### 后端集成测试

```bash
# 运行所有测试
cd english-learning-api
dotnet test

# 运行特定测试类
dotnet test --filter "FullyQualifiedName~AuthIntegrationTests"

# 运行特定测试方法
dotnet test --filter "FullyQualifiedName~Register_WithValidData"

# 生成覆盖率报告（需要安装 coverlet）
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=lcov
```

### 前端 E2E 测试

```bash
# 安装 Playwright 浏览器
cd english-learning-frontend/miniapp
npx playwright install

# 运行所有 E2E 测试
npm run test:e2e

# 使用 UI 模式运行
npm run test:e2e:ui

# 调试模式运行
npm run test:e2e:debug

# 运行特定测试文件
npx playwright test e2e/auth.spec.ts

# 运行特定浏览器测试
npx playwright test --project chromium
```

## 测试说明

### 后端集成测试

**AuthIntegrationTests** - 认证模块测试
- `Register_WithValidData_ReturnsSuccess` - 测试有效数据注册
- `Register_WithWeakPassword_ReturnsBadRequest` - 测试弱密码拒绝
- `Login_WithValidCredentials_ReturnsToken` - 测试有效登录
- `Login_WithInvalidCredentials_ReturnsUnauthorized` - 测试无效登录

**UserIntegrationTests** - 用户模块测试
- `GetUserInfo_WithValidToken_ReturnsUserInfo` - 测试获取用户信息
- `CheckIn_WithValidToken_ReturnsSuccess` - 测试每日签到
- `GetLearningSummary_WithValidToken_ReturnsLearningStats` - 测试学习统计
- `GetUserInfo_WithoutToken_ReturnsUnauthorized` - 测试未授权访问

### 前端 E2E 测试

**auth.spec.ts** - 认证流程测试
- 新用户注册
- 用户登录
- 密码错误提示

**home.spec.ts** - 首页功能测试
- 首页内容显示
- 学单词导航
- 学语法导航
- 每日挑战导航
- 错题本导航

## 测试依赖

### 后端
- xUnit - 测试框架
- FluentAssertions - 断言库
- Moq - Mock 库
- Microsoft.AspNetCore.Mvc.Testing - ASP.NET Core 集成测试支持

### 前端
- @playwright/test - E2E 测试框架
- 支持浏览器：Chromium, Firefox, WebKit
- 支持移动设备：Pixel 5, iPhone 12

## 注意事项

1. **数据库配置**: 集成测试使用独立的测试数据库，确保 appsettings.Test.json 配置正确
2. **端口占用**: E2E 测试需要启动开发服务器，确保 5173 端口可用
3. **测试数据**: 测试使用唯一用户名避免冲突
4. **CI/CD**: 在 CI 环境中设置 `CI=true` 环境变量启用重试机制
