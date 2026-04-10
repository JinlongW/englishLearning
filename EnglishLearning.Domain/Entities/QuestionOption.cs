namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 题目选项表
/// </summary>
public class QuestionOption
{
    public Guid Id { get; set; }
    public Guid QuestionId { get; set; }
    public string OptionKey { get; set; } = string.Empty;
    public string OptionContent { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
    public string? AudioUrl { get; set; }
    public int SortOrder { get; set; }

    // 导航属性
    public Question Question { get; set; } = null!;
}
