namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 每日挑战详情表
/// </summary>
public class DailyChallengeDetail
{
    public Guid Id { get; set; }
    public Guid DailyChallengeId { get; set; }
    public Guid QuestionId { get; set; }
    public int QuestionOrder { get; set; }
    public string UserAnswer { get; set; } = string.Empty;
    public bool IsCorrect { get; set; }
    public int TimeUsedSeconds { get; set; }
    public bool IsUncertain { get; set; }
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public DailyChallenge DailyChallenge { get; set; } = null!;
    public Question Question { get; set; } = null!;
}
