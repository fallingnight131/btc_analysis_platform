#!/bin/bash
#
# MySQL 快速迁移脚本
# 使用方法: bash quick_mysql_setup.sh

echo "🐬 MySQL 快速迁移工具"
echo "======================="
echo ""

# 1. 检查 MySQL 命令
if command -v mysql &> /dev/null; then
    MYSQL_CMD="mysql"
elif [ -f "/opt/anaconda3/bin/mysql" ]; then
    MYSQL_CMD="/opt/anaconda3/bin/mysql"
else
    echo "❌ 找不到 MySQL 命令"
    echo "   请先安装 MySQL: brew install mysql"
    exit 1
fi

echo "✅ 找到 MySQL: $MYSQL_CMD"
$MYSQL_CMD --version
echo ""

# 2. 提示用户输入密码
echo "请输入 MySQL root 密码（如果是首次运行，直接回车）："
read -s MYSQL_PASSWORD
echo ""

# 3. 测试连接
echo "🔗 测试 MySQL 连接..."
if [ -z "$MYSQL_PASSWORD" ]; then
    # 无密码连接
    $MYSQL_CMD -u root -e "SELECT 1;" &> /dev/null
    CONNECTION_STATUS=$?
else
    # 有密码连接
    $MYSQL_CMD -u root -p"$MYSQL_PASSWORD" -e "SELECT 1;" &> /dev/null
    CONNECTION_STATUS=$?
fi

if [ $CONNECTION_STATUS -ne 0 ]; then
    echo "❌ MySQL 连接失败"
    echo ""
    echo "💡 可能的原因："
    echo "   1. MySQL 服务未启动"
    echo "   2. 密码不正确"
    echo "   3. root 用户不存在"
    echo ""
    echo "🔧 解决方案："
    echo "   macOS: brew services start mysql"
    echo "   Linux: sudo systemctl start mysql"
    exit 1
fi

echo "✅ MySQL 连接成功"
echo ""

# 4. 创建数据库
echo "📊 创建数据库 bitcoin_db..."
if [ -z "$MYSQL_PASSWORD" ]; then
    $MYSQL_CMD -u root -e "CREATE DATABASE IF NOT EXISTS bitcoin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
else
    $MYSQL_CMD -u root -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS bitcoin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
fi

echo "✅ 数据库创建成功"
echo ""

# 5. 创建 .env 配置文件
echo "⚙️ 创建 MySQL 配置文件..."
cat > .env << EOF
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=$MYSQL_PASSWORD
MYSQL_DATABASE=bitcoin_db
EOF

echo "✅ 配置文件创建成功: .env"
echo ""

# 6. 运行 Python 迁移脚本
echo "🔄 开始数据迁移..."
echo ""

# 设置环境变量
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD="$MYSQL_PASSWORD"
export MYSQL_DATABASE=bitcoin_db

# 运行迁移
/opt/anaconda3/envs/btc_analysis_platform/bin/python migrate_to_mysql.py

echo ""
echo "✅ 迁移完成！"
echo ""
echo "📝 下一步："
echo "   1. 备份 SQLite 文件: mv bitcoin_data.db bitcoin_data.db.backup"
echo "   2. 修改 database.py 导入 MySQL 模块"
echo "   3. 重启后端服务: python app.py"
echo ""
