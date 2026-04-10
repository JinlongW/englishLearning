using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class QuestionOptionConfiguration : IEntityTypeConfiguration<QuestionOption>
{
    public void Configure(EntityTypeBuilder<QuestionOption> builder)
    {
        builder.ToTable("tb_question_option");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.QuestionId);
        builder.Property(e => e.QuestionId).HasColumnName("question_id");
        builder.Property(e => e.OptionKey).HasColumnName("option_key");
        builder.Property(e => e.OptionContent).HasColumnName("option_content");
        builder.Property(e => e.ImageUrl).HasColumnName("image_url");
        builder.Property(e => e.AudioUrl).HasColumnName("audio_url");
        builder.Property(e => e.SortOrder).HasColumnName("sort_order");
    }
}
