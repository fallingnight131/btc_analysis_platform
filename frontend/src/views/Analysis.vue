<template>
  <div class="container-fluid">
    <div class="page-header mb-4">
      <h2 class="mb-0">
        <i class="bi bi-graph-up"></i>
        深度分析
      </h2>
      <p class="text-muted mb-0">多维度技术分析与市场洞察</p>
    </div>

    <div class="row">
      <!-- 技术指标对比 -->
      <div class="col-md-12 mb-4">
        <div class="analysis-card">
          <h4><i class="bi bi-bar-chart-line"></i> 技术指标总览</h4>
          <div class="row mt-4">
            <div class="col-md-3">
              <div class="indicator-box">
                <div class="indicator-label">RSI (14)</div>
                <div class="indicator-value" :class="getRSIClass(currentRSI)">
                  {{ currentRSI.toFixed(2) }}
                </div>
                <div class="indicator-status">{{ getRSIStatus(currentRSI) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="indicator-box">
                <div class="indicator-label">MACD</div>
                <div class="indicator-value" :class="getMACDClass(currentMACD)">
                  {{ currentMACD > 0 ? '+' : '' }}{{ currentMACD.toFixed(2) }}
                </div>
                <div class="indicator-status">{{ getMACDStatus(currentMACD) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="indicator-box">
                <div class="indicator-label">波动率 (24h)</div>
                <div class="indicator-value text-info">
                  ${{ currentVolatility.toFixed(2) }}
                </div>
                <div class="indicator-status">{{ getVolatilityStatus(currentVolatility) }}</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="indicator-box">
                <div class="indicator-label">趋势强度</div>
                <div class="indicator-value text-primary">
                  {{ trendStrength }}%
                </div>
                <div class="indicator-status">{{ getTrendStatus(trendStrength) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 市场情绪分析 -->
      <div class="col-md-6 mb-4">
        <div class="analysis-card">
          <h4><i class="bi bi-emoji-smile"></i> 市场情绪</h4>
          <div class="sentiment-gauge mt-4">
            <div class="gauge-container">
              <div class="gauge-bar">
                <div class="gauge-fill" :style="{ width: sentimentIndex + '%' }"></div>
              </div>
              <div class="gauge-labels">
                <span>极度恐慌</span>
                <span>恐慌</span>
                <span>中性</span>
                <span>贪婪</span>
                <span>极度贪婪</span>
              </div>
            </div>
            <div class="sentiment-value mt-3 text-center">
              <h2 :class="getSentimentColor(sentimentIndex)">
                {{ getSentimentLabel(sentimentIndex) }}
              </h2>
              <p class="text-muted">情绪指数: {{ sentimentIndex }}/100</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 支撑位与阻力位 -->
      <div class="col-md-6 mb-4">
        <div class="analysis-card">
          <h4><i class="bi bi-layers"></i> 支撑位与阻力位</h4>
          <div class="mt-4">
            <div class="level-item resistance">
              <span class="level-label">强阻力位</span>
              <span class="level-value">${{ resistance1.toLocaleString() }}</span>
            </div>
            <div class="level-item resistance-light">
              <span class="level-label">次阻力位</span>
              <span class="level-value">${{ resistance2.toLocaleString() }}</span>
            </div>
            <div class="level-item current">
              <span class="level-label">当前价格</span>
              <span class="level-value">${{ statistics.current_price.toLocaleString() }}</span>
            </div>
            <div class="level-item support-light">
              <span class="level-label">次支撑位</span>
              <span class="level-value">${{ support1.toLocaleString() }}</span>
            </div>
            <div class="level-item support">
              <span class="level-label">强支撑位</span>
              <span class="level-value">${{ support2.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- AI分析建议 -->
      <div class="col-md-12 mb-4">
        <div class="analysis-card ai-suggestion">
          <h4><i class="bi bi-robot"></i> AI智能分析</h4>
          <div class="suggestion-content mt-3">
            <div class="row">
              <div class="col-md-4">
                <div class="suggestion-box" :class="getRecommendationClass()">
                  <i :class="getRecommendationIcon()"></i>
                  <h5>{{ getRecommendation() }}</h5>
                  <p>综合评分: {{ aiScore }}/100</p>
                </div>
              </div>
              <div class="col-md-8">
                <div class="suggestion-details">
                  <h6>分析要点:</h6>
                  <ul>
                    <li v-for="(point, index) in analysisPoints" :key="index">
                      {{ point }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Analysis',
  props: {
    statistics: Object,
    historicalData: Object,
    prediction: Object
  },
  computed: {
    currentRSI() {
      const rsi = this.historicalData?.rsi || []
      return rsi.length > 0 ? rsi[rsi.length - 1] : 50
    },
    currentMACD() {
      const macd = this.historicalData?.macd || []
      return macd.length > 0 ? macd[macd.length - 1] : 0
    },
    currentVolatility() {
      return this.statistics?.volatility || 0
    },
    trendStrength() {
      const change = this.statistics?.price_change_24h || 0
      return Math.min(Math.abs(change) * 10, 100).toFixed(0)
    },
    sentimentIndex() {
      // 综合RSI、MACD、价格变化计算情绪指数
      let score = 50
      if (this.currentRSI > 70) score += 15
      if (this.currentRSI < 30) score -= 15
      if (this.currentMACD > 0) score += 10
      if (this.currentMACD < 0) score -= 10
      if (this.statistics?.price_change_24h > 0) score += 10
      if (this.statistics?.price_change_24h < 0) score -= 10
      return Math.max(0, Math.min(100, score))
    },
    resistance1() {
      return this.statistics.current_price * 1.05
    },
    resistance2() {
      return this.statistics.current_price * 1.02
    },
    support1() {
      return this.statistics.current_price * 0.98
    },
    support2() {
      return this.statistics.current_price * 0.95
    },
    aiScore() {
      return Math.floor((this.sentimentIndex + this.trendStrength) / 2)
    },
    analysisPoints() {
      const points = []
      if (this.currentRSI > 70) points.push('RSI超买，可能面临回调压力')
      if (this.currentRSI < 30) points.push('RSI超卖，可能存在反弹机会')
      if (this.currentMACD > 0) points.push('MACD金叉，短期趋势向好')
      if (this.currentMACD < 0) points.push('MACD死叉，短期趋势偏弱')
      if (this.statistics?.price_change_24h > 5) points.push('24小时涨幅较大，注意回调风险')
      if (this.statistics?.price_change_24h < -5) points.push('24小时跌幅较大，关注支撑位')
      return points.length > 0 ? points : ['当前市场波动正常，持续观察']
    }
  },
  methods: {
    getRSIClass(rsi) {
      if (rsi > 70) return 'text-danger'
      if (rsi < 30) return 'text-success'
      return 'text-warning'
    },
    getRSIStatus(rsi) {
      if (rsi > 70) return '超买'
      if (rsi < 30) return '超卖'
      return '正常'
    },
    getMACDClass(macd) {
      return macd > 0 ? 'text-success' : 'text-danger'
    },
    getMACDStatus(macd) {
      return macd > 0 ? '多头' : '空头'
    },
    getVolatilityStatus(vol) {
      if (vol > 2000) return '高波动'
      if (vol > 1000) return '中等波动'
      return '低波动'
    },
    getTrendStatus(strength) {
      if (strength > 70) return '强趋势'
      if (strength > 40) return '中等趋势'
      return '弱趋势'
    },
    getSentimentColor(index) {
      if (index > 75) return 'text-danger'
      if (index > 55) return 'text-warning'
      if (index > 45) return 'text-info'
      if (index > 25) return 'text-primary'
      return 'text-success'
    },
    getSentimentLabel(index) {
      if (index > 75) return '极度贪婪'
      if (index > 55) return '贪婪'
      if (index > 45) return '中性'
      if (index > 25) return '恐慌'
      return '极度恐慌'
    },
    getRecommendation() {
      if (this.aiScore > 70) return '强烈看多'
      if (this.aiScore > 55) return '看多'
      if (this.aiScore > 45) return '观望'
      if (this.aiScore > 30) return '看空'
      return '强烈看空'
    },
    getRecommendationClass() {
      if (this.aiScore > 70) return 'bg-success'
      if (this.aiScore > 55) return 'bg-info'
      if (this.aiScore > 45) return 'bg-warning'
      return 'bg-danger'
    },
    getRecommendationIcon() {
      if (this.aiScore > 55) return 'bi bi-arrow-up-circle-fill'
      if (this.aiScore > 45) return 'bi bi-dash-circle-fill'
      return 'bi bi-arrow-down-circle-fill'
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

.analysis-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  height: 100%;
}

.indicator-box {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.indicator-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.indicator-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.indicator-status {
  font-size: 0.85rem;
  color: #6c757d;
}

.gauge-bar {
  height: 40px;
  background: linear-gradient(to right, #dc3545, #ffc107, #28a745);
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.gauge-fill {
  height: 100%;
  background: rgba(255,255,255,0.3);
  transition: width 0.5s;
}

.gauge-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #6c757d;
}

.level-item {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resistance {
  background: #ffe6e6;
  border-left: 4px solid #dc3545;
}

.resistance-light {
  background: #fff0f0;
  border-left: 4px solid #f8bbd0;
}

.current {
  background: #e6f3ff;
  border-left: 4px solid #2196f3;
  font-weight: bold;
}

.support-light {
  background: #f0ffe6;
  border-left: 4px solid #c8e6c9;
}

.support {
  background: #e6ffe6;
  border-left: 4px solid #4caf50;
}

.ai-suggestion {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.suggestion-box {
  text-align: center;
  padding: 2rem;
  border-radius: 15px;
  color: white;
}

.suggestion-box i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.suggestion-details {
  background: rgba(255,255,255,0.1);
  padding: 1.5rem;
  border-radius: 10px;
}

.suggestion-details ul {
  margin: 0;
  padding-left: 1.5rem;
}

.suggestion-details li {
  margin-bottom: 0.5rem;
}
</style>