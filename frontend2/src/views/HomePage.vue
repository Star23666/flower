<template>
  <div class="home-container">
    <!-- Banner 区域 -->
    <div class="home-banner">
      <div class="banner-overlay"></div>
      <div class="banner-content">
        <h1 class="animate-title">鲜花商店</h1>
        <p class="animate-subtitle">用鲜花点缀生活的每一天</p>
        <el-button type="primary" size="large" round class="banner-btn" @click="$router.push('/products')">
          立即探索 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 左右分栏主体布局 -->
    <div class="main-split-layout">
      <!-- 左侧：关于我们 -->
      <div class="layout-side about-us-section">
        <div class="purple-header">
          <span class="header-title">关于我们</span>
          <span class="header-subtitle">ABOUT US</span>
        </div>
        
        <div class="about-content">
          <div class="about-media">
            <div class="play-icon-wrapper">
              <el-icon><VideoPlay /></el-icon>
            </div>
            <!-- 使用 require 或 import 引入本地图片，或者放入 public 目录引用 -->
            <img src="@/assets/flowers-banner.png" class="about-img" alt="About Us" />
            <div class="media-overlay-text">美好生活从设计开始</div>
          </div>
          
          <div class="about-text">
            <p>不管你想要怎样的生活，你都要去努力争取。不多尝试一些事情怎么知道自己适合什么、不适合什么呢？</p>
            <p>你说你喜欢读书，让我给你列书单... 其实，美好往往就藏在这些日常的鲜花与陪伴中。</p>
          </div>
        </div>
      </div>

      <!-- 右侧：鲜花信息推荐 -->
      <div class="layout-side recommend-section">
        <div class="purple-header">
          <span class="header-title">鲜花信息推荐</span>
          <span class="header-more" @click="$router.push('/products')">查看更多 &raquo;</span>
        </div>

        <div class="gallery-grid">
          <!-- 增加 pointer 样式和点击事件 -->
          <div
            v-for="item in displayProducts"
            :key="item.id"
            class="gallery-item clickable-card"
            :class="{ 'is-hot': item.is_recommended }"  
            @click.stop="goToProduct(item.id)"
          >
            <img :src="getImageUrl(item.image_url)" class="gallery-img" loading="lazy" />
            <div class="gallery-label-bar">{{ item.name }}</div>
            
            <!-- 推荐角标 -->
            <div v-if="item.is_recommended" class="recommend-badge">
              <el-icon class="fire-icon"><Fire /></el-icon>
              <span>推荐</span>
            </div>
            
          </div>
        </div>
      </div>
    </div>

    <!-- 鲜花资讯板块 -->
    <div class="news-section">
      <div class="purple-header">
        <span class="header-title">鲜花资讯</span>
        <span class="header-more" style="cursor: default">LATEST NEWS</span>
      </div>

      <div class="news-list">
        <!-- 增加点击跳转 -->
        <div 
          v-for="news in newsList" 
          :key="news.id" 
          class="news-item clickable-card"
          @click="handleNewsClick(news)"
          title="点击查看详情"
        >
          <div class="news-text-content">
            <h3 class="news-title">{{ news.title }}</h3>
            <p class="news-desc">{{ news.content }}</p>
            <div class="news-date">
              <el-icon><Clock /></el-icon> {{ news.date }}
            </div>
          </div>
          <div class="news-img-wrapper">
            <img :src="getImageUrl(news.image)" class="news-img" loading="lazy" />
          </div>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <div class="home-footer">
      <div class="footer-content">
        <p>Flower Shop &copy; 2026</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'
import { ArrowRight, VideoPlay, Clock, Fire } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useStore()
const products = ref([])
const recommendedProducts = ref([])

