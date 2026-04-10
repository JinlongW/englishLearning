using EnglishLearning.Domain.Entities;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Infrastructure.Services;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Moq;

namespace EnglishLearning.Tests.Infrastructure.Services;

public class GradeUnitServiceTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly Mock<ILogger<GradeUnitService>> _loggerMock;
    private readonly GradeUnitService _gradeUnitService;
    private readonly Guid _testUserId;

    public GradeUnitServiceTests()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(databaseName: $"GradeUnitServiceTest_{Guid.NewGuid()}")
            .Options;

        _context = new AppDbContext(options);
        _loggerMock = new Mock<ILogger<GradeUnitService>>();
        _gradeUnitService = new GradeUnitService(_context, _loggerMock.Object);

        _testUserId = Guid.NewGuid();

        SeedTestData();
    }

    private void SeedTestData()
    {
        // 创建三年级上册 Unit 1
        var unit1 = new GradeUnit
        {
            Id = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409"),
            Grade = 3,
            Semester = "1",
            UnitNo = 1,
            UnitName = "Unit 1"
        };

        // 创建三年级上册 Unit 2
        var unit2 = new GradeUnit
        {
            Id = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890"),
            Grade = 3,
            Semester = "1",
            UnitNo = 2,
            UnitName = "Unit 2"
        };

        // 创建四年级上册 Unit 1
        var unit3 = new GradeUnit
        {
            Id = Guid.Parse("b2c3d4e5-f6a7-8901-bcde-f12345678901"),
            Grade = 4,
            Semester = "1",
            UnitNo = 1,
            UnitName = "Unit 1"
        };

        _context.GradeUnits.AddRange(unit1, unit2, unit3);

        // 为 Unit 1 添加 11 个单词
        for (int i = 0; i < 11; i++)
        {
            _context.Words.Add(new Word
            {
                Id = Guid.NewGuid(),
                GradeUnitId = unit1.Id,
                WordText = $"word{i}",
                MeaningCn = $"单词{i}",
                SortOrder = i
            });
        }

        // 为 Unit 2 添加 19 个单词
        for (int i = 0; i < 19; i++)
        {
            _context.Words.Add(new Word
            {
                Id = Guid.NewGuid(),
                GradeUnitId = unit2.Id,
                WordText = $"unit2word{i}",
                MeaningCn = $"单元 2 单词{i}",
                SortOrder = i
            });
        }

        // 为 Unit 3 添加 15 个单词
        for (int i = 0; i < 15; i++)
        {
            _context.Words.Add(new Word
            {
                Id = Guid.NewGuid(),
                GradeUnitId = unit3.Id,
                WordText = $"unit3word{i}",
                MeaningCn = $"单元 3 单词{i}",
                SortOrder = i
            });
        }

        _context.SaveChanges();
    }

    #region GetAllGradesAsync Tests

    [Fact]
    public async Task GetAllGradesAsync_ReturnsDistinctGrades()
    {
        // Act
        var result = await _gradeUnitService.GetAllGradesAsync();

        // Assert
        result.Should().HaveCount(2);
        result.Should().ContainInOrder(3, 4);
    }

    [Fact]
    public async Task GetAllGradesAsync_NoData_ReturnsEmptyList()
    {
        // Arrange
        _context.GradeUnits.RemoveRange(_context.GradeUnits);
        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetAllGradesAsync();

        // Assert
        result.Should().BeEmpty();
    }

    #endregion

    #region GetUnitsByGradeAsync Tests

    [Fact]
    public async Task GetUnitsByGradeAsync_ReturnsUnitsForGrade()
    {
        // Act
        var result = await _gradeUnitService.GetUnitsByGradeAsync(3);

        // Assert
        result.Should().HaveCount(2);
        result[0].Grade.Should().Be(3);
        result[0].Semester.Should().Be("1");
        result[0].UnitNo.Should().Be(1);
        result[0].WordCount.Should().Be(11);

        result[1].UnitNo.Should().Be(2);
        result[1].WordCount.Should().Be(19);
    }

    [Fact]
    public async Task GetUnitsByGradeAsync_NonExistentGrade_ReturnsEmptyList()
    {
        // Act
        var result = await _gradeUnitService.GetUnitsByGradeAsync(5);

        // Assert
        result.Should().BeEmpty();
    }

    [Fact]
    public async Task GetUnitsByGradeAsync_OrderBySemesterThenUnitNo()
    {
        // Arrange - 添加更多单元
        var unit4 = new GradeUnit
        {
            Id = Guid.NewGuid(),
            Grade = 3,
            Semester = "2",
            UnitNo = 1,
            UnitName = "Unit 1 (Semester 2)"
        };
        _context.GradeUnits.Add(unit4);
        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetUnitsByGradeAsync(3);

        // Assert
        result.Should().HaveCount(3);
        result[0].Semester.Should().Be("1");
        result[0].UnitNo.Should().Be(1);
        result[1].Semester.Should().Be("1");
        result[1].UnitNo.Should().Be(2);
        result[2].Semester.Should().Be("2");
        result[2].UnitNo.Should().Be(1);
    }

    #endregion

    #region GetGradeUnitTreeAsync Tests

    [Fact]
    public async Task GetGradeUnitTreeAsync_NoUserProgress_ReturnsNotStartedStatus()
    {
        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        result.Should().HaveCount(2); // 3 年级和 4 年级

        var grade3 = result.First(g => g.Grade == 3);
        grade3.Units.Should().HaveCount(2);

        foreach (var unit in grade3.Units)
        {
            unit.Status.Should().Be("not_started");
            unit.LearnedWordCount.Should().Be(0);
        }
    }

    [Fact]
    public async Task GetGradeUnitTreeAsync_WithUserProgress_ReturnsCorrectStatus()
    {
        // Arrange - 添加用户学习进度
        var unit1Id = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");
        var unit2Id = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890");

        // Unit 1: 完成 11/11 单词（已完成）
        for (int i = 0; i < 11; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit1Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit1Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "completed",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-1)
            });
        }

        // Unit 2: 完成 9/19 单词（进行中）
        for (int i = 0; i < 9; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit2Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "completed",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-1)
            });
        }

        // 添加一些未完成的进度
        var unit2Word10 = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == 10);
        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = unit2Id,
            ContentType = "word",
            ContentId = unit2Word10.Id,
            Status = "in_progress",
            Score = 50,
            CreatedAt = DateTime.Now
        });

        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        var grade3 = result.First(g => g.Grade == 3);

        var unit1 = grade3.Units.First(u => u.UnitNo == 1);
        unit1.Status.Should().Be("completed");
        unit1.LearnedWordCount.Should().Be(11);
        unit1.WordCount.Should().Be(11);

        var unit2 = grade3.Units.First(u => u.UnitNo == 2);
        unit2.Status.Should().Be("in_progress");
        unit2.LearnedWordCount.Should().Be(9);
        unit2.WordCount.Should().Be(19);
    }

    [Fact]
    public async Task GetGradeUnitTreeAsync_AllWordsCompleted_ReturnsCompletedStatus()
    {
        // Arrange
        var unit2Id = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890");

        // 完成 Unit 2 的所有 19 个单词
        for (int i = 0; i < 19; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit2Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "completed",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-1)
            });
        }

        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        var grade3 = result.First(g => g.Grade == 3);
        var unit2 = grade3.Units.First(u => u.UnitNo == 2);

        unit2.Status.Should().Be("completed");
        unit2.LearnedWordCount.Should().Be(19);
        unit2.WordCount.Should().Be(19);
    }

    [Fact]
    public async Task GetGradeUnitTreeAsync_MasteredWords_CountsAsCompleted()
    {
        // Arrange
        var unit1Id = Guid.Parse("51a042a6-f1c4-433d-a8c3-1a2a9bf95409");

        // 掌握 Unit 1 的所有单词
        for (int i = 0; i < 11; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit1Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit1Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "mastered",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-1)
            });
        }

        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        var grade3 = result.First(g => g.Grade == 3);
        var unit1 = grade3.Units.First(u => u.UnitNo == 1);

        unit1.Status.Should().Be("completed");
        unit1.LearnedWordCount.Should().Be(11);
    }

    [Fact]
    public async Task GetGradeUnitTreeAsync_MixedStatus_CorrectlyCalculatesProgress()
    {
        // Arrange
        var unit2Id = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890");

        // 5 个 completed
        for (int i = 0; i < 5; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit2Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "completed",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-1)
            });
        }

        // 3 个 mastered
        for (int i = 5; i < 8; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit2Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "mastered",
                Score = 100,
                CreatedAt = DateTime.Now.AddDays(-2)
            });
        }

        // 2 个 in_progress
        for (int i = 8; i < 10; i++)
        {
            var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == i);
            _context.LearningProgresses.Add(new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = _testUserId,
                GradeUnitId = unit2Id,
                ContentType = "word",
                ContentId = word.Id,
                Status = "in_progress",
                Score = 50,
                CreatedAt = DateTime.Now
            });
        }

        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        var grade3 = result.First(g => g.Grade == 3);
        var unit2 = grade3.Units.First(u => u.UnitNo == 2);

        unit2.Status.Should().Be("in_progress"); // 因为还有未完成的
        unit2.LearnedWordCount.Should().Be(8); // 5 completed + 3 mastered
    }

    [Fact]
    public async Task GetGradeUnitTreeAsync_OnlyNotStartedProgress_StatusIsNotStarted()
    {
        // Arrange
        var unit2Id = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890");

        // 只添加 not_started 的进度
        var word = _context.Words.First(w => w.GradeUnitId == unit2Id && w.SortOrder == 0);
        _context.LearningProgresses.Add(new LearningProgress
        {
            Id = Guid.NewGuid(),
            UserId = _testUserId,
            GradeUnitId = unit2Id,
            ContentType = "word",
            ContentId = word.Id,
            Status = "not_started",
            Score = null,
            CreatedAt = DateTime.Now
        });

        _context.SaveChanges();

        // Act
        var result = await _gradeUnitService.GetGradeUnitTreeAsync(_testUserId);

        // Assert
        var grade3 = result.First(g => g.Grade == 3);
        var unit2 = grade3.Units.First(u => u.UnitNo == 2);

        // 因为只有 not_started 的进度，所以 Status 应该是 not_started
        unit2.Status.Should().Be("not_started");
        unit2.LearnedWordCount.Should().Be(0);
    }

    #endregion

    public void Dispose()
    {
        _context.Database.EnsureDeleted();
        _context.Dispose();
    }
}
