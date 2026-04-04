product<template>
  <div class="product-list-page">
    <!-- 头部轮播图区域 -->
    <div class="banner-section">
  <el-carousel :interval="4000" type="card" height="360px">
    
    <!-- 第一张： 使用 Picsum id/129 (比较温馨自然) -->
    <el-carousel-item>
      <div class="banner-item">
        <img src="https://picsum.photos/id/129/1200/500" alt="Banner 1" class="banner-img" />
        <div class="banner-overlay">
          <h3>Flower & Life</h3>
          <p>为您精选每一束浪漫</p>
        </div>
      </div>
    </el-carousel-item>

    <!-- 第二张： 使用 Picsum id/28 (森林与花，非常清新) -->
    <el-carousel-item>
      <div class="banner-item">
        <img src="https://picsum.photos/id/28/1200/500" alt="Banner 2" class="banner-img" />
        <div class="banner-overlay">
          <h3>Flower & Life</h3>
          <p>自然与艺术的完美融合</p>
        </div>
      </div>
    </el-carousel-item>

    <!-- 第三张： 使用 Picsum id/292 (食材与静物，有生活气息) -->
    <el-carousel-item>
      <div class="banner-item">
        <img src="https://picsum.photos/id/292/1200/500" alt="Banner 3" class="banner-img" />
        <div class="banner-overlay">
          <h3>Flower & Life</h3>
          <p>每一天都值得被盛开</p>
        </div>
      </div>
    </el-carousel-item>

  </el-carousel>
</div>

    <!-- 主内容区 -->
    <div class="main-content container-xl">
      
      <!-- 搜索与筛选工具栏 -->
      <div class="filter-tool-bar glass-card mb-4">
        <el-form :inline="true" :model="search" class="search-form">
          <!-- 名称搜索 -->
          <el-form-item label="名称">
            <el-input 
              v-model="search.name" 
              placeholder="搜索花名..." 
              prefix-icon="Search" 
              clearable 
              style="width: 180px;"
            />
          </el-form-item>

          <!-- 类别下拉选择 -->
          <el-form-item label="类别">
            <el-select v-model="search.category" placeholder="全部类别" clearable style="width: 150px">
              <el-option label="全部" value="" />
              <el-option 
                v-for="cat in categories" 
                :key="cat.id" 
                :label="cat.name" 
                :value="cat.id" 
              />
            </el-select>
          </el-form-item>

          <!-- 价格区间筛选 -->
          <el-form-item label="价格">
             <div class="price-range">
                <el-input-number 
                  v-model="search.minPrice" 
                  :min="0" :controls="false" 
                  placeholder="Min" 
                  style="width: 80px" 
                />
                <span class="separator">-</span>
                <el-input-number 
                  v-model="search.maxPrice" 
                  :min="0" :controls="false" 
                  placeholder="Max" 
                  style="width: 80px" 
                />
             </div>
          </el-form-item>

          <!-- 按钮组 -->
          <el-form-item>
            <el-button type="primary" @click="onSearch" icon="Search" round color="#ff758c">查询</el-button>
            <el-button @click="resetSearch" icon="Refresh" circle></el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 商品列表网格 -->
      <div v-if="filteredProducts.length > 0">
        <el-row :gutter="24">
          <el-col 
            v-for="product in filteredProducts" 
            :key="product.id" 
            :xs="24" :sm="12" :md="8" :lg="6"
            class="mb-4"
          >
            <!-- 单个商品卡片 -->
            <div class="custom-card product-card" @click="goToDetail(product.id)">
              
              <!-- 图片区域 -->
              <div class="image-wrapper">
                <img 
                  :src="getProductImage(product)" 
                  class="product-image"
                  @error="handleImageError"
                  alt="商品图片"
                />
                <div class="hover-overlay">
                  <el-button type="primary" icon="View" round>查看详情</el-button>
                </div>
                <div class="category-badge">
                  {{ getCategoryName(product.category_id) }}
                </div>
              </div>

              <!-- 内容区域 -->
              <div class="card-body">
                <div class="product-info">
                  <h5 class="product-title" :title="product.name">{{ product.name }}</h5>
                  <p class="product-desc text-muted text-truncate">
                    {{ product.description || '暂无描述' }}
                  </p>
                </div>
                
                <div class="product-footer">
                  <span class="price">
                    <span class="symbol">¥</span> 
                    <span class="amount">{{ product.price }}</span>
                  </span>
                  <el-button 
                    type="primary" 
                    icon="ShoppingCart" 
                    circle 
                    size="small" 
                    plain 
                    @click.stop="addToCart(product)"
                  ></el-button>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div v-else class="empty-state container">
        <el-empty description="没有找到符合条件的商品~" :image-size="200"></el-empty>
      </div>

    </div>
  </div>
