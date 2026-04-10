namespace EnglishLearning.Shared.Exceptions;

/// <summary>
/// 业务异常
/// </summary>
public class BusinessException : Exception
{
    public int Code { get; set; }

    /// <summary>
    /// 对应的 HTTP 状态码
    /// </summary>
    public int HttpStatusCode { get; set; } = 200;

    public BusinessException(string message, int code = 1001, int httpStatusCode = 200) : base(message)
    {
        Code = code;
        HttpStatusCode = httpStatusCode;
    }

    public BusinessException(string message, Exception innerException, int code = 1001, int httpStatusCode = 200)
        : base(message, innerException)
    {
        Code = code;
        HttpStatusCode = httpStatusCode;
    }

    /// <summary>
    /// 创建 BadRequest 异常 (HTTP 400)
    /// </summary>
    public static BusinessException BadRequest(string message, int code = 4001)
        => new(message, code, 400);

    /// <summary>
    /// 创建 Unauthorized 异常 (HTTP 401)
    /// </summary>
    public static BusinessException Unauthorized(string message, int code = 4011)
        => new(message, code, 401);

    /// <summary>
    /// 创建 Forbidden 异常 (HTTP 403)
    /// </summary>
    public static BusinessException Forbidden(string message, int code = 4031)
        => new(message, code, 403);

    /// <summary>
    /// 创建 NotFound 异常 (HTTP 404)
    /// </summary>
    public static BusinessException NotFound(string message, int code = 4041)
        => new(message, code, 404);

    /// <summary>
    /// 创建 Conflict 异常 (HTTP 409)
    /// </summary>
    public static BusinessException Conflict(string message, int code = 4091)
        => new(message, code, 409);

    /// <summary>
    /// 创建 InternalServerError 异常 (HTTP 500)
    /// </summary>
    public static BusinessException InternalServerError(string message, int code = 5001)
        => new(message, code, 500);
}
