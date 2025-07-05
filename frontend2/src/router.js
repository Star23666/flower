import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import ProductList from './views/ProductList.vue';
import Cart from './views/Cart.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/products', component: ProductList },
  { path: '/cart', component: Cart },
  { path: '/login', component: Login },
  { path: '/register', component: Register }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;