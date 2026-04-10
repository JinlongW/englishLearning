namespace EnglishLearning.Domain.DTOs;

using System.ComponentModel.DataAnnotations;

/// <summary>
/// 创建单词请求
/// </summary>
public class CreateWordRequest
{
    /// <summary>
    /// 年级单元ID
    /// </summary>
    [Required(ErrorMessage = "年级单元ID不能为空")]
    public Guid GradeUnitId { get; set; }

    /// <summary>
    /// 单词文本
    /// </summary>
    [Required(ErrorMessage = "单词文本不能为空")]
    [MaxLength(100, ErrorMessage = "单词文本不能超过100个字符")]
    public string WordText { get; set; } = string.Empty;

    /// <summary>
    /// 英式音标
    /// </summary>
    [MaxLength(50, ErrorMessage = "英式音标不能超过50个字符")]
    public string? PhoneticUk { get; set; }

    /// <summary>
    /// 美式音标
    /// </summary>
    [MaxLength(50, ErrorMessage = "美式音标不能超过50个字符")]
    public string? PhoneticUs { get; set; }

    /// <summary>
    /// 音频URL
    /// </summary>
    [MaxLength(500, ErrorMessage = "音频URL不能超过500个字符")]
    public string? AudioUrl { get; set; }

    /// <summary>
    /// 中文释义
    /// </summary>
    [Required(ErrorMessage = "中文释义不能为空")]
    [MaxLength(500, ErrorMessage = "中文释义不能超过500个字符")]
    public string MeaningCn { get; set; } = string.Empty;

    /// <summary>
    /// 词性
    /// </summary>
    [MaxLength(50, ErrorMessage = "词性不能超过50个字符")]
    public string? PartOfSpeech { get; set; }

    /// <summary>
    /// 例句（英文）
    /// </summary>
    [MaxLength(1000, ErrorMessage = "英文例句不能超过1000个字符")]
    public string? ExampleEn { get; set; }

    /// <summary>
    /// 例句（中文）
    /// </summary>
    [MaxLength(1000, ErrorMessage = "中文例句不能超过1000个字符")]
    public string? ExampleCn { get; set; }

    /// <summary>
    /// 图片URL
    /// </summary>
    [MaxLength(500, ErrorMessage = "图片URL不能超过500个字符")]
    public string? ImageUrl { get; set; }

    /// <summary>
    /// 排序顺序
    /// </summary>
    public int SortOrder { get; set; }
}
