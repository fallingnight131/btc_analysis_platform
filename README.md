# 📊 Bitcoin Analysis Platform

> **比特币分析平台** - 使用 Docker 一键部署的全栈 Web 应用，提供实时比特币数据分析、价格预测、技术指标分析和风险评估。

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-brightgreen.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)

---

## ✨ 主要功能

- 📈 **实时数据监控** - 实时比特币价格、交易量和市场指标
- 📉 **技术分析图表** - K线图、成交量、RSI、MACD、布林带等多种技术指标
- 🔮 **价格预测** - 基于随机森林的机器学习价格预测
- ⚠️ **风险警报** - 智能风险评估和实时预警系统
- 📊 **历史数据分析** - 灵活的历史数据查询和统计分析（自动保留最近一年数据）
- 💾 **MySQL 数据库** - 生产级数据持久化
- 🔌 **离线模式** - 无网络时自动降级使用历史数据
- 🐳 **Docker 部署** - 一键启动，跨平台兼容（Windows/macOS/Linux）

---

## 🚀 快速开始

### 前置要求

只需要安装 Docker:

- **Docker Desktop**: [下载地址](https://docs.docker.com/get-docker/)
  - Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - macOS: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)

> 💡 **提示**: Docker Desktop 已包含 Docker Compose，无需单独安装。

---

### ⚙️ 安装后配置（重要）

#### macOS 用户 - PATH 配置

如果安装 Docker Desktop 后,终端提示找不到 `docker` 命令,请执行以下操作:

**临时解决**（当前终端会话有效）:
```bash
export PATH="/usr/local/bin:$PATH"
```

**永久解决**（推荐）:
```bash
# 将 Docker 路径添加到 shell 配置文件
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

> 💡 **说明**: Docker Desktop 会自动创建符号链接到 `/usr/local/bin/`,但某些终端配置可能不包含此路径。

#### 🇨🇳 中国大陆用户 - 镜像加速器配置

由于网络原因,拉取 Docker 镜像可能会很慢或超时。**强烈建议**配置镜像加速器:

**配置步骤:**

1. 打开 Docker Desktop
2. 点击右上角 **设置图标** (⚙️)
3. 选择 **Docker Engine**
4. 在编辑器中找到 `"registry-mirrors"` 配置项,添加以下内容:

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.nju.edu.cn"
  ]
}
```

5. 点击 **Apply & Restart** (应用并重启)
6. 等待 Docker 重启完成（约 10-30 秒）

**验证配置:**
```bash
docker info | grep -A 5 "Registry Mirrors"
```

应该看到类似输出:
```
Registry Mirrors:
  https://docker.m.daocloud.io/
  https://dockerproxy.com/
  https://docker.nju.edu.cn/
```

> ⚡ **效果**: 配置后,镜像下载速度可提升 **10-50 倍**,构建时间从 10 分钟缩短到 2-3 分钟。

---

### 三步部署

#### 1️⃣ 克隆项目

```bash
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform
```

#### 2️⃣ 一键启动

**macOS/Linux:**
```bash
bash docker-start.sh
```

**Windows:**
```cmd
docker-start.bat
```

或者手动执行:
```bash
docker-compose up -d --build
```

#### 3️⃣ 访问应用

启动完成后（约 2-3 分钟），在浏览器中打开:

- 🌐 **前端界面**: http://localhost:8080
- 🔌 **后端 API**: http://localhost:5001
- 🗄️ **MySQL 数据库**: localhost:3306

🎉 **恭喜！你已经成功部署了比特币分析平台！**

---

## 🐳 Docker 管理

### 🚀 启动和停止

**启动服务:**
```bash
# 首次启动（自动构建）
docker-compose up -d

# 或使用启动脚本
bash docker-start.sh        # macOS/Linux
docker-start.bat            # Windows（双击运行）
```

**停止服务（释放内存和CPU）:**
```bash
docker-compose down
```
> ✅ 停止后会立即释放内存和 CPU，但保留镜像和数据  
> ✅ 下次启动只需 10-20 秒

**重启服务:**
```bash
# 方式 1: 重启所有服务
docker-compose restart

# 方式 2: 重启特定服务
docker-compose restart backend
docker-compose restart frontend
docker-compose restart mysql

# 方式 3: 停止后重新启动
docker-compose down
docker-compose up -d
```

### 📋 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志（所有服务）
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql

# 查看实时资源占用
docker stats

# 查看磁盘占用
docker system df

# 重新构建并启动（修改代码后）
docker-compose up -d --build
```

### 🗑️ 清理和删除

```bash
# 停止并删除容器（保留镜像和数据）
docker-compose down

# 停止并删除数据卷（⚠️ 数据库数据会丢失）
docker-compose down -v

