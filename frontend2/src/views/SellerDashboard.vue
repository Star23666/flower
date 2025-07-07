<template>
  <div class="seller-dashboard">
    <!-- 左侧为商家侧边栏，右侧为内容区 -->
    <div class="dashboard-container">
      <!-- 侧边栏 -->
      <SellerSidebar />
      <!-- 内容区：根据路由显示不同管理页面 -->
      <div class="dashboard-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
// 仪表盘主布局组件，只负责显示侧边栏和内容区
import SellerSidebar from '@/components/SellerSidebar.vue'
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}
.dashboard-content {
  flex: 1;
  padding: 32px;
  background: #f7f8fa;
}
</style>