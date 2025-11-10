@echo off
REM 检查 MySQL 服务状态 (Windows)

echo 🔍 检查 MySQL 服务状态
echo ========================================

REM 检查 MySQL 进程
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% equ 0 (
    echo ✅ MySQL 正在运行
    echo.
    
    REM 尝试连接测试
    set "MYSQL_BIN=C:\ProgramData\Anaconda3\Library\bin"
    if exist "%MYSQL_BIN%\mysql.exe" (
        echo 🔗 测试连接...
        "%MYSQL_BIN%\mysql.exe" -u root -e "SELECT VERSION();" 2>nul
        if %ERRORLEVEL% equ 0 (
            echo ✅ MySQL 连接正常
        ) else (
            echo ⚠️  MySQL 运行中，但无法连接（可能需要密码）
        )
    )
) else (
    echo ❌ MySQL 未运行
    echo.
    echo 💡 启动 MySQL: start_mysql.bat
)

echo.
pause
