<template>
    <div class="container">
      <h2>Seller Login</h2>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'SellerLogin',
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://localhost:5000/api/seller/login', {
            username: this.username,
            password: this.password
          });
          localStorage.setItem('token', response.data.access_token);
          localStorage.setItem('user', JSON.stringify({
            username: response.data.username,
            role: response.data.role
          }));
          this.$store.commit('setUser', {
            username: response.data.username,
            role: response.data.role
          });
          this.$router.push('/products');
        } catch (error) {
          alert('Login failed');
        }
      }
    }
  };
  </script>