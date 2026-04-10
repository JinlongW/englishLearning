using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Constants;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 语法服务实现
/// </summary>
public class GrammarService : IGrammarService
{
    private readonly AppDbContext _context;
    private readonly IPointsService _pointsService;

    public GrammarService(AppDbContext context, IPointsService pointsService)
    {
        _context = context;
        _pointsService = pointsService;
    }

    /// <summary>
    /// 获取语法树形结构
    /// </summary>
    public async Task<List<GrammarTreeNode>> GetGrammarTreeAsync(Guid userId, int grade)
    {
        // 获取该年级的所有语法点
        var grammars = await _context.Grammars
            .Include(g => g.GradeUnit)
            .Where(g => g.GradeUnit.Grade == grade)
            .OrderBy(g => g.SortOrder)
            .ToListAsync();

        if (grammars.Count == 0)
        {
            return new List<GrammarTreeNode>();
        }

        // 获取用户学习进度
        var progressDict = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "grammar" &&
                        grammars.Select(g => g.Id).Contains(lp.ContentId))
            .ToDictionaryAsync(lp => lp.ContentId);

        // 将 Grammar 转换为 GrammarTreeNode
        var nodeDict = new Dictionary<Guid, GrammarTreeNode>();
        foreach (var grammar in grammars)
        {
            progressDict.TryGetValue(grammar.Id, out var progress);
            var status = DetermineStatus(progress, grammar.PrerequisiteId, grammars, progressDict);

            nodeDict[grammar.Id] = new GrammarTreeNode
            {
                Id = grammar.Id,
                Title = grammar.Title,
                Description = grammar.ContentType,
                Level = !string.IsNullOrEmpty(grammar.DependencyLevel) ? int.Parse(grammar.DependencyLevel) : 0,
                Category = grammar.Category,
                Status = status,
                PrerequisiteId = grammar.PrerequisiteId,
                Children = new List<GrammarTreeNode>()
            };
        }

        // 构建树形结构
        var roots = new List<GrammarTreeNode>();
        foreach (var grammar in grammars)
        {
            var node = nodeDict[grammar.Id];
            if (grammar.PrerequisiteId.HasValue && nodeDict.ContainsKey(grammar.PrerequisiteId.Value))
            {
                nodeDict[grammar.PrerequisiteId.Value].Children.Add(node);
            }
            else
            {
                roots.Add(node);
            }
        }

