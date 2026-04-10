using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("tb_user");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.Username).IsUnique();
        builder.Property(e => e.Username).HasColumnName("username");
        builder.Property(e => e.PasswordHash).HasColumnName("password_hash");
        builder.Property(e => e.Phone).HasColumnName("phone");
        builder.Property(e => e.StudentName).HasColumnName("student_name");
        builder.Property(e => e.GradeLevel).HasColumnName("grade_level");
        builder.Property(e => e.AvatarUrl).HasColumnName("avatar_url");
        builder.Property(e => e.IsActive).HasColumnName("is_active");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
        builder.Property(e => e.UpdatedAt).HasColumnName("updated_at");
    }
}
