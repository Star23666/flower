import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index';
import store from './store/index';
import 'element-plus/dist/index.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import ElementPlus from 'element-plus'

// 可以在 main.js 里加如下代码，屏蔽这个警告（仅开发环境用）：
const observerErr = /ResizeObserver loop (limit|completed)/
const realError = window.onerror
window.onerror = function (msg, ...args) {
  if (observerErr.test(msg)) return true
  return realError && realError(msg, ...args)
}

const user = JSON.parse(localStorage.getItem('user'));
if (user) {
  store.commit('setUser', user);
}
const app = createApp(App);
app.use(router);
app.use(store);
app.use(ElementPlus)
app.mount('#app');