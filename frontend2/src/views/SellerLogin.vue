<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <el-card class="login-card" shadow="hover">
      <h2 class="mb-4 text-center">商家登录</h2>
      <el-form @submit.prevent="login" :model="form" :rules="rules" ref="loginForm" status-icon>
        <el-form-item prop="username" required>
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
            clearable
          />
        </el-form-item>
        <el-form-item prop="password" required>
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            type="password"
            size="large"
            show-password
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width:100%"
            :loading="loading"
            native-type="submit"
          >
            登录
          </el-button>
        </el-form-item>
        <el-alert v-if="error" :title="error" type="error" show-icon class="mb-2" />
        <!-- 可选：返回用户登录按钮 -->
        <el-form-item>
          <el-button
            type="default"
            size="large"
            style="width:100%"
            @click="goUserLogin"
            plain
          >
            返回用户登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}
const form = reactive({
  username: '',
  password: ''
})
const loading = ref(false)
const error = ref('')
const loginForm = ref(null)

const login = async () => {
  error.value = ''
  loading.value = true
  loginForm.value.validate(async (valid) => {
    if (!valid) {
      loading.value = false
      return
    }
    try {
      await store.dispatch('login', {
        username: form.username,
        password: form.password,
        type: 'seller'
      })
      router.push('/seller/products')
    } catch (e) {
      error.value = '用户名或密码错误'
    } finally {
      loading.value = false
    }
  })
}

const goUserLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.login-card {
  width: 350px;
  padding: 32px 24px 24px 24px;
  border-radius: 16px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
  background: #fff;
}
</style>