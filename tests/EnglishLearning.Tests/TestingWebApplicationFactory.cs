using EnglishLearning.API;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.Hosting;

namespace EnglishLearning.Tests;

/// <summary>
/// 自定义 Web 应用程序工厂，用于配置测试环境
/// </summary>
public class TestingWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseSetting("RateLimiter:Enabled", "false");
    }
}
