"""
缓存管理模块
"""
from datetime import datetime


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        # 全局缓存数据
        self.cached_data = {
            'historical_7d': {'last_update': None, 'data': None},
            'historical_30d': {'last_update': None, 'data': None},
            'statistics': {'last_update': None, 'data': None},
            'prediction': {'last_update': None, 'data': None},
            'candlestick': {'last_update': None, 'data': None}
        }
        
        # API请求计数器
        self.request_counter = {
            'last_reset': datetime.now(),
            'count': 0
        }
    
    def get_cache(self, key):
        """获取缓存数据"""
        return self.cached_data.get(key, {'last_update': None, 'data': None})
    
    def set_cache(self, key, data):
        """设置缓存数据"""
        if key not in self.cached_data:
            self.cached_data[key] = {'last_update': None, 'data': None}
        
        self.cached_data[key]['data'] = data
        self.cached_data[key]['last_update'] = datetime.now()
    
    def is_cache_valid(self, key, max_age_seconds=3600):
        """检查缓存是否有效（默认1小时）"""
        cache = self.cached_data.get(key)
        if not cache or cache['last_update'] is None or cache['data'] is None:
            return False
        
        age = (datetime.now() - cache['last_update']).seconds
        return age < max_age_seconds
    
    def check_rate_limit(self, limit=10, window=60):
        """检查API请求频率限制"""
        now = datetime.now()
        
        # 重置计数器
        if (now - self.request_counter['last_reset']).seconds > window:
            self.request_counter['last_reset'] = now
            self.request_counter['count'] = 0
        
        # 检查是否超过限制
        if self.request_counter['count'] >= limit:
            return False
        
        return True
    
    def increment_request_count(self):
        """增加请求计数"""
        self.request_counter['count'] += 1


# 创建全局缓存管理器实例
cache_manager = CacheManager()
