import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import ProductListPage from '../views/ProductList.vue';
import ShoppingCart from '../views/Cart.vue';
import UserLogin from '../views/Login.vue';
import UserRegister from '../views/Register.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/products', component: ProductListPage },
  { path: '/cart', component: ShoppingCart },
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;