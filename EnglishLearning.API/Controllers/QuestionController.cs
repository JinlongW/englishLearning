using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 题目控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class QuestionController : ControllerBase
{
    private readonly IQuestionService _questionService;

    public QuestionController(IQuestionService questionService)
    {
        _questionService = questionService;
    }

    /// <summary>
    /// 获取题目详情
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<Result>> GetQuestion(Guid id)
    {
        var question = await _questionService.GetQuestionByIdAsync(id);

        if (question == null)
        {
            return NotFound(Result.NotFound("题目不存在"));
        }

        return Ok(Result.Ok(question));
    }

    /// <summary>
    /// 提交答案
    /// </summary>
    [HttpPost("{id:guid}/answer")]
    public async Task<ActionResult<Result>> SubmitAnswer(Guid id, [FromBody] SubmitAnswerRequest request)
    {
        var userId = GetCurrentUserId();

        try
        {
            var result = await _questionService.SubmitAnswerAsync(id, userId, request.UserAnswer, request.TimeUsedSeconds);

            return Ok(Result.Ok(new
            {
                isCorrect = result.IsCorrect,
                correctAnswer = result.CorrectAnswer,
                analysis = result.Analysis,
                pointsEarned = result.PointsEarned,
                expEarned = result.ExpEarned,
                levelUp = result.LevelUp
            }, result.IsCorrect ? "回答正确" : "回答错误"));
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
