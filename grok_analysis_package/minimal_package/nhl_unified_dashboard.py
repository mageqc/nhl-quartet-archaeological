#!/usr/bin/env python3
"""
🚀 DASHBOARD UNIFIÉ NHL - API OFFICIELLE + LOGOS
Dashboard complet avec données temps réel NHL et logos officiels
"""

import sqlite3
import json
import urllib.request
from datetime import datetime, timedelta
from nhl_logos_system import NHLLogosSystem

class NHLUnifiedDashboard:
    """
    🚀 DASHBOARD UNIFIÉ NHL COMPLET
    
    Fonctionnalités:
    - API NHL officielle temps réel
    - Logos officiels 32 équipes
    - Statistiques avancées équipes
    - Interface responsive moderne
    - Fallback mode hors-saison
    """
    
    def __init__(self):
        print("🚀 DASHBOARD UNIFIÉ NHL - INITIALISATION")
        print("=" * 50)
        
        self.logos_system = NHLLogosSystem()
        self.base_url = "https://api-web.nhle.com/v1"
        self.dashboard_file = "nhl_unified_dashboard.html"
        self.db_file = "nhl_unified_dashboard.db"
        
        self._init_database()
        
    def _init_database(self):
        """Initialise base de données dashboard"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Table matchs temps réel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS realtime_games (
                game_id TEXT PRIMARY KEY,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                home_score INTEGER,
                away_score INTEGER,
                period INTEGER,
                period_time TEXT,
                game_state TEXT,
                venue TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Table stats équipes temps réel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_stats (
                team_code TEXT PRIMARY KEY,
                team_name TEXT,
                wins INTEGER,
                losses INTEGER,
                otl INTEGER,  -- Overtime losses
                points INTEGER,
                games_played INTEGER,
                goals_for INTEGER,
                goals_against INTEGER,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("🗃️ Base de données initialisée")
    
    def fetch_live_data(self) -> dict:
        """Récupère données temps réel API NHL officielle"""
        
        print("📡 Récupération données NHL API officielle...")
        
        live_data = {
            'games_today': [],
            'team_standings': [],
            'api_status': 'unknown',
            'data_source': 'simulation',  # Fallback par défaut
            'last_update': datetime.now().isoformat()
        }
        
        try:
            # Tenter récupération matchs du jour
            today = datetime.now().strftime('%Y-%m-%d')
            schedule_url = f"{self.base_url}/schedule/{today}"
            
            with urllib.request.urlopen(schedule_url, timeout=10) as response:
                if response.status == 200:
                    schedule_data = json.loads(response.read().decode('utf-8'))
                    
                    if 'gameWeek' in schedule_data:
                        for week_data in schedule_data['gameWeek']:
                            if 'games' in week_data:
                                for game in week_data['games']:
                                    live_data['games_today'].append({
                                        'id': game.get('id'),
                                        'home_team': game.get('homeTeam', {}).get('abbrev', 'TBD'),
                                        'away_team': game.get('awayTeam', {}).get('abbrev', 'TBD'),
                                        'home_score': game.get('homeTeam', {}).get('score', 0),
                                        'away_score': game.get('awayTeam', {}).get('score', 0),
                                        'period': game.get('period', 0),
                                        'clock': game.get('clock', {}).get('timeRemaining', ''),
                                        'game_state': game.get('gameState', 'SCHEDULED'),
                                        'venue': game.get('venue', {}).get('default', 'TBD'),
                                        'start_time': game.get('startTimeUTC', '')
                                    })
                    
                    live_data['api_status'] = 'connected'
                    live_data['data_source'] = 'nhl_official_api'
                    print("✅ Données NHL API récupérées avec succès")
        
        except Exception as e:
            print(f"⚠️ API NHL inaccessible: {str(e)}")
            print("🎮 Basculement mode simulation...")
            
            # Mode simulation - données d'entraînement
            live_data['games_today'] = self._generate_simulation_games()
            live_data['api_status'] = 'simulation_mode'
            live_data['data_source'] = 'simulation'
        
        # Sauvegarder données récupérées
        self._save_live_data(live_data)
        
        return live_data
    
    def _generate_simulation_games(self) -> list:
        """Génère matchs simulation pour hors-saison"""
        
        nhl_teams = ['TOR', 'MTL', 'BOS', 'NYR', 'PHI', 'WSH', 'PIT', 'CAR',
                     'EDM', 'CGY', 'VAN', 'SEA', 'ANA', 'LA', 'SJ', 'VGK',
                     'COL', 'DAL', 'MIN', 'STL', 'WPG', 'NSH', 'ARI', 'CHI',
                     'TBL', 'FLA', 'OTT', 'BUF', 'DET', 'CBJ', 'NJD', 'NYI']
        
        import random
        simulation_games = []
        
        # Générer 4-8 matchs aléatoires
        num_games = random.randint(4, 8)
        
        for i in range(num_games):
            teams_sample = random.sample(nhl_teams, 2)
            away_team, home_team = teams_sample
            
            # Scores simulés (match en cours ou terminé)
            game_states = ['LIVE', 'FINAL', 'SCHEDULED']
            state = random.choice(game_states)
            
            if state == 'SCHEDULED':
                home_score = away_score = 0
                period = 0
                clock = ''
            elif state == 'LIVE':
                home_score = random.randint(0, 4)
                away_score = random.randint(0, 4)
                period = random.randint(1, 3)
                clock = f"{random.randint(1, 19)}:{random.randint(10, 59)}"
            else:  # FINAL
                home_score = random.randint(1, 6)
                away_score = random.randint(1, 6)
                period = 3
                clock = 'FINAL'
            
            simulation_games.append({
                'id': f"sim_{i+1}",
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'period': period,
                'clock': clock,
                'game_state': state,
                'venue': f"Arena {home_team}",
                'start_time': f"19:{random.randint(0, 3)}0:00"
            })
        
        return simulation_games
    
    def _save_live_data(self, live_data: dict):
        """Sauvegarde données temps réel en base"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Sauvegarder matchs
        for game in live_data['games_today']:
            cursor.execute('''
                INSERT OR REPLACE INTO realtime_games 
                (game_id, date, home_team, away_team, home_score, away_score,
                 period, period_time, game_state, venue, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game['id'],
                datetime.now().strftime('%Y-%m-%d'),
                game['home_team'],
                game['away_team'],
                game['home_score'],
                game['away_score'],
                game['period'],
                game['clock'],
                game['game_state'],
                game['venue'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def generate_unified_dashboard(self) -> str:
        """Génère dashboard HTML unifié complet"""
        
        print("🎨 Génération dashboard unifié NHL...")
        
        # Récupérer données temps réel
        live_data = self.fetch_live_data()
        
        # Génération HTML
        html_content = self._generate_dashboard_html(live_data)
        
        # Sauvegarder
        with open(self.dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard unifié généré: {self.dashboard_file}")
        return self.dashboard_file
    
    def _generate_dashboard_html(self, live_data: dict) -> str:
        """Génère HTML complet dashboard unifié"""
        
        # CSS logos
        logos_css = self.logos_system.export_logos_css()
        
        # Badges source données
        if live_data['data_source'] == 'nhl_official_api':
            source_badge = '''
                <div class="source-badge official">
                    🏒 DONNÉES NHL OFFICIELLES - TEMPS RÉEL
                </div>
            '''
        else:
            source_badge = '''
                <div class="source-badge simulation">
                    🎮 MODE SIMULATION - Données d'entraînement (Hors saison NHL)
                </div>
            '''
        
        html_content = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Dashboard NHL Unifié - API Officielle + Logos</title>
    <style>
        {self._get_dashboard_css()}
        {logos_css}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🚀 Dashboard NHL Unifié</h1>
            <p>API officielle • Logos authentiques • Données temps réel</p>
            {source_badge}
        </div>
        
        <div class="status-indicators">
            <div class="indicator api-status {live_data['api_status']}">
                API: {live_data['api_status'].upper()}
            </div>
            <div class="indicator">
                Mise à jour: {datetime.fromisoformat(live_data['last_update']).strftime('%H:%M:%S')}
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <!-- Section Matchs du jour -->
        <div class="section">
            <h2 class="section-title">
                🏒 Matchs du jour ({len(live_data['games_today'])})
            </h2>
            
            <div class="games-grid">
'''
        
        # Ajouter matchs
        if live_data['games_today']:
            for game in live_data['games_today']:
                # Matchup avec logos
                matchup_html = self.logos_system.get_matchup_html(
                    game['away_team'], game['home_team'], 
                    size='large', show_vs=True
                )
                
                # Status badge
                status_class = game['game_state'].lower()
                if status_class == 'live':
                    status_badge = f'<span class="status-badge live">🔴 EN DIRECT - P{game["period"]} {game["clock"]}</span>'
                elif status_class == 'final':
                    status_badge = '<span class="status-badge final">✅ TERMINÉ</span>'
                else:
                    status_badge = f'<span class="status-badge scheduled">🕒 {game["start_time"][:5]}</span>'
                
                html_content += f'''
                <div class="game-card {status_class}">
                    <div class="game-status">
                        {status_badge}
                    </div>
                    
                    <div class="game-matchup">
                        {matchup_html}
                    </div>
                    
                    <div class="game-score">
                        <div class="score-display">
                            <span class="away-score">{game['away_score']}</span>
                            <span class="score-separator">-</span>
                            <span class="home-score">{game['home_score']}</span>
                        </div>
                    </div>
                    
                    <div class="game-venue">
                        📍 {game['venue']}
                    </div>
                </div>
'''
        else:
            html_content += '''
                <div class="no-games">
                    🏒 Aucun match programmé aujourd'hui
                </div>
'''
        
        html_content += f'''
            </div>
        </div>
        
        <!-- Section Statistiques équipes -->
        <div class="section">
            <h2 class="section-title">
                📊 Équipes NHL ({len(self.logos_system.team_logos)})
            </h2>
            
            <div class="teams-overview">
'''
        
        # Afficher toutes les équipes avec logos
        teams_list = list(self.logos_system.team_logos.keys())
        teams_list.sort()
        
        for i in range(0, len(teams_list), 8):  # 8 équipes par ligne
            html_content += '<div class="teams-row">'
            
            for team in teams_list[i:i+8]:
                team_info = self.logos_system.team_logos[team]
                team_html = self.logos_system.get_team_logo_html(team, size='medium')
                
                html_content += f'''
                    <div class="team-overview-card">
                        {team_html}
                    </div>
'''
            
            html_content += '</div>'
        
        html_content += f'''
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="update-info">
            Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            Source: {live_data['data_source'].upper()}<br>
            🚀 Dashboard NHL Unifié avec logos officiels
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">
            🔄 Actualiser
        </button>
    </div>
    
    <script>
        console.log('🚀 Dashboard NHL Unifié chargé!');
        console.log('Source données:', '{live_data["data_source"]}');
        
        // Auto-refresh toutes les 2 minutes
        setTimeout(() => location.reload(), 120000);
        
        // Animations logos
        document.addEventListener('DOMContentLoaded', function() {{
            const teamCards = document.querySelectorAll('.team-overview-card, .game-card');
            teamCards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-8px) scale(1.02)';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0) scale(1)';
                }});
            }});
        }});
        
        // Clignotement matchs en direct
        setInterval(() => {{
            const liveGames = document.querySelectorAll('.status-badge.live');
            liveGames.forEach(badge => {{
                badge.style.opacity = badge.style.opacity === '0.6' ? '1' : '0.6';
            }});
        }}, 1000);
    </script>
</body>
</html>
        '''
        
        return html_content
    
    def _get_dashboard_css(self) -> str:
        """CSS complet dashboard unifié"""
        
        return '''
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: white;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(15px);
            padding: 20px;
            border-bottom: 3px solid #ffd700;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .header-content h1 {
            font-size: 2.5em;
            background: linear-gradient(45deg, #ffd700, #ffed4e, #4CAF50);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(255,215,0,0.3);
            margin-bottom: 5px;
        }
        
        .header-content p {
            color: #ccc;
            font-size: 1.1em;
        }
        
        .source-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .source-badge.official {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            box-shadow: 0 0 15px rgba(76,175,80,0.4);
        }
        
        .source-badge.simulation {
            background: linear-gradient(45deg, #ff9800, #f57c00);
            box-shadow: 0 0 15px rgba(255,152,0,0.4);
        }
        
        .status-indicators {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .indicator {
            background: rgba(255,255,255,0.1);
            padding: 8px 16px;
            border-radius: 15px;
            font-size: 0.9em;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .api-status.connected { 
            background: rgba(76,175,80,0.3); 
            border-color: #4CAF50;
        }
        
        .api-status.simulation_mode { 
            background: rgba(255,152,0,0.3); 
            border-color: #ff9800;
        }
        
        .main-content {
            padding: 20px;
            max-width: 1800px;
            margin: 0 auto;
        }
        
        .section {
            margin-bottom: 40px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,215,0,0.2);
        }
        
        .section-title {
            font-size: 1.8em;
            color: #ffd700;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 0 0 10px rgba(255,215,0,0.3);
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .game-card {
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .game-card:hover {
            border-color: #ffd700;
            box-shadow: 0 8px 30px rgba(255,215,0,0.2);
        }
        
        .game-card.live {
            border-color: #ff4444;
            box-shadow: 0 0 20px rgba(255,68,68,0.3);
        }
        
        .game-card.final {
            border-color: #4CAF50;
        }
        
        .game-status {
            text-align: center;
            margin-bottom: 15px;
        }
        
        .status-badge {
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .status-badge.live {
            background: #ff4444;
            color: white;
            animation: pulse 2s infinite;
        }
        
        .status-badge.final {
            background: #4CAF50;
            color: white;
        }
        
        .status-badge.scheduled {
            background: #2196F3;
            color: white;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .game-matchup {
            margin: 20px 0;
        }
        
        .game-score {
            text-align: center;
            margin: 15px 0;
        }
        
        .score-display {
            font-size: 2em;
            font-weight: bold;
        }
        
        .away-score, .home-score {
            color: #ffd700;
        }
        
        .score-separator {
            color: #ccc;
            margin: 0 10px;
        }
        
        .game-venue {
            text-align: center;
            color: #ccc;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .teams-overview {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .teams-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
        }
        
        .team-overview-card {
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .team-overview-card:hover {
            background: rgba(255,215,0,0.1);
            border-color: #ffd700;
        }
        
        .no-games {
            text-align: center;
            color: #888;
            font-size: 1.2em;
            padding: 40px;
            font-style: italic;
        }
        
        .footer {
            background: rgba(0,0,0,0.4);
            padding: 20px;
            text-align: center;
            border-top: 2px solid rgba(255,215,0,0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .update-info {
            color: #ccc;
            font-size: 0.9em;
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #0f3460;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .refresh-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(255,215,0,0.4);
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 15px;
            }
            
            .status-indicators {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .games-grid {
                grid-template-columns: 1fr;
            }
            
            .teams-row {
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            }
        }
        '''

def main():
    """Lance dashboard NHL unifié complet"""
    
    print("🚀 DASHBOARD NHL UNIFIÉ - LANCEMENT")
    
    dashboard = NHLUnifiedDashboard()
    dashboard_file = dashboard.generate_unified_dashboard()
    
    print(f"\n✅ DASHBOARD UNIFIÉ PRÊT!")
    print(f"🎨 Interface: {dashboard_file}")
    print(f"🏒 API NHL officielle + 32 logos authentiques!")
    print(f"📊 Données temps réel avec fallback hors-saison!")

if __name__ == "__main__":
    main()
