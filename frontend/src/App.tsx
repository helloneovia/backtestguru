import { useState } from 'react'
import { Container, Typography, Box, Tabs, Tab, Paper, AppBar, Toolbar, IconButton } from '@mui/material'
import { Star as StarIcon } from '@mui/icons-material'
import BacktestForm from './components/BacktestForm'
import ResultsView from './components/ResultsView'
import { BacktestResult } from './types'

function App() {
  const [results, setResults] = useState<BacktestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState(0)

  const handleBacktestComplete = (result: BacktestResult) => {
    setResults(result)
    setTab(1) // Passer à l'onglet résultats
  }

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar 
        position="static" 
        elevation={0}
        sx={{ 
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" component="div" sx={{ fontWeight: 600, letterSpacing: '0.5px' }}>
            backtest.guru
          </Typography>
          <IconButton color="inherit" edge="end">
            <StarIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography 
            variant="h3" 
            component="h1" 
            gutterBottom 
            sx={{ 
              fontWeight: 700, 
              background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1
            }}
          >
            BacktestGuru
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
            Backtesting de stratégies Forex & Crypto
          </Typography>
        </Box>

        <Paper 
          sx={{ 
            mb: 3,
            background: 'rgba(30, 41, 59, 0.5)',
            backdropFilter: 'blur(10px)',
          }}
        >
          <Tabs 
            value={tab} 
            onChange={(_, newValue) => setTab(newValue)}
            sx={{
              '& .MuiTab-root': {
                color: 'text.secondary',
                '&.Mui-selected': {
                  color: 'primary.main',
                },
              },
              '& .MuiTabs-indicator': {
                background: 'linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%)',
                height: 3,
                borderRadius: '3px 3px 0 0',
              },
            }}
          >
            <Tab label="NOUVEAU BACKTEST" />
            <Tab label="RÉSULTATS" disabled={!results} />
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
    </Box>
  )
}

export default App
