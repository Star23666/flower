<template>
<!-- 全局面包屑组件 -->

<!-- <nav aria-label="breadcrumb" class="breadcrumb-bar">
    <ol class="breadcrumb">
      <li v-for="(item, idx) in breadcrumbs" :key="idx" class="breadcrumb-item" :class="{ active: idx === breadcrumbs.length - 1 }">
        <template v-if="idx !== breadcrumbs.length - 1">
          <router-link :to="item.path">{{ item.label }}</router-link>
        </template>
        <template v-else>
          {{ item.label }}
        </template>
      </li>
    </ol>
  </nav> -->

  <div id="app">
    <!-- 只要不是登录页才显示导航栏 -->
    <!--
      一个 Bootstrap 导航栏，它在不是登录/注册/商家登录页时显示。
      导航栏包含以下链接：
      - 主页
      - 商品
      - 购物车
      - 如果用户未登录，显示登录和注册链接
      - 如果用户是商家，显示添加商品链接
      - 如果用户已经登录，显示退出登录链接
    -->
    <nav v-if="!isLoginPage" class="navbar navbar-expand-lg navbar-light bg-light">
      <!-- 你的导航栏内容 -->
      <!-- <div class="container">
        <router-link class="navbar-brand" to="/">鲜花商店</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="user && user.role === 'user'" >
              <router-link class="nav-link" to="/home">主页</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'">
              <router-link class="nav-link" to="/products">商品</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'">
              <router-link class="nav-link" to="/cart">购物车</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" to="/login">登录</router-link>
            </li> 
            <li class="nav-item" v-if="user && user.role === 'user'" >
              <router-link class="nav-link" to="/user/profile">个人中心</router-link>
            </li>
          </ul>
        </div>
      </div> -->
    </nav>
    <AppHeaderNav v-if="!isLoginPage" />
    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
// import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import AppHeaderNav from './components/AppHeaderNav.vue'
import { useStore } from 'vuex'
// // 状态
// const store = useStore()
const route = useRoute()

// const router = useRouter()

// 面包屑
// const breadcrumbs = computed(() => {
//   const arr = []
//   // 判断是否在商品详情页
//   if (route.name === 'ProductDetail') {
//     if (route.query.from === 'favorites') {
//       arr.push({ path: '/user/profile', label: '我的收藏' })
//     } else {
//       arr.push({ path: '/products', label: '商品' })
//     }
//     arr.push({ path: route.fullPath, label: route.meta.breadcrumb || '详情' })
//     return arr
//   }
//   // 其它页面用默认 route.matched
//   return route.matched
//     .filter(r => r.meta && r.meta.breadcrumb)
//     .map(r => ({
//       path: r.path.startsWith('/') ? r.path : '/' + r.path,
//       label: r.meta.breadcrumb
//     }))
// })

// 用户信息
// const user = computed(() =>
//   store.state.user || JSON.parse(localStorage.getItem('user') || 'null')
// )

// 购物车数量
// const cartCount = computed(() =>
//   (store.state.cart || []).reduce((total, item) => total + item.quantity, 0)
// )


// 是否为登录相关页面
const loginPages = ['/', '/login', '/register', '/seller/login']
const isLoginPage = computed(() => loginPages.includes(route.path))
const store = useStore()
const localUser = JSON.parse(localStorage.getItem('user') || 'null')
if (localUser && !store.state.user) {
  store.commit('setUser', localUser)
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.container {
  max-width: 1200px;
}
</style>