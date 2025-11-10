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

# 检查镜像是否存在
BACKEND_IMAGE=$(docker images -q btc_analysis_platform-backend 2>/dev/null)
FRONTEND_IMAGE=$(docker images -q btc_analysis_platform-frontend 2>/dev/null)

if [ -z "$BACKEND_IMAGE" ] || [ -z "$FRONTEND_IMAGE" ]; then
    echo "📦 首次运行，需要构建镜像（约 3-5 分钟）..."
    BUILD_FLAG="--build"
else
    echo "📦 检测到已有镜像，快速启动（约 10 秒）..."
    echo "💡 提示: 如需重新构建，请运行: docker compose up -d --build"
    BUILD_FLAG=""
fi

# 停止旧容器（但保留镜像）
echo "🧹 清理旧容器..."
docker-compose down 2>/dev/null

# 启动服务
echo "🚀 启动服务..."
echo ""
docker-compose up -d $BUILD_FLAG

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
