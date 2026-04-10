using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace EnglishLearning.API.Filters;

/// <summary>
/// 全局 ModelState 验证过滤器
/// </summary>
public class ValidateModelAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext context)
    {
        if (!context.ModelState.IsValid)
        {
            var errors = context.ModelState
                .Where(ms => ms.Value?.Errors.Count > 0)
                .SelectMany(ms => ms.Value!.Errors.Select(e => new
                {
                    field = ms.Key,
                    message = e.ErrorMessage
                }))
                .ToList();

            context.Result = new BadRequestObjectResult(new
            {
                success = false,
                message = "请求参数验证失败",
                code = 400,
                errors = errors
            });
        }

        base.OnActionExecuting(context);
    }
}
