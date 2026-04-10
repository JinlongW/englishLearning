<template>
  <div class="grammar-detail-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <h1>语法课程</h1>
      <div class="header-spacer"></div>
    </header>

    <main class="main-content" v-if="grammar">
      <!-- 课程标题卡片 -->
      <div class="title-card">
        <h2>{{ grammar.title }}</h2>
        <div class="meta-info">
          <span v-if="grammar.durationSeconds">⏱️ {{ formatDuration(grammar.durationSeconds) }}</span>
          <span :class="['status-badge', grammar.status]">
            {{ statusText }}
          </span>
        </div>
      </div>

      <!-- 标签页导航 -->
      <div class="tabs">
        <button
          :class="['tab-btn', { active: activeTab === 'learn' }]"
          @click="activeTab = 'learn'"
        >
          📖 规则学习
        </button>
        <button
          :class="['tab-btn', { active: activeTab === 'scene' }]"
          @click="activeTab = 'scene'"
        >
          🎬 情景学习
        </button>
        <button
          :class="['tab-btn', { active: activeTab === 'quiz' }]"
          @click="activeTab = 'quiz'"
        >
          📝 小测验
        </button>
      </div>

      <!-- 标签页内容区域 -->
      <div class="tab-content">
        <!-- 规则学习标签页 -->
        <div v-show="activeTab === 'learn'" class="tab-panel">
          <!-- 学习内容区域 -->
          <div v-if="contentSections.length > 0" class="content-card">
            <h3>课程内容</h3>
            <div class="content-sections">
              <div v-for="(section, index) in contentSections" :key="index" class="content-section">
                <h4 class="section-title">{{ section.title }}</h4>
                <div class="section-content" v-html="renderContent(section.content)"></div>
              </div>
            </div>
          </div>

          <!-- 例句区域 -->
          <div v-if="exampleSentences.length > 0" class="examples-card">
            <h3>例句</h3>
            <div v-for="(example, index) in exampleSentences" :key="index" class="example-item">
              <p class="example-en">{{ example.en }}</p>
              <p class="example-cn">{{ example.cn }}</p>
            </div>
          </div>
        </div>

        <!-- 情景学习标签页 -->
        <div v-show="activeTab === 'scene'" class="tab-panel">
          <div class="scene-intro">
            <p>🎬 通过生动的情景对话，轻松掌握语法知识！</p>
            <p class="hint">左右滑动切换场景</p>
          </div>

          <!-- 情景列表 -->
          <div class="scenes-list">
            <div
              v-for="(scene, index) in scenes"
              :key="index"
              class="scene-card"
              @click="enterSceneLearning(index)"
            >
              <div class="scene-icon">{{ scene.image }}</div>
              <div class="scene-info">
                <h4>{{ scene.title }}</h4>
                <p>{{ scene.dialogue.length }} 段对话 · {{ truncateText(scene.grammarPoint, 30) }}</p>
              </div>
              <div class="scene-arrow">›</div>
            </div>
          </div>

          <div v-if="scenes.length === 0" class="empty-scene">
            <p>情景内容开发中，敬请期待！</p>
          </div>
        </div>

        <!-- 小测验标签页 -->
        <div v-show="activeTab === 'quiz'" class="tab-panel">
          <div class="quiz-intro">
            <p>完成测验，检验学习成果！</p>
          </div>
          <button
            class="start-quiz-btn"
            @click="startQuiz"
            :disabled="grammar.status === 'locked'"
          >
            {{ grammar.status === 'completed' ? '重新测验' : (grammar.status === 'available' ? '开始测验' : '继续学习') }}
          </button>
          <p v-if="grammar.status === 'locked'" class="lock-hint">请先完成前面的课程</p>
        </div>
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
import { getGrammarById } from '@/api/grammar'
import type { GrammarDetailDto, SceneDto } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'

interface ContentSection {
  title: string
  content: string
}

interface ExampleSentence {
  en: string
  cn: string
}

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const grammar = ref<GrammarDetailDto | null>(null)
const activeTab = ref<'learn' | 'scene' | 'quiz'>('learn')

// 情景数据（示例数据，后续可从 contentJson 或 API 获取）
const scenes = ref<SceneDto[]>([
  {
    title: 'Tom 的日常',
    image: '🏫',
    dialogue: [
      { speaker: 'Tom', text: 'I go to school every day.' },
      { speaker: 'Lily', text: 'She goes to school at 8:00.' }
    ],
    grammarPoint: '一般现在时表示习惯性动作，第三人称单数动词加 -s'
  },
  {
    title: '午饭时间',
    image: '🍽️',
    dialogue: [
      { speaker: 'Tom', text: 'We eat lunch at 12:00.' },
      { speaker: 'Lily', text: 'He eats an apple every day.' }
    ],
    grammarPoint: '主语是复数时动词用原形，主语是第三人称单数时动词加 -s'
  },
  {
    title: '放学后',
    image: '⚽',
    dialogue: [
      { speaker: 'Tom', text: 'They play football after school.' },
      { speaker: 'Lily', text: 'She plays basketball on weekends.' }
    ],
    grammarPoint: '表示经常性、习惯性的动作或客观事实用一般现在时'
  }
])

