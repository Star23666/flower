<template>
    <div class="seller-dashboard">
      <SellerSidebar />
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </template>
  
  <script setup>
  import SellerSidebar from '@/components/SellerSidebar.vue'
  </script>
  
  <style scoped>
  .seller-dashboard {
    display: flex;
    height: 100vh;
  }
  .main-content {
    flex: 1;
    background: #f5f6fa;
    padding: 24px;
    overflow: auto;
  }
  </style>