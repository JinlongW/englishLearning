using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class UserBadgeConfiguration : IEntityTypeConfiguration<UserBadge>
{
    public void Configure(EntityTypeBuilder<UserBadge> builder)
    {
        builder.ToTable("tb_user_badge");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => e.BadgeId);
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.BadgeId).HasColumnName("badge_id");
        builder.Property(e => e.EarnedAt).HasColumnName("earned_at");
        builder.Property(e => e.IsNew).HasColumnName("is_new");
    }
}
