using EnglishLearning.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace EnglishLearning.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    // 用户相关
    public DbSet<User> Users { get; set; }
    public DbSet<UserProfile> UserProfiles { get; set; }
    public DbSet<UserLevel> UserLevels { get; set; }
    public DbSet<UserBadge> UserBadges { get; set; }
    public DbSet<UserPoints> UserPoints { get; set; }
    public DbSet<Checkin> Checkins { get; set; }

    // 内容相关
    public DbSet<GradeUnit> GradeUnits { get; set; }
    public DbSet<Word> Words { get; set; }
    public DbSet<Grammar> Grammars { get; set; }
    public DbSet<Question> Questions { get; set; }
    public DbSet<QuestionOption> QuestionOptions { get; set; }
    public DbSet<Badge> Badges { get; set; }

    // 学习记录
    public DbSet<LearningProgress> LearningProgresses { get; set; }
    public DbSet<WrongQuestion> WrongQuestions { get; set; }
    public DbSet<DailyChallenge> DailyChallenges { get; set; }
    public DbSet<DailyChallengeDetail> DailyChallengeDetails { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // 自动应用所有 IEntityTypeConfiguration 配置类 from this assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

        // 全局查询过滤器
        modelBuilder.Entity<WrongQuestion>()
            .HasQueryFilter(wq => !wq.IsDeleted);
    }

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        var now = DateTime.UtcNow;

        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.CreatedAt = now;
                entry.Entity.UpdatedAt = now;
            }
            else if (entry.State == EntityState.Modified)
            {
                entry.Entity.UpdatedAt = now;
            }
        }

        return base.SaveChangesAsync(cancellationToken);
    }
}
