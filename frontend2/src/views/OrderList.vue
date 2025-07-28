<template>
    <div>
      <h4 class="mb-3 text-center">我的订单</h4>
      <div class="order-filter-bar d-flex align-items-center justify-content-between mb-3">
    <!-- 状态Tab -->
    <div class="btn-group" role="group">
      <button
        v-for="item in statusTabs"
        :key="item.value"
        class="btn"
        :class="filters.status === item.value ? 'btn-primary' : 'btn-outline-primary'"
        @click="selectStatus(item.value)"
      >
        {{ item.label }}
      </button>
    </div>
    <!-- 搜索框 -->
    <div class="position-relative" style="width: 260px;">
  <input
    v-model="filters.keyword"
    @keyup.enter="handleSearch"
    type="text"
    class="form-control"
    placeholder="搜索订单号/商品名"
    style="padding-right: 2.5rem;"
  />
  <button
  v-if="filters.keyword"
  class="btn btn-link p-0 position-absolute top-50 end-0 translate-middle-y"
  style="right: 0.75rem; font-size: 1.3rem; color: #888;"
  @click="resetFilters"
  tabindex="-1"
  aria-label="清空"
>
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
    <path d="M2.146 2.146a.5.5 0 0 1 .708 0L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854a.5.5 0 0 1 0-.708z"/>
  </svg>
