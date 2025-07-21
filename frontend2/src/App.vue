<template>
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
      <div class="container">
        <router-link class="navbar-brand" to="/">鲜花商店</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="user && user.role === 'user'" >
              <router-link class="nav-link" to="/">主页</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'">
              <router-link class="nav-link" to="/products">商品</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'">
              <router-link class="nav-link" to="/cart">购物车 ({{ cartCount }})</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" to="/login">登录</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'" >
              <router-link class="nav-link" to="/user/profile">个人中心</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'user'"  >
              <a class="nav-link" href="#" @click="logout">退出登录</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

export default {
  name: 'AppMain',
  computed: {
    user() {
      return this.$store.state.user || JSON.parse(localStorage.getItem('user') || 'null');
    },
    cartCount() {
  return (this.$store.state.cart || []).reduce((total, item) => total + item.quantity, 0);
},
    // 新增：判断当前路由是否为登录/注册/商家登录页
    isLoginPage() {
      const loginPages = ['/', '/login', '/register', '/seller/login']
      return loginPages.includes(this.$route.path)
    }
  },
  methods: {
    logout() {
      this.$store.commit('setUser', null);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      this.$router.push('/login');
    }
  }
};
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