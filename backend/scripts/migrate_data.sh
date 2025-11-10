#!/bin/bash
#
# 迁移 MySQL 数据到新的 data 目录
#

echo "📦 迁移 MySQL 数据到新位置"
echo "========================================"

# 获取脚本所在目录的父目录（backend）
BACKEND_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NEW_DATA_DIR="$BACKEND_DIR/data/mysql"
OLD_DATA_DIR="$HOME/mysql_data"

# 检查是否需要迁移
if [ ! -d "$OLD_DATA_DIR" ]; then
    echo "ℹ️  未找到旧数据目录: $OLD_DATA_DIR"
    echo "   无需迁移。"
    exit 0
fi

if [ -d "$NEW_DATA_DIR" ]; then
    echo "⚠️  新数据目录已存在: $NEW_DATA_DIR"
    read -p "是否要覆盖？这将删除现有数据！(yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ 取消迁移"
        exit 1
    fi
    rm -rf "$NEW_DATA_DIR"
fi

# 检查 MySQL 是否在运行
if [ -f "/tmp/mysql.pid" ]; then
    PID=$(cat "/tmp/mysql.pid")
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  MySQL 正在运行，需要先停止"
        echo "   运行: bash scripts/stop_mysql.sh"
        exit 1
    fi
fi

# 创建父目录
mkdir -p "$BACKEND_DIR/data"

# 迁移数据
echo "📁 从: $OLD_DATA_DIR"
echo "📁 到:   $NEW_DATA_DIR"
echo ""
echo "🚀 开始迁移..."

cp -r "$OLD_DATA_DIR" "$NEW_DATA_DIR"

if [ $? -eq 0 ]; then
    echo "✅ 数据迁移成功！"
    echo ""
    echo "📊 新数据目录: $NEW_DATA_DIR"
    echo "💾 数据大小: $(du -sh "$NEW_DATA_DIR" | cut -f1)"
    echo ""
    echo "🔄 下一步:"
    echo "   1. 启动 MySQL: bash scripts/start_mysql.sh"
    echo "   2. 验证数据: python tests/check_db_status.py"
    echo ""
    echo "🗑️  旧数据保留在: $OLD_DATA_DIR"
    echo "   验证无误后可手动删除: rm -rf $OLD_DATA_DIR"
else
    echo "❌ 迁移失败"
    exit 1
fi
