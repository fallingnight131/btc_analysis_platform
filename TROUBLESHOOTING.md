# 🔧 故障排查指南

本文档收集了部署和使用过程中可能遇到的常见问题及解决方案。

---

## ❓ 常见问题 FAQ

### 电脑重启后需要重新构建吗？

**答案: 不需要！** ✅

**说明:**
- Docker 镜像会永久保存在磁盘（约 2.4GB）
- MySQL 数据卷会自动恢复（约 210MB）
- 重启后只需执行 `docker compose up -d` 即可
- 启动时间：**10-20 秒**（vs 首次构建 3-5 分钟）

**重启后启动命令:**
```bash
# 方式 1: 使用脚本（会自动检测是否需要构建）
bash docker-start.sh

# 方式 2: 直接启动（推荐）
docker compose up -d
```

**何时需要重新构建:**
```bash
# 只有修改了代码或依赖时才需要
docker compose up -d --build
```

需要重建的情况:
- ✏️ 修改了 `Dockerfile`
- ✏️ 修改了 `requirements.txt` 或 `package.json`
- ✏️ 修改了源代码

**验证镜像是否存在:**
```bash
docker images | grep btc_analysis_platform
# 应该看到 backend 和 frontend 两个镜像
```

---

### 如何停止和重启容器？

**停止服务（释放内存和CPU）:**
```bash
docker-compose down
```

**效果:**
- ✅ 立即释放内存和 CPU
- ✅ 保留镜像文件（下次快速启动）
- ✅ 保留数据库数据
- ✅ 下次启动只需 10-20 秒

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

**资源占用对比:**

| 状态 | 磁盘 | 内存 | CPU |
|------|------|------|-----|
| 运行中 | 2.4GB | 500MB-1GB | 1-5% |
| 停止后 | 2.4GB | 0 ✅ | 0 ✅ |
| 删除镜像后 | 0 | 0 | 0 |

> 💡 **建议**: 不使用时执行 `docker-compose down` 停止服务

---

### 容器会一直占用资源吗？

**答案: 不会！** ✅

**说明:**
- 容器只有在 **Running 状态** 时才占用 CPU 和内存
- 执行 `docker-compose down` 后立即释放所有运行时资源
- 镜像文件只占用磁盘，不占用 CPU/内存

**查看当前状态:**
```bash
# 查看容器状态
docker-compose ps

# 查看资源占用
docker stats

# 查看磁盘占用
docker system df
```

---

**答案: 不会！** ✅

**说明:**
本项目使用完整的项目标识作为容器名称，避免与其他项目冲突。

**容器命名规则:**
```
项目名称_服务名称
例如: btc_analysis_platform_backend
```

**当前项目的容器名称:**
- `btc_analysis_platform_mysql`
- `btc_analysis_platform_backend`
- `btc_analysis_platform_frontend`

**查看容器名称:**
```bash
docker ps --format "table {{.Names}}\t{{.Image}}"
```

**优势:**
1. ✅ 可以同时运行多个 Docker 项目
2. ✅ 即使其他项目也有 backend/frontend，也不会冲突
3. ✅ 容器名称清晰易识别

**示例 - 同时运行多个项目:**
```bash
# 项目 1: 比特币分析平台
btc_analysis_platform_backend
btc_analysis_platform_frontend

# 项目 2: 比特币交易系统（假设）
btc_trading_system_backend
btc_trading_system_frontend

# 完全不冲突！✨
```

**常用命令:**
```bash
# 查看特定项目的容器日志
docker logs btc_analysis_platform_backend

# 进入特定项目的容器
docker exec -it btc_analysis_platform_backend bash

# 重启特定项目的容器
docker restart btc_analysis_platform_frontend
```

💡 **提示:** 使用 Tab 键可以自动补全容器名称！

---

## 📦 Docker 安装问题

### macOS: 找不到 `docker` 命令

**症状:**
```bash
$ docker --version
zsh: command not found: docker
```

**原因:** 
终端的 PATH 环境变量未包含 Docker 命令路径。

**解决方案:**

**方法 1: 临时修复（当前终端会话有效）**
```bash
export PATH="/usr/local/bin:$PATH"
docker --version  # 验证
```

