<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { Plus } from '@element-plus/icons-vue'

const store = useStore()
const searchText = ref('')
const editDialogVisible = ref(false)
const defaultAvatar = 'https://img1.baidu.com/it/u=1234567890,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=200&h=200'

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
// function onEdit(row) {
//   editDialogVisible.value = true
// }
// function onDelete(row) {
//   // 删除逻辑（待实现）
// }
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
            <el-avatar :src="scope.row.avatar || defaultAvatar" />
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
            <el-button size="small" type="danger" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="400px">
      <!-- 表单内容... -->
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