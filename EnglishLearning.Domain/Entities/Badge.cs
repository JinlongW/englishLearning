namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 徽章表
/// </summary>
public class Badge
{
    public Guid Id { get; set; }
    public string BadgeCode { get; set; } = string.Empty;
    public string BadgeName { get; set; } = string.Empty;
    public string? BadgeIcon { get; set; }
    public string BadgeType { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? RequirementJson { get; set; }
    public int SortOrder { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public ICollection<UserBadge> UserBadges { get; set; } = new List<UserBadge>();
}
