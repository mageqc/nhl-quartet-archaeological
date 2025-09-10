#!/usr/bin/env python3
"""
🎰 ODDS FETCHER TEMPS RÉEL - SPECS CHATGPT
Intégration The Odds API pour odds live NHL

Fonctionnalités:
- Fetch odds live pour tous les bookmakers
- Calcul EV automatique vs predictions trio
- Storage DB pour tracking historique
- Dashboard odds en temps réel

Usage:
- Live: python3 odds_fetcher_live.py
- Batch: python3 odds_fetcher_live.py --batch
"""

import sqlite3
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import os

class LiveOddsFetcher:
    """
    🎰 FETCHER ODDS LIVE COMPLET
    
    Intègre The Odds API selon specs ChatGPT:
    - Fetch odds multi-bookmakers
    - Calcul EV vs predictions trio
    - Storage historique
    - Rate limiting
    """
    
    def __init__(self, api_key: str = None, db_file: str = 'nhl_trio_system.db'):
        self.api_key = api_key or os.environ.get('ODDS_API_KEY')
        self.db_file = db_file
        self.base_url = "https://api.the-odds-api.com/v4"
        
        # Rate limiting (500 requests/month free tier)
        self.last_request_time = 0
        self.min_request_interval = 2.0  # 2s entre requests
        
        # Bookmakers prioritaires
        self.priority_bookmakers = [
            'fanduel', 'draftkings', 'betmgm', 'caesars',
            'pointsbet', 'betrivers', 'unibet_us'
        ]
        
        self._ensure_odds_tables()
    
    def _ensure_odds_tables(self):
        """Assure que les tables odds existent"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Table live odds
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS live_odds (
                odds_id TEXT PRIMARY KEY,
                game_id TEXT,
                bookmaker TEXT,
                home_odds REAL,
                away_odds REAL,
                home_team TEXT,
                away_team TEXT,
                game_date TEXT,
                market_type TEXT,
                fetched_at TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Table odds history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                bookmaker TEXT,
                home_odds REAL,
                away_odds REAL,
                market_type TEXT,
                timestamp TEXT,
                odds_movement REAL
            )
        ''')
        
        # Table ev calculations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ev_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                bookmaker TEXT,
                predicted_prob_home REAL,
                predicted_prob_away REAL,
                best_odds_home REAL,
                best_odds_away REAL,
                ev_home REAL,
                ev_away REAL,
                recommended_bet TEXT,
                stake_suggestion REAL,
                calculated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Odds tables initialisées")
    
    def _rate_limit(self):
        """Rate limiting pour API calls"""
        
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_request_interval:
            sleep_time = self.min_request_interval - elapsed
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def fetch_nhl_odds(self, date_filter: str = None) -> Dict:
        """Fetch odds NHL depuis The Odds API"""
        
        if not self.api_key:
            print("⚠️ No Odds API key - using demo data")
            return self._get_demo_odds()
        
        print("🎰 Fetching NHL odds...")
        
        self._rate_limit()
        
        try:
            # Construct API URL
            params = {
                'apiKey': self.api_key,
                'sport': 'icehockey_nhl',
                'markets': 'h2h',  # Head-to-head (moneyline)
                'oddsFormat': 'american',
                'bookmakers': ','.join(self.priority_bookmakers[:4])  # Limit bookmakers
            }
            
            if date_filter:
                params['commenceTimeFrom'] = f"{date_filter}T00:00:00Z"
                params['commenceTimeTo'] = f"{date_filter}T23:59:59Z"
            
            url = f"{self.base_url}/sports/icehockey_nhl/odds"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            with urllib.request.urlopen(full_url, timeout=15) as response:
                if response.status == 200:
                    odds_data = json.loads(response.read().decode('utf-8'))
                    
                    processed_odds = []
                    
                    for game in odds_data:
                        home_team = game.get('home_team', '')
                        away_team = game.get('away_team', '')
                        game_date = game.get('commence_time', '')[:10]  # YYYY-MM-DD
                        
                        game_id = f"{away_team.lower().replace(' ', '')}_" \
                                 f"{home_team.lower().replace(' ', '')}_{game_date.replace('-', '')}"
                        
                        # Process chaque bookmaker
                        for bookmaker_data in game.get('bookmakers', []):
                            bookmaker = bookmaker_data.get('key', '')
                            
                            # Market h2h (moneyline)
                            for market in bookmaker_data.get('markets', []):
                                if market.get('key') == 'h2h':
                                    outcomes = market.get('outcomes', [])
                                    
                                    home_odds = None
                                    away_odds = None
                                    
                                    for outcome in outcomes:
                                        if outcome.get('name') == home_team:
                                            home_odds = outcome.get('price')
                                        elif outcome.get('name') == away_team:
                                            away_odds = outcome.get('price')
                                    
                                    if home_odds and away_odds:
                                        processed_odds.append({
                                            'game_id': game_id,
                                            'bookmaker': bookmaker,
                                            'home_team': home_team,
                                            'away_team': away_team,
                                            'home_odds': home_odds,
                                            'away_odds': away_odds,
                                            'game_date': game_date,
                                            'market_type': 'h2h'
                                        })
                    
                    print(f"✅ {len(processed_odds)} odds records fetched")
                    return {'status': 'success', 'odds': processed_odds}
                    
        except Exception as e:
            print(f"❌ Erreur Odds API: {str(e)}")
        
        # Fallback demo data
        return self._get_demo_odds()
    
    def _get_demo_odds(self) -> Dict:
        """Génère odds demo pour tests"""
        
        demo_odds = []
        
        # Odds présaison MTL
        games = [
            ('PIT', 'MTL', '2025-09-22'),
            ('PHI', 'MTL', '2025-09-23'),
            ('MTL', 'TOR', '2025-09-25'),
            ('MTL', 'OTT', '2025-09-27')
        ]
        
        bookmakers = ['fanduel', 'draftkings', 'betmgm']
        
        for away, home, date in games:
            game_id = f"{away.lower()}_{home.lower()}_{date.replace('-', '')}"
            
            for bookmaker in bookmakers:
                # Odds variés par bookmaker
                base_home = -125 if home == 'MTL' else 115
                base_away = 105 if away != 'MTL' else -135
                
                # Variation par bookmaker
                variation = {'fanduel': 0, 'draftkings': 5, 'betmgm': -3}[bookmaker]
                
                demo_odds.append({
                    'game_id': game_id,
                    'bookmaker': bookmaker,
                    'home_team': home,
                    'away_team': away,
                    'home_odds': base_home + variation,
                    'away_odds': base_away - variation,
                    'game_date': date,
                    'market_type': 'h2h'
                })
        
        print(f"🎮 {len(demo_odds)} demo odds générées")
        return {'status': 'demo', 'odds': demo_odds}
    
    def store_odds(self, odds_data: List[Dict]) -> int:
        """Store odds en DB avec tracking mouvement"""
        
        print("💾 Storing odds data...")
        
        conn = sqlite3.connect(self.db_file)
        stored_count = 0
        
        for odds in odds_data:
            odds_id = f"{odds['game_id']}_{odds['bookmaker']}_{odds['market_type']}"
            
            # Check si odds ont changé
            cursor = conn.execute('''
                SELECT home_odds, away_odds FROM live_odds 
                WHERE odds_id = ?
            ''', (odds_id,))
            
            existing = cursor.fetchone()
            
            # Calculate movement
            movement = 0
            if existing:
                old_home, old_away = existing
                # Movement = somme des changements absolus
                movement = abs(odds['home_odds'] - old_home) + abs(odds['away_odds'] - old_away)
            
            # Insert/update live odds
            conn.execute('''
                INSERT OR REPLACE INTO live_odds
                (odds_id, game_id, bookmaker, home_odds, away_odds, 
                 home_team, away_team, game_date, market_type, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                odds_id, odds['game_id'], odds['bookmaker'],
                odds['home_odds'], odds['away_odds'],
                odds['home_team'], odds['away_team'],
                odds['game_date'], odds['market_type'],
                datetime.now().isoformat()
            ))
            
            # Insert history si mouvement significatif
            if movement > 5:  # Changement de 5+ points
                conn.execute('''
                    INSERT INTO odds_history
                    (game_id, bookmaker, home_odds, away_odds, 
                     market_type, timestamp, odds_movement)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    odds['game_id'], odds['bookmaker'],
                    odds['home_odds'], odds['away_odds'],
                    odds['market_type'], datetime.now().isoformat(),
                    movement
                ))
            
            stored_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ {stored_count} odds records stored")
        return stored_count
    
    def calculate_ev_vs_predictions(self, game_id: str = None) -> List[Dict]:
        """Calcule EV vs predictions trio"""
        
        print("📊 Calculating EV vs predictions...")
        
        conn = sqlite3.connect(self.db_file)
        
        # Query odds + predictions
        where_clause = "WHERE o.game_id = ?" if game_id else ""
        params = [game_id] if game_id else []
        
        cursor = conn.execute(f'''
            SELECT DISTINCT
                o.game_id,
                o.home_team,
                o.away_team,
                p.prediction_confidence,
                p.predicted_winner
            FROM live_odds o
            LEFT JOIN game_predictions p ON o.game_id = p.game_id
            {where_clause}
        ''', params)
        
        games_data = cursor.fetchall()
        
        ev_results = []
        
        for game_data in games_data:
            game_id, home_team, away_team, confidence, predicted_winner = game_data
            
            if not confidence:  # Pas de prédiction
                continue
            
            # Fetch best odds pour ce game
            cursor.execute('''
                SELECT 
                    MAX(home_odds) as best_home_odds,
                    MAX(away_odds) as best_away_odds,
                    bookmaker
                FROM live_odds
                WHERE game_id = ? AND market_type = 'h2h'
                GROUP BY game_id
            ''', (game_id,))
            
            odds_result = cursor.fetchone()
            if not odds_result:
                continue
                
            best_home_odds, best_away_odds, _ = odds_result
            
            # Convert confidence to probabilities
            if predicted_winner == 'home':
                prob_home = confidence
                prob_away = 1 - confidence
            else:
                prob_home = 1 - confidence  
                prob_away = confidence
            
            # Convert American odds to decimal
            def american_to_decimal(american_odds):
                if american_odds > 0:
                    return (american_odds / 100) + 1
                else:
                    return (100 / abs(american_odds)) + 1
            
            decimal_home = american_to_decimal(best_home_odds)
            decimal_away = american_to_decimal(best_away_odds)
            
            # Calculate EV
            ev_home = (prob_home * decimal_home) - 1
            ev_away = (prob_away * decimal_away) - 1
            
            # Recommendation
            min_ev_threshold = 0.05  # 5% EV minimum
            
            recommended_bet = None
            stake_suggestion = 0
            
            if ev_home > min_ev_threshold:
                recommended_bet = f"{home_team} ML"
                # Kelly fraction simplifiée: ev / odds
                stake_suggestion = min(ev_home * 100, 50)  # Max $50
            elif ev_away > min_ev_threshold:
                recommended_bet = f"{away_team} ML" 
                stake_suggestion = min(ev_away * 100, 50)
            
            ev_calc = {
                'game_id': game_id,
                'home_team': home_team,
                'away_team': away_team,
                'predicted_prob_home': prob_home,
                'predicted_prob_away': prob_away,
                'best_odds_home': best_home_odds,
                'best_odds_away': best_away_odds,
                'ev_home': ev_home,
                'ev_away': ev_away,
                'recommended_bet': recommended_bet,
                'stake_suggestion': stake_suggestion
            }
            
            # Store EV calculation
            conn.execute('''
                INSERT INTO ev_calculations
                (game_id, predicted_prob_home, predicted_prob_away,
                 best_odds_home, best_odds_away, ev_home, ev_away,
                 recommended_bet, stake_suggestion, calculated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_id, prob_home, prob_away,
                best_home_odds, best_away_odds, ev_home, ev_away,
                recommended_bet, stake_suggestion,
                datetime.now().isoformat()
            ))
            
            ev_results.append(ev_calc)
        
        conn.commit()
        conn.close()
        
        # Display results
        print(f"\n📈 EV ANALYSIS RESULTS:")
        for ev in ev_results:
            if ev['recommended_bet']:
                print(f"   🎯 {ev['game_id']}: {ev['recommended_bet']}")
                print(f"      EV Home: {ev['ev_home']:+.1%} | Away: {ev['ev_away']:+.1%}")
                print(f"      Suggested stake: ${ev['stake_suggestion']:.0f}")
        
        return ev_results
    
    def generate_odds_dashboard(self) -> str:
        """Génère dashboard odds HTML"""
        
        print("🖥️ Generating odds dashboard...")
        
        conn = sqlite3.connect(self.db_file)
        
        # Fetch current odds avec EV
        cursor = conn.execute('''
            SELECT 
                o.game_id,
                o.home_team,
                o.away_team,
                o.bookmaker,
                o.home_odds,
                o.away_odds,
                o.fetched_at,
                ev.ev_home,
                ev.ev_away,
                ev.recommended_bet,
                ev.stake_suggestion
            FROM live_odds o
            LEFT JOIN ev_calculations ev ON o.game_id = ev.game_id
            WHERE o.is_active = 1
            ORDER BY o.game_date, o.game_id, o.bookmaker
        ''')
        
        odds_data = cursor.fetchall()
        conn.close()
        
        # Generate HTML
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>🎰 NHL Odds Live Dashboard</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #1a1a2e; color: white; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .games-grid {{ display: grid; gap: 20px; }}
        .game-card {{ 
            background: #16213e; 
            border-radius: 10px; 
            padding: 15px; 
            border-left: 4px solid #0f4c75;
        }}
        .game-header {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        .odds-table {{ width: 100%; margin-top: 10px; }}
        .odds-table th, .odds-table td {{ 
            padding: 5px 10px; 
            text-align: center; 
            border: 1px solid #444;
        }}
        .positive-ev {{ background-color: #2d5a2d !important; color: #90ee90; }}
        .negative-ev {{ background-color: #5a2d2d !important; color: #ffcccb; }}
        .recommendation {{ 
            background: #ffd700; 
            color: #000; 
            padding: 5px 10px; 
            border-radius: 5px; 
            margin-top: 10px;
            font-weight: bold;
        }}
        .timestamp {{ color: #888; font-size: 12px; }}
    </style>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</head>
<body>
    <div class="header">
        <h1>🎰 NHL ODDS LIVE DASHBOARD</h1>
        <p class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="games-grid">
'''
        
        # Group by game
        games = {}
        for row in odds_data:
            game_id = row[0]
            if game_id not in games:
                games[game_id] = {
                    'home_team': row[1],
                    'away_team': row[2], 
                    'odds': [],
                    'ev_home': row[7],
                    'ev_away': row[8],
                    'recommendation': row[9],
                    'stake': row[10]
                }
            
            games[game_id]['odds'].append({
                'bookmaker': row[3],
                'home_odds': row[4],
                'away_odds': row[5]
            })
        
        for game_id, game_data in games.items():
            html += f'''
        <div class="game-card">
            <div class="game-header">
                {game_data['away_team']} @ {game_data['home_team']}
            </div>
            
            <table class="odds-table">
                <tr>
                    <th>Bookmaker</th>
                    <th>{game_data['away_team']}</th>
                    <th>{game_data['home_team']}</th>
                </tr>
'''
            
            for odds in game_data['odds']:
                home_class = "positive-ev" if game_data.get('ev_home', 0) > 0.05 else ""
                away_class = "positive-ev" if game_data.get('ev_away', 0) > 0.05 else ""
                
                html += f'''
                <tr>
                    <td>{odds['bookmaker']}</td>
                    <td class="{away_class}">{odds['away_odds']:+.0f}</td>
                    <td class="{home_class}">{odds['home_odds']:+.0f}</td>
                </tr>
'''
            
            html += '</table>'
            
            # EV info
            if game_data.get('ev_home') or game_data.get('ev_away'):
                html += f'''
            <div style="margin-top: 10px;">
                <small>EV: {game_data['home_team']} {game_data.get('ev_home', 0):+.1%} | 
                       {game_data['away_team']} {game_data.get('ev_away', 0):+.1%}</small>
            </div>
'''
            
            # Recommendation
            if game_data.get('recommendation'):
                html += f'''
            <div class="recommendation">
                💡 BET: {game_data['recommendation']} - ${game_data.get('stake', 0):.0f}
            </div>
'''
            
            html += '</div>'
        
        html += '''
    </div>
</body>
</html>
'''
        
        # Write dashboard
        dashboard_file = 'nhl_odds_live_dashboard.html'
        with open(dashboard_file, 'w') as f:
            f.write(html)
        
        print(f"✅ Dashboard généré: {dashboard_file}")
        return dashboard_file
    
    def run_live_odds_update(self, date_filter: str = None) -> Dict:
        """Run update odds live complet"""
        
        print("🎰 STARTING LIVE ODDS UPDATE")
        print("=" * 40)
        
        start_time = datetime.now()
        
        # 1. Fetch odds
        odds_result = self.fetch_nhl_odds(date_filter)
        
        # 2. Store odds
        stored_count = 0
        if odds_result.get('odds'):
            stored_count = self.store_odds(odds_result['odds'])
        
        # 3. Calculate EV
        ev_results = self.calculate_ev_vs_predictions()
        
        # 4. Generate dashboard
        dashboard_file = self.generate_odds_dashboard()
        
        # Summary
        duration = (datetime.now() - start_time).total_seconds()
        
        summary = {
            'duration_seconds': duration,
            'odds_fetched': len(odds_result.get('odds', [])),
            'odds_stored': stored_count,
            'ev_calculations': len(ev_results),
            'positive_ev_bets': len([ev for ev in ev_results if ev['recommended_bet']]),
            'dashboard_file': dashboard_file,
            'status': 'success'
        }
        
        print(f"\n🎉 ODDS UPDATE COMPLETE!")
        print(f"⏱️ Duration: {duration:.1f}s")
        print(f"🎰 Odds stored: {stored_count}")
        print(f"💰 Positive EV bets: {summary['positive_ev_bets']}")
        print(f"🖥️ Dashboard: {dashboard_file}")
        
        return summary

def main():
    """Main entry point"""
    
    import sys
    
    # Parse arguments
    batch_mode = '--batch' in sys.argv
    date_filter = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('--date='):
            date_filter = arg.split('=')[1]
    
    # Run odds update
    fetcher = LiveOddsFetcher()
    result = fetcher.run_live_odds_update(date_filter)
    
    if not batch_mode:
        print(f"\n📊 Results: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
