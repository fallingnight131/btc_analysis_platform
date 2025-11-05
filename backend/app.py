from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
import json
import traceback

app = Flask(__name__)
CORS(app)

# 全局变量存储数据 - 改进缓存结构
cached_data = {
    'historical_7d': {'last_update': None, 'data': None},
    'historical_30d': {'last_update': None, 'data': None},
    'statistics': {'last_update': None, 'data': None},
    'prediction': {'last_update': None, 'data': None},
    'candlestick': {'last_update': None, 'data': None}
}

# API请求计数器
request_counter = {
    'last_reset': datetime.now(),
    'count': 0
}

class BitcoinAPI:
    """比特币数据API"""
    
    @staticmethod
    def fetch_realtime_data():
        """获取实时数据"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin",
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_market_cap": "true"
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'bitcoin' not in data:
                print("Error: 'bitcoin' key not found in response")
                return None
                
            btc_data = data['bitcoin']
            
            return {
                'price': btc_data.get('usd', 0),
                'market_cap': btc_data.get('usd_market_cap', 0),
                'volume_24h': btc_data.get('usd_24h_vol', 0),
                'change_24h': btc_data.get('usd_24h_change', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching realtime data: {e}")
            traceback.print_exc()
            return None
    
    @staticmethod
    def fetch_historical_data(days=7):
        """获取历史数据 - 改进版本，带重试和更长缓存"""
        # 检查API请求频率
        global request_counter
        now = datetime.now()
        if (now - request_counter['last_reset']).seconds > 60:
            request_counter['last_reset'] = now
            request_counter['count'] = 0
        
        # 检查是否超过限制（每分钟最多10次）
        if request_counter['count'] >= 10:
            print(f"⚠️ API请求频率限制，使用缓存数据")
            cache_key = f'historical_{days}d'
            if cached_data[cache_key]['data'] is not None:
                print(f"返回缓存的{days}天数据")
                return cached_data[cache_key]['data']
        
        try:
            url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days
            }
            print(f"Fetching data from: {url} with params: {params}")
            
            response = requests.get(url, params=params, timeout=15)
            request_counter['count'] += 1
            
            response.raise_for_status()
            data = response.json()
            
            # 检查返回的数据结构
            print(f"Response keys: {data.keys()}")
            
            if 'prices' not in data:
                print(f"Error: 'prices' not in response. Available keys: {list(data.keys())}")
                # 返回缓存数据
                cache_key = f'historical_{days}d'
                if cached_data[cache_key]['data'] is not None:
                    print(f"返回缓存的{days}天数据")
                    return cached_data[cache_key]['data']
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            if 'total_volumes' in data:
                volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
                df = df.merge(volumes, on='timestamp', how='left')
            else:
                df['volume'] = 0
            
            print(f"Successfully fetched {len(df)} records")
            
            # 缓存数据
            cache_key = f'historical_{days}d'
            cached_data[cache_key]['data'] = df
            cached_data[cache_key]['last_update'] = datetime.now()
            
            return df
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"⚠️ API限流 (429)，使用缓存数据")
                cache_key = f'historical_{days}d'
                if cached_data[cache_key]['data'] is not None:
                    print(f"返回缓存的{days}天数据")
                    return cached_data[cache_key]['data']
            print(f"Request error: {e}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            traceback.print_exc()
            return None
    
    @staticmethod
    def calculate_technical_indicators(df):
        """计算技术指标"""
        try:
            # 确保有足够的数据
            if len(df) < 26:
                print(f"Warning: Not enough data points ({len(df)}) for full technical analysis")
            
            # MA
            df['ma_5'] = df['price'].rolling(window=min(5, len(df))).mean()
            df['ma_10'] = df['price'].rolling(window=min(10, len(df))).mean()
            df['ma_20'] = df['price'].rolling(window=min(20, len(df))).mean()
            
            # EMA
            df['ema_12'] = df['price'].ewm(span=min(12, len(df))).mean()
            df['ema_26'] = df['price'].ewm(span=min(26, len(df))).mean()
            
            # MACD
            df['macd'] = df['ema_12'] - df['ema_26']
            df['macd_signal'] = df['macd'].ewm(span=min(9, len(df))).mean()
            
            # RSI
            delta = df['price'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=min(14, len(df))).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df))).mean()
            rs = gain / (loss + 1e-10)  # 避免除零
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # 布林带
            df['bb_middle'] = df['price'].rolling(window=min(20, len(df))).mean()
            bb_std = df['price'].rolling(window=min(20, len(df))).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            # 波动率
            df['volatility'] = df['price'].rolling(window=min(24, len(df))).std()
            
            # 填充NaN值 - 修复警告
            df = df.bfill().ffill()  # 使用新的语法
            
            return df
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            traceback.print_exc()
            return df


# ========== API路由 ==========

@app.route('/api/realtime', methods=['GET'])
def get_realtime():
    """获取实时数据"""
    try:
        data = BitcoinAPI.fetch_realtime_data()
        if data:
            return jsonify({
                'success': True,
                'data': data
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
    """获取历史数据 - 改进缓存"""
    try:
        days = request.args.get('days', default=7, type=int)
        cache_key = f'historical_{days}d'
        
        # 检查缓存 - 延长到10分钟
        now = datetime.now()
        cache_valid = (
            cached_data[cache_key]['last_update'] and 
            cached_data[cache_key]['data'] is not None and 
            (now - cached_data[cache_key]['last_update']).seconds < 600  # 10分钟缓存
        )
        
        if cache_valid:
            df = cached_data[cache_key]['data']
            print(f"✅ 使用缓存的{days}天数据")
        else:
            df = BitcoinAPI.fetch_historical_data(days)
            if df is None or df.empty:
                # 如果获取失败，尝试返回旧的缓存数据
                if cached_data[cache_key]['data'] is not None:
                    print(f"⚠️ 获取数据失败，返回旧缓存")
                    df = cached_data[cache_key]['data']
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Failed to fetch historical data'
                    }), 500
            else:
                # 计算技术指标
                df = BitcoinAPI.calculate_technical_indicators(df)
                cached_data[cache_key]['data'] = df
                cached_data[cache_key]['last_update'] = now
                print(f"✅ 获取并缓存新的{days}天数据")
        
        # 确保df有所有必要的列
        required_cols = ['datetime', 'price', 'volume', 'ma_5', 'ma_10', 'ma_20', 
                        'rsi', 'macd', 'macd_signal', 'bb_upper', 'bb_middle', 'bb_lower', 'volatility']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"⚠️ 缺少列: {missing_cols}，重新计算技术指标")
            df = BitcoinAPI.calculate_technical_indicators(df)
            cached_data[cache_key]['data'] = df
        
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
        
        return jsonify({
            'success': True,
            'data': result,
            'cached': cache_valid
        })
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
        }), 200  # 返回200但success=False


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据 - 使用缓存"""
    try:
        # 检查缓存
        now = datetime.now()
        cache_valid = (
            cached_data['statistics']['last_update'] and
            cached_data['statistics']['data'] is not None and
            (now - cached_data['statistics']['last_update']).seconds < 600  # 10分钟
        )
        
        if cache_valid:
            print("✅ 使用缓存的统计数据")
            return jsonify({
                'success': True,
                'data': cached_data['statistics']['data'],
                'cached': True
            })
        
        days = request.args.get('days', default=7, type=int)
        df = BitcoinAPI.fetch_historical_data(days)
        
        if df is None or df.empty:
            # 返回缓存的数据
            if cached_data['statistics']['data'] is not None:
                print("⚠️ 获取失败，返回缓存统计数据")
                return jsonify({
                    'success': True,
                    'data': cached_data['statistics']['data'],
                    'cached': True
                })
            return jsonify({
                'success': False,
                'message': 'Failed to fetch data'
            }), 500
        
        # 计算24小时数据（288个5分钟数据点）
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
        cached_data['statistics']['data'] = stats
        cached_data['statistics']['last_update'] = now
        
        return jsonify({
            'success': True,
            'data': stats,
            'cached': False
        })
    except Exception as e:
        print(f"Error in /api/statistics: {e}")
        traceback.print_exc()
        # 尝试返回缓存
        if cached_data['statistics']['data'] is not None:
            return jsonify({
                'success': True,
                'data': cached_data['statistics']['data'],
                'cached': True
            })
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/prediction', methods=['GET'])
def get_prediction():
    """价格预测 - 使用缓存"""
    try:
        # 检查缓存
        now = datetime.now()
        cache_valid = (
            cached_data['prediction']['last_update'] and
            cached_data['prediction']['data'] is not None and
            (now - cached_data['prediction']['last_update']).seconds < 600  # 10分钟
        )
        
        if cache_valid:
            print("✅ 使用缓存的预测数据")
            return jsonify({
                'success': True,
                'data': cached_data['prediction']['data'],
                'cached': True
            })
        
        df = BitcoinAPI.fetch_historical_data(days=7)
        if df is None or df.empty or len(df) < 20:
            # 返回缓存的预测
            if cached_data['prediction']['data'] is not None:
                print("⚠️ 获取失败，返回缓存预测")
                return jsonify({
                    'success': True,
                    'data': cached_data['prediction']['data'],
                    'cached': True
                })
            return jsonify({
                'success': False,
                'message': 'Not enough data for prediction'
            }), 500
        
        # 特征工程
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['returns'] = df['price'].pct_change()
        df['ma_5'] = df['price'].rolling(window=5).mean()
        df['ma_10'] = df['price'].rolling(window=10).mean()
        df = df.bfill().fillna(0)  # 修复警告
        
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
                
                # 预测
                last_features = df[feature_cols].iloc[-1:].values
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
        cached_data['prediction']['data'] = result
        cached_data['prediction']['last_update'] = now
        
        return jsonify({
            'success': True,
            'data': result,
            'cached': False
        })
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        # 返回缓存
        if cached_data['prediction']['data'] is not None:
            return jsonify({
                'success': True,
                'data': cached_data['prediction']['data'],
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
        
        alerts = []
        
        # 计算指标
        df['returns'] = df['price'].pct_change() * 100
        df['volume_ma'] = df['volume'].rolling(window=min(24, len(df))).mean()
        df['volume_change'] = ((df['volume'] - df['volume_ma']) / 
                               (df['volume_ma'] + 1)) * 100
        
        # 检查最近的数据
        recent = df.tail(min(50, len(df)))
        
        for i in range(len(recent)):
            row = recent.iloc[i]
            
            if pd.isna(row['returns']):
                continue
            
            # 价格剧烈波动
            if abs(row['returns']) > 3:
                alerts.append({
                    'type': 'price_volatility',
                    'severity': 'high' if abs(row['returns']) > 5 else 'medium',
                    'message': f"价格波动 {row['returns']:+.2f}%",
                    'timestamp': row['datetime'].strftime('%Y-%m-%d %H:%M'),
                    'value': float(row['returns'])
                })
            
            # 交易量异常
            if not pd.isna(row['volume_change']) and row['volume_change'] > 150:
                alerts.append({
                    'type': 'volume_surge',
                    'severity': 'medium',
                    'message': f"交易量暴增 {row['volume_change']:.0f}%",
                    'timestamp': row['datetime'].strftime('%Y-%m-%d %H:%M'),
                    'value': float(row['volume_change'])
                })
        
        # 只返回最新的10个警报
        alerts = sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[:10]
        
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
            return jsonify({
                'success': False,
                'message': 'Failed to fetch data'
            }), 500
        
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
    
    app.run(debug=True, host='0.0.0.0', port=5001)