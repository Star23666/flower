<script>
export default {
  // 改名为 CartPage 以符合 multi-word-component-names 规则
  name: 'CartPage'
}
</script>

<template>
  <div class="cart-page">
    <!-- 支付成功弹窗 -->
    <!-- <el-dialog v-model="showPaySuccessModal" title="支付成功" width="400px" center destroy-on-close :show-close="false">
      <div class="pay-success-content">
        <el-icon class="success-icon"><CircleCheckFilled /></el-icon>
        <p class="success-title">您的订单已支付成功！</p>
        <p class="success-desc">我们将尽快为您发货</p>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showPaySuccessModal = false">继续逛逛</el-button>
          <el-button type="primary" @click="toOrderList">查看我的订单</el-button>
        </div>
      </template>
    </el-dialog> -->

    <!-- 顶部轮播图展示区 (仅在购物车模式显示) -->
    <div class="cart-banner-section" v-if="!showOrderList">
       <el-carousel :interval="5000" type="card" height="200px">
        <el-carousel-item>
          <div class="promo-card bg-gradient-1">
             <h3>春季新品 🌸 限时特惠</h3>
             <p>满199减30</p>
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="promo-card bg-gradient-2">
             <h3>玫瑰花束 🌹 浪漫首选</h3>
             <p>送给最爱的人</p>
          </div>
        </el-carousel-item>
         <el-carousel-item>
          <div class="promo-card bg-gradient-3">
             <h3>会员专属 🎁 积分兑换</h3>
             <p>更多好礼等你来拿</p>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 订单列表视图 -->
    <transition name="fade-slide" mode="out-in">
    <div v-if="showOrderList" class="order-list-container" key="orderList">
       <div class="section-header">
         <el-button link @click="showOrderList = false" class="back-link">
           <el-icon><ArrowLeft /></el-icon> 返回购物车
         </el-button>
         <h2>我的订单</h2>
       </div>
       <OrderList :orders="orderList" @backToCart="showOrderList = false" />
    </div>

    <!-- 购物车主视图 -->
    <div v-else class="cart-main-container" key="cart">
      <div class="section-header">
        <div class="header-left">
          <h2>购物车</h2>
          <span class="cart-count-badge" v-if="cart.length > 0">{{ cart.length }}</span>
        </div>
        <el-button type="danger" link v-if="cart.length > 0" @click="confirmClearCart">
           <el-icon><Delete /></el-icon> 清空购物车
        </el-button>
      </div>

      <!-- 空购物车状态 -->
      <el-empty v-if="cart.length === 0" description="购物车还是空的，去挑选几束鲜花吧 🌿" :image-size="200">
         <el-button type="primary" size="large" round @click="$router.push('/products')">去逛逛鲜花</el-button>
      </el-empty>

      <!-- 购物车列表 -->
      <div v-else class="cart-content-wrapper">
        <!-- 表头 (Grid布局) -->
        <div class="cart-grid-header">
          <div class="col-check"><el-checkbox v-model="allSelected" @change="toggleAll" /></div>
          <div class="col-product">商品信息</div>
          <div class="col-price">单价</div>
          <div class="col-qty">数量</div>
          <div class="col-total">小计</div>
          <div class="col-action">操作</div>
        </div>

        <!-- 列表项 -->
        <div class="cart-items-list">
          <transition-group name="list">
            <div v-for="item in cart" :key="item.id" class="cart-item-row" :class="{ 'is-active': item.selected }">
              <div class="col-check">
                 <el-checkbox v-model="item.selected" @change="checkIfAllSelected" />
              </div>
              
              <div class="col-product">
                <div class="product-thumb" @click="$router.push(`/product/${item.id}`)">
                  <img :src="getProductImage(item)" loading="lazy" />
                </div>
                <div class="product-detail">
                  <h4 class="product-title" @click="$router.push(`/product/${item.id}`)" :title="item.name">{{ item.name }}</h4>
                  <div class="product-tags">
                   <el-tag size="small" type="success" effect="plain" round>现货</el-tag>
                  </div>
                </div>
              </div>

              <div class="col-price">
                <span class="price-unit">¥</span>{{ item.price }}
              </div>

              <div class="col-qty">
                <el-input-number 
                  v-model="item.quantity" 
                  :min="1" 
                  :max="item.stock" 
                  size="small"
                  @change="updateCart(item)" 
                  controls-position="right"
                />
                <div class="stock-warning" v-if="item.stock < 10">库存紧张: {{item.stock}}</div>
              </div>

              <div class="col-total">
                <span class="price-unit">¥</span>{{ (item.price * item.quantity).toFixed(2) }}
              </div>

              <div class="col-action">
                <el-button type="danger" circle plain @click="removeFromCart(item.id)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </transition-group>
        </div>
      </div>
      
      <!-- 底部结算栏 (吸底) -->
      <transition name="slide-up">
      <div v-if="cart.length > 0" class="cart-sticky-footer">
        <div class="footer-left">
           <el-checkbox v-model="allSelected" @change="toggleAll">全选</el-checkbox>
           <span class="text-selected">已选 <b>{{ selectedCount }}</b> 件商品</span>
        </div>
        <div class="footer-right">
           <div class="total-info">
             <span class="label">合计:</span>
             <span class="amount">¥ <span class="num">{{ totalPrice.toFixed(2) }}</span></span>
             <span class="freight-sc" v-if="totalPrice > 0">(不含运费)</span>
           </div>
           <el-button 
             type="primary" 
             size="large" 
             class="checkout-btn" 
             :disabled="selectedCount === 0"
             @click="showCheckout = true"
             color="#ff758c"
            >
             去结算
           </el-button>
        </div>
      </div>
      </transition>
    </div>
    </transition>

    <!-- 结算弹窗组件 -->
    <CheckoutModal
      v-if="showCheckout"
      :cart="cart.filter(i=>i.selected)"
      :total="totalPrice"
      :addresses="addressList"
      :balance="userBalance"
      @close="showCheckout = false"
      @pay="handlePay"
    />
  </div>
    <!-- 商品推荐组件 -->
