"""
Calculateur de cotes et probabilités pour Mise-o-jeu+

Ce module effectue tous les calculs liés aux cotes:
- Conversion cotes décimales ↔ probabilités implicites
- Calcul de value betting
- Ajustements basés sur les nouvelles et statistiques
"""

import math
from typing import Dict, List, Tuple


class OddsCalculator:
    """
    Calculateur avancé pour l'analyse des cotes de paris
    """
    
    def __init__(self):
        self.vig_rate = 0.05  # Commission typique Mise-o-jeu+ (~5%)
    
    def decimal_to_implied_prob(self, decimal_odds: float) -> float:
        """
        Convertit cotes décimales en probabilité implicite
        
        Args:
            decimal_odds (float): Cote décimale (ex: 2.50)
            
        Returns:
            float: Probabilité implicite (0.0 à 1.0)
        """
        if decimal_odds <= 1.0:
            raise ValueError("Les cotes décimales doivent être > 1.0")
        
        return 1.0 / decimal_odds
    
    def implied_prob_to_decimal(self, probability: float) -> float:
        """
        Convertit probabilité en cotes décimales
        
        Args:
            probability (float): Probabilité (0.0 à 1.0)
            
        Returns:
            float: Cotes décimales
        """
        if probability <= 0 or probability >= 1:
            raise ValueError("La probabilité doit être entre 0 et 1")
        
        return 1.0 / probability
    
    def calculate_value(self, decimal_odds: float, true_probability: float) -> float:
        """
        Calcule la valeur d'un pari (value betting)
        
        Args:
            decimal_odds (float): Cote offerte
            true_probability (float): Probabilité estimée réelle
            
        Returns:
            float: Valeur du pari (positif = value bet)
        """
        implied_prob = self.decimal_to_implied_prob(decimal_odds)
        return true_probability - implied_prob
    
    def adjust_probability_for_news(self, base_prob: float, news_impact: float, 
                                   impact_direction: str) -> float:
        """
        Ajuste la probabilité basée sur l'impact des nouvelles
        
        Args:
            base_prob (float): Probabilité de base
            news_impact (float): Force de l'impact (0.0 à 1.0)
            impact_direction (str): 'positive' ou 'negative'
            
        Returns:
            float: Probabilité ajustée
        """
        adjustment = news_impact * 0.1  # Maximum 10% d'ajustement
        
        if impact_direction == 'positive':
            adjusted = base_prob + adjustment
        else:
            adjusted = base_prob - adjustment
        
        # S'assurer que la probabilité reste dans les limites
        return max(0.01, min(0.99, adjusted))
    
    def remove_vig(self, odds_list: List[float]) -> List[float]:
        """
        Supprime la commission (vig) d'un ensemble de cotes
        
        Args:
            odds_list (list): Liste des cotes décimales
            
        Returns:
            list: Cotes ajustées sans commission
        """
        # Calculer les probabilités implicites
        implied_probs = [self.decimal_to_implied_prob(odds) for odds in odds_list]
        
        # La somme des probabilités > 1.0 indique la commission
        total_prob = sum(implied_probs)
        
        if total_prob <= 1.0:
            return odds_list  # Pas de commission détectée
        
        # Normaliser pour supprimer la commission
        fair_probs = [prob / total_prob for prob in implied_probs]
        
        # Reconvertir en cotes
        return [self.implied_prob_to_decimal(prob) for prob in fair_probs]
    
    def kelly_criterion(self, decimal_odds: float, win_probability: float, 
                       bankroll: float) -> float:
        """
        Calcule la mise optimale selon le critère de Kelly
        
        Args:
            decimal_odds (float): Cotes du pari
            win_probability (float): Probabilité de gain
            bankroll (float): Capital disponible
            
        Returns:
            float: Mise recommandée
        """
        # Kelly = (bp - q) / b
        # b = cotes - 1, p = probabilité de gain, q = probabilité de perte
        b = decimal_odds - 1
        p = win_probability
        q = 1 - p
        
        if p * b <= q:
            return 0.0  # Pas de value, ne pas parier
        
        kelly_fraction = (b * p - q) / b
        
        # Limiter à 25% max du bankroll pour la sécurité
        kelly_fraction = min(kelly_fraction, 0.25)
        
        return kelly_fraction * bankroll
    
    def calculate_expected_value(self, decimal_odds: float, win_probability: float, 
                               stake: float) -> float:
        """
        Calcule la valeur attendue d'un pari
        
        Args:
            decimal_odds (float): Cotes du pari
            win_probability (float): Probabilité de gain
            stake (float): Mise
            
        Returns:
            float: Valeur attendue (gain/perte moyen)
        """
        potential_win = stake * (decimal_odds - 1)
        potential_loss = -stake
        
        expected_value = (win_probability * potential_win + 
                         (1 - win_probability) * potential_loss)
        
        return expected_value
