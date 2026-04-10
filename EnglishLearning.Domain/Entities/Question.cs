namespace EnglishLearning.Domain.Entities;

/// <summary>
/// 题目表
/// </summary>
public class Question
{
    public Guid Id { get; set; }
    public Guid GradeUnitId { get; set; }
    public string QuestionType { get; set; } = string.Empty;
    public int Difficulty { get; set; } = 1;
    public string QuestionStem { get; set; } = string.Empty;
    public string? StemAudioUrl { get; set; }
    public string CorrectAnswer { get; set; } = string.Empty;
    public string? AnswerAnalysis { get; set; }
    public string? KnowledgePoint { get; set; }
    public string? Tags { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    // 导航属性
    public GradeUnit GradeUnit { get; set; } = null!;
    public ICollection<QuestionOption> Options { get; set; } = new List<QuestionOption>();
    public ICollection<WrongQuestion> WrongQuestions { get; set; } = new List<WrongQuestion>();
    public ICollection<DailyChallengeDetail> DailyChallengeDetails { get; set; } = new List<DailyChallengeDetail>();
}
