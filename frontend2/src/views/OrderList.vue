<template>
  <div class="order-page-container">
    <!-- 顶部筛选栏 -->
    <div class="filter-glass-card mb-4">
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
        <!-- 状态Tabs -->
        <div class="status-tabs">
          <button
            v-for="item in statusTabs"
            :key="item.value"
            class="tab-btn"
            :class="{ active: filters.status === item.value }"
            @click="selectStatus(item.value)"
          >
            {{ item.label }}
          </button>
        </div>
        
        <!-- 搜索框 -->
        <div class="search-box">
          <el-input
            v-model="filters.keyword"
            placeholder="搜索订单号或商品..."
            prefix-icon="Search"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
            class="custom-search-input"
          />
        </div>
      </div>
    </div>

    <!-- 订单列表区域 -->
    <div v-if="loading" class="text-center py-5">
      <el-skeleton :rows="3" animated />
    </div>

    <div v-else-if="filteredOrders.length === 0" class="empty-state">
      <el-empty description="暂无相关订单" :image-size="200"></el-empty>
    </div>

    <div v-else class="order-list">
      <div 
        v-for="order in filteredOrders" 
        :key="order.id" 
        class="order-card"
        @click="viewOrder(order)"
      >
        <!-- 卡片头部：订单号与状态 -->
        <div class="card-header">
          <div class="order-info">
            <span class="order-no">订单号：{{ order.order_no }}</span>
            <span class="order-time">{{ formatDate(order.created_at) }}</span>
          </div>
          <el-tag :type="getStatusType(order.status)" effect="dark" class="status-tag">
            {{ order.status }}
          </el-tag>
        </div>

        <!-- 卡片中部：商品预览 -->
        <div class="card-body">
          <div class="product-preview">
            <div 
              v-for="(item, index) in order.items.slice(0, 3)" 
              :key="index" 
              class="product-thumb"
            >
              <el-image 
                :src="fixImageUrl(item.image_url)" 
                fit="cover"
                class="thumb-img"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="item-badge" v-if="item.quantity > 1">x{{ item.quantity }}</div>
            </div>
            <div v-if="order.items.length > 3" class="more-items">
              +{{ order.items.length - 3 }}
            </div>
          </div>
          
          <div class="price-info">
            <span class="label">总金额</span>
            <span class="amount">¥ {{ order.total_amount }}</span>
          </div>
        </div>

        <!-- 卡片底部：操作按钮 -->
        <div class="card-actions" @click.stop>
          <el-button 
            v-if="order.status === '已发货'" 
            type="success" 
            plain 
            size="small" 
            round
            @click="confirmReceive(order)"
          >确认收货</el-button>
          
          <el-button 
            type="primary" 
            plain 
            size="small" 
            round
            @click="viewOrder(order)"
          >查看详情</el-button>
          
          <el-popconfirm
            title="确定删除该订单记录吗？"
            confirm-button-text="删除"
            cancel-button-text="取消"
            confirm-button-type="danger"
            @confirm="deleteOrder(order)"
          >
            <template #reference>
              <el-button type="danger" link size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
    </div>

    <!-- 订单详情弹窗 -->
    <el-dialog
      v-model="showDetailModal"
      title="订单详情"
      width="600px"
      custom-class="glass-dialog"
      align-center
    >
      <div v-if="selectedOrder" class="detail-content">
        <!-- 状态步骤条 -->
        <el-steps :active="getStepActive(selectedOrder.status)" align-center finish-status="success" class="mb-4">
          <el-step title="已下单"></el-step>
          <el-step title="已支付"></el-step>
          <el-step title="已发货"></el-step>
          <el-step title="已完成"></el-step>
        </el-steps>

        <div class="info-grid">
          <div class="info-item">
            <label>收货人</label> <span>{{ selectedOrder.receiver }}</span>
          </div>
          <div class="info-item">
            <label>联系电话</label> <span>{{ selectedOrder.receiver_phone }}</span>
          </div>
          <div class="info-item full">
            <label>收货地址</label> <span>{{ selectedOrder.receiver_address }}</span>
          </div>
          <div class="info-item full" v-if="selectedOrder.remark">
             <label>备注</label> <span class="text-muted">{{ selectedOrder.remark }}</span>
          </div>
        </div>

        <div class="product-list mt-3">
          <div v-for="item in selectedOrder.items" :key="item.product_id" class="detail-item">
            <img :src="fixImageUrl(item.image_url)" class="detail-thumb">
            <div class="detail-info">
              <div class="name">{{ item.product_name }}</div>
              <div class="price">¥{{ item.unit_price }} x {{ item.quantity }}</div>
            </div>
            <div class="total">¥{{ (item.unit_price * item.quantity).toFixed(2) }}</div>
          </div>
        </div>
        
        <div class="detail-footer mt-4">
          <div class="total-bar">
            <span>实付合计:</span>
            <span class="final-price">¥{{ selectedOrder.total_amount }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDetailModal = false">关闭</el-button>
           <el-button 
            v-if="selectedOrder && ['已支付', '已发货'].includes(selectedOrder.status)"
            type="warning"
            @click="handleRefund(selectedOrder)"
          >申请退款</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

// 状态定义
const filters = ref({ keyword: '', status: '' })
const showDetailModal = ref(false)
const selectedOrder = ref(null)
const allOrders = ref([])
const loading = ref(false)

const statusTabs = [
  { label: '全部', value: '' },
  { label: '待支付', value: '待支付' },
  { label: '已支付', value: '已支付' },
  { label: '待收货', value: '已发货' },
  { label: '已完成', value: '已完成' },
  { label: '退款/售后', value: '退款中' } // 修正后端可能的状态值
]

// 数据获取
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const fetchOrders = async () => {
  loading.value = true
  try {
    const res = await axios.get('http://localhost:5000/api/orders')
    allOrders.value = res.data
  } catch (err) {
    console.error(err)
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})

// 计算属性
const filteredOrders = computed(() => {
  const { keyword, status } = filters.value
  if (!allOrders.value) return []
  
  return allOrders.value.filter(order => {
    const k = keyword.toLowerCase()
    const keywordMatch = !keyword || 
      (order.order_no && order.order_no.toLowerCase().includes(k)) ||
      (order.items && order.items.some(i => i.product_name && i.product_name.toLowerCase().includes(k)))
    
    // 状态筛选逻辑：如果是'退款中'，可能还需要匹配 '已退款'
    let statusMatch = true
    if (status) {
        if (status === '退款中') {
             statusMatch = ['已退款', '退款审核中', '退款被拒绝'].includes(order.status)
        } else {
             statusMatch = order.status === status
        }
    }
    
    return keywordMatch && statusMatch
  })
})

// 交互方法
const selectStatus = (val) => filters.value.status = val
const handleSearch = () => {/* 可以加个防抖，目前直接计算属性处理 */}
const viewOrder = (order) => {
  selectedOrder.value = order
  showDetailModal.value = true
}

// 业务操作
const deleteOrder = async (order) => {
  try {
    await axios.delete(`http://localhost:5000/api/orders/${order.id}`)
    ElMessage.success('订单已删除')
    fetchOrders()
  } catch(e) { ElMessage.error('删除失败，可能订单状态不允许') }
}

const confirmReceive = async (order) => {
   try {
    await axios.post(`http://localhost:5000/api/orders/${order.id}/confirm`)
    ElMessage.success('确认收货成功')
    fetchOrders()
    // 关闭弹窗如果开着
    showDetailModal.value = false
  } catch(e) { ElMessage.error('操作失败') }
}

const handleRefund = async (order) => {
    if(!confirm('确认申请退款吗？')) return
    try {
        const res = await fetch(`http://localhost:5000/api/orders/${order.id}/refund`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        const d = await res.json()
        if(res.ok) {
            ElMessage.success(d.message)
            fetchOrders()
            showDetailModal.value = false
        } else {
            ElMessage.error(d.message)
        }
    } catch(e) { ElMessage.error('网络错误') }
}

// 工具函数
const formatDate = (str) => dayjs(str).format('YYYY-MM-DD HH:mm')
const fixImageUrl = (url) => {
  if (!url) return 'https://via.placeholder.com/100'
  return url.startsWith('http') ? url : `http://localhost:5000${url}`
}
const getStatusType = (status) => {
  const map = {
    '已支付': 'primary',
    '已发货': 'warning',
    '已完成': 'success',
    '已取消': 'info',
    '已退款': 'danger'
  }
  return map[status] || ''
}
const getStepActive = (status) => { 
    if(status === '待支付') return 0
    if(status === '已支付') return 1
    if(status === '已发货') return 2
    if(status === '已完成') return 3
    return 1 
}
</script>

<style scoped>
/* 容器 */
.order-page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

/* 顶部筛选栏 */
.filter-glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 16px 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid rgba(255,255,255,0.8);
}

/* Tabs */
.status-tabs {
  display: flex;
  gap: 8px;
  background: #f1f2f6;
  padding: 4px;
  border-radius: 10px;
}
.tab-btn {
  border: none;
  background: transparent;
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}
.tab-btn.active {
  background: #fff;
  color: #ff758c;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  font-weight: 500;
}

/* 订单卡片 */
.order-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.order-card {
  background: rgba(255, 255, 255, 0.85);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255,255,255,0.6);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  background: #fff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 12px;
  margin-bottom: 12px;
}
.order-no {
  font-weight: 600;
  color: #333;
  margin-right: 12px;
}
.order-time {
  color: #999;
  font-size: 12px;
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.product-preview {
  display: flex;
  gap: 12px;
}
.product-thumb {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #eee;
}
.thumb-img {
  width: 100%;
  height: 100%;
}
.item-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(0,0,0,0.6);
  color: #fff;
  font-size: 10px;
  padding: 0 4px;
  border-top-left-radius: 4px;
}
.more-items {
  width: 60px;
  height: 60px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
  font-weight: bold;
}

.price-info {
  text-align: right;
}
.price-info .label {
  display: block;
  font-size: 12px;
  color: #888;
}
.price-info .amount {
  font-size: 20px;
  color: #ff758c;
  font-weight: bold;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px dashed #eee;
}

/* 详情弹窗 */
.detail-content {
  padding: 10px;
}
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  background: #f9fafc;
  padding: 16px;
  border-radius: 8px;
}
.info-item {
  font-size: 14px;
}
.info-item.full {
  grid-column: span 2;
}
.info-item label {
  color: #888;
  margin-right: 8px;
}
.detail-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.detail-thumb {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  margin-right: 12px;
  object-fit: cover;
}
.detail-info {
  flex: 1;
}
.detail-info .name { font-size: 14px; font-weight: 500; }
.detail-info .price { font-size: 12px; color: #999; margin-top: 4px; }
.total-bar {
  display: flex;
  justify-content: flex-end;
  align-items: baseline;
  font-size: 16px;
}
.final-price {
  font-size: 24px;
  color: #ff758c;
  font-weight: bold;
  margin-left: 8px;
}
</style>