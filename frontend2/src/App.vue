<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link class="navbar-brand" to="/">鲜花商店</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">主页</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/products">商品</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/cart">购物车 ({{ cartCount }})</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" to="/login">登录</router-link>
            </li>
            <li class="nav-item" v-if="user && user.role === 'seller'">
              <router-link class="nav-link" to="/add-product">添加商品</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" to="/seller/login">商家登录</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" to="/register">注册</router-link>
            </li>
            <li class="nav-item" v-if="user">
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
    // 优先从 Vuex 取，没有就从 localStorage 取
    return this.$store.state.user || JSON.parse(localStorage.getItem('user') || 'null');
  },
  cartCount() {
    return this.$store.state.cart.reduce((total, item) => total + item.quantity, 0);
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