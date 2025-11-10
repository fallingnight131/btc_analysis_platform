#!/bin/bash
#
# 停止 Anaconda MySQL 服务
#

echo "🛑 停止 MySQL 服务"
echo "========================================"

MYSQL_PID_FILE="/tmp/mysql.pid"

if [ -f "$MYSQL_PID_FILE" ]; then
    PID=$(cat "$MYSQL_PID_FILE")
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "停止 MySQL 进程 (PID: $PID)..."
        kill $PID
        
        # 等待进程结束
        sleep 2
        
        if ps -p $PID > /dev/null 2>&1; then
            echo "强制停止..."
            kill -9 $PID
        fi
        
        rm -f "$MYSQL_PID_FILE"
        echo "✅ MySQL 已停止"
    else
        echo "⚠️  进程不存在，清理 PID 文件"
        rm -f "$MYSQL_PID_FILE"
    fi
else
    echo "⚠️  MySQL 未运行（未找到 PID 文件）"
fi

# 清理 socket 文件
rm -f /tmp/mysql.sock
echo "🧹 清理完成"
