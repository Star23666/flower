<template>
  <div class="container">
    <h2>注册</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="username" class="form-label">用户名</label>
        <input v-model="username" type="text" class="form-control" id="username" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">邮箱</label>
        <input v-model="email" type="email" class="form-control" id="email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">密码</label>
        <input v-model="password" type="password" class="form-control" id="password" required>
      </div>
      <div class="mb-3">
        <label for="gender" class="form-label">性别</label>
        <select v-model="gender" class="form-select" id="gender" required>
          <option value="" disabled>请选择性别</option>
          <option value="男">男</option>
          <option value="女">女</option>
          <option value="保密">保密</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="phone" class="form-label">电话</label>
        <input v-model="phone" type="text" class="form-control" id="phone" required>
      </div>
      <button type="submit" class="btn btn-primary">注册</button>
    </form>
  </div>
</template>
  
<script>
export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      gender: '',
      phone: ''
    };
  },
  methods: {
    async register() {
      try {
        await this.$store.dispatch('register', {
          username: this.username,
          email: this.email,
          password: this.password,
          gender: this.gender,
          phone: this.phone
        });
        this.$router.push('/login');
      } catch (error) {
        alert('Registration failed');
      }
    }
  }
};
</script>