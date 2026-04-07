using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

public class GradeUnitService : IGradeUnitService
{
    private readonly AppDbContext _context;

    public GradeUnitService(AppDbContext context)
    {
        _context = context;
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
        // 获取所有年级单元
        var allUnits = await _context.GradeUnits
            .OrderBy(g => g.Grade)
            .ThenBy(g => g.Semester)
            .ThenBy(g => g.UnitNo)
            .ToListAsync(cancellationToken);

        // 按年级和学期分组
        var gradeTree = allUnits
            .GroupBy(g => new { g.Grade, g.Semester })
            .Select(g => new GradeTreeNode
            {
                Grade = g.Key.Grade,
                Semester = g.Key.Semester,
                Label = $"{g.Key.Grade} 年级 {g.Key.Semester}",
                Units = g.Select(u => new GradeUnitTreeNode
                {
                    Id = u.Id,
                    Label = u.UnitName,
                    Grade = u.Grade,
                    Semester = u.Semester,
                    UnitNo = u.UnitNo,
                    WordCount = u.Words.Count,
                    LearnedWordCount = 0,
                    Status = "not_started"
                }).ToList()
            })
            .ToList();

        // 获取用户的学习进度
        var userProgress = await _context.LearningProgresses
            .Where(p => p.UserId == userId && p.ContentType == "word")
            .GroupBy(p => p.GradeUnitId)
            .Select(g => new
            {
                GradeUnitId = g.Key,
                LearnedCount = g.Count(p => p.Status == "completed"),
                IsStarted = g.Any(p => p.Status != "not_started"),
                IsCompleted = g.All(p => p.Status == "completed") && g.Count(p => p.Status == "completed") > 0
            })
            .ToDictionaryAsync(x => x.GradeUnitId, x => x, cancellationToken);

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
                }
            }
        }

        return gradeTree;
    }
}
