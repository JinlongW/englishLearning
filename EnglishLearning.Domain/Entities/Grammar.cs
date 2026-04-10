namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 语法知识点表
/// </summary>
public class Grammar
{
    public Guid Id { get; set; }
    public Guid GradeUnitId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string ContentType { get; set; } = string.Empty;
    public string? VideoUrl { get; set; }
    public string? ContentJson { get; set; }
    public int? DurationSeconds { get; set; }
    public int SortOrder { get; set; }
    public string? QuizJson { get; set; }
    public int PassingScore { get; set; } = 60;
    public DateTime CreatedAt { get; set; }

    // 知识图谱依赖关系字段
    public Guid? PrerequisiteId { get; set; }  // 前置语法 ID
    public string DependencyLevel { get; set; } = "1"; // 依赖层级 (1-5)
    public string Category { get; set; } = "tense"; // 分类：tense, voice, clause...

    // 导航属性
    public GradeUnit GradeUnit { get; set; } = null!;
    public Grammar? Prerequisite { get; set; }
}
