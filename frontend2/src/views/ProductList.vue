<template>
  <div class="container py-4">
    <h2 class="mb-4 text-center">精品鲜花</h2>
    <div class="row g-4">
      <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="product in products" :key="product.id">
        <div class="card h-100 shadow-sm product-card">
          <img
            :src="getProductImage(product)"
            class="card-img-top object-fit-cover"
            alt="商品图片"
            style="height: 200px; object-fit: cover;"
            @error="e => e.target.src = 'https://via.placeholder.com/300x200?text=No+Image'"
          >
          <div class="card-body d-flex flex-column">
            <h5 class="card-title text-truncate" :title="product.name">{{ product.name }}</h5>
            <p class="card-text text-muted small flex-grow-1">{{ product.description || '暂无描述' }}</p>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <span class="text-danger fw-bold fs-5">¥{{ product.price }}</span>
              <button class="btn btn-outline-primary btn-sm" @click="addToCart(product)">
                加入购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
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
  }
},
  mounted() {
    this.$store.dispatch('fetchProducts');
  }
};
</script>

<style scoped>
.product-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.product-card:hover {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.card-title {
  font-weight: 600;
}
</style>