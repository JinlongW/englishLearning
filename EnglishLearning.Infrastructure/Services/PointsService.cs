using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Constants;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 积分服务实现
/// </summary>
public class PointsService : IPointsService
{
    private readonly AppDbContext _context;
    private readonly IBadgeService _badgeService;

    public PointsService(AppDbContext context, IBadgeService badgeService)
    {
        _context = context;
        _badgeService = badgeService;
    }

    /// <summary>
    /// 添加积分
    /// </summary>
    public async Task AddPointsAsync(Guid userId, string pointsType, string changeType, int amount, string description, Guid? referenceId = null)
    {
        var balance = await _context.UserPoints
            .Where(p => p.UserId == userId && p.PointsType == pointsType)
            .SumAsync(p => p.ChangeAmount);

        var record = new UserPoints
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            PointsType = pointsType,
            ChangeType = changeType,
            ChangeAmount = amount,
            BalanceAfter = balance + amount,
            Description = description,
            ReferenceId = referenceId,
            CreatedAt = DateTime.Now
        };

        // 使用 ExecuteSqlRawAsync 避免 EF Core 的 OUTPUT 子句与 SQL Server 触发器冲突
        var referenceIdParam = new SqlParameter("@reference_id", referenceId ?? (object)DBNull.Value);

        await _context.Database.ExecuteSqlRawAsync(
            @"INSERT INTO tb_user_points (id, user_id, points_type, change_type, change_amount, balance_after, description, reference_id, created_at) VALUES (@id, @user_id, @points_type, @change_type, @change_amount, @balance_after, @description, @reference_id, @created_at)",
            new SqlParameter("@id", record.Id),
            new SqlParameter("@user_id", record.UserId),
            new SqlParameter("@points_type", record.PointsType),
            new SqlParameter("@change_type", record.ChangeType),
            new SqlParameter("@change_amount", record.ChangeAmount),
            new SqlParameter("@balance_after", record.BalanceAfter),
            new SqlParameter("@description", record.Description),
            referenceIdParam,
            new SqlParameter("@created_at", record.CreatedAt));
    }

    /// <summary>
    /// 添加经验值
    /// </summary>
    public async Task<bool> AddExpAsync(Guid userId, int exp)
    {
        var userLevel = await _context.UserLevels.FirstOrDefaultAsync(ul => ul.UserId == userId);
        if (userLevel == null)
        {
            return false;
        }

        var newExp = userLevel.CurrentExp + exp;
        var updatedAt = DateTime.Now;

        bool levelUp = false;
        int newLevel = userLevel.CurrentLevel;
        string? newLevelName = userLevel.LevelName;
        int? newExpToNext = userLevel.ExpToNext;
        DateTime? levelUpAt = null;

        // 检查是否升级
        var nextLevelInfo = LevelConfig.GetLevelInfo(userLevel.CurrentLevel + 1);
        if (newExp >= nextLevelInfo.ExpRequired)
        {
            newLevel = userLevel.CurrentLevel + 1;
            newLevelName = nextLevelInfo.Name;
            newExpToNext = LevelConfig.GetExpToNext(newLevel);
            levelUpAt = DateTime.Now;
            levelUp = true;

            // 升级奖励
            await AddPointsAsync(userId, "points", "level_up", 50, $"升级到{newLevelName}", null);
        }

        // 使用 ExecuteSqlRawAsync 避免 EF Core 的 OUTPUT 子句与 SQL Server 触发器冲突
        var newLevelNameParam = new SqlParameter("@level_name", newLevelName ?? (object)DBNull.Value);
        var newExpToNextParam = new SqlParameter("@exp_to_next", newExpToNext ?? (object)DBNull.Value);
        var levelUpAtParam = new SqlParameter("@level_up_at", levelUpAt ?? (object)DBNull.Value);

        await _context.Database.ExecuteSqlRawAsync(
            @"UPDATE tb_user_level SET current_exp = @current_exp, updated_at = @updated_at, current_level = @current_level, level_name = @level_name, exp_to_next = @exp_to_next, level_up_at = @level_up_at WHERE user_id = @user_id",
            new SqlParameter("@current_exp", newExp),
            new SqlParameter("@updated_at", updatedAt),
            new SqlParameter("@current_level", newLevel),
            newLevelNameParam,
            newExpToNextParam,
            levelUpAtParam,
            new SqlParameter("@user_id", userId));

        return levelUp;
    }

    /// <summary>
    /// 获取积分余额
    /// </summary>
    public async Task<(int points, int coins)> GetBalanceAsync(Guid userId)
    {
        var points = await _context.UserPoints
            .Where(p => p.UserId == userId && p.PointsType == "points")
            .SumAsync(p => p.ChangeAmount);

        var coins = await _context.UserPoints
            .Where(p => p.UserId == userId && p.PointsType == "coins")
            .SumAsync(p => p.ChangeAmount);

        return (points, coins);
    }
}
