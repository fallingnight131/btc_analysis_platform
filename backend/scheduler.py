"""
定时任务调度器
每小时自动更新比特币历史数据
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

# 导入必要的模块
from api import BitcoinAPI
from database import DatabaseManager
from cache import CacheManager
from utils import calculate_technical_indicators

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataUpdateScheduler:
    """数据更新调度器"""
    
    def __init__(self, db_manager: DatabaseManager, cache_manager: CacheManager):
        """
        初始化调度器
        
        Args:
            db_manager: 数据库管理器实例
            cache_manager: 缓存管理器实例
        """
        self.db_manager = db_manager
        self.cache_manager = cache_manager
        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        self.is_running = False
        
    def update_historical_data(self):
        """定时更新历史数据"""
        try:
            logger.info(f"🔄 开始定时更新历史数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 获取最近7天的数据
            df = BitcoinAPI.fetch_historical_data(days=7)
            
            if df is not None and not df.empty:
                # 过滤：只保存数据库中没有的新数据
                # 查询数据库中最新的时间戳
                try:
                    from sqlalchemy import text
                    with self.db_manager.engine.connect() as conn:
                        result = conn.execute(text("SELECT MAX(timestamp) as max_time FROM price_history"))
                        row = result.fetchone()
                        latest_db_time = row[0] if row and row[0] else None
                    
                    if latest_db_time:
                        # 只保存比数据库最新时间更新的数据
                        df = df[df['datetime'] > latest_db_time]
                        logger.info(f"📊 过滤后有 {len(df)} 条新数据需要保存（数据库最新时间: {latest_db_time}）")
                    
                    if df.empty:
                        logger.info(f"✅ 数据库已是最新，无需更新")
                        return
                except Exception as e:
                    logger.warning(f"⚠️ 查询数据库最新时间失败: {e}，将保存所有数据")
                
                # 保存到数据库（会自动清理超过365天的旧数据）
                saved_count = self.db_manager.save_historical_data(df)
                logger.info(f"✅ 成功保存 {saved_count} 条数据到数据库")
                
                # 额外执行一次数据清理，确保数据库只保留最近365天
                deleted_count = self.db_manager.clean_old_data(keep_days=365)
                if deleted_count > 0:
                    logger.info(f"🗑️ 清理了 {deleted_count} 条过期数据")
                
                # 重新获取完整的7天数据用于计算技术指标和缓存
                df_full = self.db_manager.get_historical_data(days=7)
                if df_full is not None and not df_full.empty:
                    # 计算技术指标
                    from utils import calculate_technical_indicators
                    df_full = calculate_technical_indicators(df_full)
                    
                    # 更新缓存（清除旧缓存，强制下次查询使用新数据）
                    cache_keys = ['historical_7d', 'historical_30d', 'historical_90d', 'historical_365d']
                    for key in cache_keys:
                        self.cache_manager.clear_cache(key)
                    
                    logger.info(f"✅ 清除缓存，强制使用新数据")
                    logger.info(f"✅ 定时更新完成 - 数据时间范围: {df_full['datetime'].min()} 到 {df_full['datetime'].max()}")
            else:
                logger.warning("⚠️ 获取数据失败，跳过本次更新")
                
        except Exception as e:
            logger.error(f"❌ 定时更新失败: {e}")
            import traceback
            traceback.print_exc()
    
    def start(self):
        """启动调度器"""
        if self.is_running:
            logger.warning("⚠️ 调度器已在运行")
            return
        
        try:
            # 添加定时任务：每小时的第5分钟执行
            self.scheduler.add_job(
                func=self.update_historical_data,
                trigger=CronTrigger(minute=5),  # 每小时的第5分钟
                id='update_historical_data',
                name='更新比特币历史数据',
                replace_existing=True
            )
            
            # 启动调度器
            self.scheduler.start()
            self.is_running = True
            logger.info("✅ 定时任务调度器已启动 - 每小时第5分钟更新数据")
            
            # 立即执行一次更新
            logger.info("🚀 执行初始数据更新...")
            self.update_historical_data()
            
        except Exception as e:
            logger.error(f"❌ 启动调度器失败: {e}")
            import traceback
            traceback.print_exc()
    
    def stop(self):
        """停止调度器"""
        if not self.is_running:
            logger.warning("⚠️ 调度器未运行")
            return
        
        try:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            logger.info("✅ 定时任务调度器已停止")
        except Exception as e:
            logger.error(f"❌ 停止调度器失败: {e}")
    
    def get_next_run_time(self):
        """获取下次执行时间"""
        if not self.is_running:
            return None
        
        job = self.scheduler.get_job('update_historical_data')
        if job:
            return job.next_run_time
        return None


# 全局调度器实例（将在 app.py 中初始化）
scheduler_instance = None


def init_scheduler(db_manager: DatabaseManager, cache_manager: CacheManager):
    """
    初始化全局调度器实例
    
    Args:
        db_manager: 数据库管理器实例
        cache_manager: 缓存管理器实例
    
    Returns:
        DataUpdateScheduler: 调度器实例
    """
    global scheduler_instance
    if scheduler_instance is None:
        scheduler_instance = DataUpdateScheduler(db_manager, cache_manager)
        scheduler_instance.start()
    return scheduler_instance


def get_scheduler():
    """获取调度器实例"""
    return scheduler_instance
