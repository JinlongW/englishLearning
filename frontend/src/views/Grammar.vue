<template>
  <div class="grammar-container">
    <header class="header">
      <h1>学语法</h1>
      <p>循序渐进，掌握语法规则</p>
    </header>

    <main class="main-content">
      <!-- 视图切换 -->
      <div class="view-switcher">
        <button
          :class="['switch-btn', { active: viewMode === 'list' }]"
          @click="viewMode = 'list'"
        >
          列表视图
        </button>
        <button
          :class="['switch-btn', { active: viewMode === 'tree' }]"
          @click="viewMode = 'tree'"
        >
          知识图谱
        </button>
      </div>

      <!-- 知识图谱视图 -->
      <div v-if="viewMode === 'tree'" class="tree-view-container">
        <div class="info-card">
          <p>知识图谱功能已移至独立页面</p>
          <button class="goto-tree-btn" @click="goToTree">
            打开语法知识图谱 →
          </button>
        </div>
      </div>

      <!-- 课程列表视图（原有内容） -->
      <div v-else>
        <!-- 年级单元选择器 -->
        <GradeUnitSelector v-model="selectedUnitId" @update:modelValue="onUnitChange" />

        <!-- 课程列表 -->
        <div class="lesson-list" v-if="lessons.length > 0">
          <div
            v-for="lesson in lessons"
            :key="lesson.id"
            class="lesson-card"
            :class="lesson.status"
            @click="selectLesson(lesson)"
          >
            <div class="lesson-icon">
              <span v-if="lesson.status === 'completed'">✅</span>
              <span v-else-if="lesson.status === 'learning'">📖</span>
              <span v-else>🔒</span>
            </div>
            <div class="lesson-info">
              <h3>{{ lesson.title }}</h3>
              <p>{{ lesson.description }}</p>
              <div class="lesson-meta">
                <span>⏱️ {{ lesson.duration }}分钟</span>
                <span v-if="lesson.score">得分：{{ lesson.score }}</span>
              </div>
            </div>
            <div class="lesson-arrow">›</div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>暂无语法课程</p>
        </div>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getGrammars } from '@/api/grammar'
import type { GrammarDto } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'
import GradeUnitSelector from '@/components/GradeUnitSelector.vue'

const router = useRouter()

const viewMode = ref<'list' | 'tree'>('list')
const lessons = ref<GrammarDto[]>([])
const loading = ref(false)
const selectedUnitId = ref<string>('')

// 跳转到知识图谱页面
const goToTree = () => {
  router.push('/grammar/tree')
}

// 处理单元切换
const onUnitChange = (unitId: string) => {
  selectedUnitId.value = unitId
  loadGrammars()
}

const selectLesson = async (lesson: GrammarDto) => {
  // 只有 locked 状态不能学习，其他状态都可以进入
  if (lesson.status === 'locked') {
    uni.showToast({
      title: '请先完成前面的课程',
      icon: 'none'
    })
    return
  }
  // 跳转到课程详情页面
  router.push(`/grammar/${lesson.id}`)
}

const loadGrammars = async () => {
  if (loading.value) return
  if (!selectedUnitId.value) {
    console.log('未选择单元，跳过加载')
    return
  }

  loading.value = true
  try {
    // 使用选择的单元 ID
    const response = await getGrammars(selectedUnitId.value)
    lessons.value = response || []
  } catch (error) {
    console.error('加载语法课程失败', error)
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

onMounted(() => {
  loadGrammars()
})
</script>

<style scoped>
.grammar-container {
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
  margin-bottom: 5px;
}

.header p {
  opacity: 0.9;
  font-size: 14px;
}

.main-content {
  padding: 20px;
}

/* 视图切换器 */
.view-switcher {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.switch-btn {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: white;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.switch-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

/* 知识图谱容器 */
.tree-view-container {
  margin-top: 20px;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 30px 20px;
  text-align: center;
}

.info-card p {
  color: #666;
  margin-bottom: 20px;
}

.goto-tree-btn {
  padding: 12px 24px;
  border-radius: 25px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.goto-tree-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.lesson-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.lesson-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.lesson-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.lesson-card.locked {
  opacity: 0.6;
}

.lesson-icon {
  font-size: 36px;
}

.lesson-info {
  flex: 1;
}

.lesson-info h3 {
  color: #333;
  margin-bottom: 5px;
}

.lesson-info p {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.lesson-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
}

.lesson-arrow {
  font-size: 24px;
  color: #ccc;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 15px;
}
</style>
