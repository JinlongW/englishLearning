using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using Microsoft.Extensions.Logging;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using EnglishLearning.Shared.Constants;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 徽章服务实现
/// </summary>
public class BadgeService : IBadgeService
{
    private readonly AppDbContext _context;
    private readonly ILogger<BadgeService> _logger;

    public BadgeService(AppDbContext context, ILogger<BadgeService> logger)
    {
        _context = context;
        _logger = logger;
    }

    /// <summary>
    /// 检查并授予徽章
    /// </summary>
    public async Task CheckAndAwardBadgesAsync(Guid userId, string eventType, object eventData)
    {
        try
        {
            // 获取所有活跃徽章
            var badges = await _context.Badges
                .Where(b => b.IsActive)
                .ToListAsync();

            // 获取用户已获得的徽章
            var userBadgeIds = await _context.UserBadges
                .Where(ub => ub.UserId == userId)
                .Select(ub => ub.BadgeId)
                .ToListAsync();

            foreach (var badge in badges)
            {
                // 跳过已获得的徽章
                if (userBadgeIds.Contains(badge.Id))
                {
                    continue;
                }

                // 解析要求
                if (string.IsNullOrEmpty(badge.RequirementJson))
                {
                    continue;
                }

                var requirement = JsonSerializer.Deserialize<BadgeRequirement>(badge.RequirementJson);
                if (requirement == null)
                {
                    continue;
                }

                // 检查是否满足条件
                bool isMatch = eventType switch
                {
                    "checkin" => requirement.Type == "streak" &&
                                 HasPropertyValue(eventData, "streakDays", out int streak) &&
                                 streak >= requirement.Value,

                    "challenge_complete" => requirement.Type == "perfect_score" &&
                                            HasPropertyValue(eventData, "score", out int score) &&
                                            score == 100,

                    "word_count" => requirement.Type == "word_count",
                    "grammar_count" => requirement.Type == "grammar_count",

                    _ => false
                };

                if (isMatch)
                {
                    await AwardBadgeAsync(userId, badge.Id);
                    _logger.LogInformation("用户 {UserId} 获得徽章 {BadgeName}", userId, badge.BadgeName);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "检查徽章时出错");
        }
    }

    /// <summary>
    /// 授予徽章
    /// </summary>
    public async Task AwardBadgeAsync(Guid userId, Guid badgeId)
    {
        // 检查是否已获得
        var existing = await _context.UserBadges
            .FirstOrDefaultAsync(ub => ub.UserId == userId && ub.BadgeId == badgeId);

        if (existing != null)
        {
            return;
        }

        var userBadge = new UserBadge
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            BadgeId = badgeId,
            EarnedAt = DateTime.Now,
            IsNew = true
        };

        await _context.UserBadges.AddAsync(userBadge);
        await _context.SaveChangesAsync();
    }

    /// <summary>
    /// 检查连续打卡徽章（特殊处理）
    /// </summary>
    public async Task CheckStreakBadgesAsync(Guid userId, int streakDays)
    {
        var streakBadges = await _context.Badges
            .Where(b => b.BadgeType == "streak" && b.IsActive)
            .ToListAsync();

        var userBadgeIds = await _context.UserBadges
            .Where(ub => ub.UserId == userId)
            .Select(ub => ub.BadgeId)
            .ToListAsync();

        foreach (var badge in streakBadges)
        {
            if (userBadgeIds.Contains(badge.Id))
            {
                continue;
            }

            if (string.IsNullOrEmpty(badge.RequirementJson))
            {
                continue;
            }

            var requirement = JsonSerializer.Deserialize<BadgeRequirement>(badge.RequirementJson);
            if (requirement?.Type == "streak" && streakDays >= requirement.Value)
            {
                await AwardBadgeAsync(userId, badge.Id);
            }
        }
    }

    /// <summary>
    /// 检查属性值辅助方法
    /// </summary>
    private bool HasPropertyValue(object obj, string propertyName, out int value)
    {
        value = 0;
        var prop = obj.GetType().GetProperty(propertyName);
        if (prop != null)
        {
            var propValue = prop.GetValue(obj);
            if (propValue is int intValue)
            {
                value = intValue;
                return true;
            }
        }
        return false;
    }
}

/// <summary>
/// 徽章要求
/// </summary>
public class BadgeRequirement
{
    public string Type { get; set; } = string.Empty;
    public int Value { get; set; }
}
