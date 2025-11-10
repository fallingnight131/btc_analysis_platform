"""
测试 MySQL 连接
"""
import pymysql
import sys

print("🧪 测试 MySQL 连接")
print("="*60)

# 尝试连接
try:
    print("\n1️⃣ 尝试无密码连接 MySQL...")
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        charset='utf8mb4'
    )
    print("   ✅ 无密码连接成功！")
    
    # 创建数据库
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bitcoin_db")
    print("   ✅ 数据库 bitcoin_db 已创建")
    
    # 显示数据库
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(f"\n   📊 当前数据库列表：")
    for db in databases:
        print(f"      - {db[0]}")
    
    conn.close()
    
    print("\n✅ MySQL 准备就绪！")
    print("\n💡 下一步：运行迁移脚本")
    print("   python migrate_to_mysql_auto.py")
    
except pymysql.err.OperationalError as e:
    error_code = e.args[0]
    
    if error_code == 2002:
        print("   ❌ MySQL 服务未启动")
        print("\n   🔧 请启动 MySQL 服务：")
        print("      macOS: brew services start mysql")
        print("      Linux: sudo systemctl start mysql")
        sys.exit(1)
    
    elif error_code == 1045:
        print("   ⚠️ 需要密码连接")
        print("\n   请运行: python migrate_to_mysql_auto.py")
        print("   脚本会提示你输入密码")
        sys.exit(0)
    
    else:
        print(f"   ❌ 连接失败: {e}")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ 连接失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
