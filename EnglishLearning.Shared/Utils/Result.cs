namespace EnglishLearning.Shared.Utils;

/// <summary>
/// 统一 API 响应结果
/// </summary>
public class Result
{
    public bool Success { get; set; }
    public int Code { get; set; }
    public string Message { get; set; } = string.Empty;
    public object? Data { get; set; }
    public DateTime Timestamp { get; set; }

    public static Result Ok(object? data = null, string message = "操作成功")
    {
        return new Result
        {
            Success = true,
            Code = 200,
            Message = message,
            Data = data,
            Timestamp = DateTime.Now
        };
    }

    public static Result Error(string message, int code = 500)
    {
        return new Result
        {
            Success = false,
            Code = code,
            Message = message,
            Timestamp = DateTime.Now
        };
    }

    public static Result NotFound(string message = "资源不存在")
    {
        return new Result
        {
            Success = false,
            Code = 404,
            Message = message,
            Timestamp = DateTime.Now
        };
    }

    public static Result Unauthorized(string message = "未授权")
    {
        return new Result
        {
            Success = false,
            Code = 401,
            Message = message,
            Timestamp = DateTime.Now
        };
    }
}

/// <summary>
/// 分页结果
/// </summary>
public class PageResult<T>
{
    public List<T> Items { get; set; } = new();
    public int Total { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling(Total / (double)PageSize);

    public static PageResult<T> Create(List<T> items, int total, int page, int pageSize)
    {
        return new PageResult<T>
        {
            Items = items,
            Total = total,
            Page = page,
            PageSize = pageSize
        };
    }
}
