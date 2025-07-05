<template>
  <div class="container">
    <h2>登录</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="username" class="form-label">用户名</label>
        <input v-model="username" type="text" class="form-control" id="username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">密码</label>
        <input v-model="password" type="password" class="form-control" id="password" required>
      </div>
      <button type="submit" class="btn btn-primary">登录</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UserLogin', 
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        await this.$store.dispatch('login', {
          username: this.username,
          password: this.password,
          type:'user'
        });
        this.$router.push('/products');
      } catch (error) {
        alert('Login failed');
      }
    }
  }
};
</script>