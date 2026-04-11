using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Constants;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 单词服务实现
/// </summary>
public class WordService : IWordService
{
    private readonly AppDbContext _context;
    private readonly IPointsService _pointsService;

    public WordService(AppDbContext context, IPointsService pointsService)
    {
        _context = context;
        _pointsService = pointsService;
    }

    /// <summary>
    /// 获取单词列表
    /// </summary>
    public async Task<PageResult<WordDetailResponse>> GetWordsAsync(Guid gradeUnitId, Guid userId, int page, int pageSize)
    {
        var query = _context.Words
            .Where(w => w.GradeUnitId == gradeUnitId)
            .OrderBy(w => w.SortOrder);

        var total = await query.CountAsync();
        var words = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        // 获取用户的学习进度
        var progressDict = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "word" && words.Select(w => w.Id).Contains(lp.ContentId))
            .ToDictionaryAsync(lp => lp.ContentId);

        var result = words.Select(word =>
        {
            var progress = progressDict.TryGetValue(word.Id, out var p) ? p : null;
            return new WordDetailResponse
            {
                Id = word.Id,
                WordText = word.WordText,
                PhoneticUk = word.PhoneticUk ?? "",
                PhoneticUs = word.PhoneticUs ?? "",
                AudioUrl = word.AudioUrl,
                MeaningCn = word.MeaningCn,
                PartOfSpeech = word.PartOfSpeech,
                ExampleEn = word.ExampleEn,
                ExampleCn = word.ExampleCn,
                ImageUrl = word.ImageUrl,
                Status = progress?.Status ?? "not_started",
                Score = progress?.Score
            };
        }).ToList();

