using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 语法控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public class GrammarController : ControllerBase
{
    private readonly IGrammarService _grammarService;

    public GrammarController(IGrammarService grammarService)
    {
        _grammarService = grammarService;
    }

    /// <summary>
    /// 获取语法列表
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<Result>> GetGrammars([FromQuery] Guid gradeUnitId)
    {
        if (gradeUnitId == Guid.Empty)
        {
            return BadRequest(Result.Error("年级单元 ID 不能为空", 400));
        }

        var userId = GetCurrentUserId();
        var grammars = await _grammarService.GetGrammarsAsync(gradeUnitId, userId);

        return Ok(Result.Ok(grammars));
    }

    /// <summary>
    /// 获取语法详情
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<Result>> GetGrammar(Guid id)
    {
        var userId = GetCurrentUserId();
        var grammar = await _grammarService.GetGrammarByIdAsync(id, userId);

        if (grammar == null)
        {
            return NotFound(Result.NotFound("语法课程不存在"));
        }

        return Ok(Result.Ok(grammar));
    }

    /// <summary>
    /// 提交语法测验
    /// </summary>
    [HttpPost("{id:guid}/quiz")]
    public async Task<ActionResult<Result>> SubmitQuiz(Guid id, [FromBody] List<QuizAnswerRequest> answers)
    {
        if (answers == null || answers.Count == 0)
        {
            return BadRequest(Result.Error("答案不能为空", 400));
        }

        var userId = GetCurrentUserId();

        try
        {
            var result = await _grammarService.SubmitGrammarQuizAsync(id, userId, answers);

            return Ok(Result.Ok(new
            {
                score = result.score,
                isPassed = result.isPassed,
                correctCount = result.correctCount,
                totalCount = result.totalCount,
                pointsEarned = result.pointsEarned
            }, result.isPassed ? "测验通过" : "测验未通过"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 获取语法知识树
    /// </summary>
    [HttpGet("tree")]
    public async Task<ActionResult<Result>> GetGrammarTree([FromQuery] int grade)
    {
        if (grade <= 0)
        {
            return BadRequest(Result.Error("年级参数无效", 400));
        }

        var userId = GetCurrentUserId();
        var tree = await _grammarService.GetGrammarTreeAsync(userId, grade);

        return Ok(Result.Ok(tree));
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
