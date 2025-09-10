#!/usr/bin/env python3
"""
🏒 NHL API OFFICIELLE - VRAIS MATCHS ET CALENDRIER
Connexion à l'API NHL pour récupérer le calendrier officiel

API NHL: https://api-web.nhle.com/
Endpoints:
- Schedule: /v1/schedule/now
- Team info: /v1/standings/now  
- Game details: /v1/gamecenter/{gameId}/boxscore
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3

class NHLOfficialAPI:
    """
    🏒 CONNECTEUR API NHL OFFICIELLE
    
    Récupère:
    - Calendrier officiel matchs
    - Scores en temps réel
    - Statistiques équipes
    - Informations joueurs
    """
    
    def __init__(self):
        self.base_url = "https://api-web.nhle.com/v1"
        self.headers = {
            'User-Agent': 'NHL-Calendar-Predictor/1.0',
            'Accept': 'application/json'
        }
        
        print("🏒 NHL API OFFICIELLE - CONNEXION")
        print("=" * 50)
        print("🌐 Base URL:", self.base_url)
    
    def _make_request(self, url: str) -> Dict:
        """Fait une requête HTTP avec urllib"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except urllib.error.URLError as e:
            print(f"❌ Erreur connexion: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            return {}
        except Exception as e:
            print(f"❌ Erreur requête: {e}")
            return {}
        
    def get_schedule_for_date(self, date_str: str) -> List[Dict]:
        """Récupère le calendrier NHL officiel pour une date"""
        
        try:
            # Format API NHL: YYYY-MM-DD
            url = f"{self.base_url}/schedule/{date_str}"
            
            print(f"📅 Récupération calendrier: {date_str}")
            print(f"🔗 URL: {url}")
            
            data = self._make_request(url)
            
            # Parser les matchs NHL
            games = []
            if 'gameWeek' in data:
                for day in data['gameWeek']:
                    if day['date'] == date_str:
                        for game in day.get('games', []):
                            games.append(self._parse_nhl_game(game))
            
            print(f"✅ {len(games)} matchs officiels trouvés pour {date_str}")
            return games
            
        except Exception as e:
            print(f"❌ Erreur API NHL: {e}")
            return []
    
    def get_current_schedule(self, days: int = 7) -> Dict[str, List[Dict]]:
        """Récupère calendrier NHL pour les prochains jours"""
        
        print(f"\n📅 RÉCUPÉRATION CALENDRIER OFFICIEL NHL ({days} jours)")
        
        schedule = {}
        today = datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            games = self.get_schedule_for_date(date_str)
            schedule[date_str] = games
            
            if games:
                print(f"   📊 {date_str}: {len(games)} matchs officiels")
        
        total_games = sum(len(games) for games in schedule.values())
        print(f"\n🏆 TOTAL: {total_games} matchs officiels récupérés")
        
        return schedule
    
    def _parse_nhl_game(self, game_data: Dict) -> Dict:
        """Parse un match NHL de l'API officielle"""
        
        try:
            game_id = str(game_data.get('id', ''))
            
            # Équipes
            home_team = game_data.get('homeTeam', {})
            away_team = game_data.get('awayTeam', {})
            
            home_abbrev = home_team.get('abbrev', 'UNK')
            away_abbrev = away_team.get('abbrev', 'UNK')
            
            # Heure de début
            start_time = game_data.get('startTimeUTC', '')
            if start_time:
                # Convertir UTC vers heure locale
                try:
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    # Ajuster pour EST (NHL principalement EST)
                    local_time = dt.replace(tzinfo=None) - timedelta(hours=5)
                    game_time = local_time.strftime('%H:%M')
                except:
                    game_time = "19:00"
            else:
                game_time = "19:00"
            
            # Scores si match terminé
            home_score = None
            away_score = None
            game_status = game_data.get('gameState', 'SCHEDULED')
            
            if game_status in ['FINAL', 'OFF']:
                home_score = home_team.get('score', 0)
                away_score = away_team.get('score', 0)
            
            # Venue
            venue = game_data.get('venue', {}).get('default', f"{home_abbrev} Arena")
            
            parsed_game = {
                'game_id': f"nhl_{game_id}",
                'home_team': home_abbrev,
                'away_team': away_abbrev,
                'home_team_name': home_team.get('name', {}).get('default', home_abbrev),
                'away_team_name': away_team.get('name', {}).get('default', away_abbrev),
                'start_time': game_time,
                'venue': venue,
                'game_status': game_status,
                'home_score': home_score,
                'away_score': away_score,
                'api_game_id': game_id
            }
            
            return parsed_game
            
        except Exception as e:
            print(f"⚠️  Erreur parsing match: {e}")
            return {}
    
    def get_team_stats(self, team_abbrev: str) -> Dict:
        """Récupère stats d'une équipe NHL"""
        
        try:
            # API standings pour avoir les stats
            url = f"{self.base_url}/standings/now"
            data = self._make_request(url)
            
            # Chercher l'équipe dans les standings
            for standing in data.get('standings', []):
                if standing.get('teamAbbrev', {}).get('default', '') == team_abbrev:
                    return {
                        'wins': standing.get('wins', 0),
                        'losses': standing.get('losses', 0),
                        'ties': standing.get('otLosses', 0),
                        'points': standing.get('points', 0),
                        'goals_for': standing.get('goalFor', 0),
                        'goals_against': standing.get('goalAgainst', 0),
                        'games_played': standing.get('gamesPlayed', 0)
                    }
            
            return {}
            
        except Exception as e:
            print(f"⚠️  Erreur stats équipe {team_abbrev}: {e}")
            return {}
    
    def test_api_connection(self):
        """Test de connexion à l'API NHL"""
        
        print("\n🔧 TEST CONNEXION API NHL")
        print("=" * 40)
        
        # Test 1: Schedule aujourd'hui
        today = datetime.now().strftime('%Y-%m-%d')
        games_today = self.get_schedule_for_date(today)
        
        print(f"📅 Matchs aujourd'hui ({today}): {len(games_today)}")
        
        # Test 2: Standings
        try:
            url = f"{self.base_url}/standings/now"
            standings_data = self._make_request(url)
            if standings_data:
                print(f"📊 Standings API: ✅ Connecté")
            else:
                print(f"📊 Standings API: ❌ Erreur")
        except:
            print(f"📊 Standings API: ❌ Erreur")
        
        # Test 3: Afficher quelques matchs
        if games_today:
            print(f"\n🏒 EXEMPLES MATCHS OFFICIELS:")
            for i, game in enumerate(games_today[:3], 1):
                if game:
                    print(f"{i}. {game['start_time']} - {game['away_team']} @ {game['home_team']}")
                    print(f"   🏟️  {game['venue']}")
        
        return len(games_today) > 0

def integrate_official_api_with_calendar():
    """Intègre l'API officielle NHL avec le calendrier"""
    
    print("\n🔗 INTÉGRATION API OFFICIELLE NHL")
    print("=" * 50)
    
    # Test connexion
    nhl_api = NHLOfficialAPI()
    connection_ok = nhl_api.test_api_connection()
    
    if not connection_ok:
        print("❌ Pas de matchs NHL aujourd'hui ou problème connexion")
        print("💡 Le système utilisera des matchs simulés pour la démo")
        return False
    
    # Récupérer calendrier officiel
    official_schedule = nhl_api.get_current_schedule(days=7)
    
    # Sauvegarder en base de données
    conn = sqlite3.connect("nhl_calendar_predictions.db")
    cursor = conn.cursor()
    
    # Ajouter colonne pour ID API si pas déjà fait
    try:
        cursor.execute('ALTER TABLE nhl_games ADD COLUMN api_game_id TEXT')
        cursor.execute('ALTER TABLE nhl_games ADD COLUMN official_api BOOLEAN DEFAULT 0')
    except:
        pass  # Colonnes déjà existantes
    
    games_added = 0
    
    for date_str, games in official_schedule.items():
        for game in games:
            if not game:
                continue
                
            # Insérer match officiel
            cursor.execute('''
                INSERT OR REPLACE INTO nhl_games 
                (game_id, game_date, home_team, away_team, start_time, venue,
                 home_score, away_score, game_status, api_game_id, official_api)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game['game_id'], date_str, game['home_team'], game['away_team'],
                game['start_time'], game['venue'], game.get('home_score'),
                game.get('away_score'), game['game_status'], 
                game['api_game_id'], True
            ))
            
            games_added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ {games_added} matchs officiels ajoutés à la base")
    print(f"🏒 Le calendrier affiche maintenant les VRAIS matchs NHL!")
    
    return True

def main():
    """Teste et intègre l'API NHL officielle"""
    
    print("🚀 NHL API OFFICIELLE - INTÉGRATION COMPLÈTE")
    
    # Tenter intégration API officielle
    api_success = integrate_official_api_with_calendar()
    
    if api_success:
        print(f"\n🎉 SUCCÈS! Calendrier NHL avec matchs officiels prêt!")
        print(f"🌐 Relance le calendrier pour voir les vrais matchs!")
    else:
        print(f"\n💡 Mode démo activé avec matchs simulés")
        print(f"🔧 L'API officielle sera utilisée pendant la saison NHL")

if __name__ == "__main__":
    main()
