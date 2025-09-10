"""
Scraper OFFICIEL de calendrier NHL 2025-2026

Ce module récupère TOUS les matchs officiels directement depuis l'API NHL.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess
import os


class OfficialNHLScheduleScraper:
    """
    Collecteur OFFICIEL du calendrier NHL complet via API
    """
    
    def __init__(self):
        self.season = "20252026"
        self.api_base = "https://api-web.nhle.com/v1"
        
    def get_complete_official_schedule(self) -> Dict:
        """
        Récupère le calendrier OFFICIEL complet de la saison 2025-2026
        
        Returns:
            dict: Calendrier officiel complet
        """
        print("🏒 RÉCUPÉRATION CALENDRIER OFFICIEL NHL 2025-2026")
        print("=" * 55)
        
        all_games = []
        
        # Dates de début et fin de saison
        start_date = datetime(2025, 9, 15)  # Début présaison
        end_date = datetime(2026, 6, 30)    # Fin playoffs
        
        current_date = start_date
        total_days = (end_date - start_date).days
        
        print(f"📅 Période: {start_date.strftime('%d/%m/%Y')} → {end_date.strftime('%d/%m/%Y')}")
        print(f"🔍 Analyse de {total_days} jours...")
        print()
        
        day_count = 0
        games_found = 0
        
        while current_date <= end_date:
            day_count += 1
            date_str = current_date.strftime('%Y-%m-%d')
            
            if day_count % 30 == 0:
                print(f"📊 Progression: {day_count}/{total_days} jours | {games_found} matchs trouvés")
            
            # Récupérer les matchs pour cette date
            daily_games = self._fetch_games_for_date(date_str)
            if daily_games:
                all_games.extend(daily_games)
                games_found += len(daily_games)
                
                # Afficher les dates avec matchs importants
                if any(game.get('gameType', 0) == 2 for game in daily_games):  # Saison régulière
                    if len(daily_games) >= 5:  # Journée chargée
                        print(f"📅 {date_str}: {len(daily_games)} matchs")
            
            current_date += timedelta(days=1)
        
        print()
        print(f"✅ RÉCUPÉRATION TERMINÉE!")
        print(f"📊 Total matchs officiels: {len(all_games)}")
        
        # Organiser les données
        organized_schedule = self._organize_official_schedule(all_games)
        
        # Sauvegarder
        self._save_official_schedule(organized_schedule)
        
        return organized_schedule
    
    def _fetch_games_for_date(self, date_str: str) -> List[Dict]:
        """Récupère les matchs officiels pour une date donnée"""
        try:
            # Utiliser curl pour récupérer les données
            cmd = f'curl -s "{self.api_base}/schedule/{date_str}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                
                games = []
                
                # Parser la structure de la nouvelle API NHL
                if 'gameWeek' in data:
                    for week_day in data['gameWeek']:
                        if week_day.get('date') == date_str:
                            for game in week_day.get('games', []):
                                official_game = self._parse_official_game(game, date_str)
                                if official_game:
                                    games.append(official_game)
                
                return games
                
        except Exception as e:
            # Erreur silencieuse pour ne pas polluer la sortie
            pass
        
        return []
    
    def _parse_official_game(self, game_data: Dict, date_str: str) -> Dict:
        """Parse un match depuis les données officielles NHL"""
        try:
            # Extraire les informations officielles
            away_team = game_data.get('awayTeam', {})
            home_team = game_data.get('homeTeam', {})
            
            official_game = {
                'game_id': game_data.get('id'),
                'date': date_str,
                'time': game_data.get('startTimeUTC', ''),
                'away_team_id': away_team.get('id'),
                'home_team_id': home_team.get('id'),
                'away_team': away_team.get('commonName', {}).get('default', ''),
                'home_team': home_team.get('commonName', {}).get('default', ''),
                'away_abbr': away_team.get('abbrev', ''),
                'home_abbr': home_team.get('abbrev', ''),
                'venue': game_data.get('venue', {}).get('default', ''),
                'game_type': game_data.get('gameType', 0),  # 1=Preseason, 2=Regular, 3=Playoffs
                'season': self.season,
                'game_state': game_data.get('gameState', 'FUT'),
                'tv_broadcasts': game_data.get('tvBroadcasts', []),
                'neutral_site': game_data.get('neutralSite', False),
                'timezone': game_data.get('venueTimezone', ''),
                'source': 'NHL_OFFICIAL_API'
            }
            
            # Ajouter des métadonnées utiles
            game_type_map = {1: 'Preseason', 2: 'Regular Season', 3: 'Playoffs'}
            official_game['game_type_name'] = game_type_map.get(official_game['game_type'], 'Unknown')
            
            # Nettoyer les noms d'équipes
            official_game['away_team'] = self._clean_team_name(official_game['away_team'])
            official_game['home_team'] = self._clean_team_name(official_game['home_team'])
            
            return official_game
            
        except Exception as e:
            return {}
    
    def _clean_team_name(self, team_name: str) -> str:
        """Nettoie et standardise les noms d'équipes"""
        # Corrections pour les noms d'équipes
        name_corrections = {
            'Penguins': 'Pittsburgh Penguins',
            'Sabres': 'Buffalo Sabres',
            'Rangers': 'New York Rangers',
            'Maple Leafs': 'Toronto Maple Leafs',
            'Canadiens': 'Montreal Canadiens',
            'Bruins': 'Boston Bruins',
            'Lightning': 'Tampa Bay Lightning',
            'Panthers': 'Florida Panthers',
            'Red Wings': 'Detroit Red Wings',
            'Senators': 'Ottawa Senators',
            'Islanders': 'New York Islanders',
            'Flyers': 'Philadelphia Flyers',
            'Devils': 'New Jersey Devils',
            'Blue Jackets': 'Columbus Blue Jackets',
            'Capitals': 'Washington Capitals',
            'Hurricanes': 'Carolina Hurricanes',
            'Predators': 'Nashville Predators',
            'Stars': 'Dallas Stars',
            'Blues': 'St. Louis Blues',
            'Wild': 'Minnesota Wild',
            'Blackhawks': 'Chicago Blackhawks',
            'Avalanche': 'Colorado Avalanche',
            'Jets': 'Winnipeg Jets',
            'Flames': 'Calgary Flames',
            'Oilers': 'Edmonton Oilers',
            'Canucks': 'Vancouver Canucks',
            'Kings': 'Los Angeles Kings',
            'Sharks': 'San Jose Sharks',
            'Ducks': 'Anaheim Ducks',
            'Golden Knights': 'Vegas Golden Knights',
            'Kraken': 'Seattle Kraken',
            'Utah Hockey Club': 'Utah Hockey Club'
        }
        
        return name_corrections.get(team_name, team_name)
    
    def _organize_official_schedule(self, games: List[Dict]) -> Dict:
        """Organise le calendrier officiel"""
        organized = {
            'season': self.season,
            'total_games': len(games),
            'last_updated': datetime.now().isoformat(),
            'source': 'NHL_OFFICIAL_API',
            'by_date': {},
            'by_team': {},
            'by_month': {},
            'by_game_type': {'preseason': [], 'regular': [], 'playoffs': []},
            'opening_games': [],
            'all_games': games,
            'statistics': {
                'preseason_games': 0,
                'regular_season_games': 0,
                'playoff_games': 0,
                'total_teams': set(),
                'date_range': {'start': None, 'end': None}
            }
        }
        
        dates = []
        
        for game in games:
            date = game['date']
            dates.append(date)
            
            # Par date
            if date not in organized['by_date']:
                organized['by_date'][date] = []
            organized['by_date'][date].append(game)
            
            # Par équipe
            for team in [game['home_team'], game['away_team']]:
                if team and team != '':
                    if team not in organized['by_team']:
                        organized['by_team'][team] = []
                    organized['by_team'][team].append(game)
                    organized['statistics']['total_teams'].add(team)
            
            # Par mois
            month = date[:7]  # YYYY-MM
            if month not in organized['by_month']:
                organized['by_month'][month] = []
            organized['by_month'][month].append(game)
            
            # Par type de match
            game_type = game.get('game_type', 0)
            if game_type == 1:
                organized['by_game_type']['preseason'].append(game)
                organized['statistics']['preseason_games'] += 1
            elif game_type == 2:
                organized['by_game_type']['regular'].append(game)
                organized['statistics']['regular_season_games'] += 1
                
                # Identifier les matchs d'ouverture (première semaine d'octobre)
                if date.startswith('2025-10') and date <= '2025-10-14':
                    organized['opening_games'].append(game)
                    
            elif game_type == 3:
                organized['by_game_type']['playoffs'].append(game)
                organized['statistics']['playoff_games'] += 1
        
        # Statistiques finales
        if dates:
            organized['statistics']['date_range']['start'] = min(dates)
            organized['statistics']['date_range']['end'] = max(dates)
            organized['statistics']['total_teams'] = len(organized['statistics']['total_teams'])
        
        return organized
    
    def _save_official_schedule(self, schedule_data: Dict):
        """Sauvegarde le calendrier officiel"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"data/nhl_official_schedule_{self.season}_{timestamp}.json"
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 Calendrier officiel sauvegardé: {filename}")
    
    def get_opening_week_official(self) -> List[Dict]:
        """Récupère les matchs officiels d'ouverture"""
        schedule = self.get_complete_official_schedule()
        return schedule.get('opening_games', [])
    
    def display_official_summary(self, schedule_data: Dict):
        """Affiche un résumé du calendrier officiel"""
        stats = schedule_data['statistics']
        
        print("\n🏒 CALENDRIER OFFICIEL NHL 2025-2026")
        print("=" * 45)
        print(f"📊 Total matchs: {schedule_data['total_games']}")
        print(f"🏟️  Équipes: {stats['total_teams']}")
        print(f"📅 Période: {stats['date_range']['start']} → {stats['date_range']['end']}")
        print()
        
        print("📈 RÉPARTITION PAR TYPE:")
        print(f"   🏒 Présaison: {stats['preseason_games']} matchs")
        print(f"   📅 Saison régulière: {stats['regular_season_games']} matchs")
        print(f"   🏆 Playoffs: {stats['playoff_games']} matchs")
        print()
        
        print("🎯 MATCHS D'OUVERTURE (Officiels):")
        opening_games = schedule_data.get('opening_games', [])
        for game in opening_games[:10]:  # Afficher les 10 premiers
            print(f"📅 {game['date']} - {game['away_team']} @ {game['home_team']}")
            if len(opening_games) > 10:
                print(f"   ... et {len(opening_games) - 10} autres matchs d'ouverture")
                break


# Fonction utilitaire principale
def get_official_nhl_schedule() -> Dict:
    """
    Récupère le calendrier OFFICIEL complet NHL 2025-2026
    
    Returns:
        dict: Calendrier officiel avec TOUS les matchs
    """
    scraper = OfficialNHLScheduleScraper()
    return scraper.get_complete_official_schedule()


def quick_opening_games() -> List[Dict]:
    """
    Récupère rapidement les matchs d'ouverture officiels
    
    Returns:
        list: Matchs d'ouverture officiels
    """
    scraper = OfficialNHLScheduleScraper()
    return scraper.get_opening_week_official()
