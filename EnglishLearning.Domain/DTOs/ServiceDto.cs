namespace EnglishLearning.Domain.DTOs;

using EnglishLearning.Domain.Entities;

/// <summary>
/// 注册请求
/// </summary>
public class RegisterRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public string StudentName { get; set; } = string.Empty;
    public int GradeLevel { get; set; }
    public string? Phone { get; set; }
}

/// <summary>
/// 登录请求
/// </summary>
public class LoginRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

/// <summary>
/// 用户信息 DTO
/// </summary>
public class UserInfoDto
{
    public Guid Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string StudentName { get; set; } = string.Empty;
    public int GradeLevel { get; set; }
    public string? AvatarUrl { get; set; }
    public int CurrentStreak { get; set; }
    public int CurrentLevel { get; set; }
    public string LevelName { get; set; } = string.Empty;
    public int CurrentExp { get; set; }
    public int TotalPoints { get; set; }
    public int TotalCoins { get; set; }
}

/// <summary>
/// 登录响应
/// </summary>
public class LoginResponse
{
    public string Token { get; set; } = string.Empty;
    public UserInfoDto User { get; set; } = new();
    public int ExpiresIn { get; set; } = 7200;
}

/// <summary>
/// 单词详情响应
/// </summary>
public class WordDetailResponse
{
    public Guid Id { get; set; }
    public string WordText { get; set; } = string.Empty;
    public string PhoneticUk { get; set; } = string.Empty;
    public string PhoneticUs { get; set; } = string.Empty;
    public string? AudioUrl { get; set; }
    public string MeaningCn { get; set; } = string.Empty;
    public string? PartOfSpeech { get; set; }
    public string? ExampleEn { get; set; }
    public string? ExampleCn { get; set; }
    public string? ImageUrl { get; set; }
    public int SortOrder { get; set; }
    public string Status { get; set; } = string.Empty;
    public int? Score { get; set; }
}

/// <summary>
/// 题目详情响应
/// </summary>
public class QuestionDetailResponse
{
    public Guid Id { get; set; }
    public string QuestionType { get; set; } = string.Empty;
    public int Difficulty { get; set; }
    public string QuestionStem { get; set; } = string.Empty;
    public string? StemAudioUrl { get; set; }
    public List<QuestionOptionDto> Options { get; set; } = new();
    public int? QuestionOrder { get; set; }
}

