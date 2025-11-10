<template>
  <div class="container-fluid">
    <div class="page-header mb-4">
      <h2>
        <i class="bi bi-clock-history"></i>
        历史数据
      </h2>
      <p class="text-muted mb-0">查询、分析和导出历史数据</p>
    </div>

    <!-- 查询面板 -->
    <div class="row mb-4">
      <div class="col-md-12">
        <div class="query-panel">
          <h4><i class="bi bi-search"></i> 数据查询</h4>
          <div class="row mt-3">
            <div class="col-md-3">
              <label class="form-label">开始日期</label>
              <input type="date" class="form-control" v-model="startDate">
            </div>
            <div class="col-md-3">
              <label class="form-label">结束日期</label>
              <input type="date" class="form-control" v-model="endDate">
            </div>
            <div class="col-md-2">
              <label class="form-label">数据粒度</label>
              <select class="form-select" v-model="granularity">
                <option value="1m">1分钟</option>
                <option value="5m">5分钟</option>
                <option value="15m">15分钟</option>
                <option value="1h" selected>1小时</option>
                <option value="4h">4小时</option>
                <option value="1d">1天</option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label">数据类型</label>
              <select class="form-select" v-model="dataType">
                <option value="ohlcv">OHLCV</option>
                <option value="price">价格</option>
                <option value="volume">交易量</option>
                <option value="indicators">技术指标</option>
              </select>
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button class="btn btn-primary w-100" @click="queryData" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm"></span>
                <span v-else><i class="bi bi-search"></i> 查询</span>
              </button>
            </div>
          </div>

          <!-- 快捷选择 -->
          <div class="quick-select mt-3">
            <span class="text-muted me-2">快捷选择:</span>
            <button class="btn btn-sm btn-outline-primary me-2" @click="selectRange(7)">最近7天</button>
            <button class="btn btn-sm btn-outline-primary me-2" @click="selectRange(30)">最近30天</button>
            <button class="btn btn-sm btn-outline-primary me-2" @click="selectRange(90)">最近90天</button>
            <button class="btn btn-sm btn-outline-primary" @click="selectRange(365)">最近一年</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="row mb-4" v-if="queryResult">
      <div class="col-md-12">
        <div class="stats-panel">
          <h4><i class="bi bi-bar-chart"></i> 数据统计</h4>
          <div class="row mt-3">
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">数据点数</div>
                <div class="stat-value">{{ queryResult.dataPoints }}</div>
              </div>
            </div>
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">最高价</div>
                <div class="stat-value text-success">${{ formatNumber(queryResult.highPrice) }}</div>
              </div>
            </div>
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">最低价</div>
                <div class="stat-value text-danger">${{ formatNumber(queryResult.lowPrice) }}</div>
              </div>
            </div>
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">平均价</div>
                <div class="stat-value text-primary">${{ formatNumber(queryResult.avgPrice) }}</div>
              </div>
            </div>
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">总交易量</div>
                <div class="stat-value text-info">${{ formatVolume(queryResult.totalVolume) }}</div>
              </div>
            </div>
            <div class="col-md-2">
              <div class="stat-box">
                <div class="stat-label">价格变化</div>
                <div class="stat-value" :class="queryResult.priceChange > 0 ? 'text-success' : 'text-danger'">
                  {{ queryResult.priceChange > 0 ? '+' : '' }}{{ queryResult.priceChange.toFixed(2) }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据可视化 -->
    <div class="row mb-4" v-if="queryResult">
      <div class="col-md-8">
        <div class="chart-panel">
          <div class="chart-header">
            <h4><i class="bi bi-graph-up"></i> 价格走势</h4>
            <div class="chart-controls">
              <button class="btn btn-sm btn-outline-secondary me-2" @click="chartType = 'line'" :class="{ active: chartType === 'line' }">
                <i class="bi bi-graph-up"></i> 线图
              </button>
              <button class="btn btn-sm btn-outline-secondary" @click="chartType = 'candlestick'" :class="{ active: chartType === 'candlestick' }">
                <i class="bi bi-bar-chart-line"></i> K线图
              </button>
            </div>
          </div>
          <div ref="historyChart" style="height: 400px;"></div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="chart-panel">
          <h4><i class="bi bi-pie-chart"></i> 数据分布</h4>
          <div ref="distributionChart" style="height: 400px;"></div>
        </div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="row mb-4" v-if="queryResult">
      <div class="col-md-12">
        <div class="table-panel">
          <div class="table-header">
            <h4><i class="bi bi-table"></i> 数据列表</h4>
            <div class="table-actions">
              <button class="btn btn-sm btn-success me-2" @click="exportData('csv')">
                <i class="bi bi-file-earmark-excel"></i> 导出CSV
              </button>
              <button class="btn btn-sm btn-success me-2" @click="exportData('json')">
                <i class="bi bi-file-earmark-code"></i> 导出JSON
              </button>
              <button class="btn btn-sm btn-primary" @click="showFullScreen">
                <i class="bi bi-arrows-fullscreen"></i> 全屏查看
              </button>
            </div>
          </div>

          <div class="table-responsive" style="max-height: 500px;">
            <table class="table table-hover">
              <thead class="sticky-top bg-light">
                <tr>
                  <th>时间</th>
                  <th>开盘价</th>
                  <th>最高价</th>
                  <th>最低价</th>
                  <th>收盘价</th>
                  <th>交易量</th>
                  <th>涨跌幅</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in queryResult.data" :key="index">
                  <td>{{ row.time }}</td>
                  <td>${{ formatNumber(row.open) }}</td>
                  <td class="text-success">${{ formatNumber(row.high) }}</td>
                  <td class="text-danger">${{ formatNumber(row.low) }}</td>
                  <td>${{ formatNumber(row.close) }}</td>
                  <td>${{ formatVolume(row.volume) }}</td>
                  <td :class="row.change > 0 ? 'text-success' : 'text-danger'">
                    {{ row.change > 0 ? '+' : '' }}{{ row.change.toFixed(2) }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 分页 -->
          <div class="pagination-controls mt-3">
            <nav>
              <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <a class="page-link" @click="changePage(currentPage - 1)">上一页</a>
                </li>
                <li class="page-item" v-for="page in visiblePages" :key="page" :class="{ active: page === currentPage }">
                  <a class="page-link" @click="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <a class="page-link" @click="changePage(currentPage + 1)">下一页</a>
                </li>
              </ul>
            </nav>
            <div class="text-center text-muted small">
              共 {{ queryResult.dataPoints }} 条数据，每页显示 {{ pageSize }} 条
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-if="!queryResult && !loading">
      <i class="bi bi-inbox"></i>
      <h4>暂无数据</h4>
      <p>请选择日期范围并点击查询按钮</p>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'

export default {
  name: 'HistoryView',
  props: {
    historicalData: Object,
    statistics: Object
  },
  data() {
    return {
      startDate: this.getDateStr(-30),
      endDate: this.getDateStr(0),
      granularity: '1h',
      dataType: 'ohlcv',
      loading: false,
      queryResult: null,
      chartType: 'line',
      historyChart: null,
      distributionChart: null,
      currentPage: 1,
      pageSize: 50,
      apiBaseUrl: 'http://localhost:5001/api'
    }
  },
  computed: {
    totalPages() {
      return this.queryResult ? Math.ceil(this.queryResult.dataPoints / this.pageSize) : 0
    },
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    }
  },
  watch: {
    chartType() {
      this.renderHistoryChart()
    }
  },
  methods: {
    getDateStr(daysOffset) {
      const date = new Date()
      date.setDate(date.getDate() + daysOffset)
      return date.toISOString().split('T')[0]
    },
    selectRange(days) {
      this.startDate = this.getDateStr(-days)
      this.endDate = this.getDateStr(0)
    },
    async queryData() {
      this.loading = true
      this.currentPage = 1  // 每次查询重置到第一页
      
      try {
        // 计算查询天数
        const daysDiff = Math.ceil((new Date(this.endDate) - new Date(this.startDate)) / (1000 * 60 * 60 * 24))
        
        // 调用真实API
        const response = await axios.get(`${this.apiBaseUrl}/historical?days=${Math.max(daysDiff, 7)}`)
        
        if (!response.data.success) {
          throw new Error('Failed to fetch data')
        }
        
        const apiData = response.data.data
        
        // 转换API数据格式
        const data = []
        const prices = apiData.prices || []
        const volumes = apiData.volumes || []
        const timestamps = apiData.timestamps || []
        
        for (let i = 0; i < prices.length; i++) {
          const price = prices[i]
          // 使用价格本身作为 OHLC，避免生成不一致的数据
          // 由于后端只返回单一价格点，我们将其用作所有 OHLC 值
          const open = i > 0 ? prices[i - 1] : price
          const close = price
          const high = Math.max(open, close)
          const low = Math.min(open, close)
          
          data.push({
            time: timestamps[i] || new Date().toLocaleString('zh-CN'),
            open,
            high,
            low,
            close,
            volume: volumes[i] || 0,
            change: i > 0 ? ((close - prices[i - 1]) / prices[i - 1]) * 100 : 0
          })
        }
        
        // 后端返回的数据已经是从旧到新的顺序，适合图表显示
        console.log('收到数据 - 第一条时间:', data[0]?.time, '最后一条:', data[data.length-1]?.time)
        
        // 过滤日期范围
        const startTime = new Date(this.startDate).getTime()
        const endTime = new Date(this.endDate).getTime() + 24 * 60 * 60 * 1000
        const filteredData = data.filter(d => {
          const time = new Date(d.time).getTime()
          return time >= startTime && time <= endTime
        })
        
        const actualData = filteredData.length > 0 ? filteredData : data
        
        // 为表格准备反转的数据（最新的在前）
        const tableData = [...actualData].reverse()
        
        this.queryResult = {
          dataPoints: actualData.length,
          highPrice: Math.max(...actualData.map(d => d.high)),
          lowPrice: Math.min(...actualData.map(d => d.low)),
          avgPrice: actualData.reduce((sum, d) => sum + d.close, 0) / actualData.length,
          totalVolume: actualData.reduce((sum, d) => sum + d.volume, 0),
          priceChange: actualData.length > 1 ? ((actualData[actualData.length - 1].close - actualData[0].open) / actualData[0].open) * 100 : 0,
          data: tableData.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize),
          allData: actualData,  // 图表用：从旧到新
          tableData: tableData  // 表格用：从新到旧
        }
      } catch (error) {
        console.error('Query data error:', error)
        this.$emit('show-toast', '获取数据失败，显示模拟数据', 'warning')
        
        // 失败时使用模拟数据
        const daysDiff = Math.ceil((new Date(this.endDate) - new Date(this.startDate)) / (1000 * 60 * 60 * 24))
        const dataPoints = daysDiff * 24 // 移除720限制
        
        const data = []
        let basePrice = this.statistics?.current_price || 70000
        
        // 使用确定性的伪随机数生成器，基于索引值
        const getSeededValue = (index, seed, min, max) => {
          const x = Math.sin(index * seed) * 10000
          return min + (x - Math.floor(x)) * (max - min)
        }
        
        for (let i = 0; i < dataPoints; i++) {
          // 使用基于索引的确定性变化，而不是随机数
          const changeSeed = getSeededValue(i, 12.9898, -0.01, 0.01)
          const open = basePrice
          const close = basePrice * (1 + changeSeed)
          const high = Math.max(open, close) * (1 + 0.005)
          const low = Math.min(open, close) * (1 - 0.005)
          const volume = getSeededValue(i, 78.233, 10000000, 60000000)
          
          const date = new Date(this.startDate)
          date.setHours(date.getHours() + i)
          
          data.push({
            time: date.toLocaleString('zh-CN'),
            open,
            high,
            low,
            close,
            volume,
            change: ((close - open) / open) * 100
          })
          
          basePrice = close
        }
        
        this.queryResult = {
          dataPoints,
          highPrice: Math.max(...data.map(d => d.high)),
          lowPrice: Math.min(...data.map(d => d.low)),
          avgPrice: data.reduce((sum, d) => sum + d.close, 0) / data.length,
          totalVolume: data.reduce((sum, d) => sum + d.volume, 0),
          priceChange: ((data[data.length - 1].close - data[0].open) / data[0].open) * 100,
          data: data.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize),
          allData: data
        }
      }
      
      this.loading = false
      
      this.$nextTick(() => {
        this.renderCharts()
      })
    },
    renderCharts() {
      this.renderHistoryChart()
      this.renderDistributionChart()
    },
    renderHistoryChart() {
      if (!this.$refs.historyChart || !this.queryResult) return
      
      if (!this.historyChart) {
        this.historyChart = echarts.init(this.$refs.historyChart)
      }
      
      const data = this.queryResult.allData
      
      let option
      if (this.chartType === 'line') {
        option = {
          tooltip: { trigger: 'axis' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: {
            type: 'category',
            data: data.map(d => d.time),
            axisLabel: { rotate: 45, fontSize: 10 }
          },
          yAxis: { type: 'value', scale: true },
          series: [{
            name: '价格',
            type: 'line',
            data: data.map(d => d.close),
            smooth: true,
            lineStyle: { color: '#667eea', width: 2 },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(102, 126, 234, 0.5)' },
                { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
              ])
            }
          }]
        }
      } else {
        option = {
          tooltip: { trigger: 'axis' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: {
            type: 'category',
            data: data.map(d => d.time),
            axisLabel: { rotate: 45, fontSize: 10 }
          },
          yAxis: { type: 'value', scale: true },
          series: [{
            type: 'candlestick',
            data: data.map(d => [d.open, d.close, d.low, d.high]),
            itemStyle: {
              color: '#ef5350',
              color0: '#26a69a',
              borderColor: '#ef5350',
              borderColor0: '#26a69a'
            }
          }]
        }
      }
      
      this.historyChart.setOption(option)
    },
    renderDistributionChart() {
      if (!this.$refs.distributionChart || !this.queryResult) return
      
      if (!this.distributionChart) {
        this.distributionChart = echarts.init(this.$refs.distributionChart)
      }
      
      const data = this.queryResult.allData
      const gains = data.filter(d => d.change > 0).length
      const losses = data.filter(d => d.change < 0).length
      const flat = data.filter(d => d.change === 0).length
      
      const option = {
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [{
          name: '价格变化分布',
          type: 'pie',
          radius: '60%',
          data: [
            { value: gains, name: '上涨', itemStyle: { color: '#26a69a' } },
            { value: losses, name: '下跌', itemStyle: { color: '#ef5350' } },
            { value: flat, name: '持平', itemStyle: { color: '#999' } }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }
      
      this.distributionChart.setOption(option)
    },
    exportData(format) {
      if (!this.queryResult) return
      
      const data = this.queryResult.allData
      
      if (format === 'csv') {
        const csv = [
          ['时间', '开盘价', '最高价', '最低价', '收盘价', '交易量', '涨跌幅'],
          ...data.map(d => [d.time, d.open, d.high, d.low, d.close, d.volume, d.change])
        ].map(row => row.join(',')).join('\n')
        
        const blob = new Blob([csv], { type: 'text/csv' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `btc_history_${this.startDate}_${this.endDate}.csv`
        a.click()
      } else if (format === 'json') {
        const json = JSON.stringify(data, null, 2)
        const blob = new Blob([json], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `btc_history_${this.startDate}_${this.endDate}.json`
        a.click()
      }
    },
    showFullScreen() {
      alert('全屏功能开发中...')
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
      // 使用 tableData 进行分页（最新数据在前）
      this.queryResult.data = this.queryResult.tableData.slice((page - 1) * this.pageSize, page * this.pageSize)
    },
    formatNumber(num) {
      return num ? num.toLocaleString('en-US', { maximumFractionDigits: 2 }) : '0'
    },
    formatVolume(num) {
      if (!num) return '0'
      if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
      if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
      return num.toLocaleString('en-US', { maximumFractionDigits: 0 })
    }
  },
  beforeUnmount() {
    if (this.historyChart) this.historyChart.dispose()
    if (this.distributionChart) this.distributionChart.dispose()
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

.query-panel,
.stats-panel,
.chart-panel,
.table-panel {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.quick-select button {
  border-radius: 20px;
}

.stat-box {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.stat-label {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-controls button.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table thead {
  position: sticky;
  top: 0;
  z-index: 10;
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

.pagination-controls {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
}
</style>