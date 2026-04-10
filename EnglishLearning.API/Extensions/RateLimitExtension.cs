using Microsoft.AspNetCore.RateLimiting;
using System.Threading.RateLimiting;

namespace EnglishLearning.API.Extensions;

/// <summary>
/// 速率限制扩展
/// </summary>
public static class RateLimitExtension
{
    public static IServiceCollection AddRateLimiting(this IServiceCollection services, IConfiguration? configuration = null)
    {
        // 检查是否启用了速率限制（默认启用）
        var isEnabled = configuration?.GetValue<bool>("RateLimiter:Enabled", true) ?? true;

        if (!isEnabled)
        {
            return services;
        }

        services.AddRateLimiter(options =>
        {
            // 全局速率限制：每个 IP 每秒最多 10 个请求
            options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(
                httpContext => RateLimitPartition.GetFixedWindowLimiter(
                    partitionKey: httpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown",
                    factory: _ => new FixedWindowRateLimiterOptions
                    {
                        PermitLimit = 10,
                        Window = TimeSpan.FromSeconds(1)
                    }));

            // 认证端点单独限制：每个 IP 每分钟最多 5 次登录尝试
            options.AddPolicy("auth", httpContext =>
                RateLimitPartition.GetFixedWindowLimiter(
                    partitionKey: httpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown",
                    factory: _ => new FixedWindowRateLimiterOptions
                    {
                        PermitLimit = 5,
                        Window = TimeSpan.FromMinutes(1)
                    }));

            // 拒绝时的响应
            options.OnRejected = async (context, token) =>
            {
                context.HttpContext.Response.StatusCode = 429;
                context.HttpContext.Response.Headers.ContentType = "application/json";

                var response = new
                {
                    success = false,
                    message = "请求过于频繁，请稍后再试",
                    code = 429
                };

                await context.HttpContext.Response.WriteAsJsonAsync(response, cancellationToken: token);
            };
        });

        return services;
    }
}
