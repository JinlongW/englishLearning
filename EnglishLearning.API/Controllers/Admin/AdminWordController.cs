using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;

namespace EnglishLearning.API.Controllers.Admin;

/// <summary>
/// 管理员单词管理控制器
/// </summary>
[ApiController]
[Route("api/admin/[controller]")]
[Authorize(Roles = "Admin")]
[Produces("application/json")]
[EnableRateLimiting("auth")]
public class AdminWordController : ControllerBase
{
    private readonly IWordService _wordService;

    public AdminWordController(IWordService wordService)
    {
        _wordService = wordService;
    }

    /// <summary>
    /// 获取单词分页列表（管理员）
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<Result>> GetList(
        [FromQuery] Guid gradeUnitId,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        if (gradeUnitId == Guid.Empty)
        {
            return BadRequest(Result.Error("年级单元 ID 不能为空", 400));
        }

        // 限制分页参数
        page = Math.Max(1, page);
        pageSize = Math.Clamp(pageSize, 1, 100);

        var result = await _wordService.GetPagedByGradeUnitAsync(gradeUnitId, page, pageSize, cancellationToken);
        return Ok(Result.Ok(result));
    }

    /// <summary>
    /// 获取单词详情（管理员）
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<Result>> GetById(Guid id, CancellationToken cancellationToken = default)
    {
        var word = await _wordService.GetWordByIdForAdminAsync(id, cancellationToken);
        if (word == null)
        {
            return NotFound(Result.NotFound("单词不存在"));
        }
        return Ok(Result.Ok(word));
    }

    /// <summary>
    /// 创建单词
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<Result>> Create([FromBody] CreateWordRequest request, CancellationToken cancellationToken = default)
    {
        if (request.GradeUnitId == Guid.Empty)
        {
            return BadRequest(Result.Error("年级单元 ID 不能为空", 400));
        }

        if (string.IsNullOrWhiteSpace(request.WordText))
        {
            return BadRequest(Result.Error("单词文本不能为空", 400));
        }

        if (string.IsNullOrWhiteSpace(request.MeaningCn))
        {
            return BadRequest(Result.Error("中文释义不能为空", 400));
        }

        var word = await _wordService.CreateWordAsync(request, cancellationToken);
        return Ok(Result.Ok(word, "创建成功"));
    }

    /// <summary>
    /// 更新单词
    /// </summary>
    [HttpPut("{id:guid}")]
    public async Task<ActionResult<Result>> Update(Guid id, [FromBody] UpdateWordRequest request, CancellationToken cancellationToken = default)
    {
        if (id == Guid.Empty)
        {
            return BadRequest(Result.Error("单词 ID 不能为空", 400));
        }

        if (request.GradeUnitId == Guid.Empty)
        {
            return BadRequest(Result.Error("年级单元 ID 不能为空", 400));
        }

        if (string.IsNullOrWhiteSpace(request.WordText))
        {
            return BadRequest(Result.Error("单词文本不能为空", 400));
        }

        if (string.IsNullOrWhiteSpace(request.MeaningCn))
        {
            return BadRequest(Result.Error("中文释义不能为空", 400));
        }

        var result = await _wordService.UpdateWordAsync(id, request, cancellationToken);
        if (!result)
        {
            return NotFound(Result.NotFound("单词不存在"));
        }
        return Ok(Result.Ok(true, "更新成功"));
    }

    /// <summary>
    /// 删除单词
    /// </summary>
    [HttpDelete("{id:guid}")]
    public async Task<ActionResult<Result>> Delete(Guid id, CancellationToken cancellationToken = default)
    {
        if (id == Guid.Empty)
        {
            return BadRequest(Result.Error("单词 ID 不能为空", 400));
        }

        var result = await _wordService.DeleteWordAsync(id, cancellationToken);
        if (!result)
        {
            return NotFound(Result.NotFound("单词不存在"));
        }
        return Ok(Result.Ok(true, "删除成功"));
    }
}
