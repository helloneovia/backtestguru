from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
import json
import os

try:
    from backtest_engine import BacktestEngine
    from strategy_parser import StrategyParser
    from optimizer import StrategyOptimizer
except ImportError:
    # Si importÃ© depuis la racine
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from backtest_engine import BacktestEngine
    from strategy_parser import StrategyParser
    from optimizer import StrategyOptimizer

app = FastAPI(title="BacktestGuru API", version="1.0.0")

# CORS middleware - accepter toutes les origines en production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, vous pouvez restreindre cela
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques du frontend si le dossier existe
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    # Servir les assets statiques
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve l'application SPA pour toutes les routes non-API"""
        # Ignorer les routes API
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Servir les fichiers statiques s'ils existent
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Pour le routing SPA, servir index.html pour toutes les autres routes
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="Not found")

# ModÃ¨les Pydantic
class BacktestRequest(BaseModel):
    strategy_description: Optional[str] = None
    symbol: str
    start_date: str
    end_date: str
    initial_capital: float = 10000.0
    timeframe: str = "1d"
    market_type: str = "crypto"  # "crypto" ou "forex"

class BacktestResult(BaseModel):
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    profit_factor: float
    equity_curve: List[float]
    trades: List[dict]
    optimization_suggestions: List[dict]

@app.get("/")
async def root():
    return {"message": "BacktestGuru API", "status": "running"}

@app.get("/api/symbols")
async def get_symbols(market_type: str = "crypto"):
    """Retourne la liste des symboles disponibles"""
    if market_type == "crypto":
        return {
            "symbols": [
                "BTC/USD", "ETH/USD", "BNB/USD", "SOL/USD", 
                "ADA/USD", "XRP/USD", "DOT/USD", "DOGE/USD",
                "MATIC/USD", "AVAX/USD", "LINK/USD", "UNI/USD"
            ]
        }
    else:  # forex
        return {
            "symbols": [
                "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
                "AUD/USD", "USD/CAD", "NZD/USD", "EUR/GBP",
                "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/CHF"
            ]
        }

@app.post("/api/backtest", response_model=BacktestResult)
async def run_backtest(request: BacktestRequest):
    """ExÃ©cute un backtest avec une description de stratÃ©gie"""
    try:
        engine = BacktestEngine(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            timeframe=request.timeframe,
            market_type=request.market_type
        )
        
        # Parser la stratÃ©gie depuis la description
        parser = StrategyParser()
        strategy = parser.parse_description(request.strategy_description or "")
        
        # ExÃ©cuter le backtest
        results = engine.run_backtest(strategy)
        
        # Optimisation
        optimizer = StrategyOptimizer()
        suggestions = optimizer.analyze_and_suggest(results)
        
        return BacktestResult(
            total_return=results["total_return"],
            sharpe_ratio=results["sharpe_ratio"],
            max_drawdown=results["max_drawdown"],
            win_rate=results["win_rate"],
            total_trades=results["total_trades"],
            profit_factor=results["profit_factor"],
            equity_curve=results["equity_curve"],
            trades=results["trades"],
            optimization_suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/backtest/upload")
async def upload_robot(file: UploadFile = File(...), symbol: str = None, 
                       start_date: str = None, end_date: str = None,
                       initial_capital: float = 10000.0, timeframe: str = "1d",
                       market_type: str = "crypto"):
    """Upload et exÃ©cute un backtest avec un robot trader (fichier Python)"""
    if not all([symbol, start_date, end_date]):
        raise HTTPException(status_code=400, detail="symbol, start_date et end_date sont requis")
    
    try:
        # Lire le fichier uploadÃ©
        content = await file.read()
        robot_code = content.decode("utf-8")
        
        engine = BacktestEngine(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            timeframe=timeframe,
            market_type=market_type
        )
        
        # ExÃ©cuter le backtest avec le robot
        results = engine.run_backtest_from_code(robot_code)
        
        # Optimisation
        optimizer = StrategyOptimizer()
        suggestions = optimizer.analyze_and_suggest(results)
        
        return BacktestResult(
            total_return=results["total_return"],
            sharpe_ratio=results["sharpe_ratio"],
            max_drawdown=results["max_drawdown"],
            win_rate=results["win_rate"],
            total_trades=results["total_trades"],
            profit_factor=results["profit_factor"],
            equity_curve=results["equity_curve"],
            trades=results["trades"],
            optimization_suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
