using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class DailyChallengeConfiguration : IEntityTypeConfiguration<DailyChallenge>
{
    public void Configure(EntityTypeBuilder<DailyChallenge> builder)
    {
        builder.ToTable("tb_daily_challenge");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => new { e.UserId, e.ChallengeDate }).IsUnique();
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.ChallengeDate).HasColumnName("challenge_date");
        builder.Property(e => e.Status).HasColumnName("status");
        builder.Property(e => e.TotalQuestions).HasColumnName("total_questions");
        builder.Property(e => e.CorrectCount).HasColumnName("correct_count");
        builder.Property(e => e.Score).HasColumnName("score");
        builder.Property(e => e.TimeUsedSeconds).HasColumnName("time_used_seconds");
        builder.Property(e => e.PointsEarned).HasColumnName("points_earned");
        builder.Property(e => e.CoinsEarned).HasColumnName("coins_earned");
        builder.Property(e => e.StartedAt).HasColumnName("started_at");
        builder.Property(e => e.CompletedAt).HasColumnName("completed_at");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
