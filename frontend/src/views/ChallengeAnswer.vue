<template>
  <div class="challenge-question-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <div class="header-center">
        <h1>每日挑战</h1>
        <TimerDisplay
          ref="timerRef"
          :total-time="30"
          :is-running="!showResult && !challengeFinished"
          @timeout="handleTimeout"
          @tick="handleTick"
        />
      </div>
      <div class="question-count">{{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</div>
    </header>

    <main class="main-content">
      <!-- 答题进行中 -->
      <div v-if="!challengeFinished" class="question-content">
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

          <!-- 题目音频（如果有） -->
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
                correct: showResult && option.optionKey === correctAnswers[currentQuestionIndex],
                incorrect: showResult && userAnswers[currentQuestionIndex] === option.optionKey && option.optionKey !== correctAnswers[currentQuestionIndex]
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
            @click="submitChallenge"
            :disabled="!userAnswers[currentQuestionIndex]"
          >
            提交挑战
          </button>
        </div>
      </div>

      <!-- 挑战结果 -->
      <div v-else class="result-content">
        <div class="result-card">
          <div class="result-icon" :class="resultClass">
            {{ resultIcon }}
          </div>
          <h2>{{ resultTitle }}</h2>

          <div class="score-section">
            <div class="score-circle" :class="resultClass">
              <span class="score-value">{{ challengeResult?.score }}</span>
              <span class="score-label">分</span>
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">{{ challengeResult?.correctCount }}</span>
              <span class="stat-label">答对</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ challengeResult?.totalQuestions }}</span>
              <span class="stat-label">总题数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ totalTimeUsed }}s</span>
              <span class="stat-label">总用时</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">+{{ challengeResult?.pointsEarned }}</span>
              <span class="stat-label">获得积分</span>
            </div>
          </div>

          <!-- 速答奖励详情 -->
          <div v-if="totalSpeedBonus > 0" class="speed-bonus-section">
            <h3>速答奖励</h3>
            <div class="bonus-list">
              <div
                v-for="(item, index) in questionResults"
                :key="index"
                class="bonus-item"
                :class="{ 'no-bonus': item.speedBonus === 0 }"
              >
                <span class="bonus-question">第{{ index + 1 }}题</span>
                <span class="bonus-time">{{ item.timeUsedSeconds }}秒</span>
                <span class="bonus-points" :class="getBonusClass(item.speedBonus)">
                  +{{ item.speedBonus }}分
                </span>
              </div>
            </div>
            <div class="total-bonus">
              <span>速答奖励总计：</span>
              <span class="total-bonus-points">+{{ totalSpeedBonus }}分</span>
            </div>
          </div>

          <!-- 结果消息 -->
          <div class="result-message">
            <p>{{ resultMessage }}</p>
          </div>
        </div>

        <div class="action-buttons">
          <button class="action-btn secondary" @click="goHome">
            返回首页
          </button>
          <button class="action-btn primary" @click="goHome">
            完成
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
import { submitChallenge as apiSubmitChallenge } from '@/api/challenge'
import type { QuestionDetailResponse, ChallengeResult, ChallengeQuestionResult } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'
import TimerDisplay from '@/components/TimerDisplay.vue'

const route = useRoute()
const router = useRouter()

const timerRef = ref<InstanceType<typeof TimerDisplay> | null>(null)
const questions = ref<QuestionDetailResponse[]>([])
const currentQuestionIndex = ref(0)
const userAnswers = ref<string[]>([])
const correctAnswers = ref<string[]>([])
const challengeFinished = ref(false)
const showResult = ref(false)
const challengeResult = ref<ChallengeResult | null>(null)
const currentQuestionTime = ref(0)
const questionTimings = ref<number[]>([])

const totalQuestions = computed(() => questions.value.length)
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
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

const totalTimeUsed = computed(() => {
  return challengeResult.value?.timeUsedSeconds ?? questionTimings.value.reduce((a, b) => a + b, 0)
})

const totalSpeedBonus = computed(() => {
  return challengeResult.value?.questionResults.reduce((sum, item) => sum + item.speedBonus, 0) ?? 0
})

const resultClass = computed(() => {
  if (!challengeResult.value) return ''
  if (challengeResult.value.score >= 90) return 'excellent'
  if (challengeResult.value.score >= 60) return 'good'
  return 'normal'
})

const resultIcon = computed(() => {
  if (!challengeResult.value) return ''
  if (challengeResult.value.score === 100) return '🏆'
  if (challengeResult.value.score >= 90) return '🎉'
  if (challengeResult.value.score >= 60) return '👍'
  return '💪'
})

const resultTitle = computed(() => {
  if (!challengeResult.value) return ''
  if (challengeResult.value.score === 100) return '完美！满分通过！'
  if (challengeResult.value.score >= 90) return '太棒了！优秀！'
  if (challengeResult.value.score >= 60) return '不错！继续加油！'
  return '继续努力！'
})

const resultMessage = computed(() => {
  if (!challengeResult.value) return ''
  if (challengeResult.value.score === 100) {
    return '太厉害了！所有题目都回答正确！'
  }
  if (challengeResult.value.score >= 90) {
    return '表现非常出色！继续保持！'
  }
  if (challengeResult.value.score >= 60) {
    return '通过挑战！多多练习会更好！'
  }
  return '不要气馁，多练习一定能进步！'
})

const questionResults = computed(() => {
  return challengeResult.value?.questionResults ?? []
})

// 处理计时器超时
const handleTimeout = () => {
  uni.showToast({
    title: '时间到！',
    icon: 'none'
  })
}

// 处理计时器 ticking
const handleTick = (timeLeft: number) => {
  currentQuestionTime.value = 30 - timeLeft
}

