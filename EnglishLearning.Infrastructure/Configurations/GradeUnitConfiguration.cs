using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class GradeUnitConfiguration : IEntityTypeConfiguration<GradeUnit>
{
    public void Configure(EntityTypeBuilder<GradeUnit> builder)
    {
        builder.ToTable("tb_grade_unit");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => new { e.Grade, e.Semester, e.UnitNo }).IsUnique();
        builder.Property(e => e.Grade).HasColumnName("grade");
        builder.Property(e => e.Semester).HasColumnName("semester");
        builder.Property(e => e.UnitNo).HasColumnName("unit_no");
        builder.Property(e => e.UnitName).HasColumnName("unit_name");
        builder.Property(e => e.SortOrder).HasColumnName("sort_order");
        builder.Property(e => e.IsLocked).HasColumnName("is_locked");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
    }
}
