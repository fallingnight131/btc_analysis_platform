import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 导入 Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 导入 Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// 配置 axios 基础URL
axios.defaults.baseURL = 'http://localhost:5001'

const app = createApp(App)

// 将 axios 注册为全局属性
app.config.globalProperties.$axios = axios

app.use(router)
app.mount('#app')