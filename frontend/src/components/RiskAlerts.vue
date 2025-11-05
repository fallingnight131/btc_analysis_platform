<template>
  <div style="max-height: 400px; overflow-y: auto;">
    <div v-if="alerts.length === 0" class="text-center text-muted py-5">
      <i class="bi bi-check-circle" style="font-size: 48px;"></i>
      <p class="mt-3">暂无风险警报</p>
    </div>
    <div v-for="(alert, index) in alerts" :key="index" 
         class="alert-item" 
         :class="'alert-' + alert.severity">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <strong>{{ alert.message }}</strong>
          <div class="text-muted small">{{ alert.timestamp }}</div>
        </div>
        <span class="badge" 
              :class="alert.severity === 'high' ? 'bg-danger' : 'bg-warning'">
          {{ alert.severity }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiskAlerts',
  props: {
    alerts: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.alert-item {
  border-left: 4px solid;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
  background: #f8f9fa;
}

.alert-high {
  border-color: #dc3545;
}

.alert-medium {
  border-color: #ffc107;
}
</style>