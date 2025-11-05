<template>
  <div class="row mb-4">
    <div class="col-md-12">
      <div class="prediction-card">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h4><i class="bi bi-robot"></i> AI 价格预测</h4>
            <p class="mb-2">预测未来价格走势</p>
            <h2 class="mb-0">${{ formatNumber(prediction.predicted_price) }}</h2>
            <p class="mb-0">
              预期变化: 
              <span :class="changeClass">
                {{ formatNumber(prediction.change_percent) }}%
                <i :class="changeIcon"></i>
              </span>
            </p>
          </div>
          <div class="col-md-6 text-end">
            <i :class="directionIcon" style="font-size: 100px; opacity: 0.3;"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PredictionCard',
  props: {
    prediction: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    changeClass() {
      return this.prediction.change_percent > 0 ? 'trend-up' : 'trend-down'
    },
    changeIcon() {
      return this.prediction.change_percent > 0 
        ? 'bi bi-arrow-up-circle-fill' 
        : 'bi bi-arrow-down-circle-fill'
    },
    directionIcon() {
      return this.prediction.direction === 'up' 
        ? 'bi bi-arrow-up-circle' 
        : 'bi bi-arrow-down-circle'
    }
  },
  methods: {
    formatNumber(num) {
      if (!num) return '0'
      return num.toLocaleString('en-US', { maximumFractionDigits: 2 })
    }
  }
}
</script>

<style scoped>
.prediction-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 15px;
  padding: 25px;
}

.trend-up {
  color: #90EE90;
}

.trend-down {
  color: #FFB6C6;
}
</style>