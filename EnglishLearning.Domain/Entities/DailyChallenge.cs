namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 每日挑战主表
/// </summary>
public class DailyChallenge
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public DateTime ChallengeDate { get; set; }
    public string Status { get; set; } = "pending";
    public int TotalQuestions { get; set; } = 10;
    public int CorrectCount { get; set; }
    public int Score { get; set; }
    public int TimeUsedSeconds { get; set; }
    public int PointsEarned { get; set; }
    public int CoinsEarned { get; set; }
    public DateTime? StartedAt { get; set; }
    public DateTime? CompletedAt { get; set; }
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
    public ICollection<DailyChallengeDetail> Details { get; set; } = new List<DailyChallengeDetail>();
}
