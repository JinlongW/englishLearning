using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class BadgeConfiguration : IEntityTypeConfiguration<Badge>
{
    public void Configure(EntityTypeBuilder<Badge> builder)
    {
        builder.ToTable("tb_badge");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.BadgeCode).IsUnique();
        builder.Property(e => e.BadgeCode).HasColumnName("badge_code");
        builder.Property(e => e.BadgeName).HasColumnName("badge_name");
        builder.Property(e => e.BadgeIcon).HasColumnName("badge_icon");
        builder.Property(e => e.BadgeType).HasColumnName("badge_type");
        builder.Property(e => e.Description).HasColumnName("description");
        builder.Property(e => e.RequirementJson).HasColumnName("requirement_json");
        builder.Property(e => e.SortOrder).HasColumnName("sort_order");
        builder.Property(e => e.IsActive).HasColumnName("is_active");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
