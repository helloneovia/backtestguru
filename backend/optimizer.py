import numpy as np
from typing import Dict, List

class StrategyOptimizer:
    def analyze_and_suggest(self, results: Dict) -> List[Dict]:
        suggestions = []
        if results["win_rate"] < 40:
            suggestions.append({
                "type": "win_rate",
                "priority": "high",
                "title": "Taux de rÃ©ussite faible",
                "description": f"Votre stratÃ©gie a un taux de rÃ©ussite de {results['win_rate']:.1f}%. " +
                              "ConsidÃ©rez d'ajuster vos critÃ¨res d'entrÃ©e ou d'utiliser un filtre de tendance.",
                "recommendation": "Augmenter les seuils RSI (oversold > 25, overbought < 75) ou ajouter un filtre de tendance avec une moyenne mobile plus longue."
            })
        elif results["win_rate"] > 60:
            suggestions.append({
                "type": "win_rate",
                "priority": "low",
                "title": "Excellent taux de rÃ©ussite",
                "description": f"Votre stratÃ©gie a un taux de rÃ©ussite de {results['win_rate']:.1f}%.",
                "recommendation": "Vous pourriez augmenter lÃ©gÃ¨rement la taille des positions pour maximiser les profits."
            })
        if results["profit_factor"] < 1.2:
            suggestions.append({
                "type": "profit_factor",
                "priority": "high",
                "title": "Profit factor faible",
                "description": f"Votre profit factor est de {results['profit_factor']:.2f}. " +
                              "Les pertes moyennes sont trop importantes par rapport aux gains.",
                "recommendation": "RÃ©duire le stop loss ou augmenter le take profit pour amÃ©liorer le ratio risque/rÃ©compense."
            })
        if results["max_drawdown"] > 30:
            suggestions.append({
                "type": "drawdown",
                "priority": "high",
                "title": "Drawdown maximum Ã©levÃ©",
                "description": f"Votre drawdown maximum est de {results['max_drawdown']:.1f}%. " +
                              "Cela indique une volatilitÃ© importante du capital.",
                "recommendation": "RÃ©duire la taille des positions ou ajouter un mÃ©canisme de protection du capital."
            })
        if results["sharpe_ratio"] < 1:
            suggestions.append({
                "type": "sharpe_ratio",
                "priority": "medium",
                "title": "Sharpe ratio sous-optimal",
                "description": f"Votre Sharpe ratio est de {results['sharpe_ratio']:.2f}. " +
                              "Le rendement ajustÃ© au risque peut Ãªtre amÃ©liorÃ©.",
                "recommendation": "Optimiser les paramÃ¨tres de la stratÃ©gie pour rÃ©duire la volatilitÃ© des rendements."
            })
        if results["total_trades"] < 10:
            suggestions.append({
                "type": "trades",
                "priority": "medium",
                "title": "Peu de trades",
                "description": f"Seulement {results['total_trades']} trades sur la pÃ©riode. " +
                              "La stratÃ©gie pourrait Ãªtre trop sÃ©lective.",
                "recommendation": "Assouplir les critÃ¨res d'entrÃ©e pour gÃ©nÃ©rer plus d'opportunitÃ©s de trading."
            })
        elif results["total_trades"] > 200:
            suggestions.append({
                "type": "trades",
                "priority": "low",
                "title": "Beaucoup de trades",
                "description": f"{results['total_trades']} trades sur la pÃ©riode. " +
                              "La stratÃ©gie pourrait Ãªtre trop active.",
                "recommendation": "Ajouter des filtres pour rÃ©duire le nombre de trades et amÃ©liorer la qualitÃ©."
            })
        if results["total_return"] < 0:
            suggestions.append({
                "type": "return",
                "priority": "critical",
                "title": "Rendement nÃ©gatif",
                "description": f"La stratÃ©gie a gÃ©nÃ©rÃ© un rendement de {results['total_return']:.1f}%. " +
                              "Elle n'est pas profitable sur cette pÃ©riode.",
                "recommendation": "Revoir complÃ¨tement la stratÃ©gie. ConsidÃ©rez un changement de timeframe, " +
                                "de symboles, ou de paramÃ¨tres de trading."
            })
        elif results["total_return"] > 50:
            suggestions.append({
                "type": "return",
                "priority": "low",
                "title": "Excellent rendement",
                "description": f"La stratÃ©gie a gÃ©nÃ©rÃ© un rendement de {results['total_return']:.1f}%.",
                "recommendation": "VÃ©rifiez que les rÃ©sultats ne sont pas dus Ã  la sur-optimisation. " +
                                "Testez sur d'autres pÃ©riodes pour valider la robustesse."
            })
        if results["total_return"] > 0 and results["sharpe_ratio"] > 1:
            suggestions.append({
                "type": "optimization",
                "priority": "medium",
                "title": "Optimisation des paramÃ¨tres",
                "description": "Votre stratÃ©gie montre des rÃ©sultats prometteurs.",
                "recommendation": "Testez diffÃ©rentes combinaisons de paramÃ¨tres (SMA, RSI, stop loss/take profit) " +
                                "pour trouver la configuration optimale. Utilisez une optimisation par grille ou gÃ©nÃ©tique."
            })
        return suggestions
