using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using EnglishLearning.API;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace EnglishLearning.Tests.IntegrationTests;

/// <summary>
/// 认证模块集成测试
/// </summary>
public class AuthIntegrationTests : IClassFixture<TestingWebApplicationFactory>
{
    private readonly TestingWebApplicationFactory _factory;
    private readonly HttpClient _client;

    public AuthIntegrationTests(TestingWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Register_WithValidData_ReturnsSuccess()
    {
        // Arrange
        var registerData = new
        {
            username = $"testuser_{Guid.NewGuid():N}".Substring(0, 15),
            password = "Test1234",
            studentName = "测试用户",
            gradeLevel = 7
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/register", registerData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    [Fact]
    public async Task Register_WithWeakPassword_ReturnsBadRequest()
    {
        // Arrange
        var registerData = new
        {
            username = $"testuser_{Guid.NewGuid():N}".Substring(0, 15),
            password = "123", // 密码太短
            studentName = "测试用户",
            gradeLevel = 7
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/register", registerData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Login_WithValidCredentials_ReturnsToken()
    {
        // Arrange - 先注册一个用户
        var username = $"testuser_{Guid.NewGuid():N}".Substring(0, 15);
        var registerData = new
        {
            username = username,
            password = "Test1234",
            studentName = "测试用户",
            gradeLevel = 7
        };

        await _client.PostAsJsonAsync("/api/auth/register", registerData);

        // Act - 登录
        var loginData = new
        {
            username = username,
            password = "Test1234"
        };
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();

        // 检查 data 对象中的 token
        var data = result.GetProperty("data");
        data.GetProperty("token").GetString().Should().NotBeNullOrEmpty();
    }

    [Fact(Skip = "需要配置测试数据库连接")]
    public async Task Login_WithInvalidCredentials_ReturnsUnauthorized()
    {
        // Arrange
        var loginData = new
        {
            username = "nonexistent_user",
            password = "WrongPassword123"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }
}
