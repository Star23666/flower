<template>
    <div>
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
    <h4 class="mb-3 text-center">我的订单</h4>
      <table class="table table-bordered">
        <thead>
          <tr class="align-middle">
            <th style="width:150px;">订单号</th>
            <th style="width:100px;">商品</th>
            <th style="width:50px;">总价</th>                                
            <th style="width:150px;">下单时间</th>
            <th style="width:150px;" class="text-center">操作</th>
          </tr>
        </thead>
        <tbody class="align-middle">
          <tr v-for="order in orders" :key="order.id">
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
                <div style="width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" :title="order.created_at">
                    {{ order.created_at }}
                </div>
            </td>
            <td>
              <button class="btn btn-sm btn-primary" @click="viewOrder(order)">查看</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showDetailModal: false,
        selectedOrder: null,
      }
    },
    props: {
      orders: Array
    },
    methods: {
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
.modal {
  z-index: 2000;
}
</style>