# 英语学习工具 - 快速部署指南

## 步骤 1: 配置 SQL Server 数据库

### 方法 1: 使用 SQL Server Management Studio (SSMS)

1. 打开 SSMS，连接到本地 SQL Server
2. 打开 `D:\2026\AI\english-learning-db\database.sql`
3. 执行脚本创建数据库和表
4. 打开 `D:\2026\AI\english-learning-db\init-data.sql`
5. 执行脚本插入测试数据

### 方法 2: 使用 sqlcmd 命令行

```bash
# 切换到数据库脚本目录
cd D:\2026\AI\english-learning-db

# 创建数据库（需要修改服务器名称）
sqlcmd -S localhost -E -i database.sql

# 插入测试数据
sqlcmd -S localhost -d EnglishLearning -E -i init-data.sql
```

### 验证数据库

```sql
USE EnglishLearning;
SELECT COUNT(*) FROM tb_user;
SELECT COUNT(*) FROM tb_grade_unit;
SELECT COUNT(*) FROM tb_word;
```

---

## 步骤 2: 配置数据库连接

编辑 `D:\2026\AI\english-learning-api\EnglishLearning.API\appsettings.json`

如果您的 SQL Server 不是本地默认实例，需要修改连接字符串：

```json
{
  "ConnectionStrings": {
    // 默认本地实例
    "DefaultConnection": "Server=localhost;Database=EnglishLearning;Trusted_Connection=True;TrustServerCertificate=True;"

    // 命名实例（如 SQLExpress）
    // "DefaultConnection": "Server=localhost\\SQLEXPRESS;Database=EnglishLearning;Trusted_Connection=True;TrustServerCertificate=True;"

    // 远程服务器
    // "DefaultConnection": "Server=192.168.1.100;Database=EnglishLearning;User Id=sa;Password=YourPassword;TrustServerCertificate=True;"
  }
}
```

---

## 步骤 3: 构建并运行后端

```bash
# 切换到项目目录
cd D:\2026\AI\english-learning-api

# 恢复 NuGet 包
dotnet restore

# 构建项目
dotnet build

# 运行 API
dotnet run --project EnglishLearning.API
```

运行成功后会看到：
```
Now listening on: https://localhost:5001
Now listening on: http://localhost:5000
Application started. Press Ctrl+C to shut down.
```

---

## 步骤 4: 测试 API 接口

### 使用 Swagger UI（推荐）

浏览器访问：`https://localhost:5001/swagger`

### 使用 Postman 或 HTTP 客户端

#### 1. 测试用户登录

```bash
curl -X POST https://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"xiaoming\",\"password\":\"123456\"}" \
  --insecure
```

**预期响应：**
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "...",
      "username": "xiaoming",
      "studentName": "小明",
      "gradeLevel": 6,
      "currentStreak": 5,
      "currentLevel": 3,
      "levelName": "进步之星"
    },
    "expiresIn": 7200
  }
}
```

#### 2. 获取用户信息（需要 Token）

```bash
curl -X GET https://localhost:5001/api/auth/me \
  -H "Authorization: Bearer {your_token}" \
  --insecure
```

#### 3. 每日签到

```bash
curl -X POST https://localhost:5001/api/user/checkin \
  -H "Authorization: Bearer {your_token}" \
  --insecure
```

#### 4. 获取单词列表

```bash
curl -X GET "https://localhost:5001/api/words?gradeUnitId={unit_id}" \
  -H "Authorization: Bearer {your_token}" \
  --insecure
```

---

## 步骤 5: 测试账号

| 用户名 | 密码 | 年级 | 说明 |
|-------|------|------|------|
| xiaoming | 123456 | 6 年级 | 已有学习记录 |
| xiaohong | 123456 | 3 年级 | 新用户状态 |

---

## 常见问题

### 1. 数据库连接失败

**错误**: `A network-related or instance-specific error occurred...`

**解决**:
- 检查 SQL Server 服务是否运行
- 确认连接字符串中的服务器名称正确
- 如果使用 SQL Express，使用 `localhost\SQLEXPRESS`

### 2. 证书错误

**错误**: `The certificate provided was not trusted`

**解决**: 连接字符串中添加 `TrustServerCertificate=True`

### 3. 端口被占用

**错误**: `Failed to bind to address https://localhost:5001`

**解决**: 修改 `Properties\launchSettings.json` 中的端口，或使用：
```bash
dotnet run --project EnglishLearning.API --urls "http://localhost:5000"
```

### 4. NuGet 包还原失败

**解决**:
```bash
# 清除 NuGet 缓存
dotnet nuget locals all --clear

# 重新还原
dotnet restore --force
```

---

## 下一步

后端运行正常后，可以开始：
1. 小程序前端开发（Uni-app + Vue 3）
2. Web 管理后台开发（Vue 3 + Element Plus）
