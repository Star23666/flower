<template>
  <!-- 面包屑导航 -->

    <div class="container py-4">
      <div v-if="product" class="row">
        <!-- 左侧图片，可用轮播 -->
        <AppBreadcrumbs />
        <div class="col-md-6 text-center">
          <img :src="getProductImage(product)" 
          class="img-fluid rounded shadow-sm" 
          style="max-height:420px;">
          
        </div>
        <!-- 右侧详情 -->
        <!-- 右侧详情 -->
        <div class="col-md-6 product-info-col">
          <div class="info-header">
            <h2 class="product-title">{{ product.name }}</h2>
            <el-button 
              :type="isFavorited ? 'danger' : 'default'" 
              :icon="isFavorited ? 'StarFilled' : 'Star'" 
              circle
              size="large"
              class="fav-btn"
              @click="toggleFavorite"
              :title="isFavorited ? '取消收藏' : '收藏商品'"
            ></el-button>
          </div>
          
          <div class="price-tag">
            <span class="currency">¥</span>
            <span class="amount">{{ product.price }}</span>
          </div>

          <!-- 新的美化参数区域 -->
          <div class="specs-box">
            <div class="spec-item">
              <span class="label">鲜花类型</span>
              <span class="value">
                <el-tag effect="light" type="danger" round size="small">
                   {{ getCategoryName(product.category_id) }}
                </el-tag>
              </span>
            </div>
            <div class="spec-item">
              <span class="label">适用对象</span>
              <span class="value">{{ product.target || '通用' }}</span>
            </div>

            
            <!-- <div class="spec-item full-width">
              <span class="label">鲜花花语</span>
              <span class="value text-highlight">{{ product.flower_language2 || '暂无花语' }}</span>
            </div> -->
            <div class="spec-item">
              <span class="label">适用场景</span>
              <span class="value">{{ product.scene || '通用' }}</span>
            </div>

                        <div class="spec-item full-width" v-if="product.description">
              <span class="label">商品描述</span>
              <span class="value text-desc">{{ product.description }}</span>
            </div>

            <!-- <div class="spec-item">
              <span class="label">原产地</span>
              <span class="value">{{ product.origin || '未知' }}</span>
            </div> -->
          </div>

          <!-- 操作区 (保持原有功能，美化样式) -->
          <div class="action-area">
            <el-input-number v-model="quantity" :min="1" :max="product.stock" class="qty-input" />
            <el-button type="primary" size="large" class="action-btn cart-btn" @click="addToCart" round>
              加入购物车
            </el-button>
            <el-button type="warning" size="large" class="action-btn buy-btn" @click="handleBuyNow" round>
              立即购买
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 下面可以加选项卡、评论等 -->
      <div v-else>加载中...</div>
      <!-- 点赞 -->
<div class="like-btn-wrapper">
  <el-button
    :type="isLiked ? 'success' : 'info'"
    @click="likeProduct"
    class="like-btn"
    circle
  >
  👍
  </el-button>
  <div class="like-count">{{ likeCount }} 赞</div>
</div>
<!-- 评论区 -->
 <!-- 评论区 -->
<div class="comments-section mt-4">
  <h5>商品评论</h5>
  <div v-if="comments.length === 0" class="text-muted mb-2">暂无评论，快来抢沙发吧！</div>
  <ul class="comment-list mb-3">
  <li v-for="c in comments" :key="c.id" class="comment-item">
    <div class="comment-header">
      <el-avatar
  :size="36"
  :src="c.avatar"
  :style="{ marginRight: '12px', boxShadow: '0 2px 8px #e0e0e0' }"
>
  {{ c.username?.charAt(0).toUpperCase() || 'U' }}
