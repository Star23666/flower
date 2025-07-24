<template>
    <div>
    <h4 class="mb-3 text-center">我的订单</h4>
      <table class="table table-bordered">
        
        <thead>
          <tr class="text-center">
            <th>订单号</th>
            <th>商品</th>
            <th>价格</th>
            <th>数量</th>
            <th>总价</th>
            <th>收货人</th>
            <th>电话</th>
            <th>地址</th>
            <th>下单时间</th>
            <th>备注</th>
            <th style="width:150px;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td style="max-width:50px;
            overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;" 
            :title="order.order_no">
            {{ order.order_no }}
        </td>
            <td style="width:200px;" >
              <div v-for="item in order.items" :key="item.product_id">
                {{ item.product_name }} × {{ item.quantity }}（¥{{ item.unit_price }}）
              </div>
            </td>
            <td>
            <div v-for="item in order.items" :key="item.product_id">
                {{ item.unit_price }}
            </div>
            </td>
            <td>
              <div v-for="item in order.items" :key="item.product_id">
                {{ item.quantity }}
              </div>
            </td>
            <td>¥{{ order.total_amount }}</td>
            <td>{{ order.receiver }}</td>
            <td>{{ order.receiver_phone }}</td>
            <td>{{ order.receiver_address }} </td>
            <td style="max-width:50px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" :title="order.created_at">
              {{ order.created_at }}
            </td>
            <td style="max-width:50px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ order.remark }}</td>
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
    props: {
      orders: Array
    },
    methods: {
      viewOrder(order) {
        // 可弹窗显示订单详情，或跳转详情页
        alert('订单详情：' + JSON.stringify(order, null, 2));
      }
    }
  }
  </script>