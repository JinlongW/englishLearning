using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class UserLevelConfiguration : IEntityTypeConfiguration<UserLevel>
{
    public void Configure(EntityTypeBuilder<UserLevel> builder)
    {
        builder.ToTable("tb_user_level");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId).IsUnique();
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.CurrentLevel).HasColumnName("current_level");
        builder.Property(e => e.LevelName).HasColumnName("level_name");
        builder.Property(e => e.CurrentExp).HasColumnName("current_exp");
        builder.Property(e => e.ExpToNext).HasColumnName("exp_to_next");
        builder.Property(e => e.LevelUpAt).HasColumnName("level_up_at");
        builder.Property(e => e.UpdatedAt).HasColumnName("updated_at");
    }
}
