namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 积分记录表
/// </summary>
public class UserPoints
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string PointsType { get; set; } = string.Empty;
    public string ChangeType { get; set; } = string.Empty;
    public int ChangeAmount { get; set; }
    public int BalanceAfter { get; set; }
    public string Description { get; set; } = string.Empty;
    public Guid? ReferenceId { get; set; }
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
}
