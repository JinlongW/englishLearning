using EnglishLearning.API.Extensions;
using EnglishLearning.Infrastructure.Data;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using FluentValidation;

var builder = WebApplication.CreateBuilder(args);

// 添加 Serilog
builder.Host.UseSerilog((context, services, configuration) => configuration
    .ReadFrom.Configuration(context.Configuration)
    .ReadFrom.Services(services));

// 添加应用服务
builder.Services.AddApplicationServices(builder.Configuration);
builder.Services.AddControllers(options =>
{
    // 添加全局 ModelState 验证过滤器
    options.Filters.Add<EnglishLearning.API.Filters.ValidateModelAttribute>();
})
.AddJsonOptions(options =>
{
    // 使用 camelCase 命名 JSON 属性，适配前端
    options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
});
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "英语学习工具 API", Version = "v1" });
    c.AddSecurityDefinition("Bearer", new Microsoft.OpenApi.Models.OpenApiSecurityScheme
    {
        Type = Microsoft.OpenApi.Models.SecuritySchemeType.ApiKey,
        Name = "Authorization",
        In = Microsoft.OpenApi.Models.ParameterLocation.Header,
        Description = "JWT 认证，格式：Bearer {token}"
    });
});

// 添加 JWT 认证
builder.Services.AddJwtAuthentication(builder.Configuration, builder.Environment.IsDevelopment());

// 添加速率限制
builder.Services.AddRateLimiting(builder.Configuration);

// 添加 FluentValidation (手动验证)
builder.Services.AddValidatorsFromAssemblyContaining<EnglishLearning.API.Validators.RegisterRequestValidator>();

// 添加 CORS - 限制为已知前端域名
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins(
                builder.Configuration.GetSection("AllowedOrigins").Get<string[]>()
                ?? new[] { "http://localhost:5173", "http://localhost:3000" }
            )
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials(); // 允许携带 Cookie
    });
});

var app = builder.Build();

// 配置中间件
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowFrontend");

// 仅在启用速率限制时使用
if (builder.Configuration.GetValue<bool>("RateLimiter:Enabled", true))
{
    app.UseRateLimiter();
}

app.UseAppMiddleware();
app.MapControllers();

try
{
    Log.Information("服务启动中...");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "服务启动失败");
}
finally
{
    Log.CloseAndFlush();
}

// 为了集成测试公开 Program 类
public partial class Program { }
