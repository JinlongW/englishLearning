using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace Microsoft.Extensions.DependencyInjection;

/// <summary>
/// 服务注册扩展
/// </summary>
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services, IConfiguration configuration)
    {
        // 数据库上下文
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection")));

        // 仓储
        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
        services.AddScoped<IUnitOfWork, UnitOfWork>();

        // 基础设施
        services.AddScoped<IPasswordHasher, BCryptPasswordHasher>();
        services.AddScoped<IJwtTokenGenerator, JwtTokenGenerator>();

        // 业务服务
        services.AddScoped<IAuthService, AuthService>();
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IWordService, WordService>();
        services.AddScoped<IGrammarService, GrammarService>();
        services.AddScoped<IQuestionService, QuestionService>();
        services.AddScoped<IChallengeService, ChallengeService>();
        services.AddScoped<IWrongQuestionService, WrongQuestionService>();
        services.AddScoped<IBadgeService, BadgeService>();
        services.AddScoped<IPointsService, PointsService>();
        services.AddScoped<IGradeUnitService, GradeUnitService>();

        return services;
    }
}
