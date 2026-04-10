namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 学习进度表
/// </summary>
public class LearningProgress
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public Guid GradeUnitId { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public Guid ContentId { get; set; }
    public string Status { get; set; } = "not_started";
    public int? Score { get; set; }
    public int AttemptsCount { get; set; }
    public DateTime? LastAttemptAt { get; set; }
    public DateTime? CompletedAt { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
    public GradeUnit GradeUnit { get; set; } = null!;
}
