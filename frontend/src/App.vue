<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-gradient sticky-top">
      <div class="container-fluid">
        <!-- Logo -->
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <i class="bi bi-currency-bitcoin logo-icon"></i>
          <span class="ms-2 fw-bold">全球比特币交易分析平台</span>
        </router-link>

        <!-- 移动端汉堡菜单 -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 导航菜单 -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active">
                <i class="bi bi-speedometer2"></i>
                <span class="ms-1">仪表板</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/analysis" class="nav-link" active-class="active">
                <i class="bi bi-graph-up"></i>
                <span class="ms-1">深度分析</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/trading" class="nav-link" active-class="active">
                <i class="bi bi-currency-exchange"></i>
                <span class="ms-1">交易策略</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/history" class="nav-link" active-class="active">
                <i class="bi bi-clock-history"></i>
                <span class="ms-1">历史数据</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/settings" class="nav-link" active-class="active">
                <i class="bi bi-gear"></i>
                <span class="ms-1">设置</span>
              </router-link>
            </li>
          </ul>

          <!-- 右侧功能按钮 -->
          <div class="d-flex align-items-center">
            <!-- 实时价格显示 -->
            <div class="price-badge me-3" v-if="realtimePrice">
              <span class="text-muted small">BTC</span>
              <span class="fw-bold ms-1">${{ formatPrice(realtimePrice) }}</span>
              <span 
                class="ms-1 small" 
                :class="priceChange >= 0 ? 'text-success' : 'text-danger'"
              >
                <i :class="priceChange >= 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                {{ Math.abs(priceChange).toFixed(2) }}%
              </span>
            </div>

            <!-- 刷新按钮 -->
            <button 
              class="btn btn-outline-light btn-sm me-2" 
              @click="refreshData"
              :disabled="loading"
            >
              <i 
                class="bi bi-arrow-clockwise" 
                :class="{ 'spin': loading }"
              ></i>
              <span class="ms-1 d-none d-md-inline">刷新</span>
            </button>

            <!-- 通知按钮 -->
            <button 
              class="btn btn-outline-light btn-sm position-relative"
              @click="showNotifications"
            >
              <i class="bi bi-bell"></i>
              <span 
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                v-if="alertCount > 0"
              >
                {{ alertCount }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="main-content">
      <router-view 
        :loading="loading"
        :statistics="statistics"
        :prediction="prediction"
        :historicalData="historicalData"
        :candlestickData="candlestickData"
        :riskAlerts="riskAlerts"
        @refresh="refreshData"
      />
    </div>

    <!-- 页脚 -->
    <footer class="footer mt-5 py-4 bg-dark text-white">
      <div class="container text-center">
        <p class="mb-1">
          <i class="bi bi-currency-bitcoin text-warning"></i>
          Bitcoin Analysis Platform
        </p>
        <p class="small text-muted mb-0">
          实时数据来源于 CoinGecko API | 最后更新: {{ lastUpdate }}
        </p>
      </div>
    </footer>

    <!-- 通知面板（右侧滑出） -->
    <div 
      class="notification-panel" 
      :class="{ 'show': showNotificationPanel }"
    >
      <div class="notification-header">
        <h5 class="mb-0">
          <i class="bi bi-bell"></i> 风险警报
        </h5>
        <button class="btn-close" @click="showNotificationPanel = false"></button>
      </div>
      <div class="notification-body">
        <div v-if="riskAlerts.length === 0" class="text-center text-muted py-5">
          <i class="bi bi-check-circle" style="font-size: 48px;"></i>
          <p class="mt-3">暂无警报</p>
        </div>
        <div 
          v-for="(alert, index) in riskAlerts" 
          :key="index"
          class="alert-item"
          :class="'alert-' + alert.severity"
        >
          <div class="d-flex justify-content-between">
            <strong>{{ alert.message }}</strong>
            <span 
              class="badge"
              :class="alert.severity === 'high' ? 'bg-danger' : 'bg-warning'"
            >
              {{ alert.severity }}
            </span>
          </div>
          <small class="text-muted">{{ alert.timestamp }}</small>
        </div>
      </div>
    </div>

    <!-- 遮罩层 -->
    <div 
      class="overlay" 
      :class="{ 'show': showNotificationPanel }"
      @click="showNotificationPanel = false"
    ></div>

    <!-- 更新提示 Toast -->
    <div class="update-toast" :class="{ 'show': showUpdateToast }">
      <i class="bi bi-arrow-clockwise spin"></i>
      <span class="ms-2">数据更新中...</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      loading: false,
      lastUpdate: '',
      realtimePrice: 0,
      priceChange: 0,
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
      refreshInterval: null,
      showNotificationPanel: false,
      showUpdateToast: false
    }
  },
  computed: {
    alertCount() {
      return this.riskAlerts.filter(a => a.severity === 'high').length
    }
  },
  mounted() {
    this.loadAllData()
    
    // 每30秒自动刷新（更频繁的实时更新）
    this.refreshInterval = setInterval(() => {
      this.loadAllData()
    }, 30000)
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    async loadAllData() {
      const isFirstLoad = !this.statistics.current_price
      if (isFirstLoad) {
        this.loading = true
      } else {
        // 非首次加载时显示更新提示
        this.showUpdateToast = true
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
        
        // 隐藏更新提示
        if (!isFirstLoad) {
          setTimeout(() => {
            this.showUpdateToast = false
          }, 1000)
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        this.showUpdateToast = false
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
          Object.assign(this.statistics, response.data.data)
          this.realtimePrice = this.statistics.current_price
          this.priceChange = this.statistics.price_change_24h
        }
      } catch (error) {
        console.error('Statistics error:', error)
      }
    },

    async loadPrediction() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/prediction`)
        if (response.data.success) {
          Object.assign(this.prediction, response.data.data)
        }
      } catch (error) {
        console.error('Prediction error:', error)
      }
    },

    async loadHistoricalData() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/historical?days=7`)
        if (response.data.success && response.data.data) {
          if (response.data.data.timestamps && response.data.data.timestamps.length > 0) {
            Object.assign(this.historicalData, response.data.data)
          }
        }
      } catch (error) {
        console.error('Historical data error:', error)
      }
    },

    async loadCandlestickData() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/candlestick?days=30`)
        if (response.data.success) {
          Object.assign(this.candlestickData, response.data.data)
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
    },

    showNotifications() {
      this.showNotificationPanel = !this.showNotificationPanel
    },

    formatPrice(price) {
      return price ? price.toLocaleString('en-US', { maximumFractionDigits: 2 }) : '0'
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%) !important;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 0.8rem 0;
  position: relative;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.navbar.bg-gradient {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%) !important;
}

.logo-icon {
  font-size: 2rem;
  color: #ffd700;
}

.navbar-brand {
  font-size: 1.5rem;
  transition: transform 0.3s;
  color: #ffd700 !important; /* 金色 */
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.nav-link {
  color: rgba(34, 216, 191, 0.9) !important;
  padding: 0.5rem 1rem !important;
  margin: 0 0.2rem;
  border-radius: 8px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.nav-link:hover {
  background: rgba(255,255,255,0.1);
  color: rgb(255, 255, 255) !important;
}

.nav-link.active {
  background: rgba(255,255,255,0.2);
  color: rgba(238, 158, 93, 0.9) !important;
  font-weight: 600;
}

.price-badge {
  background: rgba(102, 126, 234, 0.6);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 2rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 页脚 */
.footer {
  background: #1a1a2e !important;
  margin-top: auto;
}

/* 通知面板 */
.notification-panel {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: white;
  box-shadow: -5px 0 20px rgba(0,0,0,0.1);
  transition: right 0.3s;
  z-index: 1050;
  display: flex;
  flex-direction: column;
}

.notification-panel.show {
  right: 0;
}

.notification-header {
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.notification-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.alert-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.alert-high {
  background: #ffe6e6;
  border-color: #dc3545;
}

.alert-medium {
  background: #fff8e6;
  border-color: #ffc107;
}

/* 遮罩层 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1040;
}

.overlay.show {
  opacity: 1;
  visibility: visible;
}

/* 动画 */
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 更新提示 Toast */
.update-toast {
  position: fixed;
  top: 80px;
  right: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  display: flex;
  align-items: center;
  z-index: 1030;
  transform: translateX(400px);
  opacity: 0;
  transition: all 0.3s ease;
  font-weight: 500;
}

.update-toast.show {
  transform: translateX(0);
  opacity: 1;
}

.update-toast i {
  font-size: 1.2rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
  }

  .notification-panel {
    width: 100%;
    right: -100%;
  }

  .price-badge {
    font-size: 0.85rem;
  }
  
  .update-toast {
    top: auto;
    bottom: 20px;
    right: 50%;
    transform: translateX(50%) translateY(100px);
  }
  
  .update-toast.show {
    transform: translateX(50%) translateY(0);
  }
}
</style>