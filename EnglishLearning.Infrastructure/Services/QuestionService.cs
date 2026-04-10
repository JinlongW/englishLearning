using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 题目服务实现
/// </summary>
public class QuestionService : IQuestionService
{
    private const int PointsPerCorrectAnswer = 5;
    private const int ExpPerCorrectAnswer = 2;

    private readonly AppDbContext _context;
    private readonly IPointsService _pointsService;
    private readonly IWrongQuestionService _wrongQuestionService;

    public QuestionService(
        AppDbContext context,
        IPointsService pointsService,
        IWrongQuestionService wrongQuestionService)
    {
        _context = context;
        _pointsService = pointsService;
        _wrongQuestionService = wrongQuestionService;
    }

    /// <summary>
    /// 获取题目详情
    /// </summary>
    public async Task<QuestionDetailResponse?> GetQuestionByIdAsync(Guid questionId, CancellationToken cancellationToken = default)
    {
        var question = await _context.Questions
            .Include(q => q.Options)
            .FirstOrDefaultAsync(q => q.Id == questionId, cancellationToken);

        if (question == null || !question.IsActive)
        {
            return null;
        }

        return new QuestionDetailResponse
        {
            Id = question.Id,
            QuestionType = question.QuestionType,
            Difficulty = question.Difficulty,
            QuestionStem = question.QuestionStem,
            StemAudioUrl = question.StemAudioUrl,
            Options = question.Options
                .OrderBy(o => o.SortOrder)
                .Select(o => new QuestionOptionDto
                {
                    Id = o.Id,
                    OptionKey = o.OptionKey,
                    OptionContent = o.OptionContent,
                    ImageUrl = o.ImageUrl,
                    AudioUrl = o.AudioUrl
                }).ToList()
        };
    }

    /// <summary>
    /// 提交答案
    /// </summary>
    public async Task<AnswerResultResponse> SubmitAnswerAsync(Guid questionId, Guid userId, string? userAnswer, int timeUsedSeconds, CancellationToken cancellationToken = default)
    {
        var question = await _context.Questions
            .FirstOrDefaultAsync(q => q.Id == questionId, cancellationToken);

        if (question == null || !question.IsActive)
        {
            throw new BusinessException("题目不存在", 1005);
        }

        // 判断是否正确 - 处理 null 并确保正确的修剪
        bool isCorrect = false;
        if (!string.IsNullOrEmpty(userAnswer) && !string.IsNullOrEmpty(question.CorrectAnswer))
        {
            isCorrect = string.Equals(
                userAnswer.Trim(),
                question.CorrectAnswer.Trim(),
                StringComparison.OrdinalIgnoreCase
            );
        }

        // 记录错题
        if (!isCorrect && !string.IsNullOrEmpty(userAnswer))
        {
            await _wrongQuestionService.AddAsync(userId, questionId, userAnswer, question.CorrectAnswer);
        }

        // 计算奖励
        int pointsEarned = isCorrect ? PointsPerCorrectAnswer : 0;
        int expEarned = isCorrect ? ExpPerCorrectAnswer : 0;
        bool levelUp = false;

        if (pointsEarned > 0)
        {
            await _pointsService.AddPointsAsync(userId, "points", "question_correct", pointsEarned, "答题正确", questionId);
            levelUp = await _pointsService.AddExpAsync(userId, expEarned);
        }

        return new AnswerResultResponse
        {
            IsCorrect = isCorrect,
            CorrectAnswer = question.CorrectAnswer,
            Analysis = question.AnswerAnalysis ?? "",
            PointsEarned = pointsEarned,
            ExpEarned = expEarned,
            LevelUp = levelUp
        };
    }

    /// <summary>
    /// 获取挑战题目（智能组卷）
    /// </summary>
    public async Task<List<QuestionDetailResponse>> GetQuestionsForChallengeAsync(Guid userId, int count = 10, CancellationToken cancellationToken = default)
    {
        // 获取用户年级
        var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userId, cancellationToken);
        if (user == null)
        {
            throw new BusinessException("用户不存在", 404);
        }

