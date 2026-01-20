import {
  Paper,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip
} from '@mui/material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { BacktestResult } from '../types'

interface ResultsViewProps {
  results: BacktestResult
}

export default function ResultsView({ results }: ResultsViewProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2
    }).format(value)
  }

  const formatPercent = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'error'
      case 'high': return 'warning'
      case 'medium': return 'info'
      case 'low': return 'success'
      default: return 'default'
    }
  }

  const equityData = results.equity_curve.map((value, index) => ({
    day: index,
    capital: value
  }))

  const stats = [
    { label: 'Rendement Total', value: formatPercent(results.total_return), color: results.total_return >= 0 ? 'success.main' : 'error.main' },
    { label: 'Sharpe Ratio', value: results.sharpe_ratio.toFixed(2), color: 'text.primary' },
    { label: 'Drawdown Max', value: formatPercent(-results.max_drawdown), color: 'error.main' },
    { label: 'Taux de RÃ©ussite', value: formatPercent(results.win_rate), color: 'text.primary' },
    { label: 'Nombre de Trades', value: results.total_trades.toString(), color: 'text.primary' },
    { label: 'Profit Factor', value: results.profit_factor.toFixed(2), color: 'text.primary' }
  ]

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Grid container spacing={2}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  {stat.label}
                </Typography>
                <Typography variant="h5" sx={{ color: stat.color, fontWeight: 'bold' }}>
                  {stat.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Courbe d'Ã‰quitÃ©
        </Typography>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={equityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" label={{ value: 'Jour', position: 'insideBottom', offset: -5 }} />
            <YAxis label={{ value: 'Capital (â‚¬)', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value: number) => formatCurrency(value)} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="capital" 
              stroke="#1976d2" 
              strokeWidth={2}
              name="Capital"
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Historique des Trades ({results.trades.length})
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Date EntrÃ©e</TableCell>
                <TableCell>Date Sortie</TableCell>
                <TableCell>Position</TableCell>
                <TableCell>Prix EntrÃ©e</TableCell>
                <TableCell>Prix Sortie</TableCell>
                <TableCell align="right">P&L</TableCell>
                <TableCell align="right">P&L %</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.trades.slice(0, 50).map((trade, index) => (
                <TableRow key={index}>
                  <TableCell>{trade.entry_date}</TableCell>
                  <TableCell>{trade.exit_date}</TableCell>
                  <TableCell>
                    <Chip 
                      label={trade.position} 
                      size="small"
                      color={trade.position === 'long' ? 'success' : 'error'}
                    />
                  </TableCell>
                  <TableCell>{formatCurrency(trade.entry_price)}</TableCell>
                  <TableCell>{formatCurrency(trade.exit_price)}</TableCell>
                  <TableCell align="right" sx={{ color: trade.pnl >= 0 ? 'success.main' : 'error.main' }}>
                    {formatCurrency(trade.pnl)}
                  </TableCell>
                  <TableCell align="right" sx={{ color: trade.pnl >= 0 ? 'success.main' : 'error.main' }}>
                    {formatPercent(trade.pnl_pct)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        {results.trades.length > 50 && (
          <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
            Affichage des 50 premiers trades sur {results.trades.length} au total
          </Typography>
        )}
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Suggestions d'Optimisation
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {results.optimization_suggestions.map((suggestion, index) => (
            <Alert 
              key={index}
              severity={getPriorityColor(suggestion.priority) as any}
              sx={{ textAlign: 'left' }}
            >
              <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
                {suggestion.title}
              </Typography>
              <Typography variant="body2" paragraph>
                {suggestion.description}
              </Typography>
              <Typography variant="body2" sx={{ fontStyle: 'italic', mt: 1 }}>
                <strong>Recommandation:</strong> {suggestion.recommendation}
              </Typography>
            </Alert>
          ))}
        </Box>
      </Paper>
    </Box>
  )
}
