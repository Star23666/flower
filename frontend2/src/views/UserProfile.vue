<template>
  <div class="user-profile">
  
    <el-row :gutter="40">
    <!-- 左侧：导航栏 -->
    <el-col :span="4">
        <el-menu 
          class="user-menu"
          :default-active="activeMenu" 
          @select="handleMenuSelect"
        >
        <el-menu-item index="info">
            <el-icon><User /></el-icon>
            <span>基本信息</span>
          </el-menu-item>
          <el-menu-item index="orders">
            <el-icon><Document /></el-icon>
            <span>我的订单</span>
          </el-menu-item>
          <el-menu-item index="address">
            <el-icon><Location /></el-icon>
            <span>我的地址</span>
          </el-menu-item>
          <el-menu-item index="favorites">
            <el-icon><Star /></el-icon>
            <span>我的收藏</span>
          </el-menu-item>
        </el-menu>
    </el-col>
      <!-- 右侧：基本信息 -->
      <el-col :span="20" >
        <div v-show="activeMenu === 'info'">
        <h2>基本信息</h2>
        <el-form :model="userForm" label-width="80px" style="max-width: 400px">
          <el-form-item label="头像">
  <div style="display:flex;align-items:center;">
    <el-avatar
      :src="userForm.avatar || defaultAvatar"
      :size="80"
      style="margin-right: 20px; border:1px solid #eee;"
    />
    <el-upload
      action="http://localhost:5000/api/upload/image"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :headers="{ Authorization: `Bearer ${token}` }"
    >
      <el-button type="primary">更换头像</el-button>
    </el-upload>
  </div>
</el-form-item>
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
          <el-form-item label="余额">
            <el-input v-model="userForm.balance" disabled style="width: 120px; margin-right: 10px;" />
            <el-button type="primary" @click="showRechargeDialog = true">充值</el-button>
            <el-dialog v-model="showRechargeDialog" title="用户充值" width="500px">
  <el-form :model="rechargeForm" label-width="80px">
    <el-form-item label="充值金额">
      <el-input v-model.number="rechargeForm.amount" type="number" min="1" />
    </el-form-item>
    <el-form-item label="支付方式">
      <el-radio-group v-model="rechargeForm.payType">
        <el-radio label="微信">微信支付</el-radio>
        <el-radio label="支付宝">支付宝</el-radio>
        <el-radio label="建行">中国建设银行</el-radio>
        <el-radio label="农行">中国农业银行</el-radio>
        <el-radio label="中行">中国银行</el-radio>
        <el-radio label="交行">交通银行</el-radio>
      </el-radio-group>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showRechargeDialog = false">取消</el-button>
    <el-button type="primary" @click="confirmRecharge">确认充值</el-button>
  </template>
        </el-dialog>

          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveUserInfo">修改</el-button>
            <el-button type="danger" @click="logout">退出登录</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-show="activeMenu === 'orders'" class="orders-section">
  <h2>我的订单</h2>
  <OrderList />
</div>

      <!-- 右侧：收货地址 -->
        <div v-show="activeMenu=== 'address'">
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
      </div>

<!-- 我的收藏 -->
<div v-show="activeMenu === 'favorites'" class="favorites-section">
  <h2>我的收藏</h2>

  <el-empty v-if="favorites.length === 0" description="暂无收藏商品" />
  
  <div v-else class="favorites-grid">
  <div v-for="item in filteredFavorites" :key="item.id" class="favorite-item">
    <router-link
      :to="{ path: `/product/${item.id}`, 
        query: { from: 'favorites' } }"
      class="product-link"
      style="display:block;
      text-decoration:none;
      color:inherit"
    >
      <img :src="getProductImage(item)" class="product-image" />
      <div class="product-info">
        <h3>{{ item.name }}</h3>
        <div class="product-price">¥{{ item.price }}</div>
      </div>
    </router-link>
    <div class="product-actions">
      <el-button 
        type="danger" 
        size="small" 
        @click.stop="removeFavorite(item.id)"
        :loading="loading[item.id]"
      >
        <el-icon><StarFilled /></el-icon>
        取消收藏
      </el-button>
    </div>
  </div>
</div>
</div>
      
    </el-col>
    </el-row>
  </div>
  </template>
  
<script setup>
import { ref, onMounted,watch,computed } from 'vue'
import { ElMessage , ElMessageBox } from 'element-plus'
import { Star, User, Document, Location } from '@element-plus/icons-vue'
import { StarFilled } from '@element-plus/icons-vue'

import OrderList from './OrderList.vue'

import { useRouter,useRoute } from 'vue-router'
import { useStore } from 'vuex'

// 退出登录

const router = useRouter()
const store = useStore()


// 添加收藏相关的响应式数据和函数：
const favorites = ref([])
const loading = ref({})

const activeMenu = ref('info') // 默认选中“基本信息”标签
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
  id:'',
  avatar:'',
  username: '',
  realname: '',
  gender: '',
  phone: '',
  password: '',
  balance: ''

})

// 收货地址数据（初始为空）
const addressList = ref([])
const addressTotal = ref(0)
const pageSize = ref(10)
const currentPage = ref(1)


const route = useRoute()


