using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Infrastructure.Services;
using EnglishLearning.Shared.Exceptions;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Moq;

namespace EnglishLearning.Tests.UnitTests;

/// <summary>
/// 语法服务单元测试 - 使用数据库集成测试方式
/// </summary>
public class GrammarServiceTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly Mock<IPointsService> _mockPointsService;
    private readonly GrammarService _grammarService;

    public GrammarServiceTests()
    {
        // 创建内存数据库用于测试
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new AppDbContext(options);
        _mockPointsService = new Mock<IPointsService>();
        _grammarService = new GrammarService(_context, _mockPointsService.Object);
    }

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }

    #region GetGrammarsAsync 测试

    [Fact]
    public async Task GetGrammarsAsync_WithEmptyUnit_ReturnsEmptyList()
    {
        // Arrange
        var gradeUnitId = Guid.NewGuid();
        var userId = Guid.NewGuid();

        // Act
        var result = await _grammarService.GetGrammarsAsync(gradeUnitId, userId);

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetGrammarsAsync_WithGrammarsAndNoProgress_ReturnsAvailableStatus()
    {
        // Arrange
        var gradeUnitId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var grammarId = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = gradeUnitId,
            Title = "一般现在时",
            ContentType = "tense",
            SortOrder = 1,
            PassingScore = 60,
            PrerequisiteId = null,
            DependencyLevel = "1",
            Category = "tense"
        };

        _context.Grammars.Add(grammar);
        await _context.SaveChangesAsync();

        // Act
        var result = await _grammarService.GetGrammarsAsync(gradeUnitId, userId);

        // Assert
        result.Should().HaveCount(1);
        result[0].Id.Should().Be(grammarId);
        result[0].Title.Should().Be("一般现在时");
        result[0].Status.Should().Be("available");
    }

    [Fact]
    public async Task GetGrammarsAsync_WithCompletedProgress_ReturnsCompletedStatus()
    {
        // Arrange
        var gradeUnitId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var grammarId = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = gradeUnitId,
            Title = "一般现在时",
            ContentType = "tense",
            SortOrder = 1,
            PassingScore = 60,
            PrerequisiteId = null,
            DependencyLevel = "1",
            Category = "tense"
        };

        _context.Grammars.Add(grammar);

        var progress = new LearningProgress
        {
            UserId = userId,
            GradeUnitId = gradeUnitId,
            ContentType = "grammar",
            ContentId = grammarId,
            Status = "completed",
            Score = 85
        };

        _context.LearningProgresses.Add(progress);
        await _context.SaveChangesAsync();

        // Act
        var result = await _grammarService.GetGrammarsAsync(gradeUnitId, userId);

        // Assert
        result.Should().HaveCount(1);
        result[0].Status.Should().Be("completed");
        result[0].Score.Should().Be(85);
    }

    [Fact]
    public async Task GetGrammarsAsync_WithPrerequisiteIncomplete_ReturnsLockedStatus()
    {
        // Arrange
        var gradeUnitId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var grammarId1 = Guid.NewGuid();
        var grammarId2 = Guid.NewGuid();

        var grammar1 = new Grammar
        {
            Id = grammarId1,
            GradeUnitId = gradeUnitId,
            Title = "一般现在时",
            ContentType = "tense",
            SortOrder = 1,
            PassingScore = 60,
            PrerequisiteId = null,
            DependencyLevel = "1",
            Category = "tense"
        };

        var grammar2 = new Grammar
        {
            Id = grammarId2,
            GradeUnitId = gradeUnitId,
            Title = "现在进行时",
            ContentType = "tense",
            SortOrder = 2,
            PassingScore = 60,
            PrerequisiteId = grammarId1, // 前置条件是 grammar1
            DependencyLevel = "2",
            Category = "tense"
        };

        _context.Grammars.AddRange(grammar1, grammar2);
        await _context.SaveChangesAsync();

        // Act
        var result = await _grammarService.GetGrammarsAsync(gradeUnitId, userId);

        // Assert
        result.Should().HaveCount(2);
        result[0].Status.Should().Be("available"); // grammar1 没有前置条件
        result[1].Status.Should().Be("locked"); // grammar2 的前置条件未完成
    }

    #endregion

    #region GetGrammarByIdAsync 测试

    [Fact]
    public async Task GetGrammarByIdAsync_WithExistingGrammar_ReturnsGrammarDetail()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            Title = "一般现在时",
            ContentType = "tense",
            SortOrder = 1,
            PassingScore = 60,
            ContentJson = "{\"rules\": []}",
            QuizJson = "{\"questions\": []}"
        };

        _context.Grammars.Add(grammar);
        await _context.SaveChangesAsync();

        // Act
        var result = await _grammarService.GetGrammarByIdAsync(grammarId, userId);

        // Assert
        result.Should().NotBeNull();
        result!.Id.Should().Be(grammarId);
        result.Title.Should().Be("一般现在时");
    }

    [Fact]
    public async Task GetGrammarByIdAsync_WithNonExistingGrammar_ReturnsNull()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();

        // Act
        var result = await _grammarService.GetGrammarByIdAsync(grammarId, userId);

        // Assert
        result.Should().BeNull();
    }

    #endregion

    #region SubmitGrammarQuizAsync 测试

    [Fact]
    public async Task SubmitGrammarQuizAsync_WithNonExistingGrammar_ThrowsBusinessException()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var answers = new List<QuizAnswerRequest>();

        // Act & Assert
        await _grammarService.Invoking(s => s.SubmitGrammarQuizAsync(grammarId, userId, answers))
            .Should().ThrowAsync<BusinessException>()
            .WithMessage("语法课程不存在");
    }

    [Fact]
    public async Task SubmitGrammarQuizAsync_WithAllCorrectAnswers_ReturnsPerfectScore()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var questionId1 = Guid.NewGuid();
        var questionId2 = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = Guid.NewGuid(),
            Title = "一般现在时",
            PassingScore = 60
        };

        var questions = new List<Question>
        {
            new Question { Id = questionId1, CorrectAnswer = "A" },
            new Question { Id = questionId2, CorrectAnswer = "B" }
        };

        _context.Grammars.Add(grammar);
        _context.Questions.AddRange(questions);
        await _context.SaveChangesAsync();

        var answers = new List<QuizAnswerRequest>
        {
            new QuizAnswerRequest { QuestionId = questionId1, UserAnswer = "A" },
            new QuizAnswerRequest { QuestionId = questionId2, UserAnswer = "B" }
        };

        // Act
        var result = await _grammarService.SubmitGrammarQuizAsync(grammarId, userId, answers);

        // Assert
        result.score.Should().Be(100);
        result.isPassed.Should().BeTrue();
        result.correctCount.Should().Be(2);
        result.totalCount.Should().Be(2);
    }

    [Fact]
    public async Task SubmitGrammarQuizAsync_WithPartialCorrectAnswers_ReturnsPartialScore()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var questionId1 = Guid.NewGuid();
        var questionId2 = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = Guid.NewGuid(),
            Title = "一般现在时",
            PassingScore = 60
        };

        var questions = new List<Question>
        {
            new Question { Id = questionId1, CorrectAnswer = "A" },
            new Question { Id = questionId2, CorrectAnswer = "B" }
        };

        _context.Grammars.Add(grammar);
        _context.Questions.AddRange(questions);
        await _context.SaveChangesAsync();

        var answers = new List<QuizAnswerRequest>
        {
            new QuizAnswerRequest { QuestionId = questionId1, UserAnswer = "A" },
            new QuizAnswerRequest { QuestionId = questionId2, UserAnswer = "C" } // 错误答案
        };

        // Act
        var result = await _grammarService.SubmitGrammarQuizAsync(grammarId, userId, answers);

        // Assert
        result.score.Should().Be(50);
        result.isPassed.Should().BeFalse();
        result.correctCount.Should().Be(1);
        result.totalCount.Should().Be(2);
    }

    [Fact]
    public async Task SubmitGrammarQuizAsync_WithPassingScore_AddsPointsAndExp()
    {
        // Arrange
        var grammarId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var questionId = Guid.NewGuid();

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = Guid.NewGuid(),
            Title = "一般现在时",
            PassingScore = 60
        };

        var questions = new List<Question>
        {
            new Question { Id = questionId, CorrectAnswer = "A" }
        };

        _context.Grammars.Add(grammar);
        _context.Questions.AddRange(questions);
        await _context.SaveChangesAsync();

        var answers = new List<QuizAnswerRequest>
        {
            new QuizAnswerRequest { QuestionId = questionId, UserAnswer = "A" }
        };

        // Act
        var result = await _grammarService.SubmitGrammarQuizAsync(grammarId, userId, answers);

        // Assert
        result.isPassed.Should().BeTrue();
        _mockPointsService.Verify(p => p.AddPointsAsync(userId, "points", "grammar_complete", It.IsAny<int>(), "语法课程完成", grammarId), Times.Once);
        _mockPointsService.Verify(p => p.AddExpAsync(userId, 10), Times.Once);
    }

    #endregion

    #region GetGrammarTreeAsync 测试

    [Fact]
    public async Task GetGrammarTreeAsync_WithEmptyGrammars_ReturnsEmptyTree()
    {
        // Arrange
        var userId = Guid.NewGuid();
        var grade = 7;

        // Act
        var result = await _grammarService.GetGrammarTreeAsync(userId, grade);

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetGrammarTreeAsync_WithEmptyDependencyLevel_DoesNotThrow()
    {
        // Arrange
        var userId = Guid.NewGuid();
        var grade = 7;
        var grammarId = Guid.NewGuid();
        var gradeUnitId = Guid.NewGuid();

        var gradeUnit = new GradeUnit
        {
            Id = gradeUnitId,
            Grade = grade,
            Semester = "上册",
            UnitNo = 1,
            UnitName = "Unit 1",
            SortOrder = 1,
            IsLocked = false
        };

        var grammar = new Grammar
        {
            Id = grammarId,
            GradeUnitId = gradeUnitId,
            Title = "一般现在时",
            ContentType = "tense",
            SortOrder = 1,
            PrerequisiteId = null,
            DependencyLevel = "", // 空字符串测试
            Category = "tense"
        };

        _context.GradeUnits.Add(gradeUnit);
        _context.Grammars.Add(grammar);
        await _context.SaveChangesAsync();

        // Act
        var result = await _grammarService.GetGrammarTreeAsync(userId, grade);

        // Assert
        result.Should().HaveCount(1);
        result[0].Level.Should().Be(0); // 空字符串应返回 0
    }

    #endregion
}
