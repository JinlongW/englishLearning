<template>
  <div class="wrong-question-review-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <h1>错题复习</h1>
      <div class="progress-text">{{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</div>
    </header>

    <main class="main-content">
      <!-- 复习进行中 -->
      <div v-if="!reviewFinished" class="review-content">
        <!-- 进度条 -->
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
        </div>

        <!-- 连击显示 -->
        <ComboDisplay :combo="comboCount" :show="comboCount > 0" />

        <!-- 题目卡片 -->
        <div class="question-card">
          <div class="question-type">
            {{ questionTypeText }}
          </div>
          <h2 class="question-stem">{{ currentQuestion?.questionStem }}</h2>

          <!-- 题目音频按钮（如果有） -->
          <button v-if="currentQuestion?.stemAudioUrl" class="audio-btn" @click="playQuestionAudio">
            🔊 播放题目
          </button>

          <!-- 选项列表 -->
          <div class="options-list">
            <div
              v-for="option in currentQuestion?.options"
              :key="option.id"
              class="option-item"
              :class="{
                selected: userAnswers[currentQuestionIndex] === option.optionKey,
                correct: showResult && option.optionKey === currentQuestion?.correctAnswer,
                incorrect: showResult && userAnswers[currentQuestionIndex] === option.optionKey && option.optionKey !== currentQuestion?.correctAnswer
              }"
              @click="selectOption(option.optionKey)"
            >
              <span class="option-key">{{ option.optionKey }}</span>
              <span class="option-content">{{ option.optionContent }}</span>
            </div>
          </div>
        </div>

        <!-- 提交/下一题按钮 -->
        <div class="action-buttons">
          <button
            v-if="!showResult"
            class="action-btn primary"
            @click="submitAnswer"
            :disabled="!userAnswers[currentQuestionIndex]"
          >
            提交答案
          </button>
          <button
            v-else
            class="action-btn primary"
            @click="nextQuestion"
          >
            {{ currentQuestionIndex < totalQuestions - 1 ? '下一题' : '完成复习' }}
          </button>
        </div>

        <!-- 答案解析 -->
        <div v-if="showResult" class="analysis-card">
          <div class="analysis-header" :class="isCurrentCorrect ? 'correct' : 'incorrect'">
            <span class="analysis-icon">{{ isCurrentCorrect ? '✓' : '✗' }}</span>
            <span class="analysis-text">{{ isCurrentCorrect ? '回答正确！' : '回答错误' }}</span>
          </div>
          <div class="analysis-content">
            <div class="analysis-row">
              <span class="analysis-label">正确答案：</span>
              <span class="analysis-value">{{ currentQuestion?.correctAnswer }}</span>
            </div>
            <div class="analysis-row">
              <span class="analysis-label">你的答案：</span>
              <span class="analysis-value">{{ userAnswers[currentQuestionIndex] }}</span>
            </div>
            <div class="analysis-explanation">
              <strong>解析：</strong>
              <p>{{ currentQuestionAnalysis || '暂无解析' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 复习结果 -->
      <div v-else class="result-content">
        <div class="result-card">
          <div class="result-icon">
            {{ correctCount >= totalQuestions / 2 ? '🎉' : '💪' }}
          </div>
          <h2>{{ correctCount >= totalQuestions / 2 ? '复习完成！' : '继续加油！' }}</h2>

          <div class="score-section">
            <div class="score-circle" :class="correctCount >= totalQuestions / 2 ? 'pass' : 'fail'">
              <span class="score-value">{{ totalScore }}</span>
              <span class="score-label">总分</span>
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value" :class="correctCount >= totalQuestions / 2 ? 'good' : 'bad'">{{ correctCount }}</span>
              <span class="stat-label">答对</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ totalQuestions }}</span>
              <span class="stat-label">总题数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">+{{ pointsEarned }}</span>
              <span class="stat-label">获得积分</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ maxCombo >= 10 ? '👑' : maxCombo >= 7 ? '🔥🔥🔥' : maxCombo >= 4 ? '🔥🔥' : maxCombo >= 2 ? '🔥' : '-' }}</span>
              <span class="stat-label">最高连击</span>
            </div>
          </div>

          <div class="result-message">
            <p v-if="correctCount >= totalQuestions / 2">
              太棒了！这些错题你已经掌握了，继续保持！
            </p>
            <p v-else>
              别灰心！错题是最好的学习资源，多复习几次就能掌握！
            </p>
          </div>
        </div>

        <div class="action-buttons">
          <button class="action-btn secondary" @click="backToList">
            返回错题本
          </button>
          <button
            v-if="incorrectCount > 0"
            class="action-btn primary"
            @click="reviewIncorrect"
          >
            只练错题
          </button>
        </div>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getReviewQuestions, submitReview } from '@/api/wrong-question'
