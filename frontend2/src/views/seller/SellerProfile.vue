<template>
  <div class="seller-profile-container">
    <div class="page-header">
      <div class="header-content">
        <h2 class="page-title">账户设置</h2>
        <p class="page-desc">管理您的商家基本信息与账号安全</p>
      </div>
    </div>

    <el-row :gutter="24">
      <!-- 左侧：个人资料卡片 -->
      <el-col :xs="24" :md="10" :lg="8">
        <el-card class="profile-card" shadow="hover">
          <div class="profile-header">
            <div class="avatar-wrapper" :style="{ backgroundColor: avatarColor }">
              <span class="avatar-text">{{ avatarText }}</span>
            </div>
            <h3 class="profile-name">{{ userForm.username || '商家用户' }}</h3>
            <el-tag type="success" size="small" effect="dark" round>营业中</el-tag>
          </div>
          
          <el-divider border-style="dashed" />

          <el-form label-position="top" class="profile-form" @submit.prevent>
            <el-form-item label="商家名称 / 用户名">
              <el-input 
                v-model="userForm.username" 
                placeholder="请输入商家名称" 
                size="large"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-button 
              type="primary" 
              class="w-100 save-btn" 
              size="large"
              :loading="loading.profile"
              @click="updateUsername"
            >
              更新基本信息
            </el-button>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：安全设置卡片 -->
      <el-col :xs="24" :md="14" :lg="16">
        <el-card class="security-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Lock /></el-icon>
              <span>安全设置</span>
            </div>
          </template>

          <el-alert
            title="为了您的账号安全，建议定期更换密码。"
            type="info"
            show-icon
            :closable="false"
            class="mb-4"
          />

          <el-form 
            ref="pwdFormRef"
            :model="pwdForm" 
            :rules="pwdRules"
            label-width="120px" 
            class="security-form"
            status-icon
            @submit.prevent
          >
            <el-form-item label="当前密码" prop="old_password">
              <el-input 
                v-model="pwdForm.old_password" 
                type="password" 
                show-password 
                placeholder="请输入当前使用的密码"
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password">
              <el-input 
                v-model="pwdForm.new_password" 
                type="password" 
                show-password 
                placeholder="请输入新密码（6-20位）"
              />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input 
                v-model="pwdForm.confirm_password" 
                type="password" 
                show-password 
                placeholder="请再次输入新密码"
              />
            </el-form-item>

            <el-form-item>
              <el-button 
                type="danger" 
                @click="changePassword" 
                :loading="loading.password"
              >
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const userForm = ref({
  username: ''
})

const pwdForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const loading = reactive({
  profile: false,
  password: false
})

const pwdFormRef = ref(null)

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } else {
    if (pwdForm.value.confirm_password !== '') {
      if (pwdFormRef.value) pwdFormRef.value.validateField('confirm_password')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== pwdForm.value.new_password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const pwdRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { validator: validatePass, trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { validator: validatePass2, trigger: 'blur' }
  ]
}

// 动态头像生成
const avatarText = computed(() => {
  return userForm.value.username ? userForm.value.username.charAt(0).toUpperCase() : 'S'
})

const avatarColor = computed(() => {
  const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#9C27B0', '#3F51B5']
  let hash = 0
  const str = userForm.value.username || 'shop'
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
})

// 获取当前用户名
async function fetchProfile() {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:5000/api/seller/profile', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      userForm.value.username = data.username
    }
  } catch(e) {
    console.error('Failed to fetch profile', e)
  }
}

onMounted(() => {
  fetchProfile()
})

// 修改用户名
async function updateUsername() {
  if (!userForm.value.username.trim()) {
     ElMessage.warning('用户名不能为空')
     return
  }
  
  loading.profile = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:5000/api/seller/profile', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ username: userForm.value.username })
    })
    const data = await res.json()
    if (res.ok) {
      ElMessage.success(data.message)
    } else {
      ElMessage.error(data.message)
    }
  } catch (e) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.profile = false
  }
}

// 修改密码
function changePassword() {
  if (!pwdFormRef.value) return
  
  pwdFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.password = true
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://localhost:5000/api/seller/password', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
          body: JSON.stringify(pwdForm.value)
        })
        const data = await res.json()
        if (res.ok) {
          ElMessage.success(data.message)
          pwdForm.value.old_password = ''
          pwdForm.value.new_password = ''
          pwdForm.value.confirm_password = ''
          // 重置表单验证状态
           pwdFormRef.value.resetFields()
        } else {
          ElMessage.error(data.message)
        }
      } catch (e) {
        ElMessage.error('网络错误，请稍后重试')
      } finally {
        loading.password = false
      }
    }
  })
}
</script>

<style scoped>
.seller-profile-container {
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.page-desc {
  color: #909399;
  font-size: 14px;
  margin: 8px 0 0;
}

.profile-card {
  text-align: center;
  margin-bottom: 20px;
}

.profile-header {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  color: white;
  font-size: 40px;
  font-weight: bold;
}

.profile-name {
  font-size: 20px;
  color: #303133;
  margin: 0 0 8px;
}

.profile-form {
  text-align: left;
  padding: 0 12px;
}

.w-100 {
  width: 100%;
}

.save-btn {
  margin-top: 12px;
}

.security-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: 600;
}

.header-icon {
  margin-right: 8px;
  font-size: 18px;
}

.security-form {
  max-width: 500px;
}

.mb-4 {
  margin-bottom: 24px;
}
</style>