# 完全清理（包括镜像）
docker-compose down
docker rmi btc_analysis_platform-backend btc_analysis_platform-frontend mysql:8.0
```

### 💾 资源占用说明

**容器运行时（Up 状态）:**
- 磁盘: ~2.4GB (镜像文件)
- 内存: ~500MB-1GB
- CPU: 1-5% (空闲) / 10-30% (处理请求)

**容器停止后（执行 `docker-compose down`）:**
- 磁盘: ~2.4GB (镜像保留，快速重启)
- 内存: 0 (已释放) ✅
- CPU: 0 (已释放) ✅

> 💡 **建议**: 不使用时执行 `docker-compose down` 停止服务，释放系统资源

### 💡 重要说明

**电脑重启后无需重新构建:**
- ✅ Docker 镜像会永久保存在磁盘
- ✅ 数据库数据会自动恢复（存储在 Docker 数据卷）
- ⚡ 重启后只需 `docker compose up -d`（10-20 秒快速启动）
- 🚫 **不需要** 再执行 `--build`（除非修改了代码）

**何时需要重新构建:**
```bash
# 修改代码/依赖后才需要重建
docker compose up -d --build

# 或只重建特定服务
docker compose up -d --build backend
docker compose up -d --build frontend
```

需要重建的情况:
- ✏️ 修改了 `Dockerfile`
- ✏️ 修改了 `requirements.txt` (Python 依赖)
- ✏️ 修改了 `package.json` (Node.js 依赖)
- ✏️ 修改了应用源代码

**首次启动 vs 重启对比:**

| 操作 | 首次启动 | 电脑重启后 |
|------|----------|------------|
| 时间 | 3-5 分钟 | **10-20 秒** ⚡ |
| 下载 | 需要 | 无需 ✅ |
| 构建 | 需要 | 无需 ✅ |
| 数据 | 初始化 | 自动恢复 ✅ |

### 服务架构

项目包含 3 个 Docker 服务:

| 服务 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| **MySQL** | `btc_analysis_platform_mysql` | 3306 | 数据库服务（MySQL 8.0） |
| **Backend** | `btc_analysis_platform_backend` | 5001 | Flask API 服务（Python 3.11） |
| **Frontend** | `btc_analysis_platform_frontend` | 8080 | Vue 3 + Nginx 静态服务 |

---

## 📁 项目结构

```
btc_analysis_platform/
├── docker-compose.yml         # Docker 编排配置
├── .dockerignore             # Docker 构建忽略
├── .gitignore                # Git 忽略配置
├── .env.example              # 环境变量模板
├── docker-start.sh           # 启动脚本 (macOS/Linux)
├── docker-start.bat          # 启动脚本 (Windows)
│
├── README.md                  # 📖 项目文档（用户部署）
├── QUICKSTART.md             # 🚀 快速开始指南
├── CONTRIBUTING.md           # 🤝 开发者贡献指南
├── LICENSE                   # 📄 MIT 开源协议
│
├── backend/                   # 后端服务
│   ├── Dockerfile            # 后端 Docker 镜像
│   ├── app.py                # Flask 应用入口
│   ├── routes.py             # API 路由
│   ├── api.py                # CoinGecko API 集成
│   ├── database.py           # MySQL 数据库管理
│   ├── cache.py              # 缓存管理
│   ├── utils.py              # 工具函数（技术指标）
│   ├── requirements.txt      # Python 依赖
│   └── data/                 # 数据目录（Docker 卷挂载）
│
└── frontend/                  # 前端服务
    ├── Dockerfile            # 前端 Docker 镜像
    ├── nginx.conf            # Nginx 配置
    ├── src/                  # Vue 3 源码
    │   ├── views/           # 页面组件
    │   ├── components/      # UI 组件
    │   └── router/          # 路由配置
    ├── package.json          # npm 依赖
    └── vue.config.js         # Vue 配置
```

---

## 🔌 API 端点

后端提供以下 RESTful API:

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/realtime` | GET | 获取实时价格和市场数据 |
| `/api/historical?days=7` | GET | 获取历史数据（7/30/90/365天） |
| `/api/statistics?days=7` | GET | 获取统计数据 |
| `/api/prediction` | GET | 获取价格预测 |
| `/api/risk-alerts` | GET | 获取风险警报 |
| `/api/candlestick?days=7` | GET | 获取 K 线数据 |

### 示例请求

```bash
# 健康检查
curl http://localhost:5001/api/health

# 获取实时数据
curl http://localhost:5001/api/realtime

# 获取最近 30 天历史数据
curl http://localhost:5001/api/historical?days=30

# 获取价格预测
curl http://localhost:5001/api/prediction
```

---

## 🛠 技术栈

### 后端
- **Flask 3.0** - Python Web 框架
- **MySQL 8.0** - 关系型数据库
- **Pandas** - 数据处理
- **Scikit-learn** - 机器学习（价格预测）
- **CoinGecko API** - 加密货币数据源

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vue Router 4** - 路由管理
- **ECharts 6** - 数据可视化
- **Bootstrap 5** - UI 框架
- **Nginx** - Web 服务器（生产环境）

### 部署
- **Docker** - 容器化
- **Docker Compose** - 多容器编排

---

## 📊 数据库说明

### 自动数据保留策略

