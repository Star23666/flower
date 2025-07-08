<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <el-card class="login-card" shadow="hover">
      <h2 class="mb-4 text-center">用户注册</h2>
      <el-form @submit.prevent="register" :model="form" :rules="rules" ref="registerForm" status-icon>
        <el-form-item label="头像" prop="avatar">
          <el-upload
  class="avatar-uploader"
  action="http://localhost:5000/api/upload/image?type=avatar"
  :show-file-list="false"
  :on-success="handleAvatarSuccess"
  :before-upload="beforeAvatarUpload"
>
  <img
    v-if="form.avatar"
    :src="form.avatar"
    class="avatar"
    style="width: 80px; height: 80px; border-radius: 50%;"
  />
<el-icon v-else style="font-size:32px;"><Plus /></el-icon>
</el-upload>
  <!-- <input type="file" /> -->
</el-form-item>
        <el-form-item prop="username" required>
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" clearable />
        </el-form-item>
        <el-form-item prop="email" required>
          <el-input v-model="form.email" placeholder="请输入邮箱" size="large" clearable />
        </el-form-item>
        <el-form-item prop="password" required>
          <el-input v-model="form.password" placeholder="请输入密码" type="password" size="large" show-password clearable />
        </el-form-item>
        <el-form-item prop="gender" required>
          <el-select v-model="form.gender" placeholder="请选择性别" size="large">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
            <el-option label="保密" value="保密" />
          </el-select>
        </el-form-item>
        <el-form-item prop="phone" required>
          <el-input v-model="form.phone" placeholder="请输入电话" size="large" clearable />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width:100%"
            :loading="loading"
            native-type="submit"
          >注册</el-button>
        </el-form-item>
        <el-alert v-if="error" :title="error" type="error" show-icon class="mb-2" />
        <el-form-item>
          <el-button
            type="default"
            size="large"
            style="width:100%"
            @click="goLogin"
            plain
          >返回登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>

</template>


<script setup>
import { Plus } from '@element-plus/icons-vue'
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
const store = useStore()
const router = useRouter()
const registerForm = ref(null)
const loading = ref(false)
const error = ref('')
const form = reactive({
  username: '',
  email: '',
  password: '',
  gender: '',
  phone: '',
  avatar:''
})
function handleAvatarSuccess(res) {
  form.avatar = 'http://localhost:5000' + res.url
}
function beforeAvatarUpload(file) {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isJPG) {
    ElMessage.error('只能上传 JPG/PNG 图片!')
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
  }
  return isJPG && isLt2M
}
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [{ required: true, message: '请输入电话', trigger: 'blur' }]
}

const register = async () => {
  error.value = ''
  loading.value = true
  registerForm.value.validate(async (valid) => {
    if (!valid) {
      loading.value = false
      return
    }
    try {
      await store.dispatch('register', { ...form })
      router.push('/login')
    } catch (e) {
      error.value = '注册失败，请检查信息'
    } finally {
      loading.value = false
    }
  })
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.avatar-uploader {
  position: relative;
}
.avatar-uploader input[type="file"] {
  opacity: 0;
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;

  top: 0;
  cursor: pointer;
  z-index: 10;
  pointer-events: auto !important;
}

.avatar {
  width: 80px;
  height: 80px;
  display: block;
  border-radius: 50%;
}
.login-card {
  width: 350px;
  padding: 32px 24px 24px 24px;
  border-radius: 16px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
  background: #fff;
}

</style>
<script>
export default {
  name: 'UserRegister'
}

</script>