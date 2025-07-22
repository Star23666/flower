<template>
  <!-- 面包屑导航 -->
  <nav aria-label="breadcrumb" class="mt-3 ms-3">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <router-link to="/products">商品</router-link>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      {{ product ? (product.name || '鲜花详情') : '鲜花详情' }}
    </li>
  </ol>
</nav>
    <div class="container py-4">
      <div v-if="product" class="row">
        <!-- 左侧图片，可用轮播 -->
        <div class="col-md-6 text-center">
          <img :src="getProductImage(product)" class="img-fluid rounded shadow-sm" style="max-height:420px;">
        </div>
        <!-- 右侧详情 -->
        <div class="col-md-6">
          <h2 class="mb-3">{{ product.name }}</h2>
          <div class="mb-3 fs-4 text-danger">¥{{ product.price }}</div>
          <table  class="table table-borderless mb-3" style="width:auto">
            <tbody>
              <tr>
                <td class="text-secondary">鲜花类型</td>
                <td>
                {{ categories && categories.find ? (categories.find(c => c.id === product.category_id)?.name || '暂无') : '暂无' }}
                </td>
              </tr>
              <tr>
                <td class="text-secondary">鲜花花语</td>
                <td>{{ product.flower_language || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">鲜花花语</td>
                <td>{{ product.flower_language2 || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">鲜花产地</td>
                <td>{{ product.origin || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">适用场景</td>
                <td>{{ product.scene || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">适用对象</td>
                <td>{{ product.target || '暂无' }}</td>
              </tr>
              <tr>
                <td class="text-secondary">点击次数</td>
                <td>{{ product.click_count || 0 }}</td>
              </tr>
            </tbody>
          </table>
          <!-- 操作区 -->
          <div class="d-flex align-items-center mb-3">
            <input
              type="number"
              min="1"
              :max="product.stock"
              class="form-control mx-2"
              style="width: 80px; text-align: center;"
              v-model.number="quantity"
            >
            <button class="btn btn-success me-2" @click="addToCart">加入到购物车</button>
            <button class="btn btn-warning">立即购买</button>
          </div>
        </div>
      </div>
      <!-- 下面可以加选项卡、评论等 -->
      <div v-else>加载中...</div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return { 
        product: null,
        quantity:1,
        categories:[]
    }
    },
    mounted() {
      const id = this.$route.params.id;
      this.fetchProduct(id);
      this.fetchCategories();
  },
    methods: {
      // 获取分类
      async fetchCategories() {

        try {
          // 获取token
          const token = localStorage.getItem('token');
          const res = await fetch('http://localhost:5000/api/categories', {
            headers: {
              'Authorization': 'Bearer ' + token
            }
          });
          const data = await res.json();
          this.categories = data;
        } catch (e) {
          this.categories = [];
        }
      },
      async fetchProduct(id) {
        // 建议后端提供 /api/products/:id 接口
        const res = await fetch(`http://localhost:5000/api/products/${id}`);
        this.product = await res.json();
      },
      getProductImage(product) {
      if (!product || !product.image_url) {
        return 'https://via.placeholder.com/400x300?text=No+Image';
      }
      if (product.image_url.startsWith('http')) return product.image_url;
      return 'http://localhost:5000' + product.image_url;
    },
    increaseQty() {
    this.quantity++;
  },
    decreaseQty() {
    if (this.quantity > 1) this.quantity--;
  },
    addToCart() {

    // 防止非法输入
    if (this.quantity < 1) this.quantity = 1;
    if (this.quantity > this.product.stock) {
        this.quantity = this.product.stock;
        this.$message && this.$message.warning
        ? this.$message.warning('库存不足')
        : alert('不能超过库存');
        return;
    }
    // this.product 已经是当前详情
    this.$store.commit('addToCart', { ...this.product, quantity: this.quantity });
    // 可选：弹出提示
    this.$message && this.$message.success
      ? this.$message.success('已加入购物车')
      : alert('已加入购物车');
    }
    }
  }
  </script>