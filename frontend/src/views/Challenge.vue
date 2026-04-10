<template>
  <div class="challenge-container">
    <header class="header" :class="headerClass">
      <div class="header-top">
        <h1>每日挑战</h1>
        <div class="theme-badge" :class="themeBadgeClass">
          <span class="theme-icon">{{ todayChallenge.themeIcon }}</span>
          <span class="theme-name">{{ todayChallenge.themeName }}</span>
          <span v-if="todayChallenge.bonusMultiplier > 1" class="bonus-tag">
            {{ todayChallenge.bonusMultiplier }}倍奖励
          </span>
        </div>
      </div>
      <p>每天进步一点点！</p>
    </header>

    <main class="main-content">
      <!-- 今日挑战 -->
      <div class="today-challenge">
        <div class="challenge-card">
          <div class="challenge-header">
            <span class="challenge-icon">📅</span>
            <div class="challenge-info">
              <h3>{{ todayChallenge.date }}</h3>
              <p>已完成 {{ todayChallenge.correctCount }} / {{ todayChallenge.totalQuestions }}</p>
            </div>
          </div>
          <div class="challenge-progress">
            <div class="progress-bar">
              <div class="progress" :style="{ width: progress + '%' }"></div>
            </div>
            <span class="progress-text">{{ progress }}%</span>
          </div>
          <button class="start-btn" @click="startChallenge" :disabled="loading">
            {{ loading ? '启动中...' : todayChallenge.isCompleted ? '已完成的挑战' : '开始挑战' }}
          </button>
        </div>
      </div>

      <!-- 挑战记录 -->
      <section class="history-section">
        <h2>挑战记录</h2>
        <div class="history-list">
          <div v-for="item in history" :key="item.date" class="history-card">
            <div class="history-date">{{ item.date }}</div>
            <div class="history-score" :class="item.scoreClass">{{ item.score }}分</div>
            <div class="history-detail">{{ item.correct }} / {{ item.total }} 正确</div>
          </div>
        </div>
      </section>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTodayChallenge, startChallenge } from '@/api/challenge'
import type { DailyChallengeDto } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()

const todayChallenge = ref<DailyChallengeDto>({
  id: null,
  date: new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' }),
  status: 'pending',
  isCompleted: false,
  totalQuestions: 10,
  correctCount: 0,
  score: 0,
  pointsEarned: 0,
  coinsEarned: 0,
  theme: 'mixed',
  themeName: '综合日',
  themeIcon: '🎯',
  bonusMultiplier: 1
})

const loading = ref(false)

const headerClass = computed(() => `header-${todayChallenge.value.theme}`)

const themeBadgeClass = computed(() => `badge-${todayChallenge.value.theme}`)

const progress = computed(() => {
  if (todayChallenge.value.totalQuestions === 0) return 0
  return Math.round((todayChallenge.value.correctCount / todayChallenge.value.totalQuestions) * 100)
})

const loadTodayChallenge = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const res = await getTodayChallenge()
    todayChallenge.value = res
  } catch (error) {
    console.error('加载每日挑战失败', error)
    const errorMessage = error instanceof Error ? error.message : '加载失败，请稍后重试'
    uni.showToast({
      title: errorMessage,
      icon: 'none',
      duration: 3000
    })
  } finally {
    loading.value = false
  }
}

const startChallenge = async () => {
  if (todayChallenge.value.isCompleted) {
    uni.showToast({
      title: '今日挑战已完成，明天再来吧！',
      icon: 'none'
    })
    return
  }
  // 调用后端开始挑战，然后跳转到挑战答题页面
  try {
    const res = await startChallenge()
    // 将挑战数据保存到 sessionStorage
    sessionStorage.setItem('challengeData', JSON.stringify({
      challengeId: res.challengeId,
      questions: res.questions
    }))
    uni.showToast({
      title: `挑战已开始，共 ${res.questions.length} 道题目`,
      icon: 'success'
    })
    // 跳转到挑战答题页面，传递 challengeId
    router.push({
      path: '/challenge/answer',
      query: { challengeId: res.challengeId }
    })
  } catch (error) {
    console.error('启动挑战失败', error)
    uni.showToast({
      title: '启动失败，请稍后重试',
      icon: 'none'
    })
  }
}

onMounted(() => {
  loadTodayChallenge()
})
</script>

<style scoped>
.challenge-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  padding: 20px;
  color: white;
  transition: background 0.3s;
}

.header-vocabulary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header-grammar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.header-mixed {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.header-review {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.header-boss {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  animation: boss-pulse 2s ease-in-out infinite;
}

@keyframes boss-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.header h1 {
  margin-bottom: 5px;
}

.header p {
  opacity: 0.9;
  font-size: 14px;
}

.theme-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  font-size: 14px;
  font-weight: 600;
}

.theme-icon {
  font-size: 20px;
}

.theme-name {
  color: white;
}

.bonus-tag {
  background: #ff4757;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  animation: bonus-bounce 0.5s ease-in-out infinite alternate;
}

@keyframes bonus-bounce {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}

.badge-vocabulary {
  background: rgba(255, 255, 255, 0.3);
}

.badge-grammar {
  background: rgba(255, 255, 255, 0.3);
}

.badge-mixed {
  background: rgba(255, 255, 255, 0.3);
}

.badge-review {
  background: rgba(255, 255, 255, 0.35);
}

.badge-boss {
  background: rgba(255, 255, 255, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.main-content {
  padding: 20px;
}

.today-challenge {
  margin-bottom: 30px;
}

.challenge-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.challenge-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.challenge-icon {
  font-size: 48px;
}

.challenge-info h3 {
  color: #333;
  margin-bottom: 5px;
}

.challenge-info p {
  color: #666;
  font-size: 14px;
}

.challenge-progress {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.progress-bar {
  flex: 1;
  height: 10px;
  background: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
  transition: width 0.3s;
}

.progress-text {
  font-weight: bold;
  color: #f5576c;
  min-width: 45px;
}

.start-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.start-btn:hover {
  transform: scale(1.02);
}

.start-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.history-section {
  margin-bottom: 20px;
}

.history-section h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 18px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-card {
  background: white;
  border-radius: 15px;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.history-date {
  color: #666;
  font-size: 14px;
}

.history-score {
  font-weight: bold;
  font-size: 20px;
}

.history-score.excellent { color: #4ade80; }
.history-score.good { color: #60a5fa; }
.history-score.normal { color: #fbbf24; }

.history-detail {
  color: #999;
  font-size: 12px;
}
</style>
