import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    cart: [],
    products: [],
    categories: [],
    sellerProducts:[],
    users:[],
    orders: []
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setProducts(state, products) {
      state.products = products;
    },
    setCategories(state, list) {
      state.categories = list;
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
    setUsers(state, users) {
      state.users = users;
    },
    setOrders(state, orders) {
      state.orders = orders;
    },
  },
  actions: {
    async fetchCategories({ commit }) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/api/categories', {
          headers: { Authorization: `Bearer ${token}` }
        });
        commit('setCategories', response.data);
      } catch (error) {
        console.error('获取分类失败:', error);
      }
    },
    async fetchProducts({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/products');
        const data = await response.json()
        commit('setProducts',data);
      } catch (error) {
        console.error('获取商品失败:', error);
        
      }
    },
    async addCategory(_, payload) {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.post('http://localhost:5000/api/categories', payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        return res.data
      } catch (error) {
        // 统一错误处理，可直接抛出或自定义错误信息
        throw new Error(error.response?.data?.message || '新增分类失败')
      }
    },
 
    async updateCategory(_, category) {
      const token = localStorage.getItem('token')
      const res = await fetch(`http://localhost:5000/api/categories/${category.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json',
          Authorization:`Bearer ${token}` },
        body: JSON.stringify(category)
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.message || '编辑失败')
      }
    },
    async deleteCategory(_, id) {
      const token = localStorage.getItem('token')
      const res = await fetch(`http://localhost:5000/api/categories/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.message || '删除失败')}
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
        const msg = error.response?.data?.message || '删除失败';
        throw new Error(msg);
      }
    },
    
    async login({ commit }, { username, password, type = 'user' }) {
      try {
        // 根据 type 选择接口1
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
        throw new Error('登录失败');
      }
    },
    async register(_, credentials) {
      try {
        await axios.post('http://localhost:5000/api/auth/register', credentials);
      } catch (error) {
        throw new Error('注册失败');
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
    },
    async fetchUsers({ commit }, searchText = '') {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users', {
        params: { search: searchText },
        headers: { Authorization: `Bearer ${token}` }
      });
      commit('setUsers', response.data);
    },
    async deleteUser(_, userId) {



      console.log('deleteUser action', userId)
      const res = await fetch(`http://localhost:5000/api/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
      })
      const data = await res.json()
      if (!res.ok) {
    throw new Error(data.message || '删除失败')
      }
    },
    // 更新用户信息
    async updateUser(_, user) {
      console.log('updateUser action', user)
      const res = await fetch(`http://localhost:5000/api/users/${user.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(user)
      })
      console.log('fetch返回', res.status)
      const data = await res.json()
      if (!res.ok) {
    throw new Error(data.message || '保存失败')
      }
    },
    async fetchOrders({ commit }) {
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:5000/api/orders', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('获取订单失败')
      const data = await res.json()
      commit('setOrders', data)
    },
  }
});