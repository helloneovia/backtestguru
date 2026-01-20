import { useState, useEffect } from 'react'
import {
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  TextareaAutosize
} from '@mui/material'
import { Upload as UploadIcon } from '@mui/icons-material'
import axios from 'axios'
import { BacktestResult } from '../types'

interface BacktestFormProps {
  onComplete: (result: BacktestResult) => void
  loading: boolean
  setLoading: (loading: boolean) => void
}

export default function BacktestForm({ onComplete, loading, setLoading }: BacktestFormProps) {
  const [method, setMethod] = useState<'description' | 'upload'>('description')
  const [symbol, setSymbol] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [initialCapital, setInitialCapital] = useState(10000)
  const [timeframe, setTimeframe] = useState('1d')
  const [marketType, setMarketType] = useState<'crypto' | 'forex'>('crypto')
  const [strategyDescription, setStrategyDescription] = useState('')
  const [robotFile, setRobotFile] = useState<File | null>(null)
  const [symbols, setSymbols] = useState<string[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    loadSymbols()
  }, [marketType])

  useEffect(() => {
    const today = new Date()
    const oneYearAgo = new Date(today)
    oneYearAgo.setFullYear(today.getFullYear() - 1)
    setEndDate(today.toISOString().split('T')[0])
    setStartDate(oneYearAgo.toISOString().split('T')[0])
  }, [])

  const loadSymbols = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000')
      const response = await axios.get(`${apiUrl}/api/symbols?market_type=${marketType}`)
      setSymbols(response.data.symbols)
      if (response.data.symbols.length > 0 && !symbol) {
        setSymbol(response.data.symbols[0])
      }
    } catch (err) {
      console.error('Erreur chargement symboles:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      let response
      const apiUrl = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000')
      
      if (method === 'description') {
        response = await axios.post(`${apiUrl}/api/backtest`, {
          strategy_description: strategyDescription,
          symbol,
          start_date: startDate,
          end_date: endDate,
          initial_capital: initialCapital,
          timeframe,
          market_type: marketType
        })
      } else {
        if (!robotFile) {
          setError('Veuillez sÃ©lectionner un fichier robot')
          setLoading(false)
          return
        }

        const formData = new FormData()
        formData.append('file', robotFile)
        formData.append('symbol', symbol)
        formData.append('start_date', startDate)
        formData.append('end_date', endDate)
        formData.append('initial_capital', initialCapital.toString())
        formData.append('timeframe', timeframe)
        formData.append('market_type', marketType)

        response = await axios.post(`${apiUrl}/api/backtest/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
      }

      onComplete(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur lors du backtest')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper sx={{ p: 4 }}>
      <Tabs value={method} onChange={(_, newValue) => setMethod(newValue)} sx={{ mb: 3 }}>
        <Tab label="Description de stratÃ©gie" value="description" />
        <Tab label="Upload Robot Trader" value="upload" />
      </Tabs>

      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <FormControl fullWidth>
            <InputLabel>Type de marchÃ©</InputLabel>
            <Select
              value={marketType}
              label="Type de marchÃ©"
              onChange={(e) => setMarketType(e.target.value as 'crypto' | 'forex')}
            >
              <MenuItem value="crypto">Crypto</MenuItem>
              <MenuItem value="forex">Forex</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Symbole</InputLabel>
            <Select
              value={symbol}
              label="Symbole"
              onChange={(e) => setSymbol(e.target.value)}
            >
              {symbols.map((s) => (
                <MenuItem key={s} value={s}>{s}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              label="Date de dÃ©but"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
              required
            />
            <TextField
              fullWidth
              label="Date de fin"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
              required
            />
          </Box>

          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              label="Capital initial"
              type="number"
              value={initialCapital}
              onChange={(e) => setInitialCapital(Number(e.target.value))}
              required
            />
            <FormControl fullWidth>
              <InputLabel>Timeframe</InputLabel>
              <Select
                value={timeframe}
                label="Timeframe"
                onChange={(e) => setTimeframe(e.target.value)}
              >
                <MenuItem value="1h">1 Heure</MenuItem>
                <MenuItem value="4h">4 Heures</MenuItem>
                <MenuItem value="1d">1 Jour</MenuItem>
                <MenuItem value="1wk">1 Semaine</MenuItem>
              </Select>
            </FormControl>
          </Box>

          {method === 'description' ? (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                DÃ©crivez votre stratÃ©gie (ex: "SMA 20 et 50, RSI 14, stop loss 2%, take profit 4%")
              </Typography>
              <TextareaAutosize
                minRows={6}
                value={strategyDescription}
                onChange={(e) => setStrategyDescription(e.target.value)}
                placeholder="Exemple: StratÃ©gie basÃ©e sur croisement de moyennes mobiles (SMA 20 et SMA 50) avec RSI 14. EntrÃ©e long quand SMA 20 croise au-dessus de SMA 50 et RSI < 30. Stop loss 2%, take profit 4%."
                style={{
                  width: '100%',
                  padding: '12px',
                  fontFamily: 'inherit',
                  fontSize: '14px',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  resize: 'vertical'
                }}
              />
            </Box>
          ) : (
            <Box>
              <input
                accept=".py,.txt"
                style={{ display: 'none' }}
                id="robot-file-upload"
                type="file"
                onChange={(e) => setRobotFile(e.target.files?.[0] || null)}
              />
              <label htmlFor="robot-file-upload">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<UploadIcon />}
                  fullWidth
                  sx={{ py: 2 }}
                >
                  {robotFile ? robotFile.name : 'Choisir un fichier robot trader (.py)'}
                </Button>
              </label>
              {robotFile && (
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Fichier sÃ©lectionnÃ©: {robotFile.name}
                </Typography>
              )}
            </Box>
          )}

          {error && (
            <Alert severity="error">{error}</Alert>
          )}

          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            sx={{ py: 1.5 }}
          >
            {loading ? (
              <>
                <CircularProgress size={20} sx={{ mr: 2 }} />
                Backtest en cours...
              </>
            ) : (
              'Lancer le Backtest'
            )}
          </Button>
        </Box>
      </form>
    </Paper>
  )
}
