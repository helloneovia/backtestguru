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
    { label: 'Taux de Réussite', value: formatPercent(results.win_rate), color: 'text.primary' },
    { label: 'Nombre de Trades', value: results.total_trades.toString(), color: 'text.primary' },
    { label: 'Profit Factor', value: results.profit_factor.toFixed(2), color: 'text.primary' }
  ]

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Grid container spacing={3}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ 
              background: 'rgba(30, 41, 59, 0.5)', 
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.05)',
            }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontSize: '0.875rem', mb: 1 }}>
                  {stat.label}
                </Typography>
                <Typography variant="h5" sx={{ color: stat.color, fontWeight: 700, fontSize: '1.75rem' }}>
                  {stat.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3, background: 'rgba(30, 41, 59, 0.5)', backdropFilter: 'blur(10px)' }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
          Courbe d'Équité
        </Typography>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={equityData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
            <XAxis 
              dataKey="day" 
              label={{ value: 'Jour', position: 'insideBottom', offset: -5, fill: '#cbd5e1' }}
              stroke="#cbd5e1"
            />
            <YAxis 
              label={{ value: 'Capital (€)', angle: -90, position: 'insideLeft', fill: '#cbd5e1' }}
              stroke="#cbd5e1"
            />
            <Tooltip 
              formatter={(value: number) => formatCurrency(value)}
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#f1f5f9',
              }}
            />
            <Legend wrapperStyle={{ color: '#cbd5e1' }} />
            <Line 
              type="monotone" 
              dataKey="capital" 
              stroke="#6366f1" 
              strokeWidth={3}
              name="Capital"
              dot={false}
              activeDot={{ r: 6, fill: '#8b5cf6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>

      <Paper sx={{ p: 3, background: 'rgba(30, 41, 59, 0.5)', backdropFilter: 'blur(10px)' }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
          Historique des Trades ({results.trades.length})
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600, color: 'text.primary' }}>Date Entrée</TableCell>
                <TableCell sx={{ fontWeight: 600, color: 'text.primary' }}>Date Sortie</TableCell>
                <TableCell sx={{ fontWeight: 600, color: 'text.primary' }}>Position</TableCell>
                <TableCell sx={{ fontWeight: 600, color: 'text.primary' }}>Prix Entrée</TableCell>
                <TableCell sx={{ fontWeight: 600, color: 'text.primary' }}>Prix Sortie</TableCell>
                <TableCell align="right" sx={{ fontWeight: 600, color: 'text.primary' }}>P&L</TableCell>
                <TableCell align="right" sx={{ fontWeight: 600, color: 'text.primary' }}>P&L %</TableCell>
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

      <Paper sx={{ p: 3, background: 'rgba(30, 41, 59, 0.5)', backdropFilter: 'blur(10px)' }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
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
