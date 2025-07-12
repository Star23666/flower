<template>
    <el-row :gutter="40">
      <!-- 左侧：基本信息 -->
      <el-col :span="10">
        <h2>基本信息</h2>
        <el-form :model="userForm" label-width="80px" style="max-width: 400px">
          <el-form-item label="登录账号">
            <el-input v-model="userForm.username" disabled />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="userForm.realname" />
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="userForm.gender" placeholder="请选择">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="userForm.phone" />
          </el-form-item>
          <el-form-item label="登录密码">
            <el-input v-model="userForm.password" type="password" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveUserInfo">修改</el-button>
          </el-form-item>
        </el-form>
      </el-col>
  
      <!-- 右侧：收货地址 -->
      <el-col :span="14">
        <h2>收货地址</h2>
        <el-button type="success" @click="showAddDialog = true" style="margin-bottom: 10px;">+ 新增</el-button>
        <el-dialog v-model="showAddDialog" title="新增收货地址">
  <el-form :model="addForm" label-width="80px">
    <el-form-item label="姓名">
      <el-input v-model="addForm.realname" />
    </el-form-item>
    <el-form-item label="联系方式">
      <el-input v-model="addForm.phone" />
    </el-form-item>
    <el-form-item label="地址">
      <el-input v-model="addForm.address" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showAddDialog = false">取消</el-button>
    <el-button type="primary" @click="submitAddAddress">保存</el-button>
  </template>
</el-dialog>
        <el-table :data="addressList" style="width: 100%">
          <el-table-column prop="realname" label="姓名" />
          <el-table-column prop="phone" label="联系方式" />
          <el-table-column prop="address" label="地址" />
          <el-table-column label="操作" width="160">
            <template #default="scope">
              <el-button size="small" @click="editAddress(scope.row)">编辑</el-button>
              <el-dialog v-model="showEditDialog" title="编辑收货地址">
  <el-form :model="editForm" label-width="80px">
    <el-form-item label="姓名">
      <el-input v-model="editForm.realname" />
    </el-form-item>
    <el-form-item label="联系方式">
      <el-input v-model="editForm.phone" />
    </el-form-item>
    <el-form-item label="地址">
      <el-input v-model="editForm.address" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showEditDialog = false">取消</el-button>
    <el-button type="primary" @click="submitEditAddress">保存</el-button>
  </template>
</el-dialog>
              <el-button size="small" type="danger" @click="deleteAddress(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          background
          layout="prev, pager, next"
          :total="addressTotal"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
          style="margin-top: 10px;"
        />
      </el-col>
    </el-row>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage , ElMessageBox } from 'element-plus'

//地址编辑
const showEditDialog = ref(false)
const editForm = ref({
  id: null,
  realname: '',
  phone: '',
  address: ''
})

// 用户基本信息表单数据（初始为空）
const showAddDialog = ref(false) // 控制新增弹窗显示
const addForm = ref({
  realname: '',
  phone: '',
  address: ''
})

const userForm = ref({
  username: '',
  realname: '',
  gender: '',
  phone: '',
  password: ''
})

// 收货地址数据（初始为空）
const addressList = ref([])
const addressTotal = ref(0)
const pageSize = ref(2)
const currentPage = ref(1)

// 获取token
const token = localStorage.getItem('token')

function deleteAddress(row) {
  // 这里写删除逻辑，暂时可以先加提示
  // 你可以用 ElMessageBox.confirm 做二次确认
  // 下面是基本实现
  const token = localStorage.getItem('token')
  ElMessageBox.confirm('确定要删除该地址吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    const res = await fetch(`http://localhost:5000/api/user/addresses/${row.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      ElMessage.success(data.message)
      fetchUserAddresses()
    } else {
      ElMessage.error(data.message)
    }
  }).catch(() => {})
}

function editAddress(row) {
  editForm.value = { ...row } // 赋值当前行数据
  showEditDialog.value = true
}

async function submitEditAddress() {
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:5000/api/user/addresses/${editForm.value.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      realname: editForm.value.realname,
      phone: editForm.value.phone,
      address: editForm.value.address
    })
  })
  const data = await res.json()
  if (res.ok) {
    ElMessage.success(data.message)
    showEditDialog.value = false
    fetchUserAddresses()
  } else {
    ElMessage.error(data.message)
  }
}


// 获取用户基本信息
async function fetchUserProfile() {
  const res = await fetch('http://localhost:5000/api/user/profile', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const data = await res.json()
    // 根据后端字段填充
    userForm.value.username = data.username
    userForm.value.realname = data.realname
    userForm.value.gender = data.gender
    userForm.value.phone = data.phone
    // 密码一般不返回给前端，这里留空
    userForm.value.password = ''
  } else {
    ElMessage.error('获取用户信息失败')
  }
}

async function saveUserInfo() {
  const token = localStorage.getItem('token')
  // 构造要提交的数据对象
  const data = {
    username: userForm.value.username,
    realname: userForm.value.realname,
    gender: userForm.value.gender,
    phone: userForm.value.phone,
    // 只有当用户填写了新密码时才提交
    ...(userForm.value.password ? { password: userForm.value.password } : {})
  }
  // 获取当前用户ID（可从 profile API 获取或 JWT 解析，假设 userForm 里有 id 字段）
  const userId = userForm.value.id
  const res = await fetch(`http://localhost:5000/api/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  const result = await res.json()
  if (res.ok) {
    ElMessage.success('修改成功')
    // 密码框清空
    userForm.value.password = ''
    // 重新拉取用户信息，保证数据同步
    fetchUserProfile()
  } else {
    ElMessage.error(result.message || '修改失败')
  }
}


// 获取用户收货地址
async function fetchUserAddresses() {
  const res = await fetch('http://localhost:5000/api/user/addresses', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const data = await res.json()
    addressList.value = data.addresses // 假设后端返回 { addresses: [...], total: n }
    addressTotal.value = data.total
  } else {
    ElMessage.error('获取收货地址失败')
  }
}
async function submitAddAddress() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:5000/api/user/addresses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(addForm.value)
  })
  const data = await res.json()
  if (res.ok) {
    ElMessage.success(data.message)
    showAddDialog.value = false
    // 清空表单
    addForm.value = { realname: '', phone: '', address: '' }
    // 刷新地址列表
    fetchUserAddresses()
  } else {
    ElMessage.error(data.message)
  }
}
// 页面加载时自动调用
onMounted(() => {
  fetchUserProfile()
  fetchUserAddresses()
})
</script>