@echo off
REM 停止 MySQL 服务 (Windows)

echo 🛑 停止 MySQL 服务
echo ========================================

REM 查找 MySQL 进程
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% neq 0 (
    echo ℹ️  MySQL 未运行
    pause
    exit /b 0
)

REM 停止 MySQL
echo 停止 MySQL 进程...
taskkill /F /IM mysqld.exe >nul 2>&1

REM 等待进程结束
timeout /t 2 /nobreak >nul

REM 验证是否停止
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if %ERRORLEVEL% neq 0 (
    echo ✅ MySQL 已停止
) else (
    echo ⚠️  MySQL 可能未完全停止
    echo 请手动检查任务管理器
)

REM 清理临时文件
if exist "%TEMP%\mysql.sock" del /F /Q "%TEMP%\mysql.sock" >nul 2>&1
if exist "%TEMP%\mysql.pid" del /F /Q "%TEMP%\mysql.pid" >nul 2>&1

echo 🧹 清理完成
echo.
pause
