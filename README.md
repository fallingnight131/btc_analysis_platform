# 📊 Bitcoin Analysis Platform

比特币分析平台是一个全栈 Web 应用，提供实时比特币数据分析、价格预测、风险评估等功能。

## ✨ 主要功能

- 📈 **实时数据监控** - 实时比特币价格、交易量和市场指标
- 📉 **技术分析图表** - K线图、成交量、RSI 等多种技术指标
- 🔮 **价格预测** - 基于机器学习的价格预测功能
- ⚠️ **风险警报** - 智能风险评估和预警系统
- 📊 **历史数据分析** - 完整的历史数据查询和统计
- 💾 **数据库支持** - SQLite 本地数据持久化
- 🔌 **离线模式** - 无网络时自动使用历史数据
- 🎨 **响应式界面** - 基于 Vue 3 和 Bootstrap 5 的现代化 UI

## 🛠 技术栈

### 后端
- **Flask 3.0.0** - Web 框架
- **Flask-CORS** - 跨域请求处理
- **Pandas** - 数据处理
- **NumPy** - 数值计算
- **Scikit-learn** - 机器学习
- **SQLite** - 本地数据库（内置）
- **Requests** - HTTP 请求

### 前端
- **Vue 3** - 前端框架
- **Vue Router 4** - 路由管理
- **ECharts 6** - 数据可视化
- **Bootstrap 5** - UI 组件库
- **Axios** - HTTP 客户端
- **Day.js** - 日期处理

## 📋 系统要求

- **Python** 3.8 或更高版本
- **Node.js** 14 或更高版本
- **npm** 6 或更高版本

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform
```

### 2. 后端设置

#### 2.1 创建虚拟环境（推荐）

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
# venv\Scripts\activate  # Windows
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 启动后端服务

```bash
python app.py
```

后端服务将在 `http://localhost:5001` 启动

### 3. 前端设置

打开新的终端窗口：

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 启动开发服务器

```bash
npm run serve
```

前端应用将在 `http://localhost:8080` 启动

### 4. 访问应用

在浏览器中打开 `http://localhost:8080` 即可使用应用。

## 📦 项目结构

```
btc_analysis_platform/
├── backend/                 # 后端代码
│   ├── app.py              # Flask 应用入口
│   ├── routes.py           # 路由定义
│   ├── api.py              # API 业务逻辑
│   ├── cache.py            # 缓存管理
│   ├── utils.py            # 工具函数
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── public/            # 静态资源
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   │   ├── charts/   # 图表组件
│   │   │   ├── ChartCard.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── PageHeader.vue
│   │   │   ├── PredictionCard.vue
│   │   │   ├── RiskAlerts.vue
│   │   │   └── StatCards.vue
│   │   ├── views/        # 页面视图
│   │   │   ├── Dashboard.vue
│   │   │   ├── Analysis.vue
│   │   │   ├── History.vue
│   │   │   ├── Trading.vue
│   │   │   └── Settings.vue
│   │   ├── router/       # 路由配置
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 应用入口
│   └── package.json      # npm 依赖
└── README.md             # 项目文档
```

## 🔌 API 端点

后端提供以下 API 接口：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/realtime` | GET | 获取实时数据 |
| `/api/historical` | GET | 获取历史数据 |
| `/api/statistics` | GET | 获取统计数据 |
| `/api/prediction` | GET | 获取价格预测 |
| `/api/risk-alerts` | GET | 获取风险警报 |
| `/api/candlestick` | GET | 获取K线数据 |

### 示例请求

```bash
# 获取实时数据
curl http://localhost:5001/api/realtime

# 获取历史数据（最近7天）
curl http://localhost:5001/api/historical?days=7

# 获取价格预测
curl http://localhost:5001/api/prediction
```

## 🏗 生产部署

### 后端部署

#### 使用 Gunicorn（推荐）

1. 安装 Gunicorn：
```bash
pip install gunicorn
```

2. 启动服务：
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5001 "app:create_app()"
```

#### 使用 Docker

1. 创建 `backend/Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:create_app()"]
```

2. 构建并运行：
```bash
cd backend
docker build -t btc-backend .
docker run -d -p 5001:5001 btc-backend
```

### 前端部署

#### 构建生产版本

```bash
cd frontend
npm run build
```

构建完成后，`dist` 目录包含所有静态文件。

#### 使用 Nginx

1. 将 `dist` 目录内容复制到 Nginx 服务器

2. Nginx 配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/btc-platform;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### 使用 Docker

1. 创建 `frontend/Dockerfile`：
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

2. 构建并运行：
```bash
cd frontend
docker build -t btc-frontend .
docker run -d -p 80:80 btc-frontend
```

### 使用 Docker Compose（推荐）

创建项目根目录下的 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

启动所有服务：
```bash
docker-compose up -d
```

## 🔧 环境变量配置

### 后端环境变量

创建 `backend/.env` 文件：

```env
FLASK_ENV=production
PORT=5001
API_TIMEOUT=30
CACHE_TIMEOUT=60
```

### 前端环境变量

创建 `frontend/.env.production` 文件：

```env
VUE_APP_API_BASE_URL=https://your-api-domain.com
```

## 🧪 开发指南

### 后端开发

```bash
cd backend
# 激活虚拟环境
source venv/bin/activate
# 以调试模式运行
python app.py
```

### 前端开发

```bash
cd frontend
# 启动开发服务器（热重载）
npm run serve
# 代码检查
npm run lint
```

## 📝 常见问题

### 1. CORS 错误
确保后端已启用 Flask-CORS，并且前端请求的 API 地址正确。

### 2. 端口被占用
修改 `backend/app.py` 中的端口号，或使用环境变量：
```bash
PORT=5002 python app.py
```

### 3. 依赖安装失败
尝试升级 pip：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 离线模式
- **查看离线模式说明**: 请阅读 [DATABASE_OFFLINE_MODE.md](DATABASE_OFFLINE_MODE.md)
- **测试离线功能**: `cd backend && python test_offline.py`
- **数据库位置**: `backend/bitcoin_data.db`（自动创建）

### 4. 前端构建失败
清除缓存并重新安装：
```bash
rm -rf node_modules package-lock.json
npm install
```