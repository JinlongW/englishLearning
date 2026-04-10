using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using EnglishLearning.Tests;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace EnglishLearning.Tests.IntegrationTests;

/// <summary>
/// 用户模块集成测试
/// </summary>
public class UserIntegrationTests : IClassFixture<TestingWebApplicationFactory>
{
    private readonly TestingWebApplicationFactory _factory;
    private readonly HttpClient _client;

    public UserIntegrationTests(TestingWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    private async Task<(string token, string username)> GetAuthenticatedTokenAsync()
    {
        var username = $"testuser_{Guid.NewGuid():N}".Substring(0, 15);
        var registerData = new
        {
            username = username,
            password = "Test1234",
            studentName = "测试用户",
            gradeLevel = 7
        };

        var registerResponse = await _client.PostAsJsonAsync("/api/auth/register", registerData);
        registerResponse.EnsureSuccessStatusCode();

        var loginData = new
        {
            username = username,
            password = "Test1234"
        };

        var response = await _client.PostAsJsonAsync("/api/auth/login", loginData);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        var data = result.GetProperty("data");
        var token = data.GetProperty("token").GetString()!;

        return (token, username);
    }

    [Fact]
    public async Task GetUserInfo_WithValidToken_ReturnsUserInfo()
    {
        // Arrange
        var (token, _) = await GetAuthenticatedTokenAsync();
        _client.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

        // Act - /api/auth/me 是获取用户信息的正确端点
        var response = await _client.GetAsync("/api/auth/me");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    [Fact]
    public async Task CheckIn_WithValidToken_ReturnsSuccess()
    {
        // Arrange - 使用新的 HttpClient 避免速率限制
        var freshClient = _factory.CreateClient();
        var (token, _) = await GetAuthenticatedTokenAsync();
        freshClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

        // Act
        var response = await freshClient.PostAsync("/api/user/checkin", null);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    [Fact]
    public async Task GetLearningSummary_WithValidToken_ReturnsLearningStats()
    {
        // Arrange - 使用新的 HttpClient 避免速率限制
        var freshClient = _factory.CreateClient();
        var (token, _) = await GetAuthenticatedTokenAsync();
        freshClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

        // Act - /api/user/stats 是获取学习统计的正确端点
        var response = await freshClient.GetAsync("/api/user/stats");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    [Fact]
    public async Task GetUserInfo_WithoutToken_ReturnsUnauthorized()
    {
        // Act - 使用新的 HttpClient 避免速率限制
        var freshClient = _factory.CreateClient();
        var response = await freshClient.GetAsync("/api/auth/me");

        // Assert - 未授权用户应该返回 401
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }
}
