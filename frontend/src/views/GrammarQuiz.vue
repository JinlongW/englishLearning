<template>
  <div class="grammar-quiz-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <h1>语法测验</h1>
      <div class="progress-text">{{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</div>
    </header>

    <main class="main-content">
      <!-- 测验进行中 -->
      <div v-if="!quizFinished" class="quiz-content">
        <!-- 进度条 -->
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
        </div>

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
            v-if="currentQuestionIndex < totalQuestions - 1"
            class="action-btn primary"
            @click="nextQuestion"
            :disabled="!userAnswers[currentQuestionIndex]"
          >
            下一题
          </button>
          <button
            v-else
            class="action-btn primary"
            @click="submitQuiz"
            :disabled="!userAnswers[currentQuestionIndex]"
          >
            提交试卷
          </button>
        </div>
      </div>

      <!-- 测验结果 -->
      <div v-else class="result-content">
        <div class="result-card">
          <div class="result-icon" :class="result?.isPassed ? 'pass' : 'fail'">
            {{ result?.isPassed ? '🎉' : '💪' }}
          </div>
          <h2>{{ result?.isPassed ? '测验通过！' : '继续加油！' }}</h2>

          <div class="score-section">
            <div class="score-circle" :class="result?.isPassed ? 'pass' : 'fail'">
              <span class="score-value">{{ result?.score }}</span>
              <span class="score-label">分</span>
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">{{ result?.correctCount }}</span>
              <span class="stat-label">答对</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ result?.totalCount }}</span>
              <span class="stat-label">总题数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">+{{ result?.pointsEarned }}</span>
              <span class="stat-label">获得积分</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ result?.isPassed ? '通过' : '未通过' }}</span>
              <span class="stat-label">状态</span>
            </div>
          </div>

          <div class="result-message">
            <p v-if="result?.isPassed">
              太棒了！你已掌握这个语法点，继续学习下一个课程吧！
            </p>
            <p v-else>
              别灰心！回顾课程内容后再来挑战一次吧！
            </p>
          </div>
        </div>

        <div class="action-buttons">
          <button class="action-btn secondary" @click="reviewContent">
            回顾课程
          </button>
          <button class="action-btn primary" @click="finishQuiz">
            {{ result?.isPassed ? '返回课程列表' : '重新测验' }}
          </button>
        </div>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGrammarById, submitGrammarQuiz } from '@/api/grammar'
import type { GrammarDetailDto, GrammarQuizResult } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'

interface Question {
  id: string
  questionType: string
  questionStem: string
  stemAudioUrl?: string
  options: Array<{
    id: string
    optionKey: string
    optionContent: string
  }>
  correctAnswer?: string
}

const route = useRoute()
const router = useRouter()
const grammarId = computed(() => route.params.id as string)

const grammar = ref<GrammarDetailDto | null>(null)
const questions = ref<Question[]>([])
const currentQuestionIndex = ref(0)
const userAnswers = ref<string[]>([])
const quizFinished = ref(false)
const showResult = ref(false)
const result = ref<GrammarQuizResult | null>(null)

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

// 解析测验题目
const parseQuizQuestions = () => {
  if (!grammar.value?.quizJson) return []

  try {
    const quiz = JSON.parse(grammar.value.quizJson)
    if (Array.isArray(quiz)) {
      return quiz
    }
    if (quiz.questions && Array.isArray(quiz.questions)) {
      return quiz.questions
    }
  } catch (e) {
    console.error('解析 quizJson 失败', e)
  }
  return []
}

const selectOption = (optionKey: string) => {
  if (showResult.value) return
  userAnswers.value[currentQuestionIndex.value] = optionKey
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const submitQuiz = async () => {
  if (!confirm('确定要提交试卷吗？')) return

  try {
    uni.showLoading({ title: '提交中...', mask: true })

    // 构建答案提交数据
    const answers = questions.value.map((q, index) => ({
      questionId: q.id,
      userAnswer: userAnswers.value[index]
    }))

    const response = await submitGrammarQuiz(grammarId.value, answers)
    result.value = response.data || response
    quizFinished.value = true
    showResult.value = true
  } catch (error) {
    console.error('提交测验失败', error)
    uni.showToast({
      title: '提交失败，请稍后重试',
      icon: 'none',
      duration: 2000
    })
  } finally {
    uni.hideLoading()
  }
}

const playQuestionAudio = () => {
  if (!currentQuestion.value?.stemAudioUrl) return
  uni.showToast({
    title: '播放题目音频',
    icon: 'none'
  })
}

const reviewContent = () => {
  router.push(`/grammar/${grammarId.value}`)
}

const finishQuiz = () => {
  if (result.value?.isPassed) {
    // 通过后返回课程列表
    router.push('/grammar')
  } else {
    // 未通过重新测验
    quizFinished.value = false
    showResult.value = false
    currentQuestionIndex.value = 0
    userAnswers.value = []
  }
}

const goBack = () => {
  if (quizFinished.value) {
    finishQuiz()
  } else if (confirm('确定要退出测验吗？当前进度将不会保存')) {
    router.back()
  }
}

const loadQuiz = async () => {
  try {
    uni.showLoading({ title: '加载中...', mask: true })
    const response = await getGrammarById(grammarId.value)
    grammar.value = response.data || response
    questions.value = parseQuizQuestions()

    if (questions.value.length === 0) {
      uni.showToast({
        title: '暂无测验题目',
        icon: 'none',
        duration: 2000
      })
      router.back()
    }
  } catch (error) {
    console.error('加载测验失败', error)
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
  loadQuiz()
})
</script>

<style scoped>
.grammar-quiz-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.quiz-content,
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
  background: #667eea;
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
  border-color: #667eea;
  background: #e8ecff;
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
  color: #667eea;
  flex-shrink: 0;
}

.option-item.selected .option-key {
  background: #667eea;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background: #f0f0f0;
  color: #333;
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
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 6px solid;
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
  font-size: 42px;
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
  font-size: 18px;
  font-weight: 600;
  color: #667eea;
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
