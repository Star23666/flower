<template>
  <div class="container">
    <h2>商品名称</h2>
    <div class="row">
      <div v-for="product in products" :key="product.id" class="col-md-4">
        <div class="card">
          <img :src="product.image_url" class="card-img-top" alt="Product Image">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">${{ product.price }}</p>
            <button class="btn btn-primary" @click="addToCart(product)">加入购物车</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductListPage',
  computed: {
    products() {
      return this.$store.state.products;
    }
  },
  methods: {
    addToCart(product) {
      this.$store.commit('addToCart', product);
    }
  },
  mounted() {
    this.$store.dispatch('fetchProducts');
  }
};
</script>