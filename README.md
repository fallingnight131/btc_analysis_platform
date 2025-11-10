# 📊 Bitcoin Analysis Platform

比特币分析平台 - 一个功能完整的全栈 Web 应用，提供实时比特币数据分析、价格预测、技术指标分析和风险评估。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-brightgreen.svg)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)

## ✨ 主要功能

- 📈 **实时数据监控** - 实时比特币价格、交易量和市场指标
- 📉 **技术分析图表** - K线图、成交量、RSI、MACD、布林带等多种技术指标
- 🔮 **价格预测** - 基于随机森林的机器学习价格预测
- ⚠️ **风险警报** - 智能风险评估和实时预警系统
- 📊 **历史数据分析** - 灵活的历史数据查询和统计分析
- 💾 **MySQL 数据库** - 生产级数据持久化（自动保留最近一年数据）
- 🔌 **离线模式** - 无网络时自动降级使用历史数据
- 🎨 **响应式界面** - 基于 Vue 3 和 Bootstrap 5 的现代化 UI

## 🛠 技术栈

| 分类 | 技术 |
|------|------|
| **后端** | Flask 3.0, Python 3.8+, MySQL 5.7+ |
| **数据处理** | Pandas, NumPy, Scikit-learn |
| **前端** | Vue 3, Vue Router 4, ECharts 6, Bootstrap 5 |
| **数据源** | CoinGecko API |
| **部署** | Gunicorn, Nginx (可选) |

## 📋 系统要求

### 必需
- **Python** 3.8 或更高版本
- **Node.js** 14 或更高版本（含 npm）
- **MySQL** 5.7 或更高版本（推荐使用 Anaconda MySQL）

### 推荐配置
- **操作系统**: macOS / Linux / Windows 10+
- **内存**: 4GB RAM 或更高
- **磁盘空间**: 至少 500MB 可用空间

---

## 🚀 完整部署指南

### 第一步：克隆项目

```bash
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform
```

### 第二步：MySQL 数据库安装与配置

#### 选项 A：使用 Anaconda MySQL（推荐）

如果你已安装 Anaconda，可以直接使用：

```bash
# 1. 启动 MySQL
cd backend
bash scripts/start_mysql.sh

# 2. 设置密码（首次启动需要）
/opt/anaconda3/bin/mysql -u root

# 在 MySQL 命令行中执行：
ALTER USER 'root'@'localhost' IDENTIFIED BY 'bitcoin123';
CREATE DATABASE IF NOT EXISTS bitcoin_db;
CREATE USER IF NOT EXISTS 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';
GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 选项 B：使用系统 MySQL

**macOS (使用 Homebrew):**
```bash
# 安装 MySQL
brew install mysql

# 启动 MySQL
brew services start mysql

# 安全配置
mysql_secure_installation

# 创建数据库和用户
mysql -u root -p
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
mysql -u root -p
```

**在 MySQL 中执行：**
```sql
CREATE DATABASE bitcoin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';
GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 第三步：后端设置

#### 1. 创建 Python 虚拟环境（推荐）

```bash
cd backend

# 使用 venv
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
# venv\Scripts\activate  # Windows

# 或使用 conda
conda create -n btc_analysis_platform python=3.11
conda activate btc_analysis_platform
```

#### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 3. 验证数据库连接

```bash
# 测试 MySQL 连接
python tests/test_mysql_connection.py

# 查看数据库状态
python tests/check_db_status.py
```

#### 4. 启动后端服务

```bash
python app.py
```

成功启动后会看到：
```
✅ MySQL 数据库初始化成功
 * Running on http://127.0.0.1:5001
```

> 💡 **提示**: 后端会自动创建数据库表，首次启动时会进行初始化。

### 第四步：前端设置

打开**新的终端窗口**：

#### 1. 安装 Node.js 依赖

```bash
cd frontend
npm install
```

如果 `npm install` 速度慢，可以使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

#### 2. 启动前端开发服务器

```bash
npm run serve
```

成功启动后会看到：
```
  App running at:
  - Local:   http://localhost:8080/
```

### 第五步：访问应用

在浏览器中打开：**http://localhost:8080**

🎉 恭喜！你已经成功部署了比特币分析平台！

---

## 📁 项目结构

```
btc_analysis_platform/
├── backend/                    # 后端代码
│   ├── app.py                 # Flask 应用入口
│   ├── routes.py              # API 路由定义
│   ├── api.py                 # CoinGecko API 集成
│   ├── database.py            # MySQL 数据库管理
│   ├── cache.py               # 缓存管理
│   ├── utils.py               # 工具函数（技术指标计算）
│   ├── requirements.txt       # Python 依赖
│   ├── data/                  # 数据库数据目录
│   │   └── mysql/            # MySQL 数据文件
│   ├── scripts/               # MySQL 管理脚本
│   │   ├── start_mysql.sh    # 启动 MySQL
│   │   ├── stop_mysql.sh     # 停止 MySQL
│   │   └── check_mysql.sh    # 检查状态
│   └── tests/                 # 测试脚本
│       ├── check_db_status.py    # 数据库状态检查
│       └── test_mysql_connection.py
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   │   ├── Dashboard.vue  # 仪表盘
│   │   │   ├── Analysis.vue   # 技术分析
│   │   │   ├── History.vue    # 历史数据
│   │   │   ├── Trading.vue    # 模拟交易
│   │   │   └── Settings.vue   # 设置
│   │   ├── components/        # UI 组件
│   │   └── router/           # 路由配置
│   ├── package.json          # npm 依赖
│   └── vue.config.js         # Vue 配置
└── README.md                  # 本文档
```

