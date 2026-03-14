<template>
  <div class="seller-login-container">
    <!-- 左侧：登录表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="header-text">
          <h2>商家管理后台</h2>
          <p class="sub-text">Welcome back, Seller. 请登录您的工作台</p>
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
              placeholder="商家账号"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <el-icon class="input-icon"><Shop /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="管理密码"
              size="large"
              class="custom-input"
              show-password
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon class="input-icon"><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleLogin"
            round
          >
            进入工作台
          </el-button>

           <div class="back-link">
             <el-button link @click="goUserLogin">
               <el-icon class="me-1"><Back /></el-icon> 返回用户登录
             </el-button>
           </div>

          <!-- 错误提示 -->
          <transition name="el-fade-in">
            <div v-if="errorMsg" class="error-tip">
              <el-icon><CircleCloseFilled /></el-icon> {{ errorMsg }}
            </div>
          </transition>
        </el-form>
      </div>
      
      <div class="footer-copy">
        Flower Shop Seller System &copy; 2026
      </div>
    </div>

    <!-- 右侧：品牌视觉区 -->
    <div class="brand-side">
      <div class="brand-content">
        <h1 class="brand-title">Craft &<br>Business</h1>
        <p class="brand-slogan">用心经营这份美丽的事业</p>
      </div>
      <div class="glow-effect"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Shop, Key, CircleCloseFilled, Back } from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()
const loginFormRef = ref(null)

const form = reactive({
  username: '',
  password: ''
})
const loading = ref(false)
const errorMsg = ref('')

const rules = {
  username: [{ required: true, message: '请输入商家账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入管理密码', trigger: 'blur' }]
}

const handleLogin = async () => {
    if (!loginFormRef.value) return;
    
    await loginFormRef.value.validate(async (valid) => {
        if (valid) {
            loading.value = true
            errorMsg.value = ''
            try {
                await store.dispatch('login', {
                    username: form.username,
                    password: form.password,
                    type: 'seller'
                })
                router.push('/seller/products')
            } catch (e) {
                errorMsg.value = '账号或密码错误，请检查权限'
            } finally {
                loading.value = false
            }
        }
    })
}

const goUserLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.seller-login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #fff;
}

/* 右侧品牌区 */
.brand-side {
  flex: 1;
  /* 选用更深沉、更有质感的绿叶或花艺工作室图片 */
  background: url('https://images.unsplash.com/photo-1463936575829-25148e1db1b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1490&q=80') no-repeat center center;
  background-size: cover;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.brand-side::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  /* 墨绿色渐变遮罩，体现商务沉稳 */
  background: linear-gradient(135deg, rgba(20, 40, 30, 0.6) 0%, rgba(10, 20, 15, 0.8) 100%);
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: left;
  padding: 0 60px;
  width: 100%;
}

.brand-title {
  font-size: 4rem;
  font-family: 'Times New Roman', serif;
  margin-bottom: 24px;
  line-height: 1.1;
  text-shadow: 0 4px 12px rgba(0,0,0,0.4);
  color: #e2e8f0; /* 偏冷的灰白色 */
}

.brand-slogan {
  font-size: 1.4rem;
  font-weight: 300;
  letter-spacing: 1.5px;
  opacity: 0.8;
  color: #cbd5e1;
}

/* 左侧表单区 */
.form-side {
  width: 500px;
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
}
.header-text h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b; /* 深岩石灰 */
  margin-bottom: 8px;
}
.sub-text {
  color: #64748b;
  font-size: 14px;
}

/* 输入框样式 - 偏冷色调 */
.custom-input :deep(.el-input__wrapper) {
  background-color: #f1f5f9;
  box-shadow: none;
  border-radius: 8px;
  padding: 12px 15px;
  transition: all 0.3s;
}
.custom-input :deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  /* 聚焦时使用深青色 */
  box-shadow: 0 0 0 1px #0f766e inset !important; 
}
.input-icon { font-size: 18px; color: #94a3b8; }

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  margin-top: 24px;
  margin-bottom: 16px;
  /* 渐变色：深青 -> 墨绿 */
  background: linear-gradient(to right, #0f766e, #115e59);
  border: none;
  border-radius: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 118, 110, 0.3);
}

.back-link {
  text-align: center;
}
.back-link .el-button {
  color: #64748b;
  font-weight: normal;
}
.back-link .el-button:hover {
  color: #0f766e;
}

.error-tip {
  margin-top: 16px;
  color: #ef4444;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  background: #fef2f2;
  padding: 8px 12px;
  border-radius: 4px;
}

.footer-copy {
  position: absolute;
  bottom: 20px;
  color: #cbd5e1;
  font-size: 12px;
}

@media (max-width: 900px) {
  .brand-side { display: none; }
  .form-side { width: 100%; }
}
</style>