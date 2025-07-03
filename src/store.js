import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    cart: [],
    products: [],
    categories: []
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
    }
  },
  actions: {
    async fetchProducts({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/products');
        commit('setProducts', response.data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    },
    async fetchCategories({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/categories');
        commit('setCategories', response.data);
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    },
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('http://localhost:5000/api/auth/login', credentials);
        localStorage.setItem('token', response.data.access_token);
        commit('setUser', credentials.username);
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
        throw new Error('Order creation failed');
      }
    }
  }
});