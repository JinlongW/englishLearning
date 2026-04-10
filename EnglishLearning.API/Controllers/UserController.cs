using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 用户控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class UserController : ControllerBase
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }

    /// <summary>
    /// 获取学习统计
    /// </summary>
    [HttpGet("stats")]
    public async Task<ActionResult<Result>> GetLearningStats()
    {
        var userId = GetCurrentUserId();
        var stats = await _userService.GetLearningSummaryAsync(userId);

        return Ok(Result.Ok(stats));
    }

    /// <summary>
    /// 获取徽章列表
    /// </summary>
    [HttpGet("badges")]
    public async Task<ActionResult<Result>> GetBadges()
    {
        var userId = GetCurrentUserId();
        var badges = await _userService.GetBadgesAsync(userId);

        return Ok(Result.Ok(badges));
    }

    /// <summary>
    /// 获取积分记录
    /// </summary>
    [HttpGet("points")]
    public async Task<ActionResult<Result>> GetPointsHistory([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
    {
        var userId = GetCurrentUserId();

        // 限制分页参数
        page = Math.Max(1, page);
        pageSize = Math.Clamp(pageSize, 1, 100);

        var result = await _userService.GetPointsHistoryAsync(userId, page, pageSize);

        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 获取每日打卡题目（5道题）
    /// </summary>
    [HttpGet("daily-checkin/questions")]
    public async Task<ActionResult<Result>> GetDailyCheckinQuestions()
    {
        var userId = GetCurrentUserId();
        var questions = await _userService.GetDailyCheckinQuestionsAsync(userId);
        return Ok(Result.Ok(questions));
    }

    /// <summary>
    /// 每日打卡（完成题目后签到领奖励）
    /// </summary>
    [HttpPost("checkin")]
    public async Task<ActionResult<Result>> CheckIn()
    {
        var userId = GetCurrentUserId();

        try
        {
            var result = await _userService.CheckInAsync(userId);

            return Ok(Result.Ok(new
            {
                checkinDate = DateTime.Today.ToString("yyyy-MM-dd"),
                pointsEarned = result.pointsEarned,
                streakDays = result.streakDays,
                bonusPoints = result.bonusPoints,
                totalPoints = result.pointsEarned
            }, "打卡成功"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 检查今天是否已打卡
    /// </summary>
    [HttpGet("checkin/status")]
    public async Task<ActionResult<Result>> CheckCheckinStatus(CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        var hasCheckedIn = await _userService.HasCheckedInTodayAsync(userId, cancellationToken);
        return Ok(Result.Ok(new { hasCheckedIn }));
    }

    private Guid GetCurrentUserId()
    {
        var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        if (Guid.TryParse(userIdClaim, out var userId))
        {
            return userId;
        }
        throw new UnauthorizedAccessException("用户未授权");
    }
}
