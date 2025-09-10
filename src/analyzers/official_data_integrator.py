"""
Intégration du calendrier officiel NHL dans l'analyse Mise-o-jeu+

Ce module utilise les données officielles pour enrichir l'analyse des paris.
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from src.scrapers.official_schedule_scraper import get_official_nhl_schedule


class NHLOfficialDataIntegrator:
    """
    Intègre les données officielles NHL dans l'analyse de paris
    """
    
    def __init__(self):
        self.official_schedule = None
        self.load_official_data()
    
    def load_official_data(self):
        """Charge les données officielles (local ou récupération)"""
        
        # Chercher le fichier le plus récent
        data_files = [f for f in os.listdir('data') if f.startswith('nhl_official_schedule_')]
        
        if data_files:
            # Prendre le plus récent
            latest_file = max(data_files)
            file_path = f'data/{latest_file}'
            
            print(f"📁 Chargement calendrier officiel: {latest_file}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.official_schedule = json.load(f)
        else:
            print("📡 Récupération nouveau calendrier officiel...")
            self.official_schedule = get_official_nhl_schedule()
    
    def get_opening_games_for_betting(self) -> List[Dict]:
        """
        Récupère les matchs d'ouverture officiels pour les paris
        
        Returns:
            list: Matchs d'ouverture avec détails pour paris
        """
        if not self.official_schedule:
            return []
        
        opening_games = self.official_schedule.get('opening_games', [])
        
        # Enrichir avec des informations utiles pour les paris
        betting_games = []
        for game in opening_games:
            betting_game = {
                'game_id': game['game_id'],
                'date': game['date'],
                'time': game['time'],
                'away_team': game['away_team'],
                'home_team': game['home_team'],
                'venue': game['venue'],
                'betting_interest': self._assess_betting_interest(game),
                'rivalry_level': self._assess_rivalry(game['away_team'], game['home_team']),
                'tv_coverage': len(game.get('tv_broadcasts', [])),
                'prime_time': self._is_prime_time(game['time']),
                'market_importance': self._assess_market_importance(game)
            }
            betting_games.append(betting_game)
        
        # Trier par intérêt pour les paris
        betting_games.sort(key=lambda x: x['betting_interest'], reverse=True)
        
        return betting_games
    
    def get_team_schedule(self, team_name: str) -> List[Dict]:
        """Récupère le calendrier officiel d'une équipe"""
        if not self.official_schedule:
            return []
        
        return self.official_schedule.get('by_team', {}).get(team_name, [])
    
    def get_games_by_date(self, date_str: str) -> List[Dict]:
        """Récupère tous les matchs officiels pour une date"""
        if not self.official_schedule:
            return []
        
        return self.official_schedule.get('by_date', {}).get(date_str, [])
    
    def get_monthly_games(self, month_str: str) -> List[Dict]:
        """Récupère les matchs d'un mois (format: YYYY-MM)"""
        if not self.official_schedule:
            return []
        
        return self.official_schedule.get('by_month', {}).get(month_str, [])
    
    def get_stats_summary(self) -> Dict:
        """Retourne un résumé statistique du calendrier"""
        if not self.official_schedule:
            return {}
        
        return {
            'total_games': self.official_schedule['total_games'],
            'by_type': {
                'preseason': len(self.official_schedule['by_game_type']['preseason']),
                'regular': len(self.official_schedule['by_game_type']['regular']),
                'playoffs': len(self.official_schedule['by_game_type']['playoffs'])
            },
            'opening_games_count': len(self.official_schedule.get('opening_games', [])),
            'teams_count': self.official_schedule['statistics']['total_teams'],
            'date_range': self.official_schedule['statistics']['date_range']
        }
    
    def _assess_betting_interest(self, game: Dict) -> int:
        """Évalue l'intérêt d'un match pour les paris (1-10)"""
        score = 5  # Base
        
        # Facteurs qui augmentent l'intérêt
        away_team = game['away_team']
        home_team = game['home_team']
        
        # Grandes équipes = plus d'intérêt
        big_markets = ['Toronto Maple Leafs', 'Montreal Canadiens', 'Boston Bruins', 
                      'New York Rangers', 'Edmonton Oilers', 'Calgary Flames']
        
        if away_team in big_markets or home_team in big_markets:
            score += 2
        
        # Rivalités connues
        rivalries = [
            ('Toronto Maple Leafs', 'Montreal Canadiens'),
            ('Boston Bruins', 'Montreal Canadiens'),
            ('Edmonton Oilers', 'Calgary Flames'),
            ('New York Rangers', 'New York Islanders')
        ]
        
        for team1, team2 in rivalries:
            if (away_team == team1 and home_team == team2) or (away_team == team2 and home_team == team1):
                score += 3
                break
        
        # Couverture TV
        tv_count = len(game.get('tv_broadcasts', []))
        if tv_count > 2:
            score += 1
        
        return min(10, score)
    
    def _assess_rivalry(self, away_team: str, home_team: str) -> str:
        """Évalue le niveau de rivalité"""
        intense_rivalries = [
            ('Toronto Maple Leafs', 'Montreal Canadiens'),
            ('Boston Bruins', 'Montreal Canadiens'),
            ('Edmonton Oilers', 'Calgary Flames')
        ]
        
        moderate_rivalries = [
            ('New York Rangers', 'New York Islanders'),
            ('Pittsburgh Penguins', 'Philadelphia Flyers'),
            ('Detroit Red Wings', 'Toronto Maple Leafs')
        ]
        
        for team1, team2 in intense_rivalries:
            if (away_team == team1 and home_team == team2) or (away_team == team2 and home_team == team1):
                return 'INTENSE'
        
        for team1, team2 in moderate_rivalries:
            if (away_team == team1 and home_team == team2) or (away_team == team2 and home_team == team1):
                return 'MODERATE'
        
        return 'REGULAR'
    
    def _is_prime_time(self, time_str: str) -> bool:
        """Détermine si c'est en prime time"""
        try:
            # Extraire l'heure (format ISO)
            if 'T' in time_str:
                time_part = time_str.split('T')[1]
                hour = int(time_part.split(':')[0])
                # Prime time: 19h-22h local
                return 19 <= hour <= 22
        except:
            pass
        return False
    
    def _assess_market_importance(self, game: Dict) -> str:
        """Évalue l'importance du marché"""
        away_team = game['away_team']
        home_team = game['home_team']
        
        major_markets = ['Toronto Maple Leafs', 'Montreal Canadiens', 'New York Rangers', 
                        'Boston Bruins', 'Chicago Blackhawks', 'Detroit Red Wings']
        
        if away_team in major_markets and home_team in major_markets:
            return 'MAJOR'
        elif away_team in major_markets or home_team in major_markets:
            return 'SIGNIFICANT'
        else:
            return 'STANDARD'
    
    def display_betting_schedule_summary(self):
        """Affiche un résumé orienté paris"""
        if not self.official_schedule:
            print("❌ Aucune donnée officielle chargée")
            return
        
        stats = self.get_stats_summary()
        opening_games = self.get_opening_games_for_betting()
        
        print("🏒 CALENDRIER OFFICIEL NHL - ANALYSE PARIS")
        print("=" * 50)
        print(f"📊 Total matchs: {stats['total_games']}")
        print(f"📅 Saison régulière: {stats['by_type']['regular']} matchs")
        print(f"🎯 Matchs d'ouverture: {stats['opening_games_count']} matchs")
        print()
        
        print("🔥 TOP MATCHS D'OUVERTURE POUR PARIS:")
        for i, game in enumerate(opening_games[:5], 1):
            rivalry = "🥊" if game['rivalry_level'] == 'INTENSE' else ("⚔️" if game['rivalry_level'] == 'MODERATE' else "🏒")
            prime = "⭐" if game['prime_time'] else "📺"
            
            print(f"{i}. {rivalry} {prime} {game['date']} - {game['away_team']} @ {game['home_team']}")
            print(f"   Intérêt paris: {game['betting_interest']}/10 | Marché: {game['market_importance']}")
        
        print(f"\n📱 Utilise ces matchs pour ton analyse Mise-o-jeu+!")


# Fonction utilitaire
def get_betting_schedule_data() -> Dict:
    """
    Point d'entrée pour récupérer les données de calendrier pour les paris
    
    Returns:
        dict: Données complètes pour l'analyse de paris
    """
    integrator = NHLOfficialDataIntegrator()
    
    return {
        'opening_games': integrator.get_opening_games_for_betting(),
        'stats': integrator.get_stats_summary(),
        'full_schedule': integrator.official_schedule
    }
