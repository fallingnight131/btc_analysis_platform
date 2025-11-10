#!/bin/bash
#
# 重启 Anaconda MySQL 服务
#

echo "🔄 重启 MySQL 服务"
echo "========================================"

# 先停止
bash "$(dirname "$0")/stop_mysql.sh"

echo ""
echo "等待 2 秒..."
sleep 2
echo ""

# 再启动
bash "$(dirname "$0")/start_mysql.sh"
