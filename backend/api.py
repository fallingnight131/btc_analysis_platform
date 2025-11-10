"""
Bitcoin API 数据获取模块
支持网络检测和离线降级
"""
import requests
import pandas as pd
import traceback
from datetime import datetime
from cache import cache_manager
from database import db_manager
from utils import calculate_technical_indicators


class BitcoinAPI:
    """比特币数据API"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    @staticmethod
    def check_network():
        """检查网络连接"""
        try:
            response = requests.get("https://www.google.com", timeout=3)
            return True
        except:
            try:
                # 备用检测
                response = requests.get("https://www.baidu.com", timeout=3)
                return True
            except:
                return False
    
    @staticmethod
    def fetch_realtime_data():
        """获取实时数据"""
        try:
            # 检查网络
            if not BitcoinAPI.check_network():
                print("⚠️ 网络不可用，使用数据库最新数据")
                df = db_manager.get_historical_data(days=1)
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    return {
                        'price': float(latest['price']),
                        'market_cap': 0,
                        'volume_24h': float(latest['volume']),
                        'change_24h': 0,
                        'timestamp': latest['datetime'].isoformat(),
                        'offline_mode': True
                    }
                return None
            
            url = f"{BitcoinAPI.BASE_URL}/simple/price"
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
            
            result = {
                'price': btc_data.get('usd', 0),
                'market_cap': btc_data.get('usd_market_cap', 0),
                'volume_24h': btc_data.get('usd_24h_vol', 0),
                'change_24h': btc_data.get('usd_24h_change', 0),
                'timestamp': datetime.now().isoformat(),
                'offline_mode': False
            }
            
            # 保存到数据库
            df = pd.DataFrame([{
                'datetime': datetime.now(),
                'price': result['price'],
                'volume': result['volume_24h']
            }])
            db_manager.save_historical_data(df)
            
            return result
        except Exception as e:
            print(f"❌ 获取实时数据失败: {e}")
            # 降级到数据库
            df = db_manager.get_historical_data(days=1)
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return {
                    'price': float(latest['price']),
                    'market_cap': 0,
                    'volume_24h': float(latest['volume']),
                    'change_24h': 0,
                    'timestamp': latest['datetime'].isoformat(),
                    'offline_mode': True
                }
            traceback.print_exc()
            return None
    
    @staticmethod
    def fetch_historical_data(days=7):
        """获取历史数据（支持离线模式）"""
        # 检查API请求频率
        if not cache_manager.check_rate_limit():
            print(f"⚠️ API请求频率限制，使用缓存数据")
            cache_key = f'historical_{days}d'
            cache = cache_manager.get_cache(cache_key)
            if cache['data'] is not None:
                print(f"返回缓存的{days}天数据")
                return cache['data']
        
        # 检查网络
        if not BitcoinAPI.check_network():
            print(f"⚠️ 网络不可用，从数据库读取 {days} 天历史数据")
            df = db_manager.get_historical_data(days=days)
            if df is not None:
                return df
            print(f"❌ 数据库中没有数据")
            return None
        
        try:
            url = f"{BitcoinAPI.BASE_URL}/coins/bitcoin/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days
            }
            print(f"Fetching data from: {url} with params: {params}")
            
            response = requests.get(url, params=params, timeout=15)
            cache_manager.increment_request_count()
            
            response.raise_for_status()
            data = response.json()
            
            # 检查返回的数据结构
            print(f"Response keys: {data.keys()}")
            
            if 'prices' not in data:
                print(f"Error: 'prices' not in response. Available keys: {list(data.keys())}")
                # 降级到数据库
                df = db_manager.get_historical_data(days=days)
                if df is not None:
                    print(f"返回数据库的{days}天数据")
                    return df
                # 降级到缓存
                cache_key = f'historical_{days}d'
                cache = cache_manager.get_cache(cache_key)
                if cache['data'] is not None:
                    print(f"返回缓存的{days}天数据")
                    return cache['data']
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            if 'total_volumes' in data:
                volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
                df = df.merge(volumes, on='timestamp', how='left')
            else:
                df['volume'] = 0
            
            print(f"✅ 成功获取 {len(df)} 条数据")
            
            # 保存到数据库
            saved_count = db_manager.save_historical_data(df)
            
            # 缓存数据
            cache_key = f'historical_{days}d'
            cache_manager.set_cache(cache_key, df)
            
            return df
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"⚠️ API限流 (429)，使用数据库数据")
                df = db_manager.get_historical_data(days=days)
                if df is not None:
                    return df
                # 降级到缓存
                cache_key = f'historical_{days}d'
                cache = cache_manager.get_cache(cache_key)
                if cache['data'] is not None:
                    print(f"返回缓存的{days}天数据")
                    return cache['data']
            print(f"Request error: {e}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"❌ 获取历史数据失败: {e}")
            # 降级到数据库
            df = db_manager.get_historical_data(days=days)
            if df is not None:
                print(f"返回数据库的{days}天数据")
                return df
            traceback.print_exc()
            return None
