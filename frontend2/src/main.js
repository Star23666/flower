import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index';
import store from './store/index';
import 'element-plus/dist/index.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import ElementPlus from 'element-plus'
// main.js 或 store/index.js
const user = JSON.parse(localStorage.getItem('user'));
if (user) {
  store.commit('setUser', user);
}
const app = createApp(App);
app.use(router);
app.use(store);
app.use(ElementPlus)
app.mount('#app');