namespace EnglishLearning.API.Validators;

using FluentValidation;
using EnglishLearning.Domain.DTOs;

/// <summary>
/// 注册请求验证器
/// </summary>
public class RegisterRequestValidator : AbstractValidator<RegisterRequest>
{
    public RegisterRequestValidator()
    {
        RuleFor(x => x.Username)
            .NotEmpty().WithMessage("用户名不能为空")
            .MinimumLength(3).WithMessage("用户名至少 3 个字符")
            .MaximumLength(50).WithMessage("用户名不能超过 50 个字符")
            .Matches(@"^[a-zA-Z0-9_\u4e00-\u9fa5]+$").WithMessage("用户名只能包含字母、数字、下划线和中文");

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("密码不能为空")
            .MinimumLength(8).WithMessage("密码至少 8 个字符")
            .MaximumLength(100).WithMessage("密码不能超过 100 个字符")
            .Matches(@"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)").WithMessage("密码必须包含大小写字母和数字");

        RuleFor(x => x.StudentName)
            .NotEmpty().WithMessage("学生姓名不能为空")
            .MinimumLength(2).WithMessage("学生姓名至少 2 个字符")
            .MaximumLength(100).WithMessage("学生姓名不能超过 100 个字符");

        RuleFor(x => x.GradeLevel)
            .InclusiveBetween(1, 12).WithMessage("年级必须在 1-12 之间");

        RuleFor(x => x.Phone)
            .Matches(@"^1[3-9]\d{9}$").When(x => !string.IsNullOrEmpty(x.Phone))
            .WithMessage("手机号格式不正确");
    }
}

/// <summary>
/// 登录请求验证器
/// </summary>
public class LoginRequestValidator : AbstractValidator<LoginRequest>
{
    public LoginRequestValidator()
    {
        RuleFor(x => x.Username)
            .NotEmpty().WithMessage("用户名不能为空")
            .MinimumLength(3).WithMessage("用户名至少 3 个字符")
            .MaximumLength(50).WithMessage("用户名不能超过 50 个字符");

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("密码不能为空")
            .MinimumLength(6).WithMessage("密码至少 6 个字符")
            .MaximumLength(100).WithMessage("密码不能超过 100 个字符");
    }
}

/// <summary>
/// 提交答案请求验证器
/// </summary>
public class SubmitAnswerRequestValidator : AbstractValidator<SubmitAnswerRequest>
{
    public SubmitAnswerRequestValidator()
    {
        RuleFor(x => x.UserAnswer)
            .NotEmpty().WithMessage("答案不能为空")
            .MaximumLength(1000).WithMessage("答案不能超过 1000 个字符");

        RuleFor(x => x.TimeUsedSeconds)
            .GreaterThanOrEqualTo(0).WithMessage("用时不能为负数");
    }
}

/// <summary>
/// 挑战答案请求验证器
/// </summary>
public class ChallengeAnswerRequestValidator : AbstractValidator<ChallengeAnswerRequest>
{
    public ChallengeAnswerRequestValidator()
    {
        RuleFor(x => x.QuestionId)
            .NotEmpty().WithMessage("题目 ID 不能为空");

        RuleFor(x => x.UserAnswer)
            .NotEmpty().WithMessage("答案不能为空")
            .MaximumLength(1000).WithMessage("答案不能超过 1000 个字符");

        RuleFor(x => x.TimeUsedSeconds)
            .GreaterThanOrEqualTo(0).WithMessage("用时不能为负数");
    }
}

/// <summary>
/// 更新进度请求验证器
/// </summary>
public class UpdateProgressRequestValidator : AbstractValidator<UpdateProgressRequest>
{
    public UpdateProgressRequestValidator()
    {
        RuleFor(x => x.Score)
            .GreaterThanOrEqualTo(0).WithMessage("分数不能为负数")
            .LessThanOrEqualTo(100).WithMessage("分数不能超过 100");

        RuleFor(x => x.Status)
            .NotEmpty().WithMessage("状态不能为空");
    }
}
