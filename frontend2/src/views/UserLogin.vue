<template>
  <div class="login-container">
    <!-- 左侧：品牌视觉区 -->
    <div class="brand-side">
      <div class="brand-content">
        <h1 class="brand-title">Flower Life</h1>
        <p class="brand-slogan">每一朵花，都是写给生活的散文诗</p>
      </div>
      <!-- 装饰性光晕 -->
      <div class="glow-effect"></div>
    </div>

    <!-- 右侧：登录表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="header-text">
          <h2>欢迎回来</h2>
          <p class="sub-text">登录您的账号，继续探索美好花艺</p>
        </div>

        <el-form 
          ref="loginFormRef" 
          :model="form" 
          :rules="rules" 
          class="custom-form"
          @submit.prevent
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名 / 手机号"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <el-icon class="input-icon"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              size="large"
              class="custom-input"
              show-password
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon class="input-icon"><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <div class="remember-line">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <span class="forgot-pwd">忘记密码?</span>
          </div>

          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleLogin"
            round
          >
            立即登录
          </el-button>

          <!-- 错误提示 -->
          <transition name="el-fade-in">
            <div v-if="errorMsg" class="error-tip">
              <el-icon><Warning /></el-icon> {{ errorMsg }}
            </div>
          </transition>
        </el-form>

        <div class="divider">
          <span>或者</span>
        </div>

        <div class="other-actions">
          <el-button  class="action-btn" @click="goToRegister">注册新账号</el-button>
          <el-button  class="action-btn" @click="goToSeller" plain>商家入口</el-button>
        </div>
      </div>
      
      <div class="footer-copy">
        &copy; 2026 Flower Shop. All Rights Reserved.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { User, Lock, Warning } from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()
const loginFormRef = ref(null)

const form = reactive({
  username: '',
  password: ''
})
const rememberMe = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      errorMsg.value = ''
      try {
        await store.dispatch('login', {
          username: form.username,
          password: form.password,
          type: 'user'
        })
        router.push('/')
      } catch (e) {
        errorMsg.value = '用户名或密码错误，请重试'
      } finally {
        loading.value = false
      }
    }
  })
}

const goToRegister = () => router.push('/register')
const goToSeller = () => router.push('/seller/login')
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #fff;
}

/* 左侧品牌区 */
.brand-side {
  flex: 1;
  background: url('https://images.unsplash.com/photo-1490750967868-58cb7506aed6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center center;
  background-size: cover;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

/* 遮罩层，让文字更清晰 */
.brand-side::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(80, 50, 70, 0.4) 0%, rgba(20, 10, 30, 0.6) 100%);
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 0 40px;
}

.brand-title {
  font-size: 4rem;
  font-family: 'Times New Roman', serif;
  margin-bottom: 20px;
  letter-spacing: 2px;
  text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.brand-slogan {
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 1px;
  opacity: 0.9;
}

/* 右侧表单区 */
.form-side {
  width: 500px; /* 固定宽度，或者用 flex: 0 0 40% */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  position: relative;
  background: #fff;
}

.form-wrapper {
  width: 100%;
  max-width: 360px;
}

.header-text {
  margin-bottom: 40px;
  text-align: left;
}
.header-text h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}
.sub-text {
  color: #999;
  font-size: 14px;
}

/* 自定义 Input 样式覆盖 */
.custom-input :deep(.el-input__wrapper) {
  background-color: #f7f8fa;
  box-shadow: none; /* 去掉默认边框 */
  border-radius: 8px;
  padding: 12px 15px;
  transition: all 0.3s;
}
.custom-input :deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  box-shadow: 0 0 0 1px #ff758c inset !important; /* 聚焦时的粉色边框 */
}
.input-icon {
  font-size: 18px;
  color: #aaa;
}

.remember-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 14px;
}
.forgot-pwd {
  color: #ff758c;
  cursor: pointer;
}
.forgot-pwd:hover {
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  letter-spacing: 1px;
  background: linear-gradient(to right, #ff758c, #ff7eb3);
  border: none;
  border-radius: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(255, 117, 140, 0.4);
}

.error-tip {
  margin-top: 12px;
  color: #f56c6c;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.divider {
  margin: 30px 0;
  text-align: center;
  position: relative;
}
.divider::before {
  content: '';
  position: absolute;
  left: 0; top: 50%;
  width: 100%; height: 1px;
  background: #eee;
  z-index: 0;
}
.divider span {
  position: relative;
  z-index: 1;
  background: #fff;
  padding: 0 12px;
  color: #bbb;
  font-size: 12px;
}

.other-actions {
  display: flex;
  gap: 12px;
}
.action-btn {
  flex: 1;
  border-radius: 20px;
}

.footer-copy {
  position: absolute;
  bottom: 20px;
  color: #ccc;
  font-size: 12px;
}

/* 响应式适配 */
@media (max-width: 900px) {
  .brand-side {
    display: none; /* 手机端隐藏左侧大图 */
  }
  .form-side {
    width: 100%;
  }
}
</style>