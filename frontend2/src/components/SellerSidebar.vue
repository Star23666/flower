<template>
  <el-menu
    :default-active="activeMenu"
    class="sidebar-menu"
    unique-opened
    router
    :collapse="false"
  >
    <!-- 1. 用户管理 -->
    <el-menu-item index="/seller/users">
      <el-icon><User /></el-icon>
      <span>用户管理</span>
    </el-menu-item>

    <!-- 2. 鲜花分类 -->
    <el-menu-item index="/seller/flower-categories">
      <el-icon><Menu /></el-icon>
      <span>鲜花分类</span>
    </el-menu-item>

    <!-- 3. 商品管理 -->
    <el-menu-item index="/seller/products">
      <el-icon><Goods /></el-icon>
      <span>商品管理</span>
    </el-menu-item>

    <!-- 4. 订单管理 -->
    <el-menu-item index="/seller/orders">
      <el-icon><List /></el-icon>
      <span>订单管理</span>
    </el-menu-item>

    <!-- 5. 个人中心 -->
    <el-menu-item index="/seller/profile">
      <el-icon><Setting /></el-icon>
      <span>商家信息</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
// 引入 Element Plus 图标
import {
  User,
  List,
  Goods,
  Menu,
  Setting
} from '@element-plus/icons-vue'

const route = useRoute()

// 自动高亮当前路由对应的菜单项
const activeMenu = computed(() => {
  // 如果是子路由，也能匹配到父级菜单（例如 /seller/products/add -> /seller/products）
  if (route.path.startsWith('/seller/products')) return '/seller/products'
  return route.path
})
</script>

<style scoped>
/* 菜单容器样式 */
.sidebar-menu {
  border-right: none !important; /* 去掉 Element Plus 默认的右边框，由父容器处理 */
  background-color: transparent; /* 背景透明，复用父容器背景 */
  width: 100%; /* 关键：撑满父容器宽度 (240px) */
  min-height: 100%;
  padding-top: 10px;
}

/* 菜单项基础样式 */
:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  font-size: 15px;
  color: #606266; /* 柔和的深灰 */
  margin: 4px 12px; /* 上下留白，左右缩进，做成悬浮卡片感 */
  border-radius: 8px; /* 圆角 */
  transition: all 0.3s;
}

/* 菜单项：鼠标悬停 */
:deep(.el-menu-item:hover) {
  background-color: #f0f2f5; 
  color: #409eff;
}

/* 菜单项：选中状态 */
:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff; /* 浅蓝背景 */
  color: #409eff;            /* 品牌蓝文字 */
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.15); /* 轻微投影 */
}

/* 图标样式调整 */
:deep(.el-icon) {
  font-size: 18px;
  margin-right: 12px; 
  vertical-align: middle;
}
</style>