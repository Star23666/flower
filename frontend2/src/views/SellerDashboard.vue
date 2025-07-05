<template>
    <div class="container">
      <h2>商家仪表板</h2>
      <h3>商品管理</h3>
      <form @submit.prevent="addProduct" class="mb-4">
        <div class="mb-3">
          <label for="name" class="form-label">商品名称</label>
          <input v-model="newProduct.name" type="text" class="form-control" id="name" required>
        </div>
        <div class="mb-3">
          <label for="price" class="form-label">价格</label>
          <input v-model.number="newProduct.price" type="number" class="form-control" id="price" required>
        </div>
        <div class="mb-3">
          <label for="stock" class="form-label">库存</label>
          <input v-model.number="newProduct.stock" type="number" class="form-control" id="stock" required>
        </div>
        <div class="mb-3">
          <label for="category" class="form-label">分类</label>
          <select v-model="newProduct.category_id" class="form-control" id="category" required>
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">描述</label>
          <textarea v-model="newProduct.description" class="formPers-control" id="description"></textarea>
        </div>
        <div class="mb-3">
          <label for="image_url" class="form-label">图片URL</label>
          <input v-model="newProduct.image_url" type="text" class="form-control" id="image_url">
        </div>
        <button type="submit" class="btn btn-primary">添加商品</button>
      </form>
  
      <h3>我的商品</h3>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>价格</th>
            <th>库存</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in sellerProducts" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.price }}</td>
            <td>{{ product.stock }}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="editProduct(product)">编辑</button>
              <button class="btn btn-danger btn-sm" @click="deleteProduct(product.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <h3>我的订单</h3>
      <table class="table">
        <thead>
          <tr>
            <th>订单ID</th>
            <th>用户ID</th>
            <th>创建时间</th>
            <th>商品</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in sellerOrders" :key="order.id">
            <td>{{ order.id }}</td>
            <td>{{ order.user_id }}</td>
            <td>{{ order.created_at }}</td>
            <td>
              <ul>
                <li v-for="item in order.items" :key="item.product_id">
                  商品ID: {{ item.product_id }}, 数量: {{ item.quantity }}
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SellerDashboard',
    data() {
      return {
        newProduct: {
          name: '',
          price: 0,
          stock: 0,
          category_id: null,
          description: '',
          image_url: ''
        }
      };
    },
    computed: {
      categories() {
        return this.$store.state.categories;
      },
      sellerProducts() {
        return this.$store.state.sellerProducts;
      },
      sellerOrders() {
        return this.$store.state.sellerOrders;
      }
    },
    methods: {
      async addProduct() {
        try {
          await this.$store.dispatch('addProduct', this.newProduct);
          alert('商品添加成功');
          this.newProduct = { name: '', price: 0, stock: 0, category_id: null, description: '', image_url: '' };
        } catch (error) {
          alert('商品添加失败：' + error.message);
        }
      },
      async editProduct(product) {
        const updatedProduct = { ...product };
        try {
          await this.$store.dispatch('updateProduct', updatedProduct);
          alert('商品更新成功');
        } catch (error) {
          alert('商品更新失败：' + error.message);
        }
      },
      async deleteProduct(productId) {
        if (confirm('确定删除此商品？')) {
          try {
            await this.$store.dispatch('deleteProduct', productId);
            alert('商品删除成功');
          } catch (error) {
            alert('商品删除失败：' + error.message);
          }
        }
      }
    },
    mounted() {
      this.$store.dispatch('fetchCategories');
      this.$store.dispatch('fetchSellerProducts');
      this.$store.dispatch('fetchSellerOrders');
    }
  };
  </script>