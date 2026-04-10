namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 用户徽章表
/// </summary>
public class UserBadge
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public Guid BadgeId { get; set; }
    public DateTime EarnedAt { get; set; }
    public bool IsNew { get; set; } = true;

    // 导航属性
    public User User { get; set; } = null!;
    public Badge Badge { get; set; } = null!;
}
