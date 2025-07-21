<template>
    <el-menu
      default-active="product"
      class="el-menu-vertical-demo"
      background-color="#2d3a4b"
      text-color="#fff"
      active-text-color="#ffd04b"
      router
    >
      <el-menu-item index="/seller/users"><i class="el-icon-user"></i> 用户管理</el-menu-item>
      <el-menu-item index="/seller/flower-categories"><i class="el-icon-menu"></i> 鲜花分类</el-menu-item>
      <el-menu-item index="/seller/products"><i class="el-icon-goods"></i> 商品管理</el-menu-item>
      <el-menu-item index="/seller/orders"><i class="el-icon-tickets"></i> 订单管理</el-menu-item>
      <el-menu-item index="/seller/profile"><i class="el-icon-setting"></i> 个人中心</el-menu-item>
      <el-menu-item index="/login"><i class="el-icon-plus"></i> 退出登录</el-menu-item>
    </el-menu>
  </template>
  
  <script setup>
  // 可根据需要添加props
  </script>
  
  <style scoped>
  .el-menu-vertical-demo {
    width: 100px;
    min-height: 100vh;
  }
  </style>