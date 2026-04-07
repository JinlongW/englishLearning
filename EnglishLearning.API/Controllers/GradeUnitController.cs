using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 年级单元控制器 - 获取可用年级和单元列表
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
[EnableRateLimiting("auth")]
public class GradeUnitController : ControllerBase
{
    private readonly IGradeUnitService _gradeUnitService;

    public GradeUnitController(IGradeUnitService gradeUnitService)
    {
        _gradeUnitService = gradeUnitService;
    }

    /// <summary>
    /// 获取所有年级列表
    /// </summary>
    [HttpGet("grades")]
    public async Task<ActionResult<Result>> GetGrades(CancellationToken cancellationToken)
    {
        var grades = await _gradeUnitService.GetAllGradesAsync(cancellationToken);
        return Ok(Result.Ok(grades));
    }

    /// <summary>
    /// 获取指定年级下的所有单元
    /// </summary>
    [HttpGet("units/{grade}")]
    public async Task<ActionResult<Result>> GetUnitsByGrade(int grade, CancellationToken cancellationToken)
    {
        if (grade <= 0 || grade > 12)
        {
            return BadRequest(Result.Error("Invalid grade value"));
        }

        var units = await _gradeUnitService.GetUnitsByGradeAsync(grade, cancellationToken);
        return Ok(Result.Ok(units));
    }

    /// <summary>
    /// 获取年级单元树形结构
    /// </summary>
    [HttpGet("tree")]
    public async Task<ActionResult<Result>> GetGradeUnitTree(CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        var tree = await _gradeUnitService.GetGradeUnitTreeAsync(userId, cancellationToken);
        return Ok(Result.Ok(tree));
    }
}
