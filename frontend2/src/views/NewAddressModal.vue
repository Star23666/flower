<template>
  <el-dialog
    v-model="visible"
    title="新增收货地址"
    width="520px"
    destroy-on-close
    :close-on-click-modal="false"
    append-to-body
    @closed="handleClosed"
  >
    <div class="modal-instruction">
      <el-alert
        title="请确保地址信息真实有效，以便商品能够顺利送达"
        type="info"
        show-icon
        :closable="false"
        style="margin-bottom: 20px;"
      />
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="90px"
      class="address-form"
      status-icon
    >
      <el-form-item label="收货人" prop="realname">
        <el-input 
          v-model="form.realname" 
          placeholder="请输入收货人姓名"
          prefix-icon="User"
          clearable
        />
      </el-form-item>

      <el-form-item label="手机号码" prop="phone">
        <el-input 
          v-model="form.phone" 
          placeholder="请输入11位手机号码" 
          maxlength="11"
          prefix-icon="Iphone"
          clearable
        />
      </el-form-item>

      <el-form-item label="详细地址" prop="address">
        <el-input 
          v-model="form.address" 
          type="textarea" 
          :rows="3"
          placeholder="请输入省、市、区、街道及楼牌号等" 
          resize="none"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :loading="loading" @click="submitForm">保存地址</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Iphone } from '@element-plus/icons-vue'

// 定义事件
const emit = defineEmits(['success', 'close'])

// 控制弹窗显示（默认 true，因为外部是用 v-if 控制组件的）
const visible = ref(true)
const loading = ref(false)
const formRef = ref(null)

// 表单数据
const form = reactive({
  realname: '',
  phone: '',
  address: ''
})

// 验证规则
const rules = {
  realname: [
    { required: true, message: '请输入收货人姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号码格式不正确', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入详细地址', trigger: 'blur' },
    { min: 5, message: '地址长度不能少于5个字符', trigger: 'blur' }
  ]
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://localhost:5000/api/user/addresses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(form)
        })
        
        const data = await res.json()
        
        if (res.ok) {
          ElMessage.success('地址添加成功')
          // 发送成功事件，并传回新地址ID或对象，方便父组件更新列表
          emit('success', { ...form, id: data.id })
          visible.value = false
        } else {
          ElMessage.error(data.message || '保存失败')
        }
      } catch (error) {
        console.error(error)
        ElMessage.error('网络错误，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}

// 弹窗完全关闭后触发
const handleClosed = () => {
  emit('close')
}
</script>

<style scoped>
.address-form {
  padding: 0 10px;
}
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>