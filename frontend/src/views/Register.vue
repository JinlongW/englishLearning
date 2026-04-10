<template>
  <div class="register-container">
    <div class="register-card">
      <h1 class="title">创建新账号</h1>
      <p class="subtitle">开始你的英语学习之旅！</p>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="请输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="请输入密码"
            required
          />
        </div>

        <div class="form-group">
          <label for="studentName">学生姓名</label>
          <input
            type="text"
            id="studentName"
            v-model="studentName"
            placeholder="请输入学生姓名"
            required
          />
        </div>

        <div class="form-group">
          <label for="gradeLevel">年级</label>
          <select id="gradeLevel" v-model="gradeLevel" required>
            <option value="">请选择年级</option>
            <option value="1">一年级</option>
            <option value="2">二年级</option>
            <option value="3">三年级</option>
            <option value="4">四年级</option>
            <option value="5">五年级</option>
            <option value="6">六年级</option>
          </select>
        </div>

        <button type="submit" class="register-btn" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>

        <p class="login-link">
          已有账号？<router-link to="/login">立即登录</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const studentName = ref('')
const gradeLevel = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  if (!username.value || !password.value || !studentName.value || !gradeLevel.value) {
    error.value = '请填写所有必填项'
    return
  }

  // 验证用户名格式（3-20 位字母、数字或下划线）
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/
  if (!usernameRegex.test(username.value)) {
    error.value = '用户名必须是 3-20 位的字母、数字或下划线'
    return
  }

  // 验证密码长度（至少 6 位）
  if (password.value.length < 6) {
    error.value = '密码必须至少 6 位'
    return
  }

  // 验证学生姓名（2-20 个字符）
  if (studentName.value.length < 2 || studentName.value.length > 20) {
    error.value = '学生姓名必须是 2-20 个字符'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await userStore.registerAction({
      username: username.value,
      password: password.value,
      studentName: studentName.value,
      gradeLevel: parseInt(gradeLevel.value)
    })
    success.value = '注册成功！即将跳转到登录页面...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : '注册失败，请稍后重试'
    error.value = message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.title {
  text-align: center;
  color: #333;
  font-size: 28px;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.register-btn {
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #f44336;
  text-align: center;
  padding: 10px;
  background: #ffebee;
  border-radius: 8px;
}

.success {
  color: #4caf50;
  text-align: center;
  padding: 10px;
  background: #e8f5e9;
  border-radius: 8px;
}

.login-link {
  text-align: center;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