        // 组卷策略：40% 新题 + 30% 错题 + 30% 复习题
        var newQuestionCount = (int)(count * 0.4);
        var wrongQuestionCount = (int)(count * 0.3);
        var reviewQuestionCount = count - newQuestionCount - wrongQuestionCount;

        var selectedQuestions = new List<Question>();

        // 1. 获取错题本中的题目
        var wrongQuestions = await _context.WrongQuestions
            .Where(wq => wq.UserId == userId && !wq.IsDeleted && wq.ReviewStatus != "mastered")
            .OrderBy(wq => wq.NextReviewAt)
            .Take(wrongQuestionCount)
            .Select(wq => wq.Question)
            .ToListAsync(cancellationToken);

        selectedQuestions.AddRange(wrongQuestions);

        // 2. 获取新题（用户未学习过的单元的题目）
        var learnedQuestionIds = await _context.LearningProgresses
            .Where(lp => lp.UserId == userId && lp.ContentType == "question")
            .Select(lp => lp.ContentId)
            .ToListAsync(cancellationToken);

        var newQuestions = await _context.Questions
            .Include(q => q.Options)
            .Where(q => q.GradeUnit.Grade == user.GradeLevel &&
                       q.IsActive &&
                       !learnedQuestionIds.Contains(q.Id) &&
                       !selectedQuestions.Select(sq => sq.Id).Contains(q.Id))
            .OrderBy(q => Guid.NewGuid())
            .Take(newQuestionCount)
            .ToListAsync(cancellationToken);

        selectedQuestions.AddRange(newQuestions);

        // 3. 获取复习题
        var currentCount = selectedQuestions.Count;
        if (currentCount < count)
        {
            var remainingCount = count - currentCount;
            var reviewQuestions = await _context.Questions
                .Include(q => q.Options)
                .Where(q => q.GradeUnit.Grade == user.GradeLevel &&
                           q.IsActive &&
                           !selectedQuestions.Select(sq => sq.Id).Contains(q.Id))
                .OrderBy(q => Guid.NewGuid())
                .Take(remainingCount)
                .ToListAsync(cancellationToken);

            selectedQuestions.AddRange(reviewQuestions);
        }

        // 转换为 DTO
        return selectedQuestions.Select(q => new QuestionDetailResponse
        {
            Id = q.Id,
            QuestionType = q.QuestionType,
            Difficulty = q.Difficulty,
            QuestionStem = q.QuestionStem,
            StemAudioUrl = q.StemAudioUrl,
            Options = q.Options
                .OrderBy(o => o.SortOrder)
                .Select(o => new QuestionOptionDto
                {
                    Id = o.Id,
                    OptionKey = o.OptionKey,
                    OptionContent = o.OptionContent,
                    ImageUrl = o.ImageUrl,
                    AudioUrl = o.AudioUrl
                }).ToList()
        }).ToList();
    }

    /// <summary>
    /// 批量获取题目详情
    /// </summary>
    public async Task<List<QuestionDetailResponse>> GetQuestionDetailsAsync(List<Guid> questionIds, CancellationToken cancellationToken = default)
    {
        var questions = await _context.Questions
            .Include(q => q.Options)
            .Where(q => questionIds.Contains(q.Id) && q.IsActive)
            .OrderBy(q => q.Id)
            .ToListAsync(cancellationToken);

        return questions.Select(q => new QuestionDetailResponse
        {
            Id = q.Id,
            QuestionType = q.QuestionType,
            Difficulty = q.Difficulty,
            QuestionStem = q.QuestionStem,
            StemAudioUrl = q.StemAudioUrl,
            Options = q.Options
                .OrderBy(o => o.SortOrder)
                .Select(o => new QuestionOptionDto
                {
                    Id = o.Id,
                    OptionKey = o.OptionKey,
                    OptionContent = o.OptionContent,
                    ImageUrl = o.ImageUrl,
                    AudioUrl = o.AudioUrl
                }).ToList()
        }).ToList();
    }
}