---

## 🔌 API 端点

后端提供以下 RESTful API 接口：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/realtime` | GET | 获取实时价格和市场数据 |
| `/api/historical?days=7` | GET | 获取历史数据（支持 7/30/90/365 天） |
| `/api/statistics?days=7` | GET | 获取统计数据 |
| `/api/prediction` | GET | 获取价格预测 |
| `/api/risk-alerts` | GET | 获取风险警报 |
| `/api/candlestick?days=7` | GET | 获取 K 线数据 |

### 示例请求

```bash
# 获取实时数据
curl http://localhost:5001/api/realtime

# 获取最近 30 天历史数据
curl http://localhost:5001/api/historical?days=30

# 获取价格预测
curl http://localhost:5001/api/prediction
```

---

## 🔧 常用命令

### 后端管理

```bash
cd backend

# 启动后端
python app.py

# 查看数据库状态
python tests/check_db_status.py

# MySQL 管理
bash scripts/start_mysql.sh      # 启动 MySQL
bash scripts/stop_mysql.sh       # 停止 MySQL
bash scripts/check_mysql.sh      # 检查状态
bash scripts/restart_mysql.sh    # 重启 MySQL
```

### 前端开发

```bash
cd frontend

# 开发模式（热重载）
npm run serve

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

---

## 🐛 常见问题

### 1. MySQL 连接失败

**错误**: `Can't connect to MySQL server`

**解决方法**:
```bash
# 检查 MySQL 是否运行
bash backend/scripts/check_mysql.sh

# 如果未运行，启动 MySQL
bash backend/scripts/start_mysql.sh

# 检查端口是否被占用
lsof -i :3306
```

### 2. 端口被占用

**错误**: `Address already in use`

**解决方法**:
```bash
# 查找占用端口的进程
lsof -i :5001   # 后端端口
lsof -i :8080   # 前端端口

# 杀死进程
kill -9 <PID>

# 或修改端口号
# 后端: 在 backend/app.py 中修改 port=5001
# 前端: 在 frontend/vue.config.js 中修改 devServer.port
```

### 3. API 请求 429 错误（限流）

**原因**: CoinGecko 免费 API 有请求频率限制

**解决方法**:
- 系统已实现缓存机制（30 分钟）
- API 失败时自动降级到数据库
- 建议等待几分钟后重试

### 4. 前端页面空白

**可能原因**:
1. 后端未启动
2. API 地址配置错误

**解决方法**:
```bash
# 1. 确认后端运行
curl http://localhost:5001/api/health

# 2. 检查浏览器控制台错误
# 3. 清除浏览器缓存并刷新
```

### 5. npm install 失败

**解决方法**:
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm cache clean --force

# 使用国内镜像
npm install --registry=https://registry.npmmirror.com

# 或使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

### 6. Python 依赖安装失败

**解决方法**:
```bash
# 升级 pip
pip install --upgrade pip

# 分别安装可能有问题的包
pip install numpy
pip install pandas
pip install scikit-learn

# 重试
pip install -r requirements.txt
```

---

## 📊 数据库说明

### 数据保留策略

- 数据库**自动保留最近 365 天**的数据
- 查询超过 1 年的数据时，会实时从 API 获取（不写入数据库）
- 每次保存新数据时会自动清理过期数据

### 数据备份

```bash
# 备份数据库
tar -czf mysql_backup_$(date +%Y%m%d).tar.gz backend/data/mysql/

# 恢复数据库
# 1. 停止 MySQL
bash backend/scripts/stop_mysql.sh

# 2. 删除旧数据
rm -rf backend/data/mysql

# 3. 解压备份
tar -xzf mysql_backup_YYYYMMDD.tar.gz

# 4. 启动 MySQL
bash backend/scripts/start_mysql.sh
```

---

## 🏗 生产环境部署

### 使用 Gunicorn（推荐）

```bash
cd backend

# 安装 Gunicorn
pip install gunicorn

# 启动（4个工作进程）
gunicorn -w 4 -b 0.0.0.0:5001 "app:app"
```

### 使用 Nginx 反向代理

创建 Nginx 配置 `/etc/nginx/sites-available/btc-platform`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/btc-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 使用 Docker（可选）

```bash
# 构建后端镜像
cd backend
docker build -t btc-backend .

# 构建前端镜像
cd ../frontend
docker build -t btc-frontend .

# 使用 docker-compose
cd ..
docker-compose up -d
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 开源协议

MIT License

---

## 📞 联系方式

- **GitHub**: [@fallingnight131](https://github.com/fallingnight131)
- **项目地址**: https://github.com/fallingnight131/btc_analysis_platform

---

## 🙏 致谢

- [CoinGecko API](https://www.coingecko.com/api) - 提供免费的加密货币数据
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Web 框架
- [ECharts](https://echarts.apache.org/) - 强大的数据可视化库

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
