using System.Net;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using EnglishLearning.Domain.DTOs;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace EnglishLearning.Tests.IntegrationTests;

/// <summary>
/// 单词模块集成测试
/// </summary>
public class WordIntegrationTests : IClassFixture<TestingWebApplicationFactory>
{
    private readonly TestingWebApplicationFactory _factory;
    private readonly HttpClient _client;
    private readonly HttpClient _authenticatedClient;
    private readonly string _authToken;

    public WordIntegrationTests(TestingWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
        _authToken = GetTestUserToken();

        _authenticatedClient = factory.CreateClient();
        _authenticatedClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _authToken);
    }

    private string GetTestUserToken()
    {
        // 使用测试用户登录获取 token
        var loginData = new
        {
            username = "xiaoming",
            password = "123456"
        };

        var response = _client.PostAsJsonAsync("/api/auth/login", loginData).Result;
        if (response.IsSuccessStatusCode)
        {
            var result = response.Content.ReadFromJsonAsync<JsonElement>().Result;
            return result.GetProperty("data").GetProperty("token").GetString()!;
        }

        throw new InvalidOperationException("无法获取测试用户 token，请确保测试用户已存在");
    }

    #region GetWords Tests

    [Fact]
    public async Task GetWords_WithoutAuth_ReturnsUnauthorized()
    {
        // Act
        var response = await _client.GetAsync("/api/word?gradeUnitId=51a042a6-f1c4-433d-a8c3-1a2a9bf95409");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task GetWords_WithValidAuth_ReturnsSuccess()
    {
        // Arrange
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");

        // Act
        var response = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
        result.GetProperty("data").GetProperty("items").GetArrayLength().Should().BeGreaterThan(0);
    }

    [Fact]
    public async Task GetWords_WithInvalidGradeUnitId_ReturnsBadRequest()
    {
        // Act
        var response = await _authenticatedClient.GetAsync("/api/word?gradeUnitId=00000000-0000-0000-0000-000000000000");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task GetWords_WithPagination_ReturnsCorrectPage()
    {
        // Arrange
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");

        // Act
        var response = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}&page=1&pageSize=5");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("data").GetProperty("items").GetArrayLength().Should().BeLessThanOrEqualTo(5);
        result.GetProperty("data").GetProperty("page").GetInt32().Should().Be(1);
        result.GetProperty("data").GetProperty("pageSize").GetInt32().Should().Be(5);
    }

    #endregion

    #region GetWordById Tests

    [Fact]
    public async Task GetWordById_WithoutAuth_ReturnsUnauthorized()
    {
        // Arrange
        var wordId = Guid.NewGuid();

        // Act
        var response = await _client.GetAsync($"/api/word/{wordId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task GetWordById_WithNonExistentId_ReturnsNotFound()
    {
        // Arrange
        var wordId = Guid.NewGuid();

        // Act
        var response = await _authenticatedClient.GetAsync($"/api/word/{wordId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task GetWordById_WithValidId_ReturnsWordWithProgress()
    {
        // Arrange - 先获取单词列表找到一个单词
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var wordsResponse = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");
        var wordsResult = await wordsResponse.Content.ReadFromJsonAsync<JsonElement>();
        var firstWordId = wordsResult.GetProperty("data").GetProperty("items")[0].GetProperty("id").GetGuid();

        // Act
        var response = await _authenticatedClient.GetAsync($"/api/word/{firstWordId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
        result.GetProperty("data").GetProperty("id").GetGuid().Should().Be(firstWordId);
    }

    #endregion

    #region UpdateProgress Tests

    [Fact]
    public async Task UpdateProgress_WithoutAuth_ReturnsUnauthorized()
    {
        // Arrange
        var wordId = Guid.NewGuid();
        var updateData = new { score = 100, status = "completed" };

        // Act
        var response = await _client.PostAsJsonAsync($"/api/word/{wordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task UpdateProgress_WithNonExistentWord_ReturnsNotFound()
    {
        // Arrange
        var wordId = Guid.NewGuid();
        var updateData = new { score = 100, status = "completed" };

        // Act
        var response = await _authenticatedClient.PostAsJsonAsync($"/api/word/{wordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task UpdateProgress_WithValidData_ReturnsSuccess()
    {
        // Arrange - 先获取一个单词
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var wordsResponse = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");
        var wordsResult = await wordsResponse.Content.ReadFromJsonAsync<JsonElement>();
        var firstWordId = wordsResult.GetProperty("data").GetProperty("items")[0].GetProperty("id").GetGuid();

        var updateData = new
        {
            score = 100,
            status = "completed"
        };

        // Act
        var response = await _authenticatedClient.PostAsJsonAsync($"/api/word/{firstWordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
        result.GetProperty("data").GetProperty("pointsEarned").GetInt32().Should().BeGreaterOrEqualTo(0);
    }

    [Fact]
    public async Task UpdateProgress_WithPerfectScore_AddsBonusPoints()
    {
        // Arrange - 先获取一个单词
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var wordsResponse = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");
        var wordsResult = await wordsResponse.Content.ReadFromJsonAsync<JsonElement>();
        var firstWordId = wordsResult.GetProperty("data").GetProperty("items")[0].GetProperty("id").GetGuid();

        var updateData = new
        {
            score = 100,
            status = "completed"
        };

        // Act
        var response = await _authenticatedClient.PostAsJsonAsync($"/api/word/{firstWordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        var pointsEarned = result.GetProperty("data").GetProperty("pointsEarned").GetInt32();

        // 满分应该获得额外积分
        pointsEarned.Should().BeGreaterOrEqualTo(20); // PerfectScoreBonus
    }

    [Fact]
    public async Task UpdateProgress_WithInvalidScore_ReturnsBadRequest()
    {
        // Arrange
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var wordsResponse = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");
        var wordsResult = await wordsResponse.Content.ReadFromJsonAsync<JsonElement>();
        var firstWordId = wordsResult.GetProperty("data").GetProperty("items")[0].GetProperty("id").GetGuid();

        var updateData = new
        {
            score = 150, // 超过 100
            status = "completed"
        };

        // Act
        var response = await _authenticatedClient.PostAsJsonAsync($"/api/word/{firstWordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task UpdateProgress_WithNegativeScore_ReturnsBadRequest()
    {
        // Arrange
        var unitId = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var wordsResponse = await _authenticatedClient.GetAsync($"/api/word?gradeUnitId={unitId}");
        var wordsResult = await wordsResponse.Content.ReadFromJsonAsync<JsonElement>();
        var firstWordId = wordsResult.GetProperty("data").GetProperty("items")[0].GetProperty("id").GetGuid();

        var updateData = new
        {
            score = -10,
            status = "completed"
        };

        // Act
        var response = await _authenticatedClient.PostAsJsonAsync($"/api/word/{firstWordId}/progress", updateData);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    #endregion

    #region GetWordsDueForReview Tests

    [Fact]
    public async Task GetWordsDueForReview_WithoutAuth_ReturnsUnauthorized()
    {
        // Act
        var response = await _client.GetAsync("/api/word/review/due");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task GetWordsDueForReview_WithValidAuth_ReturnsSuccess()
    {
        // Act
        var response = await _authenticatedClient.GetAsync("/api/word/review/due");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    #endregion

    #region GetReviewSchedule Tests

    [Fact]
    public async Task GetReviewSchedule_WithoutAuth_ReturnsUnauthorized()
    {
        // Act
        var response = await _client.GetAsync("/api/word/review/schedule");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task GetReviewSchedule_WithValidAuth_ReturnsSuccess()
    {
        // Act
        var response = await _authenticatedClient.GetAsync("/api/word/review/schedule");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<JsonElement>();
        result.GetProperty("success").GetBoolean().Should().BeTrue();
    }

    #endregion
}
