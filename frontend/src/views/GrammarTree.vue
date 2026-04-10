<template>
  <div class="grammar-tree-container">
    <header class="header">
      <h1>语法知识图谱</h1>
      <p>树状结构，循序渐进</p>
    </header>

    <main class="main-content">
      <!-- 年级选择器 -->
      <div class="grade-selector">
        <label>选择年级：</label>
        <picker
          :range="gradeOptions"
          range-key="label"
          :value="gradeIndex"
          @change="onGradeChange"
        >
          <div class="picker-value">
            {{ gradeOptions[gradeIndex].label }}
            <span class="arrow">›</span>
          </div>
        </picker>
      </div>

      <!-- 分类筛选 -->
      <div class="category-filter">
        <button
          :class="['filter-btn', { active: selectedCategory === 'all' }]"
          @click="selectedCategory = 'all'"
        >
          全部
        </button>
        <button
          v-for="cat in categories"
          :key="cat.value"
          :class="['filter-btn', { active: selectedCategory === cat.value }]"
          @click="selectedCategory = cat.value"
        >
          {{ cat.label }}
        </button>
      </div>

      <!-- 知识树 -->
      <div v-if="loading" class="loading">
        <text>加载中...</text>
      </div>

      <div v-else-if="filteredTree.length === 0" class="empty-state">
        <text>暂无数据</text>
      </div>

      <div v-else class="tree-container">
        <template v-for="node in filteredTree" :key="node.id">
          <tree-node :node="node" @click-node="handleNodeClick" />
        </template>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getGrammarTree } from '@/api/grammar'
import type { GrammarTreeNode } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'
import TreeNode from '@/components/GrammarTreeNode.vue'

const router = useRouter()

// 年级选项
const gradeOptions = [
  { value: 3, label: '三年级' },
  { value: 4, label: '四年级' },
  { value: 5, label: '五年级' },
  { value: 6, label: '六年级' }
]
const gradeIndex = ref(0)

// 分类选项
const categories = [
  { value: 'tense', label: '时态' },
  { value: 'voice', label: '语态' },
  { value: 'clause', label: '从句' },
  { value: 'word', label: '词汇' },
  { value: 'sentence', label: '句型' }
]

const selectedCategory = ref('all')
const treeData = ref<GrammarTreeNode[]>([])
const loading = ref(false)

// 根据分类筛选树节点
const filteredTree = computed(() => {
  if (selectedCategory.value === 'all') {
    return treeData.value
  }
  return filterByCategory(treeData.value, selectedCategory.value)
})

// 递归筛选树节点
const filterByCategory = (nodes: GrammarTreeNode[], category: string): GrammarTreeNode[] => {
  const result: GrammarTreeNode[] = []
  for (const node of nodes) {
    if (node.category === category) {
      result.push(node)
    } else if (node.children.length > 0) {
      const filteredChildren = filterByCategory(node.children, category)
      if (filteredChildren.length > 0) {
        result.push({ ...node, children: filteredChildren })
      }
    }
  }
  return result
}

// 年级选择
const onGradeChange = (event: any) => {
  gradeIndex.value = event.detail.value
  loadTree()
}

// 加载知识树
const loadTree = async () => {
  loading.value = true
  try {
    const response = await getGrammarTree(gradeOptions[gradeIndex.value].value)
    treeData.value = response.data || []
  } catch (error) {
    console.error('加载语法树失败', error)
    uni.showToast({
      title: '加载失败，请稍后重试',
      icon: 'none',
      duration: 2000
    })
  } finally {
    loading.value = false
  }
}

// 处理节点点击
const handleNodeClick = (node: GrammarTreeNode) => {
  if (node.status === 'locked') {
    uni.showToast({
      title: '请先完成前置课程',
      icon: 'none'
    })
    return
  }
  // 跳转到语法详情页面
  router.push(`/grammar/${node.id}`)
}

onMounted(() => {
  loadTree()
})
</script>

<style scoped>
.grammar-tree-container {
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

.grade-selector {
  background: white;
  border-radius: 12px;
  padding: 15px 20px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.grade-selector label {
  color: #666;
  font-size: 14px;
}

.picker-value {
  color: #333;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.picker-value .arrow {
  color: #999;
}

.category-filter {
  background: white;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-btn {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  background: white;
  color: #666;
  font-size: 13px;
  transition: all 0.2s;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.loading,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 15px;
  color: #999;
}

.tree-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
