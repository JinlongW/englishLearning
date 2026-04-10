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
/// 用户服务实现
/// </summary>
public class UserService : IUserService
{
    private readonly AppDbContext _context;
    private readonly IBadgeService _badgeService;
    private readonly IQuestionService _questionService;

    public UserService(AppDbContext context, IBadgeService badgeService, IQuestionService questionService)
    {
        _context = context;
        _badgeService = badgeService;
        _questionService = questionService;
    }

    /// <summary>
    /// 获取学习统计
    /// </summary>
    public async Task<LearningSummaryResponse> GetLearningSummaryAsync(Guid userId)
    {
        // 使用单个查询获取用户基本信息和学习统计
        var user = await _context.Users
            .Include(u => u.Profile)
            .Include(u => u.Level)
            .FirstOrDefaultAsync(u => u.Id == userId);

        if (user == null)
        {
            throw new BusinessException("用户不存在", 404);
        }

        // 顺序执行统计查询（避免并发访问 DbContext）
        var stats = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId)
            .GroupBy(lp => lp.ContentType)
            .Select(g => new { ContentType = g.Key, CompletedCount = g.Count(lp => lp.Status == "completed") })
            .ToListAsync();

        var wordsLearned = stats.FirstOrDefault(s => s.ContentType == "word")?.CompletedCount ?? 0;
        var grammarsCompleted = stats.FirstOrDefault(s => s.ContentType == "grammar")?.CompletedCount ?? 0;

        var challengesCompleted = await _context.DailyChallenges
            .Where(dc => dc.UserId == userId && dc.Status == "completed")
            .CountAsync();

        var wrongQuestionCount = await _context.WrongQuestions
            .Where(wq => wq.UserId == userId && !wq.IsDeleted && wq.ReviewStatus != "mastered")
            .CountAsync();

        var points = await _context.UserPoints
            .Where(p => p.UserId == userId)
            .GroupBy(p => p.PointsType)
            .Select(g => new { PointsType = g.Key, Total = g.Sum(p => p.ChangeAmount) })
            .ToListAsync();

        var totalPoints = points.FirstOrDefault(p => p.PointsType == "points")?.Total ?? 0;
        var totalCoins = points.FirstOrDefault(p => p.PointsType == "coins")?.Total ?? 0;

