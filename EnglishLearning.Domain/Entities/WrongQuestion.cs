namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 错题表
/// </summary>
public class WrongQuestion
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public Guid QuestionId { get; set; }
    public string UserAnswer { get; set; } = string.Empty;
    public string CorrectAnswer { get; set; } = string.Empty;
    public string? ErrorType { get; set; }
    public string ReviewStatus { get; set; } = "new";
    public int ReviewCount { get; set; }
    public DateTime? NextReviewAt { get; set; }
    public DateTime FirstWrongAt { get; set; }
    public DateTime? LastReviewAt { get; set; }
    public DateTime? MasteredAt { get; set; }
    public bool IsDeleted { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
    public Question Question { get; set; } = null!;
}
