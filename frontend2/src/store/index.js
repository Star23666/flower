import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    cart: [],
    products: [],
    categories: [],
    sellerProducts:[]
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setProducts(state, products) {
      state.products = products;
    },
    setCategories(state, categories) {
      state.categories = categories;
    },
    addToCart(state, product) {
      const item = state.cart.find(i => i.id === product.id);
      if (item) {
        item.quantity++;
      } else {
        state.cart.push({ ...product, quantity: 1 });
      }
    },
    setSellerProducts(state, products) {
      state.sellerProducts = products;
    },

  },
  actions: {
    async fetchProducts({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/products');
        commit('setProducts', response.data);
      } catch (error) {
        console.error('获取商品失败:', error);
        
      }
    },
    async fetchCategories({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/categories');
        commit('setCategories', response.data);
      } catch (error) {
        console.error('获取分类失败:', error);
      }
    },
    async fetchSellerProducts({ commit }) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/api/seller/products', {
          headers: { Authorization: `Bearer ${token}` }
        });
        commit('setSellerProducts', response.data);
      } catch (error) {
        console.error('获取商家商品失败', error);
      }
    },

    // 添加商品
    async addProduct({ dispatch }, product) {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://localhost:5000/api/seller/products', product, {
          headers: { Authorization: `Bearer ${token}` }
        });
        // 添加成功后刷新商家商品列表
        dispatch('fetchSellerProducts');
      } catch (error) {
        throw new Error('添加商品失败');
      }
    },
  
    // 更新商品
    async updateProduct({ dispatch }, product) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://localhost:5000/api/seller/products/${product.id}`, product, {
          headers: { Authorization: `Bearer ${token}` }
        });
        dispatch('fetchSellerProducts');
      } catch (error) {
        throw new Error('更新商品失败');
      }
    },
  
    // 删除商品
    async deleteProduct({ dispatch }, productId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:5000/api/seller/products/${productId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        dispatch('fetchSellerProducts');
      } catch (error) {
        throw new Error('删除商品失败');
      }
    },
    async login({ commit }, { username, password, type = 'user' }) {
      try {
        // 根据 type 选择接口
        const url =
          type === 'seller'
            ? 'http://localhost:5000/api/seller/login'
            : 'http://localhost:5000/api/auth/login';
    
        const response = await axios.post(url, { username, password });
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify({
          username: response.data.username,
          role: response.data.role
        }));
        commit('setUser', {
          username: response.data.username,
          role: response.data.role
        });
      } catch (error) {
        throw new Error('Login failed');
      }
    },
    async register(_, credentials) {
      try {
        await axios.post('http://localhost:5000/api/auth/register', credentials);
      } catch (error) {
        throw new Error('Registration failed');
      }
    },
    async createOrder({ state }) {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://localhost:5000/api/orders', {
          items: state.cart.map(item => ({ product_id: item.id, quantity: item.quantity }))
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        state.cart = []; // Clear cart
      } catch (error) {
        throw new Error('下单失败');
      }
    }
  }
});