// 获取速答奖励等级
const getBonusClass = (bonus: number) => {
  if (bonus >= 10) return 'bonus-high'
  if (bonus >= 5) return 'bonus-medium'
  if (bonus >= 2) return 'bonus-low'
  return 'no-bonus'
}

const selectOption = (optionKey: string) => {
  if (showResult.value) return
  userAnswers.value[currentQuestionIndex.value] = optionKey
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    // 记录当前题目用时
    questionTimings.value.push(currentQuestionTime.value)
    currentQuestionIndex.value++
    currentQuestionTime.value = 0
    timerRef.value?.reset()
    timerRef.value?.start()
  }
}

const playQuestionAudio = () => {
  if (!currentQuestion.value?.stemAudioUrl) return
  uni.showToast({
    title: '播放题目音频',
    icon: 'none'
  })
}

const submitChallenge = async () => {
  uni.showModal({
    title: '提交挑战',
    content: '确定要提交挑战结果吗？',
    success: async (modalRes) => {
      if (!modalRes.confirm) return

      try {
        uni.showLoading({ title: '提交中...', mask: true })

        // 记录最后一题用时
        questionTimings.value.push(currentQuestionTime.value)

        const challengeId = route.query.challengeId as string

        // 构建答案提交数据（包含每题用时）
        const answers = questions.value.map((q, index) => {
          const userAnswer = userAnswers.value[index]
          const timeUsed = questionTimings.value[index]
          return {
            questionId: q.id,
            userAnswer,
            isCorrect: true, // 后端会重新计算
            timeUsedSeconds: timeUsed
          }
        })

        const totalSeconds = answers.reduce((sum, a) => sum + a.timeUsedSeconds, 0)
        const response = await apiSubmitChallenge(challengeId, answers, totalSeconds)

        challengeResult.value = response.data || response
        challengeFinished.value = true
        showResult.value = true
        timerRef.value?.stop()
      } catch (error) {
        console.error('提交挑战失败', error)
        uni.showToast({
          title: '提交失败，请稍后重试',
          icon: 'none',
          duration: 2000
        })
      } finally {
        uni.hideLoading()
      }
    }
  })
}

const goBack = () => {
  if (challengeFinished.value) {
    goHome()
  } else {
    uni.showModal({
      title: '退出挑战',
      content: '确定要退出挑战吗？当前进度将不会保存',
      success: (modalRes) => {
        if (modalRes.confirm) {
          router.back()
        }
      }
    })
  }
}

const goHome = () => {
  router.push('/home')
}

const loadChallenge = async () => {
  try {
    uni.showLoading({ title: '加载中...', mask: true })

    const challengeId = route.query.challengeId as string

    if (!challengeId) {
      uni.showToast({
        title: '挑战 ID 缺失',
        icon: 'none',
        duration: 2000
      })
      router.back()
      return
    }

    // 从 sessionStorage 获取挑战数据（由 Challenge.vue 保存）
    const challengeDataStr = sessionStorage.getItem('challengeData')
    if (!challengeDataStr) {
      uni.showToast({
        title: '挑战数据已过期，请重新开始',
        icon: 'none',
        duration: 2000
      })
      router.back()
      return
    }

    const challengeData = JSON.parse(challengeDataStr)
    questions.value = challengeData.questions
    userAnswers.value = new Array(questions.value.length).fill('')
    correctAnswers.value = new Array(questions.value.length).fill('')

    if (questions.value.length === 0) {
      uni.showToast({
        title: '暂无挑战题目',
        icon: 'none',
        duration: 2000
      })
      router.back()
    }
  } catch (error) {
    console.error('加载挑战失败', error)
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
  loadChallenge()
})
</script>

<style scoped>
.challenge-question-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  padding: 15px 20px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.header-center {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
  justify-content: center;
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
  white-space: nowrap;
}

.question-count {
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 20px;
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
  background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
  transition: width 0.3s;
}

.question-content,
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
  border-color: #f5576c;
  background: #fff0f3;
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
  color: #f5576c;
  flex-shrink: 0;
}

.option-item.selected .option-key {
  background: #f5576c;
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

.result-icon.excellent {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
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

.score-circle.excellent {
  border-color: #22c55e;
  background: #dcfce7;
}

.score-circle.good {
  border-color: #60a5fa;
  background: #dbeafe;
}

.score-circle.normal {
  border-color: #fbbf24;
  background: #fef3c7;
}

.score-value {
  font-size: 42px;
  font-weight: bold;
  line-height: 1;
}

.score-circle.excellent .score-value {
  color: #22c55e;
}

.score-circle.good .score-value {
  color: #60a5fa;
}

.score-circle.normal .score-value {
  color: #fbbf24;
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
  color: #f5576c;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

/* 速答奖励部分 */
.speed-bonus-section {
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 20px;
  text-align: left;
}

.speed-bonus-section h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
  text-align: center;
}

.bonus-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bonus-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: white;
  border-radius: 8px;
  font-size: 14px;
}

.bonus-item.no-bonus {
  opacity: 0.6;
}

.bonus-question {
  color: #666;
}

.bonus-time {
  color: #999;
  font-size: 12px;
}

.bonus-points {
  font-weight: 600;
  font-size: 14px;
}

.bonus-points.bonus-high {
  color: #4ade80;
}

.bonus-points.bonus-medium {
  color: #60a5fa;
}

.bonus-points.bonus-low {
  color: #fbbf24;
}

.bonus-points.no-bonus {
  color: #999;
}

.total-bonus {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 2px solid #e0e0e0;
  font-size: 16px;
  font-weight: 600;
}

.total-bonus-points {
  color: #4ade80;
  font-size: 18px;
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
