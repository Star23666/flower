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
          <el-menu-item index="likes">
            <el-icon><Pointer /></el-icon>
            <span>我的点赞</span>
          </el-menu-item>
        </el-menu>
    </el-col>
      <!-- 右侧：基本信息 -->
      <el-col :span="20" >
        <div class="content-panel" v-show="activeMenu === 'info'">
          <div class="panel-header">
            <h2>个人资料</h2>
            <span class="subtitle">管理您的档案以保护账号安全</span>
          </div>
          
          <div class="info-layout">
             <!-- 左侧：表单区域 -->
             <div class="info-form-wrapper">
               <el-form :model="userForm" label-position="right" label-width="100px" class="user-info-form">
                  
                  <el-form-item label="登录账号">
                    <span class="static-text">{{ userForm.username }}</span>
                     <el-button link type="primary" size="small" style="margin-left:15px;" @click="openPasswordDialog">修改密码</el-button>
                  </el-form-item>
  
                   <!-- 新增：修改密码弹窗 -->
                  <el-dialog v-model="showPasswordDialog" title="修改登录密码" width="400px" append-to-body destroy-on-close>
                    <el-form :model="passwordForm" label-width="80px">
                      <p style="margin-bottom:15px;color:#999;font-size:12px;margin-left:80px;">请设置您的新登录密码，修改后需重新登录</p>
                      <el-form-item label="新密码">
                        <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码"></el-input>
                      </el-form-item>
                      <el-form-item label="确认密码">
                        <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码"></el-input>
                      </el-form-item>
                    </el-form>
                    <template #footer>
                      <span class="dialog-footer">
                        <el-button @click="showPasswordDialog = false">取消</el-button>
                        <el-button type="primary" @click="confirmModifyPassword">确认修改</el-button>
                      </span>
                    </template>
                  </el-dialog>
                  
                  <el-form-item label="真实姓名">
                    <el-input v-model="userForm.realname" placeholder="请输入您的姓名" />
                  </el-form-item>
  
                  <el-form-item label="性 别">
                    <el-radio-group v-model="userForm.gender">
                      <el-radio label="男">先生</el-radio>
                      <el-radio label="女">女士</el-radio>
                      <el-radio label="保密">保密</el-radio>
                    </el-radio-group>
                  </el-form-item>
  
                  <el-form-item label="手机号码">
                    <el-input v-model="userForm.phone" placeholder="请输入手机号">
                       <template #append>修改</template>
                    </el-input>
                  </el-form-item>
  
                  <el-form-item label="账户余额">
                    <div class="balance-card">
                      <div class="balance-info">
                         <span class="currency-symbol">¥</span>
                         <span class="balance-num">{{ userForm.balance || '0.00' }}</span>
                      </div>
                      <el-button type="primary" size="small" round class="recharge-btn" @click="showRechargeDialog = true">立即充值</el-button>
                    </div>

                    <!-- 充值弹窗 -->
                    <el-dialog v-model="showRechargeDialog" title="账户充值" width="420px" center append-to-body destroy-on-close>
                        <div class="recharge-dialog-content">
                          <div class="input-amount-wrapper">
                            <span class="prefix">¥</span>
                            <el-input v-model.number="rechargeForm.amount" placeholder="请输入充值金额" type="number" min="1" size="large" />
                          </div>
                          
                          <div class="pay-section-title">目前只支持支付宝充值</div>
                          <div class="pay-types-grid">
                            <div 
                              v-for="type in ['微信', '支付宝', '建行', '农行']" 
                              :key="type"
                              class="pay-type-box"
                              :class="{ active: rechargeForm.payType === type }"
                              @click="rechargeForm.payType = type"
                            >
                              <span class="pay-icon" :class="type"></span>
                              {{ type }}
                            </div>
                          </div>
                        </div>
                        <template #footer>
                          <el-button @click="showRechargeDialog = false">取消</el-button>
                          <el-button type="primary" @click="confirmRecharge" :disabled="!rechargeForm.amount">确认支付</el-button>
                        </template>
                    </el-dialog>
                  </el-form-item>
                  
                  <el-form-item class="action-footer">
                    <el-button type="primary" size="large" class="save-btn" @click="saveUserInfo">保存更改</el-button>
                    <el-button type="text" style="color:#999" @click="logout">退出登录</el-button>
                  </el-form-item>
               </el-form>
             </div>
  
             <!-- 右侧：头像区域 -->
             <div class="avatar-section">
                <div class="avatar-wrapper">
                   <el-avatar :src="userForm.avatar || defaultAvatar" :size="100" shape="circle" fit="cover" />
                   <div class="avatar-mask">编辑</div>
                </div>
                <el-upload
                  class="avatar-uploader-btn"
                  action="http://localhost:5000/api/upload/image"
                  :data="{ type: 'avatar' }" 
                  :show-file-list="false"
                  accept="image/png,image/jpeg,image/gif"
                  :before-upload="beforeAvatarUpload"
                  :on-success="handleAvatarSuccess"
                  :headers="{ Authorization: `Bearer ${token}` }"
                >
                  <el-button plain size="small">选择图片</el-button>
                </el-upload>
                <div class="avatar-tips">
                  支持 jpg, png 格式<br>文件大小不超过 2MB
                </div>
             </div>
          </div>
        </div>

      <div v-show="activeMenu === 'orders'" class="orders-section">
  <h2>我的订单</h2>
  <OrderList />
