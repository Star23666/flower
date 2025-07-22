<template>
    <div class="modal show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">新建收货地址</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <p>新建地址弹窗开发中</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="$emit('close')">关闭</button>
            <button class="btn btn-primary" @click="$emit('success', 1)">模拟保存</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  export default { emits: ['success', 'close'] }
  </script>