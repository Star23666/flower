<template>
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


    <h4 class="mb-3 text-center">购物车</h4>
    <table class="table table-sm align-middle text-center bg-white rounded shadow-sm w-100" style="margin-bottom:0;">
      <thead class="table-light">
        <tr>
          <th scope="col" style="width:40px;"></th>
          <th scope="col" style="width:220px;">商品</th>
          <th scope="col" style="width:80px;">价格</th>
          <th scope="col" style="width:90px;">数量</th>
          <th scope="col" style="width:90px;">总价</th>
          <th scope="col" style="width:70px;">操作</th>
        </tr>
      </thead>
      <tbody>
  <tr v-for="item in cart" :key="item.id">
    <td><input type="checkbox" v-model="item.selected"></td>
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
        style="width: 60px; padding: 2px 4px;"
        :min="1"
        :step="1"
        v-model.number="item.quantity"
        @input="validateQty(item)">
    </td>
    <td class="align-middle text-center">¥{{ (item.price * item.quantity).toFixed(2) }}</td>
    <td class="align-middle">
      <button class="btn btn-danger btn-sm px-2 py-1" @click="removeItem(item)">删除</button>
    </td>
  </tr>
</tbody>
    </table>
    <div class="d-flex justify-content-end align-items-center gap-3 mt-2">
      <span class="fw-bold text-danger fs-6">总价：¥{{ totalPrice.toFixed(2) }}</span>
      <button class="btn btn-warning btn-sm px-3" @click="showCheckout = true" :disabled="cart.length === 0">去结算</button>
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

export default {
  name:'CartView',
  components:{
    CheckoutModal,
  },
  data() {
    return {
      banner3,
      cart: [], // 从 Vuex 或本地获取
      allSelected: true,
      showCheckout:false,
      addressList:[],
      userBalance:0,
      toastMessage:'',
      toastType:'', // 可扩展 info/warning/danger
    }
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((sum, item) => item.selected ? sum + item.price * item.quantity : sum, 0)
    }
  },
  methods: {
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
      if (!item.image_url) return 'https://via.placeholder.com/60x60?text=No+Image';
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
    removeItem(item) {
      this.cart = this.cart.filter(i => i.id !== item.id);
      // 若用 Vuex，需同步到 store
    },
    toggleAll() {
      this.cart.forEach(i => i.selected = this.allSelected);
    },

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
    async handlePay({ addressId, remark }) {
      if (this.userBalance < this.totalPrice) {
        this.showToast('余额不足，请充值', 'danger')
        return { success: false, message: '余额不足，请充值' }
      }
      try {
        const res = await fetch('/api/order/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + localStorage.token },
          body: JSON.stringify({
            address_id: addressId,
            items: this.cart.filter(i => i.selected),
            remark
          })
        })
        const data = await res.json()
        if (data.success) {
          this.showToast('支付成功！', 'success')
          this.showCheckout = false
          this.cart = [] // 清空购物车
          await this.loadBalance() // 自动刷新余额
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
    checkout() {
      // 跳转支付页面功能留空
      alert('结算功能开发中');
    },
    updateCart(/*item*/){
      // 若用 Vuex，提交 mutation
    }
  },
  mounted() {

    this.cart = this.$store.state.cart||[]
    this.loadAddresses();
    this.loadBalance();
    // 加载购物车数据
  }
}
// console.log('addresses:', this.addressList)
// console.log('cart:', this.cart)
// console.log('userBalance:', this.userBalance)
</script>