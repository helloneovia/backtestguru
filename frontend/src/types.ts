export interface BacktestResult {
  total_return: number
  sharpe_ratio: number
  max_drawdown: number
  win_rate: number
  total_trades: number
  profit_factor: number
  equity_curve: number[]
  trades: Trade[]
  optimization_suggestions: OptimizationSuggestion[]
}

export interface Trade {
  entry_date: string
  exit_date: string
  entry_price: number
  exit_price: number
  position: 'long' | 'short'
  pnl: number
  pnl_pct: number
}

export interface OptimizationSuggestion {
  type: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  title: string
  description: string
  recommendation: string
}
