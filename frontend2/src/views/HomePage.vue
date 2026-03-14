<template>
  <div class="home-container">
    <!-- Banner 区域：增加背景图和文字动画 -->
    <div class="home-banner">
      <div class="banner-overlay"></div>
      <div class="banner-content">
        <h1 class="animate-title">鲜花商店</h1>
        <p class="animate-subtitle">用鲜花点缀生活的每一天，让爱与美好自然发生</p>
        <el-button type="primary" size="large" round class="banner-btn" @click="$router.push('/products')">
          立即探索 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 功能导航卡片：悬浮在Banner下方的快捷入口 -->
    <div class="home-nav-section">
      <el-row :gutter="24">
        <el-col :span="8" :xs="24" class="nav-col">
          <div class="nav-card" @click="$router.push('/products')">
            <div class="nav-icon-wrapper purple">
              <el-icon><Goods /></el-icon>
            </div>
            <div class="nav-text">
              <h3>浏览商品</h3>
              <p>精选当季鲜花</p>
            </div>
            <el-icon class="nav-arrow"><ArrowRight /></el-icon>
          </div>
        </el-col>
        <el-col :span="8" :xs="24" class="nav-col">
          <div class="nav-card" @click="$router.push('/order-list')">
            <div class="nav-icon-wrapper green">
              <el-icon><List /></el-icon>
            </div>
            <div class="nav-text">
              <h3>我的订单</h3>
              <p>追踪美好送达</p>
            </div>
            <el-icon class="nav-arrow"><ArrowRight /></el-icon>
          </div>
        </el-col>
        <el-col :span="8" :xs="24" class="nav-col">
          <div class="nav-card" @click="$router.push('/user/profile')">
            <div class="nav-icon-wrapper orange">
              <el-icon><User /></el-icon>
            </div>
            <div class="nav-text">
              <h3>个人中心</h3>
              <p>管理地址与账户</p>
            </div>
            <el-icon class="nav-arrow"><ArrowRight /></el-icon>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 推荐商品区域 -->
    <div class="section-header">
      <h2>为您推荐</h2>
      <span class="subtitle">Based on your preferences</span>
    </div>

    <div class="products-grid">
      <div
        v-for="item in displayProducts"
        :key="item.id"
        class="product-card"
        @click="goToProduct(item.id)"
      >
        <div class="card-image-wrapper">
          <img :src="getImageUrl(item.image_url)" class="product-img" loading="lazy" />
          <!-- 悬停显示查看按钮 -->
          <div class="hover-overlay">
            <el-button type="primary" circle>
              <el-icon><View /></el-icon>
            </el-button>
          </div>
          <!-- 推荐标签 -->
          <div v-if="item.is_recommended" class="recommend-badge">
            <el-icon><StarFilled /></el-icon> 推荐
          </div>
        </div>
        
        <div class="card-info">
          <h3 class="product-name" :title="item.name">{{ item.name }}</h3>
          <div class="product-meta">
            <span class="price">¥{{ item.price }}</span>
            <span class="sales-count">销量 {{ Math.floor(Math.random() * 100) + 10 }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="home-footer">
      <div class="footer-content">
        <p>Flower Shop &copy; 2026</p>
        <p class="footer-desc">让生活如花绽放 | 客服微信：flower_support</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'
import { ArrowRight, Goods, List, User, View, StarFilled } from '@element-plus/icons-vue'

const router = useRouter()
const store = useStore()
const products = ref([])
const recommendedProducts = ref([])

// 优先展示推荐商品，如果没有则展示普通商品
const displayProducts = computed(() => {
  if (recommendedProducts.value.length > 0) {
    return recommendedProducts.value.map(p => ({ ...p, is_recommended: true }))
  }
  return products.value.slice(0, 8).map(p => ({ ...p, is_recommended: false }))
})

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/products')
    products.value = Array.isArray(res.data) ? res.data : []
  } catch (error) {
    console.error('获取商品列表失败', error)
  }
}

