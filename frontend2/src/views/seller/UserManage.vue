<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { Plus } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
const store = useStore()
const searchText = ref('')
const editDialogVisible = ref(false)

const getAvatarUrl = (avatar) => {
  // 如果后端返回的是相对路径
  if (!avatar) return '';
  if (avatar.startsWith('http')) return avatar;
  return 'http://localhost:5000' + avatar;
}
// 1. 绑定 users
const users = computed(() => store.state.users)

// 2. 搜索过滤
const filteredUsers = computed(() => {
  if (!searchText.value) return users.value
  return users.value.filter(
    u =>
      (u.username && u.username.includes(searchText.value)) ||
      (u.email && u.email.includes(searchText.value))
  )
})

// 3. 页面加载时获取用户
onMounted(() => {
  store.dispatch('fetchUsers')
})

function onSearch() {
  store.dispatch('fetchUsers', searchText.value)
}

function onAddUser() {
  editDialogVisible.value = true
}
// 当前编辑的用户数据
const editForm = ref({
  id: null,
  username: '',
  email: '',
  gender: '',
  phone: '',
  avatar: ''
})

// 打开编辑弹窗，并填充表单
function onEdit(row) {
  // 复制当前行数据到编辑表单
  editForm.value = { ...row }
  editDialogVisible.value = true
}

// 保存编辑
async function onEditSave() {
  try {
    console.log('点击了保存', editForm.value)
    // 这里可以做表单校验
    await store.dispatch('updateUser', editForm.value)
    ElMessage.success('保存成功')
    editDialogVisible.value = false
    store.dispatch('fetchUsers')
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  }
}
async function onDelete(row) {

  try {
    console.log('删除用户', row)
    await ElMessageBox.confirm(
      `确定要删除用户「${row.username}」吗？此操作不可撤销！`,
      '警告',
      { type: 'warning' }
    )
    // 调用 Vuex action 或直接发请求
    await store.dispatch('deleteUser', row.id)
    ElMessage.success('删除成功')
    // 重新拉取用户列表
    store.dispatch('fetchUsers')
  } catch (e) {
    ElMessage.error(e.message || '删除失败')
  }
}
</script>


<template>
  <div class="user-manage">
    <!-- 工具栏 -->
    <el-card class="toolbar-card">
      <el-input
        v-model="searchText"
        placeholder="搜索用户名/邮箱"
        style="width: 220px; margin-right: 12px;"
        clearable
        @keyup.enter="onSearch"
      />
      <el-button type="primary" @click="onAddUser">
        <el-icon><Plus /></el-icon> 新增用户
      </el-button>
    </el-card>

    <!-- 用户表格 -->
    <el-card class="table-card">
      <el-table :data="filteredUsers" border stripe style="width: 100%">
        <el-table-column prop="avatar" label="头像" width="70">
          <template #default="scope">
            <img v-if="scope.row.avatar" 
            :src="getAvatarUrl(scope.row.avatar)"  
            style="width:40px;height:40px;border-radius:50%;object-fit:cover"/>
            <span v-else style="color:#ccc;">无</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色">
          <template #default="scope">
            <el-tag :type="scope.row.role==='admin'?'danger':'success'">
              {{ scope.row.role }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="gender" label="性别" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="created_at" label="注册时间" />
        <el-table-column label="操作" width="160">
          <template #default="scope">
            <el-button size="small" @click="onEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="400px">
  <el-form :model="editForm" label-width="80px">
    <el-form-item label="用户名">
      <el-input v-model="editForm.username" />
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="editForm.email" />
    </el-form-item>
    <el-form-item label="性别">
      <el-select v-model="editForm.gender">
        <el-option label="男" value="男" />
        <el-option label="女" value="女" />
      </el-select>
    </el-form-item>
    <el-form-item label="电话">
      <el-input v-model="editForm.phone" />
    </el-form-item>
    <!-- 头像、角色等可选 -->
  </el-form>
  <template #footer>
    <el-button @click="editDialogVisible = false">取消</el-button>
    <el-button type="primary" @click="onEditSave">保存</el-button>
  </template>
</el-dialog>
  </div>
</template>
<style scoped>
.user-manage {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}
.toolbar-card {
  margin-bottom: 20px;
  background: #fff;
}
.table-card {
  background: #fff;
}
</style>