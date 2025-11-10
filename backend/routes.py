"""
API 路由模块
"""
from flask import jsonify, request
from datetime import datetime
import pandas as pd
import traceback
from sklearn.ensemble import RandomForestRegressor

from api import BitcoinAPI
from cache import cache_manager
from database import db_manager
from utils import (
    calculate_technical_indicators,
    prepare_prediction_features,
    calculate_risk_alerts
)


def register_routes(app):
    """注册所有路由"""
    
    @app.route('/api/realtime', methods=['GET'])
    def get_realtime():
        """获取实时数据"""
        try:
            data = BitcoinAPI.fetch_realtime_data()
            if data:
                offline_mode = data.pop('offline_mode', False)
                return jsonify({
                    'success': True,
                    'data': data,
                    'offline_mode': offline_mode
                })
            return jsonify({
                'success': False, 
                'message': 'Failed to fetch realtime data'
            }), 500
        except Exception as e:
            print(f"Error in /api/realtime: {e}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    
    @app.route('/api/historical', methods=['GET'])
    def get_historical():
        """获取历史数据"""
        try:
            days = request.args.get('days', default=7, type=int)
            cache_key = f'historical_{days}d'
            
            # 检查缓存 - 1小时 (历史数据不需要频繁更新)
            days_requested = days
            if cache_manager.is_cache_valid(cache_key, max_age_seconds=3600):
                cache = cache_manager.get_cache(cache_key)
                df = cache['data']
                print(f"✅ 使用缓存的{days}天数据")
            else:
                # 优先从数据库获取历史数据（更稳定，不会变化）
                print(f"📊 从数据库获取{days}天历史数据")
                df = db_manager.get_historical_data(days=min(days, 365))
                
                # 如果数据库没有足够数据，再尝试API
                if df is None or df.empty or len(df) < days * 12:  # 每天至少12个数据点
                    print(f"⚠️ 数据库数据不足，尝试API获取")
                    df_api = BitcoinAPI.fetch_historical_data(days)
                    if df_api is not None and not df_api.empty:
                        df = df_api
                    elif df is not None and not df.empty:
                        # API失败，使用数据库的数据（即使不足）
                        print(f"⚠️ API失败，使用数据库现有数据")
                    else:
                        # 如果还是失败，尝试返回旧的缓存数据
                        cache = cache_manager.get_cache(cache_key)
                        if cache['data'] is not None:
                            print(f"⚠️ 返回旧缓存数据")
                            df = cache['data']
                        else:
                            return jsonify({
                                'success': False,
                                'message': 'No data available (offline mode)',
                                'offline_mode': True
                            }), 200  # 返回200而不是500
                
                if df is not None and not df.empty:
                    # 计算技术指标
                    df = calculate_technical_indicators(df)
                    cache_manager.set_cache(cache_key, df)
                    print(f"✅ 缓存{days}天数据（{len(df)}条记录）")
            
            # 确保df有所有必要的列
            required_cols = ['datetime', 'price', 'volume', 'ma_5', 'ma_10', 'ma_20', 
                            'rsi', 'macd', 'macd_signal', 'bb_upper', 'bb_middle', 'bb_lower', 'volatility']
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"⚠️ 缺少列: {missing_cols}，重新计算技术指标")
                df = calculate_technical_indicators(df)
                cache_manager.set_cache(cache_key, df)
            
            # 转换为JSON格式
            result = {
                'timestamps': df['datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
                'prices': df['price'].round(2).tolist(),
                'volumes': df['volume'].round(0).tolist(),
                'ma_5': df['ma_5'].round(2).tolist(),
                'ma_10': df['ma_10'].round(2).tolist(),
                'ma_20': df['ma_20'].round(2).tolist(),
                'rsi': df['rsi'].round(2).tolist(),
                'macd': df['macd'].round(2).tolist(),
                'macd_signal': df['macd_signal'].round(2).tolist(),
                'bb_upper': df['bb_upper'].round(2).tolist(),
                'bb_middle': df['bb_middle'].round(2).tolist(),
                'bb_lower': df['bb_lower'].round(2).tolist(),
                'volatility': df['volatility'].round(2).tolist()
            }
            
            response_payload = {
                'success': True,
                'data': result,
                'cached': cache_manager.is_cache_valid(cache_key, max_age_seconds=1800)
            }

            # 如果用户请求超过一年，告知前端数据库仅提供最近一年的离线数据
            if days_requested > 365:
                response_payload['partial'] = True
                response_payload['notice'] = 'Database only stores the last 365 days; fetch older data live.'

            return jsonify(response_payload)
        except Exception as e:
            print(f"Error in /api/historical: {e}")
            traceback.print_exc()
            
            # 最后的容错：返回空数据而不是500错误
            return jsonify({
                'success': False,
                'message': str(e),
                'data': {
                    'timestamps': [],
                    'prices': [],
                    'volumes': [],
                    'ma_5': [],
                    'ma_10': [],
                    'ma_20': [],
                    'rsi': [],
                    'macd': [],
                    'macd_signal': [],
                    'bb_upper': [],
                    'bb_middle': [],
                    'bb_lower': [],
                    'volatility': []
                }
            }), 200
    
    
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """获取统计数据"""
        try:
            # 检查缓存
            if cache_manager.is_cache_valid('statistics', max_age_seconds=600):
                cache = cache_manager.get_cache('statistics')
                print("✅ 使用缓存的统计数据")
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'cached': True
                })
            
            days = request.args.get('days', default=7, type=int)
            df = BitcoinAPI.fetch_historical_data(days)
            
            if df is None or df.empty:
                # 返回缓存的数据
                cache = cache_manager.get_cache('statistics')
                if cache['data'] is not None:
                    print("⚠️ 获取失败，返回缓存统计数据")
                    return jsonify({
                        'success': True,
                        'data': cache['data'],
                        'cached': True
                    })
                return jsonify({
                    'success': False,
                    'message': 'Failed to fetch data'
                }), 500
            
            # 计算24小时数据
            data_24h = df.tail(min(288, len(df)))
            
            stats = {
                'current_price': float(df['price'].iloc[-1]),
                'high_24h': float(data_24h['price'].max()),
                'low_24h': float(data_24h['price'].min()),
                'avg_price': float(df['price'].mean()),
                'total_volume': float(df['volume'].sum()),
                'avg_volume': float(df['volume'].mean()),
                'price_change_24h': float(
                    ((df['price'].iloc[-1] - data_24h['price'].iloc[0]) / 
                     data_24h['price'].iloc[0] * 100)
                ) if len(data_24h) > 0 else 0,
                'volatility': float(df['price'].std()),
                'max_price': float(df['price'].max()),
                'min_price': float(df['price'].min())
            }
            
            # 缓存结果
            cache_manager.set_cache('statistics', stats)
            
            return jsonify({
                'success': True,
                'data': stats,
                'cached': False
            })
        except Exception as e:
            print(f"Error in /api/statistics: {e}")
            traceback.print_exc()
            # 尝试返回缓存
            cache = cache_manager.get_cache('statistics')
            if cache['data'] is not None:
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'cached': True
                })
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    
    @app.route('/api/prediction', methods=['GET'])
    def get_prediction():
        """价格预测"""
        try:
            # 检查缓存
            if cache_manager.is_cache_valid('prediction', max_age_seconds=600):
                cache = cache_manager.get_cache('prediction')
                print("✅ 使用缓存的预测数据")
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'cached': True
                })
            
            df = BitcoinAPI.fetch_historical_data(days=7)
            if df is None or df.empty or len(df) < 20:
                # 返回缓存的预测
                cache = cache_manager.get_cache('prediction')
                if cache['data'] is not None:
                    print("⚠️ 获取失败，返回缓存预测")
                    return jsonify({
                        'success': True,
                        'data': cache['data'],
                        'cached': True
                    })
                return jsonify({
                    'success': False,
                    'message': 'Not enough data for prediction'
                }), 500
            
            # 特征工程
            df = prepare_prediction_features(df)
            
            # 准备训练数据
            feature_cols = ['price', 'volume', 'hour', 'day_of_week', 'returns', 'ma_5', 'ma_10']
            
            if len(df) < 15:
                # 数据太少，使用简单预测
                current_price = float(df['price'].iloc[-1])
                trend = df['price'].tail(5).pct_change().mean()
                prediction = current_price * (1 + trend)
            else:
                X = df[feature_cols].iloc[:-5]
                y = df['price'].iloc[5:]
                
                if len(X) < 10:
                    current_price = float(df['price'].iloc[-1])
                    prediction = current_price
                else:
                    # 训练模型
                    model = RandomForestRegressor(n_estimators=30, max_depth=10, random_state=42)
                    model.fit(X[:min(len(X), 100)], y[:min(len(y), 100)])
                    
                    # 预测 - 保持 DataFrame 格式以避免警告
                    last_features = df[feature_cols].iloc[-1:]
                    prediction = float(model.predict(last_features)[0])
            
            current_price = float(df['price'].iloc[-1])
            change_pct = ((prediction - current_price) / current_price) * 100
            
            result = {
                'current_price': round(current_price, 2),
                'predicted_price': round(prediction, 2),
                'change_percent': round(change_pct, 2),
                'direction': 'up' if change_pct > 0 else 'down',
                'confidence': 'medium',
                'timestamp': datetime.now().isoformat()
            }
            
            # 缓存结果
            cache_manager.set_cache('prediction', result)
            
            return jsonify({
                'success': True,
                'data': result,
                'cached': False
            })
        except Exception as e:
            print(f"Prediction error: {e}")
            traceback.print_exc()
            # 返回缓存
            cache = cache_manager.get_cache('prediction')
            if cache['data'] is not None:
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'cached': True
                })
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    
    @app.route('/api/risk-alerts', methods=['GET'])
    def get_risk_alerts():
        """风险警报"""
        try:
            df = BitcoinAPI.fetch_historical_data(days=7)
            if df is None or df.empty:
                return jsonify({
                    'success': True,
                    'data': []
                })
            
            alerts = calculate_risk_alerts(df)
            
            return jsonify({
                'success': True,
                'data': alerts
            })
        except Exception as e:
            print(f"Risk alerts error: {e}")
            traceback.print_exc()
            return jsonify({
                'success': True,
                'data': []
            })
    
    
    @app.route('/api/candlestick', methods=['GET'])
    def get_candlestick():
        """获取K线数据"""
        try:
            days = request.args.get('days', default=7, type=int)
            df = BitcoinAPI.fetch_historical_data(days)
            
            if df is None or df.empty:
                # 直接从数据库获取
                print(f"⚠️ API失败，直接从数据库获取 {days} 天数据")
                df = db_manager.get_historical_data(days=days)
                
            if df is None or df.empty:
                return jsonify({
                    'success': False,
                    'message': 'No data available (offline mode)',
                    'offline_mode': True
                }), 200  # 返回200而不是500,表示这是预期的降级
            
            # 按日期聚合
            df['date'] = df['datetime'].dt.date
            daily = df.groupby('date').agg({
                'price': ['first', 'max', 'min', 'last'],
                'volume': 'sum'
            }).reset_index()
            
            daily.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            
            result = {
                'dates': daily['date'].astype(str).tolist(),
                'data': daily[['open', 'close', 'low', 'high']].round(2).values.tolist(),
                'volumes': daily['volume'].round(0).tolist()
            }
            
            return jsonify({
                'success': True,
                'data': result
            })
        except Exception as e:
            print(f"Candlestick error: {e}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'success': False, 'message': 'Endpoint not found'}), 404
    
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
