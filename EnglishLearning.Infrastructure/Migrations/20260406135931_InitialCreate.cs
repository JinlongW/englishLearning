using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EnglishLearning.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "tb_badge",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    badge_code = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    badge_name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    badge_icon = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    badge_type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    requirement_json = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    sort_order = table.Column<int>(type: "int", nullable: false),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_badge", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "tb_grade_unit",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    grade = table.Column<int>(type: "int", nullable: false),
                    semester = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    unit_no = table.Column<int>(type: "int", nullable: false),
                    unit_name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    sort_order = table.Column<int>(type: "int", nullable: false),
                    is_locked = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_grade_unit", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "tb_user",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    username = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    password_hash = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    phone = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    student_name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    grade_level = table.Column<int>(type: "int", nullable: false),
                    avatar_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_user", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "tb_grammar",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    grade_unit_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    title = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    content_type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    video_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    content_json = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    duration_seconds = table.Column<int>(type: "int", nullable: true),
                    sort_order = table.Column<int>(type: "int", nullable: false),
                    quiz_json = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    passing_score = table.Column<int>(type: "int", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_grammar", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_grammar_tb_grade_unit_grade_unit_id",
                        column: x => x.grade_unit_id,
                        principalTable: "tb_grade_unit",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_question",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    grade_unit_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    question_type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    difficulty = table.Column<int>(type: "int", nullable: false),
                    question_stem = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    stem_audio_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    correct_answer = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    answer_analysis = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    knowledge_point = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    tags = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_question", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_question_tb_grade_unit_grade_unit_id",
                        column: x => x.grade_unit_id,
                        principalTable: "tb_grade_unit",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_word",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    grade_unit_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    word_text = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    phonetic_uk = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    phonetic_us = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    audio_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    meaning_cn = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    part_of_speech = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    example_en = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    example_cn = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    image_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    sort_order = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_word", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_word_tb_grade_unit_grade_unit_id",
                        column: x => x.grade_unit_id,
                        principalTable: "tb_grade_unit",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_checkin",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    checkin_date = table.Column<DateTime>(type: "datetime2", nullable: false),
                    points_earned = table.Column<int>(type: "int", nullable: false),
                    streak_days = table.Column<int>(type: "int", nullable: false),
                    bonus_points = table.Column<int>(type: "int", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_checkin", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_checkin_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_daily_challenge",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    challenge_date = table.Column<DateTime>(type: "datetime2", nullable: false),
                    status = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    total_questions = table.Column<int>(type: "int", nullable: false),
                    correct_count = table.Column<int>(type: "int", nullable: false),
                    score = table.Column<int>(type: "int", nullable: false),
                    time_used_seconds = table.Column<int>(type: "int", nullable: false),
                    points_earned = table.Column<int>(type: "int", nullable: false),
                    coins_earned = table.Column<int>(type: "int", nullable: false),
                    started_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    completed_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_daily_challenge", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_daily_challenge_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_learning_progress",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    grade_unit_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    content_type = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    content_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    status = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    score = table.Column<int>(type: "int", nullable: true),
                    attempts_count = table.Column<int>(type: "int", nullable: false),
                    last_attempt_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    completed_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_learning_progress", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_learning_progress_tb_grade_unit_grade_unit_id",
                        column: x => x.grade_unit_id,
                        principalTable: "tb_grade_unit",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_tb_learning_progress_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_user_badge",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    badge_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    earned_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    is_new = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_user_badge", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_user_badge_tb_badge_badge_id",
                        column: x => x.badge_id,
                        principalTable: "tb_badge",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_tb_user_badge_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_user_level",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    current_level = table.Column<int>(type: "int", nullable: false),
                    level_name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    current_exp = table.Column<int>(type: "int", nullable: false),
                    exp_to_next = table.Column<int>(type: "int", nullable: false),
                    level_up_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_user_level", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_user_level_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_user_points",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    points_type = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    change_type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    change_amount = table.Column<int>(type: "int", nullable: false),
                    balance_after = table.Column<int>(type: "int", nullable: false),
                    description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    reference_id = table.Column<Guid>(type: "uniqueidentifier", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_user_points", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_user_points_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_user_profile",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    learning_style = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    difficulty_level = table.Column<int>(type: "int", nullable: false),
                    preferred_study_time = table.Column<TimeSpan>(type: "time", nullable: true),
                    parent_notify_enabled = table.Column<bool>(type: "bit", nullable: false),
                    total_learning_days = table.Column<int>(type: "int", nullable: false),
                    current_streak = table.Column<int>(type: "int", nullable: false),
                    max_streak = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_user_profile", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_user_profile_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_question_option",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    question_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    option_key = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    option_content = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    image_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    audio_url = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    sort_order = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_question_option", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_question_option_tb_question_question_id",
                        column: x => x.question_id,
                        principalTable: "tb_question",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_wrong_question",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    question_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    user_answer = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    correct_answer = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    error_type = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    review_status = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    review_count = table.Column<int>(type: "int", nullable: false),
                    next_review_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    first_wrong_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    last_review_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    mastered_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    is_deleted = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_wrong_question", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_wrong_question_tb_question_question_id",
                        column: x => x.question_id,
                        principalTable: "tb_question",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_tb_wrong_question_tb_user_user_id",
                        column: x => x.user_id,
                        principalTable: "tb_user",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tb_daily_challenge_detail",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    daily_challenge_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    question_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    question_order = table.Column<int>(type: "int", nullable: false),
                    user_answer = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    is_correct = table.Column<bool>(type: "bit", nullable: false),
                    time_used_seconds = table.Column<int>(type: "int", nullable: false),
                    is_uncertain = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tb_daily_challenge_detail", x => x.id);
                    table.ForeignKey(
                        name: "FK_tb_daily_challenge_detail_tb_daily_challenge_daily_challenge_id",
                        column: x => x.daily_challenge_id,
                        principalTable: "tb_daily_challenge",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_tb_daily_challenge_detail_tb_question_question_id",
                        column: x => x.question_id,
                        principalTable: "tb_question",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_tb_badge_badge_code",
                table: "tb_badge",
                column: "badge_code",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_checkin_user_id",
                table: "tb_checkin",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_checkin_user_id_checkin_date",
                table: "tb_checkin",
                columns: new[] { "user_id", "checkin_date" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_daily_challenge_user_id",
                table: "tb_daily_challenge",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_daily_challenge_user_id_challenge_date",
                table: "tb_daily_challenge",
                columns: new[] { "user_id", "challenge_date" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_daily_challenge_detail_daily_challenge_id",
                table: "tb_daily_challenge_detail",
                column: "daily_challenge_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_daily_challenge_detail_question_id",
                table: "tb_daily_challenge_detail",
                column: "question_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_grade_unit_grade_semester_unit_no",
                table: "tb_grade_unit",
                columns: new[] { "grade", "semester", "unit_no" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_grammar_grade_unit_id",
                table: "tb_grammar",
                column: "grade_unit_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_learning_progress_grade_unit_id",
                table: "tb_learning_progress",
                column: "grade_unit_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_learning_progress_user_id",
                table: "tb_learning_progress",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_learning_progress_user_id_content_type_content_id",
                table: "tb_learning_progress",
                columns: new[] { "user_id", "content_type", "content_id" });

            migrationBuilder.CreateIndex(
                name: "IX_tb_question_grade_unit_id",
                table: "tb_question",
                column: "grade_unit_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_question_grade_unit_id_is_active_difficulty",
                table: "tb_question",
                columns: new[] { "grade_unit_id", "is_active", "difficulty" });

            migrationBuilder.CreateIndex(
                name: "IX_tb_question_option_question_id",
                table: "tb_question_option",
                column: "question_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_username",
                table: "tb_user",
                column: "username",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_badge_badge_id",
                table: "tb_user_badge",
                column: "badge_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_badge_user_id",
                table: "tb_user_badge",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_level_user_id",
                table: "tb_user_level",
                column: "user_id",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_points_user_id",
                table: "tb_user_points",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_points_user_id_points_type",
                table: "tb_user_points",
                columns: new[] { "user_id", "points_type" });

            migrationBuilder.CreateIndex(
                name: "IX_tb_user_profile_user_id",
                table: "tb_user_profile",
                column: "user_id",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_word_grade_unit_id",
                table: "tb_word",
                column: "grade_unit_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_word_grade_unit_id_sort_order",
                table: "tb_word",
                columns: new[] { "grade_unit_id", "sort_order" });

            migrationBuilder.CreateIndex(
                name: "IX_tb_wrong_question_question_id",
                table: "tb_wrong_question",
                column: "question_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_wrong_question_user_id",
                table: "tb_wrong_question",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_tb_wrong_question_user_id_review_status",
                table: "tb_wrong_question",
                columns: new[] { "user_id", "review_status" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "tb_checkin");

            migrationBuilder.DropTable(
                name: "tb_daily_challenge_detail");

            migrationBuilder.DropTable(
                name: "tb_grammar");

            migrationBuilder.DropTable(
                name: "tb_learning_progress");

            migrationBuilder.DropTable(
                name: "tb_question_option");

            migrationBuilder.DropTable(
                name: "tb_user_badge");

            migrationBuilder.DropTable(
                name: "tb_user_level");

            migrationBuilder.DropTable(
                name: "tb_user_points");

            migrationBuilder.DropTable(
                name: "tb_user_profile");

            migrationBuilder.DropTable(
                name: "tb_word");

            migrationBuilder.DropTable(
                name: "tb_wrong_question");

            migrationBuilder.DropTable(
                name: "tb_daily_challenge");

            migrationBuilder.DropTable(
                name: "tb_badge");

            migrationBuilder.DropTable(
                name: "tb_question");

            migrationBuilder.DropTable(
                name: "tb_user");

            migrationBuilder.DropTable(
                name: "tb_grade_unit");
        }
    }
}
