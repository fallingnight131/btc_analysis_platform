# MySQL 管理脚本

这个目录包含用于管理 MySQL 数据库的脚本和配置文件。

## 脚本说明

### 启动/停止脚本
- `start_mysql.sh` - 启动 MySQL 服务
- `stop_mysql.sh` - 停止 MySQL 服务
- `restart_mysql.sh` - 重启 MySQL 服务
- `check_mysql.sh` - 检查 MySQL 服务状态

### 初始化脚本
- `init_mysql.sql` - 数据库初始化 SQL 脚本
- `quick_mysql_setup.sh` - 快速设置 MySQL（一键安装配置）
- `migrate_data.sh` - 数据迁移脚本（将旧数据迁移到新位置）

### 文档
- `MYSQL_SCRIPTS_GUIDE.md` - MySQL 脚本使用指南

## 使用方法

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

## 注意事项

- 这些脚本使用 Anaconda 提供的 MySQL（位于 `/opt/anaconda3/bin/`）
- 数据存储在 `backend/data/mysql`
- 日志文件位于 `/tmp/mysql.log`
