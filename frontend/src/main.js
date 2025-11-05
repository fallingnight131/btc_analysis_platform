import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入 Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 导入 Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router)
app.mount('#app')