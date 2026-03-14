<template>
  <div class="register-container">
    <!-- 左侧：注册表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="header-text">
          <h2>加入 Flower Life</h2>
          <p class="sub-text">创建您的账户，开启专属花艺之旅</p>
        </div>

        <el-form 
          ref="regFormRef" 
          :model="form" 
          :rules="rules" 
          class="custom-form"
          @submit.prevent
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="设置用户名"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <el-icon class="input-icon"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              placeholder="电子邮箱"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <el-icon class="input-icon"><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="设置密码 (6位以上)"
              size="large"
              class="custom-input"
              show-password
            >
              <template #prefix>
                <el-icon class="input-icon"><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="确认密码"
              size="large"
              class="custom-input"
              show-password
            >
              <template #prefix>
                <el-icon class="input-icon"><Check /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="phone">
               <el-input
              v-model="form.phone"
              placeholder="手机号码"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <el-icon class="input-icon"><Iphone /></el-icon>
              </template>
            </el-input>
          </el-form-item>

           <el-form-item prop="gender">
            <el-radio-group v-model="form.gender" class="gender-radio">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
                <el-radio label="保密">保密</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleRegister"
            round
          >
            立即注册
          </el-button>
        </el-form>

        <div class="login-link">
          已有账号？ <span @click="goToLogin">去登录</span>
        </div>
      </div>
      
      <div class="footer-copy">
        &copy; 2026 Flower Shop.
      </div>
    </div>

    <!-- 右侧：品牌视觉区 -->
    <div class="brand-side">
      <div class="brand-content">
        <h1 class="brand-title">Bloom Your<br>Dream</h1>
        <p class="brand-slogan">在花香中遇见更好的自己</p>
      </div>
      <div class="glow-effect"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Message, Check, Iphone } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const regFormRef = ref(null)

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: '',
  gender: '保密'
})
const loading = ref(false)

const validatePass2 = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '长度至少6位', trigger: 'blur' }],
  confirmPassword: [{ required: true, validator: validatePass2, trigger: 'blur' }]
}

const handleRegister = async () => {
    if (!regFormRef.value) return
    await regFormRef.value.validate(async (valid) => {
        if(valid) {
            loading.value = true
            try {
                const res = await fetch('http://localhost:5000/api/auth/register', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({
                      username: form.username,
                      email: form.email,
                      password: form.password,
                      phone: form.phone,
                      gender: form.gender
                  })
                })
                const data = await res.json()
                if(res.ok) {
                    ElMessage.success('注册成功，请登录')
                    router.push('/login')
                } else {
                    ElMessage.error(data.message || '注册失败')
                }
            } catch(e) {
                ElMessage.error('网络错误')
            } finally {
                loading.value = false
            }
        }
    })
}

const goToLogin = () => router.push('/login')
</script>

<style scoped>
.register-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #fff;
}

/* 右侧品牌区 (与登录页相反) */
.brand-side {
  flex: 1;
  /* 换一张不同的花卉图 */
  background: url('https://images.unsplash.com/photo-1507290439931-a861b5a38200?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center center;
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
  /* 稍微不同的渐变色，偏紫一点 */
  background: linear-gradient(135deg, rgba(60, 40, 80, 0.4) 0%, rgba(30, 20, 50, 0.6) 100%);
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: right; /* 文字靠右对齐更有设计感 */
  padding: 0 60px;
  width: 100%;
}

.brand-title {
  font-size: 4.5rem;
  font-family: 'Times New Roman', serif;
  margin-bottom: 20px;
  line-height: 1.1;
  text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.brand-slogan {
  font-size: 1.6rem;
  font-weight: 300;
  letter-spacing: 2px;
  opacity: 0.9;
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
  max-width: 380px;
}

.header-text {
  margin-bottom: 30px;
}
.header-text h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}
.sub-text {
  color: #999;
  font-size: 14px;
}

/* 输入框统一样式 */
.custom-input :deep(.el-input__wrapper) {
  background-color: #f7f8fa;
  box-shadow: none;
  border-radius: 8px;
  padding: 10px 15px; /* 稍微紧凑一点 */
  transition: all 0.3s;
}
.custom-input :deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  box-shadow: 0 0 0 1px #a18cd1 inset !important; /* 注册页改用紫色系高亮 */
}
.input-icon { font-size: 18px; color: #aaa; }

.gender-radio {
    margin-bottom: 15px;
    width: 100%;
    justify-content: space-around;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  margin-top: 10px;
  background: linear-gradient(to right, #a18cd1, #fbc2eb); /* 紫色系渐变 */
  border: none;
  border-radius: 24px;
}
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(161, 140, 209, 0.4);
}

.login-link {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #666;
}
.login-link span {
  color: #a18cd1;
  font-weight: bold;
  cursor: pointer;
  margin-left: 5px;
}
.login-link span:hover { text-decoration: underline; }

.footer-copy {
  position: absolute;
  bottom: 20px;
  color: #eee; /* 在白色背景上可能看不清，改成灰色 */
  color: #ddd;
  font-size: 12px;
}

@media (max-width: 900px) {
  .brand-side { display: none; }
  .form-side { width: 100%; }
}
</style>