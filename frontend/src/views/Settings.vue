<template>
  <div class="container-fluid">
    <div class="page-header mb-4">
      <h2>
        <i class="bi bi-gear"></i>
        系统设置
      </h2>
      <p class="text-muted mb-0">配置系统参数和个人偏好</p>
    </div>

    <div class="row">
      <!-- 侧边导航 -->
      <div class="col-md-3 mb-4">
        <div class="settings-nav">
          <div 
            class="nav-item" 
            v-for="item in navItems" 
            :key="item.id"
            :class="{ active: activeTab === item.id }"
            @click="activeTab = item.id"
          >
            <i :class="item.icon"></i>
            <span>{{ item.label }}</span>
          </div>
        </div>
      </div>

      <!-- 设置内容 -->
      <div class="col-md-9">
        <!-- API设置 -->
        <div class="settings-panel" v-show="activeTab === 'api'">
          <h4><i class="bi bi-server"></i> API配置</h4>
          <div class="settings-content">
            <div class="form-group mb-3">
              <label class="form-label">后端API地址</label>
              <input type="text" class="form-control" v-model="settings.apiUrl" placeholder="http://localhost:5001/api">
              <small class="text-muted">配置后端服务器地址</small>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">CoinGecko API密钥</label>
              <div class="input-group">
                <input 
                  :type="showApiKey ? 'text' : 'password'" 
                  class="form-control" 
                  v-model="settings.coinGeckoKey"
                  placeholder="可选：免费版无需配置"
                >
                <button class="btn btn-outline-secondary" @click="showApiKey = !showApiKey">
                  <i :class="showApiKey ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <small class="text-muted">配置API密钥可提高请求限制</small>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.useProxy" id="useProxy">
              <label class="form-check-label" for="useProxy">
                使用代理服务器
              </label>
            </div>

            <div class="alert alert-info">
              <i class="bi bi-info-circle"></i>
              <strong>提示：</strong> API配置更改后需要刷新页面才能生效
            </div>
          </div>
        </div>

        <!-- 通知设置 -->
        <div class="settings-panel" v-show="activeTab === 'notifications'">
          <h4><i class="bi bi-bell"></i> 通知设置</h4>
          <div class="settings-content">
            <h5 class="mb-3">价格警报</h5>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.priceAlerts" id="priceAlerts">
              <label class="form-check-label" for="priceAlerts">
                启用价格警报
              </label>
            </div>

            <div class="row mb-3" v-if="settings.priceAlerts">
              <div class="col-md-6">
                <label class="form-label">价格上限警报</label>
                <div class="input-group">
                  <span class="input-group-text">$</span>
                  <input type="number" class="form-control" v-model.number="settings.priceUpperLimit" step="1000">
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label">价格下限警报</label>
                <div class="input-group">
                  <span class="input-group-text">$</span>
                  <input type="number" class="form-control" v-model.number="settings.priceLowerLimit" step="1000">
                </div>
              </div>
            </div>

            <hr class="my-4">

            <h5 class="mb-3">市场警报</h5>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.volatilityAlert" id="volatilityAlert">
              <label class="form-check-label" for="volatilityAlert">
                波动率过高警报（24h波动 &gt; 10%）
              </label>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.volumeAlert" id="volumeAlert">
              <label class="form-check-label" for="volumeAlert">
                交易量异常警报（超过平均值2倍）
              </label>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.trendAlert" id="trendAlert">
              <label class="form-check-label" for="trendAlert">
                趋势反转警报（MA交叉）
              </label>
            </div>

            <hr class="my-4">

            <h5 class="mb-3">通知方式</h5>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.browserNotification" id="browserNotification">
              <label class="form-check-label" for="browserNotification">
                浏览器桌面通知
              </label>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.soundNotification" id="soundNotification">
              <label class="form-check-label" for="soundNotification">
                声音提示
              </label>
            </div>
          </div>
        </div>

        <!-- 显示设置 -->
        <div class="settings-panel" v-show="activeTab === 'display'">
          <h4><i class="bi bi-palette"></i> 显示设置</h4>
          <div class="settings-content">
            <div class="form-group mb-4">
              <label class="form-label">主题</label>
              <div class="row">
                <div class="col-md-4">
                  <div 
                    class="theme-card" 
                    :class="{ active: settings.theme === 'light' }"
                    @click="settings.theme = 'light'"
                  >
                    <div class="theme-preview light"></div>
                    <p class="mt-2 mb-0">浅色主题</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div 
                    class="theme-card" 
                    :class="{ active: settings.theme === 'dark' }"
                    @click="settings.theme = 'dark'"
                  >
                    <div class="theme-preview dark"></div>
                    <p class="mt-2 mb-0">深色主题</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div 
                    class="theme-card" 
                    :class="{ active: settings.theme === 'auto' }"
                    @click="settings.theme = 'auto'"
                  >
                    <div class="theme-preview auto"></div>
                    <p class="mt-2 mb-0">自动切换</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">图表配色方案</label>
              <select class="form-select" v-model="settings.chartColorScheme">
                <option value="default">默认（紫色）</option>
                <option value="blue">蓝色</option>
                <option value="green">绿色</option>
                <option value="red">红色</option>
              </select>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.animatedCharts" id="animatedCharts">
              <label class="form-check-label" for="animatedCharts">
                启用图表动画效果
              </label>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.compactView" id="compactView">
              <label class="form-check-label" for="compactView">
                紧凑视图模式
              </label>
            </div>
          </div>
        </div>

        <!-- 数据设置 -->
        <div class="settings-panel" v-show="activeTab === 'data'">
          <h4><i class="bi bi-database"></i> 数据设置</h4>
          <div class="settings-content">
            <div class="form-group mb-3">
              <label class="form-label">数据刷新间隔</label>
              <select class="form-select" v-model="settings.refreshInterval">
                <option value="30">30秒</option>
                <option value="60">1分钟</option>
                <option value="120">2分钟</option>
                <option value="300">5分钟</option>
                <option value="600">10分钟</option>
              </select>
              <small class="text-muted">自动刷新数据的时间间隔</small>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">历史数据缓存时间</label>
              <select class="form-select" v-model="settings.cacheTime">
                <option value="300">5分钟</option>
                <option value="600">10分钟</option>
                <option value="1800">30分钟</option>
                <option value="3600">1小时</option>
              </select>
            </div>

            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" v-model="settings.autoRefresh" id="autoRefresh">
              <label class="form-check-label" for="autoRefresh">
                启用自动刷新
              </label>
            </div>

            <hr class="my-4">

            <h5 class="mb-3">数据管理</h5>
            <div class="d-grid gap-2">
              <button class="btn btn-outline-primary" @click="clearCache">
                <i class="bi bi-trash"></i> 清除缓存数据
              </button>
              <button class="btn btn-outline-danger" @click="resetSettings">
                <i class="bi bi-arrow-counterclockwise"></i> 重置所有设置
              </button>
            </div>
          </div>
        </div>

        <!-- 关于 -->
        <div class="settings-panel" v-show="activeTab === 'about'">
          <h4><i class="bi bi-info-circle"></i> 关于</h4>
          <div class="settings-content">
            <div class="about-section">
              <div class="text-center mb-4">
                <i class="bi bi-currency-bitcoin display-1 text-warning"></i>
                <h3 class="mt-3">Bitcoin Analysis Platform</h3>
                <p class="text-muted">版本 1.0.0</p>
              </div>

              <div class="info-list">
                <div class="info-item">
                  <strong>开发者:</strong>
                  <span>BTC Analysis Team</span>
                </div>
                <div class="info-item">
                  <strong>技术栈:</strong>
                  <span>Vue 3 + Flask + ECharts + Bootstrap</span>
                </div>
                <div class="info-item">
                  <strong>数据来源:</strong>
                  <span>CoinGecko API</span>
                </div>
                <div class="info-item">
                  <strong>更新时间:</strong>
                  <span>2025-11-05</span>
                </div>
              </div>

              <hr class="my-4">

              <div class="text-center">
                <h5>联系我们</h5>
                <div class="social-links mt-3">
                  <a href="#" class="btn btn-outline-primary me-2">
                    <i class="bi bi-github"></i> GitHub
                  </a>
                  <a href="#" class="btn btn-outline-info me-2">
                    <i class="bi bi-twitter"></i> Twitter
                  </a>
                  <a href="#" class="btn btn-outline-danger">
                    <i class="bi bi-envelope"></i> Email
                  </a>
                </div>
              </div>

              <div class="alert alert-info mt-4">
                <i class="bi bi-lightbulb"></i>
                <strong>提示：</strong> 本平台仅供学习和研究使用，不构成任何投资建议。投资有风险，入市需谨慎。
              </div>
            </div>
          </div>
        </div>

        <!-- 保存按钮 -->
        <div class="save-actions mt-4" v-if="activeTab !== 'about'">
          <button class="btn btn-primary btn-lg" @click="saveSettings">
            <i class="bi bi-check-circle"></i> 保存设置
          </button>
          <button class="btn btn-outline-secondary btn-lg ms-2" @click="cancelChanges">
            <i class="bi bi-x-circle"></i> 取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
      activeTab: 'api',
      showApiKey: false,
      navItems: [
        { id: 'api', label: 'API配置', icon: 'bi bi-server' },
        { id: 'notifications', label: '通知设置', icon: 'bi bi-bell' },
        { id: 'display', label: '显示设置', icon: 'bi bi-palette' },
        { id: 'data', label: '数据设置', icon: 'bi bi-database' },
        { id: 'about', label: '关于', icon: 'bi bi-info-circle' }
      ],
      settings: {
        apiUrl: 'http://localhost:5001/api',
        coinGeckoKey: '',
        useProxy: false,
        priceAlerts: true,
        priceUpperLimit: 80000,
        priceLowerLimit: 60000,
        volatilityAlert: true,
        volumeAlert: true,
        trendAlert: false,
        browserNotification: true,
        soundNotification: false,
        theme: 'light',
        chartColorScheme: 'default',
        animatedCharts: true,
        compactView: false,
        refreshInterval: 120,
        cacheTime: 600,
        autoRefresh: true
      },
      originalSettings: null
    }
  },
  mounted() {
    this.loadSettings()
    this.originalSettings = JSON.parse(JSON.stringify(this.settings))
  },
  methods: {
    loadSettings() {
      const saved = localStorage.getItem('btc_settings')
      if (saved) {
        this.settings = { ...this.settings, ...JSON.parse(saved) }
      }
    },
    saveSettings() {
      localStorage.setItem('btc_settings', JSON.stringify(this.settings))
      this.originalSettings = JSON.parse(JSON.stringify(this.settings))
      
      // 显示成功提示
      alert('设置已保存！部分设置需要刷新页面后生效。')
    },
    cancelChanges() {
      this.settings = JSON.parse(JSON.stringify(this.originalSettings))
    },
    clearCache() {
      if (confirm('确定要清除所有缓存数据吗？')) {
        localStorage.removeItem('btc_cache')
        alert('缓存已清除！')
      }
    },
    resetSettings() {
      if (confirm('确定要重置所有设置为默认值吗？此操作不可撤销。')) {
        localStorage.removeItem('btc_settings')
        location.reload()
      }
    }
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

.settings-nav {
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.nav-item {
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
  display: flex;
  align-items: center;
}

.nav-item i {
  margin-right: 0.75rem;
  font-size: 1.2rem;
}

.nav-item:hover {
  background: #f8f9fa;
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
  border-left-color: #667eea;
  color: #667eea;
  font-weight: 600;
}

.settings-panel {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.settings-content {
  margin-top: 1.5rem;
}

.theme-card {
  text-align: center;
  padding: 1rem;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.theme-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}

.theme-card.active {
  border-color: #667eea;
  background: #f8f9fa;
}

.theme-preview {
  height: 80px;
  border-radius: 8px;
  margin: 0 auto;
}

.theme-preview.light {
  background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
  border: 1px solid #dee2e6;
}

.theme-preview.dark {
  background: linear-gradient(135deg, #343a40 0%, #212529 100%);
}

.theme-preview.auto {
  background: linear-gradient(90deg, #fff 0%, #fff 50%, #343a40 50%, #343a40 100%);
}

.about-section {
  text-align: center;
}

.info-list {
  max-width: 500px;
  margin: 0 auto;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.save-actions {
  text-align: center;
}
</style>