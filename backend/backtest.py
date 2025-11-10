"""
交易策略回测模块
基于真实历史数据进行策略回测
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class Backtest:
    """回测引擎"""
    
    def __init__(self, data, initial_capital=10000):
        """
        初始化回测引擎
        
        Args:
            data: DataFrame，包含价格和技术指标
            initial_capital: 初始资金
        """
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # 持仓数量
        self.trades = []
        self.equity_curve = []
        
    def run_ma_cross_strategy(self, short_period=5, long_period=20):
        """
        MA均线交叉策略
        
        Args:
            short_period: 短期均线周期
            long_period: 长期均线周期
        """
        # 计算均线
        self.data['ma_short'] = self.data['price'].rolling(window=short_period).mean()
        self.data['ma_long'] = self.data['price'].rolling(window=long_period).mean()
        
        # 生成交易信号
        self.data['signal'] = 0
        self.data.loc[self.data['ma_short'] > self.data['ma_long'], 'signal'] = 1  # 买入信号
        self.data.loc[self.data['ma_short'] < self.data['ma_long'], 'signal'] = -1  # 卖出信号
        
        # 执行交易
        self._execute_trades()
        
        return self._calculate_metrics()
    
    def run_rsi_strategy(self, period=14, oversold=30, overbought=70):
        """
        RSI反转策略
        
        Args:
            period: RSI周期
            oversold: 超卖阈值
            overbought: 超买阈值
        """
        # 使用已有的RSI或重新计算
        if 'rsi' not in self.data.columns:
            self.data['rsi'] = self._calculate_rsi(period)
        
        # 生成交易信号
        self.data['signal'] = 0
        self.data.loc[self.data['rsi'] < oversold, 'signal'] = 1  # 超卖买入
        self.data.loc[self.data['rsi'] > overbought, 'signal'] = -1  # 超买卖出
        
        # 执行交易
        self._execute_trades()
        
        return self._calculate_metrics()
    
    def run_breakout_strategy(self, lookback=20, threshold=2):
        """
        突破策略
        
        Args:
            lookback: 回溯周期
            threshold: 突破幅度百分比
        """
        # 计算最高最低价
        self.data['high_n'] = self.data['price'].rolling(window=lookback).max()
        self.data['low_n'] = self.data['price'].rolling(window=lookback).min()
        
        # 生成交易信号
        self.data['signal'] = 0
        breakout_up = self.data['price'] > self.data['high_n'].shift(1) * (1 + threshold/100)
        breakout_down = self.data['price'] < self.data['low_n'].shift(1) * (1 - threshold/100)
        
        self.data.loc[breakout_up, 'signal'] = 1  # 向上突破买入
        self.data.loc[breakout_down, 'signal'] = -1  # 向下突破卖出
        
        # 执行交易
        self._execute_trades()
        
        return self._calculate_metrics()
    
    def run_grid_strategy(self, grids=10, price_range=10):
        """
        网格策略
        
        Args:
            grids: 网格数量
            price_range: 价格区间百分比
        """
        # 计算价格中心和网格
        price_center = self.data['price'].mean()
        grid_size = price_center * price_range / 100 / grids
        
        # 生成网格价格
        grid_prices = [price_center + (i - grids/2) * grid_size for i in range(grids + 1)]
        
        # 简化版：价格下跌买入，上涨卖出
        self.data['signal'] = 0
        self.data['price_change'] = self.data['price'].pct_change()
        
        # 价格下跌超过一个网格，买入
        self.data.loc[self.data['price_change'] < -price_range/(grids*100), 'signal'] = 1
        # 价格上涨超过一个网格，卖出
        self.data.loc[self.data['price_change'] > price_range/(grids*100), 'signal'] = -1
        
        # 执行交易
        self._execute_trades()
        
        return self._calculate_metrics()
    
    def _calculate_rsi(self, period=14):
        """计算RSI指标"""
        delta = self.data['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _execute_trades(self):
        """执行交易"""
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []
        
        prev_signal = 0
        
        for idx, row in self.data.iterrows():
            if pd.isna(row['signal']):
                continue
            
            signal = row['signal']
            price = row['price']
            timestamp = row['datetime'] if 'datetime' in row else idx
            
            # 买入信号
            if signal == 1 and prev_signal != 1 and self.position == 0:
                # 全仓买入
                self.position = self.capital / price
                trade = {
                    'type': 'BUY',
                    'time': timestamp,
                    'price': price,
                    'quantity': self.position,
                    'capital': 0,
                    'profit': 0
                }
                self.trades.append(trade)
                self.capital = 0
            
            # 卖出信号
            elif signal == -1 and prev_signal != -1 and self.position > 0:
                # 全部卖出
                self.capital = self.position * price
                profit_pct = ((self.capital - self.initial_capital) / self.initial_capital) * 100
                trade = {
                    'type': 'SELL',
                    'time': timestamp,
                    'price': price,
                    'quantity': self.position,
                    'capital': self.capital,
                    'profit': profit_pct
                }
                self.trades.append(trade)
                self.position = 0
            
            # 记录权益曲线
            current_equity = self.capital + self.position * price
            self.equity_curve.append(current_equity)
            
            prev_signal = signal
        
        # 如果最后还有持仓，按最后价格平仓
        if self.position > 0:
            last_price = self.data.iloc[-1]['price']
            self.capital = self.position * last_price
            self.position = 0
    
    def _calculate_metrics(self):
        """计算回测指标"""
        if len(self.equity_curve) == 0:
            return None
        
        # 最终收益
        final_capital = self.equity_curve[-1] if self.equity_curve else self.initial_capital
        total_return = ((final_capital - self.initial_capital) / self.initial_capital) * 100
        
        # 计算交易统计
        winning_trades = [t for t in self.trades if t['type'] == 'SELL' and t['profit'] > 0]
        losing_trades = [t for t in self.trades if t['type'] == 'SELL' and t['profit'] <= 0]
        
        total_trades = len([t for t in self.trades if t['type'] == 'SELL'])
        win_count = len(winning_trades)
        loss_count = len(losing_trades)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
        
        avg_win = np.mean([t['profit'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['profit'] for t in losing_trades]) if losing_trades else 0
        
        # 最大回撤
        equity_series = pd.Series(self.equity_curve)
        cummax = equity_series.cummax()
        drawdown = (equity_series - cummax) / cummax * 100
        max_drawdown = drawdown.min()
        
        # 夏普比率（简化版）
        returns = equity_series.pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if len(returns) > 0 and returns.std() > 0 else 0
        
        # 年化收益
        days = len(self.data)
        annual_return = total_return * (365 / days) if days > 0 else 0
        
        # 盈亏比
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        
        return {
            'totalReturn': total_return,
            'annualReturn': annual_return,
            'maxDrawdown': max_drawdown,
            'sharpeRatio': sharpe_ratio,
            'totalTrades': total_trades,
            'winningTrades': win_count,
            'losingTrades': loss_count,
            'winRate': win_rate,
            'avgWin': avg_win,
            'avgLoss': avg_loss,
            'profitFactor': profit_factor,
            'equityCurve': self.equity_curve,
            'recentTrades': self._format_recent_trades(10)
        }
    
    def _format_recent_trades(self, count=10):
        """格式化最近的交易记录"""
        recent = self.trades[-count:] if len(self.trades) > count else self.trades
        formatted = []
        
        for trade in recent:
            formatted.append({
                'time': trade['time'].strftime('%Y-%m-%d') if isinstance(trade['time'], datetime) else str(trade['time']),
                'type': trade['type'],
                'price': float(trade['price']),
                'quantity': float(trade['quantity']),
                'profit': float(trade.get('profit', 0))
            })
        
        return formatted