</div>

      <!-- 右侧：收货地址 -->
<div class="content-panel" v-show="activeMenu === 'address'">
          <div class="panel-header">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div>
                <h2>收货地址</h2>
                <span class="subtitle">管理您的收货地址，下单更便捷</span>
              </div>
              <el-button type="primary" :icon="Plus" @click="showAddDialog = true">新增地址</el-button>
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty v-if="addressList.length === 0" description="暂无收货地址" :image-size="120"></el-empty>

          <!-- 地址列表表格 -->
          <el-table 
            v-else
            :data="addressList" 
            style="width: 100%; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);"
            :header-cell-style="{background:'#f5f7fa', color:'#606266', fontWeight:'bold'}"
          >
            <el-table-column prop="realname" label="收货人" width="140">
               <template #default="{ row }">
                  <div style="display:flex; align-items:center;">
                     <el-icon style="margin-right:5px; color:#409EFF"><User /></el-icon>
                     <span style="font-weight: 500;">{{ row.realname }}</span>
                  </div>
               </template>
            </el-table-column>
            <el-table-column prop="phone" label="联系电话" width="180">
              <template #default="{ row }">
                  <div style="display:flex; align-items:center;">
                     <el-icon style="margin-right:5px; color:#67C23A"><Iphone /></el-icon>
                     <span>{{ row.phone }}</span>
                  </div>
               </template>
            </el-table-column>
            <el-table-column prop="address" label="详细地址" show-overflow-tooltip />
            <el-table-column label="操作" width="180" align="center">
              <template #default="scope">
                <el-button link type="primary" :icon="Edit" @click="editAddress(scope.row)">编辑</el-button>
                <el-divider direction="vertical" />
                <el-button link type="danger" :icon="Delete" @click="deleteAddress(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div style="margin-top: 20px; display: flex; justify-content: flex-end;" v-if="addressList.length > 0">
            <el-pagination
              background
              layout="prev, pager, next"
              :total="addressTotal"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            />
          </div>

          <!-- 新增弹窗 -->
          <el-dialog v-model="showAddDialog" title="新增收货地址" width="500px" destroy-on-close align-center append-to-body>
              <el-form :model="addForm" label-width="90px" style="padding-right:20px;">
                  <el-form-item label="收货人">
                  <el-input v-model="addForm.realname" placeholder="请输入姓名" :prefix-icon="User" />
                  </el-form-item>
                  <el-form-item label="联系方式">
                  <el-input v-model="addForm.phone" placeholder="请输入手机号" :prefix-icon="Iphone" />
                  </el-form-item>
                  <el-form-item label="详细地址">
                  <el-input 
                      v-model="addForm.address" 
                      type="textarea" 
                      :rows="2" 
                      placeholder="请输入省/市/区/街道信息" 
                  />
                  </el-form-item>
              </el-form>
              <template #footer>
                  <span class="dialog-footer">
                  <el-button @click="showAddDialog = false">取消</el-button>
                  <el-button type="primary" @click="submitAddAddress">保存地址</el-button>
                  </span>
              </template>
          </el-dialog>

          <!-- 编辑弹窗 -->
          <el-dialog v-model="showEditDialog" title="编辑收货地址" width="500px" align-center append-to-body>
              <el-form :model="editForm" label-width="90px" style="padding-right:20px;">
                  <el-form-item label="收货人">
                  <el-input v-model="editForm.realname" :prefix-icon="User" />
                  </el-form-item>
                  <el-form-item label="联系方式">
                  <el-input v-model="editForm.phone" :prefix-icon="Iphone" />
                  </el-form-item>
                  <el-form-item label="详细地址">
                  <el-input v-model="editForm.address" type="textarea" :rows="2" />
                  </el-form-item>
              </el-form>
              <template #footer>
                  <span class="dialog-footer">
                  <el-button @click="showEditDialog = false">取消</el-button>
                  <el-button type="primary" @click="submitEditAddress">保存修改</el-button>
                  </span>
              </template>
          </el-dialog>
      </div>

      <!-- 右侧：我的收藏 -->
      <div class="content-panel" v-show="activeMenu === 'favorites'">
          <div class="panel-header">
            <h2>我的收藏</h2>
            <span class="subtitle">您关注的精选商品</span>
          </div>

          <!-- 空状态 -->
          <el-empty v-if="filteredFavorites.length === 0" description="暂无收藏商品" :image-size="120">
            <el-button type="primary" @click="$router.push('/')">去逛逛</el-button>
          </el-empty>
          
          <!-- 商品网格 -->
          <div v-else class="favorites-grid">
            <div v-for="item in filteredFavorites" :key="item.id" class="favorite-item">
              <!-- 图片区：带悬浮效果 -->
              <div class="image-wrapper" @click="$router.push(`/product/${item.id}`)">
                <img :src="getProductImage(item)" class="product-image" />
                <div class="hover-overlay">
                  <span class="view-txt">查看详情</span>
                </div>
              </div>
              
              <!-- 信息区 -->
              <div class="product-info">
                <h3 class="product-title" :title="item.name">{{ item.name }}</h3>
                <div class="product-meta">
                  <span class="product-price">¥{{ item.price }}</span>
                  <!-- 可选：显示库存状 -->
                  <span class="stock-tag" v-if="item.stock < 10 && item.stock > 0">仅剩 {{item.stock}} 件</span>
                  <span class="stock-tag out" v-else-if="item.stock == 0">已售罄</span>
                </div>
              </div>

              <!-- 操作区 -->
              <div class="action-bar">
                <el-button 
                  type="danger" 
                  plain 
                  size="small" 
                  :icon="Delete"
                  class="action-btn"
                  @click.stop="removeFavorite(item.id)"
                  :loading="loading[item.id]"
                >
                  取消收藏
                </el-button>
                <el-button 
                   type="primary" 
                   size="small" 
                   class="action-btn"
                   @click.stop="$router.push(`/product/${item.id}`)"
                >
                  购买
                </el-button>
              </div>
            </div>
          </div>
      </div>
      
        <!-- 右侧：我的点赞 -->
        <div class="content-panel" v-show="activeMenu === 'likes'">
            <div class="panel-header">
              <h2>我的点赞</h2>
              <span class="subtitle">您喜欢的精选商品</span>
            </div>

            <!-- 空状态 -->
            <el-empty v-if="likesList.length === 0" description="暂无点赞商品" :image-size="120">
              <el-button type="primary" @click="$router.push('/')">去逛逛</el-button>
            </el-empty>

            <!-- 商品网格 -->
            <div v-else class="favorites-grid">
              <div v-for="item in likesList" :key="item.id" class="favorite-item">
                <!-- 图片区：带悬浮效果 -->
                <div class="image-wrapper" @click="$router.push(`/product/${item.id}`)">
                  <img :src="getProductImage(item)" class="product-image" />
                  <div class="hover-overlay">
                    <span class="view-txt">查看详情</span>
                  </div>
                </div>

                <!-- 信息区 -->
                <div class="product-info">
                  <h3 class="product-title" :title="item.name">{{ item.name }}</h3>
                  <div class="product-meta">
                    <span class="product-price">¥{{ item.price }}</span>
                    <!-- 点赞数量 -->
                    <span class="stock-tag" style="background:#fef0f0;color:#f56c6c;border-radius:12px;padding:2px 8px;font-size:12px;">❤ {{ item.like_count || 0 }} 喜欢</span>
                  </div>
                </div>

                <!-- 操作区 -->
                <div class="action-bar">
                  <el-button
                    type="danger"
                    plain
                    size="small"
                    :icon="Delete"
                    class="action-btn"
                    @click.stop="removeLike(item.id)"
                    :loading="likeLoading[item.id]"
                  >
                    取消点赞
                  </el-button>
                  <el-button
                     type="primary"
                     size="small"
                     class="action-btn"
                     @click.stop="$router.push(`/product/${item.id}`)"
                  >
                     购买
                  </el-button>
                </div>
              </div>
            </div>
        </div>

    </el-col>
    </el-row>
  </div>

    <!-- 注册组件 -->
  <ProductRecommendation />

  </template>
  
