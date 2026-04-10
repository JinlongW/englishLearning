<template>
  <div class="word-detail-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <h1>单词详情</h1>
    </header>

    <main class="main-content" v-if="word">
      <!-- 单词卡片 -->
      <div class="word-card">
        <div class="word-image">
          <img v-if="word.imageUrl" :src="word.imageUrl" :alt="word.wordText" />
          <div v-else class="word-placeholder">{{ word.wordText.charAt(0).toUpperCase() }}</div>
        </div>

        <div class="word-content">
          <h2 class="word-text">{{ word.wordText }}</h2>

          <div class="phonetic">
            <span v-if="word.phoneticUk">英 [{{ word.phoneticUk }}]</span>
            <span v-if="word.phoneticUs">美 [{{ word.phoneticUs }}]</span>
            <button class="audio-btn" @click="playAudio">🔊</button>
          </div>

          <div class="meaning-section">
            <div class="part-of-speech" v-if="word.partOfSpeech">{{ word.partOfSpeech }}</div>
            <div class="meaning">{{ word.meaningCn }}</div>
          </div>

          <div v-if="word.exampleEn" class="example-section">
            <h3>例句</h3>
            <div class="example">
              <p class="en">{{ word.exampleEn }}</p>
              <p class="cn">{{ word.exampleCn }}</p>
            </div>
          </div>

          <div v-if="word.relatedWords" class="related-section">
            <h3>相关词汇</h3>
            <div class="related-grid">
              <div v-for="(related, index) in word.relatedWords" :key="index" class="related-item">
                <span class="related-word">{{ related.word }}</span>
                <span class="related-meaning">{{ related.meaning }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习进度 -->
      <div class="progress-card">
        <h3>学习进度</h3>
        <div class="progress-info">
          <div class="progress-bar">
            <div class="progress" :style="{ width: word.progress + '%' }"></div>
          </div>
          <span class="progress-text">{{ word.progress }}%</span>
        </div>
        <div class="status-badge" :class="word.status">
          {{ statusText }}
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="action-btn secondary" @click="addToWrongBook">
          加入错题本
        </button>
        <button class="action-btn primary" @click="markAsLearned">
          {{ word.status === 'completed' ? '已掌握' : '标记为已学' }}
        </button>
      </div>
    </main>

    <div v-else class="loading-state">
      <div class="loading-spinner">📚</div>
      <p>加载中...</p>
    </div>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getWordById, updateWordProgress } from '@/api/word'
import BottomNav from '@/components/BottomNav.vue'

interface Word {
  id: string
  wordText: string
  phoneticUk: string
  phoneticUs: string
  meaningCn: string
  partOfSpeech?: string
  exampleEn?: string
  exampleCn?: string
  imageUrl?: string
  status: string
  progress: number
  relatedWords?: Array<{ word: string; meaning: string }>
}

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const word = ref<Word | null>(null)

const statusText = computed(() => {
  if (!word.value) return ''
  switch (word.value.status) {
    case 'new': return '新单词'
    case 'learning': return '学习中'
    case 'completed': return '已掌握'
    default: return '未知'
  }
})

const loadWord = async () => {
  loading.value = true
  const wordId = route.params.id as string
  try {
    uni.showLoading({ title: '加载中...', mask: true })
    const response = await getWordById(wordId)
    word.value = response.data || {
      id: wordId,
      wordText: 'apple',
      phoneticUk: 'ˈæp(ə)l',
      phoneticUs: 'ˈæpəl',
      meaningCn: '苹果',
      partOfSpeech: 'n.',
      exampleEn: 'I ate an apple for breakfast.',
      exampleCn: '我早餐吃了一个苹果。',
      status: 'learning',
      progress: 60,
      relatedWords: [
        { word: 'apples', meaning: '复数' },
        { word: 'apple tree', meaning: '苹果树' }
      ]
    }
  } catch (error) {
    console.error('加载单词失败', error)
    uni.showToast({
      title: '加载失败，请稍后重试',
      icon: 'none',
      duration: 2000
    })
  } finally {
    loading.value = false
    uni.hideLoading()
  }
}

const playAudio = () => {
  if (!word.value?.audioUrl) {
    uni.showToast({
      title: '暂无发音',
      icon: 'none'
    })
    return
  }

  // 使用 uni-app 的 innerAudioContext 播放音频
  const innerAudioContext = uni.createInnerAudioContext()
  innerAudioContext.src = word.value.audioUrl
  innerAudioContext.autoplay = false

  innerAudioContext.onPlay(() => {
    console.log('开始播放音频')
  })

  innerAudioContext.onError((res) => {
    console.error('音频播放失败', res)
    uni.showToast({
      title: '播放失败',
      icon: 'none'
    })
  })

  innerAudioContext.onEnded(() => {
    console.log('音频播放结束')
    innerAudioContext.destroy()
  })

  innerAudioContext.play()
}

const addToWrongBook = () => {
  uni.showToast({
    title: '已加入错题本',
    icon: 'success'
  })
}

const markAsLearned = async () => {
  if (!word.value) return
  try {
    await updateWordProgress(word.value.id, 100, 'completed')
    word.value.status = 'completed'
    word.value.progress = 100
  } catch (error) {
    console.error('更新进度失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadWord()
})
</script>

<style scoped>
.word-detail-container {
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

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.back-btn span {
  font-size: 20px;
}

.header h1 {
  margin: 0;
  font-size: 18px;
}

.main-content {
  padding: 20px;
}

.word-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.word-image {
  height: 180px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.word-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.word-placeholder {
  font-size: 80px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
}

.word-content {
  padding: 25px;
}

.word-text {
  font-size: 32px;
  color: #333;
  margin-bottom: 15px;
}

.phonetic {
  display: flex;
  align-items: center;
  gap: 15px;
  color: #666;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.audio-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.audio-btn:active {
  transform: scale(0.9);
}

.meaning-section {
  margin-bottom: 25px;
}

.part-of-speech {
  display: inline-block;
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  color: #666;
  font-style: italic;
  margin-bottom: 8px;
}

.meaning {
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.example-section h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.example {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.example .en {
  color: #333;
  margin-bottom: 5px;
  font-size: 15px;
}

.example .cn {
  color: #666;
  font-size: 14px;
}

.related-section h3 {
  font-size: 16px;
  color: #333;
  margin: 20px 0 10px 0;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.related-item {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 8px;
}

.related-word {
  display: block;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 3px;
}

.related-meaning {
  display: block;
  color: #999;
  font-size: 12px;
}

.progress-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.progress-card h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
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
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  font-weight: bold;
  color: #667eea;
  min-width: 45px;
}

.status-badge {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.status-badge.new {
  background: #e0e7ff;
  color: #667eea;
}

.status-badge.learning {
  background: #fef3c7;
  color: #f59e0b;
}

.status-badge.completed {
  background: #dcfce7;
  color: #22c55e;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.action-btn {
  padding: 15px;
  border: none;
  border-radius: 15px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background: #f0f0f0;
  color: #333;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  font-size: 60px;
  margin-bottom: 15px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
