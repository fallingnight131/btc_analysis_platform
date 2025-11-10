"""
测试离线模式
"""
import time
from database import db_manager
from api import BitcoinAPI

print("\n" + "="*60)
print("🧪 测试数据库和离线模式功能")
print("="*60 + "\n")

# 1. 测试网络检测
print("1️⃣ 测试网络连接检测:")
is_online = BitcoinAPI.check_network()
print(f"   网络状态: {'🟢 在线' if is_online else '🔴 离线'}\n")

# 2. 获取在线数据并保存到数据库
if is_online:
    print("2️⃣ 获取在线数据并保存到数据库:")
    df_7d = BitcoinAPI.fetch_historical_data(days=7)
    if df_7d is not None:
        print(f"   ✅ 获取了 {len(df_7d)} 条 7 天数据")
        saved = db_manager.save_historical_data(df_7d)
        print(f"   ✅ 保存了 {saved} 条新数据到数据库\n")
    
    df_30d = BitcoinAPI.fetch_historical_data(days=30)
    if df_30d is not None:
        print(f"   ✅ 获取了 {len(df_30d)} 条 30 天数据")
        saved = db_manager.save_historical_data(df_30d)
        print(f"   ✅ 保存了 {saved} 条新数据到数据库\n")
else:
    print("2️⃣ 网络不可用，跳过在线数据获取\n")

# 3. 查询数据库统计
print("3️⃣ 数据库统计信息:")
total_count = db_manager.get_data_count()
print(f"   数据总量: {total_count} 条")

latest_time = db_manager.get_latest_data_time()
if latest_time:
    print(f"   最新数据: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print(f"   最新数据: 无")

# 4. 测试从数据库读取历史数据
print("\n4️⃣ 测试从数据库读取历史数据:")
df_db = db_manager.get_historical_data(days=7)
if df_db is not None:
    print(f"   ✅ 成功读取 {len(df_db)} 条数据")
    print(f"   时间范围: {df_db['datetime'].min()} ~ {df_db['datetime'].max()}")
    print(f"   价格范围: ${df_db['price'].min():.2f} ~ ${df_db['price'].max():.2f}")
else:
    print(f"   ❌ 数据库中没有数据")

# 5. 测试缓存功能
print("\n5️⃣ 测试技术指标缓存:")
test_cache = {
    'ma_5': [100, 101, 102],
    'ma_10': [99, 100, 101],
    'timestamp': time.time()
}
db_manager.save_cache('test_indicators', test_cache)

cached = db_manager.get_cache('test_indicators', max_age_hours=1)
if cached:
    print(f"   ✅ 缓存读取成功: {cached}")
else:
    print(f"   ❌ 缓存读取失败")

print("\n" + "="*60)
print("✅ 测试完成！")
print("="*60 + "\n")

# 提示
print("💡 使用方法:")
print("   1. 有网络时，系统会自动从 CoinGecko 获取数据并保存到数据库")
print("   2. 断网时，系统会自动从数据库读取历史数据")
print("   3. 前端会显示 '离线模式' 徽章提示用户")
print("   4. 数据库文件: bitcoin_data.db (SQLite格式)")
print()
