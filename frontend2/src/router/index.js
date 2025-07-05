import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import ProductListPage from '../views/ProductList.vue';
import ShoppingCart from '../views/Cart.vue';
import UserLogin from '../views/UserLogin.vue';
import UserRegister from '../views/UserRegister.vue';
import AddProduct from '../views/AddProduct.vue';
import SellerLogin from '../views/SellerLogin.vue';
const routes = [
  { path: '/', component: UserLogin },
  { path: '/home', component: HomePage },
  { path: '/products', component: ProductListPage },
  { path: '/cart', component: ShoppingCart },
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/add-product', component: AddProduct },
  { path: '/seller/login', component: SellerLogin },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫：未登录用户只能访问登录、注册等公开页面
router.beforeEach((to, from, next) => {
  // 允许匿名访问的路由
  const publicPages = ['/', '/login', '/register', '/seller/login'];
  // 检查本地存储是否有 token
  const isLoggedIn = !!localStorage.getItem('token');

  // 如果访问的是公开页，直接放行
  if (publicPages.includes(to.path)) {
    return next();
  }

  // 如果没登录，强制跳转到登录页
  if (!isLoggedIn) {
    return next('/login');
  }

  // 其它情况放行
  next();
});


export default router;