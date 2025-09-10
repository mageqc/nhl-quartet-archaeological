"""
INTÉGRATEUR AVANCÉ - APIS OFFICIELLES + BETTING MISE-O-JEU+

Combine les données en temps réel NHL avec notre analyse betting:
- Classements officiels → Tendances betting
- Stats joueurs → Props précises  
- Cotes partenaires → Comparaison value
- Rosters/blessures → Ajustements probabilités
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.scrapers.nhl_api_advanced import NHLAPIAdvanced, create_betting_intelligence_report
from src.analyzers.mise_o_jeu_analyzer import analyze_mise_o_jeu_odds
import json
from datetime import datetime
from typing import Dict, List, Any


class BettingIntelligenceIntegrator:
    """
    Intègre les APIs officielles NHL avec notre système betting
    """
    
    def __init__(self):
        self.nhl_api = NHLAPIAdvanced()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    def get_enhanced_betting_data(self) -> Dict[str, Any]:
        """
        Récupère toutes les données betting enrichies
        """
        print("🚀 RÉCUPÉRATION DONNÉES BETTING ENRICHIES")
        print("=" * 45)
        
        # 1. Rapport d'intelligence de base
        base_report = create_betting_intelligence_report()
        
        # 2. Données spécifiques pour betting
        enhanced_data = {
            'timestamp': self.timestamp,
            'base_intelligence': base_report,
            'betting_enhancements': {}
        }
        
        # 3. Enrichissements betting spécifiques
        print("\n📈 ENRICHISSEMENTS BETTING")
        print("-" * 30)
        
        # Analyse des meneurs pour props
        enhanced_data['betting_enhancements']['prop_analysis'] = self._analyze_player_props()
        
        # Analyse des équipes chaudes/froides
        enhanced_data['betting_enhancements']['team_trends'] = self._analyze_team_trends()
        
        # Cotes comparatives
        enhanced_data['betting_enhancements']['odds_comparison'] = self._analyze_partner_odds()
        
        # Facteurs de blessures/roster
        enhanced_data['betting_enhancements']['roster_impact'] = self._analyze_roster_changes()
        
        return enhanced_data
    
    def _analyze_player_props(self) -> Dict[str, Any]:
        """
        Analyse des props joueurs avec données officielles
        """
        print("🎯 Analyse props joueurs...")
        
        props_analysis = {
            'points_leaders': {},
            'goals_leaders': {},
            'assists_leaders': {},
            'goalie_props': {}
        }
        
        # Top scoreurs pour props points
        points_data = self.nhl_api.get_skater_leaders_current("points", 10)
        if points_data and 'data' in points_data:
            for player in points_data['data']:
                name = player.get('fullName', '')
                points = player.get('points', 0)
                team = player.get('teamAbbrev', '')
                games = player.get('gamesPlayed', 1)
                ppg = round(points / games, 2) if games > 0 else 0
                
                props_analysis['points_leaders'][name] = {
                    'current_points': points,
                    'team': team,
                    'ppg': ppg,
                    'games_played': games,
                    'betting_value': 'HIGH' if ppg > 1.2 else 'MEDIUM' if ppg > 1.0 else 'LOW'
                }
        
        # Top buteurs
        goals_data = self.nhl_api.get_skater_leaders_current("goals", 10)
        if goals_data and 'data' in goals_data:
            for player in goals_data['data']:
                name = player.get('fullName', '')
                goals = player.get('goals', 0)
                team = player.get('teamAbbrev', '')
                games = player.get('gamesPlayed', 1)
                gpg = round(goals / games, 2) if games > 0 else 0
                
                props_analysis['goals_leaders'][name] = {
                    'current_goals': goals,
                    'team': team,
                    'gpg': gpg,
                    'betting_value': 'HIGH' if gpg > 0.6 else 'MEDIUM' if gpg > 0.4 else 'LOW'
                }
        
        # Gardiens pour props Vezina/Wins
        goalie_data = self.nhl_api.get_goalie_leaders_current("wins", 10)
        if goalie_data and 'data' in goalie_data:
            for goalie in goalie_data['data']:
                name = goalie.get('fullName', '')
                wins = goalie.get('wins', 0)
                team = goalie.get('teamAbbrev', '')
                games = goalie.get('gamesPlayed', 1)
                win_pct = round(wins / games, 3) if games > 0 else 0
                
                props_analysis['goalie_props'][name] = {
                    'current_wins': wins,
                    'team': team,
                    'win_percentage': win_pct,
                    'betting_value': 'HIGH' if win_pct > 0.650 else 'MEDIUM' if win_pct > 0.600 else 'LOW'
                }
        
        print(f"   ✅ {len(props_analysis['points_leaders'])} meneurs points analysés")
        print(f"   ✅ {len(props_analysis['goals_leaders'])} meneurs buts analysés")
        print(f"   ✅ {len(props_analysis['goalie_props'])} gardiens analysés")
        
        return props_analysis
    
    def _analyze_team_trends(self) -> Dict[str, Any]:
        """
        Analyse les tendances d'équipes pour betting
        """
        print("📊 Analyse tendances équipes...")
        
        trends = {
            'hot_teams': [],
            'cold_teams': [],
            'value_opportunities': []
        }
        
        # Récupérer les classements pour analyser les tendances
        standings = self.nhl_api.get_current_standings()
        if standings and 'standings' in standings:
            
            # Analyser les équipes chaudes (points par match récents)
            for team_standing in standings['standings']:
                team_name = team_standing.get('teamName', {}).get('default', '')
                team_abbrev = team_standing.get('teamAbbrev', '')
                points = team_standing.get('points', 0)
                games = team_standing.get('gamesPlayed', 1)
                wins = team_standing.get('wins', 0)
                losses = team_standing.get('losses', 0)
                
                points_per_game = round(points / games, 2) if games > 0 else 0
                win_pct = round(wins / (wins + losses), 3) if (wins + losses) > 0 else 0
                
                team_data = {
                    'team': team_name,
                    'abbrev': team_abbrev,
                    'points_per_game': points_per_game,
                    'win_percentage': win_pct,
                    'total_points': points
                }
                
                # Catégoriser
                if points_per_game >= 1.40:  # Équipes très chaudes
                    trends['hot_teams'].append(team_data)
                elif points_per_game <= 1.00:  # Équipes froides
                    trends['cold_teams'].append(team_data)
                
                # Identifier les opportunités de value
                if 1.10 <= points_per_game <= 1.30:  # Équipes moyennes avec potentiel
                    trends['value_opportunities'].append(team_data)
            
            # Trier par performance
            trends['hot_teams'].sort(key=lambda x: x['points_per_game'], reverse=True)
            trends['cold_teams'].sort(key=lambda x: x['points_per_game'])
            trends['value_opportunities'].sort(key=lambda x: x['points_per_game'], reverse=True)
        
        print(f"   🔥 {len(trends['hot_teams'])} équipes chaudes identifiées")
        print(f"   🧊 {len(trends['cold_teams'])} équipes froides identifiées")
        print(f"   💎 {len(trends['value_opportunities'])} opportunités value détectées")
        
        return trends
    
    def _analyze_partner_odds(self) -> Dict[str, Any]:
        """
        Analyse des cotes partenaires officielles
        """
        print("💰 Analyse cotes partenaires...")
        
        odds_analysis = {
            'canada_odds_available': False,
            'us_odds_available': False,
            'comparison_opportunities': []
        }
        
        # Cotes Canada (potentiellement Mise-o-jeu+)
        ca_odds = self.nhl_api.get_partner_odds_ca()
        if ca_odds:
            odds_analysis['canada_odds_available'] = True
            odds_analysis['canada_data'] = ca_odds
            print("   🇨🇦 Cotes Canada récupérées")
        
        # Cotes US pour comparaison
        us_odds = self.nhl_api.get_partner_odds_us()
        if us_odds:
            odds_analysis['us_odds_available'] = True
            odds_analysis['us_data'] = us_odds
            print("   🇺🇸 Cotes US récupérées")
        
        # Analyse comparative si les deux sont disponibles
        if odds_analysis['canada_odds_available'] and odds_analysis['us_odds_available']:
            print("   🔍 Analyse comparative possible")
            # Ici on pourrait comparer les cotes pour identifier des arbitrages
            odds_analysis['arbitrage_possible'] = True
        
        return odds_analysis
    
    def _analyze_roster_changes(self) -> Dict[str, Any]:
        """
        Analyse l'impact des changements de roster
        """
        print("👥 Analyse changements roster...")
        
        roster_impact = {
            'team_analysis': {},
            'key_players_status': [],
            'betting_adjustments': []
        }
        
        # Analyser les rosters des équipes clés
        key_teams = ['TOR', 'MTL', 'EDM', 'BOS', 'NYR', 'VGK', 'DAL', 'COL']
        
        for team in key_teams:
            roster = self.nhl_api.get_team_roster_current(team)
            if roster:
                forwards_count = len(roster.get('forwards', []))
                defensemen_count = len(roster.get('defensemen', []))
                goalies_count = len(roster.get('goalies', []))
                
                roster_impact['team_analysis'][team] = {
                    'forwards': forwards_count,
                    'defensemen': defensemen_count,
                    'goalies': goalies_count,
                    'total_players': forwards_count + defensemen_count + goalies_count,
                    'roster_health': 'GOOD' if forwards_count >= 12 and defensemen_count >= 6 else 'CONCERN'
                }
        
        print(f"   ✅ {len(roster_impact['team_analysis'])} équipes analysées")
        
        return roster_impact
    
    def create_enhanced_betting_report(self, save_file: bool = True) -> Dict[str, Any]:
        """
        Crée un rapport betting enrichi complet
        """
        print("\n🎯 CRÉATION RAPPORT BETTING ENRICHI")
        print("=" * 40)
        
        # Récupérer toutes les données enrichies
        enhanced_data = self.get_enhanced_betting_data()
        
        # Générer des recommandations intégrées
        recommendations = self._generate_integrated_recommendations(enhanced_data)
        enhanced_data['integrated_recommendations'] = recommendations
        
        # Sauvegarder si demandé
        if save_file:
            filename = f"data/enhanced_betting_report_{self.timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, ensure_ascii=False, indent=2, default=str)
            print(f"💾 Rapport sauvegardé: {filename}")
        
        return enhanced_data
    
    def _generate_integrated_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère des recommandations intégrées basées sur toutes les données
        """
        recommendations = {
            'top_props': [],
            'team_bets': [],
            'value_opportunities': [],
            'risk_warnings': []
        }
        
        # Props recommendations basées sur les meneurs
        props_data = data['betting_enhancements']['prop_analysis']
        
        # Top props points
        for name, player_data in props_data['points_leaders'].items():
            if player_data['betting_value'] == 'HIGH':
                recommendations['top_props'].append({
                    'type': 'Points O/U',
                    'player': name,
                    'team': player_data['team'],
                    'current_pace': player_data['ppg'],
                    'confidence': 'HIGH',
                    'reasoning': f"Rythme actuel {player_data['ppg']} pts/match"
                })
        
        # Team bets basées sur les tendances
        trends_data = data['betting_enhancements']['team_trends']
        
        # Équipes chaudes pour ML/spread
        for team_data in trends_data['hot_teams'][:3]:  # Top 3
            recommendations['team_bets'].append({
                'type': 'Moneyline/Spread',
                'team': team_data['team'],
                'trend': 'HOT',
                'ppg': team_data['points_per_game'],
                'confidence': 'HIGH',
                'reasoning': f"Équipe chaude: {team_data['points_per_game']} pts/match"
            })
        
        # Value opportunities
        for team_data in trends_data['value_opportunities'][:2]:  # Top 2
            recommendations['value_opportunities'].append({
                'type': 'Season Props',
                'team': team_data['team'],
                'current_pace': team_data['points_per_game'],
                'reasoning': "Équipe sous-évaluée avec potentiel"
            })
        
        return recommendations


