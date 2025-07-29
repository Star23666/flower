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
<div class="home-footer">
  <p>鲜花商店 · 让生活如花绽放 | 客服微信：flower_support</p>
</div>
</div>
</template>

<script setup>

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

</style>