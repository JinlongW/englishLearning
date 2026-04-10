namespace EnglishLearning.Domain.Enums;

/// <summary>
/// 题目类型
/// </summary>
public enum QuestionType
{
    SingleChoice = 1,      // 单选
    MultipleChoice = 2,    // 多选
    FillBlank = 3,         // 填空
    SpellWord = 4,         // 拼写
    Match = 5,             // 连线
    Listening = 6          // 听力
}

/// <summary>
/// 学习状态
/// </summary>
public enum LearningStatus
{
    NotStarted = 0,    // 未开始
    Learning = 1,      // 学习中
    Completed = 2,     // 已完成
    Mastered = 3       // 已掌握
}

/// <summary>
/// 复习状态
/// </summary>
public enum ReviewStatus
{
    New = 0,           // 新错题
    Reviewing = 1,     // 复习中
    Mastered = 2       // 已掌握
}

/// <summary>
/// 徽章类型
/// </summary>
public enum BadgeType
{
    Streak = 1,        // 连续打卡
    Word = 2,          // 单词相关
    Grammar = 3,       // 语法相关
    Challenge = 4,     // 挑战相关
    Special = 5        // 特殊成就
}

/// <summary>
/// 挑战状态
/// </summary>
public enum ChallengeStatus
{
    Pending = 0,       // 未开始
    InProgress = 1,    // 进行中
    Completed = 2      // 已完成
}