- 数据库**自动保留最近 365 天**的历史数据
- 查询超过 1 年的数据时，会实时从 CoinGecko API 获取（不写入数据库）
- 每次保存新数据时会自动清理过期数据（>365天）
- 数据存储在 Docker 卷 `mysql_data` 中，持久化保存

### 数据备份与恢复

```bash
# 备份数据库
docker exec btc-mysql mysqldump -u root -pbitcoin123 bitcoin_db > backup.sql

# 恢复数据库
docker exec -i btc-mysql mysql -u root -pbitcoin123 bitcoin_db < backup.sql

# 备份数据卷
docker run --rm -v btc_analysis_platform_mysql_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/mysql_backup.tar.gz /data
```

---

## 🐛 常见问题

### 1. Docker 服务启动失败

**问题**: `docker-compose up` 报错

**解决方法**:
```bash
# 检查 Docker 是否运行
docker info

# 查看详细日志
docker-compose logs

# 完全重建
docker-compose down -v
docker-compose up -d --build
```

### 2. 端口被占用

**问题**: `Bind for 0.0.0.0:8080 failed: port is already allocated`

**解决方法**:
```bash
# 修改 docker-compose.yml 中的端口映射
# 例如将 "8080:80" 改为 "8081:80"
```

或者停止占用端口的服务:
```bash
# macOS/Linux
lsof -i :8080
kill -9 <PID>

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### 3. 前端页面空白

**可能原因**:
- 后端服务未就绪
- API 连接失败

**解决方法**:
```bash
# 1. 检查所有服务状态
docker-compose ps

# 2. 查看后端日志
docker-compose logs backend

# 3. 测试 API 连接
curl http://localhost:5001/api/health

# 4. 重启服务
docker-compose restart
```

### 4. 数据库连接失败

**问题**: 后端日志显示 MySQL 连接错误

**解决方法**:
```bash
# 1. 等待 MySQL 完全启动（首次启动需要 30-60 秒）
docker-compose logs mysql

# 2. 检查 MySQL 健康状态
docker-compose ps

# 3. 手动重启后端（等 MySQL 就绪后）
docker-compose restart backend
```

### 5. API 返回 429 错误

**原因**: CoinGecko 免费 API 有请求频率限制（50次/分钟）

**解决方案**:
- 系统已实现 30 分钟缓存机制
- API 失败时自动降级到数据库历史数据
- 建议等待几分钟后重试

---

## 🔧 开发调试

### 查看实时日志

```bash
# 所有服务
docker-compose logs -f

# 只看后端
docker-compose logs -f backend

# 只看前端
docker-compose logs -f frontend

# 只看 MySQL
docker-compose logs -f mysql
```

### 进入容器内部

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 进入 MySQL 容器
docker-compose exec mysql bash

# 连接 MySQL 数据库
docker-compose exec mysql mysql -u bitcoin_user -pbitcoin123 bitcoin_db
```

### 修改代码后重新构建

```bash
# 只重建后端
docker-compose up -d --build backend

# 只重建前端
docker-compose up -d --build frontend

# 重建所有服务
docker-compose up -d --build
```

---

## 🚀 生产环境部署

### 使用 HTTPS

1. 修改 `docker-compose.yml`，添加 Nginx 反向代理
2. 配置 SSL 证书（Let's Encrypt 推荐）
3. 更新前端 API 地址为 HTTPS

### 性能优化建议

- **MySQL**: 调整 `docker-compose.yml` 中的内存限制
- **后端**: 增加 Gunicorn worker 数量（修改 `backend/Dockerfile`）
- **前端**: 已使用 Nginx + Gzip 压缩，生产就绪

### 监控与日志

```bash
# 实时监控资源使用
docker stats

# 导出日志到文件
docker-compose logs > app.log
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🐛 故障排查

遇到问题？查看 **[故障排查指南](TROUBLESHOOTING.md)**，包含:

- ✅ Docker 安装配置（PATH、镜像加速器）
- ✅ 容器健康检查失败
- ✅ 网络和端口问题
- ✅ 数据库连接问题
- ✅ 磁盘空间管理
- ✅ 完全重新部署步骤

---

## 📚 相关文档

- 📖 [快速开始指南](QUICKSTART.md) - 5 分钟快速部署
- 🔧 [故障排查指南](TROUBLESHOOTING.md) - 常见问题解决
- 👨‍💻 [开发指南](CONTRIBUTING.md) - 本地开发和贡献
- 📝 [优化总结](OPTIMIZATION_SUMMARY.md) - 项目优化历程

---

## 📄 开源协议

本项目采用 MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **GitHub**: [@fallingnight131](https://github.com/fallingnight131)
- **项目地址**: https://github.com/fallingnight131/btc_analysis_platform

---

## 🙏 致谢

- [CoinGecko API](https://www.coingecko.com/api) - 免费的加密货币数据
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Python Web 框架
- [ECharts](https://echarts.apache.org/) - 强大的数据可视化库
- [Docker](https://www.docker.com/) - 容器化平台

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