import type { QuestionDetailResponse, WrongQuestionDetailResponse } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'
import ComboDisplay from '@/components/ComboDisplay.vue'

interface ReviewQuestion {
  id: string
  wrongQuestionId: string
  questionType: string
  questionStem: string
  stemAudioUrl?: string
  options: {
    id: string
    optionKey: string
    optionContent: string
  }[]
  correctAnswer: string
  analysis: string
}

const router = useRouter()
const route = useRoute()

const questions = ref<ReviewQuestion[]>([])
const currentQuestionIndex = ref(0)
const userAnswers = ref<string[]>([])
const showResult = ref(false)
const reviewFinished = ref(false)
const isCurrentCorrect = ref(false)
const currentQuestionAnalysis = ref('')

// 连击计数
const comboCount = ref(0)
const maxCombo = ref(0)

// 得分计算
const baseScorePerQuestion = 10
const pointsEarned = ref(0)
const totalScore = ref(0)

// 从路由参数获取题目 ID 列表
const questionIds = computed(() => {
  const ids = route.query.ids as string
  return ids ? ids.split(',') : []
})

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const totalQuestions = computed(() => questions.value.length)

const progressPercent = computed(() => {
  if (totalQuestions.value === 0) return 0
  return ((currentQuestionIndex.value + 1) / totalQuestions.value) * 100
})

const questionTypeText = computed(() => {
  if (!currentQuestion.value) return ''
  const typeMap: Record<string, string> = {
    single_choice: '单选题',
    multiple_choice: '多选题',
    true_false: '判断题',
    fill_blank: '填空题'
  }
  return typeMap[currentQuestion.value.questionType] || '题目'
})

// 统计
const correctCount = ref(0)
const incorrectCount = ref(0)
const correctRate = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((correctCount.value / totalQuestions.value) * 100)
})

// 计算连击倍率
const getComboMultiplier = (combo: number): number => {
  if (combo >= 10) return 3.0
  if (combo >= 7) return 2.5
  if (combo >= 4) return 2.0
  if (combo >= 2) return 1.5
  return 1.0
}

// 选择答案
const selectOption = (optionKey: string) => {
  if (showResult.value) return
  userAnswers.value[currentQuestionIndex.value] = optionKey
}

// 提交答案
const submitAnswer = async () => {
  if (!currentQuestion.value || !userAnswers.value[currentQuestionIndex.value]) return

  try {
    const userAnswer = userAnswers.value[currentQuestionIndex.value]
    const isCorrect = userAnswer === currentQuestion.value.correctAnswer

    // 调用 API 提交复习
    await submitReview(currentQuestion.value.wrongQuestionId, userAnswer, isCorrect)

    // 更新状态
    isCurrentCorrect.value = isCorrect
    currentQuestionAnalysis.value = currentQuestion.value.analysis || ''
    showResult.value = true

    if (isCorrect) {
      // 连击 +1
      comboCount.value++
      correctCount.value++

      // 更新最大连击
      if (comboCount.value > maxCombo.value) {
        maxCombo.value = comboCount.value
      }

      // 计算得分：基础分 * 连击倍率
      const multiplier = getComboMultiplier(comboCount.value)
      const score = Math.round(baseScorePerQuestion * multiplier)
      pointsEarned.value += score
      totalScore.value += score

      uni.showToast({
        title: `回答正确！+${score}分（×${multiplier}）`,
        icon: 'success',
        duration: 1500
      })
    } else {
      // 答错重置连击
      comboCount.value = 0
      incorrectCount.value++

      uni.showToast({
        title: '连击中断',
        icon: 'none',
        duration: 1500
      })
    }
  } catch (error) {
    console.error('提交复习失败', error)
    uni.showToast({
      title: '提交失败，请稍后重试',
      icon: 'none',
      duration: 2000
    })
  }
}

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
    showResult.value = false
    isCurrentCorrect.value = false
    currentQuestionAnalysis.value = ''
  } else {
    // 完成复习
    reviewFinished.value = true
  }
}

// 播放题目音频
const playQuestionAudio = () => {
  if (!currentQuestion.value?.stemAudioUrl) return
  uni.showToast({
    title: '播放题目音频',
    icon: 'none'
  })
}

