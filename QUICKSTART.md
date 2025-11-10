# 🚀 快速开始指南

## 一句话总结
**只需 Docker，3 个命令，5 分钟部署完整的比特币分析平台！**

---

## 📦 安装 Docker（首次使用）

### Windows
1. 下载 [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. 双击安装包，按提示完成安装
3. 重启电脑
4. 启动 Docker Desktop

### macOS
1. 下载 [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
2. 拖动到 Applications 文件夹
3. 启动 Docker.app
4. 等待 Docker 图标显示在菜单栏

### Linux (Ubuntu/Debian)
```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker
sudo systemctl start docker

# 安装 Docker Compose
sudo apt install docker-compose
```

---

## 🎯 部署比特币分析平台

### Windows 用户

```cmd
REM 1. 打开 PowerShell 或 CMD

REM 2. 克隆项目
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform

REM 3. 一键启动
docker-start.bat

REM 4. 等待 2-3 分钟，打开浏览器访问
REM http://localhost:8080
```

### macOS/Linux 用户

```bash
# 1. 打开终端

# 2. 克隆项目
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform

# 3. 一键启动
bash docker-start.sh

# 4. 等待 2-3 分钟，打开浏览器访问
# http://localhost:8080
```

---

## ✅ 验证部署

打开浏览器，依次访问：

1. **前端界面**: http://localhost:8080
   - 应该看到比特币分析平台首页
   - 显示实时价格和图表

2. **后端 API**: http://localhost:5001/api/health
   - 应该返回：`{"status": "ok", "timestamp": "..."}`

3. **查看日志**（可选）:
   ```bash
   docker-compose logs -f
   ```

---

## 🎬 视频演示时间线

### 0:00 - 0:30 | 安装 Docker
- 下载 Docker Desktop
- 双击安装
- 启动 Docker

### 0:30 - 1:00 | 克隆项目
```bash
git clone https://github.com/fallingnight131/btc_analysis_platform.git
cd btc_analysis_platform
```

### 1:00 - 1:10 | 一键启动
```bash
bash docker-start.sh  # macOS/Linux
# 或
docker-start.bat      # Windows
```

### 1:10 - 3:00 | 自动构建
- Docker 自动下载镜像
- 构建前端和后端容器
- 启动 MySQL 数据库
- 等待健康检查通过

### 3:00 - 3:30 | 访问应用
- 浏览器打开 http://localhost:8080
- 查看实时比特币价格
- 浏览技术分析图表

### 3:30 - 4:00 | 功能展示
- Dashboard 仪表盘
- 技术分析页面
- 历史数据查询
- 价格预测

### 4:00 - 4:30 | 管理命令
```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

---

## 🔧 常用管理命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 完全清理（包括数据）
docker-compose down -v
```

---

## 🐛 遇到问题？

### 端口被占用
```bash
# 修改 docker-compose.yml
# 将 "8080:80" 改为 "8081:80"
```

### Docker 未启动
```bash
# 检查 Docker 状态
docker info
```

### 查看详细错误
```bash
docker-compose logs
```

---

## 📚 更多信息

- 完整文档: [README.md](README.md)
- 开发指南: [CONTRIBUTING.md](CONTRIBUTING.md)
- 优化总结: [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)

---

**🎉 就这么简单！享受你的比特币分析平台吧！**
