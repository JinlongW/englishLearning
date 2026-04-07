using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Shared.Utils;

namespace EnglishLearning.Domain.Interfaces;

/// <summary>
/// 认证服务接口
/// </summary>
public interface IAuthService
{
    Task<(string token, UserInfoDto user)> LoginAsync(string username, string password, CancellationToken cancellationToken = default);
    Task<UserInfoDto> RegisterAsync(RegisterRequest request, CancellationToken cancellationToken = default);
    Task<UserInfoDto> GetUserInfoAsync(Guid userId, CancellationToken cancellationToken = default);
}

/// <summary>
/// 用户服务接口
/// </summary>
public interface IUserService
{
    Task<LearningSummaryResponse> GetLearningSummaryAsync(Guid userId);
    Task<List<BadgeDto>> GetBadgesAsync(Guid userId);
    Task<PageResult<UserPoints>> GetPointsHistoryAsync(Guid userId, int page, int pageSize);
    Task<(int pointsEarned, int streakDays, int bonusPoints)> CheckInAsync(Guid userId);
    /// <summary>
    /// 检查今天是否已打卡
    /// </summary>
    Task<bool> HasCheckedInTodayAsync(Guid userId, CancellationToken cancellationToken = default);
    /// <summary>
    /// 获取每日打卡题目（5道题）
    /// </summary>
    Task<List<QuestionDetailResponse>> GetDailyCheckinQuestionsAsync(Guid userId);
}

/// <summary>
/// 单词服务接口
/// </summary>
public interface IWordService
{
    Task<PageResult<WordDetailResponse>> GetWordsAsync(Guid gradeUnitId, Guid userId, int page, int pageSize);
    Task<WordDetailResponse?> GetWordByIdAsync(Guid wordId, Guid userId);
    Task<(int pointsEarned, int expEarned, bool levelUp)> UpdateWordProgressAsync(Guid wordId, Guid userId, int score, string status);

    /// <summary>
    /// 获取单词分页列表（管理员）
    /// </summary>
    Task<PageResult<WordDetailResponse>> GetPagedByGradeUnitAsync(Guid gradeUnitId, int page, int pageSize, CancellationToken cancellationToken = default);

    /// <summary>
    /// 获取单词详情（管理员）
    /// </summary>
    Task<WordDetailResponse?> GetWordByIdForAdminAsync(Guid wordId, CancellationToken cancellationToken = default);

    /// <summary>
    /// 创建单词
    /// </summary>
    Task<WordDetailResponse> CreateWordAsync(CreateWordRequest request, CancellationToken cancellationToken = default);

    /// <summary>
    /// 更新单词
    /// </summary>
    Task<bool> UpdateWordAsync(Guid wordId, UpdateWordRequest request, CancellationToken cancellationToken = default);

    /// <summary>
    /// 删除单词
    /// </summary>
    Task<bool> DeleteWordAsync(Guid wordId, CancellationToken cancellationToken = default);
}

/// <summary>
/// 语法服务接口
/// </summary>
public interface IGrammarService
{
    Task<List<GrammarDto>> GetGrammarsAsync(Guid gradeUnitId, Guid userId);
    Task<GrammarDetailDto?> GetGrammarByIdAsync(Guid grammarId, Guid userId);
    Task<(int score, bool isPassed, int correctCount, int totalCount, int pointsEarned)> SubmitGrammarQuizAsync(Guid grammarId, Guid userId, List<QuizAnswerRequest> answers);
}

/// <summary>
/// 题目服务接口
/// </summary>
public interface IQuestionService
{
    Task<QuestionDetailResponse?> GetQuestionByIdAsync(Guid questionId, CancellationToken cancellationToken = default);
    Task<List<QuestionDetailResponse>> GetQuestionDetailsAsync(List<Guid> questionIds, CancellationToken cancellationToken = default);
    Task<AnswerResultResponse> SubmitAnswerAsync(Guid questionId, Guid userId, string? userAnswer, int timeUsedSeconds, CancellationToken cancellationToken = default);
    Task<List<QuestionDetailResponse>> GetQuestionsForChallengeAsync(Guid userId, int count, CancellationToken cancellationToken = default);
}

/// <summary>
/// 挑战服务接口
/// </summary>
public interface IChallengeService
{
    Task<DailyChallengeDto> GetTodayChallengeAsync(Guid userId);
    Task<(Guid challengeId, List<QuestionDetailResponse> questions)> StartChallengeAsync(Guid userId);
    Task<ChallengeResultResponse> SubmitChallengeAsync(Guid challengeId, Guid userId, List<ChallengeAnswerRequest> answers, int timeUsedSeconds);
}

/// <summary>
/// 错题服务接口
/// </summary>
public interface IWrongQuestionService
{
    Task AddAsync(Guid userId, Guid questionId, string userAnswer, string correctAnswer);
    Task<PageResult<WrongQuestionDetailResponse>> GetWrongQuestionsAsync(Guid userId, string? status, int page, int pageSize);
    Task<List<WrongQuestionDto>> GetReviewQuestionsAsync(Guid userId, int limit);
    Task<(int reviewCount, DateTime? nextReviewAt, string reviewStatus, bool isMastered)> ReviewWrongQuestionAsync(Guid wrongQuestionId, Guid userId, string userAnswer, bool isCorrect);
    Task MarkAsMasteredAsync(Guid wrongQuestionId, Guid userId);
}

/// <summary>
/// 徽章服务接口
/// </summary>
public interface IBadgeService
{
    Task CheckAndAwardBadgesAsync(Guid userId, string eventType, object eventData);
    Task AwardBadgeAsync(Guid userId, Guid badgeId);
}

/// <summary>
/// 年级单元服务接口 - 获取可用年级和单元列表
/// </summary>
public interface IGradeUnitService
{
    /// <summary>
    /// 获取所有年级列表
    /// </summary>
    Task<List<int>> GetAllGradesAsync(CancellationToken cancellationToken = default);

    /// <summary>
    /// 获取指定年级下的所有单元
    /// </summary>
    Task<List<GradeUnitDto>> GetUnitsByGradeAsync(int grade, CancellationToken cancellationToken = default);

    /// <summary>
    /// 获取年级单元树形结构
    /// </summary>
    Task<List<GradeTreeNode>> GetGradeUnitTreeAsync(Guid userId, CancellationToken cancellationToken = default);
}

/// <summary>
/// 积分服务接口
/// </summary>
public interface IPointsService
{
    /// <summary>
    /// 添加积分
    /// </summary>
    Task AddPointsAsync(Guid userId, string pointsType, string changeType, int amount, string description, Guid? referenceId = null);

    /// <summary>
    /// 添加经验值
    /// </summary>
    Task<bool> AddExpAsync(Guid userId, int exp);

    /// <summary>
    /// 获取积分余额
    /// </summary>
    Task<(int points, int coins)> GetBalanceAsync(Guid userId);
}