def demo_enhanced_system():
    """
    Démonstration du système enrichi
    """
    print("🚀 DÉMONSTRATION SYSTÈME BETTING ENRICHI")
    print("=" * 45)
    
    integrator = BettingIntelligenceIntegrator()
    
    # Créer le rapport enrichi
    enhanced_report = integrator.create_enhanced_betting_report()
    
    # Afficher un résumé des recommandations
    print("\n🎯 RECOMMANDATIONS INTÉGRÉES")
    print("-" * 30)
    
    recommendations = enhanced_report['integrated_recommendations']
    
    # Top props
    if recommendations['top_props']:
        print("\n⭐ TOP PROPS:")
        for i, prop in enumerate(recommendations['top_props'][:3], 1):
            print(f"   {i}. {prop['type']}: {prop['player']} ({prop['team']})")
            print(f"      Rythme: {prop['current_pace']} | Confiance: {prop['confidence']}")
    
    # Team bets
    if recommendations['team_bets']:
        print("\n🏒 PARIS ÉQUIPES:")
        for i, bet in enumerate(recommendations['team_bets'][:3], 1):
            print(f"   {i}. {bet['type']}: {bet['team']}")
            print(f"      Tendance: {bet['trend']} | PPG: {bet['ppg']}")
    
    # Value opportunities
    if recommendations['value_opportunities']:
        print("\n💎 OPPORTUNITÉS VALUE:")
        for i, opp in enumerate(recommendations['value_opportunities'], 1):
            print(f"   {i}. {opp['type']}: {opp['team']}")
            print(f"      Rythme: {opp['current_pace']}")
    
    print("\n🎯 SYSTÈME ENRICHI OPÉRATIONNEL!")
    print("=" * 35)
    print("✅ APIs officielles intégrées")
    print("✅ Données temps réel")
    print("✅ Recommandations générées")
    print("🚀 Prêt pour betting professionnel!")
    
    return enhanced_report


if __name__ == "__main__":
    # Lancer la démonstration
    demo_enhanced_system()
