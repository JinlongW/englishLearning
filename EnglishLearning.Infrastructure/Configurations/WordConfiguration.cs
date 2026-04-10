using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class WordConfiguration : IEntityTypeConfiguration<Word>
{
    public void Configure(EntityTypeBuilder<Word> builder)
    {
        builder.ToTable("tb_word");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.GradeUnitId);
        builder.HasIndex(e => new { e.GradeUnitId, e.SortOrder });
        builder.Property(e => e.GradeUnitId).HasColumnName("grade_unit_id");
        builder.Property(e => e.WordText).HasColumnName("word");
        builder.Property(e => e.PhoneticUk).HasColumnName("phonetic_uk");
        builder.Property(e => e.PhoneticUs).HasColumnName("phonetic_us");
        builder.Property(e => e.AudioUrl).HasColumnName("audio_url");
        builder.Property(e => e.MeaningCn).HasColumnName("meaning_cn");
        builder.Property(e => e.PartOfSpeech).HasColumnName("part_of_speech");
        builder.Property(e => e.ExampleEn).HasColumnName("example_en");
        builder.Property(e => e.ExampleCn).HasColumnName("example_cn");
        builder.Property(e => e.ImageUrl).HasColumnName("image_url");
        builder.Property(e => e.SortOrder).HasColumnName("sort_order");

        // Ignore inverse navigation property that would cause automatic shadow property creation
        builder.Ignore(w => w.LearningProgresses);
    }
}
