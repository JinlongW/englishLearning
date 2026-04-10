using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class UserPointsConfiguration : IEntityTypeConfiguration<UserPoints>
{
    public void Configure(EntityTypeBuilder<UserPoints> builder)
    {
        builder.ToTable("tb_user_points");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => new { e.UserId, e.PointsType });
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.PointsType).HasColumnName("points_type");
        builder.Property(e => e.ChangeType).HasColumnName("change_type");
        builder.Property(e => e.ChangeAmount).HasColumnName("change_amount");
        builder.Property(e => e.BalanceAfter).HasColumnName("balance_after");
        builder.Property(e => e.Description).HasColumnName("description");
        builder.Property(e => e.ReferenceId).HasColumnName("reference_id");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
