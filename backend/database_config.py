"""
数据库配置模块
支持多种数据库：SQLite、PostgreSQL、MySQL、MongoDB
"""
import os
from enum import Enum


class DatabaseType(Enum):
    """数据库类型枚举"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"


class DatabaseConfig:
    """数据库配置"""
    
    # 从环境变量读取配置（默认使用 SQLite）
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()
    
    # SQLite 配置
    SQLITE_PATH = os.getenv('SQLITE_PATH', 'bitcoin_data.db')
    
    # PostgreSQL 配置
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'bitcoin_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'bitcoin_db')
    
    # MySQL 配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'bitcoin_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'bitcoin_db')
    
    # MongoDB 配置
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'bitcoin_db')
    
    @classmethod
    def get_connection_string(cls):
        """获取数据库连接字符串"""
        if cls.DB_TYPE == DatabaseType.SQLITE.value:
            return f"sqlite:///{cls.SQLITE_PATH}"
        
        elif cls.DB_TYPE == DatabaseType.POSTGRESQL.value:
            return (f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}"
                   f"@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}")
        
        elif cls.DB_TYPE == DatabaseType.MYSQL.value:
            return (f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}"
                   f"@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}")
        
        elif cls.DB_TYPE == DatabaseType.MONGODB.value:
            return cls.MONGODB_URI
        
        else:
            raise ValueError(f"不支持的数据库类型: {cls.DB_TYPE}")
    
    @classmethod
    def get_database_type(cls):
        """获取数据库类型"""
        return DatabaseType(cls.DB_TYPE)


# 各数据库所需依赖
DATABASE_DEPENDENCIES = {
    DatabaseType.SQLITE: [],  # Python 内置
    DatabaseType.POSTGRESQL: ['psycopg2-binary', 'sqlalchemy'],
    DatabaseType.MYSQL: ['pymysql', 'sqlalchemy'],
    DatabaseType.MONGODB: ['pymongo'],
}


def print_database_info():
    """打印当前数据库配置信息"""
    print("\n" + "="*60)
    print("📊 数据库配置信息")
    print("="*60)
    print(f"数据库类型: {DatabaseConfig.DB_TYPE.upper()}")
    
    if DatabaseConfig.DB_TYPE == DatabaseType.SQLITE.value:
        print(f"数据库文件: {DatabaseConfig.SQLITE_PATH}")
    
    elif DatabaseConfig.DB_TYPE == DatabaseType.POSTGRESQL.value:
        print(f"主机: {DatabaseConfig.POSTGRES_HOST}:{DatabaseConfig.POSTGRES_PORT}")
        print(f"数据库: {DatabaseConfig.POSTGRES_DATABASE}")
        print(f"用户: {DatabaseConfig.POSTGRES_USER}")
    
    elif DatabaseConfig.DB_TYPE == DatabaseType.MYSQL.value:
        print(f"主机: {DatabaseConfig.MYSQL_HOST}:{DatabaseConfig.MYSQL_PORT}")
        print(f"数据库: {DatabaseConfig.MYSQL_DATABASE}")
        print(f"用户: {DatabaseConfig.MYSQL_USER}")
    
    elif DatabaseConfig.DB_TYPE == DatabaseType.MONGODB.value:
        print(f"URI: {DatabaseConfig.MONGODB_URI}")
        print(f"数据库: {DatabaseConfig.MONGODB_DATABASE}")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    print_database_info()
