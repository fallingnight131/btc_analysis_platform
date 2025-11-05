<template>
  <div class="container-fluid">
    <!-- 页面标题 -->
    <div class="page-header mb-4">
      <h2 class="mb-0">
        <i class="bi bi-speedometer2"></i>
        实时仪表板
      </h2>
      <p class="text-muted mb-0">实时监控比特币市场动态</p>
    </div>

    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading && !statistics.current_price" />

    <!-- 主要内容 -->
    <div v-else>
      <!-- 统计卡片 -->
      <StatCards :statistics="statistics" />

      <!-- 价格预测 -->
      <PredictionCard :prediction="prediction" />

      <!-- 图表区域 -->
      <div class="row">
        <!-- 价格走势图 -->
        <div class="col-md-8 mb-4">
          <ChartCard title="价格走势与技术指标" icon="graph-up-arrow">
            <PriceChart :data="historicalData" />
          </ChartCard>
        </div>

        <!-- 风险警报 -->
        <div class="col-md-4 mb-4">
          <ChartCard title="风险警报" icon="exclamation-triangle">
            <RiskAlerts :alerts="riskAlerts" />
          </ChartCard>
        </div>
      </div>

      <div class="row">
        <!-- K线图 -->
        <div class="col-md-6 mb-4">
          <ChartCard title="K线图" icon="bar-chart-line">
            <CandlestickChart :data="candlestickData" />
          </ChartCard>
        </div>

        <!-- RSI指标 -->
        <div class="col-md-6 mb-4">
          <ChartCard title="RSI相对强弱指标" icon="speedometer2">
            <RSIChart :data="historicalData" />
          </ChartCard>
        </div>
      </div>

      <div class="row">
        <!-- 交易量 -->
        <div class="col-md-12 mb-4">
          <ChartCard title="交易量分析" icon="bar-chart-fill">
            <VolumeChart :data="historicalData" />
          </ChartCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue'
import StatCards from '../components/StatCards.vue'
import PredictionCard from '../components/PredictionCard.vue'
import ChartCard from '../components/ChartCard.vue'
import PriceChart from '../components/charts/PriceChart.vue'
import CandlestickChart from '../components/charts/CandlestickChart.vue'
import RSIChart from '../components/charts/RSIChart.vue'
import VolumeChart from '../components/charts/VolumeChart.vue'
import RiskAlerts from '../components/RiskAlerts.vue'

export default {
  name: 'Dashboard',
  components: {
    LoadingSpinner,
    StatCards,
    PredictionCard,
    ChartCard,
    PriceChart,
    CandlestickChart,
    RSIChart,
    VolumeChart,
    RiskAlerts
  },
  props: {
    loading: Boolean,
    statistics: Object,
    prediction: Object,
    historicalData: Object,
    candlestickData: Object,
    riskAlerts: Array
  }
}
</script>

<style scoped>
.page-header {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.page-header h2 {
  color: #667eea;
  font-weight: 700;
}
</style>