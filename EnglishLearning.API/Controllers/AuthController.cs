using EnglishLearning.Domain.DTOs;
using EnglishLearning.Domain.Interfaces;
using EnglishLearning.Shared.Utils;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using System.Security.Claims;
using FluentValidation;

namespace EnglishLearning.API.Controllers;

/// <summary>
/// 认证控制器
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class AuthController : ControllerBase
{
    private readonly IAuthService _authService;
    private readonly IValidator<LoginRequest> _loginValidator;
    private readonly IValidator<RegisterRequest> _registerValidator;

    public AuthController(IAuthService authService, IValidator<LoginRequest> loginValidator, IValidator<RegisterRequest> registerValidator)
    {
        _authService = authService;
        _loginValidator = loginValidator;
        _registerValidator = registerValidator;
    }

    /// <summary>
    /// 用户登录
    /// </summary>
    [HttpPost("login")]
    [AllowAnonymous]
    [EnableRateLimiting("auth")]
    public async Task<ActionResult<Result>> Login([FromBody] LoginRequest request, CancellationToken cancellationToken)
    {
        var validationResult = await _loginValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return BadRequest(Result.Error(validationResult.Errors.First().ErrorMessage, 400));
        }

        try
        {
            var (token, user) = await _authService.LoginAsync(request.Username, request.Password, cancellationToken);

            return Ok(Result.Ok(new LoginResponse
            {
                Token = token,
                User = user,
                ExpiresIn = 7200
            }, "登录成功"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 用户注册
    /// </summary>
    [HttpPost("register")]
    [AllowAnonymous]
    [EnableRateLimiting("auth")]
    public async Task<ActionResult<Result>> Register([FromBody] RegisterRequest request, CancellationToken cancellationToken)
    {
        var validationResult = await _registerValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return BadRequest(Result.Error(validationResult.Errors.First().ErrorMessage, 400));
        }

        try
        {
            var user = await _authService.RegisterAsync(request, cancellationToken);

            return Ok(Result.Ok(new
            {
                userId = user.Id,
                username = user.Username
            }, "注册成功"));
        }
        catch (Shared.Exceptions.BusinessException ex)
        {
            return StatusCode(ex.HttpStatusCode, Result.Error(ex.Message, ex.Code));
        }
    }

    /// <summary>
    /// 获取当前用户信息
    /// </summary>
    [HttpGet("me")]
    [Authorize]
    public async Task<ActionResult<Result>> GetCurrentUser(CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        var user = await _authService.GetUserInfoAsync(userId, cancellationToken);

        return Ok(Result.Ok(user));
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