<script setup>
import { ref, onMounted,watch,computed } from 'vue'
import { ElMessage , ElMessageBox,ElLoading } from 'element-plus'
import { Star, User, Document, Location, Pointer, Delete } from '@element-plus/icons-vue'

import OrderList from './OrderList.vue'

import { useRouter,useRoute } from 'vue-router'
import { useStore } from 'vuex'

import ProductRecommendation from '@/components/ProductRecommendation.vue'

// 退出登录
const router = useRouter()
const store = useStore()


// 添加收藏相关的响应式数据和函数：
const favorites = ref([])
const loading = ref({})

// 添加点赞相关的响应式数据和函数：
const likesList = ref([])
const likeLoading = ref({})

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



/* ================= 修改密码相关逻辑 (请添加到 script setup 中) ================= */
const showPasswordDialog = ref(false)
const passwordForm = ref({
  newPassword: '',
  confirmPassword: ''
})

function openPasswordDialog() {
  passwordForm.value.newPassword = ''
  passwordForm.value.confirmPassword = ''
  showPasswordDialog.value = true
}
async function confirmModifyPassword() {
  if (!passwordForm.value.newPassword) {
    ElMessage.warning('请输入新密码')
    return
  }

    // === 新增：密码长度校验 ===
  if (passwordForm.value.newPassword.length < 6) {
    ElMessage.warning('新密码长度不能少于 6 位')
    return
  }

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  // 复用 saveUserInfo 的接口，只传 password
  const token = localStorage.getItem('token')
  const userId = userForm.value.id
  
  if (!userId) {
     ElMessage.error('无法获取用户ID，请刷新页面重试')
     return
  }

  try {
    const res = await fetch(`http://localhost:5000/api/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ password: passwordForm.value.newPassword })
    })
    
    if (res.ok) {
       ElMessage.success('密码修改成功，请重新登录')
       showPasswordDialog.value = false
       // 登出
       logout()
    } else {
       const result = await res.json()
       ElMessage.error(result.message || '修改失败')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('无法连接服务器')
  }
}

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

  try {
    // 请求后端获取支付链接
    const res = await fetch(`http://localhost:5000/api/pay/recharge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ 
        amount: rechargeForm.value.amount 
      })
    })

    const result = await res.json()
    if (res.ok && result.pay_url) {
      // 这里的 payType 逻辑如果是支付宝才跳转
      if (rechargeForm.value.payType === '支付宝') {
         window.location.href = result.pay_url
      } else {
         ElMessage.warning('目前仅支持支付宝沙箱充值')
      }
    } else {
      ElMessage.error(result.error || '获取支付链接失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}

// 2. 修改 onMounted 方法，添加支付回调检查
onMounted(async () => {
  // 处理菜单高亮
  if (route.query.menu === 'favorites') {
    activeMenu.value = 'favorites'
  }
  
  // 检查是否是从支付宝回调回来的 (URL 中通过 query 参数携带 out_trade_no)
  const { out_trade_no } = route.query
  if (out_trade_no && out_trade_no.startsWith('R')) { // 我们的充值订单以R开头
      await verifyRecharge(out_trade_no)
      // 清除 URL 参数，避免刷新重复触发
      router.replace({ path: route.path, query: { ...route.query, out_trade_no: undefined, trade_no: undefined } })
  }
})

// 3. 新增 verifyRecharge 方法
async function verifyRecharge(out_trade_no) {
    const loading = ElLoading.service({ text: '正在确认充值结果...' })
    try {
        const res = await fetch(`http://localhost:5000/api/pay/check_recharge`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ out_trade_no })
        })
        const result = await res.json()
        if (res.ok) {
            ElMessage.success('充值到账成功！')
            // 重新获取用户信息刷新余额
            // 如果你有 getUserInfo 方法，调用它。或者直接手动更新：
            // userForm.value.balance = result.new_balance (如果后端返回了)
            // 这里我们假设页面会重新加载数据
            saveUserInfo() // 或者刷新整个页面 location.reload()
            setTimeout(() => location.reload(), 1000)
        } else {
            ElMessage.warning(result.error || '充值确认失败，请查看订单状态')
        }
    } catch(e) {
        ElMessage.error('验证支付失败')
    } finally {
        loading.close()
    }
}



