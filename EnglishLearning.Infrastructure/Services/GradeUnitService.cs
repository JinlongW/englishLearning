using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace EnglishLearning.Infrastructure.Services;

public class GradeUnitService : IGradeUnitService
{
    private readonly AppDbContext _context;
    private readonly ILogger<GradeUnitService> _logger;

    public GradeUnitService(AppDbContext context, ILogger<GradeUnitService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<List<int>> GetAllGradesAsync(CancellationToken cancellationToken = default)
    {
        var grades = await _context.GradeUnits
            .Select(g => g.Grade)
            .Distinct()
            .OrderBy(g => g)
            .ToListAsync(cancellationToken);

        return grades;
    }

    public async Task<List<GradeUnitDto>> GetUnitsByGradeAsync(int grade, CancellationToken cancellationToken = default)
    {
        var units = await _context.GradeUnits
            .Where(g => g.Grade == grade)
            .OrderBy(g => g.Semester)
            .ThenBy(g => g.UnitNo)
            .Select(g => new GradeUnitDto
            {
                Id = g.Id,
                Grade = g.Grade,
                Semester = g.Semester,
                UnitNo = g.UnitNo,
                UnitName = g.UnitName,
                WordCount = g.Words.Count
            })
            .ToListAsync(cancellationToken);

        return units;
    }

    public async Task<List<GradeTreeNode>> GetGradeUnitTreeAsync(Guid userId, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("GetGradeUnitTreeAsync called for userId: {UserId}", userId);

        // 获取所有年级单元（不预加载 Words，使用投影查询）
        var allUnits = await _context.GradeUnits
            .OrderBy(g => g.Grade)
            .ThenBy(g => g.Semester)
            .ThenBy(g => g.UnitNo)
            .ToListAsync(cancellationToken);

        // 获取每个单元的单词总数
        var unitWordCounts = await _context.Words
            .GroupBy(w => w.GradeUnitId)
            .ToDictionaryAsync(g => g.Key, g => g.Count(), cancellationToken);

        _logger.LogInformation("Total units: {UnitCount}, unit word counts loaded for {WordCountUnits} units",
            allUnits.Count, unitWordCounts.Count);

        // 按年级分组
        var gradeTree = allUnits
            .GroupBy(g => g.Grade)
            .Select(g => new GradeTreeNode
            {
                Grade = g.Key,
                Label = $"{g.Key}年级",
                Units = g.Select(u => new GradeUnitTreeNode
                {
                    Id = u.Id,
                    Label = u.UnitName,
                    Grade = u.Grade,
                    Semester = u.Semester,
                    UnitNo = u.UnitNo,
                    WordCount = unitWordCounts.TryGetValue(u.Id, out var count) ? count : 0,
                    LearnedWordCount = 0,
                    Status = "not_started"
                }).ToList()
            })
            .ToList();

        _logger.LogInformation("Initial grade tree built with {GradeCount} grades", gradeTree.Count);

        // 获取用户的学习进度 - 按 GradeUnitId 和 ContentId 分组，统计每个单元的不同单词数量
        var userProgress = await _context.LearningProgresses
            .Where(p => p.UserId == userId && p.ContentType == "word")
            .GroupBy(p => p.GradeUnitId)
            .Select(g => new
            {
                GradeUnitId = g.Key,
                LearnedCount = g.Count(p => p.Status == "completed" || p.Status == "mastered"),
                IsStarted = g.Any(p => p.Status != "not_started"),
                IsCompleted = g.All(p => p.Status == "completed" || p.Status == "mastered") && g.Count(p => p.Status == "completed" || p.Status == "mastered") > 0
            })
            .ToDictionaryAsync(x => x.GradeUnitId, x => x, cancellationToken);

        _logger.LogInformation("User progress loaded for {ProgressCount} units", userProgress.Count);

        // 日志：输出每个单元的进度详情
        foreach (var progress in userProgress)
        {
            _logger.LogInformation("Unit {UnitId}: learned={Learned}, started={Started}, completed={Completed}",
                progress.Key, progress.Value.LearnedCount, progress.Value.IsStarted, progress.Value.IsCompleted);
        }

        // 填充学习进度信息
        foreach (var gradeNode in gradeTree)
        {
            foreach (var unitNode in gradeNode.Units)
            {
                if (userProgress.TryGetValue(unitNode.Id, out var progress))
                {
                    unitNode.LearnedWordCount = progress.LearnedCount;
                    unitNode.Status = progress.IsCompleted
                        ? "completed"
                        : progress.IsStarted
                            ? "in_progress"
                            : "not_started";

                    _logger.LogInformation("Unit {UnitId} ({UnitName}): wordCount={WordCount}, learned={Learned}",
                        unitNode.Id, unitNode.Label, unitNode.WordCount, unitNode.LearnedWordCount);
                }
            }
        }

        return gradeTree;
    }
}
