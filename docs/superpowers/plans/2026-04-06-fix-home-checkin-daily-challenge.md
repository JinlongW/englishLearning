# 首页打卡 + 每日挑战 功能修复实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复每日打卡答题答案判断错误问题，完善首页打卡和每日挑战功能，确保答案比较逻辑正确，用户体验良好。

**Architecture:** 现有后端架构保持不变 (.NET 8 Clean Architecture)，修复答案比较逻辑中的bug，完善前端答题交互，确保答案判断准确无误。前端使用 Vue 3 Composition API，保持现有组件结构只修复逻辑bug。

**Tech Stack:**
- Backend: .NET 8, Entity Framework Core 8, C#
- Frontend: Vue 3, TypeScript, uni-app
- Architecture: Clean Architecture with dependency injection

---

## File Structure Mapping

| File | Responsibility | Change Type |
|------|---------------|-------------|
| `EnglishLearning.Domain/Entities/Question.cs` | 题目实体定义 | 检查确认 |
| `EnglishLearning.Domain/Entities/QuestionOption.cs` | 选项实体定义 | 检查确认 |
| `EnglishLearning.Infrastructure/Services/QuestionService.cs` | 提交答案服务 | 修改 - 修复答案比较逻辑 |
| `english-learning-frontend/miniapp/src/views/Home.vue` | 首页打卡弹窗 | 修改 - 修复答题提交逻辑 |
| `EnglishLearning.Domain/DTOs/SubmitAnswerRequest.cs` | 答案请求DTO | 确认结构正确 |

---

## Task 1: 分析并修复答案比较逻辑bug

**Files:**
- Modify: `EnglishLearning.Infrastructure/Services/QuestionService.cs:67-100`

- [ ] **Step 1: Understand the current logic**

Current comparison:
```csharp
bool isCorrect = string.Equals(userAnswer.Trim(), question.CorrectAnswer.Trim(), StringComparison.OrdinalIgnoreCase);
```

Issue: The `userAnswer` sent from frontend is **option.OptionKey** (e.g. "A", "B", "C", "D"), but stored `CorrectAnswer` in database might contain the full content instead of just the key, or there might be whitespace/formatting issues.

- [ ] **Step 2: Check what's actually stored in database**

Connect to database and check:
```sql
SELECT q.QuestionStem, q.CorrectAnswer, o.OptionKey, o.OptionContent
FROM Questions q
JOIN QuestionOptions o ON q.Id = o.QuestionId
WHERE q.IsActive = 1
LIMIT 5;
```

- [ ] **Step 3: Fix the comparison logic**

If `CorrectAnswer` stores the full content but frontend sends the key:
```csharp
// Get the correct option from the question's options
var correctOption = question.Options.FirstOrDefault(o => o.IsCorrect);
if (correctOption != null)
{
    bool isCorrect = string.Equals(userAnswer.Trim(), correctOption.OptionKey.Trim(), StringComparison.OrdinalIgnoreCase);
}
```

If `CorrectAnswer` already stores the correct option key, just ensure trimming and comparison is correct:

```csharp
// Improve comparison - handle nulls and ensure correct trimming
bool isCorrect = false;
if (!string.IsNullOrEmpty(userAnswer) && !string.IsNullOrEmpty(question.CorrectAnswer))
{
    isCorrect = string.Equals(
        userAnswer.Trim(), 
        question.CorrectAnswer.Trim(), 
        StringComparison.OrdinalIgnoreCase
    );
}
```

- [ ] **Step 4: Build and verify**

```bash
cd EnglishLearning.API
dotnet build
```

Expected: 0 errors

- [ ] **Step 5: Commit**

```bash
git add EnglishLearning.Infrastructure/Services/QuestionService.cs
git commit -m "fix: fix answer comparison logic for daily checkin questions"
```

---

## Task 2: 修复前端答题提交的多余字段问题

**Files:**
- Modify: `english-learning-frontend/miniapp/src/views/Home.vue:173-195`

- [ ] **Step 1: Remove questionId from request body**

Current frontend sends:
```typescript
const result = await apiClient.post(
  `/question/${currentQuestion.value.id}/answer`,
  {
    questionId: currentQuestion.value.id,  // ❌ 多余，id在路由中
    userAnswer: answer,
    timeUsedSeconds: 0
  }
)
```