<ProductRecommendation />
</template>

<script setup>
import { ref, computed, onMounted,h } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import { ElMessageBox, ElMessage,ElNotification } from 'element-plus'
import { Delete, ArrowLeft } from '@element-plus/icons-vue'
import CheckoutModal from './CheckoutModal.vue'
import OrderList from './OrderList.vue'

import ProductRecommendation from '@/components/ProductRecommendation.vue'

// Vuex & Router
const store = useStore()
const route = useRoute()

// Reactive Data
const showCheckout = ref(false)
// const showPaySuccessModal = ref(false)
const showOrderList = ref(false)
const addressList = ref([])
const userBalance = ref(0)
const orderList = ref([])
const allSelected = ref(false)

// Computed
const cart = computed(() => store.state.cart)
const totalPrice = computed(() => store.getters.totalPrice || 0)
const selectedCount = computed(() => cart.value.filter(i => i.selected).length)

// Methods
const getProductImage = (item) => {
  if (!item.image_url) return require('@/assets/logo.png')
  return item.image_url.startsWith('http') ? item.image_url : `http://localhost:5000${item.image_url}`
}

const toggleAll = (val) => {
  store.commit('toggleAllSelection', val)
}

const checkIfAllSelected = () => {
  allSelected.value = cart.value.length > 0 && cart.value.every(i => i.selected)
}

const updateCart = (item) => {
  store.commit('updateCart', { id: item.id, quantity: item.quantity })
}

const removeFromCart = (id) => {
  store.commit('removeFromCart', id)
  checkIfAllSelected()
}

const confirmClearCart = () => {
  ElMessageBox.confirm(
    '确定要清空购物车里的所有商品吗？',
    '提示',
    {
      confirmButtonText: '狠心清空',
      cancelButtonText: '再想想',
      type: 'warning',
      center: true
    }
  ).then(() => {
    store.commit('clearCart')
    ElMessage.success('购物车已清空')
  }).catch(() => {})
}

