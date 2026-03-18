<template>
  <div class="recommend-wrapper" v-if="recommendations.length > 0">
    <div class="divider-header">
      <span class="line"></span>
      <span class="title">猜你喜欢</span>
      <span class="line"></span>
    </div>

    <div class="product-grid">
      <div 
        v-for="item in recommendations" 
        :key="item.product_id" 
        class="product-card"
        @click="goToDetail(item.product_id)"
      >
        <div class="img-box">
          <img :src="getImageUrl(item.image_url)" loading="lazy" />
          <!-- 角标：区分是算法推荐还是新品 -->
          <div class="badge" :class="item.type">
            {{ item.type === 'cf' ? '精选' : '新品' }}
          </div>
        </div>
        <div class="info">
          <div class="name" :title="item.name">{{ item.name }}</div>
          <div class="price-row">
            <span class="price">¥{{ item.price }}</span>
            <!-- <span class="sales">已售 {{ getFakeSales(item.product_id) }}</span> -->
          </div>
          <div class="reason" v-if="item.reason">{{ item.reason }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const store = useStore()
const router = useRouter()
const route = useRoute()

const recommendations = ref([])
const defaultImg = 'https://placeholder.pics/svg/300x300/E3E3E3/999/暂无图片'

// === 新增：图片地址处理函数 ===
const getImageUrl = (url) => {
  if (!url) return defaultImg
  // 如果已经是完整路径则直接返回，否则拼接后端地址
  if (url.startsWith('http')) return url
  return `http://localhost:5000${url}`
}


const user = computed(() => store.state.user)

// 1. 获取推荐数据
const fetchRecommendations = async () => {
  // 如果没登录，暂时不展示，或者也可以调用一个不带ID的 public 接口
  // 这里我们假设没登录就不显示，保持页面清爽
  if (!user.value || !user.value.id) {
     recommendations.value = []
     return
  }

  try {
    // 复用你已有的后端接口
    const res = await axios.get(`http://localhost:5000/api/recommend/${user.value.id}`)
    if (res.data.code === 200) {
      recommendations.value = res.data.data || []
    }
  } catch (error) {
    console.error("获取推荐失败", error)
  }
}

// 2. 跳转详情
const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

// // 3. 生成假销量 (为了好看)
// const getFakeSales = (id) => {
//   return Math.floor((id * 93) % 500 + 50)
// }

// 4. 监听路由变化，如果在详情页互跳，需要刷新推荐
watch(() => route.path, () => {
  // 可以选择刷新，也可以不刷新，看需求
  // fetchRecommendations() 
})

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
.recommend-wrapper {
  margin-top: 60px;
  margin-bottom: 40px;
  padding: 0 10px;
}

/* 分割线标题 */
.divider-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  color: #999;
}
.divider-header .line {
  width: 60px;
  height: 1px;
  background: #e0e0e0;
}
.divider-header .title {
  margin: 0 20px;
  font-size: 18px;
  color: #333;
  font-weight: 600;
  display: flex;
  align-items: center;
}
.divider-header .title::before {
  content: '♥';
  color: #ff4400;
  margin-right: 8px;
  font-size: 14px;
}

/* 网格布局：自适应 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #f0f0f0;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.img-box {
  width: 100%;
  height: 200px;
  position: relative;
  background: #f9f9f9;
}
.img-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.badge {
  position: absolute;
  top: 0;
  left: 0;
  padding: 2px 6px;
  color: #fff;
  font-size: 10px;
  border-bottom-right-radius: 6px;
}
.badge.cf { background: linear-gradient(135deg, #ff4400, #ff8800); }
.badge.latest { background: linear-gradient(135deg, #2196F3, #00BCD4); }

.info {
  padding: 12px;
}
.name {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.price-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.price {
  color: #ff4400;
  font-size: 16px;
  font-weight: bold;
}
.sales {
  color: #999;
  font-size: 12px;
}
.reason {
  margin-top: 6px;
  font-size: 10px;
  color: #ff4400;
  background: #fff0eb;
  padding: 2px 4px;
  border-radius: 2px;
  display: inline-block;
}
</style>