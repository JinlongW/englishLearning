using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class GrammarConfiguration : IEntityTypeConfiguration<Grammar>
{
    public void Configure(EntityTypeBuilder<Grammar> builder)
    {
        builder.ToTable("tb_grammar");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.GradeUnitId);
        builder.Property(e => e.GradeUnitId).HasColumnName("grade_unit_id");
        builder.Property(e => e.Title).HasColumnName("title");
        builder.Property(e => e.ContentType).HasColumnName("content_type");
        builder.Property(e => e.VideoUrl).HasColumnName("video_url");
        builder.Property(e => e.ContentJson).HasColumnName("content_json");
        builder.Property(e => e.DurationSeconds).HasColumnName("duration_seconds");
        builder.Property(e => e.SortOrder).HasColumnName("sort_order");
        builder.Property(e => e.QuizJson).HasColumnName("quiz_json");
        builder.Property(e => e.PassingScore).HasColumnName("passing_score");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