// API Calls
const loadOrders = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await fetch('http://localhost:5000/api/orders', {
      headers: { Authorization: 'Bearer ' + token }
    })
    if (res.ok) orderList.value = await res.json()
  } catch (e) {
    console.error(e)
  }
}

const loadAddresses = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await fetch('http://localhost:5000/api/user/addresses', { headers: { Authorization: 'Bearer ' + token } })
    const data = await res.json()
    addressList.value = data.addresses || []
  } catch(e) { console.error(e) }
}

const loadBalance = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await fetch('http://localhost:5000/api/user/profile', { headers: { Authorization: 'Bearer ' + token } })
    const data = await res.json()
    userBalance.value = Number(data.balance) || 0
  } catch(e) { console.error(e) }
}

const toOrderList = () => {
  showOrderList.value = true
}

const handlePay = async ({ addressId, remark }) => {
  const selectedAddr = addressList.value.find(addr => addr.id === addressId)
  
  if (userBalance.value < totalPrice.value) {
    ElMessage.error('余额不足，请充值')
    return { success: false }
  }
  
  if (!selectedAddr) {
    ElMessage.warning('请选择收货地址')
    return { success: false }
  }

  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:5000/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
      body: JSON.stringify({
        items: cart.value.filter(i => i.selected).map(item =>({
          product_id: item.id,
          quantity: item.quantity
        })),
        receiver: selectedAddr.realname,
        receiver_phone: selectedAddr.phone,
        receiver_address: selectedAddr.address,
        remark: remark,
      })
    })
    const data = await res.json()
    
    if (res.ok) {
      showCheckout.value = false
      store.commit('clearCart') // 可以优化为只清除选中的商品
      await loadBalance()
      await loadOrders()
      ElNotification({
        title: '支付支付成功 ヾ(≧▽≦*)o',
        message: h('div', { style: 'color: teal' }, [
          h('p', { style: 'margin: 0 0 10px 0' }, '您的订单已确认，我们会尽快为您发货！'),
          h('div', { style: 'display: flex; gap: 10px' }, [
            h('button', { 
              class: 'el-button el-button--primary el-button--small',
              onClick: () => { 
                toOrderList(); // 跳转到订单列表
                ElNotification.closeAll(); // 关闭通知
              }
            }, '查看订单'),
            h('button', { 
              class: 'el-button el-button--default el-button--small',
              onClick: () => ElNotification.closeAll() 
            }, '继续逛逛')
          ])
        ]),
        type: 'success',
        duration: 5000,
        position: 'top-right', // 改为右上角弹出
        offset: 100 // 稍微往下一点，避开 Header
      })
      return { success: true }
    } else {
      ElMessage.error(data.message || '支付失败')
      return { success: false, message: data.message }
    }
  } catch (e) {
    ElMessage.error('网络错误，请重试')
    return { success: false }
  }
}

// Lifecycle
onMounted(() => {
  loadAddresses()
  loadBalance()
  loadOrders()
  // 检查是否是从订单跳转
  if (route.query.order === '1') {
    showOrderList.value = true
  }
})

</script>

<style scoped>
.cart-page {
  /* max-width: 1200px; */
  /* margin: 0 auto; */
  /* padding-bottom: 80px;  留出底部栏高度 */
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  min-height: 80vh;
}

/* 轮播图卡片 */
.cart-banner-section {
  margin-bottom: 24px;
}
.promo-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-radius: 12px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.promo-card h3 { margin: 0 0 8px 0; font-size: 24px; font-weight: bold; }
.promo-card p { margin: 0; font-size: 14px; opacity: 0.9; letter-spacing: 1px;}

.bg-gradient-1 { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); }
.bg-gradient-2 { background: linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%); }
.bg-gradient-3 { background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }

/* 容器样式 */
.cart-main-container, .order-list-container {
  /* background: #ffffff; */
  /* border-radius: 16px; */
  padding: 10px;
  /* box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04); */
  min-height: 500px;
  position: relative;
}

