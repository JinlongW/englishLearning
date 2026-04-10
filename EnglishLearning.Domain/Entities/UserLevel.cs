namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 用户等级表
/// </summary>
public class UserLevel
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public int CurrentLevel { get; set; } = 1;
    public string LevelName { get; set; } = "英语小白";
    public int CurrentExp { get; set; }
    public int ExpToNext { get; set; } = 100;
    public DateTime? LevelUpAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    // 导航属性
    public User User { get; set; } = null!;
}
