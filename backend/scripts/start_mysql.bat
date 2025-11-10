@echo off
setlocal enabledelayedexpansion
REM 启动 Anaconda MySQL 服务 (Windows)

echo 🐬 启动 Anaconda MySQL 服务
echo ========================================

REM 获取脚本所在目录的父目录（backend）
set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%.."
set "DATA_DIR=%BACKEND_DIR%\data"

REM MySQL 相关路径
set "MYSQL_DATA_DIR=%DATA_DIR%\mysql"

REM 1. 自动检测 MySQL 安装位置
set "MYSQL_BIN="

REM 检测系统 MySQL（最常见）
if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" (
    set "MYSQL_BIN=C:\Program Files\MySQL\MySQL Server 8.0\bin"
    echo ✅ 检测到 MySQL Server 8.0
)
if exist "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld.exe" (
    set "MYSQL_BIN=C:\Program Files\MySQL\MySQL Server 5.7\bin"
    echo ✅ 检测到 MySQL Server 5.7
)

REM 检测 Anaconda MySQL
if "%MYSQL_BIN%"=="" (
    if exist "C:\ProgramData\Anaconda3\Library\bin\mysqld.exe" (
        set "MYSQL_BIN=C:\ProgramData\Anaconda3\Library\bin"
        echo ✅ 检测到 Anaconda MySQL
    )
)

REM 检测 PATH 中的 MySQL
if "%MYSQL_BIN%"=="" (
    where mysqld.exe >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        for /f "delims=" %%i in ('where mysqld.exe') do set "MYSQL_BIN=%%~dpi"
        set "MYSQL_BIN=!MYSQL_BIN:~0,-1!"
        echo ✅ 检测到 PATH 中的 MySQL
    )
)

REM 如果都没找到，提示用户
if "%MYSQL_BIN%"=="" (
    echo ❌ 未找到 MySQL 安装
    echo.
    echo 💡 请先安装 MySQL:
    echo    1. 下载 MySQL Installer: https://dev.mysql.com/downloads/installer/
    echo    2. 或使用 Chocolatey: choco install mysql
    echo    3. 或手动指定 MySQL 路径（编辑此脚本）
    pause
    exit /b 1
)

echo 📁 使用 MySQL: %MYSQL_BIN%
echo.

REM 2. 创建数据目录
if not exist "%MYSQL_DATA_DIR%" (
    echo 📁 创建 MySQL 数据目录: %MYSQL_DATA_DIR%
    mkdir "%MYSQL_DATA_DIR%"
    
    echo 🔧 初始化 MySQL 数据库...
    "%MYSQL_BIN%\mysqld.exe" --initialize-insecure --datadir="%MYSQL_DATA_DIR%"
    
    if %ERRORLEVEL% equ 0 (
        echo ✅ 数据库初始化成功
    ) else (
        echo ❌ 数据库初始化失败
        pause
        exit /b 1
    )
)

REM 3. 检查是否已经运行
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% equ 0 (
    echo ⚠️  MySQL 已经在运行
    echo.
    echo 💡 如需重启，请先运行: stop_mysql.bat
    pause
    exit /b 0
)

REM 4. 启动 MySQL
echo 🚀 启动 MySQL 服务...
start "MySQL Server" /B "%MYSQL_BIN%\mysqld.exe" --datadir="%MYSQL_DATA_DIR%" --port=3306 --bind-address=127.0.0.1

REM 5. 等待启动
echo ⏳ 等待 MySQL 启动...
timeout /t 5 /nobreak >nul

REM 6. 检查是否成功
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% equ 0 (
    echo ✅ MySQL 启动成功
    echo.
    echo 📊 MySQL 信息:
    echo    数据目录: %MYSQL_DATA_DIR%
    echo    端口: 3306
    echo.
    echo 🔑 首次启动无密码，请立即设置:
    echo    "%MYSQL_BIN%\mysql.exe" -u root
    echo    然后执行:
    echo    ALTER USER 'root'@'localhost' IDENTIFIED BY 'bitcoin123';
    echo    CREATE DATABASE IF NOT EXISTS bitcoin_db;
    echo    CREATE USER IF NOT EXISTS 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';
    echo    GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';
    echo    FLUSH PRIVILEGES;
    echo    EXIT;
    echo.
    echo 💡 下一步: python tests\test_mysql_connection.py
) else (
    echo ❌ MySQL 启动失败
    echo 请检查日志或手动启动
)

echo.
pause
