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
/// 错题服务实现
/// </summary>
public class WrongQuestionService : IWrongQuestionService
{
    private readonly AppDbContext _context;

    public WrongQuestionService(AppDbContext context)
    {
        _context = context;
    }

    /// <summary>
    /// 添加错题
    /// </summary>
    public async Task AddAsync(Guid userId, Guid questionId, string userAnswer, string correctAnswer)
    {
        // 检查是否已存在
        var existing = await _context.WrongQuestions
            .FirstOrDefaultAsync(wq => wq.UserId == userId && wq.QuestionId == questionId && !wq.IsDeleted);

        if (existing != null)
        {
            // 更新现有错题
            existing.UserAnswer = userAnswer;
            existing.LastReviewAt = DateTime.Now;
            existing.ReviewCount++;
            // 重新计算下次复习时间
            existing.NextReviewAt = CalculateNextReviewTime(existing.ReviewCount);
        }
        else
        {
            // 创建新错题
            var wrongQuestion = new WrongQuestion
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                QuestionId = questionId,
                UserAnswer = userAnswer,
                CorrectAnswer = correctAnswer,
                ErrorType = null,
                ReviewStatus = "new",
                ReviewCount = 0,
                NextReviewAt = CalculateNextReviewTime(0), // 立即复习
                FirstWrongAt = DateTime.Now,
                IsDeleted = false
            };
            await _context.WrongQuestions.AddAsync(wrongQuestion);
        }

        await _context.SaveChangesAsync();
    }

    /// <summary>
    /// 获取错题列表
    /// </summary>
    public async Task<PageResult<WrongQuestionDetailResponse>> GetWrongQuestionsAsync(Guid userId, string? status, int page, int pageSize)
    {
        var query = _context.WrongQuestions
            .Include(wq => wq.Question)
            .Where(wq => wq.UserId == userId && !wq.IsDeleted);

        if (!string.IsNullOrEmpty(status))
        {
            query = query.Where(wq => wq.ReviewStatus == status);
        }

        var total = await query.CountAsync();

        var items = await query
            .OrderByDescending(wq => wq.LastReviewAt ?? wq.FirstWrongAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        var result = items.Select(wq => new WrongQuestionDetailResponse
        {
            Id = wq.Id,
            QuestionId = wq.QuestionId,
            QuestionStem = wq.Question.QuestionStem,
            QuestionType = wq.Question.QuestionType,
            KnowledgePoint = wq.Question.KnowledgePoint ?? "",
            UserAnswer = wq.UserAnswer,
            CorrectAnswer = wq.CorrectAnswer,
            Analysis = wq.Question.AnswerAnalysis ?? "",
            ReviewCount = wq.ReviewCount,
            NextReviewAt = wq.NextReviewAt,
            ReviewStatus = wq.ReviewStatus
        }).ToList();

        return PageResult<WrongQuestionDetailResponse>.Create(result, total, page, pageSize);
    }

    /// <summary>
    /// 获取需要复习的错题
    /// </summary>
    public async Task<List<WrongQuestionDto>> GetReviewQuestionsAsync(Guid userId, int limit)
    {
        var now = DateTime.Now;

        var questions = await _context.WrongQuestions
            .Include(wq => wq.Question)
            .Where(wq => wq.UserId == userId &&
                        !wq.IsDeleted &&
                        wq.ReviewStatus == "reviewing" &&
                        (wq.NextReviewAt == null || wq.NextReviewAt <= now))
            .OrderBy(wq => wq.NextReviewAt)
            .Take(limit)
            .Select(wq => new WrongQuestionDto
            {
                Id = wq.Id,
                QuestionId = wq.QuestionId,
                QuestionStem = wq.Question.QuestionStem,
                QuestionType = wq.Question.QuestionType,
                ReviewCount = wq.ReviewCount
            })
            .ToListAsync();

        return questions;
    }

    /// <summary>
    /// 复习错题
    /// </summary>
    public async Task<(int reviewCount, DateTime? nextReviewAt, string reviewStatus, bool isMastered)> ReviewWrongQuestionAsync(
        Guid wrongQuestionId, Guid userId, string userAnswer, bool isCorrect)
    {
        var wrongQuestion = await _context.WrongQuestions
            .FirstOrDefaultAsync(wq => wq.Id == wrongQuestionId && wq.UserId == userId && !wq.IsDeleted);

        if (wrongQuestion == null)
        {
            throw new BusinessException("错题记录不存在", 404);
        }

        wrongQuestion.LastReviewAt = DateTime.Now;
        wrongQuestion.ReviewCount++;

        if (isCorrect)
        {
            // 答对了，延长下次复习时间
            wrongQuestion.NextReviewAt = CalculateNextReviewTime(wrongQuestion.ReviewCount);

            // 检查是否已掌握（复习 6 次且正确）
            if (wrongQuestion.ReviewCount >= 6)
            {
                wrongQuestion.ReviewStatus = "mastered";
                wrongQuestion.MasteredAt = DateTime.Now;
            }
            else
            {
                wrongQuestion.ReviewStatus = "reviewing";
            }
        }
        else
        {
            // 答错了，重新计算复习时间
            wrongQuestion.ReviewCount = 0; // 重置
            wrongQuestion.NextReviewAt = CalculateNextReviewTime(0);
            wrongQuestion.ReviewStatus = "reviewing";
        }

        await _context.SaveChangesAsync();

        return (
            wrongQuestion.ReviewCount,
            wrongQuestion.NextReviewAt,
            wrongQuestion.ReviewStatus,
            wrongQuestion.ReviewStatus == "mastered"
        );
    }

    /// <summary>
    /// 标记为已掌握
    /// </summary>
    public async Task MarkAsMasteredAsync(Guid wrongQuestionId, Guid userId)
    {
        var wrongQuestion = await _context.WrongQuestions
            .FirstOrDefaultAsync(wq => wq.Id == wrongQuestionId && wq.UserId == userId && !wq.IsDeleted);

        if (wrongQuestion == null)
        {
            throw new BusinessException("错题记录不存在", 404);
        }

        wrongQuestion.ReviewStatus = "mastered";
        wrongQuestion.MasteredAt = DateTime.Now;

        await _context.SaveChangesAsync();
    }

    /// <summary>
    /// 计算下次复习时间（艾宾浩斯记忆曲线）
    /// </summary>
    private DateTime? CalculateNextReviewTime(int reviewCount)
    {
        if (reviewCount >= EbbinghausIntervals.Intervals.Length)
        {
            return null; // 已掌握
        }

        int minutesToAdd = EbbinghausIntervals.Intervals[reviewCount];
        return DateTime.Now.AddMinutes(minutesToAdd);
    }
}