        return new LearningSummaryResponse
        {
            TotalLearningDays = user.Profile?.TotalLearningDays ?? 0,
            CurrentStreak = user.Profile?.CurrentStreak ?? 0,
            MaxStreak = user.Profile?.MaxStreak ?? 0,
            WordsLearned = wordsLearned,
            GrammarsCompleted = grammarsCompleted,
            ChallengesCompleted = challengesCompleted,
            WrongQuestionCount = wrongQuestionCount,
            TotalPoints = totalPoints,
            TotalCoins = totalCoins,
            CurrentLevel = user.Level?.CurrentLevel ?? 1,
            LevelName = user.Level?.LevelName ?? "英语小白"
        };
    }

    /// <summary>
    /// 获取徽章列表
    /// </summary>
    public async Task<List<BadgeDto>> GetBadgesAsync(Guid userId)
    {
        // 获取所有徽章
        var allBadges = await _context.Badges
            .Where(b => b.IsActive)
            .OrderBy(b => b.SortOrder)
            .ToListAsync();

        // 获取用户已获得的徽章
        var userBadges = await _context.UserBadges
            .Where(ub => ub.UserId == userId)
            .ToListAsync();

        var userBadgeIds = userBadges.Select(ub => ub.BadgeId).ToHashSet();

        // 合并数据
        var result = allBadges.Select(badge => new BadgeDto
        {
            Id = badge.Id,
            BadgeCode = badge.BadgeCode,
            BadgeName = badge.BadgeName,
            BadgeType = badge.BadgeType,
            Description = badge.Description,
            BadgeIcon = badge.BadgeIcon,
            IsEarned = userBadgeIds.Contains(badge.Id),
            IsNew = userBadges.FirstOrDefault(ub => ub.BadgeId == badge.Id)?.IsNew ?? false,
            EarnedAt = userBadges.FirstOrDefault(ub => ub.BadgeId == badge.Id)?.EarnedAt
        }).ToList();

        return result;
    }

    /// <summary>
    /// 获取积分记录
    /// </summary>
    public async Task<PageResult<UserPoints>> GetPointsHistoryAsync(Guid userId, int page, int pageSize)
    {
        var query = _context.UserPoints
            .Where(p => p.UserId == userId)
            .OrderByDescending(p => p.CreatedAt);

        var total = await query.CountAsync();
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return PageResult<UserPoints>.Create(items, total, page, pageSize);
    }

    /// <summary>
    /// 每日签到
    /// </summary>
    public async Task<(int pointsEarned, int streakDays, int bonusPoints)> CheckInAsync(Guid userId)
    {
        var today = DateTime.Today;

        // 检查今天是否已签到
        var existingCheckin = await _context.Checkins
            .FirstOrDefaultAsync(c => c.UserId == userId && c.CheckinDate == today);

        if (existingCheckin != null)
        {
            throw new BusinessException("今天已签到", 1006);
        }

        // 获取昨天签到记录
        var yesterday = today.AddDays(-1);
        var yesterdayCheckin = await _context.Checkins
            .FirstOrDefaultAsync(c => c.UserId == userId && c.CheckinDate == yesterday);

        // 获取用户画像
        var user = await _context.Users
            .Include(u => u.Profile)
            .FirstOrDefaultAsync(u => u.Id == userId);

        if (user == null)
        {
            throw new BusinessException("用户不存在", 404);
        }

        // 计算连续天数
        int streakDays;
        if (yesterdayCheckin != null)
        {
            streakDays = user.Profile!.CurrentStreak + 1;
        }
        else
        {
            // 检查之前的连续天数是否要重置
            var lastCheckin = await _context.Checkins
                .Where(c => c.UserId == userId && c.CheckinDate < today)
                .OrderByDescending(c => c.CheckinDate)
                .FirstOrDefaultAsync();

            if (lastCheckin != null && lastCheckin.CheckinDate < yesterday)
            {
                streakDays = 1; // 中断了，重新开始
            }
            else
            {
                streakDays = user.Profile?.CurrentStreak + 1 ?? 1;
            }
        }

        // 计算基础积分
        int pointsEarned = PointRules.SignIn;
        int bonusPoints = 0;

        // 连续奖励
        if (streakDays == 7)
        {
            bonusPoints = PointRules.StreakBonus7Days;
        }
        else if (streakDays == 30)
        {
            bonusPoints = PointRules.StreakBonus30Days;
        }
        else if (streakDays % 7 == 0)
        {
            bonusPoints = PointRules.StreakBonus7Days; // 每 7 天奖励
        }

        // 使用事务确保数据一致性
        using var transaction = await _context.Database.BeginTransactionAsync();
        try
        {
            // 创建签到记录
            var now = DateTime.UtcNow;
            var checkin = new Checkin
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                CheckinDate = today,
                PointsEarned = pointsEarned,
                StreakDays = streakDays,
                BonusPoints = bonusPoints,
                CreatedAt = now
            };
            await _context.Checkins.AddAsync(checkin);

            // 更新用户画像
            if (user.Profile != null)
            {
                user.Profile.CurrentStreak = streakDays;
                if (streakDays > user.Profile.MaxStreak)
                {
                    user.Profile.MaxStreak = streakDays;
                }
                user.Profile.TotalLearningDays++;
            }

            // 记录积分
            await AddPointsAsync(userId, "points", "signin", pointsEarned + bonusPoints, "每日签到", checkin.Id);
            await AddPointsAsync(userId, "coins", "signin", PointRules.SignIn, "每日签到奖励", checkin.Id);

            await _context.SaveChangesAsync();
            await transaction.CommitAsync();
        }
        catch
        {
            await transaction.RollbackAsync();
            throw;
        }

        // 检查徽章
        await _badgeService.CheckAndAwardBadgesAsync(userId, "checkin", new { streakDays = streakDays });

        return (pointsEarned + bonusPoints, streakDays, bonusPoints);
    }

    /// <summary>
    /// 获取每日打卡题目（5道题）
    /// </summary>
    public async Task<List<QuestionDetailResponse>> GetDailyCheckinQuestionsAsync(Guid userId)
    {
        // 获取 5 道题用于每日打卡，复用挑战的智能组卷策略
        return await _questionService.GetQuestionsForChallengeAsync(userId, 5);
    }

    /// <summary>
    /// 检查今天是否已打卡
    /// </summary>
    public async Task<bool> HasCheckedInTodayAsync(Guid userId, CancellationToken cancellationToken = default)
    {
        var today = DateTime.Today;
        return await _context.Checkins
            .AnyAsync(c => c.UserId == userId && c.CheckinDate == today, cancellationToken);
    }

    /// <summary>
    /// 添加积分记录
    /// </summary>
    private async Task AddPointsAsync(Guid userId, string pointsType, string changeType, int amount, string description, Guid referenceId)
    {
        var balance = await _context.UserPoints
            .Where(p => p.UserId == userId && p.PointsType == pointsType)
            .SumAsync(p => p.ChangeAmount);

        var record = new UserPoints
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            PointsType = pointsType,
            ChangeType = changeType,
            ChangeAmount = amount,
            BalanceAfter = balance + amount,
            Description = description,
            ReferenceId = referenceId,
            CreatedAt = DateTime.UtcNow
        };

        await _context.UserPoints.AddAsync(record);
    }
}
