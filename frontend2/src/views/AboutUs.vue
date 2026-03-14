<template>
  <div class="about-page">
    
    <!-- Hero 区域：顶部大图 -->
    <div class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content container">
         <!-- 这里的文字带有淡入动画 -->
        <h1 class="animate-up">传递美好，点缀生活</h1>
        <p class="subtitle animate-up delay-200">Flower & Life — Since 2023</p>
      </div>
    </div>

    <!-- 品牌故事 -->
    <div class="section-container container-xl">
      <el-row :gutter="40" align="middle">
        <el-col :md="12" class="mb-4 mb-md-0">
          <!-- 左侧图片装饰 -->
          <div class="story-image-wrapper">
             <img src="https://images.unsplash.com/photo-1526047932273-341f2a7631f9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Our Story" class="img-fluid rounded shadow-lg story-img" />
             <div class="story-badge">
               <span>100%</span>
               <small>Fresh</small>
             </div>
          </div>
        </el-col>
        <el-col :md="12">
          <!-- 右侧文字内容 -->
          <div class="story-content">
            <h2 class="section-title">我们的故事</h2>
            <div class="divider-line"></div>
            <p class="text-muted">
              “花漾生活”不仅仅是一家花店，更是情感传递的使者。我们相信，每一朵花都有它的语言，每一束花都能讲述一个唯美的故事。
            </p>
            <p class="text-muted">
              从原产地直采到精心养护，再到花艺师的灵感创作，我们致力于将大自然最纯粹的美好，原封不动地送到您的手中。无论是节日的惊喜，还是日常的小确幸，我们都愿为您锦上添花。
            </p>
            <el-button type="primary" color="#ff758c" round size="large" class="mt-3">
              联系如果我们 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 核心价值 (图标展示) -->
    <div class="features-section">
      <div class="container-xl">
        <h2 class="text-center section-title mb-5">为什么选择我们</h2>
        <div class="row g-4">
          <!-- 价值卡片 1 -->
          <div class="col-md-4">
            <div class="feature-card text-center">
              <div class="icon-circle">
                <el-icon :size="32"><Stopwatch /></el-icon>
              </div>
              <h4>极速配送</h4>
              <p>同城2小时送达，准时传递您的心意，不让爱迟到。</p>
            </div>
          </div>
          <!-- 价值卡片 2 -->
          <div class="col-md-4">
            <div class="feature-card text-center">
              <div class="icon-circle">
                <el-icon :size="32"><Sugar /></el-icon>
              </div>
              <h4>顶级花材</h4>
              <p>精选全球优质花田，每日清晨采摘，确保每一朵都鲜嫩欲滴。</p>
            </div>
          </div>
          <!-- 价值卡片 3 -->
          <div class="col-md-4">
            <div class="feature-card text-center">
              <div class="icon-circle">
                <el-icon :size="32"><Star /></el-icon>
              </div>
              <h4>独家设计</h4>
              <p>资深花艺师团队，为您打造独一无二的专属花礼。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计数据条 -->
    <div class="stats-bar">
      <div class="container">
         <div class="row text-center text-white">
            <div class="col-4">
               <div class="stat-number">5000+</div>
               <div class="stat-label">服务客户</div>
            </div>
            <div class="col-4">
               <div class="stat-number">99%</div>
               <div class="stat-label">好评率</div>
            </div>
            <div class="col-4">
               <div class="stat-number">24/7</div>
               <div class="stat-label">在线支持</div>
            </div>
         </div>
      </div>
    </div>

  </div>
</template>

<script setup>
// 引入需要的 Element Plus 图标
import { ArrowRight, Stopwatch, Sugar, Star } from '@element-plus/icons-vue'
</script>

<style scoped>
/* --------- 全局及布局 --------- */
.about-page {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  overflow-x: hidden;
  background-color: #fff;
}

.section-container {
  padding: 80px 20px;
}

.section-title {
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  position: relative;
  display: inline-block;
}

/* 标题下方的粉色装饰线 */
.divider-line {
  width: 60px;
  height: 4px;
  background: #ff758c;
  margin-bottom: 30px;
  border-radius: 2px;
}

/* --------- Hero 区域 --------- */
.hero-section {
  position: relative;
  height: 400px;
  /* 使用 unsplash 的随机花卉图作为背景 */
  background: url('https://images.unsplash.com/photo-1507290439931-a861b5a38200?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

.hero-overlay {
  position: absolute;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4); /* 黑色半透明遮罩，突出文字 */
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-content h1 {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  letter-spacing: 2px;
}

.hero-content .subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  opacity: 0.9;
}

/* --------- 品牌故事 --------- */
.story-image-wrapper {
  position: relative;
  padding: 10px;
}

.story-img {
  border-radius: 12px;
  transition: transform 0.5s ease;
}

.story-image-wrapper:hover .story-img {
  transform: scale(1.02); /* 鼠标悬停轻微放大 */
}

/* 图片上的圆形标签 */
.story-badge {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 100px;
  height: 100px;
  background: #ff758c; /* 主色调 */
  color: white;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(255, 117, 140, 0.4);
  font-weight: bold;
  border: 4px solid #fff;
}

.story-content p {
  line-height: 1.8;
  font-size: 1.05rem;
  margin-bottom: 1.5rem;
}

/* --------- 核心价值 --------- */
.features-section {
  background-color: #f9f9f9; /* 浅灰背景区分板块 */
  padding: 80px 20px;
}

.feature-card {
  background: white;
  padding: 40px 20px;
  border-radius: 16px;
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
  border: 1px solid #eee;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.08); /* 悬浮投影 */
}

.icon-circle {
  width: 70px;
  height: 70px;
  background: rgba(255, 117, 140, 0.1);
  color: #ff758c;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  transition: background 0.3s;
}

.feature-card:hover .icon-circle {
  background: #ff758c;
  color: white; /* 悬浮时图标反白 */
}

.feature-card h4 {
  margin-bottom: 15px;
  font-weight: 600;
}

.feature-card p {
  color: #666;
  font-size: 0.95rem;
}

/* --------- 统计条 --------- */
.stats-bar {
  background: #333; /* 深色底 */
  padding: 60px 0;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ff758c;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.8;
}

/* --------- 简单动画类 --------- */
.animate-up {
  animation: fadeInUp 1s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

.delay-200 {
  animation-delay: 0.2s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  .story-badge {
    right: 10px;
    bottom: -10px;
    width: 80px;
    height: 80px;
    font-size: 0.8rem;
  }
}
</style>