// 资讯列表
const newsList = ref([
  {
    id: 1,
    title: "有梦想，就要努力去实现",
        content: "不管你想要怎样的生活，你都要去努力争取。不多尝试一些事情怎么知道自己适合什么、不适合什么呢？如果不去尝试，你永远不知道自己有多大的潜力。生活中的每一束鲜花，都是对美好未来的期许。让我们在忙碌的日子里，也不忘给心灵放个假，去追寻那些看似遥不可及的梦想。或许路途遥远，但沿途的风景，已足够治愈这一生的疲惫。",

    date: "2025-02-19 09:16:22",
    image: "",
    productId: null // 新增字段
  },
  {
    id: 2,
    title: "又是一年毕业季，鲜花寄托离别情",
    content: "又是一年毕业季，感慨万千，还记得自己刚进学校那时候的情景，仿佛就在昨天。那时候的我们，青涩懵懂，对未来充满了无限的憧憬。如今即将各奔东西，心中难免有些不舍。送上一束鲜花，既是对过去美好时光的怀念，也是对未来前程似锦的祝福。愿我们在不同的地方，都能绽放出属于自己的光彩。...",
    date: "2025-06-12 14:20:05",
    image: "",
    productId: null
  },
  {
    id: 3,
    title: "浪漫七夕，花礼先行",
    content: "七夕今宵看碧霄，牵牛织女渡河桥。在这个充满爱意的传统节日里，鲜花是表达爱意最好的信使。不仅仅是玫瑰，百合代表百年好合，郁金香代表高贵的爱，洋桔梗代表真诚不变的爱。精心挑选一束花，写上一张卡片，告诉那个特别的人，他在你心中是多么的重要。让这份浪漫，定格在美丽的七夕夜。",
    date: "2025-08-04 10:00:00",
    image: "",
    productId: null
  },
  {
    id: 4,
    title: "家居插花指南：如何让鲜花保鲜更久",
    content: "买回来的鲜花没几天就枯萎了？这可能是你的养护方法不对。首先，修剪花枝时要在水中斜切，增加吸水面积；其次，每天换水并清洗花瓶，防止细菌滋生；最后，避免阳光直射和空调直吹。只要用心呵护，鲜花也能陪伴你更久，为你的家居生活增添一份生机与活力。",
    date: "2025-09-15 08:30:00",
    image: "",
    productId: null
  },
  {
    id: 5,
    title: "不同颜色的玫瑰花语，你送对了吗？",
    content: "红玫瑰代表热情真爱，适合热恋中的情侣；粉玫瑰代表初恋与感动，适合表白或送给朋友；白玫瑰代表纯洁无瑕，适合婚礼或表示尊敬；黄玫瑰代表友情或道歉，送礼时需谨慎。了解每种颜色的花语，才能让你的心意更准确地传达给对方。选对了颜色，花语便是一首无声的情诗。",
    date: "2025-10-20 16:45:12",
    image: "",
    productId: null
  },
  {
    id: 6,
    title: "冬季养花小贴士：温暖过冬",
    content: "冬天到了，气温骤降，家里的绿植和鲜花也需要特别的呵护。对于喜暖的植物，要及时搬入室内，保持适宜的温度；减少浇水频率，避免根部积水腐烂；利用中午温暖的阳光进行光合作用。只要注意这些细节，即使在寒冷的冬季，你的家依然可以生机勃勃，绿意盎然。",
    date: "2025-12-01 11:20:33",
    image: "",
    productId: null
  }
])

const displayProducts = computed(() => {
  let list = []
  
  // 1. 直拿推荐商品
  if (recommendedProducts.value.length > 0) {
    list = recommendedProducts.value.map(p => ({ 
      ...p, 
      id: p.product_id,   // 确保映射 product_id 为 id
      is_recommended: true // 这些都是推荐商品，显示金边和推荐标
    }))
  }

  // (删除了原先的“自动补位”逻辑)
  
  // 2. 截取前9个，并添加辅助显示的属性
  return list.slice(0, 9).map(item => ({
    ...item,
    salesCount: getFakeSales(item.id), 
    displayPrice: parseFloat(item.price || 0).toFixed(2) 
  }))
})

// 随机分配图片和ID给News
const assignRandomImages = () => {
  if (products.value.length === 0) return
  
  const tempProducts = [...products.value]
  
  newsList.value.forEach(news => {
    if (tempProducts.length > 0) {
      const randomIndex = Math.floor(Math.random() * tempProducts.length)
      const selectedProduct = tempProducts[randomIndex]
      if (selectedProduct) {
        // 重要：同时关联图片和商品ID
        if(selectedProduct.image_url) news.image = selectedProduct.image_url
        news.productId = selectedProduct.id
      }
    }
  })
}

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/products')
    products.value = Array.isArray(res.data) ? res.data : []
    if(products.value.length > 0) {
      assignRandomImages()
    }
  } catch (error) {
    console.error('获取商品列表失败', error)
  }
}

