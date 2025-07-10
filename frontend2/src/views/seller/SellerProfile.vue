<template>
  <el-card>
    <h2>商家个人中心</h2>
    <el-divider />
    <!-- 修改用户名 -->
    <el-form :model="userForm" label-width="120px" style="max-width: 400px;">
      <el-form-item label="用户名">
        <el-input v-model="userForm.username" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="updateUsername">保存用户名</el-button>
      </el-form-item>
    </el-form>

    <el-divider />
    <!-- 修改密码 -->
    <el-form :model="pwdForm" label-width="120px" style="max-width: 400px;">
      <el-form-item label="旧密码">
        <el-input v-model="pwdForm.old_password" type="password" show-password />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="pwdForm.new_password" type="password" show-password />
      </el-form-item>
      <el-form-item label="确认新密码" min-length="6" max-length="20" >
        <el-input v-model="pwdForm.confirm_password" type="password" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="changePassword">修改密码</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>

import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const userForm = ref({
  username: '' // 初始化时可通过接口获取
})

const pwdForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 获取当前用户名（可选，首次进入页面时调用）
async function fetchProfile() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:5000/api/seller/profile', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const data = await res.json()
    userForm.value.username = data.username
  }
}
fetchProfile()

// 修改用户名
async function updateUsername() {
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
}

// 修改密码
async function changePassword() {
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
  } else {
    ElMessage.error(data.message)
  }
}
</script>