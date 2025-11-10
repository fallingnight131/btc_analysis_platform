# Data Directory

此目录用于存放所有数据库相关文件。

## 目录说明

- `mysql/` - MySQL 数据库数据文件（由 MySQL 自动管理）
- 此目录下的所有文件都已添加到 `.gitignore`，不会提交到版本控制

## 数据存储位置

- **MySQL 数据**: `backend/data/mysql/`
- **MySQL 日志**: `/tmp/mysql.log`

## 注意事项

⚠️ **重要**：此目录包含数据库文件，请勿手动修改或删除。

如需清理数据：
```bash
# 停止 MySQL
bash backend/scripts/stop_mysql.sh

# 删除数据（谨慎操作！）
rm -rf backend/data/mysql

# 重新初始化
bash backend/scripts/start_mysql.sh
```

## 备份建议

建议定期备份此目录：
```bash
# 备份数据库
tar -czf mysql_backup_$(date +%Y%m%d).tar.gz backend/data/mysql/
```
