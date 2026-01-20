"""
Exemple de robot trader pour BacktestGuru

Ce fichier montre comment crÃ©er un robot trader personnalisÃ©.
Le robot doit utiliser les variables suivantes disponibles:
- data: DataFrame pandas avec les colonnes (open, high, low, close, volume)
- initial_capital: Capital initial
- symbol: Symbole tradÃ©

Le robot doit dÃ©finir une variable 'results' avec le format suivant:
{
    "total_return": float,
    "sharpe_ratio": float,
    "max_drawdown": float,
    "win_rate": float,
    "total_trades": int,
    "profit_factor": float,
    "equity_curve": List[float],
    "trades": List[dict],
    "final_capital": float
}
"""

import pandas as pd
import numpy as np

# Exemple de stratÃ©gie simple: Achat et vente basÃ© sur RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Initialisation
df = data.copy()
capital = initial_capital
position = 0  # 0 = pas de position, 1 = long
entry_price = 0
trades = []
equity_curve = [capital]

# Calcul des indicateurs
df['rsi'] = calculate_rsi(df['close'], 14)
df['sma_20'] = df['close'].rolling(20).mean()

# Logique de trading
for i in range(20, len(df)):
    current_price = df['close'].iloc[i]
    rsi = df['rsi'].iloc[i]
    sma = df['sma_20'].iloc[i]
    
    # Gestion de la position existante
    if position == 1:
        # Sortie si RSI > 70 ou si prix < SMA (stop loss implicite)
        if rsi > 70 or current_price < sma * 0.98:
            pnl_pct = (current_price - entry_price) / entry_price
            pnl = capital * pnl_pct
            capital += pnl
            trades.append({
                'entry_date': str(df.index[entry_price]),
                'exit_date': str(df.index[i]),
                'entry_price': entry_price,
                'exit_price': current_price,
                'position': 'long',
                'pnl': pnl,
                'pnl_pct': pnl_pct * 100
            })
            position = 0
            entry_price = 0
    
    # Nouvelles entrÃ©es
    if position == 0:
        # Achat si RSI < 30 et prix > SMA
        if rsi < 30 and current_price > sma:
            position = 1
            entry_price = current_price
    
    equity_curve.append(capital)

# Fermer la position finale si nÃ©cessaire
if position == 1:
    final_price = df['close'].iloc[-1]
    pnl_pct = (final_price - entry_price) / entry_price
    pnl = capital * pnl_pct
    capital += pnl
    trades.append({
        'entry_date': str(df.index[entry_price]),
        'exit_date': str(df.index[-1]),
        'entry_price': entry_price,
        'exit_price': final_price,
        'position': 'long',
        'pnl': pnl,
        'pnl_pct': pnl_pct * 100
    })

# Calcul des mÃ©triques
total_return = (capital - initial_capital) / initial_capital * 100
winning_trades = [t for t in trades if t['pnl'] > 0]
losing_trades = [t for t in trades if t['pnl'] < 0]
win_rate = len(winning_trades) / len(trades) * 100 if trades else 0

total_profit = sum(t['pnl'] for t in winning_trades) if winning_trades else 0
total_loss = abs(sum(t['pnl'] for t in losing_trades)) if losing_trades else 1
profit_factor = total_profit / total_loss if total_loss > 0 else 0

# Sharpe ratio
returns = np.diff(equity_curve) / equity_curve[:-1]
sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0

# Max drawdown
peak = np.maximum.accumulate(equity_curve)
drawdown = (equity_curve - peak) / peak
max_drawdown = abs(np.min(drawdown)) * 100

# RÃ©sultats
results = {
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
