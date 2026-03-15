<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from 'vuex'
import { 
  Plus, 
  Search, 
  Edit, 
  Delete, 
  Picture,
  UploadFilled
} from '@element-plus/icons-vue'

const store = useStore()

// ------------------------------------------------
// 状态管理
// ------------------------------------------------
const dialogVisible = ref(false)
const isEdit = ref(false)
const searchText = ref('')
const currentProduct = ref({
  id: null,
  name: '',
  price: 0,
  stock: 0,
  category_id: null,
  description: '',
  image_url: '',
  target: '',
  status: 'active'
})

// ------------------------------------------------
// 数据绑定 & 计算属性
// ------------------------------------------------
// 分类数据
const categories = computed(() => store.state.categories)

// 商品数据 (含前端搜索)
const products = computed(() => {
  const list = store.state.sellerProducts
  if (!searchText.value) return list
  
  const text = searchText.value.trim().toLowerCase()
  return list.filter(p => 
    (p.name && p.name.toLowerCase().includes(text)) ||
    (p.description && p.description.toLowerCase().includes(text))
  )
})

// 辅助：获取分类名称
const getCategoryName = (id) => {
  const cat = categories.value.find(c => String(c.id) === String(id))
  return cat ? cat.name : '未分类'
}

// 辅助：获取图片完整URL
function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return 'http://localhost:5000' + url
}

// ------------------------------------------------
// 核心逻辑 (保持原有功能不变)
// ------------------------------------------------
onMounted(() => {
  store.dispatch('fetchSellerProducts')
  store.dispatch('fetchCategories')
})

function onSearch() {
  // 触发 computed 更新
}

// 打开新增弹窗
const onAddProduct = () => {
  isEdit.value = false
  currentProduct.value = {
    id: null, name: '', price: 0, stock: 100, category_id: null,
    description: '', image_url: '', target: '', status: 'active'
  }
  dialogVisible.value = true
}

// 打开编辑弹窗
const onEdit = (row) => {
  isEdit.value = true
  currentProduct.value = { ...row } // 浅拷贝
  dialogVisible.value = true
}

// 保存逻辑
const onSave = async () => {
  try {
    let categoryId = currentProduct.value.category_id;
    // 支持直接输入新分类名（虽然 UI 上是 Select，但逻辑保留）
    if (typeof categoryId === 'string' && categoryId) {
      const res = await store.dispatch('addCategory', { name: categoryId });
      categoryId = res.id;
    }
    currentProduct.value.category_id = categoryId;

    if (isEdit.value) {
      await store.dispatch('updateProduct', currentProduct.value)
      ElMessage.success('商品已更新')
    } else {
      await store.dispatch('addProduct', currentProduct.value)
      ElMessage.success('商品已发布')
    }
    dialogVisible.value = false
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}

// 删除逻辑
const onDelete = (row) => {
  ElMessageBox.confirm(
    `确定要下架并删除商品「${row.name}」吗？`,
    '风险操作',
    { type: 'warning', confirmButtonText: '确定删除', cancelButtonText: '取消' }
  ).then(async () => {
    try {
      await store.dispatch('deleteProduct', row.id)
      ElMessage.success('删除成功')
    } catch (e) {
      if (e && e.message && e.message.includes('已有订单')) {
        ElMessage.error('该商品已有关联订单，无法直接删除！')
      } else {
        ElMessage.error(e.message || '删除失败')
      }   
    }
  }).catch(() => {})
}

// 图片上传钩子
function handleUploadSuccess(response) {
  currentProduct.value.image_url = response.url
  ElMessage.success('图片上传成功')
}
function beforeUpload(file) {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isJpgOrPng) ElMessage.error('请上传 JPG/PNG 格式图片')
  if (!isLt2M) ElMessage.error('图片大小不能超过 2MB')
  
  return isJpgOrPng && isLt2M
}
</script>

