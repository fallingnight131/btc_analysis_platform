<template>
  <div class="page-header">
    <div class="row align-items-center">
      <div class="col-md-8">
        <h1 class="mb-0">
          <i class="bi bi-currency-bitcoin text-warning"></i>
          比特币实时数据分析平台
        </h1>
        <p class="text-muted mb-0 mt-2">
          <i class="bi bi-clock"></i> 最后更新: {{ lastUpdate }}
        </p>
      </div>
      <div class="col-md-4 text-end">
        <button class="btn btn-primary" @click="$emit('refresh')" :disabled="loading">
          <i class="bi bi-arrow-clockwise" :class="{ 'spin': loading }"></i> 
          刷新数据
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    lastUpdate: String,
    loading: Boolean
  }
}
</script>

<style scoped>
.page-header {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

h1 {
  font-size: 1.8rem;
  font-weight: 700;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>