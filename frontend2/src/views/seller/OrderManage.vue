<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Search,
  Refresh,
  Van,
  View,
  Timer
} from '@element-plus/icons-vue'

const store = useStore()

// ------------------------------------------------
// 状态管理
// ------------------------------------------------
const loading = ref(false)
const drawerVisible = ref(false)
const currentOrder = ref(null)
const searchText = ref('')
const activeTab = ref('all') // 用于 Tabs v-model

// ------------------------------------------------
// 数据初始化
// ------------------------------------------------
onMounted(() => {
  fetchData()
})

const fetchData = async () => {
  loading.value = true
  await store.dispatch('fetchOrders')
  loading.value = false
}

// ------------------------------------------------
// 计算属性：过滤逻辑
// ------------------------------------------------
const orderList = computed(() => store.state.orders)

const filteredOrders = computed(() => {
  let list = orderList.value
  
  // 1. 状态过滤 (Tab 页签)
  // 映射 Tab name 到实际状态值
  if (activeTab.value !== 'all') {
    list = list.filter(order => order.status === activeTab.value)
  }

  // 2. 搜索过滤
  if (searchText.value) {
    const text = searchText.value.trim().toLowerCase()
    list = list.filter(order =>
      (order.order_no && order.order_no.toLowerCase().includes(text)) ||
      (order.receiver && order.receiver.toLowerCase().includes(text)) ||
      (order.receiver_phone && order.receiver_phone.toLowerCase().includes(text))
    )
  }
  
  // 3. 排序：最新的在上面
  return list.slice().sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

// ------------------------------------------------
// 业务操作
// ------------------------------------------------

// 查看详情
function showDetail(order) {
  currentOrder.value = { ...order }
  drawerVisible.value = true
}

// 发货
async function handleShip(order) {
  try {
    await ElMessageBox.confirm(`确认对订单 ${order.order_no} 进行发货操作？`, '发货确认', {
      confirmButtonText: '确认发货',
      cancelButtonText: '取消',
      type: 'success'
    })
    
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/orders/${order.id}/ship`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    })
    
    if (res.ok) {
      ElMessage.success('发货成功')
      fetchData()
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '发货失败')
    }
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('操作取消或失败')
  }
}

// 处理退款 (同意)
async function approveRefund(order) {
  try {
    await ElMessageBox.confirm('确定同意该用户的退款申请吗？资金将原路退回。', '退款审核', {
       type: 'warning', confirmButtonText: '同意退款'
    })
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/orders/${order.id}/refund/approve`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      ElMessage.success('已同意退款')
      fetchData()
      drawerVisible.value = false
    } else {
      const data = await res.json()
      ElMessage.error(data.message || '操作失败')
    }
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

// 处理退款 (拒绝)
async function rejectRefund(order) {
  try {
    await ElMessageBox.confirm('确定拒绝退款申请吗？', '退款审核', {
       type: 'info', confirmButtonText: '拒绝退款'
    })
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/orders/${order.id}/refund/reject`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      ElMessage.success('已拒绝退款')
      fetchData()
      drawerVisible.value = false
    } else {
      const data = await res.json()
      ElMessage.error(data.message || '操作失败')
    }
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

// 删除订单
function handleDelete(order) {
  ElMessageBox.confirm(
    `确定要删除订单 ${order.order_no} 吗？此操作不可恢复。`,
    '删除警告',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/orders/${order.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      ElMessage.success('删除成功')
      fetchData()
    } else {
      const err = await res.json()
      ElMessage.error(err.message || '删除失败')
    }
  }).catch(() => {})
}

// ------------------------------------------------
// UI 辅助函数
// ------------------------------------------------
// 状态颜色映射
const getStatusType = (status) => {
  const map = {
    '已支付': 'success',
    '已发货': 'primary',
    '已完成': 'success',
    '已取消': 'info',
    '退款审核中': 'warning',
    '已退款': 'danger'
  }
  return map[status] || 'info'
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return timeStr.replace('T', ' ').substring(0, 16)
}
</script>

<template>
  <div class="page-container">
    
    <!-- 顶部工具栏 -->
    <div class="toolbar-wrapper">
      <div class="left-panel">
        <h2 class="page-title">订单中心 <span class="sub-title">Order Center</span></h2>
      </div>
      
      <div class="right-panel">
        <el-input
          v-model="searchText"
          placeholder="搜索订单号 / 收货人 / 电话"
          class="search-input"
          clearable
          @keyup.enter="fetchData"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-button circle plain @click="fetchData" :loading="loading">
          <el-icon><Refresh /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 状态筛选 Tabs -->
    <div class="tabs-container">
      <el-tabs v-model="activeTab" class="custom-tabs">
        <el-tab-pane label="全部订单" name="all" />
        <el-tab-pane label="待发货" name="已支付" />
        <el-tab-pane label="已发货" name="已发货" />
        <el-tab-pane label="退款售后" name="退款审核中" />
        <el-tab-pane label="已完成" name="已完成" />
        <el-tab-pane label="已取消" name="已取消" />
      </el-tabs>
    </div>

    <!-- 订单列表 -->
    <div class="table-container">
      <el-table 
        :data="filteredOrders" 
        style="width: 100%" 
        v-loading="loading"
        header-cell-class-name="table-header"
      >
        <!-- 订单基本信息 -->
        <el-table-column label="订单信息" min-width="220">
          <template #default="{ row }">
            <div class="order-info-cell">
              <span class="order-no">{{ row.order_no }}</span>
              <div class="order-time">
                <el-icon><Timer /></el-icon> {{ formatTime(row.created_at) }}
              </div>
            </div>
          </template>
        </el-table-column>

        <!-- 收货信息 -->
        <el-table-column label="收货人" min-width="150">
          <template #default="{ row }">
            <div class="receiver-cell">
              <div class="name">{{ row.receiver }}</div>
              <div class="phone">{{ row.receiver_phone }}</div>
            </div>
          </template>
        </el-table-column>

        <!-- 金额 -->
        <el-table-column label="总金额" width="120" align="right">
          <template #default="{ row }">
            <div class="amount-cell">
              <span class="currency">¥</span>
              <span class="value">{{ row.total_amount }}</span>
            </div>
          </template>
        </el-table-column>

        <!-- 状态 -->
        <el-table-column label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" effect="light" round>
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 操作 -->
        <el-table-column label="操作" width="180" align="right" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">
              <el-icon class="mr-1"><View /></el-icon>详情
            </el-button>
            
            <el-divider direction="vertical" />

            <!-- 根据状态显示不同按钮 -->
            <template v-if="row.status === '已支付'">
              <el-button link type="success" @click="handleShip(row)">
                <el-icon class="mr-1"><Van /></el-icon>发货
              </el-button>
            </template>
            
            <template v-else-if="row.status === '退款审核中'">
              <el-button link type="warning" @click="showDetail(row)">
                审核
              </el-button>
            </template>

            <template v-else>
               <el-button link type="danger" @click="handleDelete(row)">
                删除
              </el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 订单详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="订单详情"
      size="500px"
      direction="rtl"
      destroy-on-close
    >
      <div v-if="currentOrder" class="drawer-content">
        <!-- 状态横幅 -->
        <div class="status-banner" :class="getStatusType(currentOrder.status)">
          <div class="status-text">{{ currentOrder.status }}</div>
          <div class="order-id">NO. {{ currentOrder.order_no }}</div>
        </div>

        <!-- 详情列表 -->
        <div class="section-title">收货信息</div>
        <div class="info-grid">
          <div class="label">收货人</div><div class="value">{{ currentOrder.receiver }}</div>
          <div class="label">电话</div><div class="value">{{ currentOrder.receiver_phone }}</div>
          <div class="label">地址</div><div class="value address">{{ currentOrder.receiver_address }}</div>
        </div>

        <div class="section-title">支付信息</div>
        <div class="info-grid">
          <div class="label">总金额</div><div class="value price">¥ {{ currentOrder.total_amount }}</div>
          <div class="label">支付方式</div><div class="value">{{ currentOrder.pay_method }}</div>
          <div class="label">下单时间</div><div class="value">{{ formatTime(currentOrder.created_at) }}</div>
        </div>

        <div class="section-title">商品清单</div>
        <div class="goods-list">
          <div v-for="item in currentOrder.items" :key="item.product_id" class="goods-item">
            <div class="goods-info">
              <div class="goods-name">{{ item.product_name }}</div>
              <div class="goods-price">¥ {{ item.unit_price }} x {{ item.quantity }}</div>
            </div>
            <div class="goods-total">¥ {{ (item.unit_price * item.quantity).toFixed(2) }}</div>
          </div>
        </div>

        <!-- 审核操作区 -->
        <div v-if="currentOrder.status === '退款审核中'" class="action-footer">
          <div class="audit-title">退款审核</div>
          <div class="btn-row">
            <el-button type="success" @click="approveRefund(currentOrder)" icon="Check">同意退款</el-button>
            <el-button type="danger" @click="rejectRefund(currentOrder)" icon="Close">拒绝退款</el-button>
          </div>
        </div>

        <div v-if="currentOrder.status === '已支付'" class="action-footer">
           <el-button type="primary" @click="handleShip(currentOrder)" icon="Van" style="width: 100%">确认发货</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
.page-container {
  min-height: 100%;
}

/* 顶部栏 */
.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.page-title {
  font-size: 24px; font-weight: 700; color: #1f2937; margin: 0;
}
.sub-title {
  font-size: 14px; color: #9ca3af; font-weight: 400; font-family: 'Helvetica Neue', sans-serif;
}
.right-panel {
  display: flex; gap: 12px; align-items: center;
}
.search-input { width: 240px; }
.search-input :deep(.el-input__wrapper) { border-radius: 20px; }

/* Tabs */
.tabs-container {
  background: #fff;
  padding: 6px 20px 0;
  border-radius: 12px 12px 0 0;
  border-bottom: 1px solid #f0f0f0;
}
.custom-tabs :deep(.el-tabs__header) { margin-bottom: 0; }
.custom-tabs :deep(.el-tabs__nav-wrap::after) { height: 0; }

/* 表格 */
.table-container {
  background: #fff;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  padding: 16px;
}

:deep(.table-header) {
  background: #f9fafb !important;
  color: #374151;
  font-weight: 600;
}

/* 单元格样式 */
.order-info-cell { display: flex; flex-direction: column; gap: 4px; }
.order-no { font-family: monospace; font-weight: bold; color: #111827; font-size: 15px; }
.order-time { font-size: 12px; color: #9ca3af; display: flex; align-items: center; gap: 4px; }

.receiver-cell { display: flex; flex-direction: column; }
.receiver-cell .name { font-weight: 500; color: #374151; }
.receiver-cell .phone { font-size: 12px; color: #6b7280; }

.amount-cell { font-weight: bold; color: #f56c6c; }
.amount-cell .currency { font-size: 12px; margin-right: 2px; }
.amount-cell .value { font-size: 16px; }

.mr-1 { margin-right: 4px; }

/* 详情抽屉样式 */
.status-banner {
  padding: 20px; border-radius: 8px; color: #fff; margin-bottom: 24px;
  display: flex; justify-content: space-between; align-items: center;
}
.status-banner.success { background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%); }
.status-banner.primary { background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%); }
.status-banner.warning { background: linear-gradient(135deg, #e6a23c 0%, #f3d19e 100%); }
.status-banner.danger { background: linear-gradient(135deg, #f56c6c 0%, #f89898 100%); }
.status-banner.info { background: linear-gradient(135deg, #909399 0%, #b1b3b8 100%); }

.status-text { font-size: 20px; font-weight: bold; }
.order-id { opacity: 0.8; font-family: monospace; }

.section-title {
  font-size: 14px; font-weight: 700; color: #111827; margin: 24px 0 12px;
  padding-left: 8px; border-left: 3px solid #409eff;
}

.info-grid {
  display: grid; grid-template-columns: 80px 1fr; row-gap: 12px; font-size: 14px;
}
.info-grid .label { color: #9ca3af; }
.info-grid .value { color: #374151; }
.info-grid .address { line-height: 1.4; }
.info-grid .price { color: #f56c6c; font-weight: bold; font-size: 16px; }

.goods-list { background: #f9fafb; border-radius: 8px; padding: 12px; }
.goods-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px dashed #e5e7eb;
}
.goods-item:last-child { border-bottom: none; }
.goods-name { font-size: 14px; color: #374151; font-weight: 500; }
.goods-price { font-size: 12px; color: #9ca3af; margin-top: 2px; }
.goods-total { font-weight: bold; color: #374151; }

.action-footer {
  margin-top: 40px; border-top: 1px solid #f0f0f0; padding-top: 20px;
}
.audit-title { font-weight: bold; margin-bottom: 12px; color: #e6a23c; }
.btn-row { display: flex; gap: 12px; }
.btn-row .el-button { flex: 1; }
</style>