<template>
  <div class="page-container">
    
    <!-- 顶部工具栏 -->
    <div class="toolbar-wrapper">
      <div class="left-panel">
        <h2 class="page-title">商品管理 <span class="sub-title">Product List</span></h2>
        <span class="count-badge">当前库存 {{ products.length }} 件商品</span>
      </div>
      
      <div class="right-panel">
        <el-input
          v-model="searchText"
          placeholder="搜索商品名称 / 描述"
          class="search-input"
          clearable
          @clear="onSearch"
          @keyup.enter="onSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-button type="primary" class="add-btn" @click="onAddProduct">
          <el-icon class="btn-icon"><Plus /></el-icon>
          发布商品
        </el-button>
      </div>
    </div>

    <!-- 商品数据表格 -->
    <div class="table-container">
      <el-table 
        :data="products" 
        style="width: 100%" 
        :header-cell-style="{ background: '#f8f9fb', color: '#606266', fontWeight: 'bold' }"
        row-class-name="product-row"
      >
        <!-- 主图与名称 -->
        <el-table-column label="商品信息" min-width="280">
          <template #default="{ row }">
            <div class="product-info-cell">
              <div class="img-wrapper">
                <el-image 
                  v-if="row.image_url"
                  :src="getImageUrl(row.image_url)" 
                  class="product-img" 
                  fit="cover"
                  preview-teleported
                  :preview-src-list="[getImageUrl(row.image_url)]"
                />
                <div v-else class="img-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
              </div>
              <div class="text-info">
                <div class="product-name" :title="row.name">{{ row.name }}</div>
                <div class="product-desc" :title="row.description">{{ row.description || '暂无描述' }}</div>
                <div class="product-tags">
                   <el-tag size="small" type="info" effect="plain">{{ getCategoryName(row.category_id) }}</el-tag>
                   <el-tag v-if="row.target" size="small" type="warning" effect="plain" style="margin-left: 4px;">{{ row.target }}</el-tag>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <!-- 价格 -->
        <el-table-column label="售价" width="120" align="right">
          <template #default="{ row }">
            <span class="price-text">¥ {{ row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>

        <!-- 库存 -->
        <el-table-column label="库存" width="120" align="center">
          <template #default="{ row }">
             <span :class="['stock-text', row.stock < 10 ? 'low-stock' : '']">
               {{ row.stock }}
             </span>
          </template>
        </el-table-column>

        <!-- 状态 -->
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
             <el-tag 
               :type="row.status === 'active' ? 'success' : 'info'" 
               effect="light" 
               round
             >
                <span class="dot" :class="row.status"></span>
                {{ row.status === 'active' ? '上架中' : '已下架' }}
             </el-tag>
          </template>
        </el-table-column>

        <!-- 操作 -->
        <el-table-column label="操作" width="150" align="right" fixed="right">
          <template #default="{ row }">
            <el-tooltip content="编辑商品" placement="top" :hide-after="0">
              <el-button 
                circle 
                plain 
                type="primary" 
                size="small" 
                @click="onEdit(row)"
              >
                <el-icon><Edit /></el-icon>
              </el-button>
            </el-tooltip>

            <el-tooltip content="删除/下架" placement="top" :hide-after="0">
              <el-button 
                circle 
                plain 
                type="danger" 
                size="small" 
                @click="onDelete(row)" 
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑 弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '发布新商品'"
      width="600px"
      align-center
      destroy-on-close
      class="custom-dialog"
    >
      <el-form :model="currentProduct" label-width="80px" class="edit-form" size="large">
        
        <!-- 图片上传区 -->
        <div class="upload-area">
          <el-upload
            class="avatar-uploader"
            action="http://localhost:5000/api/upload/image"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            name="file"
          >
            <div v-if="currentProduct.image_url" class="img-preview-box">
               <img :src="getImageUrl(currentProduct.image_url)" class="avatar" />
               <div class="hover-mask"><el-icon><Edit /></el-icon> 更换</div>
            </div>
            <div v-else class="upload-placeholder">
               <el-icon class="upload-icon"><UploadFilled /></el-icon>
               <span>点击上传主图</span>
               <div class="sub-tip">支持 JPG/PNG，小于 2MB</div>
            </div>
          </el-upload>
        </div>

        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="商品名称">
              <el-input v-model="currentProduct.name" placeholder="请输入鲜花名称" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
             <el-form-item label="状态">
                <el-select v-model="currentProduct.status">
                  <el-option label="上架" value="active" />
                  <el-option label="下架" value="inactive" />
                </el-select>
             </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
           <el-col :span="12">
             <el-form-item label="商品分类">
                <el-select 
                  v-model="currentProduct.category_id"
                  placeholder="选择或输入新分类"
                  filterable
                  allow-create
                  default-first-option
                  style="width: 100%"
                >
                  <el-option
                    v-for="cat in categories"
                    :key="cat.id"
                    :label="cat.name"
                    :value="cat.id"
                  />
                </el-select>
             </el-form-item>
           </el-col>
           <el-col :span="12">
             <el-form-item label="适用对象">
               <el-input v-model="currentProduct.target" placeholder="如：恋人、长辈" />
             </el-form-item>
           </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
             <el-form-item label="售价 (¥)">
               <el-input-number v-model="currentProduct.price" :min="0" :precision="2" :step="1" style="width: 100%" />
             </el-form-item>
          </el-col>
          <el-col :span="12">
             <el-form-item label="库存数量">
               <el-input-number v-model="currentProduct.stock" :min="0" :step="10" style="width: 100%" />
             </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="商品描述">
          <el-input 
            v-model="currentProduct.description" 
            type="textarea" 
            :rows="3" 
            placeholder="简要描述鲜花的特色、花语等..." 
          />
        </el-form-item>

      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="onSave" color="#409eff">保存商品</el-button>
        </div>
      </template>
    </el-dialog>
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
  margin-bottom: 24px;
}

.left-panel .page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.sub-title {
  font-size: 14px; color: #9ca3af; font-weight: 400;
}
.count-badge {
  display: inline-block; margin-top: 4px; font-size: 12px;
  background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 10px;
}

.right-panel {
  display: flex; gap: 16px; align-items: center;
}
.search-input { width: 220px; }
.search-input :deep(.el-input__wrapper) { border-radius: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.add-btn { border-radius: 8px; font-weight: 600; box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1); }
.btn-icon { margin-right: 6px; }

/* 表格样式 */
.table-container {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02), 0 1px 2px 0 rgba(0, 0, 0, 0.02);
  border: 1px solid #f3f4f6;
  padding-bottom: 8px;
  overflow: hidden;
}

