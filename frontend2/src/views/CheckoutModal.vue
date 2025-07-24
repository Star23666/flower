<template>
    <div class="modal show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">确认下单</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <!-- 地址选择 -->
            <div>
              <label class="fw-bold mb-2">选择收货地址：</label>
              <!-- 地址表格 -->
            <table class="table table-bordered table-sm mb-3">
            <thead>
            <tr>
            <th style="width:40px;"></th>
            <th>收货人</th>
            <th>联系方式</th>
            <th>地址</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="addr in addresses" :key="addr.id">
            <td>
            <input type="radio" v-model="selectedAddressId" :value="addr.id" />
            </td>
            <td>{{ addr.realname }}</td>
            <td>{{ addr.phone }}</td>
            <td>{{ addr.address }}</td>
            </tr>
            <tr v-if="!addresses || addresses.length === 0">
            <td colspan="4" class="text-center text-muted">暂无地址，请先在个人中心添加</td>
            </tr>
            </tbody>
            </table>
            </div>
            <!-- 商品列表 -->
            <div>
              <label class="fw-bold mb-2">清单列表：</label>
              <table class="table table-sm align-middle">
            <thead>
            <tr>
            <th>商品图片</th>
            <th>商品名称</th>
            <th>单价</th>
            <th>数量</th>
            <th>总价</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="item in cart" :key="item.id">
            <td>
                <img :src="getProductImage(item)" style="width:60px;height:60px;object-fit:cover;">
            </td>
            <td>{{ item.name }}</td>
            <td>¥{{ item.price }}</td>
            <td>{{ item.quantity }}</td>
            <td>¥{{ (item.price * item.quantity).toFixed(2) }}</td>
            </tr>
            </tbody>
            </table>
            </div>
            <!-- 备注 -->
            <div class="mb-3">
              <label>备注：</label>
              <input v-model="remark" class="form-control" placeholder="可选，给商家留言"/>
            </div>
          </div>
          <div class="modal-footer justify-content-between">
            <span class="fw-bold text-danger">
                总价：¥{{ Number(total).toFixed(2) }}（余额：¥{{ Number(balance).toFixed(2) }}）
            </span>
            <button 
              class="btn btn-success" 
              :disabled="!selectedAddressId || cart.length === 0 || loading" 
              @click="pay">
              {{ loading ? '支付中...' : '支付' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: [
        'cart',
        'total', 
        'addresses', 
        'balance'
    ],
    emits: ['close', 'pay'],
    data() {
      return {
        selectedAddressId: this.addresses && this.addresses.length ? this.addresses[0].id : null,
        remark: '',
        loading: false
      }
    },
    watch: {
      addresses: {
        immediate: true,
        handler(newVal) {
          console.log('watch addresses', newVal, this.selectedAddressId);
          if (newVal && newVal.length > 0 && !this.selectedAddressId) {
            this.selectedAddressId = newVal[0].id;
            console.log('auto set selectedAddressId', this.selectedAddressId);
          }
        }
      }
    },
    methods: {
      getProductImage(item) {
    // 与商品页一致
      if (!item.image_url) return 'https://via.placeholder.com/60x60?text=No+Image';
      if (/^https?:\/\//.test(item.image_url)) return item.image_url;
      return 'http://localhost:5000' + item.image_url;
    },
      
      async pay() {
        console.log('pay emit', this.selectedAddressId, typeof this.selectedAddressId, this.remark);
        if (!this.selectedAddressId) {
          this.$emit('toast', {msg: '请选择收货地址', type: 'danger'})
          return
        }
        this.loading = true
        try {
          this.$emit('pay', { addressId: this.selectedAddressId, remark: this.remark })
        } finally {
          this.loading = false
        }
      }
    },
  }
  </script>

