@echo off
REM 检查 MySQL 服务状态 (Windows)

echo 🔍 检查 MySQL 服务状态
echo ========================================

REM 检查 MySQL 进程
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% equ 0 (
    echo ✅ MySQL 正在运行
    echo.
    
    REM 自动检测 MySQL 客户端位置
    set "MYSQL_CLIENT="
    
    REM 检测系统 MySQL
    if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" (
        set "MYSQL_CLIENT=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    ) else if exist "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe" (
        set "MYSQL_CLIENT=C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
    ) else if exist "C:\ProgramData\Anaconda3\Library\bin\mysql.exe" (
        set "MYSQL_CLIENT=C:\ProgramData\Anaconda3\Library\bin\mysql.exe"
    ) else (
        where mysql.exe >nul 2>&1
        if %ERRORLEVEL% equ 0 (
            for /f "delims=" %%i in ('where mysql.exe') do set "MYSQL_CLIENT=%%i"
        )
    )
    
    if not "%MYSQL_CLIENT%"=="" (
        echo 🔗 测试连接...
        "%MYSQL_CLIENT%" -u root -e "SELECT VERSION();" 2>nul
        if %ERRORLEVEL% equ 0 (
            echo ✅ MySQL 连接正常
        ) else (
            echo ⚠️  MySQL 运行中，但无法连接（可能需要密码）
        )
    ) else (
        echo ⚠️  未找到 MySQL 客户端，无法测试连接
    )
) else (
    echo ❌ MySQL 未运行
    echo.
    echo 💡 启动 MySQL: start_mysql.bat
)

echo.
pause