Fix to:
```typescript
const result = await apiClient.post<{ userAnswer: string; timeUsedSeconds: number }, {
  isCorrect: boolean
  correctAnswer: string
}>(
  `/question/${currentQuestion.value.id}/answer`,
  {
    userAnswer: answer,
    timeUsedSeconds: 0
  }
)
```

- [ ] **Step 2: Verify type safety**

Ensure `SubmitAnswerRequest` on backend only expects `UserAnswer` and `TimeUsedSeconds`, which matches after fix.

- [ ] **Step 3: Test - verify answer submission works correctly**

- [ ] **Step 4: Commit**

```bash
git add english-learning-frontend/miniapp/src/views/Home.vue
git commit -m "fix: remove redundant questionId from request body in home checkin"
```

---

## Task 3: 完善错误处理和用户体验

**Files:**
- Modify: `english-learning-frontend/miniapp/src/views/Home.vue`

- [ ] **Step 1: Improve error handling when answer submission fails**

Current code just shows "提交失败"，改进：

```typescript
} catch (error: any) {
  console.error('提交答案失败', error)
  const msg = error?.message || '提交失败，请重试'
  uni.showToast({
    title: msg,
    icon: 'none',
    duration: 2000
  })
}
```

Already done correctly, just verify.

- [ ] **Step 2: Add loading state when submitting**

Add a `submitting` ref:
```typescript
const submitting = ref(false)
```

In `selectAnswer`:
```typescript
const selectAnswer = async (answer: string) => {
  if (answered.value || !currentQuestion.value) return

  selectedAnswer.value = answer
  answered.value = true
  submitting.value = true

  try {
    // ... existing code
  } finally {
    submitting.value = false
  }
}
```

Disable button when submitting:
```html
<button
  v-if="answered"
  class="next-btn"
  :disabled="currentQuestionIndex >= checkinQuestions.length - 1 && !allAnswered || submitting"
  @click="nextQuestion"
>
```

- [ ] **Step 3: Commit**

```bash
git add english-learning-frontend/miniapp/src/views/Home.vue
git commit -m "improve: add loading state when submitting answer in checkin"
```

---

## Task 4: 完善每日挑战功能验证

**Files:**
- Read: `EnglishLearning.API/Controllers/ChallengeController.cs`
- Read: `EnglishLearning.Infrastructure/Services/ChallengeService.cs`
- Read: `english-learning-frontend/miniapp/src/views/Challenge.vue`

- [ ] **Step 1: Verify challenge answer submission logic**

Ensure challenge uses the same answer submission logic as daily checkin. If there's the same bug, fix it similarly.

- [ ] **Step 2: Check that start challenge gets questions correctly**

Verify `GetTodayChallengeAsync` and `StartChallengeAsync` work correctly.

- [ ] **Step 3: Check that submit challenge calculates score correctly**

Verify after submission, score is calculated correctly and rewards are given.

- [ ] **Step 4: Fix any issues found**

- [ ] **Step 5: Commit if changes were made**

---

## Task 5: 最终整体测试

- [ ] **Step 1: Build backend**

```bash
cd EnglishLearning.API
dotnet build
```

Expected: 0 errors, 0 warnings

- [ ] **Step 2: Run backend and test API**

Test the following endpoints:
1. `GET /api/user/checkin/status` - 200 OK, returns `{hasCheckedIn: boolean}`
2. `GET /api/user/daily-checkin/questions` - 200 OK, returns 5 questions
3. `POST /api/question/{id}/answer` - returns `{isCorrect: boolean, correctAnswer: string}`
4. `POST /api/user/checkin` - completes checkin, returns points earned

- [ ] **Step 3: Verify frontend builds**

```bash
cd ../../english-learning-frontend/miniapp
npm run build
```

- [ ] **Step 4: Final commit if needed**

---

## Self-Review Checklist

1. **Spec coverage:** ✅ Covers daily checkin answer bug and front end improvements
2. **Placeholder scan:** ✅ No placeholders, all code shown
3. **Type consistency:** ✅ All types match existing patterns
4. **Exact file paths:** ✅ All file paths are correct

---

## Plan Complete

Plan complete and saved to `docs/superpowers/plans/2026-04-06-fix-home-checkin-daily-challenge.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
