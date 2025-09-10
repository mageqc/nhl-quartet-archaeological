"""
Gestionnaire de portefeuille pour optimiser les mises

Ce module gère l'allocation du budget selon différentes stratégies
et génère des recommandations de paris équilibrées.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.calculators.odds_calculator import OddsCalculator


@dataclass
class BetRecommendation:
    """Structure pour une recommandation de pari"""
    market: str
    selection: str
    odds: float
    stake: float
    expected_return: float
    confidence: str  # 'SAFE', 'MID', 'BOLD'
    reasoning: str


class PortfolioManager:
    """
    Gestionnaire pour l'allocation optimale du budget de paris
    """
    
    def __init__(self, budget: float, strategy: str = 'mixed'):
        self.budget = budget
        self.strategy = strategy
        self.odds_calc = OddsCalculator()
        
        # Allocation selon la stratégie
        self.allocations = {
            'safe': {'SAFE': 0.8, 'MID': 0.2, 'BOLD': 0.0},
            'mixed': {'SAFE': 0.5, 'MID': 0.3, 'BOLD': 0.2},
            'bold': {'SAFE': 0.2, 'MID': 0.3, 'BOLD': 0.5}
        }
    
    def generate_recommendations(self, opportunities: List[Dict]) -> List[BetRecommendation]:
        """
        Génère les recommandations finales de paris
        
        Args:
            opportunities (list): Opportunités identifiées par l'analyseur
            
        Returns:
            list: Liste des recommandations avec mises optimales
        """
        if not opportunities:
            # Générer des opportunités d'exemple si aucune fournie
            opportunities = self._get_sample_opportunities()
        
        recommendations = []
        allocation = self.allocations[self.strategy]
        
        # Séparer par catégorie de risque
        safe_bets = [op for op in opportunities if op['confidence'] == 'SAFE']
        mid_bets = [op for op in opportunities if op['confidence'] == 'MID']
        bold_bets = [op for op in opportunities if op['confidence'] == 'BOLD']
        
        # Allouer le budget
        safe_budget = self.budget * allocation['SAFE']
        mid_budget = self.budget * allocation['MID']
        bold_budget = self.budget * allocation['BOLD']
        
        # Créer les recommandations pour chaque catégorie
        recommendations.extend(self._allocate_category_budget(safe_bets, safe_budget, 'SAFE'))
        recommendations.extend(self._allocate_category_budget(mid_bets, mid_budget, 'MID'))
        recommendations.extend(self._allocate_category_budget(bold_bets, bold_budget, 'BOLD'))
        
        return recommendations
    
    def _allocate_category_budget(self, bets: List[Dict], budget: float, 
                                 category: str) -> List[BetRecommendation]:
        """
        Alloue le budget pour une catégorie de paris
        """
        if not bets or budget <= 0:
            return []
        
        recommendations = []
        
        # Trier par valeur décroissante
        sorted_bets = sorted(bets, key=lambda x: x['value'], reverse=True)
        
        # Prendre les meilleurs paris selon la catégorie
        if category == 'SAFE':
            selected_bets = sorted_bets[:2]  # 2 paris sûrs max
        elif category == 'MID':
            selected_bets = sorted_bets[:3]  # 3 paris moyens max
        else:  # BOLD
            selected_bets = sorted_bets[:2]  # 2 longshots max
        
        # Distribuer le budget équitablement
        if selected_bets:
            stake_per_bet = budget / len(selected_bets)
            
            for bet in selected_bets:
                # Ajuster la mise avec Kelly si value très élevée
                if bet['value'] > 0.1:  # Value > 10%
                    kelly_stake = self.odds_calc.kelly_criterion(
                        bet['odds'], bet['adjusted_prob'], budget
                    )
                    stake = min(stake_per_bet, kelly_stake)
                else:
                    stake = stake_per_bet
                
                expected_return = self.odds_calc.calculate_expected_value(
                    bet['odds'], bet['adjusted_prob'], stake
                )
                
                recommendation = BetRecommendation(
                    market=bet['market'],
                    selection=bet['selection'],
                    odds=bet['odds'],
                    stake=round(stake, 2),
                    expected_return=round(expected_return, 2),
                    confidence=category,
                    reasoning=bet['reasoning']
                )
                
                recommendations.append(recommendation)
        
        return recommendations
    
    def display_recommendations(self, recommendations: List[BetRecommendation]):
        """
        Affiche les recommandations de manière formatée
        """
        if not recommendations:
            print("❌ Aucune recommandation générée")
            return
        
        total_stake = sum(rec.stake for rec in recommendations)
        total_expected = sum(rec.expected_return for rec in recommendations)
        
        print(f"💰 BUDGET TOTAL: {self.budget}$ | MISÉ: {total_stake:.2f}$")
        print(f"📈 VALEUR ATTENDUE: {total_expected:.2f}$")
        print(f"📊 ROI ATTENDU: {(total_expected/total_stake)*100:.1f}%")
        print()
        
        # Grouper par catégorie
        for category in ['SAFE', 'MID', 'BOLD']:
            category_recs = [r for r in recommendations if r.confidence == category]
            if not category_recs:
                continue
            
            print(f"🎯 {category} ({len(category_recs)} paris)")
            print("-" * 40)
            
            for rec in category_recs:
                potential_win = rec.stake * (rec.odds - 1)
                roi = (potential_win / rec.stake) * 100
                
                print(f"🏒 {rec.market}: {rec.selection}")
                print(f"   Cote: {rec.odds:.2f} | Mise: {rec.stake:.2f}$")
                print(f"   Gain potentiel: {potential_win:.2f}$ ({roi:.0f}%)")
                print(f"   💡 {rec.reasoning}")
                print()
    
    def _get_sample_opportunities(self) -> List[Dict]:
        """
        Génère des opportunités d'exemple pour la démonstration
        """
        return [
            {
                'market': 'Vainqueur Division Atlantique',
                'selection': 'Toronto Maple Leafs',
                'odds': 3.50,
                'implied_prob': 0.286,
                'adjusted_prob': 0.35,
                'value': 0.064,
                'confidence': 'SAFE',
                'reasoning': 'Roster amélioré, cotes sous-évaluées'
            },
            {
                'market': 'Plus de points (saison)',
                'selection': 'Connor McDavid O 140.5',
                'odds': 1.90,
                'implied_prob': 0.526,
                'adjusted_prob': 0.65,
                'value': 0.124,
                'confidence': 'MID',
                'reasoning': 'Santé confirmée, ligne offensive renforcée'
            },
            {
                'market': 'Coupe Stanley',
                'selection': 'Seattle Kraken',
                'odds': 25.00,
                'implied_prob': 0.040,
                'adjusted_prob': 0.08,
                'value': 0.040,
                'confidence': 'BOLD',
                'reasoning': 'Progression constante, roster jeune et affamé'
            },
            {
                'market': 'Rookie de l\'année',
                'selection': 'Macklin Celebrini',
                'odds': 4.25,
                'implied_prob': 0.235,
                'adjusted_prob': 0.30,
                'value': 0.065,
                'confidence': 'MID',
                'reasoning': '1er choix, opportunité immédiate à San Jose'
            },
            {
                'market': 'Plus de buts (saison)',
                'selection': 'Cole Caufield O 35.5',
                'odds': 2.10,
                'implied_prob': 0.476,
                'adjusted_prob': 0.55,
                'value': 0.074,
                'confidence': 'SAFE',
                'reasoning': 'Progression naturelle, meilleur jeu de puissance'
            }
        ]