</el-avatar>
      <span class="username">{{ c.username }}</span>
    </div>
    <div class="comment-content">{{ c.content }}</div>
    <!-- 后端返回 ISO 格式时间字符串
        前端用 dayjs 格式化显示 -->
    <div class="comment-time">
      {{ dayjs.utc(c.created_at).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm') }}
</div>
  </li>
</ul>
  <div class="comment-form d-flex">
    <el-input
      v-model="newComment"
      placeholder="写下你的评论..."
      class="me-2"
      style="flex:1"
      size="large"
      :rows="2"
      type="textarea"
    />
    <el-button type="primary" @click="submitComment" :disabled="!newComment.trim()">发送</el-button>
  </div>
</div>
    </div>

        <!-- 商品推荐组件 -->
<ProductRecommendation />
  </template>
  
<script setup>
  /* eslint-disable no-unused-vars */
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import AppBreadcrumbs from '@/components/AppBreadcrumbs.vue'
import ProductRecommendation from '@/components/ProductRecommendation.vue'
dayjs.extend(utc)
dayjs.extend(timezone)

const store = useStore()
const route = useRoute()
const router = useRouter()

const product = ref({})
const categories = ref([])
const quantity = ref(1)

// 状态标识
const isFavorited = ref(false)
const isLiked = ref(false)
const likeCount = ref(0)

// 评论相关
const comments = ref([])
const newComment = ref('')

// --- 核心数据获取 ---

// 初始化加载
onMounted(async () => {
  const id = route.params.id
  if(id) {
    await fetchCategories()
    await fetchProduct(id)
    fetchComments(id)
    
    // 如果用户已登录，获取个性化状态
    if (store.state.user || localStorage.getItem('token')) {
      checkFavoriteStatus(id)
      checkLikeStatus(id)
    }
  }
})

// 监听路由变化（防止同一组件内跳转不刷新）
watch(() => route.params.id, (newId) => {
  if(newId) {
    product.value = {}
    fetchProduct(newId)
    // ...重新获取其他状态
  }
})

const fetchProduct = async (id) => {
  try {
    const res = await fetch(`http://localhost:5000/api/products/${id}`)
    if(res.ok){
      product.value = await res.json()
      // 如果后端有点赞数，初始化它
      if(product.value.like_count) likeCount.value = product.value.like_count
    }
  } catch(e) { console.error(e) }
}

const fetchCategories = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/categories')
    if(res.ok) categories.value = await res.json()
  } catch(e) { console.error(e) }
}

const fetchComments = async (pid) => {
  try {
    const id = pid || product.value.id
    const res = await fetch(`http://localhost:5000/api/products/${id}/comments`)
    if(res.ok) comments.value = await res.json()
  } catch(e) { console.error(e) }
}

// --- 交互逻辑 ---

const getCategoryName = (cid) => {
  // 1. 如果分类数据还没取回来，显示加载中
  if (!categories.value || categories.value.length === 0) return '加载中...'
  
  // 2. 如果商品详情里没有 valid 的 category_id
  if (!cid) return '暂无'

  // 3. 核心修复：使用 String() 强制转换两边为字符串再比较，避免 1 !== "1" 的问题
  const cat = categories.value.find(c => String(c.id) === String(cid))
  
  return cat ? cat.name : '暂无'
}

const getProductImage = (p) => {
  if (!p || !p.image_url) return 'https://via.placeholder.com/400x400?text=No+Image'
  if (p.image_url.startsWith('http')) return p.image_url
  return `http://localhost:5000${p.image_url}`
}

// 加入购物车
const addToCart = () => {
  if (!checkLogin()) return
  if (quantity.value > product.value.stock) {
    ElMessage.warning('库存不足')
    return
  }
  store.commit('addToCart', { ...product.value, quantity: quantity.value })
  ElMessage.success({
    message: '成功加入购物车',
    type: 'success',
  })
}

// 立即购买
const handleBuyNow = () => {
  if (!checkLogin()) return
  // 直接加入购物车并跳转到结算页
  addToCart()
  router.push('/cart')
}

