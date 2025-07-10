<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
const store = useStore()
const dialogVisible = ref(false)
const currentOrder = ref(null)
const searchText = ref('')

onMounted(() => store.dispatch('fetchOrders'))
const orderList = computed(() => store.state.orders)

const filteredOrders = computed(() => {
  if (!searchText.value) return orderList.value
  return orderList.value.filter(order => {
    const text = searchText.value.trim().toLowerCase()
    return (
      (order.order_no && order.order_no.toLowerCase().includes(text)) ||
      (order.receiver && order.receiver.toLowerCase().includes(text)) ||
      (order.receiver_phone && order.receiver_phone.toLowerCase().includes(text))
    )
  })
})

function showDetail(order) {
  currentOrder.value = order
  dialogVisible.value = true
}
</script>

<template>
<div style="margin-bottom: 12px; display: flex; gap: 12px;">
  <el-input
    v-model="searchText"
    placeholder="搜索订单号/收货人/电话"
    clearable
    style="width: 260px;"
  />
</div>

<el-table :data="filteredOrders" border style="margin-top: 10px;">
  <el-table-column prop="order_no" label="订单号" width="140" show-overflow-tooltip />
  <el-table-column prop="user_id" label="用户ID" width="80" align="center" />
  <el-table-column prop="total_amount" label="总价" width="80" align="right" />
  <el-table-column prop="pay_method" label="支付方式" width="90" align="center" />
  <el-table-column prop="receiver" label="收货人" width="90" align="center" />
  <el-table-column prop="receiver_phone" label="电话" width="120" show-overflow-tooltip />
  <el-table-column prop="receiver_address" label="地址" min-width="160" show-overflow-tooltip />
  <el-table-column prop="status" label="状态" width="80" align="center" />
  <el-table-column prop="created_at" label="下单时间" width="160" show-overflow-tooltip />
  <el-table-column label="操作" width="100" fixed="right" align="center">
    <template #default="scope">
      <el-button size="small" @click="showDetail(scope.row)">详情</el-button>
    </template>
  </el-table-column>
</el-table>

  <el-dialog v-model="dialogVisible" title="订单详情" width="600px">
    <div v-if="currentOrder">
      <p>订单号：{{ currentOrder.order_no }}</p>
      <p>下单用户ID：{{ currentOrder.user_id }}</p>
      <p>收货人：{{ currentOrder.receiver }}</p>
      <p>收货电话：{{ currentOrder.receiver_phone }}</p>
      <p>收货地址：{{ currentOrder.receiver_address }}</p>
      <el-table :data="currentOrder.items" style="margin-top: 10px;">
        <el-table-column prop="product_id" label="商品ID" />
        <el-table-column prop="product_name" label="商品名称" />
        <el-table-column prop="quantity" label="数量" />
        <el-table-column prop="unit_price" label="单价" />
      </el-table>
    </div>
  </el-dialog>
</template>