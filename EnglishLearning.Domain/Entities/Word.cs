namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 单词表
/// </summary>
public class Word
{
    public Guid Id { get; set; }
    public Guid GradeUnitId { get; set; }
    public string WordText { get; set; } = string.Empty;
    public string? PhoneticUk { get; set; }
    public string? PhoneticUs { get; set; }
    public string? AudioUrl { get; set; }
    public string MeaningCn { get; set; } = string.Empty;
    public string? PartOfSpeech { get; set; }
    public string? ExampleEn { get; set; }
    public string? ExampleCn { get; set; }
    public string? ImageUrl { get; set; }
    public int SortOrder { get; set; }

    // 导航属性
    public GradeUnit GradeUnit { get; set; } = null!;
    public ICollection<LearningProgress> LearningProgresses { get; set; } = new List<LearningProgress>();
}
