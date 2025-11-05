<template>
  <div id="app">
    <div class="background-gradient"></div>
    
    <div class="container-fluid">
      <!-- 页面标题 -->
      <PageHeader 
        :lastUpdate="lastUpdate" 
        @refresh="refreshData"
        :loading="loading"
      />

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

    <!-- 浮动刷新按钮 -->
    <button 
      class="btn btn-primary refresh-btn" 
      @click="refreshData" 
      :disabled="loading"
    >
      <i 
        class="bi bi-arrow-clockwise" 
        :class="{ 'spin': loading }"
      ></i>
    </button>
  </div>
</template>

<script>
import axios from 'axios'
import PageHeader from './components/PageHeader.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'
import StatCards from './components/StatCards.vue'
import PredictionCard from './components/PredictionCard.vue'
import ChartCard from './components/ChartCard.vue'
import PriceChart from './components/charts/PriceChart.vue'
import CandlestickChart from './components/charts/CandlestickChart.vue'
import RSIChart from './components/charts/RSIChart.vue'
import VolumeChart from './components/charts/VolumeChart.vue'
import RiskAlerts from './components/RiskAlerts.vue'

export default {
  name: 'App',
  components: {
    PageHeader,
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
  data() {
    return {
      loading: true,
      lastUpdate: '',
      statistics: {
        current_price: 0,
        high_24h: 0,
        low_24h: 0,
        avg_volume: 0,
        price_change_24h: 0
      },
      prediction: {
        current_price: 0,
        predicted_price: 0,
        change_percent: 0,
        direction: 'neutral'
      },
      historicalData: {
        timestamps: [],
        prices: [],
        volumes: [],
        ma_5: [],
        ma_10: [],
        ma_20: [],
        rsi: [],
        macd: [],
        macd_signal: []
      },
      candlestickData: {
        dates: [],
        data: [],
        volumes: []
      },
      riskAlerts: [],
      apiBaseUrl: 'http://localhost:5001/api',
      refreshInterval: null
    }
  },
  mounted() {
    this.loadAllData()
    
    // 改为每2分钟自动刷新一次（避免API限流）
    this.refreshInterval = setInterval(() => {
      console.log('🔄 Auto refresh...')
      this.loadAllData()
    }, 120000) // 120秒 = 2分钟
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    async loadAllData() {
      // 不要在刷新时设置loading=true，避免闪烁
      const isFirstLoad = !this.statistics.current_price
      if (isFirstLoad) {
        this.loading = true
      }
      
      try {
        await Promise.all([
          this.loadStatistics(),
          this.loadPrediction(),
          this.loadHistoricalData(),
          this.loadCandlestickData(),
          this.loadRiskAlerts()
        ])
        this.lastUpdate = new Date().toLocaleString('zh-CN')
        console.log('✅ All data loaded successfully')
      } catch (error) {
        console.error('加载数据失败:', error)
        // 只在首次加载失败时显示错误
        if (isFirstLoad) {
          alert('数据加载失败，请检查后端服务是否运行在 http://localhost:5001')
        }
      } finally {
        this.loading = false
      }
    },

    async loadStatistics() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/statistics`)
        if (response.data.success) {
          // 使用Object.assign保持响应式
          Object.assign(this.statistics, response.data.data)
          console.log('✅ Statistics loaded:', this.statistics)
        }
      } catch (error) {
        console.error('Statistics error:', error)
        // 不要重置为空对象，保持现有数据
      }
    },

    async loadPrediction() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/prediction`)
        if (response.data.success) {
          // 使用Object.assign保持响应式
          Object.assign(this.prediction, response.data.data)
          console.log('✅ Prediction loaded:', this.prediction)
        }
      } catch (error) {
        console.error('Prediction error:', error)
        // 保持现有预测数据
      }
    },

    async loadHistoricalData() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/historical?days=7`)
        if (response.data.success && response.data.data) {
          // 检查数据是否有效
          if (response.data.data.timestamps && response.data.data.timestamps.length > 0) {
            // 使用Object.assign保持响应式
            Object.assign(this.historicalData, response.data.data)
            console.log('✅ Historical data loaded:', this.historicalData.prices?.length, 'points')
            // 不需要手动更新图表，图表组件会通过watch自动更新
          } else {
            console.warn('⚠️ Historical data is empty')
          }
        } else {
          console.warn('⚠️ Historical data request failed:', response.data.message)
        }
      } catch (error) {
        console.error('Historical data error:', error)
      }
    },

    async loadCandlestickData() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/candlestick?days=30`)
        if (response.data.success) {
          // 使用Object.assign保持响应式
          Object.assign(this.candlestickData, response.data.data)
          console.log('✅ Candlestick data loaded:', this.candlestickData.dates?.length, 'days')
          // 图表组件会通过watch自动更新
        }
      } catch (error) {
        console.error('Candlestick data error:', error)
      }
    },

    async loadRiskAlerts() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/risk-alerts`)
        if (response.data.success) {
          this.riskAlerts = response.data.data
        }
      } catch (error) {
        console.error('Risk alerts error:', error)
        this.riskAlerts = []
      }
    },

    refreshData() {
      this.loadAllData()
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  min-height: 100vh;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
  padding: 20px 0;
  position: relative;
}

.background-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: -1;
}

.refresh-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 24px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.2);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  transition: transform 0.3s;
}

.refresh-btn:hover {
  transform: scale(1.1);
}

.refresh-btn:disabled {
  opacity: 0.6;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式 */
@media (max-width: 768px) {
  #app {
    padding: 10px 0;
  }
  
  .refresh-btn {
    width: 50px;
    height: 50px;
    font-size: 20px;
    bottom: 20px;
    right: 20px;
  }
}
</style>