namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 用户画像表
/// </summary>
public class UserProfile
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string? LearningStyle { get; set; }
    public int DifficultyLevel { get; set; } = 1;
    public TimeSpan? PreferredStudyTime { get; set; }
    public bool ParentNotifyEnabled { get; set; } = true;
    public int TotalLearningDays { get; set; }
    public int CurrentStreak { get; set; }
    public int MaxStreak { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
}
