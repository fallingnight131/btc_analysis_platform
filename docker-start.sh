#!/bin/bash
#
# Docker 快速启动脚本
#

echo "🐳 Bitcoin Analysis Platform - Docker 启动"
echo "========================================"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装"
    echo "请先安装 Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 停止并删除旧容器
echo "🧹 清理旧容器..."
docker-compose down 2>/dev/null

# 构建并启动服务
echo "🚀 构建并启动服务..."
echo ""
docker-compose up -d --build

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 服务状态:"
docker-compose ps

# 显示访问信息
echo ""
echo "============================================"
echo "✅ 启动完成！"
echo ""
echo "🌐 访问地址:"
echo "   前端: http://localhost:8080"
echo "   后端: http://localhost:5001"
echo "   MySQL: localhost:3306"
echo ""
echo "📝 常用命令:"
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo "============================================"
