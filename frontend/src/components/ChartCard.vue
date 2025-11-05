<template>
  <div class="dashboard-container">
    <h4><i :class="'bi bi-' + icon"></i> {{ title }}</h4>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'ChartCard',
  props: {
    title: String,
    icon: String
  }
}
</script>

<style scoped>
.dashboard-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  padding: 30px;
  height: 100%;
}

h4 {
  margin-bottom: 20px;
  font-weight: 600;
}
</style>