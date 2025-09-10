"""
SYSTÈME AVANCÉ NHL API - DONNÉES EN TEMPS RÉEL

Intégration complète des APIs officielles NHL:
- api-web.nhle.com (données de base)
- api.nhle.com/stats/rest (statistiques avancées)

Nouvelles capacités pour notre analyseur betting:
✅ Standings en temps réel
✅ Statistiques joueurs actuelles  
✅ Cotes partenaires officielles
✅ Rosters et blessures
✅ Scores et résultats live
"""

import subprocess
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union


class NHLAPIAdvanced:
    """
    Interface avancée pour les APIs officielles NHL
    """
    
    def __init__(self):
        self.base_web_api = "https://api-web.nhle.com"
        self.base_stats_api = "https://api.nhle.com/stats/rest"
        self.season_current = "20252026"  # Format YYYYYYYY
        self.use_curl = True  # Utiliser curl comme avant pour éviter les problèmes requests
    
    def _make_api_call(self, url: str) -> Optional[Dict]:
        """
        Appel API avec curl pour compatibilité maximale
        """
        try:
            if self.use_curl:
                result = subprocess.run([
                    'curl', '-s', '-L', url
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    return json.loads(result.stdout)
            else:
                # Fallback vers requests - désactivé pour éviter les dépendances
                print(f"⚠️ Requests non disponible pour {url}")
                return None
                    
        except Exception as e:
            print(f"⚠️ Erreur API call {url}: {e}")
        return None
    
    # === STANDINGS & CLASSEMENTS ===
    
    def get_current_standings(self) -> Optional[Dict]:
        """
        Classements actuels - CRUCIAL pour betting
        """
        url = f"{self.base_web_api}/v1/standings/now"
        return self._make_api_call(url)
    
    def get_standings_by_date(self, date: str) -> Optional[Dict]:
        """
        Classements à une date spécifique (format: YYYY-MM-DD)
        """
        url = f"{self.base_web_api}/v1/standings/{date}"
        return self._make_api_call(url)
    
    # === STATISTIQUES ÉQUIPES ===
    
    def get_team_stats_current(self, team_code: str) -> Optional[Dict]:
        """
        Stats actuelles d'une équipe (ex: "TOR", "MTL", "EDM")
        """
        url = f"{self.base_web_api}/v1/club-stats/{team_code}/now"
        return self._make_api_call(url)
    
    def get_team_roster_current(self, team_code: str) -> Optional[Dict]:
        """
        Roster actuel - important pour blessures/changements
        """
        url = f"{self.base_web_api}/v1/roster/{team_code}/current"
        return self._make_api_call(url)
    
    def get_team_schedule_current(self, team_code: str) -> Optional[Dict]:
        """
        Calendrier d'équipe pour la saison
        """
        url = f"{self.base_web_api}/v1/club-schedule-season/{team_code}/now"
        return self._make_api_call(url)
    
    # === STATISTIQUES JOUEURS ===
    
    def get_skater_leaders_current(self, categories: str = "points", limit: int = 10) -> Optional[Dict]:
        """
        Meneurs actuels - crucial pour props betting
        Categories: points, goals, assists, gamesPlayed, etc.
        """
        url = f"{self.base_web_api}/v1/skater-stats-leaders/current?categories={categories}&limit={limit}"
        return self._make_api_call(url)
    
    def get_goalie_leaders_current(self, categories: str = "wins", limit: int = 10) -> Optional[Dict]:
        """
        Meneurs gardiens - pour props Vezina/wins
        Categories: wins, gaa, savePercentage, shutouts, etc.
        """
        url = f"{self.base_web_api}/v1/goalie-stats-leaders/current?categories={categories}&limit={limit}"
        return self._make_api_call(url)
    
    def get_player_info(self, player_id: int) -> Optional[Dict]:
        """
        Info détaillée d'un joueur spécifique
        """
        url = f"{self.base_web_api}/v1/player/{player_id}/landing"
        return self._make_api_call(url)
    
    def get_player_game_log_current(self, player_id: int) -> Optional[Dict]:
        """
        Journal de matchs actuel d'un joueur
        """
        url = f"{self.base_web_api}/v1/player/{player_id}/game-log/now"
        return self._make_api_call(url)
    
    # === SCORES & MATCHS EN TEMPS RÉEL ===
    
    def get_daily_scores_now(self) -> Optional[Dict]:
        """
        Scores du jour - pour suivi live des paris
        """
        url = f"{self.base_web_api}/v1/score/now"
        return self._make_api_call(url)
    
    def get_daily_scores_date(self, date: str) -> Optional[Dict]:
        """
        Scores d'une date spécifique (YYYY-MM-DD)
        """
        url = f"{self.base_web_api}/v1/score/{date}"
        return self._make_api_call(url)
    
    def get_schedule_now(self) -> Optional[Dict]:
        """
        Calendrier actuel - matchs du jour
        """
        url = f"{self.base_web_api}/v1/schedule/now"
        return self._make_api_call(url)
    
    def get_schedule_by_date(self, date: str) -> Optional[Dict]:
        """
        Calendrier d'une date spécifique
        """
        url = f"{self.base_web_api}/v1/schedule/{date}"
        return self._make_api_call(url)
    
    # === COTES OFFICIELLES PARTENAIRES ===
    
    def get_partner_odds_us(self) -> Optional[Dict]:
        """
        🎯 CRUCIAL: Cotes officielles des partenaires NHL (US)
        """
        url = f"{self.base_web_api}/v1/partner-game/US/now"
        return self._make_api_call(url)
    
    def get_partner_odds_ca(self) -> Optional[Dict]:
        """
        🎯 CRUCIAL: Cotes officielles des partenaires NHL (Canada)
        Peut inclure des données Mise-o-jeu+!
        """
        url = f"{self.base_web_api}/v1/partner-game/CA/now"
        return self._make_api_call(url)
    
    # === INFORMATIONS DE MATCH DÉTAILLÉES ===
    
    def get_game_boxscore(self, game_id: int) -> Optional[Dict]:
        """
        Boxscore détaillé d'un match
        """
        url = f"{self.base_web_api}/v1/gamecenter/{game_id}/boxscore"
        return self._make_api_call(url)
    
    def get_game_play_by_play(self, game_id: int) -> Optional[Dict]:
        """
        Jeu par jeu d'un match
        """
        url = f"{self.base_web_api}/v1/gamecenter/{game_id}/play-by-play"
        return self._make_api_call(url)
    
    # === STATISTIQUES AVANCÉES (Stats API) ===
    
    def get_advanced_team_stats(self, cayenne_exp: Optional[str] = None) -> Optional[Dict]:
        """
        Statistiques avancées d'équipes
        Exemple cayenne_exp: "seasonId=20252026 and gameTypeId=2"
        """
        if not cayenne_exp:
            cayenne_exp = f"seasonId={self.season_current} and gameTypeId=2"
        
        url = f"{self.base_stats_api}/en/team/summary?cayenneExp={cayenne_exp}"
        return self._make_api_call(url)
    
    def get_advanced_skater_stats(self, cayenne_exp: Optional[str] = None, limit: int = 50) -> Optional[Dict]:
        """
        Statistiques avancées de joueurs
        """
        if not cayenne_exp:
            cayenne_exp = f"seasonId={self.season_current}"
        
        url = f"{self.base_stats_api}/en/skater/summary?limit={limit}&cayenneExp={cayenne_exp}"
        return self._make_api_call(url)
    
    def get_advanced_goalie_stats(self, cayenne_exp: Optional[str] = None, limit: int = 30) -> Optional[Dict]:
        """
        Statistiques avancées de gardiens
        """
        if not cayenne_exp:
            cayenne_exp = f"seasonId={self.season_current}"
        
        url = f"{self.base_stats_api}/en/goalie/summary?limit={limit}&cayenneExp={cayenne_exp}"
        return self._make_api_call(url)


def create_betting_intelligence_report():
    """
    Génère un rapport d'intelligence betting avec données live
    """
    api = NHLAPIAdvanced()
    
    print("🚀 RAPPORT D'INTELLIGENCE BETTING NHL")
    print("=" * 45)
    print("📡 Données officielles en temps réel")
    print()
    
    # 1. CLASSEMENTS ACTUELS
    print("🏆 CLASSEMENTS ACTUELS")
    print("-" * 25)
    standings = api.get_current_standings()
    if standings:
        # Analyser les divisions pour trends betting
        print("✅ Classements récupérés - analyse en cours...")
        
        # Exemple d'extraction des leaders de division
        if 'standings' in standings:
            for standing in standings['standings'][:8]:  # Top 8 équipes
                team_name = standing.get('teamName', {}).get('default', 'N/A')
                points = standing.get('points', 0)
                wins = standing.get('wins', 0)
                losses = standing.get('losses', 0)
                print(f"   {team_name[:20]:20} | {points:3d} pts | {wins:2d}W-{losses:2d}L")
    else:
        print("❌ Erreur récupération classements")
    
    print()
    
    # 2. MENEURS STATISTIQUES
    print("⭐ MENEURS ACTUELS (Props Betting)")
    print("-" * 35)
    
    # Points leaders
    points_leaders = api.get_skater_leaders_current("points", 5)
    if points_leaders and 'data' in points_leaders:
        print("🎯 POINTS:")
        for i, player in enumerate(points_leaders['data'][:5], 1):
            name = player.get('fullName', 'N/A')
            points = player.get('points', 0)
            team = player.get('teamAbbrev', 'N/A')
            print(f"   {i}. {name[:20]:20} ({team}) - {points} pts")
    
    print()
    
    # Goals leaders
    goals_leaders = api.get_skater_leaders_current("goals", 5)
    if goals_leaders and 'data' in goals_leaders:
        print("🥅 BUTS:")
        for i, player in enumerate(goals_leaders['data'][:5], 1):
            name = player.get('fullName', 'N/A')
            goals = player.get('goals', 0)
            team = player.get('teamAbbrev', 'N/A')
            print(f"   {i}. {name[:20]:20} ({team}) - {goals} buts")
    
    print()
    
    # 3. COTES PARTENAIRES OFFICIELLES
    print("💰 COTES PARTENAIRES OFFICIELLES")
    print("-" * 35)
    
    # Essayer Canada d'abord (Mise-o-jeu+)
    odds_ca = api.get_partner_odds_ca()
    if odds_ca:
        print("🇨🇦 Cotes Canada récupérées ✅")
        # Analyser les données de cotes ici
    else:
        print("🇨🇦 Cotes Canada non disponibles")
    
    # Fallback sur US
    odds_us = api.get_partner_odds_us()
    if odds_us:
        print("🇺🇸 Cotes US récupérées ✅")
    else:
        print("🇺🇸 Cotes US non disponibles")
    
    print()
    
    # 4. SCORES & CALENDRIER DU JOUR
    print("📅 ACTIVITÉ AUJOURD'HUI")
    print("-" * 25)
    
    today_scores = api.get_daily_scores_now()
    if today_scores:
        print("✅ Scores du jour récupérés")
        if 'games' in today_scores:
            game_count = len(today_scores['games'])
            print(f"   {game_count} matchs programmés/en cours")
    
    today_schedule = api.get_schedule_now()
    if today_schedule:
        print("✅ Calendrier du jour récupéré")
    
    print()
    print("🎯 SYSTÈME D'INTELLIGENCE BETTING OPÉRATIONNEL!")
    print("=" * 50)
    print("🔄 Données actualisées en temps réel")
    print("📊 Prêt pour analyse betting avancée")
    
    return {
        'standings': standings,
        'points_leaders': points_leaders,
        'goals_leaders': goals_leaders,
        'odds_ca': odds_ca,
        'odds_us': odds_us,
        'today_scores': today_scores,
        'today_schedule': today_schedule
    }


def analyze_specific_teams_for_betting(teams: List[str]):
    """
    Analyse spécifique d'équipes pour betting
    """
    api = NHLAPIAdvanced()
    
    print(f"🔍 ANALYSE SPÉCIFIQUE - {', '.join(teams)}")
    print("=" * 40)
    
    team_analysis = {}
    
    for team in teams:
        print(f"\n🏒 {team.upper()}")
        print("-" * 20)
        
        # Stats actuelles
        stats = api.get_team_stats_current(team)
        if stats:
            print("✅ Stats actuelles récupérées")
            # Extraire les métriques clés
            if 'data' in stats:
                data = stats['data']
                wins = data.get('wins', 0)
                losses = data.get('losses', 0)
                points = data.get('points', 0)
                print(f"   Fiche: {wins}W-{losses}L ({points} pts)")
        
        # Roster actuel
        roster = api.get_team_roster_current(team)
        if roster:
            print("✅ Roster actuel récupéré")
            if 'forwards' in roster:
                forward_count = len(roster['forwards'])
                print(f"   Attaquants: {forward_count}")
        
        # Calendrier
        schedule = api.get_team_schedule_current(team)
        if schedule:
            print("✅ Calendrier récupéré")
        
        team_analysis[team] = {
            'stats': stats,
            'roster': roster,
            'schedule': schedule
        }
    
    return team_analysis


if __name__ == "__main__":
    # Test du système
    print("🧪 TEST SYSTÈME API AVANCÉ NHL")
    print("=" * 35)
    
    # Rapport général
    intelligence_report = create_betting_intelligence_report()
    
    print("\n" + "="*50)
    
    # Analyse spécifique des équipes populaires pour betting
    key_teams = ["TOR", "MTL", "EDM", "BOS", "NYR"]
    team_analysis = analyze_specific_teams_for_betting(key_teams)
    
    print(f"\n🎯 ANALYSE TERMINÉE!")
    print("=" * 20)
    print("✅ Intelligence betting opérationnelle")
    print("✅ APIs officielles NHL intégrées")
    print("🚀 Prêt pour betting avancé!")