/* 头部 Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}
.header-left { display: flex; align-items: center; gap: 10px; }
.section-header h2 { font-size: 22px; color: #333; margin: 0; font-weight: 600; }
.cart-count-badge { background: #ff758c; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }
.back-link { font-size: 16px; color: #666; }
.back-link:hover { color: #ff758c; }

/* 购物车 GRID 布局 */
.cart-grid-header {
  display: grid;
  grid-template-columns: 50px 3fr 1fr 1.2fr 1fr 80px;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  color: #888;
  font-size: 13px;
  margin-bottom: 16px;
  text-transform: uppercase;
}
.cart-grid-header div { text-align: center; }
.cart-grid-header .col-product { text-align: left; padding-left: 20px;}

.cart-item-row {
  display: grid;
  grid-template-columns: 50px 3fr 1fr 1.2fr 1fr 80px;
  align-items: center;
  padding: 24px 12px;
  border-bottom: 1px solid #f5f5f5;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: #fff;
  border-radius: 8px;
  margin-bottom: 10px;
}
.cart-item-row:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transform: translateY(-2px);
  z-index: 2;
}
.cart-item-row.is-active {
  background: #fffafa;
  border-left: 3px solid #ff758c;
}

/* 列样式 */
.col-check { display: flex; justify-content: center; }
.col-product { display: flex; align-items: center; gap: 16px; text-align: left; }
.col-price, .col-qty, .col-total, .col-action { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }

/* 商品信息 */
.product-thumb {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #eee;
  flex-shrink: 0;
  cursor: pointer;
}
.product-thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
.product-thumb:hover img { transform: scale(1.1); }

.product-detail { display: flex; flex-direction: column; gap: 6px; }
.product-title { margin: 0; font-size: 16px; color: #333; font-weight: 500; cursor: pointer; transition: color 0.2s;}
.product-title:hover { color: #ff758c; }
.product-tags .el-tag { border: none; }

/* 价格与总价 */
.col-price { font-size: 15px; color: #666; font-family: 'Helvetica Neue', sans-serif;}
.col-total { font-size: 16px; color: #ff4081; font-weight: bold; font-family: 'Helvetica Neue', sans-serif;}
.price-unit { font-size: 12px; margin-right: 2px;}

/* 库存警告 */
.stock-warning { font-size: 12px; color: #e6a23c; margin-top: 4px; }

/* 底部吸底栏 */
.cart-sticky-footer {
  position: sticky;
  bottom: 0px;
  margin-top: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 -4px 24px rgba(0,0,0,0.08); /* 向上阴影 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
  border: 1px solid #ebeef5;
}

.footer-left { display: flex; align-items: center; gap: 16px; }
.text-selected b { color: #ff758c; font-size: 16px; margin: 0 4px; }

.footer-right { display: flex; align-items: center; gap: 24px; }
.total-info { display: flex; align-items: baseline; }
.total-info .label { font-size: 14px; color: #666; margin-right: 8px;}
.total-info .amount { font-size: 20px; color: #f56c6c; font-weight: bold; font-family: 'Helvetica Neue', sans-serif;}
.total-info .amount .num { font-size: 28px; }
.freight-sc { font-size: 12px; color: #999; margin-left: 6px; }

.checkout-btn {
  width: 140px;
  font-size: 16px;
  border-radius: 30px; /* 圆角按钮 */
  letter-spacing: 1px;
  box-shadow: 0 4px 12px rgba(255, 117, 140, 0.4);
}
.checkout-btn:disabled { box-shadow: none; }

/* 支付成功弹窗内容 */
.pay-success-content {
  text-align: center;
  padding: 20px 0;
}
.success-icon { font-size: 64px; color: #67c23a; margin-bottom: 16px; display: block; }
.success-title { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 8px; }
.success-desc { color: #999; font-size: 14px; }
.dialog-footer { display: flex; justify-content: center; gap: 16px; padding-bottom: 10px;}

/* 动画效果 */
.list-enter-active, .list-leave-active { transition: all 0.4s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(30px); }

.fade-slide-enter-active, .fade-slide-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(10px); }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s ease, opacity 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); opacity: 0; }
</style>