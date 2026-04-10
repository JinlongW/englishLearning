using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class UserProfileConfiguration : IEntityTypeConfiguration<UserProfile>
{
    public void Configure(EntityTypeBuilder<UserProfile> builder)
    {
        builder.ToTable("tb_user_profile");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId).IsUnique();
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.LearningStyle).HasColumnName("learning_style");
        builder.Property(e => e.DifficultyLevel).HasColumnName("difficulty_level");
        builder.Property(e => e.PreferredStudyTime).HasColumnName("preferred_study_time");
        builder.Property(e => e.ParentNotifyEnabled).HasColumnName("parent_notify_enabled");
        builder.Property(e => e.TotalLearningDays).HasColumnName("total_learning_days");
        builder.Property(e => e.CurrentStreak).HasColumnName("current_streak");
        builder.Property(e => e.MaxStreak).HasColumnName("max_streak");
    }
}
