# 🤝 Contributing to Bitcoin Analysis Platform

感谢你对比特币分析平台的关注！我们欢迎各种形式的贡献。

---

## 📋 开发环境设置

### 前置要求

- **Docker Desktop** (推荐) - 用于快速开发环境
- **Python 3.11+** - 后端开发
- **Node.js 18+** - 前端开发
- **Git** - 版本控制

---

## 🚀 本地开发

### 方式一：使用 Docker（推荐）

这是最快速的开发方式，无需手动配置数据库和依赖:

```bash
# 1. Fork 并克隆项目
git clone https://github.com/<your-username>/btc_analysis_platform.git
cd btc_analysis_platform

# 2. 启动所有服务
docker-compose up -d --build

# 3. 查看日志
docker-compose logs -f
```

**修改代码后**:
```bash
# 重建后端
docker-compose up -d --build backend

# 重建前端
docker-compose up -d --build frontend
```

---

### 方式二：本地开发环境

如果你想要更灵活的开发环境（热重载、调试等），可以使用本地开发模式:

#### 1. 启动 MySQL（使用 Docker）

```bash
# 只启动 MySQL 服务
docker-compose up -d mysql

# 验证 MySQL 运行
docker-compose ps mysql
```

或者手动安装 MySQL 8.0:
```bash
# macOS
brew install mysql@8.0
brew services start mysql@8.0

# Ubuntu/Debian
sudo apt install mysql-server
sudo systemctl start mysql

# Windows
# 下载 MySQL Installer: https://dev.mysql.com/downloads/installer/
```

#### 2. 配置数据库

```bash
# 连接 MySQL
mysql -u root -p

# 创建数据库和用户
CREATE DATABASE bitcoin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bitcoin_user'@'localhost' IDENTIFIED BY 'bitcoin123';
GRANT ALL PRIVILEGES ON bitcoin_db.* TO 'bitcoin_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3. 后端开发

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# 安装依赖
pip install -r requirements.txt

# 启动后端（开发模式，支持热重载）
export FLASK_ENV=development  # macOS/Linux
# set FLASK_ENV=development   # Windows
python app.py
```

后端将运行在: http://localhost:5001

#### 4. 前端开发

打开新终端:

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（支持热重载）
npm run serve
```

前端将运行在: http://localhost:8080

---

## 🔍 代码规范

### Python 后端

- 遵循 **PEP 8** 代码规范
- 使用 4 空格缩进
- 函数和方法添加 docstring

```python
def calculate_rsi(prices: list, period: int = 14) -> float:
    """
    计算相对强弱指标(RSI)
    
    Args:
        prices: 价格列表
        period: 计算周期（默认14天）
    
    Returns:
        RSI 值（0-100）
    """
    # 实现代码...
```

### Vue 前端

- 遵循 **Vue 3 Composition API** 风格
- 组件使用 PascalCase 命名
- 使用 2 空格缩进

```vue
<template>
  <div class="chart-card">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const data = ref([])

onMounted(() => {
  // 初始化逻辑
})
</script>
```

---

## 🧪 测试

### 后端测试

```bash
cd backend

# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_api.py

# 测试数据库连接
python tests/test_mysql_connection.py

# 查看数据库状态
python tests/check_db_status.py
```

### 前端测试

```bash
cd frontend

# 运行单元测试
npm run test:unit

# 运行 E2E 测试
npm run test:e2e

# 代码检查
npm run lint
```

---

## 📦 提交 Pull Request

### 1. 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name

# 或修复 bug
git checkout -b fix/bug-description
```

### 2. 提交更改

```bash
# 添加更改
git add .

# 提交（使用清晰的提交信息）
git commit -m "feat: 添加 XXX 功能"
# 或
git commit -m "fix: 修复 XXX 问题"
```

**提交信息规范**:
- `feat:` - 新功能
- `fix:` - 修复 bug
- `docs:` - 文档更新
- `style:` - 代码格式调整（不影响功能）
- `refactor:` - 代码重构
- `test:` - 添加测试
- `chore:` - 构建/工具链更改

### 3. 推送分支

