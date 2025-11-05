<template>
  <div class="row">
    <div class="col-md-3">
      <div class="stat-card">
        <div class="stat-label">
          <i class="bi bi-cash-coin"></i> 当前价格
        </div>
        <div class="stat-value">${{ formatNumber(statistics.current_price) }}</div>
        <div class="stat-change" :class="changeClass">
          <i :class="changeIcon"></i>
          {{ formatNumber(statistics.price_change_24h) }}% (24h)
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="stat-card card-2">
        <div class="stat-label">
          <i class="bi bi-graph-up"></i> 24h最高
        </div>
        <div class="stat-value">${{ formatNumber(statistics.high_24h) }}</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="stat-card card-3">
        <div class="stat-label">
          <i class="bi bi-graph-down"></i> 24h最低
        </div>
        <div class="stat-value">${{ formatNumber(statistics.low_24h) }}</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="stat-card card-4">
        <div class="stat-label">
          <i class="bi bi-bar-chart"></i> 24h交易量
        </div>
        <div class="stat-value">${{ formatVolume(statistics.avg_volume) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatCards',
  props: {
    statistics: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    changeClass() {
      return this.statistics.price_change_24h > 0 ? 'trend-up' : 'trend-down'
    },
    changeIcon() {
      return this.statistics.price_change_24h > 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'
    }
  },
  methods: {
    formatNumber(num) {
      if (!num) return '0'
      return num.toLocaleString('en-US', { maximumFractionDigits: 2 })
    },
    formatVolume(num) {
      if (!num) return '0'
      if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
      if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
      return num.toLocaleString('en-US', { maximumFractionDigits: 0 })
    }
  }
}
</script>

<style scoped>
.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.stat-card.card-2 {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-card.card-3 {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.stat-card.card-4 {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #333;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 10px 0;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.trend-up {
  color: #90EE90;
}

.trend-down {
  color: #FFB6C6;
}
</style>