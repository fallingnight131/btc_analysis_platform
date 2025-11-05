<template>
  <div ref="chart" class="chart-container"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'RSIChart',
  props: {
    data: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.initChart()
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose()
    }
    window.removeEventListener('resize', this.handleResize)
  },
  watch: {
    data: {
      handler() {
        this.updateChart()
      },
      deep: true
    }
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chart)
      this.updateChart()
    },
    updateChart() {
      if (!this.data.timestamps || this.data.timestamps.length === 0) return

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
          data: this.data.timestamps,
          axisLabel: { rotate: 45, fontSize: 10 }
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          splitLine: {
            lineStyle: { color: '#ddd' }
          }
        },
        visualMap: {
          show: false,
          pieces: [
            { gt: 70, lte: 100, color: '#ef5350' },
            { gt: 30, lte: 70, color: '#ffa726' },
            { gte: 0, lte: 30, color: '#26a69a' }
          ]
        },
        series: [{
          name: 'RSI',
          type: 'line',
          data: this.data.rsi,
          smooth: true,
          lineStyle: { width: 3 },
          markLine: {
            data: [
              { yAxis: 70, label: { formatter: '超买 70' } },
              { yAxis: 30, label: { formatter: '超卖 30' } }
            ],
            lineStyle: { color: '#999', type: 'dashed' }
          }
        }]
      }
      this.chart.setOption(option)
    },
    handleResize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>