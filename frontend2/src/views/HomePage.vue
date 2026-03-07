<template>
  <div class="home-container">
<div class="home-banner">
  <div class="banner-text">
    <h1>欢迎来到鲜花商店</h1>
    <p>用鲜花点缀生活的每一天</p>
  </div>
  <div class="home-cards">
  <el-row :gutter="20">
    <el-col :span="8">
      <el-card shadow="hover">
        <h3>浏览商品</h3>
        <p>挑选你喜欢的花束</p>
        <el-button type="primary" @click="$router.push('/products')">去逛逛</el-button>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="hover">
        <h3>我的订单</h3>
        <p>随时查看订单进度</p>
        <el-button type="success" @click="$router.push('/order-list')">订单中心</el-button>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="hover">
        <h3>个人中心</h3>
        <p>管理收货地址和账户</p>
        <el-button type="info" @click="$router.push('/user/profile')">个人中心</el-button>
      </el-card>
    </el-col>
  </el-row>
</div>
</div>

<div class="random-products-grid-grid">
  <div
    v-for="item in recommendedProducts "
    :key="item.product_id"
    class="custom-card"
    @click="goToProduct(item.product_id)"
  >
    <img :src="getImageUrl(item.image_url)" class="custom-card-img" />
    <div class="custom-card-title">
      {{ item.name }}
    </div>
    <!-- 新增：推荐标识 -->
    <div v-if="item.pred_score" class="recommend-badge">推荐</div>
  </div>
</div>

<div class="home-footer">
  <p>鲜花商店 · 让生活如花绽放 | 客服微信：flower_support</p>
</div>
</div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'


const router = useRouter()
const products = ref([])
const randomProducts = ref([])  

const recommendedProducts = ref([]);  // 新增推荐数据

const fetchProducts = async () => {
  const res = await axios.get('http://localhost:5000/api/products')
  console.log(res.data)
  console.log(products.value)
  products.value = Array.isArray(res.data) ? res.data : []
  // 随机打乱并取前4个
  randomProducts.value = products.value
    .map(p => ({...p}))
    .sort(() => Math.random() - 0.5)
    .slice(0, 4)
}

const fetchRecommendations = async () => {
  const userId = 1;  // 假设用户ID为1，可以从登录状态获取
  try {
    const res = await axios.get(`http://localhost:5000/api/recommend/${userId}`);
    if (res.data.code === 200) {
      recommendedProducts.value = res.data.data.slice(0, 4);  // 取前4个推荐
    }
  } catch (error) {
    console.error('推荐加载失败', error);
    // 如果推荐失败，回退到随机
    fetchProducts();
  }
};

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

// 图片
const getImageUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http')
    ? url
    : `http://localhost:5000${url}`
}


// 第1和第个商品为竖卡，其余横卡
// const isVerticalCard = idx => idx === 0 || idx === 2
// const getColSpan = idx => isVerticalCard(idx) ? 6 : 6
// const getColStyle = idx => isVerticalCard(idx)
//   ? { display: 'flex', flexDirection: 'column', height: '540px' }
//   : { height: '260px' }

onMounted(() => {
  //fetchProducts()  //注释掉随机
  fetchRecommendations();  // 改为推荐
})


</script>

<style scoped>
/* 卡片动画 */
.el-card {
  transition: box-shadow 0.3s, transform 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-radius: 12px;
}
.el-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  transform: translateY(-6px) scale(1.03);
}

/* 按钮动画 */
.el-button {
  transition: box-shadow 0.2s, transform 0.2s;
}
.el-button:hover {
  box-shadow: 0 4px 16px rgba(64,158,255,0.18);
  transform: translateY(-2px) scale(1.04);
}

/* 底部信息 */
.home-footer {
  margin-top: 40px;
  padding: 16px 0 10px 0;
  text-align: center;
  color: #888;
  font-size: 15px;
  letter-spacing: 1px;
  background: rgba(255,255,255,0.7);
  border-radius: 0 0 12px 12px;
}

/* 内容居中 */
.home-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 0 20px;
}

/* 卡片区块和横幅增加间距 */
.home-banner {
  margin-bottom: 36px;
}
.home-cards {
  margin: 40px 0 0 0;
}
.el-row {
  margin-left: 0 !important;
  margin-right: 0 !important;
}
.el-col {
  padding-left: 10px !important;
  padding-right: 10px !important;
  margin-bottom: 24px;
}
.el-card {
  min-height: 200px;
  margin-bottom: 0;
}

/* 卡片内部内容上下留白 */
.el-card h3 {
  margin-top: 22px;
  margin-bottom: 12px;
}
.el-card p {
  margin-bottom: 28px;
  color: #666;
}
.el-card .el-button {
  margin-bottom: 18px;
}

/* Banner 区域上下空间 */
.home-banner {
  margin-top: 18px;
  margin-bottom: 36px;
}
.banner-img {
  border-radius: 12px;
}


/* 商品卡片 */
.random-products-grid-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 四列横卡 */
  grid-auto-rows: 260px;
  gap: 24px;
  margin: 40px auto 0;
  max-width: 1100px;
}

.custom-card {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 16px #e0c3fc22;
  cursor: pointer;
  transition: box-shadow 0.2s;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.custom-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  position: absolute;
  left: 0; top: 0; right: 0; bottom: 0;
  z-index: 1;
}

.custom-card-title {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35);
  color: #fff;
  font-size: 18px;
  text-align: center;
  padding: 12px 0 10px 0;
  z-index: 2;
  font-weight: 500;
  letter-spacing: 1px;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  user-select: none;
}

.recommend-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #ff4081;
  color: #fff;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  z-index: 3;
}

</style>