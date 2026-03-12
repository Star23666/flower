<template>
<nav class="header-bar">
  <router-link to="/" class="logo-area">
    <el-icon class="logo-icon"><Grid /></el-icon>
    <span class="logo-text">花漾生活</span>
  </router-link>
  <div class="header-actions">
  <div class="nav-links">
    <router-link to="/home" class="nav-link" active-class="active-link">
      <el-icon class="nav-icon"><House /></el-icon>
      <span>首页</span>
    </router-link>
    <router-link to="/products" class="nav-link" active-class="active-link">
      <el-icon class="nav-icon"><Grid /></el-icon>
      <span>商品</span>
    </router-link>
    <router-link to="/cart" class="nav-link" active-class="active-link">
      <el-icon class="nav-icon"><ShoppingCart /></el-icon>
      <span>购物车</span>
    </router-link>
    <router-link to="/about" class="nav-link" active-class="active-link">
      <el-icon class="nav-icon"><InfoFilled /></el-icon>
      <span>关于</span>
    </router-link>
  </div>

  <router-link to="/user/profile" class="avatar-link">
    <img
      v-if="userAvatar"
      :src="userAvatar"
      :alt="userName"
      class="avatar-img"
    />
    <span
      v-else
      class="avatar-fallback"
    >
      {{ userName?.charAt(0).toUpperCase() || 'U' }}
    </span>
  </router-link>
</div>
</nav>
</template>
  
<script setup>
import {ShoppingCart, House, Grid, InfoFilled } from '@element-plus/icons-vue'

import { computed ,ref,watch} from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const user = ref(store.state.user || JSON.parse(localStorage.getItem('user') || 'null'))
// 只要 store.state.user 变化就同步 user
watch(
  () => store.state.user,
  (newUser) => {
    user.value = newUser || JSON.parse(localStorage.getItem('user') || 'null')
  },
  { immediate: true, deep: true }
)

// 轮询 localStorage 防止其它窗口登录/退出
setInterval(() => {
  const local = JSON.parse(localStorage.getItem('user') || 'null')
  if (JSON.stringify(local) !== JSON.stringify(user.value)) {
    user.value = local
    store.commit && store.commit('setUser', local)
  }
}, 1000)

const userAvatar = computed(() => {
  if (!user.value?.avatar) return ''
  return user.value.avatar.startsWith('http')
    ? user.value.avatar
    : `http://localhost:5000${user.value.avatar}`
})
const userName = computed(() => user.value?.username || '')

console.log('user:', user.value)
  </script>
  
  <style scoped>

.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(90deg, #f9fafc 60%, #e0c3fc 100%);
  box-shadow: 0 2px 12px #ececec;
  padding: 0 48px;
  height: 64px;
  border-radius: 0 0 16px 16px;
}

.logo-area {
  display: flex;
  align-items: center;
  font-size: 26px;
  color: #409eff;
  font-weight: bold;
  text-decoration: none;
  margin-right: 36px;
}

.logo-icon {
  font-size: 32px;
  margin-right: 10px;
  color: #67c23a;
}

.logo-text {
  letter-spacing: 2px;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
}
.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* 让内容靠右 */
  background: linear-gradient(90deg, #f9fafc 60%, #e0c3fc 100%);
  box-shadow: 0 2px 12px #ececec;
  padding: 0 48px;
  height: 64px;
  border-radius: 0 0 16px 16px;
}
.nav-links {
  display: flex;
  align-items: center;
}

.avatar-link {
  margin-left: 18px;
  display: flex;
  align-items: center;
}
.nav-link {
  display: flex;
  align-items: center;
  color: #409eff;
  font-size: 17px;
  padding: 0 18px;
  transition: color 0.2s, background 0.2s;
  border-radius: 6px;
  height: 48px;
  text-decoration: none;
}

.nav-link .nav-icon {
  margin-right: 7px;
  font-size: 22px;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active-link {
  color: #67c23a;
  background: #f0f9eb;
}

.nav-link:hover .nav-icon,
.nav-link.active-link .nav-icon {
  color: #67c23a;
}

.avatar-link {
  margin-left: 18px;
  display: flex;
  align-items: center;
}

.avatar-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  box-shadow: 0 2px 8px #e0e0e0;
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  display: inline-block;
  background: #409eff;
  color: #fff;
  text-align: center;
  line-height: 32px;
  border-radius: 50%;
  font-weight: bold;
  font-size: 18px;
}

  </style>