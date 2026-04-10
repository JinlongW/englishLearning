using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EnglishLearning.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddGrammarKnowledgeGraph : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Category",
                table: "tb_grammar",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "DependencyLevel",
                table: "tb_grammar",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<Guid>(
                name: "PrerequisiteId",
                table: "tb_grammar",
                type: "uniqueidentifier",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_tb_grammar_PrerequisiteId",
                table: "tb_grammar",
                column: "PrerequisiteId");

            migrationBuilder.AddForeignKey(
                name: "FK_tb_grammar_tb_grammar_PrerequisiteId",
                table: "tb_grammar",
                column: "PrerequisiteId",
                principalTable: "tb_grammar",
                principalColumn: "id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_tb_grammar_tb_grammar_PrerequisiteId",
                table: "tb_grammar");

            migrationBuilder.DropIndex(
                name: "IX_tb_grammar_PrerequisiteId",
                table: "tb_grammar");

            migrationBuilder.DropColumn(
                name: "Category",
                table: "tb_grammar");

            migrationBuilder.DropColumn(
                name: "DependencyLevel",
                table: "tb_grammar");

            migrationBuilder.DropColumn(
                name: "PrerequisiteId",
                table: "tb_grammar");
        }
    }
}
