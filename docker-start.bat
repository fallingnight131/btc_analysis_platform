@echo off
REM Docker 快速启动脚本 (Windows)

echo 🐳 Bitcoin Analysis Platform - Docker 启动
echo ========================================

REM 检查 Docker 是否安装
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker 未安装
    echo 请先安装 Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM 检查 Docker 是否运行
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker 未运行
    echo 请启动 Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker 环境检查通过
echo.

REM 检查镜像是否存在
docker images btc_analysis_platform-backend >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo 📦 检测到已有镜像，快速启动（约 10 秒）...
    echo 💡 提示: 如需重新构建，请运行: docker-compose up -d --build
    set BUILD_FLAG=
) else (
    echo 📦 首次运行，需要构建镜像（约 3-5 分钟）...
    set BUILD_FLAG=--build
)

REM 停止旧容器（但保留镜像）
echo 🧹 清理旧容器...
docker-compose down 2>nul

REM 启动服务
echo 🚀 启动服务...
echo.
docker-compose up -d %BUILD_FLAG%

REM 等待服务启动
echo.
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

REM 检查服务状态
echo.
echo 📊 服务状态:
docker-compose ps

REM 显示访问信息
echo.
echo ============================================
echo ✅ 启动完成！
echo.
echo 🌐 访问地址:
echo    前端: http://localhost:8080
echo    后端: http://localhost:5001
echo    MySQL: localhost:3306
echo.
echo 📝 常用命令:
echo    查看日志: docker-compose logs -f
echo    停止服务: docker-compose down
echo    重启服务: docker-compose restart
echo ============================================
echo.
pause
