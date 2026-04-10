using EnglishLearning.API.Middleware;
using Serilog;

namespace EnglishLearning.API.Extensions;

/// <summary>
/// 应用扩展
/// </summary>
public static class AppExtensions
{
    public static IApplicationBuilder UseAppMiddleware(this IApplicationBuilder app)
    {
        // 全局异常处理
        app.UseMiddleware<ExceptionHandlerMiddleware>();

        // 请求日志
        app.UseSerilogRequestLogging();

        // 认证中间件
        app.UseAuthentication();
        app.UseAuthorization();

        return app;
    }
}
