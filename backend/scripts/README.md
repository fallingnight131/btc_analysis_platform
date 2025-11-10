# MySQL 管理脚本

这个目录包含用于管理 MySQL 数据库的脚本和配置文件。

## 脚本说明

### 启动/停止脚本

**macOS/Linux:**
- `start_mysql.sh` - 启动 MySQL 服务
- `stop_mysql.sh` - 停止 MySQL 服务
- `restart_mysql.sh` - 重启 MySQL 服务
- `check_mysql.sh` - 检查 MySQL 服务状态

**Windows:**
- `start_mysql.bat` - 启动 MySQL 服务
- `stop_mysql.bat` - 停止 MySQL 服务
- `restart_mysql.bat` - 重启 MySQL 服务
- `check_mysql.bat` - 检查 MySQL 服务状态

### 初始化脚本
- `init_mysql.sql` - 数据库初始化 SQL 脚本
- `quick_mysql_setup.sh` - 快速设置 MySQL（一键安装配置）
- `migrate_data.sh` - 数据迁移脚本（将旧数据迁移到新位置）

### 文档
- `MYSQL_SCRIPTS_GUIDE.md` - MySQL 脚本使用指南

## 使用方法

**macOS/Linux:**
```bash
# 从 backend 目录运行
cd backend

# 启动 MySQL
bash scripts/start_mysql.sh

# 检查状态
bash scripts/check_mysql.sh

# 停止 MySQL
bash scripts/stop_mysql.sh
```

**Windows:**
```cmd
REM 从 backend 目录运行
cd backend

REM 启动 MySQL
scripts\start_mysql.bat

REM 检查状态
scripts\check_mysql.bat

REM 停止 MySQL
scripts\stop_mysql.bat
```

## 注意事项

- **macOS/Linux**: 脚本使用 Anaconda 提供的 MySQL（位于 `/opt/anaconda3/bin/`）
- **Windows**: 脚本会自动检测 MySQL 安装位置
  - 优先检测系统 MySQL (`C:\Program Files\MySQL\`)
  - 其次检测 Anaconda MySQL (`C:\ProgramData\Anaconda3\Library\bin\`)
  - 最后检测 PATH 环境变量中的 MySQL
- 数据存储在 `backend/data/mysql`
- 日志文件位于 `/tmp/mysql.log` (macOS/Linux) 或 `%TEMP%\mysql.log` (Windows)
