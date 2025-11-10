@echo off
REM 重启 MySQL 服务 (Windows)

echo 🔄 重启 MySQL 服务
echo ========================================

echo 1️⃣ 停止 MySQL...
call "%~dp0stop_mysql.bat"

echo.
echo 2️⃣ 启动 MySQL...
call "%~dp0start_mysql.bat"
