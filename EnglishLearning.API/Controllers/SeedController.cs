using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Infrastructure.SeedData;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 数据导入控制器（仅用于开发环境）
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class SeedController : ControllerBase
{
    private readonly AppDbContext _context;
    private readonly IConfiguration _configuration;
    private readonly IWebHostEnvironment _environment;

    public SeedController(AppDbContext context, IConfiguration configuration, IWebHostEnvironment environment)
    {
        _context = context;
        _configuration = configuration;
        _environment = environment;
    }

    /// <summary>
    /// 导入人教版小学英语题库数据
    /// </summary>
    [HttpPost("import-textbook-data")]
    public async Task<IActionResult> ImportTextbookData()
    {
        // 仅允许在开发环境下执行
        if (!_environment.IsDevelopment())
        {
            return Forbid();
        }

        try
        {
            var connectionString = _configuration.GetConnectionString("DefaultConnection")
                ?? throw new InvalidOperationException("DefaultConnection 未配置");
            var seeder = new SqlSeeder(connectionString);
            seeder.Run();

            return Ok(new { success = true, message = "数据导入成功！" });
        }
        catch (Exception ex)
        {
            return BadRequest(new { success = false, message = $"导入失败：{ex.Message}" });
        }
    }

    /// <summary>
    /// 检查当前题库数据统计
    /// </summary>
    [HttpGet("stats")]
    public async Task<IActionResult> GetStats()
    {
        var gradeUnitCount = await _context.GradeUnits.CountAsync();
        var wordCount = await _context.Words.CountAsync();
        var grammarCount = await _context.Grammars.CountAsync();
        var questionCount = await _context.Questions.CountAsync();

        return Ok(new
        {
            success = true,
            data = new
            {
                gradeUnits = gradeUnitCount,
                words = wordCount,
                grammars = grammarCount,
                questions = questionCount
            }
        });
    }

    /// <summary>
    /// 更新单词音频 URL（使用有道词典发音 API）
    /// </summary>
    [HttpPost("update-audio-urls")]
    public IActionResult UpdateAudioUrls()
    {
        try
        {
            var connectionString = _configuration.GetConnectionString("DefaultConnection")
                ?? throw new InvalidOperationException("DefaultConnection 未配置");
            var seeder = new SqlSeeder(connectionString);
            seeder.UpdateWordAudioUrls();

            return Ok(new { success = true, message = "音频 URL 更新成功！" });
        }
        catch (Exception ex)
        {
            return BadRequest(new { success = false, message = $"更新失败：{ex.Message}" });
        }
    }
}
