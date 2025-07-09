<script setup>

import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from 'vuex'

const store = useStore()

// 分类列表
const categoryList = ref([])
// 编辑弹窗显示
const editDialogVisible = ref(false)
// 当前编辑的分类
const editForm = ref({ id: null, name: '' })

// 获取分类列表
async function fetchCategories() {
  // 假设有 vuex action: fetchCategories
  await store.dispatch('fetchCategories')
  categoryList.value = store.state.categoryList
}

// 新增分类
function onAddCategory() {
  editForm.value = { id: null, name: '' }
  editDialogVisible.value = true
}

// 编辑分类
function onEdit(row) {
  editForm.value = { ...row }
  editDialogVisible.value = true
}

// 保存编辑/新增
async function onEditSave() {
  try {
    if (editForm.value.id) {
      await store.dispatch('updateCategory', editForm.value)
      ElMessage.success('编辑成功')
    } else {
      await store.dispatch('addCategory', editForm.value)
      ElMessage.success('新增成功')
    }
    editDialogVisible.value = false
    fetchCategories()
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}

// 删除分类
async function onDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除分类「${row.name}」吗？`, '警告', { type: 'warning' })
    await store.dispatch('deleteCategory', row.id)
    ElMessage.success('删除成功')
    fetchCategories()
  } catch (e) {
    ElMessage.error(e.message || '删除失败')
  }
}

onMounted(fetchCategories)

</script>

<template>
    <div>
      <el-button type="primary" @click="onAddCategory" style="margin-bottom: 16px;">新增分类</el-button>
      <el-table :data="categoryList" border stripe style="width: 100%">
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="name" label="鲜花类型" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" @click="onEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 编辑/新增弹窗 -->
      <el-dialog v-model="editDialogVisible" :title="editForm.id ? '编辑分类' : '新增分类'" width="400px">
        <el-form :model="editForm" label-width="80px">
          <el-form-item label="类型名称">
            <el-input v-model="editForm.name" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="onEditSave">保存</el-button>
        </template>
      </el-dialog>
    </div>
  </template>