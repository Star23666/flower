/* eslint-disable */
<template>
    <div class="container mt-5">
      <h2>添加新商品</h2>
      <form @submit.prevent="addProduct">
        <div class="mb-3">
          <label class="form-label">商品名称</label>
          <input v-model="form.name" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">价格</label>
          <input v-model.number="form.price" type="number" step="0.01" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">库存</label>
          <input v-model.number="form.stock" type="number" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">分类ID</label>
          <input v-model.number="form.category_id" type="number" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">描述</label>
          <textarea v-model="form.description" class="form-control"></textarea>
        </div>
        <div class="mb-3">
          <label class="form-label">图片URL</label>
          <input v-model="form.image_url" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">添加商品</button>
        <div v-if="message" class="alert mt-3" :class="{'alert-success': success, 'alert-danger': !success}">
          {{ message }}
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const form = ref({
    name: '',
    price: 0,
    stock: 0,
    category_id: 1,
    description: '',
    image_url: ''
  })
  
  const message = ref('')
  const success = ref(false)
  
  const addProduct = async () => {
    try {
      const token = localStorage.getItem('token')
       await axios.post('http://localhost:5000/api/seller/products', form.value, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      message.value = '商品添加成功！'
      success.value = true
      // 清空表单
      form.value = {
        name: '',
        price: 0,
        stock: 0,
        category_id: 1,
        description: '',
        image_url: ''
      }
    } catch (err) {
      message.value = err.response?.data?.message || '添加失败'
      success.value = false
    }
  }
  </script>