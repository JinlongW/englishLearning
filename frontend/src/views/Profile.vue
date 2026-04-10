<template>
  <div class="profile-container">
    <header class="header">
      <div class="user-info">
        <div class="avatar">
          {{ userStore.studentName?.charAt(0) || '学' }}
        </div>
        <div class="user-detail">
          <h2>{{ userStore.studentName || '同学' }}</h2>
          <p>{{ userStore.username }}</p>
          <span class="grade-badge">{{ gradeText }}</span>
        </div>
      </div>
    </header>

    <main class="main-content">
      <!-- 等级信息 -->
      <section class="level-section">
        <div class="level-card">
          <div class="level-info">
            <span class="level-icon">⭐</span>
            <div>
              <div class="level-name">{{ userStore.levelName }}</div>
              <div class="level-progress">
                Lv.{{ userStore.currentLevel }} · EXP {{ userStore.currentExp }} / 500
              </div>
            </div>
          </div>
          <div class="exp-bar">
            <div class="exp-progress" :style="{ width: expPercent + '%' }"></div>
          </div>
        </div>
      </section>

      <!-- 学习统计 -->
      <section class="stats-section">
        <h2>学习统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">📚</div>
            <div class="stat-value">{{ stats.wordsLearned }}</div>
            <div class="stat-label">学习单词</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📝</div>
            <div class="stat-value">{{ stats.grammarLearned }}</div>
            <div class="stat-label">语法课程</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">{{ stats.challengesCompleted }}</div>
            <div class="stat-label">完成挑战</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🔥</div>
            <div class="stat-value">{{ userStore.currentStreak }}</div>
            <div class="stat-label">连续打卡</div>
          </div>
        </div>
      </section>

      <!-- 积分和徽章 -->
      <section class="rewards-section">
        <h2>我的成就</h2>
        <div class="rewards-grid">
          <div class="reward-card">
            <div class="reward-icon">💰</div>
            <div class="reward-info">
              <div class="reward-value">{{ stats.totalPoints }}</div>
              <div class="reward-label">总积分</div>
            </div>
          </div>
          <div class="reward-card">
            <div class="reward-icon">🎖️</div>
            <div class="reward-info">
              <div class="reward-value">{{ badges.length }}</div>
              <div class="reward-label">徽章</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 徽章展示 -->
      <section class="badges-section">
        <h2>徽章收藏</h2>
        <div class="badges-grid">
          <div
            v-for="badge in badges"
            :key="badge.id"
            class="badge-card"
            :class="{ earned: badge.earned }"
          >
            <div class="badge-icon">{{ badge.icon }}</div>
            <div class="badge-name">{{ badge.name }}</div>
          </div>
          <!-- 未获得的徽章 -->
          <div v-for="i in 4" :key="'lock-' + i" class="badge-card locked">
            <div class="badge-icon">🔒</div>
            <div class="badge-name">???</div>
          </div>
        </div>
      </section>

      <!-- 设置选项 -->
      <section class="settings-section">
        <h2>设置</h2>
        <div class="settings-list">
          <button class="setting-item">
            <span class="setting-icon">🔔</span>
            <span>通知设置</span>
            <span class="setting-arrow">›</span>
          </button>
          <button class="setting-item">
            <span class="setting-icon">🔒</span>
            <span>修改密码</span>
            <span class="setting-arrow">›</span>
          </button>
          <button class="setting-item" @click="handleLogout">
            <span class="setting-icon">🚪</span>
            <span>退出登录</span>
            <span class="setting-arrow">›</span>
          </button>
        </div>
      </section>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()

const gradeText = computed(() => {
  const grades = ['', '一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '七年级', '八年级', '九年级', '高一', '高二', '高三']
  return grades[userStore.gradeLevel] || '未知年级'
})

const expPercent = computed(() => {
  return Math.min((userStore.currentExp / 500) * 100, 100)
})

const stats = {
  wordsLearned: 120,
  grammarLearned: 15,
  challengesCompleted: 8,
  totalPoints: 450
}

const badges = [
  { id: '1', icon: '🌟', name: '学习新星', earned: true },
  { id: '2', icon: '🔥', name: '打卡达人', earned: true },
  { id: '3', icon: '📚', name: '单词大师', earned: true },
  { id: '4', icon: '🏆', name: '挑战王者', earned: false }
]

const handleLogout = async () => {
  try {
    const { confirm } = await uni.showModal({
      title: '提示',
      content: '确定要退出登录吗？'
    })
    if (confirm) {
      userStore.logout()
      uni.showToast({
        title: '已退出登录',
        icon: 'success'
      })
      router.push('/login')
    }
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 20px;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
}

.user-detail h2 {
  margin: 0 0 5px 0;
  font-size: 24px;
}

.user-detail p {
  margin: 0 0 8px 0;
  opacity: 0.9;
  font-size: 14px;
}

.grade-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.main-content {
  padding: 20px;
}

.level-section {
  margin-bottom: 20px;
}

.level-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.level-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.level-icon {
  font-size: 48px;
}

.level-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.level-progress {
  font-size: 14px;
  color: #666;
}

.exp-bar {
  height: 10px;
  background: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
}

.exp-progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.stats-section,
.rewards-section,
.badges-section,
.settings-section {
  margin-bottom: 20px;
}

section h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 18px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.stat-item {
  background: white;
  border-radius: 15px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.rewards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.reward-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.reward-icon {
  font-size: 40px;
}

.reward-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.reward-label {
  font-size: 12px;
  color: #999;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.badge-card {
  background: white;
  border-radius: 15px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.badge-card.locked {
  opacity: 0.5;
}

.badge-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.badge-name {
  font-size: 12px;
  color: #666;
}

.settings-list {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.setting-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px 20px;
  background: none;
  border: none;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item:hover {
  background: #f5f7fa;
}

.setting-icon {
  font-size: 24px;
}

.setting-item span:nth-child(2) {
  flex: 1;
  text-align: left;
  font-size: 16px;
  color: #333;
}

.setting-arrow {
  font-size: 24px;
  color: #ccc;
}
</style>
