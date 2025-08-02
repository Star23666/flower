<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <el-card class="login-card" shadow="hover">
      <h2 class="mb-4 text-center">用户登录</h2>
      <el-form @submit.prevent="login" :model="form" :rules="rules" ref="loginForm" status-icon>
        <el-form-item prop="username" required>
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            clearable
            size="large"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password" required>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            clearable
            show-password
            size="large"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            @click="login"
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
        <el-form-item>
  <el-button
    type="success"
    size="large"
    style="width:100%"
    @click="goRegister"
    plain>
    注册新账号
  </el-button>
</el-form-item>
<el-form-item>
  <el-button
    type="danger"
    size="large"
    style="width:100%"
    @click="goSellerLogin"
    plain>
    管理员登录
  </el-button>
</el-form-item>
        <el-alert v-if="error" :title="error" type="error" show-icon class="mb-2" />
      </el-form>
    </el-card>
  </div>
</template>


<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
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
  try {
    loginForm.value.validate((valid) => {
      if (!valid) {
        return
      }
    })
    await store.dispatch('login', {
      username: form.username,
      password: form.password,
      type: 'user'
    })
    router.push('/home')
  } catch (e) {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
const goRegister = () => {
  router.push('/register')
}
const goSellerLogin = () => {
  router.push('/seller/login')
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