using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Constants;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 每日挑战服务实现
/// </summary>
public class ChallengeService : IChallengeService
{
    private readonly AppDbContext _context;
    private readonly IQuestionService _questionService;
    private readonly IPointsService _pointsService;
    private readonly IBadgeService _badgeService;

    public ChallengeService(
        AppDbContext context,
        IQuestionService questionService,
        IPointsService pointsService,
        IBadgeService badgeService)
    {
        _context = context;
        _questionService = questionService;
        _pointsService = pointsService;
        _badgeService = badgeService;
    }

    /// <summary>
    /// 获取今日挑战状态
    /// </summary>
    public async Task<DailyChallengeDto> GetTodayChallengeAsync(Guid userId)
    {
        var today = DateTime.Today;
        var themeInfo = GetDailyTheme(today);

        var challenge = await _context.DailyChallenges
            .FirstOrDefaultAsync(dc => dc.UserId == userId && dc.ChallengeDate == today);

        if (challenge == null)
        {
            return new DailyChallengeDto
            {
                Id = null,
                Date = today,
                Status = "pending",
                IsCompleted = false,
                TotalQuestions = 10,
                CorrectCount = 0,
                Score = 0,
                PointsEarned = 0,
                CoinsEarned = 0,
                Theme = themeInfo.Theme,
                ThemeName = themeInfo.ThemeName,
                ThemeIcon = themeInfo.ThemeIcon,
                BonusMultiplier = themeInfo.BonusMultiplier
            };
        }

        return new DailyChallengeDto
        {
            Id = challenge.Id,
            Date = challenge.ChallengeDate,
            Status = challenge.Status,
            IsCompleted = challenge.Status == "completed",
            TotalQuestions = challenge.TotalQuestions,
            CorrectCount = challenge.CorrectCount,
            Score = challenge.Score,
            PointsEarned = challenge.PointsEarned,
            CoinsEarned = challenge.CoinsEarned,
            Theme = themeInfo.Theme,
            ThemeName = themeInfo.ThemeName,
            ThemeIcon = themeInfo.ThemeIcon,
            BonusMultiplier = themeInfo.BonusMultiplier
        };
    }

    /// <summary>
    /// 根据星期几获取主题日信息
    /// </summary>
    private static (string Theme, string ThemeName, string ThemeIcon, int BonusMultiplier) GetDailyTheme(DateTime date)
    {
        return date.DayOfWeek switch
        {
            DayOfWeek.Monday => ("vocabulary", "单词日", "📝", 1),
            DayOfWeek.Tuesday => ("vocabulary", "单词日", "📚", 1),
            DayOfWeek.Wednesday => ("grammar", "语法日", "📖", 1),
            DayOfWeek.Thursday => ("grammar", "语法日", "📖", 1),
            DayOfWeek.Friday => ("mixed", "综合日", "🎯", 1),
            DayOfWeek.Saturday => ("review", "复习日", "🔄", 1),
            DayOfWeek.Sunday => ("boss", "BOSS 战", "👑", 2),
            _ => ("mixed", "综合日", "🎯", 1)
        };
    }

    /// <summary>
    /// 开始挑战
    /// </summary>
    public async Task<(Guid challengeId, List<QuestionDetailResponse> questions)> StartChallengeAsync(Guid userId)
    {
        var today = DateTime.Today;

        // 检查是否已存在今日挑战
        var existingChallenge = await _context.DailyChallenges
            .Include(dc => dc.Details)
            .FirstOrDefaultAsync(dc => dc.UserId == userId && dc.ChallengeDate == today);

        if (existingChallenge != null)
        {
            if (existingChallenge.Status == "completed")
            {
                throw new BusinessException("今日挑战已完成", 1004);
            }

            // 获取已有题目的详细信息
            var questionIds = existingChallenge.Details.Select(d => d.QuestionId).ToList();
            var existingQuestions = await _questionService.GetQuestionDetailsAsync(questionIds);
            return (existingChallenge.Id, existingQuestions);
        }

        // 创建新挑战
        var challenge = new DailyChallenge
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            ChallengeDate = today,
            Status = "in_progress",
            TotalQuestions = 10,
            CorrectCount = 0,
            Score = 0,
            TimeUsedSeconds = 0,
            PointsEarned = 0,
            CoinsEarned = 0,
            StartedAt = DateTime.Now,
            CreatedAt = DateTime.Now
        };

        await _context.DailyChallenges.AddAsync(challenge);
        await _context.SaveChangesAsync();

        // 获取题目
        var questions = await _questionService.GetQuestionsForChallengeAsync(userId, 10);