const fetchRecommendations = async () => {
  // 尝试从 Store 或 LocalStorage 获取用户ID
  const user = store.state.user || JSON.parse(localStorage.getItem('user'))
  const userId = user ? user.id : 1; // 默认 fallback 到用户 1
  
  try {
    const res = await axios.get(`http://localhost:5000/api/recommend/${userId}`);
    if (res.data.code === 200 && res.data.data.length > 0) {
      recommendedProducts.value = res.data.data.slice(0, 8);
    } else {
      await fetchProducts()
    }
  } catch (error) {
    console.warn('推荐加载失败，加载默认列表');
    await fetchProducts();
  }
};

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

const getImageUrl = (url) => {
  if (!url) return '' // 可以设置一个默认图片
  return url.startsWith('http') ? url : `http://localhost:5000${url}`
}

onMounted(() => {
  fetchRecommendations();
})
</script>

<style scoped>
/* 全局容器和字体 */
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
  color: #333;
}

/* Banner 样式 */
.home-banner {
  margin-top: 24px;
  height: 360px;
  border-radius: 20px;
  /* 使用 assets 中的图片，或者你可以改为网络图片 */
  background-image: url('@/assets/flowers-banner.png'); 
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  overflow: hidden;
}

/* 遮罩层，让文字更清晰 */
.banner-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
}

.banner-content {
  z-index: 2;
  position: relative;
}

.animate-title {
  font-size: 3rem;
  margin-bottom: 12px;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  letter-spacing: 2px;
}

.animate-subtitle {
  font-size: 1.2rem;
  margin-bottom: 32px;
  opacity: 0.95;
}

.banner-btn {
  padding: 22px 42px;
  font-size: 1.1rem;
  background-color: #ff758c; /* 鲜花粉色 */
  border-color: #ff758c;
  font-weight: bold;
  transition: all 0.3s;
}
.banner-btn:hover {
  background-color: #ff5e78;
  border-color: #ff5e78;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 117, 140, 0.4);
}

/* 导航卡片区 */
.home-nav-section {
  margin-top: -40px; /* 向上偏移，产生层叠感 */
  position: relative;
  z-index: 3;
  margin-bottom: 50px;
}

.nav-col {
  margin-bottom: 15px;
}

.nav-card {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

/* 图标背景色 */
.nav-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}
.nav-icon-wrapper.purple { background: #f3e5f5; color: #9c27b0; }
.nav-icon-wrapper.green { background: #e8f5e9; color: #4caf50; }
.nav-icon-wrapper.orange { background: #fff3e0; color: #ff9800; }

.nav-text h3 {
  margin: 0 0 4px 0;
  font-size: 17px;
  color: #2c3e50;
}
.nav-text p {
  margin: 0;
  font-size: 13px;
  color: #999;
}
.nav-arrow {
  margin-left: auto;
  color: #ddd;
}

/* 标题样式 */
.section-header {
  text-align: center;
  margin-bottom: 30px;
}
.section-header h2 {
  font-size: 26px;
  color: #333;
  font-weight: 600;
  margin-bottom: 5px;
}
.section-header .subtitle {
  color: #aaa;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 商品网格布局 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); /* 自适应列 */
  gap: 24px;
  margin-bottom: 60px;
}

.product-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05); /* 初始淡阴影 */
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1); /* 悬浮深阴影 */
}

/* 图片容器，保证图片比例一致 (1:1) */
.card-image-wrapper {
  position: relative;
  padding-top: 100%;
  background: #f9f9f9;
  overflow: hidden;
}

.product-img {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.product-card:hover .product-img {
  transform: scale(1.08); /* 图片轻微放大 */
}

/* 悬停时的遮罩 */
.hover-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}
.product-card:hover .hover-overlay {
  opacity: 1;
}

/* 推荐标签样式 */
.recommend-badge {
  position: absolute;
  top: 10px; right: 10px;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 4px;
  z-index: 2;
}

/* 商品信息区 */
.card-info {
  padding: 16px;
  background: #fff;
}
.product-name {
  font-size: 16px;
  color: #333;
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.price {
  color: #ff4081;
  font-size: 18px;
  font-weight: bold;
}
.sales-count {
  font-size: 12px;
  color: #999;
}

/* 底部 */
.home-footer {
  text-align: center;
  padding: 30px 0;
  border-top: 1px solid #f0f0f0;
  color: #999;
  font-size: 14px;
}
</style>