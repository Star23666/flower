<script setup>
// 商品管理页面（全用 Vuex 管理数据）
// --------------------------------------------
// 1. 商品列表、增删改查全部用 Vuex actions
// 2. 表格数据直接绑定 Vuex state
// 3. 分类数据动态获取
// 4. 关键代码处均有注释
// --------------------------------------------

import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from 'vuex'
import { Plus } from '@element-plus/icons-vue'

function handleUploadSuccess(response) {
  currentProduct.value.image_url = response.url
}
function beforeUpload(file) {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isJpgOrPng) {
    ElMessage.error('只能上传 JPG/PNG 图片!')
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
  }
  return isJpgOrPng && isLt2M
}
const store = useStore()

// 控制新增/编辑弹窗
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentProduct = ref({
  id: null,
  name: '',
  price: 0,
  stock: 0,
  category_id: null,
  description: '',
  image_url: ''
})

// 商品表格数据，直接绑定 Vuex state
const products = computed(() => store.state.sellerProducts)
// 分类数据，直接绑定 Vuex state
const categories = computed(() => store.state.categories)

// 页面加载时获取商家商品和分类
onMounted(() => {
  store.dispatch('fetchSellerProducts')
  store.dispatch('fetchCategories')
})

// 打开新增商品弹窗
const onAddProduct = () => {
  isEdit.value = false
  currentProduct.value = {
    id: null,
    name: '',
    price: 0,
    stock: 0,
    category_id: null,
    description: '',
    image_url: ''
  }
  dialogVisible.value = true
}

// 打开编辑商品弹窗
const onEdit = (row) => {
  isEdit.value = true
  currentProduct.value = { ...row }
  dialogVisible.value = true
}

// 删除商品（带二次确认）
const onDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除商品「${row.name}」吗？`,
    '提示',
    { type: 'warning' }
  ).then(async () => {
    try {
      await store.dispatch('deleteProduct', row.id)
      ElMessage.success('删除成功')
    } catch (e) {
      // 这里根据后端返回的 message 精准提示
      if (e && e.message && e.message.includes('已有订单')) {
        ElMessage.error('该商品已有订单，无法删除！')
      } else {
        ElMessage.error(e.message || '删除失败')
      }   
    }
  }).catch(() => {})
}

// 上传图片成功后的处理函数，生成图片的完整访问 URL
function getImageUrl(url) {
   // 如果已经是 http 开头（绝对路径），直接返回
  if (!url) return ''
  if (url.startsWith('http')) return url
   // 否则拼接后端服务器地址，生成完整访问路径
  return 'http://localhost:5000' + url
}
// 保存商品（新增或编辑）
const onSave = async () => {
  try {
    if (isEdit.value) {
      await store.dispatch('updateProduct',currentProduct.value)
      ElMessage.success('修改成功')
    } else {
      await store.dispatch('addProduct',currentProduct.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}
</script>

<template>
  <div class="product-manage">
    <!-- 工具栏：新增按钮 -->
    <div class="toolbar">
      <el-button type="success" @click="onAddProduct" class="toolbar-item">+ 添加商品</el-button>
    </div>

    <!-- 商品表格 -->
    <el-table :data="products" border style="width: 100%; margin-top: 16px;">
      <el-table-column prop="name" label="鲜花名称" />
      <el-table-column prop="category_id" label="类别">
        <template #default="scope">
          <!-- 分类名映射 -->
          <span>
            {{ categories.find(cat => cat.id === scope.row.category_id)?.name || '未知' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="image_url" label="鲜花图片" width="100">
        <template #default="scope">
           <!-- 通过 getImageUrl 方法拼接图片完整地址，保证图片能正常显示 -->
          <el-image :src="getImageUrl(scope.row.image_url)" style="width: 60px; height: 60px;" fit="cover" />
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
  <template #default="scope">
    <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
      {{ scope.row.status === 'active' ? '上架' : '下架' }}
    </el-tag>
  </template>
</el-table-column>
      <el-table-column prop="stock" label="库存" />
      <el-table-column prop="price" label="售价" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" type="primary" @click="onEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑商品弹窗表单 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '新增商品'"
      width="500px"
    >
      <el-form :model="currentProduct" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="currentProduct.name" />
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="currentProduct.category_id" placeholder="请选择类别">
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
  <el-select v-model="currentProduct.status">
    <el-option label="上架" value="active" />
    <el-option label="下架" value="inactive" />
  </el-select>
</el-form-item>
        <el-form-item label="图片">
        <el-upload
    class="avatar-uploader"
    action="http://localhost:5000/api/upload/image"
    :show-file-list="false"
    :on-success="handleUploadSuccess"
    :before-upload="beforeUpload"
    name="file"
  >
    <img v-if="currentProduct.image_url" :src="currentProduct.image_url" class="avatar" />
    <el-icon v-else><Plus /></el-icon>
  </el-upload>
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="currentProduct.stock" :min="0" />
        </el-form-item>
        <el-form-item label="售价">
          <el-input-number v-model="currentProduct.price" :min="0" :step="0.01" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="currentProduct.description" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.product-manage {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  min-height: 600px;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.toolbar-item {
  min-width: 120px;
}
</style>