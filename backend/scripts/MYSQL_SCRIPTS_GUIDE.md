# MySQL 服务管理脚本使用指南

## 📁 脚本说明

已为您创建了 4 个 MySQL 管理脚本:

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `start_mysql.sh` | 启动 MySQL 服务 | 首次启动或停止后重新启动 |
| `stop_mysql.sh` | 停止 MySQL 服务 | 需要关闭 MySQL 时 |
| `restart_mysql.sh` | 重启 MySQL 服务 | 修改配置后或出现问题时 |
| `check_mysql.sh` | 检查 MySQL 状态 | 排查问题、查看运行状态 |

---

## 🚀 快速开始

### 1️⃣ 启动 MySQL 服务

```bash
cd /Users/fallingnight/代码/Python/2025_10/btc_analysis_platform/backend
bash start_mysql.sh
```

**首次启动会自动:**
- 创建数据目录 `~/mysql_data`
- 初始化数据库
- 启动 mysqld 守护进程
- 监听在 `localhost:3306`
- 生成日志文件 `/tmp/mysql.log`

**输出示例:**
```
🚀 启动 Anaconda MySQL 服务
========================================
数据目录: /Users/fallingnight/mysql_data
✅ MySQL 正在启动...
⏳ 等待 MySQL 启动...
✅ MySQL 已成功启动!
```

---

### 2️⃣ 检查服务状态

```bash
bash check_mysql.sh
```

**会显示:**
- ✅ 进程运行状态
- 🔌 端口监听情况 (3306)
- 📂 Socket 文件状态
- 📋 日志文件最后 10 行
- 🔗 连接测试结果

---

### 3️⃣ 停止 MySQL 服务

```bash
bash stop_mysql.sh
```

**会自动:**
- 读取 PID 文件
- 优雅关闭进程
- 清理 PID 和 Socket 文件

---

### 4️⃣ 重启 MySQL 服务

```bash
bash restart_mysql.sh
```

等同于 `stop_mysql.sh` + `start_mysql.sh`

---

## 🔧 首次启动后的配置

### 设置 root 密码

首次启动后,root 用户**没有密码**,需要立即设置:

```bash
# 1. 连接到 MySQL
/opt/anaconda3/bin/mysql -u root

# 2. 设置密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
exit;
```

**推荐密码:** `bitcoin123` (与迁移脚本默认一致)

---

### 创建数据库和用户

```bash
# 连接到 MySQL
/opt/anaconda3/bin/mysql -u root -p

# 执行以下 SQL
CREATE DATABASE bitcoin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';

GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';

FLUSH PRIVILEGES;

exit;
```

---

## 📊 验证安装

### 方法 1: 使用 Python 测试脚本

```bash
cd backend
python test_mysql_connection.py
```

**成功输出:**
```
✅ MySQL 连接成功!
服务器版本: 5.7.24-log
```

---

### 方法 2: 使用 mysql 命令行

```bash
/opt/anaconda3/bin/mysql -u root -p -e "SELECT VERSION();"
```

---

## 🔄 数据迁移

设置好 MySQL 后,运行自动迁移脚本:

```bash
cd backend
python migrate_to_mysql_auto.py
```

**步骤:**
1. 选择 `1` (使用真实 MySQL)
2. 输入密码 `bitcoin123`
3. 等待迁移完成 (4385 条记录)

---

## 🐛 常见问题

### 1. 启动失败 - 端口被占用

**错误信息:** `bind on TCP/IP port: Address already in use`

**解决方法:**
```bash
# 查找占用 3306 端口的进程
lsof -i :3306

# 停止进程
bash stop_mysql.sh
```

---

### 2. 启动失败 - 权限问题

**错误信息:** `Can't create/write to file`

**解决方法:**
```bash
# 检查数据目录权限
ls -la ~/mysql_data

# 修复权限
chmod -R 755 ~/mysql_data
```

---

### 3. 无法连接 - Connection refused

**解决方法:**
```bash
# 1. 检查服务状态
bash check_mysql.sh

# 2. 查看日志
tail -n 50 /tmp/mysql.log

# 3. 重启服务
bash restart_mysql.sh
```

---

### 4. 忘记 root 密码

**解决方法:**
```bash
# 1. 停止 MySQL
bash stop_mysql.sh

# 2. 以安全模式启动 (已在 start_mysql.sh 中配置)
bash start_mysql.sh

# 3. 无密码连接并重置
/opt/anaconda3/bin/mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;

# 4. 重启 MySQL
bash restart_mysql.sh
```

---

## 📂 重要文件位置

| 文件/目录 | 路径 | 说明 |
|----------|------|------|
| 数据目录 | `~/mysql_data` | 存储所有数据库文件 |
| 日志文件 | `/tmp/mysql.log` | MySQL 运行日志 |
| PID 文件 | `/tmp/mysql.pid` | 进程 ID 文件 |
| Socket 文件 | `/tmp/mysql.sock` | 本地连接 socket |
| MySQL 可执行文件 | `/opt/anaconda3/bin/mysql` | 客户端工具 |
| mysqld 守护进程 | `/opt/anaconda3/bin/mysqld` | 服务器程序 |

---

## 🎯 下一步操作

完成 MySQL 启动后,按以下顺序操作:

1. ✅ **启动服务:** `bash start_mysql.sh`
2. 🔑 **设置密码:** 运行上述 `ALTER USER` 命令
3. 🗄️ **创建数据库:** 创建 `bitcoin_db` 和 `bitcoin_user`
4. 🔄 **迁移数据:** 运行 `python migrate_to_mysql_auto.py`
5. ⚙️ **更新配置:** 设置环境变量或修改 `database.py`
6. 🚀 **重启后端:** `python app.py`

---

## 💡 提示

- **开机自启动:** macOS 不建议设置自启动,按需启动即可
- **性能优化:** 5.7.24 版本适合开发和学习
- **备份:** 定期备份 `~/mysql_data` 目录
- **安全:** 生产环境请使用更强的密码

---

## 📞 获取帮助

如果遇到问题,可以:
1. 查看日志: `tail -f /tmp/mysql.log`
2. 检查状态: `bash check_mysql.sh`
3. 重启服务: `bash restart_mysql.sh`

祝使用愉快! 🎉
