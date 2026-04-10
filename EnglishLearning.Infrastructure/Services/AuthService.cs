using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Entities;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Infrastructure.Data;
using EnglishLearning.Shared.Constants;
using EnglishLearning.Shared.Exceptions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace EnglishLearning.Infrastructure.Services;

/// <summary>
/// 认证服务实现
/// </summary>
public class AuthService : IAuthService
{
    private readonly AppDbContext _context;
    private readonly IConfiguration _configuration;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtTokenGenerator _tokenGenerator;

    public AuthService(
        AppDbContext context,
        IConfiguration configuration,
        IPasswordHasher passwordHasher,
        IJwtTokenGenerator tokenGenerator)
    {
        _context = context;
        _configuration = configuration;
        _passwordHasher = passwordHasher;
        _tokenGenerator = tokenGenerator;
    }

    /// <summary>
    /// 用户登录
    /// </summary>
    public async Task<(string token, UserInfoDto user)> LoginAsync(string username, string password, CancellationToken cancellationToken = default)
    {
        // 查找用户
        var user = await _context.Users
            .Include(u => u.Profile)
            .Include(u => u.Level)
            .FirstOrDefaultAsync(u => u.Username == username && u.IsActive, cancellationToken);

        if (user == null)
        {
            throw new BusinessException("用户不存在", 1002);
        }

        // 验证密码
        if (!_passwordHasher.Verify(password, user.PasswordHash))
        {
            throw new BusinessException("用户名或密码错误", 1002);
        }

        // 生成 JWT Token
        var token = _tokenGenerator.GenerateToken(user);

        // 构建用户信息
        var userInfo = await BuildUserInfoAsync(user, cancellationToken);

        return (token, userInfo);
    }

    /// <summary>
    /// 用户注册
    /// </summary>
    public async Task<UserInfoDto> RegisterAsync(RegisterRequest request, CancellationToken cancellationToken = default)
    {
        // 检查用户名是否已存在
        var existingUser = await _context.Users
            .FirstOrDefaultAsync(u => u.Username == request.Username, cancellationToken);

        if (existingUser != null)
        {
            throw new BusinessException("用户名已存在", 1003);
        }

        // 创建用户
        var now = DateTime.UtcNow;
        var user = new User
        {
            Id = Guid.NewGuid(),
            Username = request.Username,
            PasswordHash = _passwordHasher.Hash(request.Password),
            StudentName = request.StudentName,
            GradeLevel = request.GradeLevel,
            Phone = request.Phone,
            IsActive = true,
            CreatedAt = now,
            UpdatedAt = now
        };

        await _context.Users.AddAsync(user, cancellationToken);

        // 创建用户画像
        var profile = new UserProfile
        {
            Id = Guid.NewGuid(),
            UserId = user.Id,
            LearningStyle = null,
            DifficultyLevel = 1,
            PreferredStudyTime = null,
            ParentNotifyEnabled = true,
            TotalLearningDays = 0,
            CurrentStreak = 0,
            MaxStreak = 0
        };
        await _context.UserProfiles.AddAsync(profile, cancellationToken);

        // 创建用户等级
        var levelInfo = LevelConfig.GetLevelInfo(1);
        var userLevel = new UserLevel
        {
            Id = Guid.NewGuid(),
            UserId = user.Id,
            CurrentLevel = 1,
            LevelName = levelInfo.Name,
            CurrentExp = 0,
            ExpToNext = LevelConfig.GetExpToNext(1),
            LevelUpAt = now,
            UpdatedAt = now
        };
        await _context.UserLevels.AddAsync(userLevel, cancellationToken);

        await _context.SaveChangesAsync(cancellationToken);

        return await BuildUserInfoAsync(user, cancellationToken);
    }

    /// <summary>
    /// 获取用户信息
    /// </summary>
    public async Task<UserInfoDto> GetUserInfoAsync(Guid userId, CancellationToken cancellationToken = default)
    {
        var user = await _context.Users
            .Include(u => u.Profile)
            .Include(u => u.Level)
            .FirstOrDefaultAsync(u => u.Id == userId, cancellationToken);

        if (user == null)
        {
            throw new BusinessException("用户不存在", 404);
        }

        return await BuildUserInfoAsync(user, cancellationToken);
    }

    /// <summary>
    /// 构建用户信息 DTO
    /// </summary>
    private async Task<UserInfoDto> BuildUserInfoAsync(User user, CancellationToken cancellationToken = default)
    {
        // 获取积分和金币余额
        var pointsBalance = await _context.UserPoints
            .Where(p => p.UserId == user.Id && p.PointsType == "points")
            .SumAsync(p => p.ChangeAmount, cancellationToken);

        var coinsBalance = await _context.UserPoints
            .Where(p => p.UserId == user.Id && p.PointsType == "coins")
            .SumAsync(p => p.ChangeAmount, cancellationToken);

        return new UserInfoDto
        {
            Id = user.Id,
            Username = user.Username,
            StudentName = user.StudentName,
            GradeLevel = user.GradeLevel,
            AvatarUrl = user.AvatarUrl,
            CurrentStreak = user.Profile?.CurrentStreak ?? 0,
            CurrentLevel = user.Level?.CurrentLevel ?? 1,
            LevelName = user.Level?.LevelName ?? "英语小白",
            CurrentExp = user.Level?.CurrentExp ?? 0,
            TotalPoints = pointsBalance,
            TotalCoins = coinsBalance
        };
    }
}

/// <summary>
/// 密码哈希接口
/// </summary>
public interface IPasswordHasher
{
    string Hash(string password);
    bool Verify(string password, string hash);
}

/// <summary>
/// 密码哈希实现 (BCrypt)
/// </summary>
public class BCryptPasswordHasher : IPasswordHasher
{
    public string Hash(string password)
    {
        return BCrypt.Net.BCrypt.HashPassword(password);
    }

    public bool Verify(string password, string hash)
    {
        return BCrypt.Net.BCrypt.Verify(password, hash);
    }
}

/// <summary>
/// JWT Token 生成接口
/// </summary>
public interface IJwtTokenGenerator
{
    string GenerateToken(User user);
}

/// <summary>
/// JWT Token 生成实现
/// </summary>
public class JwtTokenGenerator : IJwtTokenGenerator
{
    private readonly IConfiguration _configuration;

    public JwtTokenGenerator(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public string GenerateToken(User user)
    {
        var jwtSettings = _configuration.GetSection("JwtSettings");
        var secretKey = jwtSettings["SecretKey"]
            ?? throw new InvalidOperationException("JwtSettings:SecretKey is not configured.");
        var issuer = jwtSettings["Issuer"] ?? "EnglishLearning";
        var audience = jwtSettings["Audience"] ?? "EnglishLearning";
        var expirationMinutes = int.Parse(jwtSettings["ExpirationMinutes"] ?? "120");

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.Username),
            new Claim("studentName", user.StudentName),
            new Claim("gradeLevel", user.GradeLevel.ToString())
        };

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(expirationMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
