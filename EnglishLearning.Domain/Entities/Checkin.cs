namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 签到记录表
/// </summary>
public class Checkin
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public DateTime CheckinDate { get; set; }
    public int PointsEarned { get; set; } = 5;
    public int StreakDays { get; set; } = 1;
    public int BonusPoints { get; set; }
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
}
