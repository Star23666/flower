<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { 
  Plus, 
  Search, 
  Edit, 
  Delete, 
  UserFilled,
  Male,
  Female,
  Message,
  Iphone
} from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'

const store = useStore()
const searchText = ref('')
const editDialogVisible = ref(false)

// ------------------------------------------------
// 获取头像 URL，增加防错处理
// ------------------------------------------------
const getAvatarUrl = (avatar) => {
  if (!avatar) return '';
  if (avatar.startsWith('http')) return avatar;
  return 'http://localhost:5000' + avatar;
}

// ------------------------------------------------
// Store 数据绑定
// ------------------------------------------------
const users = computed(() => store.state.users)

// ------------------------------------------------
// 搜索过滤逻辑
// ------------------------------------------------
const filteredUsers = computed(() => {
  const text = searchText.value.trim().toLowerCase()
  if (!text) return users.value
  
  return users.value.filter(u => {
    const name = u.username ? u.username.toLowerCase() : ''
    const mail = u.email ? u.email.toLowerCase() : ''
    const phone = u.phone ? u.phone : ''
    return name.includes(text) || mail.includes(text) || phone.includes(text)
  })
})

// ------------------------------------------------
// 生命周期：加载数据
// ------------------------------------------------
onMounted(() => {
  store.dispatch('fetchUsers')
})

function onSearch() {
  store.dispatch('fetchUsers', searchText.value)
}

function onAddUser() {
  editForm.value = {
    id: null,
    username: '',
    email: '',
    gender: '保密',
    phone: '',
    role: 'user', // 默认角色
    avatar: ''
  }
  editDialogVisible.value = true
}

// 表单数据
const editForm = ref({
  id: null,
  username: '',
  email: '',
  gender: '',
  phone: '',
  role: '',
  avatar: ''
})

// 打开编辑
function onEdit(row) {
  editForm.value = { ...row }
  editDialogVisible.value = true
}

