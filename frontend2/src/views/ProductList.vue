<template>
<!-- 轮播图 -->
<div id="carouselExampleIndicators" class="carousel slide mb-4" data-bs-ride="carousel" data-bs-interval="2500">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"></button>
  </div>
  <div class="carousel-inner" >
    <div class="carousel-item active" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner1">
      
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner2">
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner3">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
    <span class="carousel-control-next-icon"></span>
  </button>
</div>
  <div class="container py-4">
    <h2 class="mb-4 text-center">精品鲜花</h2>
    <div class="row row-cols-2 row-cols-md-4 g-3">
  <div class="col d-flex" v-for="product in products" :key="product.id">
    <div class="card h-100 shadow-sm product-card flex-fill" @click="goToDetail(product.id)" style="cursor:pointer;">
      <img
        :src="getProductImage(product)"
        class="card-img-top"
        alt="商品图片"
        style="height: 180px; object-fit: cover; border-radius: 0.5rem 0.5rem 0 0;"
        @error="e => e.target.src = 'https://via.placeholder.com/300x200?text=No+Image'"
      >
      <div class="card-body p-2">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="fw-bold text-truncate" :title="product.name">{{ product.name }}</span>
          <span class="text-danger fw-bold">¥{{ product.price }}</span>
        </div>
        <p class="card-text text-muted small mb-1" style="min-height:1.5em;">
          {{ product.category_id || '未知类型' }}
        </p>
        <div class="d-flex justify-content-end">
          <button class="btn btn-outline-primary btn-sm" @click.stop="addToCart(product)">加入购物车</button>
        </div>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script>
// import banner1 from '@/assets/compass.jpg'
// import banner2 from '@/assets/banner2.png'
import banner3 from '@/assets/banner3.png'
export default {
  data() {
    return {
      // banner1,
      // banner2,
      banner3,
    }
  },
  name: 'ProductList',

  computed: {
    products() {
      return this.$store.state.products;
    }
  },
  methods: {
    addToCart(product) {
      this.$store.commit('addToCart', product);
    },
    getProductImage(product) {
    // 如果 image_url 已经是完整 URL 或 /static 开头的相对路径
    if (product.image_url) {
      // 如果 image_url 不是完整 URL，则补全域名
      if (product.image_url.startsWith('http')) {
        return product.image_url;
      } else {
        return 'http://localhost:5000' + product.image_url;
      }
    }
    // 没有图片时用占位图
    return 'https://via.placeholder.com/300x200?text=No+Image';
  },
  goToDetail(id) {
    this.$router.push({ name: 'ProductDetail', params: { id } });
 }
},
  mounted() {
    this.$store.dispatch('fetchProducts');
  }
};
</script>

<style scoped>

.product-card {
  border-radius: 0.5rem;
  transition: box-shadow 0.2s, transform 0.2s;
}
.product-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  transform: translateY(-2px) scale(1.01);
}
.card-img-top {
  border-bottom: 1px solid #eee;
}

</style>