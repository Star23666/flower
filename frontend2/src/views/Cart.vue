<template>


<div v-if="showPaySuccessModal">
  <div class="modal-backdrop show"></div>
  <div class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">支付成功</h5>
        </div>
        <div class="modal-body">
          <p>您的订单已支付成功！</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" @click="showPaySuccessModal = false">确定</button>
          <button class="btn btn-success" @click="toOrderList">我的订单</button>
        </div>
      </div>
    </div>
  </div>
</div>
  
  <!-- 保持轮播图不变 -->
  <div class="container py-2">
  <div id="carouselExampleIndicators" class="carousel slide mb-4" data-bs-ride="carousel" data-bs-interval="2500">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"></button>
  </div>
  <div class="carousel-inner" >
    <div class="carousel-item active" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner1">
      
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner2">
    </div>
    <div class="carousel-item" >
      <img :src="banner3" class="d-block w-100" style="height:320px;object-fit:cover;" alt="banner3">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
    <span class="carousel-control-next-icon"></span>
  </button>
</div>
</div>

<div v-if="!showOrderList"> 
    <h4 class="mb-3 text-center">购物车</h4>
    <table class="table table-sm align-middle text-center bg-white rounded shadow-sm w-100" style="margin-bottom:0;">
      <thead class="table-light">
        <tr>
          <th style="width:40px;">
          <input
          type="checkbox"
          class="cart-checkbox"
          v-model="allSelected"
          @change="toggleAll"
          />
        </th>
          <th scope="col" style="width:220px;">商品</th>
          <th scope="col" style="width:80px;">价格</th>
          <th scope="col" style="width:90px;">数量</th>
          <th scope="col" style="width:90px;">总价</th>
          <th scope="col" style="width:70px;">操作</th>
        </tr>
      </thead>
      <tbody>
    <tr v-for="item in cart" :key="item.id">
    <td>
      <input 
      type="checkbox" 
      class="cart-checkbox"
      v-model="item.selected"
      @change="checkIfAllSelected"
      />
    </td>
    <!-- 商品列左对齐 -->
    <td class="d-flex align-items-center gap-2 p-2" style="justify-content: flex-start;">
      <img :src="getProductImage(item)" style="width:48px;height:48px;object-fit:cover;border-radius:8px;" class="me-2">
      <span>{{ item.name }}</span>
    </td>
    <!-- 价格、数量、总价列居中 -->
    <td class="align-middle text-center">¥{{ item.price }}</td>
    <td class="align-middle text-center">
      <input type="number"
        class="form-control text-center mx-auto"
        style="width: 50px; padding: 2px 4px;"
        :min="1"
        :max="item.stock"
        v-model.number="item.quantity"
        @input="validateQty(item)">
    </td>
    <td class="align-middle text-center">¥{{ (item.price * item.quantity).toFixed(2) }}</td>
    <td class="align-middle">
      <button class="btn btn-danger btn-sm px-2 py-1" @click="removeFromCart(item.id)">删除</button>
    </td>
  </tr>
</tbody>
    </table>
    <div v-if="cart.length === 0 && !showOrderList" class="text-center text-muted my-5">
      购物车空空如也，快去选购商品吧！
    </div>
    <div class="d-flex justify-content-end align-items-center gap-3 mt-2">
      <span class="fw-bold text-danger fs-6">总价：¥{{ totalPrice.toFixed(2) }}</span>
      <button class="btn btn-warning btn-sm px-3" @click="showCheckout = true" :disabled="cart.length === 0">去结算</button>
    </div>
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
    <!-- 购物车内容 -->
  <div v-else>
    <OrderList 
    :orders="orderList" 
    @backToCart="showOrderList = false" />
  </div>

  <div 
  class="toast align-items-center text-bg-success border-0 position-fixed bottom-0 end-0 m-3" 
  role="alert" 
  aria-live="assertive" 
  aria-atomic="true"
  ref="toast"
  style="z-index: 9999;"
>
  <div class="d-flex">
    <div class="toast-body">
      {{ toastMessage }}
    </div>
    <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="hideToast"></button>
  </div>
</div>

</template>

<script>


import banner3 from '@/assets/banner3.png'

import CheckoutModal from './CheckoutModal.vue'
import OrderList from './OrderList.vue'