```bash
git push origin feature/your-feature-name
```

### 4. 创建 Pull Request

1. 访问你 Fork 的仓库页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述:
   - **标题**: 简洁描述你的更改
   - **描述**: 详细说明你做了什么、为什么这样做
   - **相关 Issue**: 如果有，链接相关的 Issue

**PR 模板**:
```markdown
## 更改描述
简要描述你的更改内容

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 性能优化
- [ ] 代码重构

## 测试
- [ ] 已在本地测试
- [ ] 已添加/更新测试用例

## 截图（如有UI更改）
粘贴截图

## 相关 Issue
Closes #123
```

---

## 🐛 报告 Bug

如果你发现了 bug，请创建一个 Issue:

1. 使用清晰的标题描述问题
2. 提供复现步骤
3. 说明预期行为 vs 实际行为
4. 提供环境信息（OS、Docker 版本等）
5. 如果可能，提供错误日志

**Bug Report 模板**:
```markdown
## Bug 描述
简要描述 bug

## 复现步骤
1. 打开应用
2. 点击 XXX
3. 观察到 XXX 错误

## 预期行为
应该显示 XXX

## 实际行为
显示了 XXX

## 环境信息
- OS: macOS 13.0
- Docker 版本: 24.0.5
- 浏览器: Chrome 118

## 日志
```
粘贴相关日志
```
```

---

## 💡 功能建议

欢迎提出新功能建议！创建一个 Issue:

1. 使用 "Feature Request" 标签
2. 清晰描述你希望添加的功能
3. 说明为什么需要这个功能
4. 如果可能，提供实现思路

---

## 🏗 项目架构

### 后端架构

```
backend/
├── app.py              # Flask 应用入口
├── routes.py           # API 路由定义
├── api.py              # CoinGecko API 封装
├── database.py         # MySQL 数据库操作
├── cache.py            # 缓存管理（30分钟TTL）
└── utils.py            # 工具函数（RSI、MACD等）
```

**关键组件**:
- `CoinGeckoAPI`: API 调用 + 限流处理
- `DatabaseManager`: 数据库 CRUD + 365天保留策略
- `CacheManager`: 内存缓存 + 过期清理

### 前端架构

```
frontend/src/
├── views/              # 页面组件
│   ├── Dashboard.vue   # 仪表盘
│   ├── Analysis.vue    # 技术分析
│   └── History.vue     # 历史数据
├── components/         # 可复用组件
│   ├── charts/         # 图表组件
│   └── StatCards.vue   # 统计卡片
└── router/             # Vue Router 配置
```

**技术选型**:
- Vue 3 Composition API
- ECharts 数据可视化
- Bootstrap 5 UI 框架

---

## 📚 开发资源

### API 文档

- [CoinGecko API](https://www.coingecko.com/en/api/documentation)
- [Flask 文档](https://flask.palletsprojects.com/)
- [Vue 3 文档](https://vuejs.org/)
- [ECharts 文档](https://echarts.apache.org/)

### 相关技术

- **技术指标**: RSI、MACD、布林带算法实现
- **机器学习**: Scikit-learn 随机森林价格预测
- **数据库**: MySQL 8.0 + 365天数据保留策略

---

## 🎯 开发路线图

当前规划的功能（欢迎认领）:

- [ ] 添加更多技术指标（KDJ、威廉指标等）
- [ ] 支持多种加密货币（ETH、BNB等）
- [ ] 实现用户账户系统
- [ ] 添加实时价格推送（WebSocket）
- [ ] 移动端适配优化
- [ ] 数据导出功能（CSV/Excel）

---

## ❓ 获取帮助

如果你在开发过程中遇到问题:

1. 查看 [常见问题](README.md#-常见问题)
2. 搜索现有的 [Issues](https://github.com/fallingnight131/btc_analysis_platform/issues)
3. 创建新 Issue 提问
4. 在 Discussions 中讨论

---

## 📜 行为准则

请遵守以下准则:

- 尊重所有贡献者
- 接受建设性批评
- 关注项目目标
- 保持友好和包容

---

**再次感谢你的贡献！🎉**
