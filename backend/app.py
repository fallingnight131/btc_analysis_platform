"""
Bitcoin Analysis Platform - 主应用
重构后的精简版
"""
from flask import Flask
from flask_cors import CORS

from routes import register_routes


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    CORS(app)
    
    # 注册所有路由
    register_routes(app)
    
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
    print("\n✅ Server running on http://localhost:5001")
    print("🔍 Debug mode enabled - Check console for detailed logs\n")
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
