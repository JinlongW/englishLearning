using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 每日挑战控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class ChallengeController : ControllerBase
{
    private readonly IChallengeService _challengeService;

    public ChallengeController(IChallengeService challengeService)
    {
        _challengeService = challengeService;
    }

    /// <summary>
    /// 获取今日挑战状态
    /// </summary>
    [HttpGet("today")]
    public async Task<ActionResult<Result>> GetTodayChallenge()
    {
        var userId = GetCurrentUserId();
        var result = await _challengeService.GetTodayChallengeAsync(userId);

        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 开始挑战
    /// </summary>
    [HttpPost("start")]
    public async Task<ActionResult<Result>> StartChallenge()
    {
        var userId = GetCurrentUserId();

        try
        {
            var (challengeId, questions) = await _challengeService.StartChallengeAsync(userId);

            return Ok(Result.Ok(new
            {
                challengeId = challengeId,
                questions = questions
            }, "挑战开始"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 提交挑战结果
    /// </summary>
    [HttpPost("{id:guid}/submit")]
    public async Task<ActionResult<Result>> SubmitChallenge(Guid id, [FromBody] List<ChallengeAnswerRequest> answers)
    {
        if (answers == null || answers.Count == 0)
        {
            return BadRequest(Result.Error("答案不能为空", 400));
        }

        var userId = GetCurrentUserId();

        try
        {
            var timeUsedSeconds = answers.Sum(a => a.TimeUsedSeconds);
            var result = await _challengeService.SubmitChallengeAsync(id, userId, answers, timeUsedSeconds);

            return Ok(Result.Ok(result, "挑战完成"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
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
