namespace EnglishLearning.Shared.Constants;

/// <summary>
/// 积分规则配置
/// </summary>
public static class PointRules
{
    public static readonly int SignIn = 5;
    public static readonly int DailyChallengeComplete = 50;
    public static readonly int WordLevelComplete = 10;
    public static readonly int GrammarLevelComplete = 20;
    public static readonly int StreakBonus7Days = 10;
    public static readonly int StreakBonus30Days = 50;
    public static readonly int PerfectScoreBonus = 20;
}

/// <summary>
/// 等级配置
/// </summary>
public static class LevelConfig
{
    public static readonly Dictionary<int, (string Name, int ExpRequired)> Levels = new()
    {
        { 1, ("英语小白", 0) },
        { 2, ("入门学徒", 100) },
        { 3, ("进步之星", 300) },
        { 4, ("勤奋少年", 600) },
        { 5, ("英语新星", 1000) },
        { 6, ("学习能手", 1500) },
        { 7, ("词汇达人", 2200) },
        { 8, ("语法高手", 3000) },
        { 9, ("英语达人", 4000) },
        { 10, ("英语大师", 5500) },
        { 11, ("单词王者", 7500) },
        { 12, ("英语学霸", 10000) }
    };

    public static (string Name, int ExpRequired) GetLevelInfo(int level)
    {
        if (Levels.TryGetValue(level, out var info))
        {
            return info;
        }
        return ("英语学霸", 10000);
    }

    public static int GetExpToNext(int currentLevel)
    {
        var info = GetLevelInfo(currentLevel);
        var nextLevel = currentLevel + 1;
        if (Levels.TryGetValue(nextLevel, out var nextInfo))
        {
            return nextInfo.ExpRequired - info.ExpRequired;
        }
        return 999999;
    }
}

/// <summary>
/// 艾宾浩斯复习间隔 (分钟)
/// </summary>
public static class EbbinghausIntervals
{
    public static readonly int[] Intervals = { 0, 5, 1440, 4320, 10080, 21600, 43200 };
    //                                   即时  5 分钟  1 天   3 天    7 天   15 天   30 天
}
