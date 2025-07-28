<script setup>

import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessageBox, ElMessage } from 'element-plus'

const store = useStore()
const dialogVisible = ref(false)
const currentOrder = ref(null)
const searchText = ref('')
const statusFilter = ref('')

onMounted(() => store.dispatch('fetchOrders'))
const orderList = computed(() => store.state.orders)

const filteredOrders = computed(() => {
  let list = orderList.value
  if (statusFilter.value) {
    list = list.filter(order => order.status === statusFilter.value)
  }
  if (searchText.value) {
    const text = searchText.value.trim().toLowerCase()
    list = list.filter(order =>
      (order.order_no && order.order_no.toLowerCase().includes(text)) ||
      (order.receiver && order.receiver.toLowerCase().includes(text)) ||
      (order.receiver_phone && order.receiver_phone.toLowerCase().includes(text))
    )
  }
  return list
})

function showDetail(order) {
  currentOrder.value = order
  dialogVisible.value = true
}
function handleDelete(order) {
  // 二次确认
  ElMessageBox.confirm(
    `确定要删除订单号为 ${order.order_no} 的订单吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    // 调用后端删除接口（假设为 DELETE /api/orders/:id）
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/orders/${order.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      ElMessage.success('删除成功')
      // 刷新订单列表
      store.dispatch('fetchOrders')
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '删除失败')
    }
  }).catch(() => {})
}

async function handleShip(order) {
  const token = localStorage.getItem('token')
  // 调用后端接口，更新订单状态为“已发货”
  const res = await fetch(`http://localhost:5000/api/orders/${order.id}/ship`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  })
  if (res.ok) {
    ElMessage.success('发货成功')
    store.dispatch('fetchOrders') // 刷新订单列表
  } else {
    const err = await res.json()
    ElMessage.error(err.message || '发货失败')
  }
}

</script>

<template>
  <div style="margin-bottom: 12px; display: flex; gap: 12px;">
    <el-button-group>
      <el-button :type="statusFilter === '' ? 'primary' : 'default'" @click="statusFilter = ''">全部订单</el-button>
      <el-button :type="statusFilter === '已支付' ? 'primary' : 'default'" @click="statusFilter = '已支付'">已支付订单</el-button>
      <el-button :type="statusFilter === '已完成' ? 'primary' : 'default'" @click="statusFilter = '已完成'">已完成订单</el-button>
      <el-button :type="statusFilter === '已取消' ? 'primary' : 'default'" @click="statusFilter = '已取消'">已取消订单</el-button>
      <el-button :type="statusFilter === '已退款' ? 'primary' : 'default'" @click="statusFilter = '已退款'">已退款订单</el-button>
      <el-button :type="statusFilter === '已发货' ? 'primary' : 'default'" @click="statusFilter = '已发货'">已发货订单</el-button>
    </el-button-group>
    <el-input
      v-model="searchText"
      placeholder="搜索订单号/收货人/电话"
      clearable
      style="width: 260px; margin-left: 16px;"
    />
  </div>

<el-table :data="filteredOrders" border style="margin-top: 10px;">
  <el-table-column prop="order_no" label="订单号" width="100" show-overflow-tooltip />
  <el-table-column prop="user_id" label="用户ID" width="70" align="center" />
  <el-table-column prop="total_amount" label="总价" width="100" align="right" />
  <el-table-column prop="pay_method" label="支付方式" width="90" align="center" />
  <el-table-column prop="receiver" label="收货人" width="80" align="center" />
  <el-table-column prop="receiver_phone" label="电话" width="80" show-overflow-tooltip />
  <el-table-column prop="receiver_address" label="地址" min-width="60" show-overflow-tooltip />
  <el-table-column prop="status" label="状态" width="80" align="center" />
  <el-table-column prop="created_at" label="下单时间" width="100" show-overflow-tooltip />
  <el-table-column label="操作" width="200" fixed="right" align="center">
  <template #default="scope">
    <el-button-group>
      <el-button size="small" @click="showDetail(scope.row)">详情</el-button>
      <el-button
        v-if="scope.row.status === '已支付'"
        size="small"
        type="success"
        @click="handleShip(scope.row)"
      >发货</el-button>
      <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>

    </el-button-group>
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