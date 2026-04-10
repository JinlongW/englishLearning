<template>
  <div class="grade-unit-selector">
    <!-- 年级标签页 -->
    <div class="grade-tabs">
      <div
        v-for="grade in gradeOptions"
        :key="grade.value"
        class="grade-tab"
        :class="{ active: selectedGrade === grade.value }"
        @click="selectGrade(grade.value)"
      >
        {{ grade.label }}
      </div>
    </div>

    <!-- 学期选择 -->
    <div class="semester-tabs">
      <div
        v-for="semester in semesterOptions"
        :key="semester.value"
        class="semester-tab"
        :class="{ active: selectedSemester === semester.value }"
        @click="selectSemester(semester.value)"
      >
        {{ semester.label }}
      </div>
    </div>

    <!-- 单元网格 -->
    <div class="unit-grid">
      <div
        v-for="unit in currentUnits"
        :key="unit.id"
        class="unit-card"
        :class="[unit.status, { selected: unit.id === modelValue }]"
        @click="selectUnit(unit)"
      >
        <div class="unit-header">
          <span class="unit-title">{{ unit.label }}</span>
          <span class="unit-icon">
            <span v-if="unit.status === 'completed'">✅</span>
            <span v-else-if="unit.status === 'learning'">📖</span>
            <span v-else>⚪</span>
          </span>
        </div>
        <div class="unit-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: getProgressPercent(unit) + '%' }"
            ></div>
          </div>
          <span class="progress-text">{{ unit.learnedWordCount }}/{{ unit.wordCount }}</span>
        </div>
      </div>
    </div>

    <div v-if="currentUnits.length === 0" class="empty-state">
      <p>暂无单元数据</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getGradeUnitTree } from '@/api/grade-unit'
import type { GradeTreeNode, GradeUnitTreeNode } from '@/types/api'

const props = defineProps<{
  modelValue?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [unitId: string]
  'loaded': [unitId: string, learnedCount: number, totalCount: number]
}>()

const loading = ref(false)
const gradeTree = ref<GradeTreeNode[]>([])
const selectedGrade = ref<number>(3)
const selectedSemester = ref<string>('上')

// 年级选项（3-6 年级）
const gradeOptions = [
  { value: 3, label: '三年级' },
  { value: 4, label: '四年级' },
  { value: 5, label: '五年级' },
  { value: 6, label: '六年级' }
]

// 学期选项
const semesterOptions = [
  { value: '上', label: '上册' },
  { value: '下', label: '下册' }
]

// 当前选中的单元列表
const currentUnits = computed(() => {
  const gradeNode = gradeTree.value.find(g => g.grade === selectedGrade.value)
  if (!gradeNode) return []

  return gradeNode.units.filter(u => u.semester === selectedSemester.value)
})

// 选择年级
const selectGrade = (grade: number) => {
  selectedGrade.value = grade
}

// 选择学期
const selectSemester = (semester: string) => {
  selectedSemester.value = semester
}

// 选择单元
const selectUnit = (unit: GradeUnitTreeNode) => {
  emit('update:modelValue', unit.id)
}

// 计算进度百分比
const getProgressPercent = (unit: GradeUnitTreeNode): number => {
  if (unit.wordCount === 0) return 0
  return Math.round((unit.learnedWordCount / unit.wordCount) * 100)
}

// 加载年级单元树
const loadGradeUnitTree = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const data = await getGradeUnitTree()
    // API 拦截器已经解包了响应，data 直接就是 GradeTreeNode[]
    if (data && Array.isArray(data)) {
      gradeTree.value = data
      console.log('年级单元树加载成功:', gradeTree.value)

      // 找到当前选中的单元，通知父组件更新进度
      if (props.modelValue) {
        for (const gradeNode of gradeTree.value) {
          const unit = gradeNode.units.find(u => u.id === props.modelValue)
          if (unit) {
            emit('loaded', props.modelValue, unit.learnedWordCount, unit.wordCount)
            break
          }
        }
      }
    } else {
      console.warn('年级单元树数据格式异常:', data)
    }
  } catch (error) {
    console.error('加载年级单元树失败', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 暴露刷新方法给父组件调用
defineExpose({
  refresh: loadGradeUnitTree
})

onMounted(() => {
  loadGradeUnitTree()
})
</script>

<style scoped>
.grade-unit-selector {
  background: white;
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
}

.grade-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  overflow-x: auto;
}

.grade-tab {
  padding: 8px 16px;
  background: #f5f7fa;
  border-radius: 20px;
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s;
}

.grade-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.semester-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.semester-tab {
  flex: 1;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 10px;
  font-size: 14px;
  color: #666;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.semester-tab.active {
  background: #e0e7ff;
  color: #667eea;
  font-weight: 600;
}

.unit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.unit-card {
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s;
}

.unit-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.unit-card.completed {
  border-color: #4ade80;
  background: #f0fdf4;
}

.unit-card.learning {
  border-color: #667eea;
  background: #eef2ff;
}

.unit-card.selected {
  border-color: #667eea;
  border-width: 3px;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.unit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.unit-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.unit-icon {
  font-size: 16px;
}

.unit-progress {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.unit-card.completed .progress-fill {
  background: #4ade80;
}

.unit-card.learning .progress-fill {
  background: #667eea;
}

.progress-text {
  font-size: 11px;
  color: #999;
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #999;
}
</style>
