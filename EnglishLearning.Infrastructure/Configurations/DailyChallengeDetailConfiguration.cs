using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class DailyChallengeDetailConfiguration : IEntityTypeConfiguration<DailyChallengeDetail>
{
    public void Configure(EntityTypeBuilder<DailyChallengeDetail> builder)
    {
        builder.ToTable("tb_daily_challenge_detail");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.DailyChallengeId);
        builder.HasIndex(e => e.QuestionId);
        builder.Property(e => e.DailyChallengeId).HasColumnName("daily_challenge_id");
        builder.Property(e => e.QuestionId).HasColumnName("question_id");
        builder.Property(e => e.QuestionOrder).HasColumnName("question_order");
        builder.Property(e => e.UserAnswer).HasColumnName("user_answer");
        builder.Property(e => e.IsCorrect).HasColumnName("is_correct");
        builder.Property(e => e.TimeUsedSeconds).HasColumnName("time_used_seconds");
        builder.Property(e => e.IsUncertain).HasColumnName("is_uncertain");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
