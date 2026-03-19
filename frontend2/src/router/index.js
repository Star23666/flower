/* eslint-disable */
import { createRouter, createWebHistory } from 'vue-router';
// ... 保持您的 imports 不变 ...
import HomePage from '../views/HomePage.vue';
import ProductListPage from '../views/ProductList.vue';
import ShoppingCart from '../views/Cart.vue';
import UserLogin from '../views/UserLogin.vue';
import UserRegister from '../views/UserRegister.vue';
// import AddProduct from '../views/AddProduct.vue'; // 删除未使用的引用
import SellerLogin from '../views/SellerLogin.vue';
import SellerDashboard from '@/views/SellerDashboard.vue';
import ProductManage from '@/views/seller/ProductManage.vue';
import OrderManage from '@/views/seller/OrderManage.vue';
import UserManage from '@/views/seller/UserManage.vue';
import Profile from '@/views/seller/SellerProfile.vue';
import FlowerCategoryManage from '@/views/seller/FlowerCategoryManage.vue';
import UserProfile from '@/views/UserProfile.vue';
import OrderList from '@/views/OrderList.vue';
import MainLayout from '@/views/MainLayout.vue';
import AboutUs from '@/views/AboutUs.vue';
// ... 如果有 ProductDetail 懒加载 import，这里不需要改 ...

const routes = [
  // 1. 根路径重定向：已登录去首页，未登录去登录页
  {
    path: '/',
    redirect: () => { // 删掉 'to' 参数
        return localStorage.getItem('token') ? '/home' : '/login'
    }
  },
  
  // 2. 公开页面
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/seller/login', component: SellerLogin },

  // 3. 商家后台（需要权限）
  {
    path: '/seller',
    component: SellerDashboard,
    meta: { requiresSeller: true },
    children: [
      { path: '', redirect: '/seller/products' }, // 默认跳商品管理
      { path: 'products', component: ProductManage, meta: { requiresSeller: true, breadcrumb: '商品'} },
      { path: 'orders', component: OrderManage, meta: { requiresSeller: true, breadcrumb: '订单'} },
      { path: 'users', component: UserManage, meta: { requiresSeller: true, breadcrumb: '用户'} },
      { path: 'profile', component: Profile, meta: { requiresSeller: true, breadcrumb: '商家信息'} },
      { path: 'flower-categories', component: FlowerCategoryManage, meta: { requiresSeller: true, breadcrumb: '花材分类'} },
    ]
  },

  // 4. 买家前台布局（包含头部导航）
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: 'home', component: HomePage }, // /home
      { path: 'products', component: ProductListPage }, // /products
      { path: 'product/:id', name: 'ProductDetail', component: () => import('@/views/ProductDetail.vue') },
      { path: 'cart', component: ShoppingCart, meta: { requiresAuth: true } }, // 购物车通常需要登录
      { path: 'order-list', component: OrderList, meta: { requiresAuth: true } },
      { path: 'user/profile', component: UserProfile, meta: { requiresAuth: true } },
      { path: 'about', component: AboutUs },
    ]
  },
  
  // 5. 捕获所有未匹配路径（404）
  { 
    path: '/:pathMatch(.*)*', 
    redirect: '/home' 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  // === 新增：滚动行为控制 ===
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' } 
    }
  }
});

// --- 路由守卫修正版 ---
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  // 必须同时有 token 和 user 信息才算作“有效登录”
  const isLoggedIn = !!token && !!user;

  // 定义公开路径（不需要登录也能访问）
  const publicPaths = ['/login', '/register', '/seller/login'];
  // 其他公开页面也包含在内，或者下面逻辑覆盖
  
  // 1. 如果去的是 登录/注册页
  if (publicPaths.includes(to.path)) {
    // 【修改点】：不再强制踢回首页
    // 允许用户访问登录页，即使他有 token（可能是为了切换账号）
    // 为了避免状态混乱，我们可以顺便清理一下旧状态，或者直接放行
    if (isLoggedIn) {
        // 可选：如果已登录去登录页，这里可以选择清除旧 token，让用户重新登录
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        // store.commit('logout') // 如果能访问 store
    }
    return next();
  }

  // 2. 如果去的是其他公开页面 (Home, Products, About)
  // 不需要 meta.requiresAuth 的页面直接放行
  if (!to.meta.requiresAuth && !to.meta.requiresSeller) {
      return next();
  }

  // 3. 如果未登录，去受保护页面 -> 跳转登录
  if (!isLoggedIn) {
    if (to.path.startsWith('/seller')) {
        return next('/seller/login');
    }
    return next(`/login?redirect=${to.fullPath}`);
  }

  // 4. 已登录，检查商家权限
  if (to.matched.some(record => record.meta.requiresSeller)) {
    if (user && user.role === 'seller') {
      return next();
    } else {
      // 没权限，踢回买家首页
      return next('/home');
    }
  }

  // 5. 其他情况（买家需登录的页面，且已登录）
  next();
});

export default router;