export default {
  name:'CartView',
  components:{
    CheckoutModal,
    OrderList,
  },
  data() {
    return {
      banner3,
      showCheckout:false,
      addressList:[],
      userBalance:0,
      toastMessage:'',
      toastType:'',
      allSelected:false,
      showOrderList:false,
      lastOrder:[],  //支付成功后存储订单详情
      orderList:[], //订单列表
      showPaySuccessModal:false,
    }
  },
  computed: {
    cart(){
      return this.$store.state.cart;
    },
    totalPrice() {
      return this.$store.getters.totalPrice;
    },
  },
  methods: {

    toOrderList(){
      this.showPaySuccessModal = false;
      this.showOrderList = true;
    },

    async loadOrders() {
      const res = await fetch('http://localhost:5000/api/orders', { 
        headers: { Authorization: 'Bearer ' + localStorage.token 

        } 
      });
      const data = await res.json()
      this.orderList = data;
    },
    
    async handlePaySuccess() {
      this.showOrderList = true;
      await this.loadOrders();
    },
    
    addToCart(product){
      this.$store.commit('addToCart',product);
    },
    removeFromCart(id){
      this.$store.commit('removeFromCart',id);
    },
    updateCart(id, quantity){
      this.$store.commit('updateCart' , {id ,quantity});
    },
    toggleItemSelected(id, selected) {
      this.$store.commit('toggleItemSelected', { id, selected });
    },
    clearCart() {
      this.$store.commit('clearCart');
    },
    toggleAll(){
      this.cart.forEach(i=> i.selected = this.allSelected);
    },
    checkIfAllSelected(){
      this.allSelected = this.cart.every(i => i.selected);
    },
    showToast(msg,type = 'success'){
      this.toastMessage = msg
      this.toastType = type
      const toastEl = this.$refs.toast
      if (window.bootstrap && toastEl){
        if (!this._toast){
          
          this._toastInstance = window.bootstrap.Toast.getOrCreateInstance(toastEl)

        }
        this._toastInstance.show()
      }
    },
    hideToast(){
      if (this._toastInstance) this._toastInstance.hide()   
    },
    getProductImage(item) {
      // 与商品页一致
      if (!item.image_url) return 'http://localhost:5000/static/uploads/products/no-image.png';
      if (item.image_url.startsWith('http')) return item.image_url;
      return 'http://localhost:5000' + item.image_url;
    },
    increaseQty(item) {
      item.quantity = Math.floor(item.quantity) + 1;
      this.validateQty(item);
      this.updateCart(item);
    },
    decreaseQty(item) {
      item.quantity = Math.max(1, Math.floor(item.quantity) - 1);
      this.updateCart(item);
    },
    validateQty(item) {
      // 只允许大于0的整数
      if (!item.quantity || item.quantity < 1) item.quantity = 1;
      item.quantity = Math.floor(item.quantity);
      this.updateCart(item);
    },
    // removeItem(item) {
    //   this.cart = this.cart.filter(i => i.id !== item.id);
    //   // 若用 Vuex，需同步到 store
    // },
    // 获取地址
    async loadAddresses() {
      const res = await fetch('http://localhost:5000/api/user/addresses', { headers: { Authorization: 'Bearer ' + localStorage.token } })
      const data = await res.json()
      this.addressList = data.addresses || []
      if (this.addressList.length) this.selectedAddressId = this.addressList[0].id
    },
    async loadBalance() {
      const res = await fetch('http://localhost:5000/api/user/profile',{ headers: { Authorization: 'Bearer ' + localStorage.token } })
      const data = await res.json()
      console.log('user profile:', data) 
      this.userBalance = Number(data.balance) || 0
    },
    async refreshAddressList(newId) {
      await this.loadAddresses()
      if (newId) this.selectedAddressId = newId
    },

    async handlePay({ addressId,remark } = {}) {
      console.log('Cart.vue handlePay', addressId, typeof addressId, remark);
      console.log('addressList:', this.addressList);
      console.log('addressId:', addressId);
      console.log('selectedAddress:', this.selectedAddress);
      // 根据当前选中的地址ID，找到对应的地址对象，并赋值给 this.selectedAddress，
      // 以便下单时能获取收货人、电话、地址等信息。
      
      this.selectedAddress = this.addressList.find(addr => addr.id === addressId) 
      if (this.userBalance < this.totalPrice) {
        this.showToast('余额不足，请充值', 'danger')
        return { success: false, message: '余额不足，请充值' }
      }
      
      if (!this.selectedAddress){
        this.showToast('请选择收货地址','danger');
        return { success: false, message: '请选择收货地址'}

      }
      try {
        const res = await fetch('http://localhost:5000/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + localStorage.token },
          body: JSON.stringify({
            items: this.cart.filter(i => i.selected).map(item =>({
              product_id: item.id,
              quantity:item.quantity
            })),
            receiver: this.selectedAddress.realname,
            receiver_phone: this.selectedAddress.phone,
            receiver_address: this.selectedAddress.address,
            remark:remark,

          })
        })
        const data = await res.json()
        if (res.ok) {  // res.ok 为 true 表示 2xx 响应
          this.showToast('支付成功！', 'success')
          this.showCheckout = false
          this.$store.commit('clearCart'); // 清空购物车（同步 localStorage）
          await this.loadBalance() // 自动刷新余额
          // 支付成功后,显示订单详情
          this.lastOrder =  data.order || null,
          await this.loadOrders();
          // 只弹出支付成功弹窗，不切换订单列表
          this.showPaySuccessModal = true; // 弹出支付成功弹窗
          return { success: true }
        } else {
          this.showToast(data.message || '支付失败', 'danger')
          return { success: false, message: data.message || '支付失败' }
        }
      } catch (e) {
        this.showToast('网络错误，请重试', 'danger')
        return { success: false, message: '网络错误，请重试' }
      }
    },
  },
  mounted() {
    this.loadAddresses();
    this.loadBalance();
    this.loadOrders(); //加载一次订单，防止刷新后为空
    if (this.$route.query.order === '1'){
      this.showOrderList = true;
    }
  }
}
</script>
<style scoped>
.cart-checkbox {
  width: 1em;
  height: 1em;
  accent-color: #ffc107; /* Bootstrap黄色 */
}

.modal-content {
  background: #fff !important;
  opacity: 1 !important;
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
}

</style>