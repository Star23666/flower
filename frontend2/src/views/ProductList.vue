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
      <img :src="banner3" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner1">
      
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner2">
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:400px;object-fit:cover;" alt="banner3">
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
  <!-- 检索内容表单 -->
  <form class="row g-2 align-items-center mb-4 bg-light p-3 rounded shadow-sm" @submit.prevent="onSearch">
  <div class="col-6 col-md-auto">
    <div class="input-group input-group-sm">
      <span class="input-group-text"><i class="bi bi-search"></i> 名称</span>
      <input type="text" class="form-control" v-model="search.name">
    </div>
  </div>
  <div class="col-6 col-md-auto">
    <div class="input-group input-group-sm">
      <span class="input-group-text"><i class="bi bi-flower1"></i> 类别</span>
      <select class="form-select" v-model="search.category">
        <option value="">全部</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
    </div>
  </div>
  <!-- 其它下拉/输入框同理 -->
  <div class="col-12 col-md-auto">
    <div class="input-group input-group-sm">
      <span class="input-group-text">价格</span>
      <input type="number" class="form-control" style="width: 70px;" v-model.number="search.minPrice" placeholder="最小">
      <span class="input-group-text">-</span>
      <input type="number" class="form-control" style="width: 70px;" v-model.number="search.maxPrice" placeholder="最大">
    </div>
  </div>
  <div class="col-12 col-md-auto">
    <button class="btn btn-primary btn-sm w-100" type="submit">
      <i class="bi bi-search"></i> 查询
    </button>
  </div>
</form>
    <div class="row row-cols-2 row-cols-md-4 g-3">
  <div class="col d-flex" v-for="product in filteredProducts" :key="product.id">
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
          {{ categories.find(c => c.id === product.category_id)?.name || '未知类型' }}
        </p>
        <!-- <div class="d-flex justify-content-end">
          <button @click="handleAddToCart(product)">加入购物车</button>
        </div> -->
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script>
import banner3 from '@/assets/banner3.png'
export default {
  data() {
    return {
      // banner1,
      // banner2,
      banner3,
      categories:[],
      search:{
        name:'',
        flower_language:'',
        category:'',
        scene:'',
        target:'',
        minPrice:'',
        maxPrice:''
      }
      
    }
  },
  name: 'ProductList',

  computed: {
    filteredProducts() {
    return this.products.filter(p => {
      if (this.search.name && !p.name.includes(this.search.name)) return false;
      if (this.search.flower_language && !(p.flower_language || '').includes(this.search.flower_language)) return false;
      if (this.search.category && !(p.category_id || '').toString().includes(this.search.category)) return false;
      if (this.search.scene && !(p.scene || '').includes(this.search.scene)) return false;
      if (this.search.target && !(p.target || '').includes(this.search.target)) return false;
      if (this.search.minPrice && p.price < this.search.minPrice) return false;
      if (this.search.maxPrice && p.price > this.search.maxPrice) return false;
      return true;
    });
  },
    products() {
      // 过滤掉 is_active 为 inactive(下架) 的商品
      return this.$store.state.products.filter(p => p.status !=='inactive');  
    }
  },
  methods: {

  //   handleAddToCart(product) {
  //   this.$store.commit('addToCart', product);
  // },
    
    // 获取分类
    async fetchCategories(){
  try{
    const token = localStorage.getItem('token');
    const res = await fetch('http://localhost:5000/api/categories', {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    });
    const data = await res.json();
    this.categories = data;
  }catch (e){
    this.categories = [];
  }
},
    onSearch(){
      this.$store.dispatch('fetchProducts', this.search);
    },
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
    this.fetchCategories();

    this.$nextTick(() => {
    // 重新初始化 Bootstrap Carousel
      const carouselEl = document.getElementById('carouselExampleIndicators');
      if (window.bootstrap && carouselEl) {
        window.bootstrap.Carousel.getOrCreateInstance(carouselEl);
      }
    });
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