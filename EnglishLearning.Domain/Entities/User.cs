namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 用户表
/// </summary>
public class User
{
    public Guid Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string? Phone { get; set; }
    public string StudentName { get; set; } = string.Empty;
    public int GradeLevel { get; set; }
    public string? AvatarUrl { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    // 导航属性
    public UserProfile? Profile { get; set; }
    public UserLevel? Level { get; set; }
    public ICollection<LearningProgress> LearningProgresses { get; set; } = new List<LearningProgress>();
    public ICollection<WrongQuestion> WrongQuestions { get; set; } = new List<WrongQuestion>();
    public ICollection<DailyChallenge> DailyChallenges { get; set; } = new List<DailyChallenge>();
    public ICollection<UserBadge> UserBadges { get; set; } = new List<UserBadge>();
    public ICollection<UserPoints> UserPoints { get; set; } = new List<UserPoints>();
    public ICollection<Checkin> Checkins { get; set; } = new List<Checkin>();
}
