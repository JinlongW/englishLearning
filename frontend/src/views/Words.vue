<template>
  <div class="words-container">
    <header class="header">
      <h1>学单词</h1>
      <div class="progress-info">
        <span>已学：{{ learnedCount }} / {{ totalCount }}</span>
        <div class="progress-bar">
          <div class="progress" :style="{ width: progressPercent + '%' }"></div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <!-- 年级单元选择器 -->
      <GradeUnitSelector ref="gradeUnitSelectorRef" v-model="selectedUnitId" @update:modelValue="onUnitChange" @loaded="onGradeUnitLoaded" />

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner">📚</div>
        <p>加载中...</p>
      </div>

      <!-- 单词卡片 -->
      <div class="word-card" v-else-if="currentWord">
        <div class="word-image">
          <img v-if="currentWord.imageUrl" :src="currentWord.imageUrl" :alt="currentWord.wordText" />
          <div v-else class="word-placeholder">🔤</div>
        </div>

        <div class="word-content">
          <h2 class="word-text">{{ currentWord.wordText }}</h2>
          <div class="phonetic">
            <span v-if="currentWord.phoneticUk">英 [{{ currentWord.phoneticUk }}]</span>
            <span v-if="currentWord.phoneticUs">美 [{{ currentWord.phoneticUs }}]</span>
            <button class="audio-btn" @click="playAudio">🔊</button>
          </div>

          <div class="meaning">
            <p class="cn">{{ currentWord.meaningCn }}</p>
            <p v-if="currentWord.partOfSpeech" class="pos">{{ currentWord.partOfSpeech }}</p>
          </div>

          <div v-if="currentWord.exampleEn" class="example">
            <p class="en">{{ currentWord.exampleEn }}</p>
            <p class="cn">{{ currentWord.exampleCn }}</p>
          </div>
        </div>

        <div class="actions">
          <button class="action-btn prev" @click="prevWord">上一个</button>
          <button class="action-btn know" @click="markAsKnown">认识</button>
          <button class="action-btn unknown" @click="markAsUnknown">不认识</button>
          <button class="action-btn next" @click="nextWord">下一个</button>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🎉</div>
        <p>太棒了！这个单元的单词都学完了！</p>
        <button class="next-unit-btn" @click="nextUnit">下一个单元</button>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getWords, updateWordProgress } from '@/api/word'
import type { Word } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'
import GradeUnitSelector from '@/components/GradeUnitSelector.vue'

const gradeUnitSelectorRef = ref<InstanceType<typeof GradeUnitSelector> | null>(null)
const loading = ref(false)
const learnedCount = ref(0)
const totalCount = ref(0)
const currentWordIndex = ref(0)
const words = ref<Word[]>([])
const selectedUnitId = ref<string>('')

const currentWord = computed(() => words.value[currentWordIndex.value])
const progressPercent = computed(() => (learnedCount.value / (totalCount.value || 1)) * 100)

// 处理单元切换
const onUnitChange = (unitId: string) => {
  selectedUnitId.value = unitId
  loadWords()
}

// 处理年级单元加载完成
const onGradeUnitLoaded = (unitId: string, count: number, totalCount: number) => {
  // 同步已学数量，确保顶部进度与单元卡片一致
  learnedCount.value = count
  totalCount.value = totalCount
}

const loadWords = async () => {
  if (loading.value) return
  if (!selectedUnitId.value) {
    console.log('未选择单元，跳过加载')
    return
  }

  loading.value = true
  try {
    uni.showLoading({ title: '加载中...', mask: true })

    console.log('开始加载单词... gradeUnitId:', selectedUnitId.value)
    const response = await getWords(selectedUnitId.value)
    console.log('API 响应:', response)
    // API 拦截器可能已经解包响应，需要处理两种情况
    const data = response?.data || response
    words.value = data?.items || []
    totalCount.value = data?.total || words.value.length
    console.log('加载完成，words 数量:', words.value.length, 'total:', totalCount.value)
    // 计算已学数量：状态为 completed 或 mastered 的单词
    learnedCount.value = words.value.filter(w => w.status === 'completed' || w.status === 'mastered').length

    // 加载完成后同步单元进度显示
    gradeUnitSelectorRef.value?.refresh()
  } catch (error) {
    console.error('加载单词失败', error)
    const errorMessage = error instanceof Error ? error.message : String(error)
    uni.showToast({
      title: '加载失败: ' + errorMessage,
      icon: 'none',
      duration: 3000
    })
    words.value = []
    totalCount.value = 0
    learnedCount.value = 0
  } finally {
    loading.value = false
    uni.hideLoading()
  }
}

const playAudio = () => {
  if (!currentWord.value) {
    uni.showToast({
      title: '无单词数据',
      icon: 'none'
    })
    return
  }

  const wordText = currentWord.value.wordText
  const audioUrl = currentWord.value.audioUrl
  console.log('播放单词发音:', wordText, '音频 URL:', audioUrl)

  // 检测是否为移动设备
  const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)

  if (isMobile && audioUrl) {
    // 移动端优先使用音频 URL
    playWithAudioUrl(audioUrl)
  } else if ('speechSynthesis' in window) {
    // PC 端或无音频 URL 时使用语音合成
    playWithSpeechSynthesis(wordText)
  } else {
    // 降级方案：尝试使用音频 URL
    if (audioUrl) {
      playWithAudioUrl(audioUrl)
    } else {
      uni.showToast({
        title: '不支持发音',
        icon: 'none'
      })
    }
  }
}