        return PageResult<WordDetailResponse>.Create(result, total, page, pageSize);
    }

    /// <summary>
    /// 获取单词详情
    /// </summary>
    public async Task<WordDetailResponse?> GetWordByIdAsync(Guid wordId, Guid userId)
    {
        var word = await _context.Words.FindAsync(wordId);
        if (word == null)
        {
            return null;
        }

        // 获取用户学习进度
        var progress = await _context.LearningProgresses
            .FirstOrDefaultAsync(lp => lp.UserId == userId && lp.ContentType == "word" && lp.ContentId == wordId);

        return new WordDetailResponse
        {
            Id = word.Id,
            WordText = word.WordText,
            PhoneticUk = word.PhoneticUk ?? "",
            PhoneticUs = word.PhoneticUs ?? "",
            AudioUrl = word.AudioUrl,
            MeaningCn = word.MeaningCn,
            PartOfSpeech = word.PartOfSpeech,
            ExampleEn = word.ExampleEn,
            ExampleCn = word.ExampleCn,
            ImageUrl = word.ImageUrl,
            Status = progress?.Status ?? "not_started",
            Score = progress?.Score
        };
    }

    /// <summary>
    /// 更新单词学习进度
    /// </summary>
    public async Task<(int pointsEarned, int expEarned, bool levelUp)> UpdateWordProgressAsync(Guid wordId, Guid userId, int score, string status)
    {
        var word = await _context.Words.FindAsync(wordId);
        if (word == null)
        {
            throw new BusinessException("单词不存在", 404);
        }

        // 获取或创建学习进度
        var progress = await _context.LearningProgresses
            .FirstOrDefaultAsync(lp => lp.UserId == userId && lp.ContentType == "word" && lp.ContentId == wordId);

        bool isNewCompletion = false;
        if (progress == null)
        {
            progress = new LearningProgress
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                GradeUnitId = word.GradeUnitId,
                ContentType = "word",
                ContentId = wordId,
                CreatedAt = DateTime.Now
            };
            await _context.LearningProgresses.AddAsync(progress);
            isNewCompletion = true;

            // 使用 SaveChangesAsync 插入新记录（INSERT 不受触发器影响）
            await _context.SaveChangesAsync();
        }
        else
        {
            // 使用 ExecuteSqlRawAsync 避免 EF Core 的 OUTPUT 子句与 SQL Server 触发器冲突
            var now = DateTime.Now;
            var attemptsCount = progress.AttemptsCount + 1;
            var completedAt = (status == "completed" || status == "mastered") ? now : (DateTime?)null;

            var completedAtParam = new Microsoft.Data.SqlClient.SqlParameter("@completed_at", completedAt ?? (object)DBNull.Value);

            var rowsAffected = await _context.Database.ExecuteSqlRawAsync(
                @"UPDATE tb_learning_progress SET status = @status, score = @score, attempts_count = @attempts_count, last_attempt_at = @last_attempt_at, updated_at = @updated_at, completed_at = @completed_at WHERE id = @id",
                new Microsoft.Data.SqlClient.SqlParameter("@status", status),
                new Microsoft.Data.SqlClient.SqlParameter("@score", score),
                new Microsoft.Data.SqlClient.SqlParameter("@attempts_count", attemptsCount),
                new Microsoft.Data.SqlClient.SqlParameter("@last_attempt_at", now),
                new Microsoft.Data.SqlClient.SqlParameter("@updated_at", now),
                completedAtParam,
                new Microsoft.Data.SqlClient.SqlParameter("@id", progress.Id));

            // 验证更新是否成功
            if (rowsAffected == 0)
            {
                throw new BusinessException("更新学习进度失败", 500);
            }

            // 更新内存中的实体以保持一致性
            progress.Status = status;
            progress.Score = score;
            progress.AttemptsCount = attemptsCount;
            progress.LastAttemptAt = now;
            progress.UpdatedAt = now;
            progress.CompletedAt = completedAt;

            // 注意：ExecuteSqlRawAsync 已经直接执行了 SQL UPDATE，不需要再调用 SaveChangesAsync
            // 但需要清除 EF Core 的 change tracking，避免后续操作冲突
            _context.Entry(progress).State = EntityState.Detached;
        }

        // 计算奖励
        int pointsEarned = 0;
        int expEarned = 0;
        bool levelUp = false;

        if (isNewCompletion && score >= 60)
        {
            // 首次完成奖励
            pointsEarned = PointRules.WordLevelComplete;
            expEarned = 5;

            // 检查升级
            levelUp = await _pointsService.AddExpAsync(userId, expEarned);
        }

        if (score == 100)
        {
            // 满分额外奖励
            pointsEarned += PointRules.PerfectScoreBonus;
        }

        // 记录积分
        if (pointsEarned > 0)
        {
            await _pointsService.AddPointsAsync(userId, "points", "word_complete", pointsEarned, "单词学习完成", wordId);
        }

        return (pointsEarned, expEarned, levelUp);
    }

    /// <summary>
    /// 获取单词分页列表（管理员）
    /// </summary>
    public async Task<PageResult<WordDetailResponse>> GetPagedByGradeUnitAsync(Guid gradeUnitId, int page, int pageSize, CancellationToken cancellationToken = default)
    {
        var query = _context.Words
            .Where(w => w.GradeUnitId == gradeUnitId)
            .OrderBy(w => w.SortOrder);

        var total = await query.CountAsync(cancellationToken);
        var words = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(cancellationToken);

        var result = words
            .Select(word => new WordDetailResponse
            {
                Id = word.Id,
                WordText = word.WordText,
                PhoneticUk = word.PhoneticUk ?? "",
                PhoneticUs = word.PhoneticUs ?? "",
                AudioUrl = word.AudioUrl,
                MeaningCn = word.MeaningCn,
                PartOfSpeech = word.PartOfSpeech,
                ExampleEn = word.ExampleEn,
                ExampleCn = word.ExampleCn,
                ImageUrl = word.ImageUrl,
                SortOrder = word.SortOrder
            })
            .ToList();

        return PageResult<WordDetailResponse>.Create(result, total, page, pageSize);
    }

    /// <summary>
    /// 获取单词详情（管理员）
    /// </summary>
    public async Task<WordDetailResponse?> GetWordByIdForAdminAsync(Guid wordId, CancellationToken cancellationToken = default)
    {
        var word = await _context.Words.FindAsync([wordId], cancellationToken);
        if (word == null)
        {
            return null;
        }

        return new WordDetailResponse
        {
            Id = word.Id,
            WordText = word.WordText,
            PhoneticUk = word.PhoneticUk ?? "",
            PhoneticUs = word.PhoneticUs ?? "",
            AudioUrl = word.AudioUrl,
            MeaningCn = word.MeaningCn,
            PartOfSpeech = word.PartOfSpeech,
            ExampleEn = word.ExampleEn,
            ExampleCn = word.ExampleCn,
            ImageUrl = word.ImageUrl,
            SortOrder = word.SortOrder
        };
    }

    /// <summary>
    /// 创建单词
    /// </summary>
    public async Task<WordDetailResponse> CreateWordAsync(CreateWordRequest request, CancellationToken cancellationToken = default)
    {
        // 验证年级单元是否存在
        var gradeUnitExists = await _context.GradeUnits.AnyAsync(g => g.Id == request.GradeUnitId, cancellationToken);
        if (!gradeUnitExists)
        {
            throw new BusinessException("指定的年级单元不存在", 400);
        }

        var word = new Word
        {
            Id = Guid.NewGuid(),
            GradeUnitId = request.GradeUnitId,
            WordText = request.WordText,
            PhoneticUk = request.PhoneticUk,
            PhoneticUs = request.PhoneticUs,
            AudioUrl = request.AudioUrl,
            MeaningCn = request.MeaningCn,
            PartOfSpeech = request.PartOfSpeech,
            ExampleEn = request.ExampleEn,
            ExampleCn = request.ExampleCn,
            ImageUrl = request.ImageUrl,
            SortOrder = request.SortOrder
        };

        _context.Words.Add(word);
        await _context.SaveChangesAsync(cancellationToken);

        return new WordDetailResponse
        {
            Id = word.Id,
            WordText = word.WordText,
            PhoneticUk = word.PhoneticUk ?? "",
            PhoneticUs = word.PhoneticUs ?? "",
            AudioUrl = word.AudioUrl,
            MeaningCn = word.MeaningCn,
            PartOfSpeech = word.PartOfSpeech,
            ExampleEn = word.ExampleEn,
            ExampleCn = word.ExampleCn,
            ImageUrl = word.ImageUrl,
            SortOrder = word.SortOrder
        };
    }

    /// <summary>
    /// 更新单词
    /// </summary>
    public async Task<bool> UpdateWordAsync(Guid wordId, UpdateWordRequest request, CancellationToken cancellationToken = default)
    {
        var word = await _context.Words.FindAsync([wordId], cancellationToken);
        if (word == null)
        {
            return false;
        }

        // 验证年级单元是否存在
        var gradeUnitExists = await _context.GradeUnits.AnyAsync(g => g.Id == request.GradeUnitId, cancellationToken);
        if (!gradeUnitExists)
        {
            throw new BusinessException("指定的年级单元不存在", 400);
        }

        word.WordText = request.WordText;
        word.PhoneticUk = request.PhoneticUk;
        word.PhoneticUs = request.PhoneticUs;
        word.AudioUrl = request.AudioUrl;
        word.MeaningCn = request.MeaningCn;
        word.PartOfSpeech = request.PartOfSpeech;
        word.ExampleEn = request.ExampleEn;
        word.ExampleCn = request.ExampleCn;
        word.ImageUrl = request.ImageUrl;
        word.SortOrder = request.SortOrder;
        word.GradeUnitId = request.GradeUnitId;

        await _context.SaveChangesAsync(cancellationToken);
        return true;
    }

    /// <summary>
    /// 删除单词
    /// </summary>
    public async Task<bool> DeleteWordAsync(Guid wordId, CancellationToken cancellationToken = default)
    {
        var word = await _context.Words.FindAsync([wordId], cancellationToken);
        if (word == null)
        {
            return false;
        }

        _context.Words.Remove(word);
        await _context.SaveChangesAsync(cancellationToken);
        return true;
    }

    /// <summary>
    /// 艾宾浩斯复习间隔（分钟）
    /// </summary>
    private static readonly int[] EbbinghausIntervals = [5, 30, 12 * 60, 24 * 60, 3 * 24 * 60, 7 * 24 * 60];

    /// <summary>
    /// 获取需要复习的单词列表（基于艾宾浩斯记忆曲线）
    /// </summary>
    public async Task<List<WordReviewDto>> GetWordsDueForReviewAsync(Guid userId, int limit = 20)
    {
        var now = DateTime.Now;

        // 查询已完成学习的单词（有学习进度的）
        var learnedProgresses = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "word" && lp.Status == "completed")
            .ToListAsync();

        var wordIds = learnedProgresses.Select(lp => lp.ContentId).ToList();
        if (!wordIds.Any())
        {
            return new List<WordReviewDto>();
        }

        // 获取单词详情
        var words = await _context.Words
            .Where(w => wordIds.Contains(w.Id))
            .ToDictionaryAsync(w => w.Id);

        var result = new List<WordReviewDto>();

        foreach (var progress in learnedProgresses)
        {
            if (!words.TryGetValue(progress.ContentId, out var word))
            {
                continue;
            }

            // 计算下次复习时间
            var reviewCount = progress.AttemptsCount - 1; // 已复习次数
            DateTime nextReviewAt;

            if (reviewCount < 0)
            {
                reviewCount = 0;
            }

            if (reviewCount >= EbbinghausIntervals.Length)
            {
                // 已掌握，跳过
                continue;
            }

            // 根据最后复习时间和复习次数计算下次复习时间
            var lastReviewAt = progress.LastAttemptAt ?? progress.CreatedAt;
            var intervalMinutes = EbbinghausIntervals[reviewCount];
            nextReviewAt = lastReviewAt.AddMinutes(intervalMinutes);

            // 检查是否到期（未来 24 小时内或已过期）
            var threshold = now.AddHours(24);
            if (nextReviewAt <= threshold)
            {
                result.Add(new WordReviewDto
                {
                    Id = word.Id,
                    WordText = word.WordText,
                    MeaningCn = word.MeaningCn,
                    ReviewCount = reviewCount,
                    NextReviewAt = nextReviewAt,
                    IsUrgent = nextReviewAt <= now // 已过期或即将到期
                });
            }
        }

        // 按紧急程度排序：优先返回已过期的，然后是按下次复习时间排序
        return result
            .OrderBy(x => x.IsUrgent ? 0 : 1)
            .ThenBy(x => x.NextReviewAt)
            .Take(limit)
            .ToList();
    }

    /// <summary>
    /// 获取一周复习计划
    /// </summary>
    public async Task<List<ReviewScheduleDto>> GetReviewScheduleAsync(Guid userId)
    {
        var now = DateTime.Now;
        var today = new DateTime(now.Year, now.Month, now.Day);

        // 查询已完成学习的单词
        var learnedProgresses = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "word" && lp.Status == "completed")
            .ToListAsync();

        var wordIds = learnedProgresses.Select(lp => lp.ContentId).ToList();
        if (!wordIds.Any())
        {
            return new List<ReviewScheduleDto>();
        }

        // 获取单词详情
        var words = await _context.Words
            .Where(w => wordIds.Contains(w.Id))
            .ToDictionaryAsync(w => w.Id);

        // 初始化 7 天的计划
        var scheduleDict = new Dictionary<DateTime, List<WordReviewDto>>();
        for (int i = 0; i < 7; i++)
        {
            scheduleDict[today.AddDays(i)] = new List<WordReviewDto>();
        }

        foreach (var progress in learnedProgresses)
        {
            if (!words.TryGetValue(progress.ContentId, out var word))
            {
                continue;
            }

            var reviewCount = progress.AttemptsCount - 1;
            if (reviewCount < 0)
            {
                reviewCount = 0;
            }

            if (reviewCount >= EbbinghausIntervals.Length)
            {
                // 已掌握
                continue;
            }

            // 计算下次复习时间
            var lastReviewAt = progress.LastAttemptAt ?? progress.CreatedAt;
            var intervalMinutes = EbbinghausIntervals[reviewCount];
            var nextReviewAt = lastReviewAt.AddMinutes(intervalMinutes);

            // 分配到最近的日期
            var reviewDate = new DateTime(nextReviewAt.Year, nextReviewAt.Month, nextReviewAt.Day);
            var daysFromToday = (reviewDate - today).Days;

            if (daysFromToday >= 0 && daysFromToday < 7)
            {
                scheduleDict[reviewDate].Add(new WordReviewDto
                {
                    Id = word.Id,
                    WordText = word.WordText,
                    MeaningCn = word.MeaningCn,
                    ReviewCount = reviewCount,
                    NextReviewAt = nextReviewAt,
                    IsUrgent = nextReviewAt <= now
                });
            }
        }

        // 转换为 DTO 列表
        return scheduleDict
            .Select(kvp => new ReviewScheduleDto
            {
                Date = kvp.Key,
                WordCount = kvp.Value.Count,
                PreviewWords = kvp.Value.Take(5).Select(w => w.WordText).ToList()
            })
            .OrderBy(x => x.Date)
            .ToList();
    }
}
