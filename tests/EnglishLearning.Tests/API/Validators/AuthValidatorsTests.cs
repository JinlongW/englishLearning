using EnglishLearning.API.Validators;
using EnglishLearning.Domain.DTOs;
using FluentAssertions;
using FluentValidation;
using FluentValidation.TestHelper;

namespace EnglishLearning.Tests.API.Validators;

public class AuthValidatorsTests
{
    private readonly LoginRequestValidator _loginValidator;
    private readonly RegisterRequestValidator _registerValidator;

    public AuthValidatorsTests()
    {
        _loginValidator = new LoginRequestValidator();
        _registerValidator = new RegisterRequestValidator();
    }

    #region LoginRequestValidator Tests

    [Fact]
    public void LoginRequestValidator_ValidRequest_PassesValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "testuser",
            Password = "123456"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveAnyValidationErrors();
    }

    [Fact]
    public void LoginRequestValidator_EmptyUsername_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "",
            Password = "123456"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名不能为空");
    }

    [Fact]
    public void LoginRequestValidator_UsernameTooShort_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "ab",
            Password = "123456"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名至少 3 个字符");
    }

    [Fact]
    public void LoginRequestValidator_UsernameTooLong_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = new string('a', 51),
            Password = "123456"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名不能超过 50 个字符");
    }

    [Fact]
    public void LoginRequestValidator_EmptyPassword_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "testuser",
            Password = ""
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码不能为空");
    }

    [Fact]
    public void LoginRequestValidator_PasswordTooShort_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "testuser",
            Password = "12345"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码至少 6 个字符");
    }

    [Fact]
    public void LoginRequestValidator_NullUsername_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = null!,
            Password = "123456"
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名不能为空");
    }

    [Fact]
    public void LoginRequestValidator_NullPassword_FailsValidation()
    {
        // Arrange
        var request = new LoginRequest
        {
            Username = "testuser",
            Password = null!
        };

        // Act
        var result = _loginValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码不能为空");
    }

    #endregion

    #region RegisterRequestValidator Tests

    [Fact]
    public void RegisterRequestValidator_ValidRequest_PassesValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3,
            Phone = "13800138000"
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveAnyValidationErrors();
    }

    [Fact]
    public void RegisterRequestValidator_EmptyUsername_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名不能为空");
    }

    [Fact]
    public void RegisterRequestValidator_UsernameTooShort_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "ab",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名至少 3 个字符");
    }

    [Fact]
    public void RegisterRequestValidator_UsernameWithInvalidCharacters_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "test@user",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
            .WithErrorMessage("用户名只能包含字母、数字、下划线和中文");
    }

    [Fact]
    public void RegisterRequestValidator_UsernameWithValidCharacters_PassesValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "test_user123 测试",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Username);
    }

    [Fact]
    public void RegisterRequestValidator_PasswordWithoutUpperCase_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "test123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码必须包含大小写字母和数字");
    }

    [Fact]
    public void RegisterRequestValidator_PasswordWithoutLowerCase_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "TEST123456",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码必须包含大小写字母和数字");
    }

    [Fact]
    public void RegisterRequestValidator_PasswordWithoutDigit_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "TestPassword",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码必须包含大小写字母和数字");
    }

    [Fact]
    public void RegisterRequestValidator_PasswordTooShort_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123",
            StudentName = "张三",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Password)
            .WithErrorMessage("密码至少 8 个字符");
    }

    [Fact]
    public void RegisterRequestValidator_EmptyStudentName_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.StudentName)
            .WithErrorMessage("学生姓名不能为空");
    }

    [Fact]
    public void RegisterRequestValidator_StudentNameTooShort_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张",
            GradeLevel = 3
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.StudentName)
            .WithErrorMessage("学生姓名至少 2 个字符");
    }

    [Fact]
    public void RegisterRequestValidator_InvalidGradeLevel_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 13
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.GradeLevel)
            .WithErrorMessage("年级必须在 1-12 之间");
    }

    [Fact]
    public void RegisterRequestValidator_GradeLevelOutOfRange_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 0
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.GradeLevel)
            .WithErrorMessage("年级必须在 1-12 之间");
    }

    [Fact]
    public void RegisterRequestValidator_InvalidPhoneFormat_FailsValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3,
            Phone = "12345678901"
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Phone)
            .WithErrorMessage("手机号格式不正确");
    }

    [Fact]
    public void RegisterRequestValidator_ValidPhoneFormat_PassesValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3,
            Phone = "13800138000"
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Phone);
    }

    [Fact]
    public void RegisterRequestValidator_NullPhone_PassesValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3,
            Phone = null
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Phone);
    }

    [Fact]
    public void RegisterRequestValidator_EmptyPhone_PassesValidation()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Username = "testuser",
            Password = "Test123456",
            StudentName = "张三",
            GradeLevel = 3,
            Phone = ""
        };

        // Act
        var result = _registerValidator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Phone);
    }

    #endregion
}
