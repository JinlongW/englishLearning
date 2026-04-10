---
name: 测试覆盖率分析
description: EnglishLearning.API 项目测试覆盖率分析结果和改进建议
type: reference
---

# EnglishLearning.API 测试覆盖率报告

## 测试执行结果 (2026-04-10)

### 总体统计
- 测试总数：92
- 通过：74 (80%)
- 失败：17
- 跳过：1

### 按类别分

| 测试类别 | 通过 | 失败 | 说明 |
|----------|------|------|------|
| AuthValidatorsTests | 25+ | 0 | 登录/注册验证器测试全部通过 |
| GradeUnitServiceTests | 10+ | 0 | 年级单元服务测试通过 |
| WordServiceTests | 部分 | 部分 | 使用 ExecuteSqlRawAsync 的测试失败 |
| WordIntegrationTests | 部分 | 部分 | 边界验证测试失败 |

## 已知问题

### 1. ExecuteSqlRawAsync 与 InMemory 数据库不兼容

**问题**: WordService.UpdateWordProgressAsync 使用 `ExecuteSqlRawAsync` 执行 SQL UPDATE，但测试使用 EF Core InMemory 数据库，导致错误：
```
System.InvalidOperationException : Relational-specific methods can only be used when the context is using a relational database provider.
```

**解决方案选项**:

1. **使用 TestContainers** (推荐)
   - 在测试容器中使用真实的 SQL Server
   - 最准确的集成测试

2. **抽象数据访问层**
   - 将 `ExecuteSqlRawAsync` 调用封装到接口中
   - 测试时 Mock 该接口

3. **条件跳过测试**
   - 对于无法在 InMemory 运行的测试使用 `[Fact(Skip = "...")]`

### 2. 集成测试边界验证失败

以下集成测试失败，因为 API 没有正确验证输入：

- `UpdateProgress_WithNonExistentWord_ReturnsNotFound` - 预期 404
- `UpdateProgress_WithInvalidScore_ReturnsBadRequest` - 预期 400 (score > 100)
- `UpdateProgress_WithNegativeScore_ReturnsBadRequest` - 预期 400 (score < 0)

**原因**: UpdateProgressRequestValidator 验证规则存在，但可能在某些情况下未正确应用。

## 已创建测试文件

1. `tests/EnglishLearning.Tests/Infrastructure/Services/WordServiceTests.cs` - 20+ 测试
2. `tests/EnglishLearning.Tests/Infrastructure/Services/GradeUnitServiceTests.cs` - 15+ 测试
3. `tests/EnglishLearning.Tests/API/Validators/AuthValidatorsTests.cs` - 25+ 测试
4. `tests/EnglishLearning.Tests/IntegrationTests/WordIntegrationTests.cs` - 20+ 测试

## 下一步建议

1. 对于 WordService 测试，建议使用 TestContainers.Microsoft.SqlServer 进行真实数据库测试
2. 修复边界验证逻辑或调整测试预期
3. 添加覆盖率收集工具（如 coverlet）生成 HTML 覆盖率报告
4. 目标：达到 80%+ 代码覆盖率