// 使用音频 URL 播放
const playWithAudioUrl = (url: string) => {
  console.log('使用音频 URL 播放:', url)
  const audio = new Audio(url)
  audio.preload = 'auto'

  audio.addEventListener('play', () => {
    console.log('音频开始播放')
  })

  audio.addEventListener('ended', () => {
    console.log('音频播放结束')
  })

  audio.addEventListener('error', (e) => {
    console.error('音频播放失败:', e)
    // 如果音频 URL 播放失败，降级到语音合成
    if ('speechSynthesis' in window && currentWord.value) {
      console.log('降级到语音合成')
      playWithSpeechSynthesis(currentWord.value.wordText)
    } else {
      uni.showToast({
        title: '播放失败',
        icon: 'none',
        duration: 2000
      })
    }
  })

  audio.play().catch((err) => {
    console.error('Audio.play() 失败:', err)
    // 降级到语音合成
    if ('speechSynthesis' in window && currentWord.value) {
      console.log('降级到语音合成')
      playWithSpeechSynthesis(currentWord.value.wordText)
    }
  })
}

// 使用语音合成播放
const playWithSpeechSynthesis = (text: string) => {
  console.log('使用语音合成播放:', text)
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'en-US'
  utterance.rate = 0.8
  utterance.pitch = 1

  utterance.addEventListener('start', () => {
    console.log('语音合成开始')
  })

  utterance.addEventListener('end', () => {
    console.log('语音合成结束')
  })

  utterance.addEventListener('error', (e) => {
    console.error('语音合成失败:', e)
    uni.showToast({
      title: '播放失败',
      icon: 'none',
      duration: 2000
    })
  })

  speechSynthesis.speak(utterance)
}

const markAsKnown = async () => {
  if (!currentWord.value) return

  // 如果已经是完成状态，只跳转到下一个单词
  if (currentWord.value.status === 'completed' || currentWord.value.status === 'mastered') {
    nextWord()
    return
  }

  try {
    await updateWordProgress(currentWord.value.id, 100, 'completed')
    // API 调用成功后才更新本地状态
    currentWord.value.status = 'completed'

    // 重新计算已学数量
    learnedCount.value = words.value.filter(w => w.status === 'completed' || w.status === 'mastered').length

    // 每次成功后都刷新单元进度显示
    gradeUnitSelectorRef.value?.refresh()

    // 检查是否所有单词都已完成
    const allCompleted = words.value.every(w => w.status === 'completed' || w.status === 'mastered')
    if (allCompleted) {
      // 显示完成提示
      uni.showToast({
        title: '本单元已学完！',
        icon: 'success'
      })
    }

    nextWord()
  } catch (error) {
    console.error('更新进度失败', error)
    const errorMessage = error instanceof Error ? error.message : '更新失败'
    uni.showToast({
      title: errorMessage,
      icon: 'none',
      duration: 2000
    })
    // 不跳转到下一个单词，让用户重试
  }
}

const markAsUnknown = async () => {
  if (!currentWord.value) return

  try {
    await updateWordProgress(currentWord.value.id, 0, 'learning')
    // API 调用成功后才更新本地状态
    currentWord.value.status = 'learning'
    nextWord()
  } catch (error) {
    console.error('更新进度失败', error)
    const errorMessage = error instanceof Error ? error.message : '更新失败'
    uni.showToast({
      title: errorMessage,
      icon: 'none',
      duration: 2000
    })
    // 不跳转到下一个单词，让用户重试
  }
}

const prevWord = () => {
  if (currentWordIndex.value > 0) {
    currentWordIndex.value--
  }
}

const nextWord = () => {
  if (currentWordIndex.value < words.value.length - 1) {
    currentWordIndex.value++
  } else {
    // 已经是最后一个单词，检查是否全部学完
    const allCompleted = words.value.every(w => w.status === 'completed' || w.status === 'mastered')
    if (allCompleted) {
      uni.showToast({
        title: '本单元已学完！',
        icon: 'success',
        duration: 2000
      })
      // 刷新单元进度显示
      gradeUnitSelectorRef.value?.refresh()
    }
  }
}

const nextUnit = () => {
  uni.showToast({
    title: '切换到下一个单元',
    icon: 'none'
  })
}

onMounted(() => {
  loadWords()
})
</script>

<style scoped>
.words-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.header h1 {
  margin-bottom: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #4ade80;
  transition: width 0.3s;
}

.main-content {
  padding: 20px;
}

.word-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.word-image {
  height: 200px;
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
}

.word-content {
  padding: 25px;
}

.word-text {
  font-size: 36px;
  color: #333;
  margin-bottom: 10px;
}

.phonetic {
  display: flex;
  align-items: center;
  gap: 15px;
  color: #666;
  margin-bottom: 20px;
}

.audio-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.meaning {
  margin-bottom: 20px;
}

.meaning .cn {
  font-size: 20px;
  color: #333;
  margin-bottom: 5px;
}

.meaning .pos {
  font-size: 14px;
  color: #999;
  font-style: italic;
}

.example {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 10px;
}

.example .en {
  color: #333;
  margin-bottom: 5px;
}

.example .cn {
  color: #666;
  font-size: 14px;
}

.actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  padding: 20px;
}

.action-btn {
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s;
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn.prev {
  background: #e0e0e0;
  color: #333;
}

.action-btn.know {
  background: #4ade80;
  color: white;
}

.action-btn.unknown {
  background: #f87171;
  color: white;
}

.action-btn.next {
  background: #667eea;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
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

.next-unit-btn {
  margin-top: 20px;
  padding: 15px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
}
</style>