const fetchRecommendations = async () => {
  const user = store.state.user || JSON.parse(localStorage.getItem('user'))
  // 修复：确保 user 存在且有 id，否则默认为 1。避免 undefined 导致 404
  const userId = (user && user.id) ? user.id : 1; 
  
  console.log('Fetching recommend for User ID:', userId); // 调试日志

  try {
    const res = await axios.get(`http://localhost:5000/api/recommend/${userId}`);
    if (res.data.code === 200 && res.data.data.length > 0) {
      recommendedProducts.value = res.data.data;
    } 
    // 注意：这里不要在 else 里调 fetchProducts，
    // 因为我们需要 products 数据来填充 News 的图片，无论是否有推荐
  } catch (error) {
    console.error('获取推荐失败', error)
  }
};

// 跳转到商品详情
const goToProduct = (id) => {
  console.log('Trying to go to product:', id)
  if (id) {
    router.push(`/product/${id}`)
  } else {
    console.error('Invalid Product ID')
    ElMessage.warning('该商品暂时无法查看详情')
  }
}

// 资讯点击跳转
const handleNewsClick = (news) => {
  if (news.productId) {
    console.log('News clicked, go to:', news.productId)
    router.push(`/product/${news.productId}`)
  } else {
    // 如果没有关联商品（比如商品加载失败），可以跳转到商品列表页
    router.push('/products')
  }
}

const getImageUrl = (url) => {
  if (!url) return 'https://placeholder.pics/svg/320x180/E0E0E0/888888/Flower+News'
  return url.startsWith('http') ? url : `http://localhost:5000${url}`
}

/* === 在这里插入缺失的 getFakeSales 函数 === */
const getFakeSales = (id) => {
  if (!id) return 100 // 默认值，防止 id 为空出错
  // 算法：(ID * 质数) 取余 + 基础销量，保证对于同一个 ID 生成的数字是固定的
  return Math.floor((id * 167) % 800 + 120)
}

onMounted(async () => {
  // 并行获取推荐和商品列表，确保 News 总是有数据
  await Promise.all([
    fetchRecommendations(),
    fetchProducts()
  ])
})
</script>

<style scoped>
/* 容器 */
.home-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 20px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
  color: #333;
}

/* 强制增加层级，防止被遮挡 */
.clickable-card {
  cursor: pointer;
  position: relative; 
  z-index: 5; 
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.clickable-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  z-index: 10;
}