// --- 收藏逻辑 ---
const checkFavoriteStatus = async (pid) => {
  const token = localStorage.getItem('token')
  if(!token) return
  try {
    const res = await fetch(`http://localhost:5000/api/favorites/check?product_id=${pid}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if(res.ok) {
      const data = await res.json()
      isFavorited.value = data.is_favorited
    }
  } catch(e) { console.error(e) }
}

const toggleFavorite = async () => {
  if (!checkLogin()) return
  const token = localStorage.getItem('token')
  
  try {
    const method = isFavorited.value ? 'DELETE' : 'POST'
    const url = isFavorited.value 
      ? `http://localhost:5000/api/favorites/${product.value.id}` 
      : 'http://localhost:5000/api/favorites'
      
    const body = !isFavorited.value ? JSON.stringify({ product_id: product.value.id }) : null
    
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body
    })

    if(res.ok) {
      isFavorited.value = !isFavorited.value
      ElMessage.success(isFavorited.value ? '已收藏' : '已取消收藏')
    } else {
      ElMessage.error('操作失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

// --- 点赞逻辑 ---
const checkLikeStatus = async (pid) => {
  const token = localStorage.getItem('token')
  // 如果后端有点赞状态查询接口
  try {
    const res = await fetch(`http://localhost:5000/api/products/${pid}/like/status`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if(res.ok) {
      const data = await res.json()
      // 如果后端返回当前用户是否已点赞的字段（例如 liked: true/false）
      if (data.liked !== undefined) {
        isLiked.value = data.liked
      }
      likeCount.value = data.like_count
    }
  } catch(e) {
    console.error(e)
  }
}

const likeProduct = async () => {
  if (!checkLogin()) return
  if (isLiked.value) {
    ElMessage.info('您已经赞过该商品了')
    return 
  }
  
  const token = localStorage.getItem('token')
  try {
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/like`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    const data = await res.json()
    
    if(res.ok) {
      likeCount.value = data.like_count
      isLiked.value = true
      ElMessage.success('感谢您的点赞！')
    } else {
      // 捕获后端返回的具体错误信息
      // 假设后端返回 { message: "You have already liked this product" }
      if (res.status === 400 && (data.message.includes('already') || data.message.includes('已点赞'))) {
        isLiked.value = true // 同步状态
        ElMessage.warning('您已经点过赞了')
      } else {
        ElMessage.error(data.message || '点赞失败')
      }
    }
  } catch(e) {
    ElMessage.error('网络错误，点赞失败')
  }
}

// --- 评论逻辑 ---
const submitComment = async () => {
  if (!checkLogin()) return
  if (!newComment.value.trim()) return

  const token = localStorage.getItem('token')
  try {
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ content: newComment.value })
    })
    if(res.ok) {
      ElMessage.success('评论发布成功')
      newComment.value = ''
      fetchComments()
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '评论失败')
    }
  } catch(e) { ElMessage.error('网络错误') }
}

// 工具函数
const checkLogin = () => {
  const token = localStorage.getItem('token')
  if(!token) {
    ElMessage.warning('请先登录后再操作')
    router.push('/login')
    return false
  }
  return true
}

const formatTime = (timeStr) => {
  return dayjs.utc(timeStr).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm')
}

// 简单的根据用户名生成颜色
const getRandomColor = (name) => {
  if(!name) return '#ccc'
  const colors = ['#ff758c', '#ff7eb3', '#8ec5fc', '#e0c3fc', '#fbc2eb', '#a18cd1']
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  return colors[Math.abs(hash) % colors.length]
}
  </script>

<style scoped>
.favorite-btn {
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.favorite-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 已收藏状态的星星动画 */
.favorite-btn .el-icon {
  transition: all 0.3s ease;
}

.favorite-btn:hover .el-icon {
  transform: scale(1.2);
}

/* 点赞按钮 */
.like-btn-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 18px 0;
}
.like-btn {
  font-size: 22px;
  padding: 16px 32px;
  border-radius: 32px;
  box-shadow: 0 2px 8px #eee;
  margin-bottom: 8px;
}
.like-count {
  font-size: 16px;
  color: #888;
}

/* 评论区 */
.comments-section {
  max-width: 600px;
  margin: 32px auto 0 auto;
  background: #fafbfc;
  border-radius: 12px;
  box-shadow: 0 2px 12px #ececec;
  padding: 24px 32px 16px 32px;
}
.comments-section h5 {
  margin-bottom: 18px;
  color: #333;
  font-weight: 600;
}
.list-group {
  border: none;
  padding: 0;
  margin-bottom: 16px;
}
.list-group-item {
  border: none;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #fff;
  box-shadow: 0 1px 4px #f0f0f0;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
}
.list-group-item strong {
  color: #409eff;
  margin-right: 8px;
}
.list-group-item .text-muted {
  margin-top: 2px;
  font-size: 12px;
}
.comment-form {
  margin-top: 12px;
  display: flex;
  align-items: flex-end;
}
.comment-form .el-input__wrapper {
  border-radius: 8px;
  box-shadow: 0 1px 4px #eee;
}
.comment-form .el-button {
  margin-left: 12px;
  height: 40px;
  border-radius: 8px;
}
.text-muted.mb-2 {
  display: flex;
  align-items: center;
  color: #aaa;
  font-size: 15px;
  margin-bottom: 18px;
}
.comment-list {
  list-style: none;
  padding: 0;
  margin-bottom: 16px;
}
.comment-item {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 6px #f0f0f0;
  padding: 14px 18px 10px 18px;
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}
.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}
.avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #8ec5fc 0%, #e0c3fc 100%);
  border-radius: 50%;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  box-shadow: 0 2px 8px #e0e0e0;
}
.username {
  font-weight: 500;
  color: #409eff;
  font-size: 16px;
}
.comment-content {
  margin-left: 48px;
  font-size: 15px;
  color: #333;
  margin-bottom: 4px;
  word-break: break-all;
}
.comment-time {
  margin-left: 48px;
  font-size: 12px;
  color: #aaa;
}
/* --- 产品详情布局美化 --- */
.product-info-col {
  padding-left: 2rem;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.product-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.price-tag {
  color: #ff758c;
  font-weight: bold;
  margin-bottom: 2rem;
  display: flex;
  align-items: baseline;
}

.price-tag .currency {
  font-size: 1.5rem;
  margin-right: 4px;
}

.price-tag .amount {
  font-size: 2.5rem;
  line-height: 1;
}

/* 参数网格样式 (替代表格) */
.specs-box {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  padding: 20px;
  display: grid;
  grid-template-columns: 1fr 1fr; /* 两列布局 */
  gap: 20px 24px;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.spec-item {
  display: flex;
  flex-direction: column;
}

/* 让花语占满一整行，因为通常字数较多 */
.spec-item.full-width {
  grid-column: span 2; 
  background: rgba(255, 240, 245, 0.5); /* 淡淡的粉色背景强调花语 */
  padding: 10px 12px;
  border-radius: 8px;
}

.spec-item .label {
  font-size: 13px;
  color: #888;
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}

.spec-item .value {
  font-size: 15px;
  color: #444;
  font-weight: 500;
  line-height: 1.4;
}

.text-highlight {
  color: #555;
  font-style: italic;
}

/* 操作按钮区 */
.action-area {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 2rem;
}

.qty-input {
  width: 120px;
}

.action-btn {
  padding: 12px 32px;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.2s;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.cart-btn {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
  border: none;
}

.buy-btn {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
  border: none;
  color: #fff;
}
.text-desc {
  white-space: pre-wrap; /* 保留数据库中的换行符 */
  line-height: 1.6;
  color: #666;
  font-size: 14px;
  display: block; /* 确保占满容器 */
}
</style>