</template>

<script>
// 【修改点1】移除了 icon 的引入，因为 main.js 已经全局注册了

export default {
  name: 'ProductList', 
  // 【修改点2】移除了 components: { ... } 注册块
  data() {
    return {
      categories: [],
      search: {
        name: '',
        category: '',
        minPrice: undefined,
        maxPrice: undefined
      }
    }
  },
  
  computed: {
    filteredProducts() {
      let products = this.$store.state.products.filter(p => p.status !== 'inactive');
      
      return products.filter(p => {
        if (this.search.name && !p.name.includes(this.search.name)) return false;
        if (this.search.category && String(p.category_id) !== String(this.search.category)) return false;
        if (this.search.minPrice !== undefined && p.price < this.search.minPrice) return false;
        if (this.search.maxPrice !== undefined && p.price > this.search.maxPrice) return false;
        return true;
      });
    }
  },

  methods: {
    async fetchCategories(){
      try{
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:5000/api/categories', {
          headers: {
            'Authorization': 'Bearer ' + token
          }
        });
        const data = await res.json();
        this.categories = Array.isArray(data) ? data : []; 
      } catch (e){
        console.error('加载分类失败', e);
        this.categories = [];
      }
    },

    onSearch(){
      console.log('执行筛选:', this.search);
    },

    resetSearch() {
      this.search = {
        name: '',
        category: '',
        minPrice: undefined,
        maxPrice: undefined
      };
    },

    addToCart(product) {
      this.$store.commit('addToCart', product);
      this.$message.success(`已加入购物车: ${product.name}`);
    },

    getProductImage(product) {
      if (product.image_url) {
        if (product.image_url.startsWith('http')) {
          return product.image_url;
        } else {
          return 'http://localhost:5000' + product.image_url;
        }
      }
      return 'https://via.placeholder.com/300x200?text=No+Image';
    },

    handleImageError(e) {
      e.target.src = 'https://via.placeholder.com/300x200?text=Error';
    },

    goToDetail(id) {
      this.$router.push({ name: 'ProductDetail', params: { id } });
    },

    getCategoryName(id) {
      const cat = this.categories.find(c => c.id === id);
      return cat ? cat.name : '精选';
    }
  },

  mounted() {
    this.$store.dispatch('fetchProducts');
    this.fetchCategories();
  }
};
</script>

<style scoped>
.product-list-page {
  padding-bottom: 60px;
}

.banner-section {
  padding-top: 20px;
  margin-bottom: 30px;
}

.banner-item {
  position: relative;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
  color: white;
  padding: 20px;
  text-align: center;
}

.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.price-range {
  display: flex;
  align-items: center;
}

.separator {
  margin: 0 8px;
  color: #999;
}

.custom-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.custom-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
  border-color: #ff758c;
}

.image-wrapper {
  position: relative;
  height: 220px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.custom-card:hover .product-image {
  transform: scale(1.08); 
}

.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.custom-card:hover .hover-overlay {
  opacity: 1;
}

.category-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  backdrop-filter: blur(4px);
}

.card-body {
  padding: 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-desc {
  font-size: 0.85rem;
  margin-bottom: 15px;
  height: 20px;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.price {
  color: #ff758c;
  font-weight: bold;
}

.price .symbol {
  font-size: 0.9rem;
}

.price .amount {
  font-size: 1.3rem;
}

@media (max-width: 768px) {
  .banner-section {
    display: none;
  }
  .image-wrapper {
    height: 180px;
  }
}
</style>