#!/bin/bash
#
# 检查 Anaconda MySQL 服务状态
#

echo "🔍 MySQL 服务状态检查"
echo "========================================"

MYSQL_PID_FILE="/tmp/mysql.pid"
MYSQL_LOG="/tmp/mysql.log"

# 检查 PID 文件
if [ -f "$MYSQL_PID_FILE" ]; then
    PID=$(cat "$MYSQL_PID_FILE")
    echo "PID 文件: $MYSQL_PID_FILE"
    echo "进程 ID: $PID"
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "状态: ✅ 运行中"
        
        # 检查端口
        PORT_CHECK=$(lsof -i :3306 2>/dev/null | grep LISTEN)
        if [ -n "$PORT_CHECK" ]; then
            echo "端口 3306: ✅ 监听中"
        else
            echo "端口 3306: ⚠️  未监听"
        fi
        
        # 检查 socket
        if [ -S "/tmp/mysql.sock" ]; then
            echo "Socket: ✅ /tmp/mysql.sock"
        else
            echo "Socket: ⚠️  未找到"
        fi
    else
        echo "状态: ❌ 进程不存在"
        echo "⚠️  PID 文件存在但进程不存在，可能需要清理"
    fi
else
    echo "状态: ❌ 未运行"
    
    # 检查是否有其他 MySQL 进程
    MYSQL_PROC=$(ps aux | grep mysqld | grep -v grep)
    if [ -n "$MYSQL_PROC" ]; then
        echo "⚠️  发现其他 MySQL 进程:"
        echo "$MYSQL_PROC"
    fi
fi

echo ""
echo "📋 日志文件: $MYSQL_LOG"
if [ -f "$MYSQL_LOG" ]; then
    echo "最后 10 行:"
    tail -n 10 "$MYSQL_LOG"
else
    echo "⚠️  日志文件不存在"
fi

echo ""
echo "🔌 网络连接测试:"
/opt/anaconda3/bin/mysql -u root -e "SELECT 'MySQL 连接成功!' as status;" 2>&1