// 保存提交
async function onEditSave() {
  try {
    // 简单的非空校验
    if (!editForm.value.username) {
      ElMessage.warning('用户名不能为空')
      return
    }
    
    await store.dispatch('updateUser', editForm.value)
    ElMessage.success('保存成功')
    editDialogVisible.value = false
    // 刷新列表
    store.dispatch('fetchUsers')
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}

// 删除用户
async function onDelete(row) {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户「${row.username}」吗？此操作将无法撤销。`,
      '危险操作警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        icon: Delete
      }
    )
    await store.dispatch('deleteUser', row.id)
    ElMessage.success('用户已删除')
    store.dispatch('fetchUsers')
  } catch (e) {
    if (e !== 'cancel') {
       ElMessage.error(e.message || '删除失败')
    }
  }
}

// 辅助：获取性别图标颜色
const getGenderColor = (gender) => {
  if (gender === '男') return '#409eff'
  if (gender === '女') return '#f56c6c'
  return '#909399'
}
</script>

<template>
  <div class="page-container">
    
    <!-- 顶部工具栏 -->
    <div class="toolbar-wrapper">
      <div class="left-panel">
        <h2 class="page-title">用户管理 <span class="sub-title">User Management</span></h2>
        <span class="user-count">共 {{ filteredUsers.length }} 位用户</span>
      </div>
      
      <div class="right-panel">
        <el-input
          v-model="searchText"
          placeholder="搜索用户名 / 邮箱 / 电话"
          class="search-input"
          clearable
          @clear="onSearch"
          @keyup.enter="onSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-button type="primary" class="add-btn" @click="onAddUser">
          <el-icon class="btn-icon"><Plus /></el-icon>
          新增用户
        </el-button>
      </div>
    </div>

    <!-- 用户数据表格 -->
    <div class="table-container">
      <el-table 
        :data="filteredUsers" 
        style="width: 100%" 
        :header-cell-style="{ background: '#f8f9fb', color: '#606266', fontWeight: '600' }"
        highlight-current-row
      >
        <!-- 头像与用户名 -->
        <el-table-column label="用户" min-width="180">
          <template #default="{ row }">
            <div class="user-info-cell">
              <div class="avatar-wrapper">
                <el-avatar 
                  v-if="row.avatar" 
                  :size="44" 
                  :src="getAvatarUrl(row.avatar)"
                  class="custom-avatar"
                />
                <el-avatar v-else :size="44" class="fallback-avatar">
                   {{ row.username ? row.username.charAt(0).toUpperCase() : 'U' }}
                </el-avatar>
              </div>
              <div class="info-text">
                <div class="username-text">{{ row.username }}</div>
                <div class="id-text">ID: {{ row.id }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <!-- 角色 -->
        <el-table-column prop="role" label="角色" width="100" align="center">
          <template #default="{ row }">
            <el-tag 
              :type="row.role === 'admin' ? 'danger' : row.role === 'seller' ? 'warning' : ''" 
              effect="light"
              round
              size="small"
            >
              {{ row.role === 'admin' ? '管理员' : row.role === 'seller' ? '商家' : '会员' }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 性别 -->
        <el-table-column label="性别" width="80" align="center">
          <template #default="{ row }">
             <el-icon :color="getGenderColor(row.gender)" size="16">
               <Male v-if="row.gender === '男'" />
               <Female v-else-if="row.gender === '女'" />
               <UserFilled v-else />
             </el-icon>
          </template>
        </el-table-column>

        <!-- 联系方式 -->
        <el-table-column label="联系方式" min-width="200">
          <template #default="{ row }">
            <div class="contact-info">
              <div class="contact-item" v-if="row.email">
                <el-icon><Message /></el-icon> {{ row.email }}
              </div>
              <div class="contact-item" v-if="row.phone">
                <el-icon><Iphone /></el-icon> {{ row.phone }}
              </div>
              <div v-if="!row.email && !row.phone" class="no-contact">暂无联系方式</div>
            </div>
          </template>
        </el-table-column>

        <!-- 注册时间 -->
        <el-table-column prop="created_at" label="注册时间" width="180" sortable>
          <template #default="{ row }">
            <span class="date-text">{{ row.created_at || '未知' }}</span>
          </template>
        </el-table-column>

        <!-- 操作 -->
        <el-table-column label="操作" width="150" align="right" fixed="right">
          <template #default="{ row }">
            <el-tooltip content="编辑资料" placement="top" :hide-after="0">
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

            <el-tooltip content="删除用户" placement="top" :hide-after="0">
              <el-button 
                circle 
                plain 
                type="danger" 
                size="small" 
                @click="onDelete(row)" 
                :disabled="row.role === 'admin'"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 编辑/新增 弹窗 -->
    <el-dialog 
      v-model="editDialogVisible" 
      :title="editForm.id ? '编辑用户信息' : '新增用户'" 
      width="480px"
      align-center
      destroy-on-close
      class="custom-dialog"
    >
      <el-form :model="editForm" label-width="80px" class="edit-form" size="large">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" placeholder="example@flower.com" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-select v-model="editForm.gender" placeholder="选择性别" style="width: 100%">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
                <el-option label="保密" value="保密" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
             <el-form-item label="角色">
              <el-select v-model="editForm.role" placeholder="选择角色" style="width: 100%">
                <el-option label="普通会员" value="user" />
                <el-option label="商家" value="seller" />
                <el-option label="管理员" value="admin" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="手机号">
          <el-input v-model="editForm.phone" placeholder="请输入手机号码" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="onEditSave" color="#409eff">保 存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 页面容器：去除原有的 card 背景，使其更轻量融入 Dashboard */
.page-container {
  min-height: 100%;
}

/* 顶部工具栏 */
.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: transparent;
}

.left-panel .page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.sub-title {
  font-size: 14px;
  color: #9ca3af;
  font-weight: 400;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.user-count {
  display: block;
  margin-top: 4px;
  font-size: 13px;
  color: #6b7280;
}

.right-panel {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-input {
  width: 260px;
  transition: all 0.3s;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.add-btn {
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06);
}

.btn-icon {
  margin-right: 6px;
}

/* 表格容器 */
.table-container {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02), 0 1px 2px 0 rgba(0, 0, 0, 0.02);
  border: 1px solid #f3f4f6;
  overflow: hidden;
}

/* 用户信息单元格 */
.user-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-wrapper {
  position: relative;
}

.custom-avatar {
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.fallback-avatar {
  background-color: #e0e7ff;
  color: #4f46e5;
  font-weight: 700;
  border: 2px solid #fff;
}

.info-text {
  display: flex;
  flex-direction: column;
}

.username-text {
  font-weight: 600;
  color: #111827;
  font-size: 14px;
}

.id-text {
  font-size: 12px;
  color: #9ca3af;
}

/* 联系方式 */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-item {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #4b5563;
  gap: 6px;
}
.contact-item .el-icon {
  color: #9ca3af;
}

.no-contact {
  font-size: 12px;
  color: #d1d5db;
  font-style: italic;
}

.date-text {
  color: #6b7280;
  font-size: 13px;
  font-family: monospace;
}

/* 弹窗样式微调 */
.edit-form {
  padding: 10px 20px 0 0;
}

.dialog-footer {
  padding-top: 10px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .toolbar-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .right-panel {
    width: 100%;
    justify-content: space-between;
  }
  
  .search-input {
    width: 100%;
    max-width: 200px;
  }
}
</style>