/* Banner */
.home-banner {
  margin-top: 20px;
  height: 280px;
  border-radius: 4px;
  background-image: url('@/assets/flowers-banner.png'); 
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
  margin-bottom: 40px;
}
.banner-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
}
.banner-content { z-index: 2; }
.animate-title { font-size: 2.5rem; margin-bottom: 10px; font-weight: 300; letter-spacing: 4px; }
.animate-subtitle { margin-bottom: 20px; opacity: 0.9; }
.banner-btn { background-color: transparent; border: 1px solid #fff; }
.banner-btn:hover { background-color: #fff; color: #333; border-color: #fff; }

/* 紫色标题条 */
.purple-header {
  background: linear-gradient(90deg, #9c27b0, #7b1fa2);
  /* 使用 clip-path 做斜角效果 */
  clip-path: polygon(0 0, 100% 0, 98% 100%, 0% 100%);
  color: #fff;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.header-title { font-size: 16px; font-weight: 500; letter-spacing: 1px; }
.header-more { 
  font-size: 12px; 
  opacity: 0.9; 
  font-weight: 300; 
  cursor: pointer; 
  margin-right: 20px; /* 避开斜角区域 */
}
.header-more:hover { text-decoration: underline; }

/* 左右分栏布局 */
.main-split-layout {
  display: flex;
  gap: 30px;
  margin-bottom: 50px;
  align-items: flex-start;
}
.about-us-section { flex: 0 0 320px; } /* 固定宽度 */
.recommend-section { flex: 1; min-width: 0; } /* 剩余空间 */

.about-media {
  position: relative; width: 100%; height: 200px;
  overflow: hidden; border-radius: 4px; margin-bottom: 15px;
}
.about-img {
  width: 100%; height: 100%; object-fit: cover;
}
.play-icon-wrapper {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  color: #fff; font-size: 40px; opacity: 0.8;
  z-index: 2;
}
.media-overlay-text {
  position: absolute; bottom: 10px; left: 10px;
  color: #fff; background: rgba(0,0,0,0.5);
  padding: 2px 8px; font-size: 12px;
}
.about-text p {
  font-size: 13px; color: #666; line-height: 1.6; margin-bottom: 10px;
  text-align: justify;
}

/* 推荐商品网格 */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}
.gallery-item {
  background: #f8f8f8;
  border-radius: 8px; /*稍微圆润一点*/
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative; /* 确保定位基准 */
  overflow: hidden;   /* 确保角标不溢出圆角 */
}
.gallery-img {
  width: 100%; height: 140px; object-fit: cover;
  border-radius: 2px; margin-bottom: 8px;
}
.gallery-label-bar {
  background: #eee; width: 100%; text-align: center;
  padding: 6px 0; font-size: 13px; color: #555;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.corner-badge {
  position: absolute; top: 0; right: 0;
  background: #ff5252; color: #fff;
  font-size: 10px; padding: 2px 6px;
  border-bottom-left-radius: 4px;
}

/* 新增：右上角推荐角标样式 */
.recommend-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%); /* 渐变橙红色 */
  color: #fff;
  font-size: 11px;
  font-weight: bold;
  padding: 4px 8px 4px 6px;
  border-bottom-left-radius: 12px;
  box-shadow: -2px 2px 5px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 2px;
  z-index: 2; /* 确保在图片上层 */
}

.fire-icon {
  font-size: 12px;
  animation: flicker 1.5s infinite alternate; /* 增加好玩的微动效 */
}

/* 火焰微闪动画 */
@keyframes flicker {
  0% { opacity: 0.8; transform: scale(1); }
  100% { opacity: 1; transform: scale(1.1); }
}

/* 资讯列表 */
.news-section { margin-bottom: 80px; }
.news-list {
  display: flex;
  flex-direction: column;
  gap: 40px; /* 增加间距 */
}
.news-item {
  display: flex; 
  align-items: flex-start; /* 改成顶部对齐 */
  justify-content: space-between;
  background: transparent;
  padding: 50px 0; /*稍微紧凑一点点的垂直间距*/
  border-bottom: 1px solid #eaeaea;
  transition: all 0.3s ease;
  min-height: 220px;
}
.news-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(156, 39, 176, 0.15); /* 悬停紫色光晕 */
}
.news-text-content {
  flex: 1; 
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 内容也顶部对齐 */
  padding-right: 60px; /* 间距稍微调小一点，留给文字更多空间 */
  padding-left: 0;
}
.news-title {
  font-size: 22px; 
  font-weight: 700; 
  color: #333;
  margin-bottom: 16px;
  line-height: 1.4;
}
.news-desc {
  font-size: 15px; /* 稍微调小1px让长文看起来更精致 */
  color: #555; 
  line-height: 1.8; 
  margin-bottom: 24px;
  white-space: pre-wrap;
  word-wrap: break-word;
  word-break: break-word; /* 兼容性写法 */
  text-align: justify;    /* 两端对齐，看起来像报刊 */
}
.news-date {
  font-size: 13px; 
  color: #999; 
  display: flex; 
  align-items: center; 
  gap: 8px;
  border-top: 1px dashed #eee;
  padding-top: 15px;
  width: 100%;
}
.news-img-wrapper {
  width: 320px; /* 更大的图片 */
  height: 200px; 
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  position: relative;
}
.news-img {
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
  border-radius: 8px;
  transition: transform 0.6s ease; /* 更慢更顺滑的动画 */
}
.news-item:hover .news-img {
  transform: scale(1.08);
}

/* 底部 */
.home-footer {
  border-top: 1px solid #eee; padding: 20px 0;
  text-align: center; color: #999; font-size: 12px;
}

/* 推荐商品加个金边，一眼看出来 */
.gallery-item.is-hot {
  border: 1px solid #ffd700; /* 金色边框 */
  background: #fffcf0;       /* 淡淡的暖背景 */
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2); /* 加一点光晕 */
}

/* 1. 还原 .is-hot 为优雅的金边 (去掉原来的 !important 红框) */
.gallery-item.is-hot {
  border: 1px solid #ffd700; /* 金色边框 */
  background: #fffcf0;       /* 淡淡的暖背景 */
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2); /* 加一点光晕 */
}

/* 2. 删除 .debug-reason 及其相关样式 */
/* .debug-reason { ... }  <-- 删除 */

/* 3. 删除之前那个覆盖用的 .is-hot (带 !important 的那个) */
/* .is-hot { border: 2px solid red ... } <-- 删除 */

/* 新增调试样式 */
.recommend-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ff4400;
  color: white;
  padding: 2px 6px;
  font-size: 12px;
  border-bottom-left-radius: 8px;
  z-index: 20;
}

.debug-reason {
  font-size: 12px;
  color: red;
  font-weight: bold;
  background: yellow;
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  z-index: 20;
  opacity: 0.9;
}
</style>