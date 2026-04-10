using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace EnglishLearning.Infrastructure.Configurations;

public sealed class WrongQuestionConfiguration : IEntityTypeConfiguration<WrongQuestion>
{
    public void Configure(EntityTypeBuilder<WrongQuestion> builder)
    {
        builder.ToTable("tb_wrong_question");

        builder.Property(e => e.Id).HasColumnName("id");
        builder.HasIndex(e => e.UserId);
        builder.HasIndex(e => new { e.UserId, e.ReviewStatus });
        builder.Property(e => e.UserId).HasColumnName("user_id");
        builder.Property(e => e.QuestionId).HasColumnName("question_id");
        builder.Property(e => e.UserAnswer).HasColumnName("user_answer");
        builder.Property(e => e.CorrectAnswer).HasColumnName("correct_answer");
        builder.Property(e => e.ErrorType).HasColumnName("error_type");
        builder.Property(e => e.ReviewStatus).HasColumnName("review_status");
        builder.Property(e => e.ReviewCount).HasColumnName("review_count");
        builder.Property(e => e.NextReviewAt).HasColumnName("next_review_at");
        builder.Property(e => e.FirstWrongAt).HasColumnName("first_wrong_at");
        builder.Property(e => e.LastReviewAt).HasColumnName("last_review_at");
        builder.Property(e => e.MasteredAt).HasColumnName("mastered_at");
        builder.Property(e => e.IsDeleted).HasColumnName("is_deleted");

        // Global query filter handled in AppDbContext
    }
}
