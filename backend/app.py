"""
Bitcoin Analysis Platform - 主应用
重构后的精简版
"""
from flask import Flask
from flask_cors import CORS
import atexit

from routes import register_routes
from database import db_manager
from cache import cache_manager
from scheduler import init_scheduler, get_scheduler


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    CORS(app)
    
    # 注册所有路由
    register_routes(app)
    
    # 初始化定时任务调度器
    init_scheduler(db_manager, cache_manager)
    
    # 注册清理函数，确保应用关闭时停止调度器
    @atexit.register
    def shutdown_scheduler():
        scheduler = get_scheduler()
        if scheduler:
            scheduler.stop()
    
    return app


if __name__ == '__main__':
    print("🚀 Starting Bitcoin Analysis API...")
    print("📊 API Endpoints:")
    print("   - GET /api/realtime       - 实时数据")
    print("   - GET /api/historical     - 历史数据")
    print("   - GET /api/statistics     - 统计数据")
    print("   - GET /api/prediction     - 价格预测")
    print("   - GET /api/risk-alerts    - 风险警报")
    print("   - GET /api/candlestick    - K线数据")
    print("   - GET /api/health         - 健康检查")
    print("\n⏰ 定时任务: 每小时第5分钟自动更新数据")
    print("✅ Server running on http://localhost:5001")
    print("🔍 Debug mode enabled - Check console for detailed logs\n")
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