/* 商品卡片单元格 */
.product-info-cell {
  display: flex; gap: 16px; align-items: flex-start; padding: 8px 0;
}
.img-wrapper {
  width: 64px; height: 64px; border-radius: 8px; overflow: hidden; border: 1px solid #e5e7eb;
  flex-shrink: 0;
}
.product-img { width: 100%; height: 100%; }
.img-placeholder {
  width: 100%; height: 100%; background: #f9fafb; display: flex;
  align-items: center; justify-content: center; color: #d1d5db; font-size: 20px;
}
.text-info { display: flex; flex-direction: column; gap: 4px; justify-content: center; min-width: 0; }
.product-name { font-weight: 600; color: #111827; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.product-desc { font-size: 12px; color: #6b7280; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 200px; }
.product-tags { margin-top: 2px; }

.price-text {
  font-family: 'DIN Alternate', sans-serif;
  font-weight: 700;
  color: #f56c6c;
  font-size: 16px;
}
.stock-text { font-family: monospace; color: #374151; }
.low-stock { color: #e6a23c; font-weight: bold; }

.dot {
  display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 4px;
}
.dot.active { background-color: #67c23a; }
.dot.inactive { background-color: #909399; }

/* 图片上传区美化 */
.upload-area {
  display: flex; justify-content: center; margin-bottom: 24px;
}
.avatar-uploader .el-upload {
  cursor: pointer; position: relative; overflow: hidden;
  transition: var(--el-transition-duration-fast);
}
.img-preview-box {
  width: 120px; height: 120px; border-radius: 8px; overflow: hidden; position: relative;
  border: 1px solid #e5e7eb;
}
.avatar { width: 100%; height: 100%; object-fit: cover; display: block; }
.hover-mask {
  position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5);
  color: #fff; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s;
  gap: 4px; font-size: 12px;
}
.img-preview-box:hover .hover-mask { opacity: 1; }

.upload-placeholder {
  width: 120px; height: 120px; border: 1px dashed #d9d9d9; border-radius: 8px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: #8c939d; background: #fafafa;
}
.upload-placeholder:hover { border-color: #409eff; color: #409eff; }
.upload-icon { font-size: 24px; margin-bottom: 8px; }
.sub-tip { font-size: 10px; margin-top: 4px; color: #9ca3af; }

</style>