// 获取token
const token = localStorage.getItem('token')

const ALLOWED_AVATAR_TYPES = ['image/jpeg', 'image/png', 'image/gif']
const ALLOWED_AVATAR_EXTS = ['jpg', 'jpeg', 'png', 'gif']
const MAX_AVATAR_SIZE_MB = 2

function beforeAvatarUpload(rawFile) {
  const mimeType = (rawFile.type || '').toLowerCase()
  const ext = (rawFile.name.split('.').pop() || '').toLowerCase()

  const validType = ALLOWED_AVATAR_TYPES.includes(mimeType) || ALLOWED_AVATAR_EXTS.includes(ext)
  if (!validType) {
    ElMessage.error('仅支持 JPG/PNG/GIF 格式图片')
    return false
  }

  const validSize = rawFile.size / 1024 / 1024 <= MAX_AVATAR_SIZE_MB
  if (!validSize) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }

  return true
}

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
console.log('Token:', token);  // 确保 token 存在
async function fetchUserProfile() {
  const res = await fetch('http://localhost:5000/api/user/profile', {
    headers: { Authorization: `Bearer ${token}` }
  });
  console.log('Response status:', res.status);  // 检查状态
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

  if (userForm.value.password && String(userForm.value.password).trim() !== '') {
    data.password = userForm.value.password
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

const fetchLikes = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:5000/api/user/likes', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include'
    })

    if (!res.ok) {
      throw new Error('获取点赞列表失败')
    }
    const data = await res.json()
    likesList.value = data.items || []
  } catch (error) {
    console.error('获取点赞列表失败:', error)
    ElMessage.error(error.message || '获取点赞信息出错')
  }
}