        return (challenge.Id, questions);
    }

    /// <summary>
    /// 提交挑战结果
    /// </summary>
    public async Task<ChallengeResultResponse> SubmitChallengeAsync(
        Guid challengeId, Guid userId, List<ChallengeAnswerRequest> answers, int timeUsedSeconds)
    {
        var challenge = await _context.DailyChallenges
            .Include(dc => dc.Details)
            .FirstOrDefaultAsync(dc => dc.Id == challengeId && dc.UserId == userId);

        if (challenge == null)
        {
            throw new BusinessException("挑战不存在", 404);
        }

        if (challenge.Status == "completed")
        {
            throw new BusinessException("挑战已完成", 1004);
        }

        // 使用事务
        using var transaction = await _context.Database.BeginTransactionAsync();

        try
        {
            // 计算结果
            int correctCount = answers.Count(a => a.IsCorrect);
            int score = (int)(correctCount * 10.0 / answers.Count * 100);

            // 更新挑战
            challenge.Status = "completed";
            challenge.CorrectCount = correctCount;
            challenge.Score = score;
            challenge.TimeUsedSeconds = timeUsedSeconds;
            challenge.CompletedAt = DateTime.Now;

            // 计算奖励
            int pointsEarned = PointRules.DailyChallengeComplete;
            int coinsEarned = 20;

            // 满分奖励
            if (score == 100)
            {
                pointsEarned += PointRules.PerfectScoreBonus;
            }

            challenge.PointsEarned = pointsEarned;
            challenge.CoinsEarned = coinsEarned;

            // 保存挑战详情
            foreach (var answer in answers)
            {
                var detail = new DailyChallengeDetail
                {
                    Id = Guid.NewGuid(),
                    DailyChallengeId = challengeId,
                    QuestionId = answer.QuestionId,
                    QuestionOrder = answers.IndexOf(answer) + 1,
                    UserAnswer = answer.UserAnswer,
                    IsCorrect = answer.IsCorrect,
                    TimeUsedSeconds = answer.TimeUsedSeconds,
                    CreatedAt = DateTime.Now
                };
                await _context.DailyChallengeDetails.AddAsync(detail);
            }

            await _context.SaveChangesAsync();

            // 添加积分
            await _pointsService.AddPointsAsync(userId, "points", "daily_challenge", pointsEarned, "完成每日挑战", challengeId);
            await _pointsService.AddPointsAsync(userId, "coins", "daily_challenge", coinsEarned, "完成每日挑战奖励", challengeId);

            // 添加经验
            await _pointsService.AddExpAsync(userId, 20);

            // 更新用户学习天数
            await UpdateLearningDaysAsync(userId);

            await _context.SaveChangesAsync();
            await transaction.CommitAsync();

            // 获取题目详情用于返回
            var questionIds = answers.Select(a => a.QuestionId).ToList();
            var questions = await _context.Questions
                .Where(q => questionIds.Contains(q.Id))
                .ToListAsync();

            var questionResults = answers.Select(a =>
            {
                var q = questions.FirstOrDefault(q => q.Id == a.QuestionId);
                var speedBonus = CalculateSpeedBonus(a.TimeUsedSeconds);
                return new ChallengeQuestionResult
                {
                    QuestionId = a.QuestionId,
                    QuestionStem = q?.QuestionStem ?? "",
                    UserAnswer = a.UserAnswer,
                    CorrectAnswer = a.IsCorrect ? a.UserAnswer : q?.CorrectAnswer ?? "",
                    IsCorrect = a.IsCorrect,
                    TimeUsedSeconds = a.TimeUsedSeconds,
                    SpeedBonus = speedBonus,
                    Analysis = q?.AnswerAnalysis ?? ""
                };
            }).ToList();

            // 检查徽章
            await _badgeService.CheckAndAwardBadgesAsync(userId, "challenge_complete", new
            {
                challengeId = challengeId,
                score = score
            });

            return new ChallengeResultResponse
            {
                Id = challenge.Id,
                TotalQuestions = challenge.TotalQuestions,
                CorrectCount = challenge.CorrectCount,
                Score = challenge.Score,
                TimeUsedSeconds = challenge.TimeUsedSeconds,
                PointsEarned = challenge.PointsEarned,
                CoinsEarned = challenge.CoinsEarned,
                QuestionResults = questionResults
            };
        }
        catch
        {
            await transaction.RollbackAsync();
            throw;
        }
    }

    /// <summary>
    /// 更新学习天数
    /// </summary>
    private async Task UpdateLearningDaysAsync(Guid userId)
    {
        var today = DateTime.Today;

        var user = await _context.Users
            .Include(u => u.Profile)
            .FirstOrDefaultAsync(u => u.Id == userId);

        if (user?.Profile != null)
        {
            // 检查今天是否已增加过学习天数
            var lastCheckin = await _context.Checkins
                .Where(c => c.UserId == userId)
                .OrderByDescending(c => c.CheckinDate)
                .FirstOrDefaultAsync();

            if (lastCheckin == null || lastCheckin.CheckinDate < today)
            {
                user.Profile.TotalLearningDays++;
            }
        }
    }

    /// <summary>
    /// 根据用时计算速答奖励分
    /// 0-5 秒：+10 分
    /// 6-10 秒：+5 分
    /// 11-15 秒：+2 分
    /// 16-30 秒：+0 分
    /// 超时：0 分
    /// </summary>
    private static int CalculateSpeedBonus(int timeUsedSeconds)
    {
        if (timeUsedSeconds > 30)
        {
            return 0; // 超时
        }

        if (timeUsedSeconds <= 5)
        {
            return 10; // 0-5 秒：+10 分
        }

        if (timeUsedSeconds <= 10)
        {
            return 5; // 6-10 秒：+5 分
        }

        if (timeUsedSeconds <= 15)
        {
            return 2; // 11-15 秒：+2 分
        }

        return 0; // 16-30 秒：+0 分
    }
}
