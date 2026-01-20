import numpy as np
from typing import Dict, List

class StrategyOptimizer:
    def analyze_and_suggest(self, results: Dict) -> List[Dict]:
        suggestions = []
        if results["win_rate"] < 40:
            suggestions.append({
                "type": "win_rate",
                "priority": "high",
                "title": "Taux de réussite faible",
                "description": f"Votre stratégie a un taux de réussite de {results['win_rate']:.1f}%. " +
                              "Considérez d'ajuster vos critères d'entrée ou d'utiliser un filtre de tendance.",
                "recommendation": "Augmenter les seuils RSI (oversold > 25, overbought < 75) ou ajouter un filtre de tendance avec une moyenne mobile plus longue."
            })
        elif results["win_rate"] > 60:
            suggestions.append({
                "type": "win_rate",
                "priority": "low",
                "title": "Excellent taux de réussite",
                "description": f"Votre stratégie a un taux de réussite de {results['win_rate']:.1f}%.",
                "recommendation": "Vous pourriez augmenter légèrement la taille des positions pour maximiser les profits."
            })
        if results["profit_factor"] < 1.2:
            suggestions.append({
                "type": "profit_factor",
                "priority": "high",
                "title": "Profit factor faible",
                "description": f"Votre profit factor est de {results['profit_factor']:.2f}. " +
                              "Les pertes moyennes sont trop importantes par rapport aux gains.",
                "recommendation": "Réduire le stop loss ou augmenter le take profit pour améliorer le ratio risque/récompense."
            })
        if results["max_drawdown"] > 30:
            suggestions.append({
                "type": "drawdown",
                "priority": "high",
                "title": "Drawdown maximum élevé",
                "description": f"Votre drawdown maximum est de {results['max_drawdown']:.1f}%. " +
                              "Cela indique une volatilité importante du capital.",
                "recommendation": "Réduire la taille des positions ou ajouter un mécanisme de protection du capital."
            })
        if results["sharpe_ratio"] < 1:
            suggestions.append({
                "type": "sharpe_ratio",
                "priority": "medium",
                "title": "Sharpe ratio sous-optimal",
                "description": f"Votre Sharpe ratio est de {results['sharpe_ratio']:.2f}. " +
                              "Le rendement ajusté au risque peut être amélioré.",
                "recommendation": "Optimiser les paramètres de la stratégie pour réduire la volatilité des rendements."
            })
        if results["total_trades"] < 10:
            suggestions.append({
                "type": "trades",
                "priority": "medium",
                "title": "Peu de trades",
                "description": f"Seulement {results['total_trades']} trades sur la période. " +
                              "La stratégie pourrait être trop sélective.",
                "recommendation": "Assouplir les critères d'entrée pour générer plus d'opportunités de trading."
            })
        elif results["total_trades"] > 200:
            suggestions.append({
                "type": "trades",
                "priority": "low",
                "title": "Beaucoup de trades",
                "description": f"{results['total_trades']} trades sur la période. " +
                              "La stratégie pourrait être trop active.",
                "recommendation": "Ajouter des filtres pour réduire le nombre de trades et améliorer la qualité."
            })
        if results["total_return"] < 0:
            suggestions.append({
                "type": "return",
                "priority": "critical",
                "title": "Rendement négatif",
                "description": f"La stratégie a généré un rendement de {results['total_return']:.1f}%. " +
                              "Elle n'est pas profitable sur cette période.",
                "recommendation": "Revoir complètement la stratégie. Considérez un changement de timeframe, " +
                                "de symboles, ou de paramètres de trading."
            })
        elif results["total_return"] > 50:
            suggestions.append({
                "type": "return",
                "priority": "low",
                "title": "Excellent rendement",
                "description": f"La stratégie a généré un rendement de {results['total_return']:.1f}%.",
                "recommendation": "Vérifiez que les résultats ne sont pas dus à la sur-optimisation. " +
                                "Testez sur d'autres périodes pour valider la robustesse."
            })
        if results["total_return"] > 0 and results["sharpe_ratio"] > 1:
            suggestions.append({
                "type": "optimization",
                "priority": "medium",
                "title": "Optimisation des paramètres",
                "description": "Votre stratégie montre des résultats prometteurs.",
                "recommendation": "Testez différentes combinaisons de paramètres (SMA, RSI, stop loss/take profit) " +
                                "pour trouver la configuration optimale. Utilisez une optimisation par grille ou génétique."
            })
        return suggestions
