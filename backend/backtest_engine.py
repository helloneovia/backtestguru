import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import yfinance as yf
import ccxt
import time

class BacktestEngine:
    def __init__(self, symbol: str, start_date: str, end_date: str, 
                 initial_capital: float = 10000.0, timeframe: str = "1d",
                 market_type: str = "crypto"):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.timeframe = timeframe
        self.market_type = market_type
        self.data = None
        self.load_data()
    
    def load_data(self):
        if self.market_type == "crypto":
            self.data = self._load_crypto_data()
        else:
            self.data = self._load_forex_data()
    
    def _load_crypto_data(self):
        try:
            symbol_clean = self.symbol.replace("/", "-")
            ticker = yf.Ticker(symbol_clean)
            df = ticker.history(start=self.start_date, end=self.end_date, interval=self.timeframe)
            if df.empty:
                exchange = ccxt.binance()
                symbol_ccxt = self.symbol.replace("/USD", "/USDT") if "/USD" in self.symbol else self.symbol
                ohlcv = exchange.fetch_ohlcv(symbol_ccxt, self.timeframe, 
                                            exchange.parse8601(f"{self.start_date}T00:00:00Z"),
                                            exchange.parse8601(f"{self.end_date}T23:59:59Z"))
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
            else:
                df.columns = [col.lower() for col in df.columns]
            return df[['open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Erreur chargement crypto: {e}")
            return self._generate_demo_data()
    
    def _load_forex_data(self):
        try:
            symbol_clean = self.symbol.replace("/", "") + "=X"
            ticker = yf.Ticker(symbol_clean)
            df = ticker.history(start=self.start_date, end=self.end_date, interval=self.timeframe)
            if not df.empty:
                df.columns = [col.lower() for col in df.columns]
                return df[['open', 'high', 'low', 'close', 'volume']]
            else:
                return self._generate_demo_data()
        except Exception as e:
            print(f"Erreur chargement forex: {e}")
            return self._generate_demo_data()
    
    def _generate_demo_data(self):
        dates = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
        df = pd.DataFrame({
            'open': prices * (1 + np.random.randn(len(dates)) * 0.01),
            'high': prices * (1 + np.abs(np.random.randn(len(dates)) * 0.02)),
            'low': prices * (1 - np.abs(np.random.randn(len(dates)) * 0.02)),
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }, index=dates)
        return df
    
    def run_backtest(self, strategy: Dict) -> Dict:
        df = self.data.copy()
        capital = self.initial_capital
        position = 0
        entry_price = 0
        entry_index = 0
        trades = []
        equity_curve = [capital]
        sma_short = strategy.get("sma_short", 20)
        sma_long = strategy.get("sma_long", 50)
        rsi_period = strategy.get("rsi_period", 14)
        rsi_oversold = strategy.get("rsi_oversold", 30)
        rsi_overbought = strategy.get("rsi_overbought", 70)
        stop_loss_pct = strategy.get("stop_loss", 0.02)
        take_profit_pct = strategy.get("take_profit", 0.04)
        df['sma_short'] = df['close'].rolling(sma_short).mean()
        df['sma_long'] = df['close'].rolling(sma_long).mean()
        df['rsi'] = self._calculate_rsi(df['close'], rsi_period)
        for i in range(max(sma_long, rsi_period), len(df)):
            current_price = df['close'].iloc[i]
            sma_cross_up = (df['sma_short'].iloc[i] > df['sma_long'].iloc[i] and 
                           df['sma_short'].iloc[i-1] <= df['sma_long'].iloc[i-1])
            sma_cross_down = (df['sma_short'].iloc[i] < df['sma_long'].iloc[i] and 
                             df['sma_short'].iloc[i-1] >= df['sma_long'].iloc[i-1])
            rsi_oversold_signal = df['rsi'].iloc[i] < rsi_oversold
            rsi_overbought_signal = df['rsi'].iloc[i] > rsi_overbought
            if position != 0:
                pnl_pct = (current_price - entry_price) / entry_price if position == 1 else (entry_price - current_price) / entry_price
                if (position == 1 and (pnl_pct <= -stop_loss_pct or pnl_pct >= take_profit_pct)) or \
                   (position == -1 and (pnl_pct <= -stop_loss_pct or pnl_pct >= take_profit_pct)):
                    pnl = capital * pnl_pct
                    capital += pnl
                    entry_date = df.index[entry_index]
                    exit_date = df.index[i]
                    trades.append({
                        'entry_date': entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date),
                        'exit_date': exit_date.strftime('%Y-%m-%d') if hasattr(exit_date, 'strftime') else str(exit_date),
                        'entry_price': entry_price,
                        'exit_price': current_price,
                        'position': 'long' if position == 1 else 'short',
                        'pnl': pnl,
                        'pnl_pct': pnl_pct * 100
                    })
                    position = 0
                    entry_price = 0
                    entry_index = 0
            if position == 0:
                if sma_cross_up or rsi_oversold_signal:
                    position = 1
                    entry_price = current_price
                    entry_index = i
                elif sma_cross_down or rsi_overbought_signal:
                    position = -1
                    entry_price = current_price
                    entry_index = i
            equity_curve.append(capital)
        if position != 0:
            final_price = df['close'].iloc[-1]
            pnl_pct = (final_price - entry_price) / entry_price if position == 1 else (entry_price - final_price) / entry_price
            pnl = capital * pnl_pct
            capital += pnl
            entry_date = df.index[entry_index]
            exit_date = df.index[-1]
            trades.append({
                'entry_date': entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date),
                'exit_date': exit_date.strftime('%Y-%m-%d') if hasattr(exit_date, 'strftime') else str(exit_date),
                'entry_price': entry_price,
                'exit_price': final_price,
                'position': 'long' if position == 1 else 'short',
                'pnl': pnl,
                'pnl_pct': pnl_pct * 100
            })
        total_return = (capital - self.initial_capital) / self.initial_capital * 100
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        total_profit = sum(t['pnl'] for t in winning_trades) if winning_trades else 0
        total_loss = abs(sum(t['pnl'] for t in losing_trades)) if losing_trades else 1
        profit_factor = total_profit / total_loss if total_loss > 0 else 0
        returns = np.diff(equity_curve) / equity_curve[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        peak = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - peak) / peak
        max_drawdown = abs(np.min(drawdown)) * 100
        return {
            "total_return": round(total_return, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2),
            "win_rate": round(win_rate, 2),
            "total_trades": len(trades),
            "profit_factor": round(profit_factor, 2),
            "equity_curve": [round(x, 2) for x in equity_curve],
            "trades": trades,
            "final_capital": round(capital, 2)
        }
    
    def run_backtest_from_code(self, robot_code: str) -> Dict:
        namespace = {
            'pd': pd,
            'np': np,
            'data': self.data.copy(),
            'initial_capital': self.initial_capital,
            'symbol': self.symbol
        }
        try:
            exec(robot_code, namespace)
            if 'results' in namespace:
                return namespace['results']
            else:
                from strategy_parser import StrategyParser
                parser = StrategyParser()
                strategy = parser.parse_description("")
                return self.run_backtest(strategy)
        except Exception as e:
            raise Exception(f"Erreur dans l'exÃ©cution du robot: {str(e)}")
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
