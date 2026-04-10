using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class QuestionConfiguration : IEntityTypeConfiguration<Question>
{
    public void Configure(EntityTypeBuilder<Question> builder)
    {
        builder.ToTable("tb_question");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.GradeUnitId);
        builder.HasIndex(e => new { e.GradeUnitId, e.IsActive, e.Difficulty });
        builder.Property(e => e.GradeUnitId).HasColumnName("grade_unit_id");
        builder.Property(e => e.QuestionStem).HasColumnName("question_stem");
        builder.Property(e => e.QuestionType).HasColumnName("question_type");
        builder.Property(e => e.KnowledgePoint).HasColumnName("knowledge_point");
        builder.Property(e => e.Difficulty).HasColumnName("difficulty");
        builder.Property(e => e.CorrectAnswer).HasColumnName("correct_answer");
        builder.Property(e => e.AnswerAnalysis).HasColumnName("answer_analysis");
        builder.Property(e => e.StemAudioUrl).HasColumnName("stem_audio_url");
        builder.Property(e => e.Tags).HasColumnName("tags");
        builder.Property(e => e.IsActive).HasColumnName("is_active");
        builder.Property(e => e.CreatedAt).HasColumnName("created_at");
        builder.Property(e => e.UpdatedAt).HasColumnName("updated_at");
    }
}
