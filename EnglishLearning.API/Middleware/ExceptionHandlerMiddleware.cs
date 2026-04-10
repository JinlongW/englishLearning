namespace EnglishLearning.API.Middleware;

/// <summary>
/// 全局异常处理中间件
/// </summary>
public class ExceptionHandlerMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlerMiddleware> _logger;

    public ExceptionHandlerMiddleware(RequestDelegate next, ILogger<ExceptionHandlerMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        _logger.LogError(exception, "发生未处理的异常");

        var response = context.Response;
        response.ContentType = "application/json";

        var result = exception switch
        {
            Shared.Exceptions.BusinessException bizEx => new Shared.Utils.Result
            {
                Success = false,
                Code = bizEx.Code,
                Message = bizEx.Message,
                Timestamp = DateTime.Now
            },
            _ => new Shared.Utils.Result
            {
                Success = false,
                Code = 500,
                Message = "服务器内部错误，请稍后重试",
                Timestamp = DateTime.Now
            }
        };

        response.StatusCode = result.Code;
        await response.WriteAsJsonAsync(result);
    }
}