const showRechargeDialog = ref(false)
const rechargeForm = ref({
  amount: 0,
  payType: '微信'
})

// 监听路由的 query：
onMounted(() => {
  if (route.query.menu === 'favorites') {
    activeMenu.value = 'favorites'
  }
})

//菜单栏绑定事件
function handleMenuSelect(index) {
  activeMenu.value = index
}

async function confirmRecharge() {
  if (!rechargeForm.value.amount || rechargeForm.value.amount <= 0) {
    ElMessage.error('请输入有效的充值金额')
    return
  }
  // 用数值加法，防止字符串拼接
  userForm.value.balance = Number(userForm.value.balance) + Number(rechargeForm.value.amount)

  // 同步到后端
  const userId = userForm.value.id
  const res = await fetch(`http://localhost:5000/api/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ balance: userForm.value.balance })
  })
  const result = await res.json()
  if (res.ok) {
    ElMessage.success('充值成功！')
    showRechargeDialog.value = false
    rechargeForm.value.amount = 0
    rechargeForm.value.payType = '微信'
  } else {
    ElMessage.error(result.message || '充值失败')
  }
}



// 获取token
const token = localStorage.getItem('token')

const defaultAvatar = 'http://localhost:5000/static/uploads/avatars/default-avatar.jpg'
function handleAvatarSuccess(response) {
  userForm.value.avatar = 'http://localhost:5000' + response.url
  ElMessage.success('头像上传成功')
}

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
    userForm.value.id = data.id // 关键：一定要赋值id
    userForm.value.username = data.username
    userForm.value.realname = data.realname
    userForm.value.gender = data.gender
    userForm.value.phone = data.phone
    userForm.value.avatar = data.avatar // 头像
    userForm.value.password = ''
    userForm.value.balance = data.balance

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
    avatar: userForm.value.avatar,
    password: userForm.value.password,
    id:userForm.value.id,
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
const fetchFavorites = async () => {
  
  try {
    
    console.log('开始获取收藏列表...')
    const token = localStorage.getItem('token')
    console.log('Token:', token)  // 检查token是否存在

    const res = await fetch('http://localhost:5000/api/favorites', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include'
    })
    
    if (!res.ok) {
      const error = await res.json().catch(() => ({}))
      throw new Error(error.message || '获取收藏列表失败')
    }
    const data = await res.json()
    console.log('收藏接口返回数据:', data)
    console.log('data.items:', data.items) //
    favorites.value = (data.items || []).filter(Boolean)
    console.log('filteredFavorites:', filteredFavorites.value)

  } catch (error) {
    console.error('获取收藏列表失败:', error)
    ElMessage.error('获取收藏列表失败')
    
  }
}

const removeFavorite = async (productId) => {
  try {
    loading.value[productId] = true
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/favorites/${productId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (res.ok) {
      ElMessage.success('已取消收藏')
      fetchFavorites()
    }
  } catch (error) {
    console.error('取消收藏失败:', error)
    ElMessage.error('取消收藏失败')
  } finally {
    loading.value[productId] = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  // 如果你需要根据页码重新获取数据，可以在这里调用相应的方法
  // 例如：fetchAddresses()
}


const filteredFavorites = computed(() => (favorites.value || []).filter(Boolean))

const getProductImage = (product) => {
  if (!product || !product.image_url) {
    // 返回一个默认图片
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZWVlZWVlIi8+CiAgPHRleHQgeD0iNTAlIiB5PSI1JSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5OTk5Ij5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+'
  }
  if (product.image_url.startsWith('http')) {
    return product.image_url
  }
  return `http://localhost:5000${product.image_url}`
}

// 退出登录
function logout() {
  store.commit('setUser', null)
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

watch(activeMenu, (newVal) => {
  console.log('activeMenu 变化:', newVal)
  if (newVal === 'favorites' || newVal === '/favorites') {
    console.log('触发获取收藏列表')
    fetchFavorites()
  }
})

// 页面加载时自动调用
onMounted(() => {
  fetchUserProfile()
  fetchUserAddresses()
})
</script>

<style scoped>
.profile-sidebar {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-right: 20px;
  height: fit-content;
}
.sidebar-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
  padding-left: 10px;
}
.profile-menu {
  border-right: none;
}
.user-profile {
  padding: 20px;
}
.user-menu {
  border-right: none;
}

.favorites-section {
  padding: 20px;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.favorite-item {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.favorite-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.product-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-info {
  padding: 15px;
}

.product-info h3 {
  margin: 0 0 10px;
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

.product-actions {
  padding: 0 15px 15px;
  display: flex;
  gap: 10px;
}

.product-actions .el-button {
  flex: 1;
}

.orders-section {
  width: 100%;
  box-sizing: border-box;
  padding: 16px 0;
}

.orders-section .el-table .el-table__cell {
  padding: 12px 8px !important;
  font-size: 15px;
}
.orders-section .el-table__row {
  height: 48px;
}

.el-form-item .el-button {
  margin-right: 16px;
  min-width: 100px;
  font-size: 16px;
  border-radius: 8px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.08);
  transition: box-shadow 0.2s;
}
.el-form-item .el-button:last-child {
  margin-right: 0;
}
.el-form-item .el-button:hover {
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.18);
}


</style>