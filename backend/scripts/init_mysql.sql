-- MySQL 数据库初始化脚本
-- 在首次启动 MySQL 后运行此脚本

-- 1. 设置 root 密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'bitcoin123';
FLUSH PRIVILEGES;

-- 2. 创建数据库
CREATE DATABASE IF NOT EXISTS bitcoin_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 3. 创建用户
CREATE USER IF NOT EXISTS 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';

-- 4. 授予权限
GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';
FLUSH PRIVILEGES;

-- 5. 验证
USE bitcoin_db;
SHOW TABLES;
SELECT USER();
