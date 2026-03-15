<template>
  <div class="dashboard-layout">
    <!-- 左侧侧边栏 (固定宽度) -->
    <aside class="sidebar-wrapper">
      <div class="logo-area">
        <h1>Flower MS</h1>
      </div>
      <!-- 引用独立的侧边栏组件 -->
      <SellerSidebar />
    </aside>

    <!-- 右侧主体区 -->
    <div class="main-content-wrapper">
      <!-- 顶部个人信息栏 -->
      <header class="dashboard-header">
        <div class="breadcrumb">
           <!-- 面包屑导航 -->
           <el-breadcrumb separator="/">
              <el-breadcrumb-item>商家后台</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
           </el-breadcrumb>
        </div>
        <div class="user-action">
           <el-dropdown>
            <span class="el-dropdown-link user-profile">
              <el-avatar :size="32" :icon="UserFilled" class="avatar" />
              <span class="username">{{ sellerName }}</span>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <!-- 内容展示区 (滚动) -->
      <main class="content-scroll-area">
        <!-- 移除 transition，增加 :key，解决白页问题 -->
        <router-view v-slot="{ Component, route }">
          <component :is="Component" :key="route.path" v-if="Component" />
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import SellerSidebar from '@/components/SellerSidebar.vue'
import { ArrowDown, UserFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()
const route = useRoute()

const sellerName = computed(() => store.state.user?.username || 'Seller')

// 获取当前路由名称，用于显示面包屑
const currentRouteName = computed(() => {
  const map = {
    '/seller/products': '商品管理',
    '/seller/orders': '订单管理',
    '/seller/users': '用户管理',
    '/seller/profile': '商家信息',
    '/seller/flower-categories': '花材分类'
  }
  // 简单匹配，如果路径以 key 开头
  const key = Object.keys(map).find(k => route.path.startsWith(k))
  return map[key] || '管理面板'
})

const logout = () => {
  store.commit('logout')
  router.push('/seller/login')
  ElMessage.success('已退出商家后台')
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  min-height: 100vh;
  width: 100vw;
  background-color: #f3f4f6;
  overflow: hidden; 
}

/* 侧边栏容器 */
.sidebar-wrapper {
  width: 240px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  z-index: 10;
  box-shadow: 2px 0 8px rgba(0,0,0,0.02);
}

.logo-area {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f0f0;
}
.logo-area h1 {
  font-size: 20px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.5px;
  margin: 0;
  font-family: 'Times New Roman', serif;
}

/* 右侧主体布局 */
.main-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0; 
}

/* 顶部Header */
.dashboard-header {
  height: 64px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #4b5563;
}
.username {
  margin: 0 8px;
  font-weight: 500;
}

/* 内容区域 */
.content-scroll-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 24px; 
}
</style>