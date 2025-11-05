<template>
  <div ref="chart" class="chart-container"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'PriceChart',
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
      handler(newVal) {
        if (newVal && newVal.timestamps && newVal.timestamps.length > 0) {
          this.$nextTick(() => {
            this.updateChart()
          })
        }
      },
      deep: true,
      immediate: false
    }
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chart)
      this.updateChart()
    },
    updateChart() {
      if (!this.data.timestamps || this.data.timestamps.length === 0) {
        console.warn('PriceChart: No data available')
        return
      }

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross' }
        },
        legend: {
          data: ['价格', 'MA5', 'MA10', 'MA20'],
          top: '5%',  // 将图例放在顶部
          left: 'center'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',  // 增加底部空间,避免与x轴标签重叠
          top: '15%',  // 增加顶部空间,为图例留出位置
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.data.timestamps,
          axisLabel: { 
            rotate: 45, 
            fontSize: 10,
            margin: 10  // 增加标签与轴的距离
          }
        },
        yAxis: {
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '价格',
            type: 'line',
            data: this.data.prices,
            smooth: true,
            lineStyle: { width: 3, color: '#667eea' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(102, 126, 234, 0.5)' },
                { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
              ])
            }
          },
          {
            name: 'MA5',
            type: 'line',
            data: this.data.ma_5,
            smooth: true,
            lineStyle: { color: '#f5576c', width: 2 }
          },
          {
            name: 'MA10',
            type: 'line',
            data: this.data.ma_10,
            smooth: true,
            lineStyle: { color: '#4facfe', width: 2 }
          },
          {
            name: 'MA20',
            type: 'line',
            data: this.data.ma_20,
            smooth: true,
            lineStyle: { color: '#00f2fe', width: 2 }
          }
        ]
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