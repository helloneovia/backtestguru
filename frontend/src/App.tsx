import { useState } from 'react'
import { Container, Typography, Box, Tabs, Tab, Paper } from '@mui/material'
import BacktestForm from './components/BacktestForm'
import ResultsView from './components/ResultsView'
import { BacktestResult } from './types'

function App() {
  const [results, setResults] = useState<BacktestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState(0)

  const handleBacktestComplete = (result: BacktestResult) => {
    setResults(result)
    setTab(1) // Passer Ã  l'onglet rÃ©sultats
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
          BacktestGuru
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Backtesting de stratÃ©gies Forex & Crypto
        </Typography>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tab} onChange={(_, newValue) => setTab(newValue)}>
          <Tab label="Nouveau Backtest" />
          <Tab label="RÃ©sultats" disabled={!results} />
        </Tabs>
      </Paper>

      {tab === 0 && (
        <BacktestForm 
          onComplete={handleBacktestComplete} 
          loading={loading}
          setLoading={setLoading}
        />
      )}

      {tab === 1 && results && (
        <ResultsView results={results} />
      )}
    </Container>
  )
}

export default App