**方法 2: 永久修复（推荐）**
```bash
# 添加到 zsh 配置文件
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 如果使用 bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

**验证:**
```bash
docker --version
# 应输出: Docker version 28.x.x, build ...

docker compose version
# 应输出: Docker Compose version v2.x.x
```

---

## 🌐 网络问题

### 中国大陆: Docker 镜像下载超时

**症状:**
```
ERROR: failed to solve: failed to fetch ...
=> => transferring dockerfile: ... 30.0s timeout
```

**原因:**
直接连接 Docker Hub (docker.io) 速度慢或被墙。

**解决方案: 配置镜像加速器**

#### Docker Desktop (Windows/macOS)

1. 打开 Docker Desktop
2. 点击右上角 **设置图标** (⚙️)
3. 选择 **Docker Engine** (左侧菜单)
4. 编辑 JSON 配置,添加 `registry-mirrors`:

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

5. 点击 **Apply & Restart**
6. 等待 Docker 重启（约 10-30 秒）

#### Linux (Docker Engine)

编辑或创建 `/etc/docker/daemon.json`:

```bash
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.nju.edu.cn"
  ]
}
EOF

# 重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

**验证配置:**
```bash
docker info | grep -A 5 "Registry Mirrors"
```

**预期输出:**
```
Registry Mirrors:
  https://docker.m.daocloud.io/
  https://dockerproxy.com/
  https://docker.nju.edu.cn/
```

**效果:**
- 构建时间从 **10 分钟** 缩短到 **2-3 分钟**
- 下载速度提升 **10-50 倍**

---

## 🐳 Docker 容器问题

### 容器健康检查失败

**症状:**
```bash
$ docker compose ps
NAME          STATUS
btc_backend   Up 2 minutes (unhealthy)
btc_frontend  Up 5 minutes (unhealthy)
```

**诊断步骤:**

#### 1. 查看健康检查日志
```bash
# 查看后端健康检查详情
docker inspect btc_backend --format='{{json .State.Health}}' | python3 -m json.tool

# 查看前端健康检查详情
docker inspect btc_frontend --format='{{json .State.Health}}' | python3 -m json.tool
```

#### 2. 常见原因和解决方案

**后端: curl 命令不存在**

**错误信息:**
```json
{
  "Status": "unhealthy",
  "Log": [{
    "ExitCode": -1,
    "Output": "exec: \"curl\": executable file not found in $PATH"
  }]
}
```

**解决方案:** 确保 `backend/Dockerfile` 包含 curl:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

重建容器:
```bash
docker compose up -d --build backend
```

**前端: localhost 连接被拒绝**

**错误信息:**
```json
{
  "Status": "unhealthy",
  "Log": [{
    "ExitCode": 1,
    "Output": "wget: can't connect to remote host: Connection refused"
  }]
}
```

**解决方案:** 在 `docker-compose.yml` 中将 `localhost` 改为 `127.0.0.1`:
```yaml
frontend:
  healthcheck:
    test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1:80"]
    interval: 30s
    timeout: 10s
    retries: 3
```

重启容器:
```bash
docker compose up -d frontend
```

#### 3. 验证服务实际可用性

即使显示 "unhealthy",服务可能仍在正常工作:

```bash
# 测试后端 API
curl http://localhost:5001/api/health

# 测试前端
curl -I http://localhost:8080
```

---

## 🔌 端口占用问题

**症状:**
```
Error: bind: address already in use
```

**解决方案:**

### 方法 1: 查找并停止占用端口的进程

```bash
# macOS/Linux: 查看端口占用
lsof -i :8080  # 前端端口
lsof -i :5001  # 后端端口
lsof -i :3306  # MySQL 端口

# 停止进程
kill -9 <PID>
```

```cmd
REM Windows: 查看端口占用
netstat -ano | findstr :8080

REM 停止进程
taskkill /PID <PID> /F
```

### 方法 2: 修改端口映射

编辑 `docker-compose.yml`,修改左侧端口（宿主机端口）:

