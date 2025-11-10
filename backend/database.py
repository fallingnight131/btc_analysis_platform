"""
数据库管理模块 - MySQL
支持离线模式：无网络时使用历史数据
"""
import pymysql
from sqlalchemy import create_engine, text
import pandas as pd
import json
from datetime import datetime, timedelta
import os


class DatabaseManager:
    """MySQL 数据库管理器"""
    
    def __init__(self):
        """初始化数据库连接"""
        # 数据库连接配置
        self.db_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'bitcoin_user'),
            'password': os.getenv('MYSQL_PASSWORD', 'bitcoin123'),
            'database': os.getenv('MYSQL_DATABASE', 'bitcoin_db'),
            'charset': 'utf8mb4'
        }
        
        # 创建 SQLAlchemy 引擎
        connection_string = (
            f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}"
            f"@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            f"?charset=utf8mb4"
        )
        self.engine = create_engine(connection_string, pool_pre_ping=True)
        self.init_database()
    
    def init_database(self):
        """创建数据库表"""
        try:
            with self.engine.connect() as conn:
                # 历史价格数据表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS price_history (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        timestamp DATETIME NOT NULL UNIQUE,
                        price DECIMAL(20, 8) NOT NULL,
                        volume DECIMAL(20, 8) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_timestamp (timestamp)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                '''))
                
                # 技术指标缓存表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS technical_cache (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        cache_key VARCHAR(255) UNIQUE NOT NULL,
                        data LONGTEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_cache_key (cache_key)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                '''))
                
                conn.commit()
            print(f"✅ MySQL 数据库初始化成功")
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
    
    def save_historical_data(self, df):
        """保存历史数据到数据库"""
        try:
            # 准备数据
            # 仅保存最近一年的数据到数据库，避免数据库无限膨胀
            keep_days = 365
            cutoff_time = datetime.now() - timedelta(days=keep_days)
            if 'datetime' in df.columns:
                df = df[df['datetime'] >= cutoff_time]

            records = []
            for _, row in df.iterrows():
                records.append({
                    'timestamp': row['datetime'],
                    'price': float(row['price']),
                    'volume': float(row['volume'])
                })
            
            if not records:
                return 0
            
            # 使用 INSERT IGNORE 避免重复键错误
            from sqlalchemy import text
            with self.engine.connect() as conn:
                for record in records:
                    try:
                        conn.execute(text('''
                            INSERT IGNORE INTO price_history (timestamp, price, volume)
                            VALUES (:timestamp, :price, :volume)
                        '''), record)
                    except:
                        # 忽略个别记录的错误
                        pass
                conn.commit()
            
            count = len(records)
            if count > 0:
                print(f"✅ 尝试保存 {count} 条历史数据到 MySQL")
                # 保存完成后，确保数据库只保留最近一年的数据
                try:
                    self.clean_old_data(keep_days=keep_days)
                except Exception:
                    pass
            return count
        except Exception as e:
            print(f"❌ 保存历史数据失败: {e}")
            return 0
    
    def get_historical_data(self, days=7, max_keep_days=365):
        """从数据库获取历史数据"""
        try:
            # 限制从数据库返回的数据天数，数据库仅保留最近 max_keep_days 天
            if days > max_keep_days:
                print(f"⚠️ 请求 {days} 天，数据库仅保留最近 {max_keep_days} 天，返回最近 {max_keep_days} 天的数据")
                days = max_keep_days

            # 计算时间范围
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            # 查询数据 - 使用 text() 来处理参数绑定
            from sqlalchemy import text
            query = text('''
                SELECT timestamp, price, volume
                FROM price_history
                WHERE timestamp >= :start_time
                ORDER BY timestamp ASC
            ''')
            
            df = pd.read_sql_query(
                query,
                self.engine,
                params={'start_time': start_time}
            )
            
            if df.empty:
                print(f"⚠️ 数据库中没有 {days} 天的数据")
                return None
            
            # 转换数据类型
            df['datetime'] = pd.to_datetime(df['timestamp'])
            df['price'] = df['price'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            print(f"✅ 从 MySQL 读取了 {len(df)} 条历史数据")
            return df
            
        except Exception as e:
            print(f"❌ 读取历史数据失败: {e}")
            return None
    
    def save_cache(self, cache_key, data):
        """保存计算结果到数据库（JSON格式）"""
        try:
            # 序列化数据
            if isinstance(data, pd.DataFrame):
                json_data = data.to_json(orient='split', date_format='iso')
            else:
                json_data = json.dumps(data, default=str)
            
            # 使用 REPLACE INTO 插入或更新
            with self.engine.connect() as conn:
                conn.execute(text('''
                    REPLACE INTO technical_cache (cache_key, data, updated_at)
                    VALUES (:cache_key, :data, :updated_at)
                '''), {
                    'cache_key': cache_key,
                    'data': json_data,
                    'updated_at': datetime.now()
                })
                conn.commit()
            
            print(f"✅ 缓存已保存到 MySQL: {cache_key}")
            return True
        except Exception as e:
            print(f"❌ 保存缓存失败: {e}")
            return False
    
    def get_cache(self, cache_key, max_age_hours=24):
        """从数据库获取缓存"""
        try:
            with self.engine.connect() as conn:
                # 查询缓存
                result = conn.execute(text('''
                    SELECT data, updated_at
                    FROM technical_cache
                    WHERE cache_key = :cache_key
                '''), {'cache_key': cache_key})
                
                row = result.fetchone()
            
            if not row:
                return None
            
            data_json, updated_at = row
            
            # 检查是否过期
            age_hours = (datetime.now() - updated_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                print(f"⚠️ 缓存已过期: {cache_key} (已有 {age_hours:.1f} 小时)")
                return None
            
            # 反序列化
            try:
                data = json.loads(data_json)
                # 如果是DataFrame格式，转换回来
                if isinstance(data, dict) and 'columns' in data:
                    data = pd.read_json(data_json, orient='split')
                print(f"✅ 从 MySQL 读取缓存: {cache_key}")
                return data
            except:
                return data_json
                
        except Exception as e:
            print(f"❌ 读取缓存失败: {e}")
            return None
    
    def get_latest_data_time(self):
        """获取数据库中最新数据的时间"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT MAX(timestamp) FROM price_history
                '''))
                
                row = result.fetchone()
            
            if row and row[0]:
                return row[0]
            return None
        except Exception as e:
            print(f"❌ 获取最新数据时间失败: {e}")
            return None
    
    def get_data_count(self):
        """获取数据库中的数据量"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('SELECT COUNT(*) FROM price_history'))
                count = result.fetchone()[0]
            return count
        except Exception as e:
            print(f"❌ 获取数据量失败: {e}")
            return 0
    
    def clean_old_data(self, keep_days=365):
        """清理旧数据（保留最近N天）"""
        try:
            cutoff_time = datetime.now() - timedelta(days=keep_days)
            
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    DELETE FROM price_history
                    WHERE timestamp < :cutoff_time
                '''), {'cutoff_time': cutoff_time})
                
                deleted = result.rowcount
                conn.commit()
            
            if deleted > 0:
                print(f"✅ 清理了 {deleted} 条过期数据（保留 {keep_days} 天）")
            return deleted
        except Exception as e:
            print(f"❌ 清理数据失败: {e}")
            return 0


# 创建全局数据库管理器实例
db_manager = DatabaseManager()
