"""
Analyseur de valeur pour identifier les meilleures opportunités de paris

Ce module combine les données de nouvelles, statistiques et cotes
pour identifier les paris avec la meilleure valeur attendue.
"""

from typing import Dict, List
from src.scrapers.news_scraper import NHLNewsScraper
from src.calculators.odds_calculator import OddsCalculator


class ValueAnalyzer:
    """
    Analyseur principal pour identifier les opportunités de value betting
    """
    
    def __init__(self):
        self.news_scraper = NHLNewsScraper()
        self.odds_calc = OddsCalculator()
        
        # Base de données des équipes et statistiques
        self.team_stats = self._load_team_stats()
        self.player_stats = self._load_player_stats()
    
    def find_value_bets(self) -> List[Dict]:
        """
        Identifie toutes les opportunités de value betting
        
        Returns:
            list: Liste des opportunités triées par valeur
        """
        opportunities = []
        
        # Analyser différents types de marchés
        opportunities.extend(self._analyze_division_winners())
        opportunities.extend(self._analyze_player_props())
        opportunities.extend(self._analyze_stanley_cup())
        opportunities.extend(self._analyze_awards())
        
        # Trier par valeur décroissante
        opportunities.sort(key=lambda x: x['value'], reverse=True)
        
        return opportunities
    
    def _analyze_division_winners(self) -> List[Dict]:
        """Analyse les marchés de vainqueurs de division"""
        opportunities = []
        
        # Données d'exemple pour les divisions
        division_odds = {
            'Atlantique': {
                'Toronto Maple Leafs': 3.50,
                'Florida Panthers': 4.00,
                'Boston Bruins': 4.50,
                'Tampa Bay Lightning': 5.00
            },
            'Métropolitaine': {
                'New York Rangers': 3.25,
                'Carolina Hurricanes': 3.75,
                'New Jersey Devils': 4.25,
                'Philadelphia Flyers': 8.00
            }
        }
        
        for division, teams in division_odds.items():
            for team, odds in teams.items():
                # Calculs basiques de probabilité
                implied_prob = self.odds_calc.decimal_to_implied_prob(odds)
                
                # Ajustement basé sur les nouvelles et stats
                team_code = self._get_team_code(team)
                news_impact = self.news_scraper.get_team_impact_score(team_code)
                base_prob = self._get_team_base_probability(team, division)
                
                adjusted_prob = self.odds_calc.adjust_probability_for_news(
                    base_prob, news_impact, 'positive' if news_impact > 0.5 else 'negative'
                )
                
                value = self.odds_calc.calculate_value(odds, adjusted_prob)
                
                if value > 0.02:  # Seuil minimum de 2% de valeur
                    confidence = self._determine_confidence_level(value, odds)
                    
                    opportunities.append({
                        'market': f'Vainqueur Division {division}',
                        'selection': team,
                        'odds': odds,
                        'implied_prob': implied_prob,
                        'adjusted_prob': adjusted_prob,
                        'value': value,
                        'confidence': confidence,
                        'reasoning': self._generate_reasoning(team, value, news_impact)
                    })
        
        return opportunities
    
    def _analyze_player_props(self) -> List[Dict]:
        """Analyse les props de joueurs (buts, points, etc.)"""
        opportunities = []
        
        # Props d'exemple
        player_props = {
            'Connor McDavid Points O/U 140.5': {'over': 1.90, 'under': 1.90},
            'Cole Caufield Buts O/U 35.5': {'over': 2.10, 'under': 1.75},
            'Erik Karlsson Points O/U 85.5': {'over': 2.25, 'under': 1.65}
        }
        
        for prop, odds_dict in player_props.items():
            for selection, odds in odds_dict.items():
                player_name = prop.split()[0] + " " + prop.split()[1]
                
                implied_prob = self.odds_calc.decimal_to_implied_prob(odds)
                base_prob = self._get_player_base_probability(player_name, prop, selection)
                
                # Ajustement minimal pour les props de joueurs
                adjusted_prob = base_prob * 1.02  # Léger ajustement
                
                value = self.odds_calc.calculate_value(odds, adjusted_prob)
                
                if value > 0.01:
                    confidence = self._determine_confidence_level(value, odds)
                    
                    opportunities.append({
                        'market': prop,
                        'selection': f'{player_name} {selection}',
                        'odds': odds,
                        'implied_prob': implied_prob,
                        'adjusted_prob': adjusted_prob,
                        'value': value,
                        'confidence': confidence,
                        'reasoning': self._generate_player_reasoning(player_name, selection)
                    })
        
        return opportunities
    
    def _analyze_stanley_cup(self) -> List[Dict]:
        """Analyse les cotes de la Coupe Stanley"""
        stanley_cup_odds = {
            'Edmonton Oilers': 6.50,
            'Toronto Maple Leafs': 8.00,
            'Colorado Avalanche': 9.00,
            'Seattle Kraken': 25.00,
            'Montreal Canadiens': 50.00
        }
        
        opportunities = []
        
        for team, odds in stanley_cup_odds.items():
            implied_prob = self.odds_calc.decimal_to_implied_prob(odds)
            base_prob = self._get_stanley_cup_probability(team)
            
            value = self.odds_calc.calculate_value(odds, base_prob)
            
            if value > 0.005:  # Seuil plus bas pour la Coupe Stanley
                confidence = 'BOLD' if odds > 15.0 else ('MID' if odds > 8.0 else 'SAFE')
                
                opportunities.append({
                    'market': 'Coupe Stanley',
                    'selection': team,
                    'odds': odds,
                    'implied_prob': implied_prob,
                    'adjusted_prob': base_prob,
                    'value': value,
                    'confidence': confidence,
                    'reasoning': f'Analyse approfondie suggère {base_prob*100:.1f}% vs {implied_prob*100:.1f}% implicite'
                })
        
        return opportunities
    
    def _analyze_awards(self) -> List[Dict]:
        """Analyse les trophées individuels"""
        awards_odds = {
            'Hart Trophy': {
                'Connor McDavid': 3.50,
                'Nathan MacKinnon': 5.00,
                'Auston Matthews': 6.00
            },
            'Calder Trophy': {
                'Macklin Celebrini': 4.25,
                'Matvei Michkov': 5.50,
                'Logan Cooley': 8.00
            }
        }
        
        opportunities = []
        
        for award, candidates in awards_odds.items():
            for player, odds in candidates.items():
                implied_prob = self.odds_calc.decimal_to_implied_prob(odds)
                base_prob = self._get_award_probability(player, award)
                
                value = self.odds_calc.calculate_value(odds, base_prob)
                
                if value > 0.01:
                    confidence = self._determine_confidence_level(value, odds)
                    
                    opportunities.append({
                        'market': award,
                        'selection': player,
                        'odds': odds,
                        'implied_prob': implied_prob,
                        'adjusted_prob': base_prob,
                        'value': value,
                        'confidence': confidence,
                        'reasoning': f'Contexte favorable pour {award.split()[0]}'
                    })
        
        return opportunities
    
    def _determine_confidence_level(self, value: float, odds: float) -> str:
        """Détermine le niveau de confiance du pari"""
        if odds < 2.0 and value > 0.05:
            return 'SAFE'
        elif odds > 10.0:
            return 'BOLD'
        else:
            return 'MID'
    
    def _generate_reasoning(self, team: str, value: float, news_impact: float) -> str:
        """Génère une justification pour la recommandation"""
        reasons = []
        
        if value > 0.1:
            reasons.append("Valeur exceptionnelle détectée")
        elif value > 0.05:
            reasons.append("Bonne opportunité de valeur")
        
        if news_impact > 0.5:
            reasons.append("Impact positif des nouvelles récentes")
        
        if not reasons:
            reasons.append("Analyse statistique favorable")
        
        return ", ".join(reasons)
    
    def _generate_player_reasoning(self, player: str, selection: str) -> str:
        """Génère une justification pour les props de joueurs"""
        if 'McDavid' in player:
            return "Santé confirmée, ligne offensive renforcée"
        elif 'Caufield' in player:
            return "Progression naturelle, meilleur jeu de puissance"
        else:
            return "Analyse des tendances favorable"
    
    # Méthodes utilitaires pour les probabilités de base
    def _get_team_code(self, team_name: str) -> str:
        """Convertit nom d'équipe en code"""
        codes = {
            'Toronto Maple Leafs': 'TOR',
            'Edmonton Oilers': 'EDM',
            'Montreal Canadiens': 'MTL',
            'Winnipeg Jets': 'WPG'
        }
        return codes.get(team_name, 'UNK')
    
    def _get_team_base_probability(self, team: str, division: str) -> float:
        """Probabilité de base pour gagner la division"""
        base_probs = {
            'Toronto Maple Leafs': 0.35,
            'Edmonton Oilers': 0.40,
            'Florida Panthers': 0.25,
            'Boston Bruins': 0.22
        }
        return base_probs.get(team, 0.15)
    
    def _get_player_base_probability(self, player: str, prop: str, selection: str) -> float:
        """Probabilité de base pour les props de joueurs"""
        if 'McDavid' in player and 'over' in selection:
            return 0.65
        elif 'Caufield' in player and 'over' in selection:
            return 0.55
        else:
            return 0.52
    
    def _get_stanley_cup_probability(self, team: str) -> float:
        """Probabilité de base pour la Coupe Stanley"""
        probs = {
            'Edmonton Oilers': 0.18,
            'Toronto Maple Leafs': 0.14,
            'Seattle Kraken': 0.08,
            'Montreal Canadiens': 0.03
        }
        return probs.get(team, 0.05)
    
    def _get_award_probability(self, player: str, award: str) -> float:
        """Probabilité de base pour les trophées"""
        if 'McDavid' in player and 'Hart' in award:
            return 0.32
        elif 'Celebrini' in player and 'Calder' in award:
            return 0.30
        else:
            return 0.20
    
    def _load_team_stats(self) -> Dict:
        """Charge les statistiques d'équipe (placeholder)"""
        return {}
    
    def _load_player_stats(self) -> Dict:
        """Charge les statistiques de joueurs (placeholder)"""
        return {}