```yaml
# 原配置
ports:
  - "8080:80"  # 前端
  - "5001:5001"  # 后端

# 修改为
ports:
  - "8081:80"  # 前端改为 8081
  - "5002:5001"  # 后端改为 5002
```

重启服务:
```bash
docker compose down
docker compose up -d
```

---

## 💾 数据库连接问题

### 后端无法连接 MySQL

**症状:**
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'mysql'")
```

**解决方案:**

#### 1. 确认 MySQL 容器健康
```bash
docker compose ps
# mysql 应该显示 (healthy)
```

#### 2. 检查数据库配置

在 `docker-compose.yml` 中确认:
```yaml
backend:
  environment:
    MYSQL_HOST: mysql  # 服务名称,不是 localhost
    MYSQL_PORT: 3306
    MYSQL_USER: bitcoin_user
    MYSQL_PASSWORD: bitcoin123
    MYSQL_DATABASE: bitcoin_db
  depends_on:
    mysql:
      condition: service_healthy  # 等待 MySQL 健康才启动
```

#### 3. 查看后端日志
```bash
docker compose logs backend | grep -i mysql
```

#### 4. 测试数据库连接

进入后端容器测试:
```bash
docker exec -it btc_backend bash

# 安装 MySQL 客户端
apt-get update && apt-get install -y default-mysql-client

# 测试连接
mysql -h mysql -u bitcoin_user -pbitcoin123 bitcoin_db
```

---

## 🗑️ 磁盘空间问题

### Docker 占用过多磁盘空间

**查看 Docker 磁盘使用:**
```bash
docker system df
```

**输出示例:**
```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          3         3         5.565GB   3.129GB (56%)
Containers      3         3         127B      0B (0%)
Local Volumes   1         1         210.6MB   0B (0%)
Build Cache     41        0         3.958GB   3.958GB (100%)
```

**清理策略:**

#### 1. 清理构建缓存（安全，推荐）
```bash
docker builder prune
# 可回收 ~4GB
```

#### 2. 清理未使用的镜像
```bash
docker image prune -a
```

#### 3. 完全清理（包括数据卷，谨慎使用）
```bash
# ⚠️ 警告: 会删除所有数据！
docker compose down -v  # 停止并删除数据卷
docker system prune -a --volumes  # 清理所有未使用资源
```

#### 4. 仅清理项目数据（保留其他 Docker 资源）
```bash
cd btc_analysis_platform
docker compose down -v  # 删除项目容器和数据卷
```

---

## 📝 日志查看

### 查看实时日志
```bash
# 所有服务
docker compose logs -f

# 特定服务
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mysql

# 最近 50 行
docker compose logs --tail 50 backend
```

### 查看容器内部状态
```bash
# 进入容器
docker exec -it btc_backend bash
docker exec -it btc_frontend sh
docker exec -it btc_mysql bash

# 查看进程
docker exec btc_backend ps aux

# 查看端口监听
docker exec btc_backend netstat -tlnp
docker exec btc_frontend netstat -tlnp
```

---

## 🔄 完全重新部署

如果遇到无法解决的问题,尝试完全重新部署:

```bash
# 1. 停止并删除所有容器和数据卷
docker compose down -v

# 2. 删除镜像（可选）
docker rmi btc_analysis_platform-backend btc_analysis_platform-frontend

# 3. 清理构建缓存
docker builder prune -f

# 4. 重新构建和启动
docker compose up -d --build

# 5. 查看启动日志
docker compose logs -f
```

---

## 🆘 获取帮助

如果以上方案都无法解决问题:

1. **查看完整日志:**
   ```bash
   docker compose logs > logs.txt
   ```

2. **检查系统信息:**
   ```bash
   docker info > docker-info.txt
   docker compose config > compose-config.txt
   ```

3. **提交 Issue:**
   - 访问: https://github.com/fallingnight131/btc_analysis_platform/issues
   - 附上日志文件和系统信息
   - 详细描述问题复现步骤

4. **联系方式:**
   - GitHub Issues (推荐)
   - 项目 README 中的联系方式

---

## 📚 相关文档

- [README.md](README.md) - 项目完整文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [CONTRIBUTING.md](CONTRIBUTING.md) - 开发指南

---

**最后更新:** 2025年11月10日
