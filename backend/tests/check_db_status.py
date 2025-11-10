#!/usr/bin/env python
"""
数据库状态检查工具
快速查看数据库中的数据量和时间范围
"""
import sys
import os
# 添加父目录到路径以便导入 backend 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db_manager
from datetime import datetime, timedelta

def check_database_status():
    """检查数据库状态"""
    print("=" * 60)
    print("📊 Bitcoin 数据库状态检查")
    print("=" * 60)
    
    # 获取总记录数
    total_count = db_manager.get_data_count()
    print(f"\n✅ 总记录数: {total_count:,} 条")
    
    # 获取最新数据时间
    latest_time = db_manager.get_latest_data_time()
    if latest_time:
        print(f"📅 最新数据: {latest_time}")
        
        # 计算数据覆盖的天数
        time_diff = datetime.now() - latest_time
        print(f"⏰ 数据新鲜度: {time_diff.total_seconds() / 3600:.1f} 小时前")
    else:
        print("⚠️  数据库中没有数据")
        return
    
    # 查询不同时间范围的数据量
    print("\n📈 各时间段数据分布:")
    for days in [7, 30, 90, 180, 365]:
        df = db_manager.get_historical_data(days=days)
        if df is not None and not df.empty:
            oldest = df['datetime'].min()
            newest = df['datetime'].max()
            span_days = (newest - oldest).days
            print(f"  最近 {days:3d} 天: {len(df):5d} 条记录 (实际跨度: {span_days} 天)")
        else:
            print(f"  最近 {days:3d} 天: 无数据")
    
    # 检查是否有超过一年的数据
    print("\n🔍 数据保留策略检查:")
    one_year_ago = datetime.now() - timedelta(days=365)
    
    try:
        from sqlalchemy import text
        with db_manager.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) as old_count
                FROM price_history
                WHERE timestamp < :cutoff_time
            """), {'cutoff_time': one_year_ago})
            old_count = result.fetchone()[0]
            
            if old_count > 0:
                print(f"  ⚠️  发现 {old_count} 条超过一年的数据（应该被清理）")
            else:
                print(f"  ✅ 所有数据都在一年以内（符合保留策略）")
    except Exception as e:
        print(f"  ❌ 检查失败: {e}")
    
    print("\n" + "=" * 60)
    print("提示: 数据库配置为最多保留最近 365 天的数据")
    print("=" * 60)

if __name__ == "__main__":
    check_database_status()
