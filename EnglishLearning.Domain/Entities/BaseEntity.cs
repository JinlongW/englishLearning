namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 基础实体类（带 CreatedAt 和 UpdatedAt）
/// </summary>
public abstract class BaseEntity
{
    public Guid Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
