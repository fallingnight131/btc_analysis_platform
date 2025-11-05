"""
工具函数模块
"""
import pandas as pd
import traceback


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
        
        # 填充NaN值
        df = df.bfill().ffill()
        
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        traceback.print_exc()
        return df


def prepare_prediction_features(df):
    """准备预测特征"""
    try:
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['returns'] = df['price'].pct_change()
        df['ma_5'] = df['price'].rolling(window=5).mean()
        df['ma_10'] = df['price'].rolling(window=10).mean()
        df = df.bfill().fillna(0)
        
        return df
    except Exception as e:
        print(f"Error preparing features: {e}")
        traceback.print_exc()
        return df


def calculate_risk_alerts(df):
    """计算风险警报"""
    try:
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
        
        return alerts
    except Exception as e:
        print(f"Error calculating risk alerts: {e}")
        traceback.print_exc()
        return []
