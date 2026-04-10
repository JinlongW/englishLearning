using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 错题本控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class WrongQuestionController : ControllerBase
{
    private readonly IWrongQuestionService _wrongQuestionService;

    public WrongQuestionController(IWrongQuestionService wrongQuestionService)
    {
        _wrongQuestionService = wrongQuestionService;
    }

    /// <summary>
    /// 获取错题列表
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<Result>> GetWrongQuestions(
        [FromQuery] string? status,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var userId = GetCurrentUserId();

        // 限制分页参数
        page = Math.Max(1, page);
        pageSize = Math.Clamp(pageSize, 1, 100);

        var result = await _wrongQuestionService.GetWrongQuestionsAsync(userId, status, page, pageSize);

        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 获取复习推送
    /// </summary>
    [HttpGet("review")]
    public async Task<ActionResult<Result>> GetReviewQuestions([FromQuery] int limit = 10)
    {
        var userId = GetCurrentUserId();
        var questions = await _wrongQuestionService.GetReviewQuestionsAsync(userId, limit);

        return Ok(Result.Ok(questions));
    }

    /// <summary>
    /// 复习错题
    /// </summary>
    [HttpPost("{id:guid}/review")]
    public async Task<ActionResult<Result>> ReviewWrongQuestion(Guid id, [FromBody] ReviewRequest request)
    {
        var userId = GetCurrentUserId();

        try
        {
            var result = await _wrongQuestionService.ReviewWrongQuestionAsync(id, userId, request.UserAnswer, request.IsCorrect);

            return Ok(Result.Ok(new
            {
                reviewCount = result.reviewCount,
                nextReviewAt = result.nextReviewAt,
                reviewStatus = result.reviewStatus,
                isMastered = result.isMastered
            }, result.isMastered ? "已掌握" : "复习完成"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 标记为已掌握
    /// </summary>
    [HttpPost("{id:guid}/master")]
    public async Task<ActionResult<Result>> MarkAsMastered(Guid id)
    {
        var userId = GetCurrentUserId();

        try
        {
            await _wrongQuestionService.MarkAsMasteredAsync(id, userId);

            return Ok(Result.Ok(null, "已标记为掌握"));
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

/// <summary>
/// 复习请求
/// </summary>
public class ReviewRequest
{
    public string UserAnswer { get; set; } = string.Empty;
    public bool IsCorrect { get; set; }
}
