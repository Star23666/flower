<template>
  <!-- 关键修改：添加 append-to-body 属性，防止被父组件样式限制 -->
  <el-drawer
    v-model="visible"
    title="确认订单"
    direction="rtl"
    size="500px"
    :before-close="handleClose"
    class="checkout-drawer"
    append-to-body 
  >
    <div class="checkout-content">
      <!-- 1. 收货地址部分 -->
      <div class="section-block">
        <h4 class="section-title">
          <el-icon><Location /></el-icon> 收货地址
        </h4>
        
        <div v-if="!addresses || addresses.length === 0" class="empty-address">
          <el-empty description="暂无地址" :image-size="80">
            <el-button type="primary" size="small" @click="$router.push('/user/profile')">去添加地址</el-button>
          </el-empty>
        </div>

        <div v-else class="address-grid">
          <div 
            v-for="addr in addresses" 
            :key="addr.id" 
            class="address-card"
            :class="{ active: selectedAddressId === addr.id }"
            @click="selectedAddressId = addr.id"
          >
            <div class="card-header">
              <span class="name">{{ addr.realname }}</span>
              <span class="phone">{{ addr.phone }}</span>
            </div>
            <div class="card-body">
              {{ addr.address }}
            </div>
            <div class="check-mark" v-if="selectedAddressId === addr.id">
              <el-icon><Check /></el-icon>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. 商品清单部分 -->
      <div class="section-block">
        <h4 class="section-title">
          <el-icon><Goods /></el-icon> 商品清单
        </h4>
        <div class="goods-list">
          <div v-for="item in cart" :key="item.id" class="goods-item">
            <el-image :src="getProductImage(item)" class="goods-img" fit="cover" />
            <div class="goods-info">
              <div class="goods-name">{{ item.name }}</div>
              <div class="goods-meta">
                <span class="price">¥{{ item.price }}</span>
                <span class="count">x {{ item.quantity }}</span>
              </div>
            </div>
            <div class="goods-total">
              ¥{{ (item.price * item.quantity).toFixed(2) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 3. 备注与优惠 -->
      <div class="section-block">
        <div class="form-item">
          <span class="label">订单备注</span>
          <el-input 
            v-model="remark" 
            placeholder="选填，请先与商家协商一致" 
            type="textarea" 
            :rows="2"
          />
        </div>
      </div>

    </div>

    <!-- 底部固定结算栏 -->
    <template #footer>
      <div class="drawer-footer">
        <div class="price-summary">
          <div class="row-item">
            <span>商品总价:</span>
            <span>¥{{ Number(total).toFixed(2) }}</span>
          </div>
          <div class="row-item balance" :class="{ 'text-danger': balance < total }">
            <span>当前余额:</span>
            <span>¥{{ Number(balance).toFixed(2) }}</span>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button @click="handleClose">取消</el-button>
          <el-button 
            type="primary" 
            color="#ff758c" 
            class="pay-btn"
            :loading="loading"
            :disabled="!selectedAddressId || hasLowBalance"
            @click="pay"
          >
            {{ hasLowBalance ? '余额不足' : '立即支付' }}
          </el-button>
        </div>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
/* global defineProps, defineEmits */
import { ref, computed, watch } from 'vue'
import { Check, Location, Goods } from '@element-plus/icons-vue'

const props = defineProps(['cart', 'total', 'addresses', 'balance'])
const emit = defineEmits(['close', 'pay'])

// 控制抽屉显示（父组件通过 v-if 控制组件挂载，这里直接设为 true 即可）
const visible = ref(true)

const selectedAddressId = ref(null)
const remark = ref('')
const loading = ref(false)

// 初始化选中第一个地址
watch(() => props.addresses, (newVal) => {
  if (newVal && newVal.length > 0 && !selectedAddressId.value) {
    selectedAddressId.value = newVal[0].id
  }
}, { immediate: true })

const hasLowBalance = computed(() => {
  return Number(props.balance) < Number(props.total)
})

const getProductImage = (item) => {
  if (!item.image_url) return 'https://via.placeholder.com/100'
  return item.image_url.startsWith('http') ? item.image_url : `http://localhost:5000${item.image_url}`
}

const handleClose = () => {
  visible.value = false
  setTimeout(() => emit('close'), 300) // 等待动画结束
}

const pay = async () => {
  loading.value = true
  // 模拟网络延迟感
  await new Promise(r => setTimeout(r, 500))
  emit('pay', { addressId: selectedAddressId.value, remark: remark.value })
  loading.value = false
}
</script>

<style scoped>
/* 关键修复：强制让 Drawer 的主体内容区域可以滚动 */
:deep(.el-drawer__body) {
  overflow-y: auto !important;
  /* 增加底部内边距，防止内容被底部按钮遮挡 */
  padding-bottom: 20px; 
}

/* 整个抽屉内容区 */
.checkout-content {
  padding: 0 10px;
}

.section-block {
  margin-bottom: 30px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

/* 地址卡片样式 */
.address-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.address-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 12px 16px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
  background: #fff;
}

.address-card:hover {
  border-color: #ffb6c1;
  background: #fffdfd;
}

.address-card.active {
  border-color: #ff758c;
  background: #fff0f3;
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-weight: 500;
  color: #303133;
}

.card-body {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

.check-mark {
  position: absolute;
  right: 0;
  bottom: 0;
  background: #ff758c;
  color: white;
  padding: 2px 6px;
  border-top-left-radius: 8px;
  border-bottom-right-radius: 8px;
  font-size: 12px;
}

/* 商品列表样式 */
.goods-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
}

.goods-img {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  background: #fff;
}

.goods-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 60px;
}

.goods-name {
  font-size: 14px;
  color: #333;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.goods-meta {
  font-size: 12px;
  color: #999;
}

.goods-total {
  font-weight: bold;
  color: #333;
}

/* 底部结算栏 */
.drawer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-summary {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

.row-item {
  display: flex;
  gap: 10px;
}

.row-item span:first-child {
  color: #666;
}
.row-item span:last-child {
  font-weight: bold;
}

.balance.text-danger span:last-child {
  color: #f56c6c;
}

.pay-btn {
  width: 120px;
  font-weight: bold;
  font-size: 15px;
}
</style>