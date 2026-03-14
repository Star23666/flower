<template>
  <div id="app-container">
    <AppHeaderNav v-if="!isLoginPage" />
    
    <!-- 根据是否为登录页，决定是否使用 container 限制宽度 -->
    <div :class="contentClass">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import AppHeaderNav from './components/AppHeaderNav.vue'

const route = useRoute()
const store = useStore()

// 判断当前是否在登录/注册相关页面
// 这些页面通常需要全屏背景，不需要顶部导航
const isLoginPage = computed(() => {
  const loginPaths = ['/login', '/register', '/seller/login']
  return loginPaths.some(path => route.path.startsWith(path))
})

const contentClass = computed(() => {
  return isLoginPage.value ? 'full-width-content' : 'main-container'
})

// 初始化用户信息
const localUser = JSON.parse(localStorage.getItem('user') || 'null')
if (localUser && !store.state.user) {
  store.commit('setUser', localUser)
}
</script>

<style>
/* 全局样式清理 */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  /* 使用高雅的浅色花卉背景图 */
  /* 这张图是浅粉色调的模糊背景，非常适合做全局底图 */
  background: url('https://images.pexels.com/photos/1083822/pexels-photo-1083822.jpeg?auto=compress&cs=tinysrgb&w=1920') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
}

#app-container {
  min-height: 100vh;
  /* 全局遮罩层/色调层：叠加一层淡淡的白色，让背景更柔和，不抢戏 */
  background-color: rgba(255, 255, 255, 0.4); 
  display: flex;
  flex-direction: column;
}

/* 非登录页的主容器样式 */
.main-container {
  width: 100%;
  max-width: 1200px;
  margin: 30px auto 60px; /* 增加底部留白 */
  padding: 40px;
  /* 内容区背景：高透明度的纯白，类似于高级纸张的质感 */
  background: rgba(255, 255, 255, 0.95); 
  border-radius: 16px; /* 圆角 */
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08); /* 更柔和且深邃的投影 */
  backdrop-filter: blur(10px); /* 磨砂玻璃效果 */
  flex: 1; /* 撑满剩余高度 */
  
  /* 增加边框，提升精致感 */
  border: 1px solid rgba(255, 255, 255, 0.6);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .main-container {
    margin: 15px auto;
    padding: 20px;
    width: 95%; /* 移动端稍宽一点 */
  }
}

/* 登录页全宽容器 */
.full-width-content {
  width: 100%;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px); /* 轻微的上浮效果 */
}
</style>