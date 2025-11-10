#!/bin/bash
#
# 启动 Anaconda MySQL 服务
#

echo "🐬 启动 Anaconda MySQL 服务"
echo "========================================"

# 获取脚本所在目录的父目录（backend）
BACKEND_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$BACKEND_DIR/data"

# MySQL 相关路径
MYSQL_BIN="/opt/anaconda3/bin"
MYSQL_DATA_DIR="$DATA_DIR/mysql"
MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_PID_FILE="/tmp/mysql.pid"

# 1. 创建数据目录
if [ ! -d "$MYSQL_DATA_DIR" ]; then
    echo "📁 创建 MySQL 数据目录: $MYSQL_DATA_DIR"
    mkdir -p "$MYSQL_DATA_DIR"
    
    echo "🔧 初始化 MySQL 数据库..."
    $MYSQL_BIN/mysqld --initialize-insecure --user=$USER --datadir="$MYSQL_DATA_DIR"
    
    if [ $? -eq 0 ]; then
        echo "✅ 数据库初始化成功"
    else
        echo "❌ 数据库初始化失败"
        exit 1
    fi
fi

# 2. 检查是否已经运行
if [ -f "$MYSQL_PID_FILE" ]; then
    PID=$(cat "$MYSQL_PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  MySQL 已经在运行 (PID: $PID)"
        echo ""
        echo "💡 如需重启，请先运行: bash stop_mysql.sh"
        exit 0
    else
        echo "🧹 清理旧的 PID 文件"
        rm -f "$MYSQL_PID_FILE"
    fi
fi

# 3. 启动 MySQL
echo "🚀 启动 MySQL 服务..."
$MYSQL_BIN/mysqld \
    --datadir="$MYSQL_DATA_DIR" \
    --socket="$MYSQL_SOCKET" \
    --pid-file="$MYSQL_PID_FILE" \
    --port=3306 \
    --bind-address=127.0.0.1 \
    > /tmp/mysql.log 2>&1 &

# 4. 等待启动
echo "⏳ 等待 MySQL 启动..."
sleep 5

# 5. 检查是否成功
if [ -f "$MYSQL_PID_FILE" ]; then
    PID=$(cat "$MYSQL_PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ MySQL 启动成功 (PID: $PID)"
        echo ""
        echo "📊 MySQL 信息:"
        echo "   数据目录: $MYSQL_DATA_DIR"
        echo "   Socket: $MYSQL_SOCKET"
        echo "   端口: 3306"
        echo "   日志: /tmp/mysql.log"
        echo ""
        echo "🔑 首次启动无密码，请立即设置:"
        echo "   $MYSQL_BIN/mysql -u root"
        echo "   然后执行:"
        echo "   ALTER USER 'root'@'localhost' IDENTIFIED BY 'bitcoin123';"
        echo "   FLUSH PRIVILEGES;"
        echo ""
        echo "💡 下一步: python test_mysql_connection.py"
    else
        echo "❌ MySQL 启动失败"
        echo "查看日志: cat /tmp/mysql.log"
        exit 1
    fi
else
    echo "❌ MySQL 启动失败（未找到 PID 文件）"
    echo "查看日志: cat /tmp/mysql.log"
    exit 1
fi
