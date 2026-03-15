<template>
  <nav class="header-bar" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-container">
      <!-- Logo 区域 -->
      <router-link to="/" class="logo-area">
        <div class="logo-icon-wrapper">
          <!-- 如果你有 logo 图片，取消注释下一行并确保路径正确 -->
          <!-- <img src="@/assets/logo.png" alt="Logo" class="logo-img" /> -->
          <el-icon class="logo-icon"><MoonNight /></el-icon>
        </div>
        <div class="logo-text-group">
          <span class="logo-title">花漾生活</span>
          <span class="logo-subtitle">FLOWER LIFE</span>
        </div>
      </router-link>

      <!-- 中间导航链接 (桌面端显示) -->
      <div class="nav-middle">
        <router-link to="/home" class="nav-item" active-class="active-link">
          <span>首页</span>
          <div class="nav-indicator"></div>
        </router-link>
        <router-link to="/products" class="nav-item" active-class="active-link">
          <span>鲜花系列</span>
          <div class="nav-indicator"></div>
        </router-link>
        <router-link to="/about" class="nav-item" active-class="active-link">
          <span>关于我们</span>
          <div class="nav-indicator"></div>
        </router-link>
      </div>

      <!-- 右侧操作区 -->
      <div class="header-actions">
        
        <!-- 购物车 -->
        <router-link to="/cart" class="action-btn icon-btn" title="购物车">
          <el-badge :value="cartCount" :hidden="!cartCount" class="cart-badge" type="primary">
            <el-icon><ShoppingCart /></el-icon>
          </el-badge>
        </router-link>

        <!-- 分割线 -->
        <div class="divider"></div>

        <!-- 用户区域：根据登录状态显示不同内容 -->
        <div class="user-area">
          <template v-if="user">
            <el-dropdown trigger="click" @command="handleCommand">
              <div class="user-profile-trigger">
                <img v-if="userAvatar" :src="userAvatar" class="user-avatar" />
                <div v-else class="avatar-fallback">{{ userInitial }}</div>
                <span class="username">{{ user.username }}</span>
                <el-icon class="arrow-icon"><CaretBottom /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu class="custom-dropdown">
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="orders">
                    <el-icon><List /></el-icon>我的订单
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout" style="color: #f56c6c;">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          
          <template v-else>
            <router-link to="/login" class="login-btn">
              登录
            </router-link>
            <router-link to="/register" class="register-btn">
              注册
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { 
  ShoppingCart, User, List, SwitchButton, 
  CaretBottom, MoonNight 
} from '@element-plus/icons-vue'

import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

// 状态
const isScrolled = ref(false)
const user = ref(store.state.user || JSON.parse(localStorage.getItem('user') || 'null'))

// 监听滚动，改变导航栏样式
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// 监听 User 变化
watch(
  () => store.state.user,
  (newUser) => {
    user.value = newUser || JSON.parse(localStorage.getItem('user') || 'null')
  },
  { deep: true }
)

// Computed
const userAvatar = computed(() => {
  if (!user.value?.avatar) return ''
  return user.value.avatar.startsWith('http')
    ? user.value.avatar
    : `http://localhost:5000${user.value.avatar}`
})

const userInitial = computed(() => {
  return user.value?.username?.charAt(0).toUpperCase() || 'U'
})

// 购物车数量（即使 Vuex 里没有，也可以先设为0或者读取 localStorage）
const cartCount = computed(() => {
  return 0 // 这里可以对接你的 store.state.cartCount
})

// 下拉菜单逻辑
const handleCommand = (command) => {
  if (command === 'logout') {
    // 调用 store 的 logout 方法，一次性清除所有状态
    store.commit('logout') 
    
    // 强制跳转到登录页
    router.push('/login')
    
    // 可选：刷新页面以确保彻底重置（解决某些极端缓存情况）
    setTimeout(() => location.reload(), 100) 
  } else if (command === 'profile') {
    router.push('/user/profile')
  } else if (command === 'orders') {
    router.push('/order-list')
  }
}
</script>

<style scoped>
/* 导航栏容器 - 磨砂玻璃效果 */
.header-bar {
  position: sticky;
  top: 0;
  width: 100%;
  height: 70px;
  background: rgba(255, 255, 255, 0.85); /* 半透明背景 */
  backdrop-filter: blur(10px); /* 模糊效果 */
  box-shadow: 0 1px 0 rgba(0,0,0,0.05); /* 极细边框线 */
  z-index: 1000;
  transition: all 0.3s ease;
}

.header-bar.is-scrolled {
  background: rgba(255, 255, 255, 0.98);
  height: 60px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08); /* 滚动后阴影加深 */
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 左侧 Logo */
.logo-area {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 12px;
}

.logo-icon-wrapper {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 4px 10px rgba(161, 140, 209, 0.4);
}

.logo-text-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
  letter-spacing: 1px;
}

.logo-subtitle {
  font-size: 10px;
  color: #999;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* 中间导航 - 居中悬浮 */
.nav-middle {
  display: flex;
  align-items: center;
  gap: 40px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav-item {
  position: relative;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  color: #555;
  padding: 6px 0;
  transition: color 0.3s;
}

.nav-item:hover, .nav-item.active-link {
  color: #a18cd1; /* 主题紫 */
}

/* 动态下划线 */
.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #a18cd1, #fbc2eb);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 2px;
}

.nav-item:hover .nav-indicator,
.nav-item.active-link .nav-indicator {
  width: 100%;
}

/* 右侧操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 图标按钮 */
.action-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 20px;
  border-radius: 50%;
  transition: all 0.2s;
  text-decoration: none;
}

.action-btn:hover {
  background: #f5f7fa;
  color: #a18cd1;
}

/* 分割线 */
.divider {
  width: 1px;
  height: 20px;
  background: #eee;
  margin: 0 12px;
}

/* 用户头像区 */
.user-profile-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 20px;
  transition: background 0.2s;
}

.user-profile-trigger:hover {
  background: #f0f2f5;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #a18cd1;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

.username {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.arrow-icon {
  font-size: 12px;
  color: #bbb;
}

/* 登录/注册按钮 */
.login-btn, .register-btn {
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s;
}

.login-btn {
  color: #666;
}
.login-btn:hover {
  color: #a18cd1;
}

.register-btn {
  background: #333;
  color: #fff;
  margin-left: 8px;
}
.register-btn:hover {
  background: #a18cd1;
  box-shadow: 0 4px 12px rgba(161, 140, 209, 0.4);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .nav-middle {
    display: none; /* 移动端暂时隐藏中间菜单 */
  }
  .username, .arrow-icon {
    display: none;
  }
  .divider {
    display: none;
  }
}
</style>