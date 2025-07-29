<script setup>
import BannerCarousel from '@/components/BannerCarousel.vue'
</script>
<template>
  <div>
    <BannerCarousel />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>