/// <summary>
/// 题目选项 DTO
/// </summary>
public class QuestionOptionDto
{
    public Guid Id { get; set; }
    public string OptionKey { get; set; } = string.Empty;
    public string OptionContent { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
    public string? AudioUrl { get; set; }
}

/// <summary>
/// 答题结果
/// </summary>
public class AnswerResultResponse
{
    public bool IsCorrect { get; set; }
    public string CorrectAnswer { get; set; } = string.Empty;
    public string Analysis { get; set; } = string.Empty;
    public int PointsEarned { get; set; }
    public int ExpEarned { get; set; }
    public bool LevelUp { get; set; }
}

/// <summary>
/// 每日挑战结果
/// </summary>
public class ChallengeResultResponse
{
    public Guid Id { get; set; }
    public int TotalQuestions { get; set; }
    public int CorrectCount { get; set; }
    public int Score { get; set; }
    public int TimeUsedSeconds { get; set; }
    public int PointsEarned { get; set; }
    public int CoinsEarned { get; set; }
    public List<ChallengeQuestionResult> QuestionResults { get; set; } = new();
}

/// <summary>
/// 挑战题目结果
/// </summary>
public class ChallengeQuestionResult
{
    public Guid QuestionId { get; set; }
    public string QuestionStem { get; set; } = string.Empty;
    public string UserAnswer { get; set; } = string.Empty;
    public string CorrectAnswer { get; set; } = string.Empty;
    public bool IsCorrect { get; set; }
    public int TimeUsedSeconds { get; set; }
    public int SpeedBonus { get; set; }
    public string? Analysis { get; set; }
}

/// <summary>
/// 错题详情
/// </summary>
public class WrongQuestionDetailResponse
{
    public Guid Id { get; set; }
    public Guid QuestionId { get; set; }
    public string QuestionStem { get; set; } = string.Empty;
    public string QuestionType { get; set; } = string.Empty;
    public string KnowledgePoint { get; set; } = string.Empty;
    public string UserAnswer { get; set; } = string.Empty;
    public string CorrectAnswer { get; set; } = string.Empty;
    public string Analysis { get; set; } = string.Empty;
    public int ReviewCount { get; set; }
    public DateTime? NextReviewAt { get; set; }
    public string ReviewStatus { get; set; } = string.Empty;
}

/// <summary>
/// 错题 DTO
/// </summary>
public class WrongQuestionDto
{
    public Guid Id { get; set; }
    public Guid QuestionId { get; set; }
    public string QuestionStem { get; set; } = string.Empty;
    public string QuestionType { get; set; } = string.Empty;
    public int ReviewCount { get; set; }
}

/// <summary>
/// 学习统计
/// </summary>
public class LearningSummaryResponse
{
    public int TotalLearningDays { get; set; }
    public int CurrentStreak { get; set; }
    public int MaxStreak { get; set; }
    public int WordsLearned { get; set; }
    public int GrammarsCompleted { get; set; }
    public int ChallengesCompleted { get; set; }
    public int WrongQuestionCount { get; set; }
    public int TotalPoints { get; set; }
    public int TotalCoins { get; set; }
    public int CurrentLevel { get; set; }
    public string LevelName { get; set; } = string.Empty;
}

/// <summary>
/// 徽章信息
/// </summary>
public class BadgeDto
{
    public Guid Id { get; set; }
    public string BadgeCode { get; set; } = string.Empty;
    public string BadgeName { get; set; } = string.Empty;
    public string? BadgeIcon { get; set; }
    public string BadgeType { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public DateTime? EarnedAt { get; set; }
    public bool IsEarned { get; set; }
    public bool IsNew { get; set; }
}

/// <summary>
/// 语法 DTO
/// </summary>
public class GrammarDto
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string ContentType { get; set; } = string.Empty;
    public int? DurationSeconds { get; set; }
    public int SortOrder { get; set; }
    public int PassingScore { get; set; }
    public string Status { get; set; } = string.Empty;
    public int? Score { get; set; }
}

/// <summary>
/// 语法详情 DTO
/// </summary>
public class GrammarDetailDto : GrammarDto
{
    public string? ContentJson { get; set; }
    public string? QuizJson { get; set; }
}

/// <summary>
/// 情景对话条目
/// </summary>
public class SceneDialogue
{
    public string Speaker { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
}

/// <summary>
/// 情景学习场景 DTO
/// </summary>
public class SceneDto
{
    public string Title { get; set; } = string.Empty;
    public string Image { get; set; } = string.Empty;
    public List<SceneDialogue> Dialogue { get; set; } = new();
    public string GrammarPoint { get; set; } = string.Empty;
}

/// <summary>
/// 情景学习内容 DTO（添加到 GrammarDetailDto 的扩展）
/// </summary>
public class GrammarDetailWithScenesDto : GrammarDetailDto
{
    public List<SceneDto>? Scenes { get; set; }
}

/// <summary>
/// 测验答案请求
/// </summary>
public class QuizAnswerRequest
{
    public Guid QuestionId { get; set; }
    public string UserAnswer { get; set; } = string.Empty;
}

/// <summary>
/// 挑战答案请求
/// </summary>
public class ChallengeAnswerRequest
{
    public Guid QuestionId { get; set; }
    public string UserAnswer { get; set; } = string.Empty;
    public bool IsCorrect { get; set; }
    public int TimeUsedSeconds { get; set; }
}

/// <summary>
/// 每日挑战 DTO
/// </summary>
public class DailyChallengeDto
{
    public Guid? Id { get; set; }
    public DateTime Date { get; set; }
    public string Status { get; set; } = string.Empty;
    public bool IsCompleted { get; set; }
    public int TotalQuestions { get; set; }
    public int CorrectCount { get; set; }
    public int Score { get; set; }
    public int PointsEarned { get; set; }
    public int CoinsEarned { get; set; }
    public string Theme { get; set; } = "mixed";
    public string ThemeName { get; set; } = "综合日";
    public string ThemeIcon { get; set; } = "🎯";
    public int BonusMultiplier { get; set; } = 1;
}

/// <summary>
/// 更新进度请求
/// </summary>
public class UpdateProgressRequest
{
    public int Score { get; set; }
    public string Status { get; set; } = "completed";
}

/// <summary>
/// 提交答案请求
/// </summary>
public class SubmitAnswerRequest
{
    public string UserAnswer { get; set; } = string.Empty;
    public int TimeUsedSeconds { get; set; }
}

/// <summary>
/// 年级单元 DTO
/// </summary>
public class GradeUnitDto
{
    public Guid Id { get; set; }
    public int Grade { get; set; }
    public string Semester { get; set; } = string.Empty;
    public int UnitNo { get; set; }
    public string UnitName { get; set; } = string.Empty;
    public int WordCount { get; set; }
}

/// <summary>
/// 年级单元树节点 DTO
/// </summary>
public class GradeUnitTreeNode
{
    public Guid Id { get; set; }
    public string Label { get; set; } = string.Empty;
    public int Grade { get; set; }
    public string Semester { get; set; } = string.Empty;
    public int UnitNo { get; set; }
    public int WordCount { get; set; }
    public int LearnedWordCount { get; set; }
    public string Status { get; set; } = "not_started";
}

/// <summary>
/// 年级树节点 DTO
/// </summary>
public class GradeTreeNode
{
    public int Grade { get; set; }
    public string Label { get; set; } = string.Empty;
    public List<GradeUnitTreeNode> Units { get; set; } = new();
}

/// <summary>
/// 语法知识树节点 DTO
/// </summary>
public class GrammarTreeNode
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public int Level { get; set; }
    public string Category { get; set; } = string.Empty;
    public string Status { get; set; } = "locked"; // locked, available, completed, learning
    public Guid? PrerequisiteId { get; set; }
    public List<GrammarTreeNode> Children { get; set; } = new();
}

/// <summary>
/// 单词复习 DTO（艾宾浩斯智能复习）
/// </summary>
public class WordReviewDto
{
    public Guid Id { get; set; }
    public string WordText { get; set; } = string.Empty;
    public string MeaningCn { get; set; } = string.Empty;
    public int ReviewCount { get; set; }
    public DateTime NextReviewAt { get; set; }
    public bool IsUrgent { get; set; } // 24 小时内到期
}

/// <summary>
/// 复习计划 DTO（一周复习计划）
/// </summary>
public class ReviewScheduleDto
{
    public DateTime Date { get; set; }
    public int WordCount { get; set; }
    public List<string> PreviewWords { get; set; } = new();
}
