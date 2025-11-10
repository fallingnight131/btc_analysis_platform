"""
数据库管理模块 - SQLite
支持离线模式：无网络时使用历史数据
"""
import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
import os


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path='bitcoin_data.db'):
        """初始化数据库"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 历史价格数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                price REAL NOT NULL,
                volume REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 技术指标缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON price_history(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cache_key 
            ON technical_cache(cache_key)
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化成功: {self.db_path}")
    
    def save_historical_data(self, df):
        """保存历史数据到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # 准备数据
            records = []
            for _, row in df.iterrows():
                records.append((
                    row['datetime'].isoformat(),
                    float(row['price']),
                    float(row['volume'])
                ))
            
            # 批量插入（忽略重复）
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT OR IGNORE INTO price_history (timestamp, price, volume)
                VALUES (?, ?, ?)
            ''', records)
            
            conn.commit()
            count = cursor.rowcount
            conn.close()
            
            if count > 0:
                print(f"✅ 保存了 {count} 条历史数据到数据库")
            return count
        except Exception as e:
            print(f"❌ 保存历史数据失败: {e}")
            return 0
    
    def get_historical_data(self, days=7):
        """从数据库获取历史数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # 计算时间范围
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            # 查询数据
            query = '''
                SELECT timestamp, price, volume
                FROM price_history
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
            '''
            
            df = pd.read_sql_query(
                query, 
                conn, 
                params=(start_time.isoformat(),)
            )
            conn.close()
            
            if df.empty:
                print(f"⚠️ 数据库中没有 {days} 天的数据")
                return None
            
            # 转换数据类型（使用混合格式解析）
            df['datetime'] = pd.to_datetime(df['timestamp'], format='mixed')
            df['price'] = df['price'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            print(f"✅ 从数据库读取了 {len(df)} 条历史数据")
            return df
            
        except Exception as e:
            print(f"❌ 读取历史数据失败: {e}")
            return None
    
    def save_cache(self, cache_key, data):
        """保存计算结果到数据库（JSON格式）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 序列化数据
            if isinstance(data, pd.DataFrame):
                json_data = data.to_json(orient='split', date_format='iso')
            else:
                json_data = json.dumps(data, default=str)
            
            # 插入或更新
            cursor.execute('''
                INSERT OR REPLACE INTO technical_cache 
                (cache_key, data, updated_at)
                VALUES (?, ?, ?)
            ''', (cache_key, json_data, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            print(f"✅ 缓存已保存: {cache_key}")
            return True
        except Exception as e:
            print(f"❌ 保存缓存失败: {e}")
            return False
    
    def get_cache(self, cache_key, max_age_hours=24):
        """从数据库获取缓存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询缓存
            cursor.execute('''
                SELECT data, updated_at
                FROM technical_cache
                WHERE cache_key = ?
            ''', (cache_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            data_json, updated_at = result
            
            # 检查是否过期
            update_time = datetime.fromisoformat(updated_at)
            age_hours = (datetime.now() - update_time).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                print(f"⚠️ 缓存已过期: {cache_key} (已有 {age_hours:.1f} 小时)")
                return None
            
            # 反序列化
            try:
                data = json.loads(data_json)
                # 如果是DataFrame格式，转换回来
                if isinstance(data, dict) and 'columns' in data:
                    data = pd.read_json(data_json, orient='split')
                print(f"✅ 从数据库读取缓存: {cache_key}")
                return data
            except:
                return data_json
                
        except Exception as e:
            print(f"❌ 读取缓存失败: {e}")
            return None
    
    def get_latest_data_time(self):
        """获取数据库中最新数据的时间"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT MAX(timestamp) FROM price_history
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return datetime.fromisoformat(result[0])
            return None
        except Exception as e:
            print(f"❌ 获取最新数据时间失败: {e}")
            return None
    
    def get_data_count(self):
        """获取数据库中的数据量"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM price_history')
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except Exception as e:
            print(f"❌ 获取数据量失败: {e}")
            return 0
    
    def clean_old_data(self, keep_days=90):
        """清理旧数据（保留最近N天）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = (datetime.now() - timedelta(days=keep_days)).isoformat()
            
            cursor.execute('''
                DELETE FROM price_history
                WHERE timestamp < ?
            ''', (cutoff_time,))
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            if deleted > 0:
                print(f"✅ 清理了 {deleted} 条过期数据（保留 {keep_days} 天）")
            return deleted
        except Exception as e:
            print(f"❌ 清理数据失败: {e}")
            return 0


# 创建全局数据库管理器实例
db_manager = DatabaseManager()
