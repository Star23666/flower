<template>
    <nav aria-label="breadcrumb" class="breadcrumb-bar" style="margin-bottom: 18px;">
      <ol class="breadcrumb">
        <li v-for="(item, idx) in breadcrumbs" :key="idx" class="breadcrumb-item" :class="{ active: idx === breadcrumbs.length - 1 }">
          <template v-if="idx !== breadcrumbs.length - 1">
            <router-link :to="{ path: item.path, query: item.query }">{{ item.label }}</router-link>
          </template>
          <template v-else>
            {{ item.label }}
          </template>
        </li>
      </ol>
    </nav>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const breadcrumbs = computed(() => {
    const arr = []
    if (route.name === 'ProductDetail') {
      if (route.query.from === 'favorites') {
        arr.push({ path: '/user/profile', label: '我的收藏', query: { menu: 'favorites' } })
      } else {
        arr.push({ path: '/products', label: '商品' })
      }
      arr.push({ path: route.fullPath, label: route.meta.breadcrumb || '详情' })
      return arr
    }
    return route.matched
      .filter(r => r.meta && r.meta.breadcrumb)
      .map(r => ({
        path: r.path.startsWith('/') ? r.path : '/' + r.path,
        label: r.meta.breadcrumb
      }))
  })
  </script>

<script>

export default {
  name: 'AppBreadcrumbs'
}
</script>