// 解析内容区域
const contentSections = computed<ContentSection[]>(() => {
  if (!grammar.value?.contentJson) return []

  try {
    const content = JSON.parse(grammar.value.contentJson)
    if (Array.isArray(content)) {
      return content.map((section: { title?: string; rule?: string; explanation?: string; content?: string }) => ({
        title: section.title || '语法规则',
        content: section.rule || section.explanation || section.content || ''
      }))
    }
    if (typeof content === 'object') {
      return Object.entries(content).map(([title, value]) => ({
        title,
        content: typeof value === 'string' ? value : JSON.stringify(value)
      }))
    }
  } catch (e) {
    console.error('解析 contentJson 失败', e)
  }
  return []
})

// 解析例句
const exampleSentences = computed<ExampleSentence[]>(() => {
  if (!grammar.value?.contentJson) return []

  try {
    const content = JSON.parse(grammar.value.contentJson)
    if (Array.isArray(content)) {
      const examples: ExampleSentence[] = []
      content.forEach((section: { examples?: Array<{ en: string; cn: string }> }) => {
        if (section.examples && Array.isArray(section.examples)) {
          examples.push(...section.examples)
        }
      })
      return examples
    }
  } catch (e) {
    console.error('解析例句失败', e)
  }
  return []
})

const statusText = computed(() => {
  if (!grammar.value) return ''
  switch (grammar.value.status) {
    case 'locked': return '未解锁'
    case 'not_started': return '未开始'
    case 'available': return '可学习'
    case 'learning': return '学习中'
    case 'completed': return '已完成'
    default: return '未知'
  }
})

const formatDuration = (seconds: number): string => {
  const minutes = Math.round(seconds / 60)
  return `${minutes}分钟`
}

const renderContent = (content: string): string => {
  // 将换行符转换为<br>标签
  return content.replace(/\n/g, '<br>')
}

const startQuiz = () => {
  router.push(`/grammar/${grammar.value?.id}/quiz`)
}

const goBack = () => {
  router.back()
}

// 进入情景学习页面
const enterSceneLearning = (sceneIndex: number) => {
  if (!grammar.value) return
  router.push({
    path: '/grammar/story-learning',
    query: {
      id: grammar.value.id,
      title: grammar.value.title,
      sceneIndex: sceneIndex.toString()
    }
  })
}

// 截断文本
const truncateText = (text: string, length: number): string => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

const loadGrammar = async () => {
  loading.value = true
  const grammarId = route.params.id as string
  try {
    uni.showLoading({ title: '加载中...', mask: true })
    const response = await getGrammarById(grammarId)
    grammar.value = response.data || response
  } catch (error) {
    console.error('加载语法课程失败', error)
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

onMounted(() => {
  loadGrammar()
})
</script>

<style scoped>
.grammar-detail-container {
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

.header-spacer {
  flex: 1;
}

.main-content {
  padding: 20px;
}

.title-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.title-card h2 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 20px;
}

.meta-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.meta-info span {
  font-size: 14px;
  color: #666;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.locked {
  background: #e0e7ff;
  color: #667eea;
}

.status-badge.not_started {
  background: #fef3c7;
  color: #f59e0b;
}

.status-badge.available {
  background: #dcfce7;
  color: #22c55e;
}

.status-badge.learning {
  background: #dbeafe;
  color: #3b82f6;
}

.status-badge.completed {
  background: #dcfce7;
  color: #22c55e;
}

/* 标签页样式 */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  background: white;
  padding: 10px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.tab-btn {
  flex: 1;
  padding: 12px 8px;
  background: #f5f7fa;
  border: none;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.tab-btn:active {
  opacity: 0.8;
}

.tab-content {
  padding-bottom: 20px;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-card,
.examples-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.content-card h3,
.examples-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-section {
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.content-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 15px;
  color: #667eea;
  margin-bottom: 10px;
  font-weight: 600;
}

.section-content {
  color: #666;
  line-height: 1.8;
  font-size: 14px;
}

.section-content :deep(br) {
  margin-bottom: 5px;
}

.example-item {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
  margin-bottom: 10px;
}

.example-item:last-child {
  margin-bottom: 0;
}

.example-en {
  color: #333;
  font-size: 15px;
  margin-bottom: 5px;
}

.example-cn {
  color: #666;
  font-size: 14px;
  margin: 0;
}

/* 情景学习标签页样式 */
.scene-intro {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  padding: 15px 20px;
  border-radius: 15px;
  margin-bottom: 20px;
  text-align: center;
}

.scene-intro p {
  margin: 0;
  color: #e65100;
  font-size: 14px;
}

.scene-intro .hint {
  margin-top: 8px;
  font-size: 12px;
  opacity: 0.8;
}

.scenes-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.scene-card {
  background: white;
  border-radius: 15px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.scene-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.scene-card:active {
  transform: scale(0.98);
}

.scene-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 12px;
}

.scene-info {
  flex: 1;
}

.scene-info h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 16px;
}

.scene-info p {
  margin: 0;
  color: #666;
  font-size: 12px;
}

.scene-arrow {
  font-size: 24px;
  color: #ccc;
}

.empty-scene {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 15px;
  color: #999;
}

/* 小测验标签页样式 */
.quiz-intro {
  text-align: center;
  padding: 30px 20px;
  background: white;
  border-radius: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.quiz-intro p {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.start-quiz-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.start-quiz-btn:active {
  transform: scale(0.95);
}

.start-quiz-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lock-hint {
  margin-top: 10px;
  color: #999;
  font-size: 13px;
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
