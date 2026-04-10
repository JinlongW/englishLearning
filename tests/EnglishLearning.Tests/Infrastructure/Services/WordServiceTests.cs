using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Infrastructure.Services;
using EnglishLearning.Shared.Constants;
using FluentAssertions;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Moq;

namespace EnglishLearning.Tests.Infrastructure.Services;

public class WordServiceTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly Mock<IPointsService> _pointsServiceMock;
    private readonly WordService _wordService;
    private readonly Guid _testUserId;
    private readonly Guid _testUnitId;
    private readonly Guid _testWordId;

    public WordServiceTests()
    {
        // 使用 InMemory 数据库进行测试
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(databaseName: $"WordServiceTest_{Guid.NewGuid()}")
            .Options;

        _context = new AppDbContext(options);
        _pointsServiceMock = new Mock<IPointsService>();
        _wordService = new WordService(_context, _pointsServiceMock.Object);

        _testUserId = Guid.NewGuid();
        _testUnitId = Guid.NewGuid();
        _testWordId = Guid.NewGuid();

        SeedTestData();
    }

    private void SeedTestData()
    {
        // 创建测试年级单元
        _context.GradeUnits.Add(new GradeUnit
        {
            Id = _testUnitId,
            Grade = 3,
            Semester = "1",
            UnitNo = 1,
            UnitName = "Unit 1"
        });

        // 创建测试单词
        _context.Words.Add(new Word
        {
            Id = _testWordId,
            GradeUnitId = _testUnitId,
            WordText = "test",
            MeaningCn = "测试",
            PartOfSpeech = "v.",
            SortOrder = 1
        });

        _context.SaveChanges();
    }

    #region UpdateWordProgressAsync Tests

    [Fact]
    public async Task UpdateWordProgressAsync_NewWord_CreatesProgressRecordAndReturnsPoints()
    {
        // Arrange
        var score = 100;
        var status = "completed";

        _pointsServiceMock.Setup(x => x.AddExpAsync(_testUserId, 5))
            .ReturnsAsync(false);

        _pointsServiceMock.Setup(x => x.AddPointsAsync(
            _testUserId,
            "points",
            "word_complete",
            PointRules.WordLevelComplete + PointRules.PerfectScoreBonus,
            "单词学习完成",
            _testWordId))
            .Returns(Task.CompletedTask);

        // Act
        var result = await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        result.pointsEarned.Should().Be(PointRules.WordLevelComplete + PointRules.PerfectScoreBonus);
        result.expEarned.Should().Be(5);
        result.levelUp.Should().BeFalse();

        // 验证进度记录已创建
        var progress = await _context.LearningProgresses
            .FirstOrDefaultAsync(p => p.UserId == _testUserId && p.ContentId == _testWordId);

        progress.Should().NotBeNull();
        progress!.Status.Should().Be(status);
        progress.Score.Should().Be(score);
        progress.AttemptsCount.Should().Be(0);
    }

    [Fact]
    public async Task UpdateWordProgressAsync_ExistingWord_UpdatesProgressRecord()
    {
        // Arrange
        var existingProgress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "not_started",
            AttemptsCount = 2,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(existingProgress);
        _context.SaveChanges();

        var score = 85;
        var status = "completed";

        // Act
        var result = await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        var updatedProgress = await _context.LearningProgresses
            .FirstOrDefaultAsync(p => p.Id == existingProgress.Id);

        updatedProgress.Should().NotBeNull();
        updatedProgress!.Status.Should().Be(status);
        updatedProgress.Score.Should().Be(score);
        updatedProgress.AttemptsCount.Should().Be(3); // 2 + 1
        updatedProgress.LastAttemptAt.Should().BeCloseTo(DateTime.Now, TimeSpan.FromSeconds(5));
    }

    [Fact]
    public async Task UpdateWordProgressAsync_NonExistentWord_ThrowsBusinessException()
    {
        // Arrange
        var nonExistentWordId = Guid.NewGuid();

        // Act & Assert
        var act = async () => await _wordService.UpdateWordProgressAsync(nonExistentWordId, _testUserId, 100, "completed");
        await act.Should().ThrowAsync<Shared.Exceptions.BusinessException>()
            .WithMessage("单词不存在");
    }

    [Fact]
    public async Task UpdateWordProgressAsync_FirstCompletionWithPassingScore_AddsExpAndPoints()
    {
        // Arrange
        var score = 80; // >= 60, 首次完成
        var status = "completed";

        _pointsServiceMock.Setup(x => x.AddExpAsync(_testUserId, 5))
            .ReturnsAsync(true); // level up

        _pointsServiceMock.Setup(x => x.AddPointsAsync(
            _testUserId,
            "points",
            "word_complete",
            PointRules.WordLevelComplete,
            "单词学习完成",
            _testWordId))
            .Returns(Task.CompletedTask);

        // Act
        var result = await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        result.pointsEarned.Should().Be(PointRules.WordLevelComplete);
        result.expEarned.Should().Be(5);
        result.levelUp.Should().BeTrue();

        _pointsServiceMock.Verify(x => x.AddExpAsync(_testUserId, 5), Times.Once);
        _pointsServiceMock.Verify(x => x.AddPointsAsync(
            _testUserId,
            "points",
            "word_complete",
            PointRules.WordLevelComplete,
            "单词学习完成",
            _testWordId), Times.Once);
    }

    [Fact]
    public async Task UpdateWordProgressAsync_PerfectScore_AddsBonusPoints()
    {
        // Arrange - 已存在的进度记录，不是首次完成
        var existingProgress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "in_progress",
            AttemptsCount = 1,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(existingProgress);
        _context.SaveChanges();

        var score = 100; // 满分
        var status = "completed";

        _pointsServiceMock.Setup(x => x.AddPointsAsync(
            _testUserId,
            "points",
            "word_complete",
            PointRules.PerfectScoreBonus,
            "单词学习完成",
            _testWordId))
            .Returns(Task.CompletedTask);

        // Act
        var result = await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        result.pointsEarned.Should().Be(PointRules.PerfectScoreBonus);
        result.expEarned.Should().Be(0);
        result.levelUp.Should().BeFalse();
    }

    [Fact]
    public async Task UpdateWordProgressAsync_CompletedStatus_SetsCompletedAt()
    {
        // Arrange
        var existingProgress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "in_progress",
            AttemptsCount = 1,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(existingProgress);
        _context.SaveChanges();

        var score = 100;
        var status = "completed";

        // Act
        await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        var updatedProgress = await _context.LearningProgresses
            .FirstOrDefaultAsync(p => p.Id == existingProgress.Id);

        updatedProgress.Should().NotBeNull();
        updatedProgress!.CompletedAt.Should().NotBeNull();
        updatedProgress.CompletedAt.Value.Should().BeCloseTo(DateTime.Now, TimeSpan.FromSeconds(5));
    }

    [Fact]
    public async Task UpdateWordProgressAsync_InProgressStatus_DoesNotSetCompletedAt()
    {
        // Arrange
        var existingProgress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "not_started",
            AttemptsCount = 0,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(existingProgress);
        _context.SaveChanges();

        var score = 50;
        var status = "in_progress";

        // Act
        await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        var updatedProgress = await _context.LearningProgresses
            .FirstOrDefaultAsync(p => p.Id == existingProgress.Id);

        updatedProgress.Should().NotBeNull();
        updatedProgress!.CompletedAt.Should().BeNull();
    }

    [Fact]
    public async Task UpdateWordProgressAsync_MasteredStatus_SetsCompletedAt()
    {
        // Arrange
        var existingProgress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "completed",
            AttemptsCount = 3,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(existingProgress);
        _context.SaveChanges();

        var score = 100;
        var status = "mastered";

        // Act
        await _wordService.UpdateWordProgressAsync(_testWordId, _testUserId, score, status);

        // Assert
        var updatedProgress = await _context.LearningProgresses
            .FirstOrDefaultAsync(p => p.Id == existingProgress.Id);

        updatedProgress.Should().NotBeNull();
        updatedProgress!.CompletedAt.Should().NotBeNull();
    }

    #endregion

    #region GetWordsAsync Tests

    [Fact]
    public async Task GetWordsAsync_ReturnsPagedResultWithProgress()
    {
        // Arrange
        // 添加更多测试单词
        var word2 = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = _testUnitId,
            WordText = "apple",
            MeaningCn = "苹果",
            PartOfSpeech = "n.",
            SortOrder = 2
        };
        _context.Words.Add(word2);

        // 添加用户学习进度
        var progress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = word2.Id,
            Status = "completed",
            Score = 90,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(progress);
        _context.SaveChanges();

        // Act
        var result = await _wordService.GetWordsAsync(_testUnitId, _testUserId, 1, 10);

        // Assert
        result.Should().NotBeNull();
        result.Total.Should().Be(2);
        result.Page.Should().Be(1);
        result.PageSize.Should().Be(10);
        result.Items.Should().HaveCount(2);

        var appleWord = result.Items.FirstOrDefault(w => w.WordText == "apple");
        appleWord.Should().NotBeNull();
        appleWord!.Status.Should().Be("completed");
        appleWord.Score.Should().Be(90);

        var testWord = result.Items.FirstOrDefault(w => w.WordText == "test");
        testWord.Should().NotBeNull();
        testWord!.Status.Should().Be("not_started");
        testWord.Score.Should().BeNull();
    }

    [Fact]
    public async Task GetWordsAsync_EmptyUnit_ReturnsEmptyResult()
    {
        // Arrange
        var emptyUnitId = Guid.NewGuid();

        // Act
        var result = await _wordService.GetWordsAsync(emptyUnitId, _testUserId, 1, 10);

        // Assert
        result.Should().NotBeNull();
        result.Total.Should().Be(0);
        result.Items.Should().BeEmpty();
    }

    [Fact]
    public async Task GetWordsAsync_Pagination_ReturnsCorrectPage()
    {
        // Arrange - 添加 15 个单词
        for (int i = 0; i < 15; i++)
        {
            _context.Words.Add(new Word
            {
                Id = Guid.NewGuid(),
                GradeUnitId = _testUnitId,
                WordText = $"word{i}",
                MeaningCn = $"单词{i}",
                SortOrder = i + 3
            });
        }
        _context.SaveChanges();

        // Act - 获取第 2 页，每页 10 个
        var result = await _wordService.GetWordsAsync(_testUnitId, _testUserId, 2, 10);

        // Assert
        result.Total.Should().Be(17); // 2 个原有 + 15 个新增
        result.Page.Should().Be(2);
        result.PageSize.Should().Be(10);
        result.Items.Should().HaveCount(7); // 第 2 页只有 7 个
    }

    #endregion

    #region GetWordByIdAsync Tests

    [Fact]
    public async Task GetWordByIdAsync_ExistingWord_ReturnsWordWithProgress()
    {
        // Arrange
        var progress = new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = _testWordId,
            Status = "completed",
            Score = 95,
            CreatedAt = DateTime.Now.AddDays(-1)
        };
        _context.LearningProgresses.Add(progress);
        _context.SaveChanges();

        // Act
        var result = await _wordService.GetWordByIdAsync(_testWordId, _testUserId);

        // Assert
        result.Should().NotBeNull();
        result!.Id.Should().Be(_testWordId);
        result.Status.Should().Be("completed");
        result.Score.Should().Be(95);
    }

    [Fact]
    public async Task GetWordByIdAsync_NonExistentWord_ReturnsNull()
    {
        // Arrange
        var nonExistentWordId = Guid.NewGuid();

        // Act
        var result = await _wordService.GetWordByIdAsync(nonExistentWordId, _testUserId);

        // Assert
        result.Should().BeNull();
    }

    [Fact]
    public async Task GetWordByIdAsync_NoProgress_ReturnsWordWithNotStartedStatus()
    {
        // Act
        var result = await _wordService.GetWordByIdAsync(_testWordId, _testUserId);

        // Assert
        result.Should().NotBeNull();
        result!.Status.Should().Be("not_started");
        result.Score.Should().BeNull();
    }

    #endregion

    #region GetWordsDueForReviewAsync Tests

    [Fact]
    public async Task GetWordsDueForReviewAsync_NoLearnedWords_ReturnsEmptyList()
    {
        // Act
        var result = await _wordService.GetWordsDueForReviewAsync(_testUserId, 20);

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetWordsDueForReviewAsync_WordsDueForReview_ReturnsUrgentWordsFirst()
    {
        // Arrange
        var word1 = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = _testUnitId,
            WordText = "review1",
            MeaningCn = "复习 1",
            SortOrder = 100
        };
        var word2 = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = _testUnitId,
            WordText = "review2",
            MeaningCn = "复习 2",
            SortOrder = 101
        };
        _context.Words.AddRange(word1, word2);

        // 添加已完成的进度记录，一个已过期，一个即将到期
        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = word1.Id,
            Status = "completed",
            AttemptsCount = 1,
            LastAttemptAt = DateTime.Now.AddDays(-1), // 已过期
            CreatedAt = DateTime.Now.AddDays(-1)
        });

        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = word2.Id,
            Status = "completed",
            AttemptsCount = 1,
            LastAttemptAt = DateTime.Now, // 刚学习，5 分钟后复习
            CreatedAt = DateTime.Now
        });

        _context.SaveChanges();

        // Act
        var result = await _wordService.GetWordsDueForReviewAsync(_testUserId, 20);

        // Assert
        result.Should().HaveCount(2);
        result[0].IsUrgent.Should().BeTrue(); // 已过期的排在前面
    }

    [Fact]
    public async Task GetWordsDueForReviewAsync_MasteredWord_NotIncluded()
    {
        // Arrange
        var word = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = _testUnitId,
            WordText = "mastered",
            MeaningCn = "已掌握",
            SortOrder = 100
        };
        _context.Words.Add(word);

        // 添加已掌握的进度记录（复习次数超过间隔数组长度）
        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = word.Id,
            Status = "completed",
            AttemptsCount = 10, // 超过 EbbinghausIntervals.Length
            LastAttemptAt = DateTime.Now.AddDays(-1),
            CreatedAt = DateTime.Now.AddDays(-1)
        });

        _context.SaveChanges();

        // Act
        var result = await _wordService.GetWordsDueForReviewAsync(_testUserId, 20);

        // Assert
        result.Should().BeEmpty();
    }

    #endregion

    #region GetReviewScheduleAsync Tests

    [Fact]
    public async Task GetReviewScheduleAsync_NoLearnedWords_ReturnsEmptySchedule()
    {
        // Act
        var result = await _wordService.GetReviewScheduleAsync(_testUserId);

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetReviewScheduleAsync_HasLearnedWords_Returns7DaySchedule()
    {
        // Arrange
        var word = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = _testUnitId,
            WordText = "schedule",
            MeaningCn = "计划",
            SortOrder = 100
        };
        _context.Words.Add(word);

        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = _testUnitId,
            ContentType = "word",
            ContentId = word.Id,
            Status = "completed",
            AttemptsCount = 1,
            LastAttemptAt = DateTime.Now,
            CreatedAt = DateTime.Now
        });

        _context.SaveChanges();

        // Act
        var result = await _wordService.GetReviewScheduleAsync(_testUserId);

        // Assert
        result.Should().NotBeEmpty();
        result.Should().HaveCount(7); // 7 天的计划
    }

    #endregion

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }
}