// 只练错题
const reviewIncorrect = () => {
  // TODO: 重新加载错题
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

// 返回错题本
const backToList = () => {
  router.push('/wrong-questions')
}

// 返回
const goBack = () => {
  if (reviewFinished.value) {
    backToList()
  } else if (confirm('确定要退出复习吗？当前进度将不会保存')) {
    router.back()
  }
}

// 加载复习题目
const loadReviewQuestions = async () => {
  try {
    uni.showLoading({ title: '加载中...', mask: true })

    let questionList: WrongQuestionDetailResponse[] = []

    if (questionIds.value.length > 0) {
      // 如果有指定的题目 ID 列表，获取这些题目
      // TODO: 实现批量获取题目的 API
      const promises = questionIds.value.map(id =>
        getReviewQuestions(1).then(res => {
          // 这里需要根据实际 API 调整
          return res.data || res
        })
      )
      // 暂时使用待复习题目
      const res = await getReviewQuestions(questionIds.value.length)
      questionList = res.data || res
    } else {
      // 否则获取默认的待复习题目
      const res = await getReviewQuestions(10)
      questionList = res.data || res
    }

    // 转换为 ReviewQuestion 格式
    questions.value = questionList.map((q: WrongQuestionDetailResponse) => ({
      id: q.id,
      wrongQuestionId: q.id,
      questionType: q.questionType || 'single_choice',
      questionStem: q.questionText,
      options: q.options || [],
      correctAnswer: q.correctAnswer,
      analysis: q.analysis || ''
    }))

    if (questions.value.length === 0) {
      uni.showToast({
        title: '暂无需要复习的题目',
        icon: 'none',
        duration: 2000
      })
      router.back()
    }
  } catch (error) {
    console.error('加载复习题目失败', error)
    uni.showToast({
      title: '加载失败，请稍后重试',
      icon: 'none',
      duration: 2000
    })
  } finally {
    uni.hideLoading()
  }
}

onMounted(() => {
  loadReviewQuestions()
})
</script>

<style scoped>
.wrong-question-review-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  padding: 15px 20px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.back-btn span {
  font-size: 20px;
}

.header h1 {
  margin: 0;
  font-size: 18px;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
}

.main-content {
  padding: 20px;
}

.progress-bar-container {
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  margin-bottom: 20px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  transition: width 0.3s;
}

.review-content,
.result-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.question-type {
  display: inline-block;
  background: #4facfe;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  margin-bottom: 15px;
}

.question-stem {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.5;
}

.audio-btn {
  background: #f0f0f0;
  border: none;
  padding: 10px 15px;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background 0.2s;
}

.audio-btn:active {
  background: #e0e0e0;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.option-item:hover {
  background: #e8ecf1;
}

.option-item.selected {
  border-color: #4facfe;
  background: #e8f4ff;
}

.option-item.correct {
  border-color: #22c55e;
  background: #dcfce7;
}

.option-item.incorrect {
  border-color: #ef4444;
  background: #fee2e2;
}

.option-key {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  font-weight: 600;
  color: #4facfe;
  flex-shrink: 0;
}

.option-item.selected .option-key {
  background: #4facfe;
  color: white;
}

.option-item.correct .option-key {
  background: #22c55e;
  color: white;
}

.option-item.incorrect .option-key {
  background: #ef4444;
  color: white;
}

.option-content {
  flex: 1;
  color: #333;
  font-size: 15px;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.action-btn {
  flex: 1;
  padding: 16px;
  border: none;
  border-radius: 15px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.primary {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.action-btn.secondary {
  background: #f0f0f0;
  color: #333;
}

.analysis-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  color: white;
}

.analysis-header.correct {
  background: #22c55e;
}

.analysis-header.incorrect {
  background: #ef4444;
}

.analysis-icon {
  font-size: 20px;
  font-weight: bold;
}

.analysis-text {
  font-size: 16px;
  font-weight: 600;
}

.analysis-content {
  padding: 20px;
}

.analysis-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 15px;
}

.analysis-label {
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
}

.analysis-value {
  color: #333;
}

.analysis-explanation {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.analysis-explanation strong {
  color: #666;
  display: block;
  margin-bottom: 8px;
}

.analysis-explanation p {
  margin: 0;
  color: #555;
  line-height: 1.6;
  font-size: 14px;
}

.result-card {
  background: white;
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.result-icon {
  font-size: 80px;
  margin-bottom: 15px;
}

.result-card h2 {
  margin: 0 0 25px 0;
  color: #333;
}

.score-section {
  margin-bottom: 25px;
}

.score-circle {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 8px solid;
}

.score-circle.pass {
  border-color: #22c55e;
  background: #dcfce7;
}

.score-circle.fail {
  border-color: #ef4444;
  background: #fee2e2;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  line-height: 1;
}

.score-circle.pass .score-value {
  color: #22c55e;
}

.score-circle.fail .score-value {
  color: #ef4444;
}

.score-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
}

.stat-value.good {
  color: #22c55e;
}

.stat-value.bad {
  color: #ef4444;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.result-message {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 10px;
  margin-bottom: 20px;
}

.result-message p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}
</style>
