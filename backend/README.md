# Backend - Bitcoin Analysis Platform

比特币分析平台后端服务，基于 Flask 框架，提供 RESTful API 接口。

## 📁 目录结构

```
backend/
├── app.py              # Flask 应用入口（启动文件）
├── routes.py           # API 路由定义
├── api.py              # Bitcoin API 数据获取
├── cache.py            # 缓存管理
├── database.py         # MySQL 数据库管理
├── utils.py            # 工具函数（技术指标计算等）
├── requirements.txt    # Python 依赖包
├── data/               # 数据库数据文件目录
│   └── mysql/              # MySQL 数据文件（自动生成）
├── scripts/            # MySQL 管理脚本
│   ├── start_mysql.sh      # 启动 MySQL
│   ├── stop_mysql.sh       # 停止 MySQL
│   ├── check_mysql.sh      # 检查状态
│   └── init_mysql.sql      # 初始化数据库
└── tests/              # 测试和调试脚本
    ├── check_db_status.py      # 数据库状态检查
    ├── test_mysql_connection.py # MySQL 连接测试
    └── test_offline.py         # 离线模式测试
```

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 MySQL

```bash
bash scripts/start_mysql.sh
```

### 3. 启动后端服务

```bash
python app.py
```

后端将在 `http://localhost:5001` 启动。

## 📊 数据库管理

### 查看数据库状态

```bash
python tests/check_db_status.py
```

### MySQL 管理

```bash
# 检查 MySQL 状态
bash scripts/check_mysql.sh

# 重启 MySQL
bash scripts/restart_mysql.sh

# 停止 MySQL
bash scripts/stop_mysql.sh
```

## 🔧 核心模块说明

### app.py
Flask 应用入口，配置 CORS、注册路由、启动服务。

### routes.py
定义所有 API 路由端点：
- `/api/realtime` - 实时数据
- `/api/historical` - 历史数据
- `/api/statistics` - 统计数据
- `/api/prediction` - 价格预测
- `/api/risk-alerts` - 风险警报
- `/api/candlestick` - K线数据

### api.py
CoinGecko API 数据获取，包含：
- 网络状态检测
- API 请求限流
- 多层数据回退（API → 数据库 → 缓存）

### database.py
MySQL 数据库管理：
- 数据保留策略：最多保留最近 365 天
- 自动清理过期数据
- 支持离线模式（无网络时使用历史数据）

### cache.py
内存缓存管理：
- 减少 API 调用频率
- 提高响应速度
- 降低 API 限流风险

### utils.py
工具函数集合：
- 技术指标计算（MA、RSI、MACD、布林带等）
- 特征工程
- 风险评估

## 📝 开发注意事项

1. **数据库保留策略**：数据库只保留最近 365 天的数据，超过一年的数据需要实时从 API 获取
2. **API 限流**：CoinGecko 免费 API 有频率限制，建议合理使用缓存
3. **离线模式**：当 API 不可用时，系统会自动降级到数据库数据
4. **缓存策略**：不同数据类型有不同的缓存时间（详见 `routes.py`）

## 🧪 测试

```bash
# 测试数据库连接
python tests/test_mysql_connection.py

# 测试离线模式
python tests/test_offline.py

# 查看数据库状态
python tests/check_db_status.py
```

## 📚 更多信息

- MySQL 脚本使用：参见 `scripts/README.md`
- 测试脚本说明：参见 `tests/README.md`
