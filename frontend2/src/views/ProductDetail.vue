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
        <div class="col-md-6">
          <h2 class="mb-0">{{ product.name }}</h2>
          <el-button 
  :type="isFavorited ? 'danger' : 'primary'" 
  :icon="isFavorited ? 'StarFilled' : 'Star'" 
  @click="toggleFavorite"
  class="favorite-btn"
>
  {{ isFavorited ? '已收藏' : '点我收藏' }}
</el-button>
          <div class="mb-3 fs-4 text-danger">¥{{ product.price }}</div>
          <table  class="table table-borderless mb-3" style="width:auto">
            <tbody>
              <tr>
                <td class="text-secondary">鲜花类型</td>
                <td>
                {{ categories && categories.find ? (categories.find(c => c.id === product.category_id)?.name || '暂无') : '暂无' }}
                </td>
              </tr>
              <tr>
                <td class="text-secondary">鲜花花语</td>
                <td>{{ product.flower_language2 || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">鲜花产地</td>
                <td>{{ product.origin || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">适用场景</td>
                <td>{{ product.scene || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">适用对象</td>
                <td>{{ product.target || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">点击次数</td>
                <td>{{ product.click_count || 0 }}</td>
              </tr>
            </tbody>
          </table>
          <!-- 操作区 -->
          <div class="d-flex align-items-center mb-3">
            <input
              type="number"
              min="1"
              :max="product.stock"
              class="form-control mx-2"
              style="width: 80px; text-align: center;"
              v-model.number="quantity"
            >
            <button class="btn btn-success me-2" @click="addToCart">加入到购物车</button>
            <button class="btn btn-warning">立即购买</button>
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
  </template>
  
<script setup>
  import dayjs from 'dayjs'
  import utc from 'dayjs/plugin/utc'
  import timezone from 'dayjs/plugin/timezone'


  
  import { ref, onMounted, computed } from 'vue'
  import { ElMessage } from 'element-plus'
  import { useStore } from 'vuex'
  import { useRoute } from 'vue-router'
  import AppBreadcrumbs from '@/components/AppBreadcrumbs.vue'
  
  dayjs.extend(utc)
  dayjs.extend(timezone)

  const store = useStore()
  const route = useRoute()
  
  const product = ref({})
  const quantity = ref(1)
  const categories = ref([])
  const isFavorited = ref(false)
  
  // 点赞
  const likeCount = ref(product.value.like_count || 0)
  const isLiked = ref(false) // 可根据用户是否已点赞初始化
  const user = computed(() =>
  store.state.user || JSON.parse(localStorage.getItem('user') || 'null')
)
  const likeProduct = async () => {
  if (!user.value) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/like`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (res.ok) {
      
      const data = await res.json()
      likeCount.value = data.like_count // 用后端返回的点赞数
      isLiked.value = true
      ElMessage.success('点赞成功！')
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '点赞失败')
    }
  } catch (e) {
    ElMessage.error('点赞失败')
  }
}


  // const from = route.query.from


  // 面包屑
  // const breadcrumbs = computed(() => {
  //   const arr = []
  //   if (from === 'favorites') {
  //     arr.push({ path: '/user/profile', label: '我的收藏' })
  //   } else {
  //     arr.push({ path: '/products', label: '商品' })
  //   }
  //   arr.push({ path: route.fullPath, label: product.value?.name || '详情' })
  //   return arr
  // })
  // 获取分类

  // 评论区
  const comments = ref([
  // 示例数据
  // { id: 1, username: '小明', content: '很漂亮的花！', created_at: '2025-08-01 16:00' }
])
  const newComment = ref('')

  const submitComment = async () => {
    if (!newComment.value.trim()) return
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ content: newComment.value })
  })
    if (res.ok) {
      console.log(comments.value)
      console.log('评论接口状态', res.status)
      const data = await res.json()
      console.log('评论接口响应', data)
      ElMessage.success(data.message)
      newComment.value = ''
      fetchComments() // 重新加载评论
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '评论失败')
    }
  }



  const fetchCategories = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:5000/api/categories', {
        headers: {
          'Authorization': 'Bearer ' + token
        }
      })
      categories.value = await res.json()
    } catch (e) {
      categories.value = []
    }
  }
  
  // 获取商品详情
  const fetchProduct = async (id) => {
    const res = await fetch(`http://localhost:5000/api/products/${id}`)
    product.value = await res.json()
  }
  
  // 切换收藏状态
  const toggleFavorite = async () => {
    const token = localStorage.getItem('token')
    if (!token){
      ElMessage.warning('请先登录')
      return
    }

    try {
      const method = isFavorited.value ? 'DELETE' : 'POST'
      const url = isFavorited.value 
      ? `http://localhost:5000/api/favorites/${product.value.id}`
      : 'http://localhost:5000/api/favorites'
      
      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: !isFavorited.value ? JSON.stringify({ product_id: product.value.id }) : null
      })
      
      if (res.ok) {
        isFavorited.value = !isFavorited.value
        ElMessage.success(isFavorited.value ? '已添加到收藏夹' : '已取消收藏')
      }else{
        const error = await res.json()
        ElMessage.error(error.messagege || '操作失败，请重试') 
      }
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败，请重试')
    }
  }
  
  // 获取商品图片
  const getProductImage = (product) => {
    if (!product || !product.image_url) {
      return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZWVlZWVlIi8+CiAgPHRleHQgeD0iNTAlIiB5PSI1JSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5OTk5Ij5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+'
    }
    if (product.image_url.startsWith('http')) return product.image_url
    return `http://localhost:5000${product.image_url}`
  }
  
  // 增加数量
  // const increaseQty = () => {
  //   quantity.value++
  // }
  
  // // 减少数量
  // const decreaseQty = () => {
  //   if (quantity.value > 1) quantity.value--
  // }
  
  // 添加到购物车
  const addToCart = () => {
    if (quantity.value < 1) quantity.value = 1
    if (quantity.value > product.value.stock) {
      quantity.value = product.value.stock
      ElMessage.warning('库存不足')
      return
    }
    
    store.commit('addToCart', { ...product.value, quantity: quantity.value })
    ElMessage.success('已加入购物车')
  }
  
  // 检查是否已收藏
  const checkFavoriteStatus = async () => {
    const token = localStorage.getItem('token')
    if(!token) return
    
    try {
      const res = await fetch(`http://localhost:5000/api/favorites/check?product_id=${product.value.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (res.ok) {
        const data = await res.json()
        isFavorited.value = data.is_favorited
      }
    } catch (error) {
      console.error('检查收藏状态失败:', error)
    }
  }
  // 获取评论区

  const fetchComments = async () => {
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/comments`)
    if (res.ok) {
      comments.value = await res.json()
    }
  }

  // 组件挂载时获取数据
  onMounted(async () => {
    const id = route.params.id
    console.log('组件挂载时的登录状态:',store.state.isLoggedIn)
    await fetchProduct(id)
    await fetchCategories()
    await checkFavoriteStatus()
    fetchComments()

    // 获取点赞状态
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/products/${product.value.id}/like/status`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (res.ok) {
    const data = await res.json()
    likeCount.value = data.like_count
    isLiked.value = data.liked
    }
  })
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
</style>