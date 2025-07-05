<template>
    <div class="container">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" id="email" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserRegister', // Changed from 'Register'
    data() {
      return {
        username: '',
        email: '',
        password: ''
      };
    },
    methods: {
      async register() {
        try {
          await this.$store.dispatch('register', {
            username: this.username,
            email: this.email,
            password: this.password
          });
          this.$router.push('/login');
        } catch (error) {
          alert('Registration failed');
        }
      }
    }
  };
  </script>