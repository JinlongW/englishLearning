<template>
  <div class="home-container">
    <header class="header">
      <div class="user-info">
        <span class="welcome">你好，{{ userStore.studentName || '同学' }}!</span>
        <span class="level-badge">{{ userStore.levelName }}</span>
      </div>
    </header>

    <main class="main-content">
      <!-- 每日打卡 -->
      <section class="checkin-section">
        <div class="checkin-card" :class="{ checked: checked }">
          <div class="checkin-info">
            <h3>每日打卡</h3>
            <p>连续签到 {{ userStore.currentStreak }} 天</p>
          </div>
          <button class="checkin-btn" @click="startDailyCheckin" :disabled="checked || checkingIn">
            {{ checkingIn ? '加载中...' : checked ? '已打卡' : '去打卡' }}
          </button>
        </div>
      </section>

      <!-- 学习进度 -->
      <section class="stats-section">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-value">{{ stats.wordsLearned }}</div>
          <div class="stat-label">已学单词</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-value">{{ stats.grammarLearned }}</div>
          <div class="stat-label">语法课程</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏆</div>
          <div class="stat-value">{{ stats.challengesCompleted }}</div>
          <div class="stat-label">完成挑战</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">❌</div>
          <div class="stat-value">{{ stats.wrongQuestions }}</div>
          <div class="stat-label">错题本</div>
        </div>
      </section>

      <!-- 快捷入口 -->
      <section class="quick-actions">
        <h2>开始学习</h2>
        <div class="action-grid">
          <router-link to="/words" class="action-card word">
            <div class="action-icon">🔤</div>
            <span>学单词</span>
          </router-link>
          <router-link to="/grammar" class="action-card grammar">
            <div class="action-icon">📖</div>
            <span>学语法</span>
          </router-link>
          <router-link to="/challenge" class="action-card challenge">
            <div class="action-icon">⚔️</div>
            <span>每日挑战</span>
          </router-link>
          <router-link to="/wrong-questions" class="action-card wrong">
            <div class="action-icon">📝</div>
            <span>错题本</span>
          </router-link>
        </div>
      </section>
    </main>

    <BottomNav />

    <!-- 每日打卡答题弹窗 -->
    <div v-if="showCheckinModal" class="modal-overlay" @click.self="closeCheckinModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>每日打卡 - {{ currentQuestionIndex + 1 }} / {{ checkinQuestions.length }}</h3>
          <button class="close-btn" @click="closeCheckinModal">✕</button>
        </div>

        <div class="question-container" v-if="currentQuestion">
          <div class="question-card">
            <div class="question-stem">{{ currentQuestion.questionStem }}</div>
            <div class="options-list">
              <button
                v-for="option in currentQuestion.options"
                :key="option.id"
                class="option-item"
                :class="{ selected: selectedAnswer === option.optionKey, disabled: answered }"
                @click="selectAnswer(option.optionKey)"
              >
                {{ option.optionContent }}
              </button>
            </div>
          </div>
          <div v-if="answered" class="answer-feedback" :class="{ correct: isCorrect, wrong: !isCorrect }">
            <p><strong>{{ isCorrect ? '✓ 回答正确' : '✗ 回答错误' }}</strong></p>
            <p v-if="!isCorrect">正确答案：<strong>{{ correctAnswer }}</strong></p>
            <p v-if="currentQuestion.questionStem" class="analysis">{{ currentQuestion.answerAnalysis || '' }}</p>
          </div>
          <button
            v-if="answered"
            class="next-btn"
            :disabled="currentQuestionIndex >= checkinQuestions.length - 1 && !allAnswered || submitting"
            @click="nextQuestion"
          >
            {{ submitting ? '提交中...' : (currentQuestionIndex >= checkinQuestions.length - 1 ? '完成打卡' : '下一题') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import apiClient from '@/api/request'
import type { QuestionDetailResponse } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'

const userStore = useUserStore()
const checked = ref(false)
const checkingIn = ref(false)
const submitting = ref(false)
const showCheckinModal = ref(false)
const checkinQuestions = ref<QuestionDetailResponse[]>([])
const currentQuestionIndex = ref(0)
const selectedAnswer = ref<string | null>(null)
const answered = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')

const stats = ref({
  wordsLearned: 0,
  grammarLearned: 0,
  challengesCompleted: 0,
  wrongQuestions: 0
})

const currentQuestion = computed(() => checkinQuestions.value[currentQuestionIndex.value])

const allAnswered = computed(() => {
  return currentQuestionIndex.value >= checkinQuestions.value.length - 1 && answered.value
})

// 开始每日打卡 - 加载题目
const startDailyCheckin = async () => {
  if (checkingIn.value || checked.value) return

  try {
    checkingIn.value = true
    const questions = await apiClient.get<never, QuestionDetailResponse[]>('/user/daily-checkin/questions')
    if (!questions || questions.length === 0) {
      uni.showToast({ title: '暂无题目，请稍后重试', icon: 'none' })
      return
    }
    checkinQuestions.value = questions
    currentQuestionIndex.value = 0
    selectedAnswer.value = null
    answered.value = false
    isCorrect.value = false
    correctAnswer.value = ''
    showCheckinModal.value = true
  } catch (error) {
    console.error('加载打卡题目失败', error)
    uni.showToast({ title: '加载失败，请重试', icon: 'none', duration: 2000 })
  } finally {
    checkingIn.value = false
  }
}

// 选择答案
const selectAnswer = async (answer: string) => {
  if (answered.value || !currentQuestion.value) return

  selectedAnswer.value = answer
  answered.value = true
  submitting.value = true

  try {
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
    isCorrect.value = result.isCorrect
    correctAnswer.value = result.correctAnswer
  } catch (error) {
    console.error('提交答案失败', error)
    uni.showToast({ title: '提交失败，请重试', icon: 'none' })
  } finally {
    submitting.value = false
  }
}

// 下一题 / 完成打卡
const nextQuestion = async () => {
  if (!allAnswered.value) {
    currentQuestionIndex.value++
    selectedAnswer.value = null
    answered.value = false
    isCorrect.value = false
    correctAnswer.value = ''
    return
  }

  // 所有题目完成，正式打卡签到
  try {
    await apiClient.post('/user/checkin')
    checked.value = true
    showCheckinModal.value = false
    uni.showToast({
      title: `打卡成功！+5 积分`,
      icon: 'success',
      duration: 2000
    })
    // 刷新用户信息和统计
    await userStore.fetchUserInfo()
    const res = await apiClient.get('/user/stats')
    stats.value = {
      wordsLearned: res.wordsLearned || 0,
      grammarLearned: res.grammarsCompleted || 0,
      challengesCompleted: res.challengesCompleted || 0,
      wrongQuestions: res.wrongQuestionCount || 0
    }
  } catch (error: any) {
    console.error('打卡失败', error)
    uni.showToast({
      title: error.message || '打卡失败，请重试',
      icon: 'none',
      duration: 2000
    })
  }
}

// 关闭弹窗
const closeCheckinModal = () => {
  if (!answered.value || confirm('确认退出打卡？未保存当前答案')) {
    showCheckinModal.value = false
  }
}

onMounted(async () => {
  try {
    await userStore.fetchUserInfo()
    // 检查今天是否已打卡
    try {
      const statusRes = await apiClient.get<never, { hasCheckedIn: boolean }>('/user/checkin/status')
      checked.value = statusRes.hasCheckedIn
    } catch (statusError) {
      // 如果状态检查失败，保持默认 false 不变，不影响用户使用
      console.warn('检查打卡状态失败', statusError)
    }
    // 获取学习统计数据
    const res = await apiClient.get('/user/stats')
    stats.value = {
      wordsLearned: res.wordsLearned || 0,
      grammarLearned: res.grammarsCompleted || 0,
      challengesCompleted: res.challengesCompleted || 0,
      wrongQuestions: res.wrongQuestionCount || 0
    }
  } catch (error) {
    console.error('加载用户信息失败', error)
    uni.showToast({
      title: '加载失败，请重试',
      icon: 'none',
      duration: 2000
    })
  }
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome {
  font-size: 18px;
}

.level-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.main-content {
  padding: 20px;
}

.checkin-section {
  margin-bottom: 20px;
}

.checkin-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.checkin-card.checked {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.checkin-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
}

.checkin-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.checkin-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 15px 10px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.quick-actions {
  margin-bottom: 20px;
}

.quick-actions h2 {
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.action-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  text-decoration: none;
  color: #333;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.action-card.word .action-icon { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); -webkit-background-clip: text; }
.action-card.grammar .action-icon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; }
.action-card.challenge .action-icon { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; }
.action-card.wrong .action-icon { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; }

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
}

.question-container {
  padding: 20px;
}

.question-card {
  margin-bottom: 20px;
}

.question-stem {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.6;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 10px;
  background: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.option-item:hover:not(:disabled) {
  border-color: #667eea;
  background: #f0f4ff;
}

.option-item.selected {
  border-color: #667eea;
  background: #f0f4ff;
}

.option-item.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.answer-feedback {
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
}

.answer-feedback.correct {
  background: #dcfce7;
  color: #166534;
}

.answer-feedback.wrong {
  background: #fee2e2;
  color: #991b1b;
}

.answer-feedback .analysis {
  margin-top: 8px;
  font-size: 14px;
  opacity: 0.8;
}

.next-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
