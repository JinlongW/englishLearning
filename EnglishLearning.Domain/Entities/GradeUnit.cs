namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 年级单元表
/// </summary>
public class GradeUnit
{
    public Guid Id { get; set; }
    public int Grade { get; set; }
    public string Semester { get; set; } = string.Empty;
    public int UnitNo { get; set; }
    public string UnitName { get; set; } = string.Empty;
    public int SortOrder { get; set; }
    public bool IsLocked { get; set; }
    public DateTime CreatedAt { get; set; }

    // 导航属性
    public ICollection<Word> Words { get; set; } = new List<Word>();
    public ICollection<Grammar> Grammars { get; set; } = new List<Grammar>();
    public ICollection<Question> Questions { get; set; } = new List<Question>();
    public ICollection<LearningProgress> LearningProgresses { get; set; } = new List<LearningProgress>();
}
