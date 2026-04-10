using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class CheckinConfiguration : IEntityTypeConfiguration<Checkin>
{
    public void Configure(EntityTypeBuilder<Checkin> builder)
    {
        builder.ToTable("tb_checkin");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => new { e.UserId, e.CheckinDate }).IsUnique();
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.CheckinDate).HasColumnName("checkin_date");
        builder.Property(e => e.PointsEarned).HasColumnName("points_earned");
        builder.Property(e => e.StreakDays).HasColumnName("streak_days");
        builder.Property(e => e.BonusPoints).HasColumnName("bonus_points");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