</button>
</div>
  </div>
        <!-- 订单详情弹窗 -->
        <div class="modal fade show" tabindex="-1" style="display:block;" v-if="showDetailModal">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">订单详情</h5>
                        <button type="button" class="btn-close" @click="showDetailModal = false"></button>
                    </div>
                    <div class="modal-body" v-if="selectedOrder">
                        <p><strong>订单号：</strong>{{ selectedOrder.order_no }}</p>
                        <p><strong>收货人：</strong>{{ selectedOrder.receiver }}{{ selectedOrder.receiver_phone }}</p>
                        <p><strong>地址：</strong>{{ selectedOrder.receiver_address }}</p>
                        <p><strong>下单时间：</strong>{{ selectedOrder.created_at }}</p>
                        <p><strong>备注：</strong>{{ selectedOrder.remark }}</p>
                        <hr>
                        <h6>商品明细</h6>
                        <table class="table table-sm">
                            <thead>
                                <tr  class="align-middle">
                                    <th>图片</th>
                                    <th>商品</th>
                                    <th>数量</th>
                                    <th>单价</th>
                                </tr>
                            </thead>
                            <tbody >
                                <tr v-for="item in selectedOrder.items" :key="item.product_id" class="align-middle">
                                    <td>
                                        <img :src="fixImageUrl(item.image_url)" 
                                        alt = "商品图片" 
                                        style="width:50px;height:50px;object-fit:cover;" 
                                        v-if="item.image_url">
                                    </td>
                                    <td>{{ item.product_name }}</td>
                                    <td>{{ item.quantity }}</td>
                                    <td>¥{{ item.unit_price }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="text-end"><strong>总价：</strong>¥{{ selectedOrder.total_amount }}</div>
                    </div>
                    <div class="modal-footer">
        <button class="btn btn-secondary" @click="showDetailModal = false">关闭</button>
      </div>
    </div>
  </div>
  <!-- 遮罩层 -->
  <div class="modal fade show"></div>
</div>
      <table class="table table-bordered">
        <thead>
          <tr class="align-middle">
            <th style="width:150px;">订单号</th>
            <th style="width:100px;">商品</th>
            <th style="width:50px;">总价</th> 
            <th style="width:100px;">状态</th>                               
            <th style="width:150px;">下单时间</th>
            <th style="width:150px;" class="text-center">操作</th>
          </tr>
        </thead>
        <tbody class="align-middle">
          <tr v-for="order in filteredOrders" :key="order.id">
            <td>
            <div style="width:150px;overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;" 
            :title="order.order_no">
                {{ order.order_no }}
            </div>
            </td>
            <td style="width:100px;">
                <div v-for="item in order.items" :key="item.product_id" style="width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" :title="item.product_name">
                {{ item.product_name }} × {{ item.quantity }}（¥{{ item.unit_price }}）
            </div>
            </td>
            <td >
                <div style="width: 50px;">
                ¥{{ order.total_amount }}
                </div>
            </td>
            <td>
                <span>{{ getStatusText(order.status) }}</span>
            </td>
            <td>
                <div style="width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" :title="order.created_at">
                    {{ order.created_at }}
                </div>
            </td>
            <td>
  <div class="d-flex gap-2">
    <button 
      class="btn btn-sm btn-primary" 
      @click="viewOrder(order)"
    >查看</button>
    <button
      class="btn btn-sm btn-success"
      v-if="order.status === '已发货'"
      @click="confirmReceive(order)"
    >确认收货</button>
    <button
      class="btn btn-sm btn-danger"
      @click="deleteOrder(order)"
    >删除</button>
  </div>
</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
import axios from 'axios';
// 全局 axios 拦截器,所有 axios 请求都会自动带上 token。
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

  export default {
    data() {
      return {
        filters: {
          keyword: '',
          status: '',
        },
        statusTabs: [
        { label: '全部订单', value: '' },
        { label: '已支付订单', value: '已支付' },
        { label: '已完成订单', value: '已完成' },
        { label: '已取消订单', value: '已取消' },
        { label: '已退款订单', value: '已退款' },
        { label: '已发货订单', value: '已发货' }
      ],
        showDetailModal: false,
        selectedOrder: null,
        allOrders:[],
      }
    },
    computed: {
      filteredOrders() {
        const { keyword, status } = this.filters;
        if (!this.allOrders) return [];
        return this.allOrders.filter(order => {
          const keywordMatch = !keyword || 
          (order.order_no && order.order_no.toLowerCase().includes(keyword.toLowerCase())) ||
          (order.items && order.items.some(item => 
            item.product_name && item.product_name.toLowerCase().includes(keyword.toLowerCase())
          ));
        
        const statusMatch = !status || order.status === status;
        
        return keywordMatch && statusMatch;
      });
    }
  },
  async created() {
    await this.fetchOrders();
  },

    methods: {
      async confirmReceive(order) {
        try {
          await axios.post(`http://localhost:5000/api/orders/${order.id}/confirm`);
          this.$message && this.$message.success('确认收货成功');
          this.fetchOrders();
        } catch (error) {
          alert('确认收货失败');
        }
      },
      async deleteOrder(order) {
        if (!confirm('确定要删除该订单吗？')) return;
        try {
          await axios.delete(`http://localhost:5000/api/orders/${order.id}`);
          this.$message && this.$message.success('删除成功');
          this.fetchOrders();
        } catch (error) {
          alert('删除失败');
        }
      },
      selectStatus(status) {
        this.filters.status = status;
      },
      
      resetFilters(){
        this.filters = {
          keyword:'',
          status:'',
        };
      },
      async fetchOrders() {
        try {
          const response = await axios.get('http://localhost:5000/api/orders');
          this.allOrders = response.data;
          console.log(this.allOrders);
          console.log(this.allOrders.map(o => o.status));
        } catch (error) {
          console.error('获取订单失败:', error);
        }
      },
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleString('zh-CN');
      },
      getStatusText(status) {
        const statusMap = {
        'pending': '待付款',
        'paid': '已付款',
        'shipped': '已发货',
        'completed': '已完成',
        'cancelled': '已取消'
      };
      return statusMap[status] || status;
    },
      viewOrder(order) {
        // 可弹窗显示订单详情，或跳转详情页
        this.selectedOrder = order;
        this.showDetailModal = true;
        
      },
    // 前端渲染时判断，如果 image_url 
    // 以 /static/开头，
    // 则拼接 http://localhost:5000：
      fixImageUrl(url) {
        if (!url) return '';
        if (url.startsWith('/static/')) {
          return 'http://localhost:5000' + url;
        }
        return url;
      }
    },
  }
  </script>

<style scoped>
.order-filter-bar {
  background: #f8f9fa;
  padding: 12px 18px;
  border-radius: 8px;
}
.btn-group .btn {
  min-width: 110px;
}
</style>