        return roots;
    }

    /// <summary>
    /// 确定节点状态
    /// </summary>
    private static string DetermineStatus(
        LearningProgress? progress,
        Guid? prerequisiteId,
        List<Grammar> grammars,
        Dictionary<Guid, LearningProgress> progressDict)
    {
        if (progress != null && progress.Status == "completed")
        {
            return "completed";
        }

        if (progress != null && progress.Status == "learning")
        {
            return "learning";
        }

        // 检查前置条件是否完成
        if (prerequisiteId.HasValue)
        {
            progressDict.TryGetValue(prerequisiteId.Value, out var prereqProgress);
            if (prereqProgress == null || prereqProgress.Status != "completed")
            {
                return "locked";
            }
        }

        return "available";
    }

    /// <summary>
    /// 获取语法列表
    /// </summary>
    public async Task<List<GrammarDto>> GetGrammarsAsync(Guid gradeUnitId, Guid userId)
    {
        var grammars = await _context.Grammars
            .Where(g => g.GradeUnitId == gradeUnitId)
            .OrderBy(g => g.SortOrder)
            .ToListAsync();

        // 获取用户学习进度
        var progressDict = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "grammar" &&
                        grammars.Select(g => g.Id).Contains(lp.ContentId))
            .ToDictionaryAsync(lp => lp.ContentId);

        return grammars.Select(g =>
        {
            progressDict.TryGetValue(g.Id, out var progress);
            // 根据前置条件确定状态
            var status = DetermineGrammarStatus(progress, g.PrerequisiteId, progressDict);

            return new GrammarDto
            {
                Id = g.Id,
                Title = g.Title,
                ContentType = g.ContentType,
                DurationSeconds = g.DurationSeconds,
                SortOrder = g.SortOrder,
                PassingScore = g.PassingScore,
                Status = status,
                Score = progress?.Score
            };
        }).ToList();
    }

    /// <summary>
    /// 确定语法课程状态
    /// </summary>
    private static string DetermineGrammarStatus(
        LearningProgress? progress,
        Guid? prerequisiteId,
        Dictionary<Guid, LearningProgress> progressDict)
    {
        if (progress != null && progress.Status == "completed")
        {
            return "completed";
        }

        if (progress != null && progress.Status == "learning")
        {
            return "learning";
        }

        // 检查前置条件是否完成
        if (prerequisiteId.HasValue)
        {
            progressDict.TryGetValue(prerequisiteId.Value, out var prereqProgress);
            if (prereqProgress == null || prereqProgress.Status != "completed")
            {
                return "locked";
            }
        }

        // 没有前置条件或前置条件已完成，课程可用
        return "available";
    }

    /// <summary>
    /// 获取语法详情
    /// </summary>
    public async Task<GrammarDetailDto?> GetGrammarByIdAsync(Guid grammarId, Guid userId)
    {
        var grammar = await _context.Grammars
            .FirstOrDefaultAsync(g => g.Id == grammarId);

        if (grammar == null)
        {
            return null;
        }

        // 获取用户学习进度
        var progress = await _context.LearningProgresses
            .FirstOrDefaultAsync(lp => lp.UserId == userId && lp.ContentType == "grammar" && lp.ContentId == grammarId);

        return new GrammarDetailDto
        {
            Id = grammar.Id,
            Title = grammar.Title,
            ContentType = grammar.ContentType,
            DurationSeconds = grammar.DurationSeconds,
            SortOrder = grammar.SortOrder,
            PassingScore = grammar.PassingScore,
            Status = progress?.Status ?? "not_started",
            Score = progress?.Score,
            ContentJson = grammar.ContentJson,
            QuizJson = grammar.QuizJson
        };
    }

    /// <summary>
    /// 提交语法测验
    /// </summary>
    public async Task<(int score, bool isPassed, int correctCount, int totalCount, int pointsEarned)> SubmitGrammarQuizAsync(
        Guid grammarId, Guid userId, List<QuizAnswerRequest> answers)
    {
        var grammar = await _context.Grammars.FirstOrDefaultAsync(g => g.Id == grammarId);
        if (grammar == null)
        {
            throw new BusinessException("语法课程不存在", 404);
        }

        int correctCount = 0;
        int totalCount = answers.Count;

        // 比对答案
        foreach (var answer in answers)
        {
            var question = await _context.Questions.FirstOrDefaultAsync(q => q.Id == answer.QuestionId);
            if (question != null && string.Equals(answer.UserAnswer, question.CorrectAnswer, StringComparison.OrdinalIgnoreCase))
            {
                correctCount++;
            }
        }

        int score = (int)(correctCount * 100.0 / totalCount);
        bool isPassed = score >= grammar.PassingScore;
        int pointsEarned = 0;

        // 更新学习进度
        var progress = await _context.LearningProgresses
            .FirstOrDefaultAsync(lp => lp.UserId == userId && lp.ContentType == "grammar" && lp.ContentId == grammarId);

        if (progress == null)
        {
            progress = new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                GradeUnitId = grammar.GradeUnitId,
                ContentType = "grammar",
                ContentId = grammarId,
                CreatedAt = DateTime.Now
            };
            await _context.LearningProgresses.AddAsync(progress);
        }

        progress.Status = isPassed ? "completed" : "learning";
        progress.Score = score;
        progress.AttemptsCount++;
        progress.LastAttemptAt = DateTime.Now;
        progress.UpdatedAt = DateTime.Now;

        if (isPassed)
        {
            progress.CompletedAt = DateTime.Now;
            pointsEarned = PointRules.GrammarLevelComplete;
            await _pointsService.AddPointsAsync(userId, "points", "grammar_complete", pointsEarned, "语法课程完成", grammarId);
            await _pointsService.AddExpAsync(userId, 10);
        }

        await _context.SaveChangesAsync();

        return (score, isPassed, correctCount, totalCount, pointsEarned);
    }
}
