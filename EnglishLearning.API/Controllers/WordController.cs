using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 单词控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class WordController : ControllerBase
{
    private readonly IWordService _wordService;

    public WordController(IWordService wordService)
    {
        _wordService = wordService;
    }

    /// <summary>
    /// 获取单词列表
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<Result>> GetWords(
        [FromQuery] Guid gradeUnitId,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 100)
    {
        if (gradeUnitId == Guid.Empty)
        {
            return BadRequest(Result.Error("年级单元 ID 不能为空", 400));
        }

        // 限制分页参数
        page = Math.Max(1, page);
        pageSize = Math.Clamp(pageSize, 1, 100);

        var userId = GetCurrentUserId();
        var result = await _wordService.GetWordsAsync(gradeUnitId, userId, page, pageSize);

        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 获取单词详情
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<Result>> GetWord(Guid id)
    {
        var userId = GetCurrentUserId();
        var word = await _wordService.GetWordByIdAsync(id, userId);

        if (word == null)
        {
            return NotFound(Result.NotFound("单词不存在"));
        }

        return Ok(Result.Ok(word));
    }

    /// <summary>
    /// 更新单词学习进度
    /// </summary>
    [HttpPost("{id:guid}/progress")]
    public async Task<ActionResult<Result>> UpdateProgress(Guid id, [FromBody] UpdateProgressRequest request)
    {
        var userId = GetCurrentUserId();

        try
        {
            var result = await _wordService.UpdateWordProgressAsync(id, userId, request.Score, request.Status);

            return Ok(Result.Ok(new
            {
                pointsEarned = result.pointsEarned,
                expEarned = result.expEarned,
                levelUp = result.levelUp
            }, "进度更新成功"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 获取需要复习的单词列表（艾宾浩斯智能复习）
    /// </summary>
    [HttpGet("review/due")]
    public async Task<ActionResult<Result>> GetWordsDueForReview([FromQuery] int limit = 20)
    {
        var userId = GetCurrentUserId();
        var result = await _wordService.GetWordsDueForReviewAsync(userId, limit);

        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 获取一周复习计划
    /// </summary>
    [HttpGet("review/schedule")]
    public async Task<ActionResult<Result>> GetReviewSchedule()
    {
        var userId = GetCurrentUserId();
        var schedule = await _wordService.GetReviewScheduleAsync(userId);

        return Ok(Result.Ok(schedule));
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
