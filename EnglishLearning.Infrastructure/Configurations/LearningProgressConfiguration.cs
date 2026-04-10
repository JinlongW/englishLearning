using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class LearningProgressConfiguration : IEntityTypeConfiguration<LearningProgress>
{
    public void Configure(EntityTypeBuilder<LearningProgress> builder)
    {
        builder.ToTable("tb_learning_progress");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => e.GradeUnitId);
        builder.HasIndex(e => new { e.UserId, e.ContentType, e.ContentId });
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.GradeUnitId).HasColumnName("grade_unit_id");
        builder.Property(e => e.ContentType).HasColumnName("content_type");
        builder.Property(e => e.ContentId).HasColumnName("content_id");
        builder.Property(e => e.Status).HasColumnName("status");
        builder.Property(e => e.Score).HasColumnName("score");
        builder.Property(e => e.AttemptsCount).HasColumnName("attempts_count");
        builder.Property(e => e.LastAttemptAt).HasColumnName("last_attempt_at");
        builder.Property(e => e.CompletedAt).HasColumnName("completed_at");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
        builder.Property(e => e.UpdatedAt).HasColumnName("updated_at");
    }
}