const removeLike = async (productId) => {
  try {
    likeLoading.value[productId] = true
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/products/${productId}/like`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (res.ok) {
      ElMessage.success('已取消点赞')
      fetchLikes()
    }
  } catch (error) {
    console.error('取消点赞失败:', error)
    ElMessage.error('取消点赞失败')
  } finally {
    likeLoading.value[productId] = false
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
  if (newVal === 'likes' || newVal === '/likes') {
    console.log('触发获取点赞列表')
    fetchLikes()
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


/* 右侧内容面板容器 */
.content-panel {
  background: #fff;
  min-height: 600px;
  padding: 30px 40px;
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 20px rgba(0,0,0,0.05); /* 轻柔阴影 */
}

/* 标题区 */
.panel-header {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 20px;
  margin-bottom: 30px;
}
.panel-header h2 {
  font-size: 20px;
  color: #333;
  margin: 0 0 8px 0;
  font-weight: 600;
}
.subtitle {
  font-size: 13px;
  color: #999;
}

/* 布局：左表单 右头像 */
.info-layout {
  display: flex;
  justify-content: space-between;
  gap: 60px;
}

.info-form-wrapper {
  flex: 1; /* 占据主要宽度 */
  max-width: 500px;
}

.user-info-form .el-form-item {
  margin-bottom: 24px;
}

.static-text {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* 余额卡片 */
.balance-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #fdfdfd;
  border: 1px solid #eee;
  padding: 10px 20px;
  border-radius: 6px;
  width: 100%;
}
.balance-info {
  display: flex;
  align-items: baseline;
  color: #ff5000; /* 淘宝橙 */
}
.currency-symbol { font-size: 14px; margin-right: 2px; }
.balance-num { font-size: 20px; font-weight: bold; }
.recharge-btn {
  background-color: #ff5000;
  border-color: #ff5000;
  font-weight: normal;
}
.recharge-btn:hover {
  background-color: #ff6a00;
  border-color: #ff6a00;
}

/* 头像区域 */
.avatar-section {
  width: 200px;
  border-left: 1px solid #f0f0f0;
  padding-left: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
}
.avatar-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 4px solid #f8f8f8; /* 外圈装饰 */
  overflow: hidden;
}
.avatar-mask {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: rgba(0,0,0,0.5);
  color: #fff;
  font-size: 12px;
  text-align: center;
  padding: 4px 0;
  opacity: 0;
  transition: opacity 0.3s;
}
.avatar-wrapper:hover .avatar-mask {
  opacity: 1;
}

.avatar-uploader-btn {
  margin-bottom: 15px;
}

.avatar-tips {
  font-size: 12px;
  color: #999;
  text-align: center;
  line-height: 1.6;
}

/* 按钮区 */
.action-footer {
  margin-top: 40px;
}
.save-btn {
  width: 140px;
  font-weight: 500;
}

/* 充值弹窗样式优化 */
.recharge-dialog-content { padding: 10px 20px; }
.input-amount-wrapper {
  display: flex;
  align-items: center;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 30px;
}
.input-amount-wrapper .prefix {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-right: 10px;
}
.input-amount-wrapper .el-input {
  font-size: 24px;
  border: none;
  box-shadow: none; /* 去掉默认边框 */
}
.input-amount-wrapper .el-input__inner {
  border: none !important;
  padding: 0;
  height: 40px;
  line-height: 40px;
  font-weight: bold;
}

.pay-section-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}
.pay-types-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}
.pay-type-box {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  color: #333;
}
.pay-type-box:hover {
  border-color: #409eff;
  color: #409eff;
}
.pay-type-box.active {
  border-color: #409eff;
  background-color: #ecf5ff;
  color: #409eff;
  font-weight: bold;
}
</style>