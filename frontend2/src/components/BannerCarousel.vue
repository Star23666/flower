<template>
    <div id="carouselExampleIndicators" class="carousel slide mb-4" data-bs-ride="carousel" data-bs-interval="2500">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img :src="images[0]" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner1">
        </div>
        <div class="carousel-item">
          <img :src="images[1]" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner2">
        </div>
        <div class="carousel-item">
          <img :src="images[2]" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner3">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon"></span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>
  </template>
  
  <script setup>
  
  import banner1 from '@/assets/banner3.png'
  import banner2 from '@/assets/banner3.png'
  import banner3 from '@/assets/banner3.png'
  
  const images = [banner1, banner2, banner3]
  </script>