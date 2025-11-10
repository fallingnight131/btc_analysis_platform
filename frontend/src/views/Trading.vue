<template>
  <div class="container-fluid">
    <div class="page-header mb-4">
      <h2>
        <i class="bi bi-currency-exchange"></i>
        交易策略
      </h2>
      <p class="text-muted mb-0">量化交易策略与回测分析</p>
    </div>

    <!-- 策略选择器 -->
    <div class="row mb-4">
      <div class="col-md-12">
        <div class="strategy-selector">
          <h4 class="mb-3">选择交易策略</h4>
          <div class="row">
            <div 
              v-for="strategy in strategies" 
              :key="strategy.id"
              class="col-md-3 mb-3"
            >
              <div 
                class="strategy-card"
                :class="{ 'active': selectedStrategy === strategy.id }"
                @click="selectStrategy(strategy.id)"
              >
                <i :class="strategy.icon"></i>
                <h5>{{ strategy.name }}</h5>
                <p class="small">{{ strategy.description }}</p>
                <div class="strategy-stats">
                  <span class="badge" :class="strategy.riskLevel === 'low' ? 'bg-success' : strategy.riskLevel === 'medium' ? 'bg-warning' : 'bg-danger'">
                    {{ getRiskLabel(strategy.riskLevel) }}
                  </span>
                  <span class="ms-2 text-muted small">
                    预期收益: {{ strategy.expectedReturn }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 策略详情 -->
    <div class="row" v-if="selectedStrategy">
      <!-- 策略参数设置 -->
      <div class="col-md-4 mb-4">
        <div class="parameter-card">
          <h4><i class="bi bi-sliders"></i> 策略参数</h4>
          <div class="parameter-form">
            <div class="form-group mb-3" v-for="param in currentStrategyParams" :key="param.name">
              <label class="form-label">{{ param.label }}</label>
              <input 
                type="number" 
                class="form-control"
                v-model.number="param.value"
                :min="param.min"
                :max="param.max"
                :step="param.step"
              >
              <small class="text-muted">{{ param.description }}</small>
            </div>
            
            <div class="form-group mb-3">
              <label class="form-label">初始资金</label>
              <div class="input-group">
                <span class="input-group-text">$</span>
                <input 
                  type="number" 
                  class="form-control"
                  v-model.number="initialCapital"
                  min="1000"
                  step="1000"
                >
              </div>
            </div>

            <button 
              class="btn btn-primary w-100"
              @click="runBacktest"
              :disabled="backtesting"
            >
              <i class="bi bi-play-circle" v-if="!backtesting"></i>
              <span class="spinner-border spinner-border-sm" v-else></span>
              {{ backtesting ? '回测中...' : '开始回测' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 回测结果 -->
      <div class="col-md-8 mb-4">
        <div class="backtest-result">
          <h4><i class="bi bi-graph-up"></i> 回测结果</h4>
          
          <div v-if="!backtestResult" class="empty-state">
            <i class="bi bi-bar-chart-line"></i>
            <p>设置参数后点击"开始回测"查看结果</p>
          </div>

          <div v-else>
            <!-- 性能指标 -->
            <div class="row mb-4">
              <div class="col-md-3">
                <div class="metric-box">
                  <div class="metric-label">总收益率</div>
                  <div class="metric-value" :class="backtestResult.totalReturn > 0 ? 'text-success' : 'text-danger'">
                    {{ backtestResult.totalReturn > 0 ? '+' : '' }}{{ backtestResult.totalReturn.toFixed(2) }}%
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="metric-box">
                  <div class="metric-label">年化收益</div>
                  <div class="metric-value text-primary">
                    {{ backtestResult.annualReturn.toFixed(2) }}%
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="metric-box">
                  <div class="metric-label">最大回撤</div>
                  <div class="metric-value text-danger">
                    {{ backtestResult.maxDrawdown.toFixed(2) }}%
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="metric-box">
                  <div class="metric-label">夏普比率</div>
                  <div class="metric-value text-info">
                    {{ backtestResult.sharpeRatio.toFixed(2) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 收益曲线 -->
            <div class="chart-section">
              <h5>资产曲线</h5>
              <div ref="equityChart" style="height: 300px;"></div>
            </div>

            <!-- 交易统计 -->
            <div class="trade-stats mt-4">
              <h5>交易统计</h5>
              <div class="row">
                <div class="col-md-6">
                  <ul class="list-unstyled">
                    <li><strong>总交易次数:</strong> {{ backtestResult.totalTrades }}</li>
                    <li><strong>盈利交易:</strong> {{ backtestResult.winningTrades }} ({{ backtestResult.winRate.toFixed(2) }}%)</li>
                    <li><strong>亏损交易:</strong> {{ backtestResult.losingTrades }}</li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <ul class="list-unstyled">
                    <li><strong>平均盈利:</strong> {{ backtestResult.avgWin.toFixed(2) }}%</li>
                    <li><strong>平均亏损:</strong> {{ backtestResult.avgLoss.toFixed(2) }}%</li>
                    <li><strong>盈亏比:</strong> {{ backtestResult.profitFactor.toFixed(2) }}</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- 交易记录 -->
            <div class="trade-history mt-4">
              <h5>最近交易记录</h5>
              <div class="table-responsive">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>时间</th>
                      <th>类型</th>
                      <th>价格</th>
                      <th>数量</th>
                      <th>盈亏</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(trade, index) in backtestResult.recentTrades" :key="index">
                      <td>{{ trade.time }}</td>
                      <td>
                        <span class="badge" :class="trade.type === 'BUY' ? 'bg-success' : 'bg-danger'">
                          {{ trade.type }}
                        </span>
                      </td>
                      <td>${{ trade.price.toLocaleString() }}</td>
                      <td>{{ trade.quantity.toFixed(4) }} BTC</td>
                      <td :class="trade.profit > 0 ? 'text-success' : 'text-danger'">
                        {{ trade.profit > 0 ? '+' : '' }}{{ trade.profit.toFixed(2) }}%
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 策略对比 -->
    <div class="row">
      <div class="col-md-12">
        <div class="comparison-card">
          <h4><i class="bi bi-bar-chart-steps"></i> 策略对比</h4>
          <div class="comparison-table">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>策略名称</th>
                    <th>风险等级</th>
                    <th>预期收益</th>
                    <th>最大回撤</th>
                    <th>胜率</th>
                    <th>适合场景</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="strategy in strategies" :key="strategy.id">
                    <td><strong>{{ strategy.name }}</strong></td>
                    <td>
                      <span class="badge" :class="strategy.riskLevel === 'low' ? 'bg-success' : strategy.riskLevel === 'medium' ? 'bg-warning' : 'bg-danger'">
                        {{ getRiskLabel(strategy.riskLevel) }}
                      </span>
                    </td>
                    <td class="text-success">{{ strategy.expectedReturn }}%</td>
                    <td class="text-danger">{{ strategy.maxDrawdown }}%</td>
                    <td>{{ strategy.winRate }}%</td>
                    <td class="text-muted small">{{ strategy.scenario }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'TradingView',
  props: {
    historicalData: Object,
    statistics: Object
  },
  data() {
    return {
      selectedStrategy: 'ma_cross',
      initialCapital: 10000,
      backtesting: false,
      backtestResult: null,
      equityChart: null,
      strategies: [
        {
          id: 'ma_cross',
          name: 'MA交叉策略',
          icon: 'bi bi-arrow-left-right',
          description: '基于移动平均线交叉的趋势跟踪策略',
          riskLevel: 'medium',
          expectedReturn: 15,
          maxDrawdown: -12,
          winRate: 55,
          scenario: '趋势明显的市场'
        },
        {
          id: 'rsi',
          name: 'RSI反转策略',
          icon: 'bi bi-arrow-repeat',
          description: '利用RSI超买超卖区域进行反转交易',
          riskLevel: 'high',
          expectedReturn: 25,
          maxDrawdown: -18,
          winRate: 48,
          scenario: '震荡市场'
        },
        {
          id: 'breakout',
          name: '突破策略',
          icon: 'bi bi-lightning',
          description: '捕捉价格突破关键位置的机会',
          riskLevel: 'high',
          expectedReturn: 30,
          maxDrawdown: -22,
          winRate: 45,
          scenario: '波动较大的市场'
        },
        {
          id: 'grid',
          name: '网格策略',
          icon: 'bi bi-grid-3x3',
          description: '在价格区间内高抛低吸',
          riskLevel: 'low',
          expectedReturn: 10,
          maxDrawdown: -8,
          winRate: 65,
          scenario: '横盘震荡市场'
        }
      ],
      strategyParams: {
        ma_cross: [
          { name: 'short_ma', label: '短期均线', value: 5, min: 3, max: 20, step: 1, description: '快速移动平均线周期' },
          { name: 'long_ma', label: '长期均线', value: 20, min: 10, max: 50, step: 1, description: '慢速移动平均线周期' }
        ],
        rsi: [
          { name: 'period', label: 'RSI周期', value: 14, min: 7, max: 28, step: 1, description: 'RSI计算周期' },
          { name: 'oversold', label: '超卖阈值', value: 30, min: 20, max: 40, step: 5, description: '低于此值视为超卖' },
          { name: 'overbought', label: '超买阈值', value: 70, min: 60, max: 80, step: 5, description: '高于此值视为超买' }
        ],
        breakout: [
          { name: 'lookback', label: '回溯周期', value: 20, min: 10, max: 50, step: 5, description: '计算最高最低价的周期' },
          { name: 'threshold', label: '突破幅度%', value: 2, min: 1, max: 5, step: 0.5, description: '突破有效性阈值' }
        ],
        grid: [
          { name: 'grids', label: '网格数量', value: 10, min: 5, max: 20, step: 1, description: '价格区间划分的网格数' },
          { name: 'range', label: '价格区间%', value: 10, min: 5, max: 20, step: 1, description: '上下边界的百分比' }
        ]
      }
    }
  },
  computed: {
    currentStrategyParams() {
      return this.strategyParams[this.selectedStrategy] || []
    }
  },
  methods: {
    selectStrategy(id) {
      this.selectedStrategy = id
      this.backtestResult = null
    },
    getRiskLabel(level) {
      const labels = { low: '低风险', medium: '中风险', high: '高风险' }
      return labels[level] || level
    },
    async runBacktest() {
      this.backtesting = true
      
      try {
        console.log('🚀 开始真实回测...')
        
        // 准备回测参数
        const params = {}
        this.currentStrategyParams.forEach(param => {
          params[param.name] = param.value
        })
        
        console.log('📊 回测参数:', {
          strategy: this.selectedStrategy,
          params,
          initialCapital: this.initialCapital
        })
        
        // 调用后端真实回测API
        const response = await this.$axios.post('/api/backtest', {
          strategy: this.selectedStrategy,
          params: params,
          initial_capital: this.initialCapital,
          days: 90  // 使用90天的历史数据进行回测
        })
        
        if (response.data.success) {
          this.backtestResult = response.data.data
          
          console.log('✅ 回测完成:', {
            totalReturn: this.backtestResult.totalReturn.toFixed(2) + '%',
            trades: this.backtestResult.totalTrades,
            winRate: this.backtestResult.winRate.toFixed(2) + '%',
            sharpeRatio: this.backtestResult.sharpeRatio.toFixed(2)
          })
          
          this.$nextTick(() => {
            this.renderEquityChart()
          })
        } else {
          console.error('❌ 回测失败:', response.data.message)
          alert('回测失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('❌ 回测错误:', error)
        alert('回测出错,请稍后重试')
      } finally {
        this.backtesting = false
      }
    },
    renderEquityChart() {
      if (!this.$refs.equityChart) return
      
      // 销毁旧图表实例,重新创建
      if (this.equityChart) {
        this.equityChart.dispose()
        this.equityChart = null
      }
      
      // 创建新的图表实例
      this.equityChart = echarts.init(this.$refs.equityChart)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.backtestResult.equityCurve.map((_, i) => `Day ${i + 1}`)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '${value}'
          }
        },
        series: [{
          name: '资产',
          type: 'line',
          data: this.backtestResult.equityCurve,
          smooth: true,
          lineStyle: {
            color: '#667eea',
            width: 3
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(102, 126, 234, 0.5)' },
              { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
            ])
          },
          markLine: {
            data: [
              { yAxis: this.initialCapital, label: { formatter: '初始资金' } }
            ],
            lineStyle: { color: '#999', type: 'dashed' }
          }
        }]
      }
      
      this.equityChart.setOption(option)
    }
  },
  beforeUnmount() {
    if (this.equityChart) {
      this.equityChart.dispose()
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

.strategy-selector,
.parameter-card,
.backtest-result,
.comparison-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.strategy-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
  text-align: center;
}

.strategy-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.strategy-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.strategy-card i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #667eea;
}

.strategy-card.active i {
  color: white;
}

.strategy-stats {
  margin-top: 1rem;
}

.parameter-form {
  margin-top: 1.5rem;
}

.metric-box {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.metric-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.8rem;
  font-weight: bold;
}

.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 5rem;
  opacity: 0.3;
  margin-bottom: 1rem;
}

.chart-section {
  margin-top: 2rem;
}

.trade-stats ul li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.trade-history table {
  font-size: 0.9rem;
}

.comparison-table {
  margin-top: 1.5rem;
}
</style>