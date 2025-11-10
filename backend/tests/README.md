# 测试脚本

这个目录包含用于测试和调试的脚本。

## 测试脚本说明

- `test_mysql_connection.py` - 测试 MySQL 数据库连接
- `test_offline.py` - 测试离线模式功能
- `check_db_status.py` - 检查数据库状态和数据量

## 使用方法

### 检查数据库状态

```bash
# 从 backend 目录（推荐）
cd backend
python tests/check_db_status.py

# 或从项目根目录
python backend/tests/check_db_status.py
```

这会显示：
- 数据库记录总数
- 最新数据时间
- 各时间段的数据分布
- 数据保留策略检查

### 测试 MySQL 连接

```bash
cd backend
python tests/test_mysql_connection.py
```

### 测试离线模式

```bash
cd backend
python tests/test_offline.py
```

## 快速查询命令

```bash
# 查询总记录数
python -c "from database import db_manager; print(db_manager.get_data_count())"

# 查询最新数据时间
python -c "from database import db_manager; print(db_manager.get_latest_data_time())"
```
