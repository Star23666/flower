<template>
  <div class="dashboard-layout">
    <!-- 左侧侧边栏 (固定宽度) -->
    <aside class="sidebar-wrapper">
      <div class="logo-area">
        <h1>Flower MS</h1>
      </div>
      <SellerSidebar />
    </aside>

    <!-- 右侧主体区 -->
    <div class="main-content-wrapper">
      <!-- 顶部个人信息栏 -->
      <header class="dashboard-header">
        <div class="breadcrumb">
           <!-- 这里可以放面包屑，或者简单的问候语 -->
           <span>Good day, 商家管理员</span>
        </div>
        <div class="user-action">
           <el-dropdown>
            <span class="el-dropdown-link user-profile">
              <el-avatar :size="32" icon="UserFilled" class="avatar" />
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
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
             <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import SellerSidebar from '@/components/SellerSidebar.vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const sellerName = computed(() => store.state.user?.username || 'Seller')

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
  min-height: 100vh; /* 兜底 */
  width: 100vw;
  background-color: #f3f4f6;
  overflow: hidden; /* 防止双滚动条 */
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
  min-width: 0; /* 防止子元素撑开flex */
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
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  z-index: 5;
}

.breadcrumb {
  font-size: 14px;
  color: #6b7280;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.user-profile:hover {
  background: #f3f4f6;
}
.user-profile .avatar {
  background: #e0e7ff;
  color: #4f46e5;
  margin-right: 8px;
}
.user-profile .username {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

/* 内容滚动区 */
.content-scroll-area {
  flex: 1;
  overflow-y: auto; /* 只有这里滚动 */
  padding: 24px 32px;
  background: #f9fafb;
}

/* 路由转场动画 */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>