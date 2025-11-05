<template>
  <div class="dashboard-container loading">
    <div class="spinner-border text-primary" role="status"></div>
    <p class="mt-3">正在加载数据...</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner'
}
</script>

<style scoped>
.dashboard-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  padding: 30px;
  margin-bottom: 30px;
}

.loading {
  text-align: center;
  padding: 50px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>