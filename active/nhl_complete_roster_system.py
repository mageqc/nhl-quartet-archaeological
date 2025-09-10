#!/usr/bin/env python3
"""
🏒 NHL COMPLETE ROSTER DOWNLOADER & MONITOR
==============================================
📥 Download TOUS les rosters NHL 2025-26
🔄 Monitor échanges & transactions en temps réel
📊 Base de données complète pour analyse comparative
🚨 Alertes automatiques pour changements majeurs
"""

import requests
import sqlite3
from datetime import datetime, timedelta
import json
import time
from concurrent.futures import ThreadPoolExecutor
import hashlib

class NHLCompleteRosterSystem:
    def __init__(self):
        self.db_path = "nhl_complete_rosters.db"
        self.nhl_api_base = "https://api-web.nhle.com/v1"
        self.teams = {
            # Atlantic
            "BOS": "Boston Bruins", "BUF": "Buffalo Sabres", "DET": "Detroit Red Wings",
            "FLA": "Florida Panthers", "MTL": "Montreal Canadiens", "OTT": "Ottawa Senators",
            "TBL": "Tampa Bay Lightning", "TOR": "Toronto Maple Leafs",
            
            # Metropolitan  
            "CAR": "Carolina Hurricanes", "CBJ": "Columbus Blue Jackets", "NJD": "New Jersey Devils",
            "NYI": "New York Islanders", "NYR": "New York Rangers", "PHI": "Philadelphia Flyers",
            "PIT": "Pittsburgh Penguins", "WSH": "Washington Capitals",
            
            # Central
            "ARI": "Arizona Coyotes", "CHI": "Chicago Blackhawks", "COL": "Colorado Avalanche",
            "DAL": "Dallas Stars", "MIN": "Minnesota Wild", "NSH": "Nashville Predators",
            "STL": "St. Louis Blues", "WPG": "Winnipeg Jets",
            
            # Pacific
            "ANA": "Anaheim Ducks", "CGY": "Calgary Flames", "EDM": "Edmonton Oilers",
            "LAK": "Los Angeles Kings", "SJS": "San Jose Sharks", "SEA": "Seattle Kraken",
            "VAN": "Vancouver Canucks", "VGK": "Vegas Golden Knights"
        }
        self.init_complete_database()
        
    def init_complete_database(self):
        """🗄️ Base de données complète pour monitoring NHL"""
        conn = sqlite3.connect(self.db_path)
        
        # Table principale des joueurs
        conn.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY,
                name TEXT,
                team_code TEXT,
                position TEXT,
                jersey_number INTEGER,
                age INTEGER,
                height TEXT,
                weight TEXT,
                birthdate TEXT,
                nationality TEXT,
                shoots_catches TEXT,
                salary INTEGER,
                contract_years INTEGER,
                draft_year INTEGER,
                draft_round INTEGER,
                draft_position INTEGER,
                games_played INTEGER,
                goals INTEGER,
                assists INTEGER,
                points INTEGER,
                plus_minus INTEGER,
                pim INTEGER,
                last_updated TEXT,
                UNIQUE(player_id, team_code)
            )
        ''')
        
        # Table des transactions/échanges
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT,
                transaction_type TEXT,
                player_id INTEGER,
                player_name TEXT,
                from_team TEXT,
                to_team TEXT,
                details TEXT,
                trade_value TEXT,
                picks_involved TEXT,
                created_at TEXT
            )
        ''')
        
        # Table des snapshots roster (pour détecter changements)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS roster_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_code TEXT,
                roster_hash TEXT,
                player_count INTEGER,
                snapshot_date TEXT,
                changes_detected TEXT
            )
        ''')
        
        # Table des stats d'équipe calculées
        conn.execute('''
            CREATE TABLE IF NOT EXISTS team_analytics (
                team_code TEXT PRIMARY KEY,
                total_salary INTEGER,
                avg_age REAL,
                roster_strength REAL,
                offense_rating REAL,
                defense_rating REAL,
                goalie_rating REAL,
                prospect_factor REAL,
                injury_concern REAL,
                trade_rumors INTEGER,
                last_calculated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("🏗️ Complete NHL database initialized")
        
    def fetch_team_roster_api(self, team_code):
        """📥 Download roster complet d'une équipe via NHL API"""
        try:
            # API officielle NHL pour roster
            url = f"{self.nhl_api_base}/roster/{team_code}/20252026"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                players = []
                # Parse forwards
                for player in data.get('forwards', []):
                    players.append(self.parse_player_data(player, team_code, 'F'))
                
                # Parse defensemen
                for player in data.get('defensemen', []):
                    players.append(self.parse_player_data(player, team_code, 'D'))
                
                # Parse goalies
                for player in data.get('goalies', []):
                    players.append(self.parse_player_data(player, team_code, 'G'))
                
                print(f"✅ {team_code}: {len(players)} players downloaded")
                return players
                
            else:
                print(f"⚠️ {team_code}: API error {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ {team_code}: Error {str(e)}")
            return []
    
    def parse_player_data(self, player_json, team_code, position_override=None):
        """🔧 Parse les données joueur depuis l'API NHL"""
        return {
            'player_id': player_json.get('id'),
            'name': f"{player_json.get('firstName', {}).get('default', '')} {player_json.get('lastName', {}).get('default', '')}".strip(),
            'team_code': team_code,
            'position': position_override or player_json.get('positionCode', ''),
            'jersey_number': player_json.get('sweaterNumber'),
            'age': self.calculate_age(player_json.get('birthDate')),
            'height': player_json.get('heightInCentimeters'),
            'weight': player_json.get('weightInKilograms'),
            'birthdate': player_json.get('birthDate'),
            'nationality': player_json.get('birthCountry'),
            'shoots_catches': player_json.get('shootsCatches'),
            'last_updated': datetime.now().isoformat()
        }
    
    def calculate_age(self, birthdate_str):
        """📅 Calcule l'âge à partir de la date de naissance"""
        if not birthdate_str:
            return None
        try:
            birth_date = datetime.strptime(birthdate_str, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return None
    
    def download_all_rosters(self):
        """🌐 Download TOUS les rosters NHL en parallèle"""
        print(f"🚀 Starting complete NHL rosters download - {len(self.teams)} teams")
        
        start_time = time.time()
        all_players = []
        
        # Download en parallèle pour speed
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_team = {
                executor.submit(self.fetch_team_roster_api, team_code): team_code 
                for team_code in self.teams.keys()
            }
            
            for future in future_to_team:
                team_code = future_to_team[future]
                try:
                    players = future.result()
                    all_players.extend(players)
                except Exception as e:
                    print(f"❌ {team_code} failed: {e}")
        
        # Sauvegarde en base
        self.save_all_players(all_players)
        
        duration = time.time() - start_time
        print(f"✅ Complete download finished: {len(all_players)} players in {duration:.1f}s")
        
        return all_players
    
    def save_all_players(self, players_list):
        """💾 Sauvegarde tous les joueurs en base"""
        conn = sqlite3.connect(self.db_path)
        
        for player in players_list:
            conn.execute('''
                INSERT OR REPLACE INTO players 
                (player_id, name, team_code, position, jersey_number, age, height, weight, 
                 birthdate, nationality, shoots_catches, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player['player_id'], player['name'], player['team_code'], player['position'],
                player['jersey_number'], player['age'], player['height'], player['weight'],
                player['birthdate'], player['nationality'], player['shoots_catches'],
                player['last_updated']
            ))
        
        conn.commit()
        conn.close()
        
    def detect_roster_changes(self, team_code):
        """🔍 Détecte les changements de roster depuis le dernier snapshot"""
        current_roster = self.fetch_team_roster_api(team_code)
        current_hash = self.calculate_roster_hash(current_roster)
        
        conn = sqlite3.connect(self.db_path)
        
        # Récupère le dernier snapshot
        cursor = conn.execute('''
            SELECT roster_hash, snapshot_date FROM roster_snapshots 
            WHERE team_code = ? ORDER BY snapshot_date DESC LIMIT 1
        ''', (team_code,))
        
        last_snapshot = cursor.fetchone()
        
        changes = []
        if last_snapshot and last_snapshot[0] != current_hash:
            # Changements détectés !
            changes = self.analyze_roster_differences(team_code, current_roster)
            
            # Log les changements
            for change in changes:
                self.log_transaction(change)
        
        # Sauvegarde nouveau snapshot
        conn.execute('''
            INSERT INTO roster_snapshots (team_code, roster_hash, player_count, snapshot_date)
            VALUES (?, ?, ?, ?)
        ''', (team_code, current_hash, len(current_roster), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return changes
    
    def calculate_roster_hash(self, roster):
        """🔐 Calcule un hash du roster pour détecter les changements"""
        roster_string = json.dumps(sorted([
            f"{p['player_id']}:{p['name']}:{p['team_code']}" 
            for p in roster
        ]))
        return hashlib.md5(roster_string.encode()).hexdigest()
    
    def analyze_roster_differences(self, team_code, current_roster):
        """📊 Analyse les différences de roster"""
        conn = sqlite3.connect(self.db_path)
        
        # Récupère l'ancien roster
        cursor = conn.execute('''
            SELECT player_id, name FROM players WHERE team_code = ?
        ''', (team_code,))
        
        old_players = {row[0]: row[1] for row in cursor.fetchall()}
        current_players = {p['player_id']: p['name'] for p in current_roster}
        
        changes = []
        
        # Joueurs ajoutés
        for player_id, name in current_players.items():
            if player_id not in old_players:
                changes.append({
                    'type': 'ADDED',
                    'player_id': player_id,
                    'player_name': name,
                    'team': team_code,
                    'date': datetime.now().isoformat()
                })
        
        # Joueurs retirés  
        for player_id, name in old_players.items():
            if player_id not in current_players:
                changes.append({
                    'type': 'REMOVED',
                    'player_id': player_id,
                    'player_name': name,
                    'team': team_code,
                    'date': datetime.now().isoformat()
                })
        
        conn.close()
        return changes
    
    def log_transaction(self, change_data):
        """📝 Log une transaction/changement"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO transactions 
            (transaction_date, transaction_type, player_id, player_name, to_team, details, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            change_data['date'], change_data['type'], change_data['player_id'],
            change_data['player_name'], change_data['team'], 
            json.dumps(change_data), datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    
    def monitor_all_teams(self):
        """🔄 Monitor tous les rosters pour détecter les changements"""
        print("🔍 Starting NHL-wide roster monitoring...")
        
        all_changes = []
        for team_code in self.teams.keys():
            changes = self.detect_roster_changes(team_code)
            if changes:
                print(f"🚨 {team_code}: {len(changes)} changes detected!")
                all_changes.extend(changes)
            else:
                print(f"✅ {team_code}: No changes")
            
            time.sleep(0.5)  # Rate limiting
        
        return all_changes
    
    def get_team_comparison(self, team1, team2):
        """⚔️ Compare deux équipes avec données complètes"""
        conn = sqlite3.connect(self.db_path)
        
        def get_team_stats(team_code):
            cursor = conn.execute('''
                SELECT COUNT(*), AVG(age), position FROM players 
                WHERE team_code = ? 
                GROUP BY position
            ''', (team_code,))
            
            stats = {'F': 0, 'D': 0, 'G': 0, 'avg_age': 0}
            for count, avg_age, pos in cursor.fetchall():
                stats[pos] = count
                stats['avg_age'] += avg_age
            
            return stats
        
        team1_stats = get_team_stats(team1)
        team2_stats = get_team_stats(team2)
        
        conn.close()
        
        return {
            'team1': {'code': team1, 'stats': team1_stats},
            'team2': {'code': team2, 'stats': team2_stats},
            'comparison_date': datetime.now().isoformat()
        }
    
    def get_recent_transactions(self, days=7):
        """📰 Récupère les transactions récentes"""
        conn = sqlite3.connect(self.db_path)
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor = conn.execute('''
            SELECT * FROM transactions 
            WHERE created_at > ? 
            ORDER BY created_at DESC
        ''', (since_date,))
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'id': row[0], 'date': row[1], 'type': row[2],
                'player_name': row[4], 'team': row[6], 'details': row[7]
            })
        
        conn.close()
        return transactions

# Test du système complet
if __name__ == "__main__":
    print("🏒 NHL COMPLETE ROSTER SYSTEM - Starting...")
    
    system = NHLCompleteRosterSystem()
    
    print("\n1️⃣ Downloading all NHL rosters...")
    all_players = system.download_all_rosters()
    
    print(f"\n2️⃣ Total players in database: {len(all_players)}")
    
    print("\n3️⃣ Testing team comparison (MTL vs TOR)...")
    comparison = system.get_team_comparison("MTL", "TOR")
    print(f"MTL: {comparison['team1']['stats']}")
    print(f"TOR: {comparison['team2']['stats']}")
    
    print("\n4️⃣ Monitoring for changes...")
    changes = system.monitor_all_teams()
    print(f"Changes detected: {len(changes)}")
    
    print("\n✅ Complete NHL roster system ready!")
    print("📊 Use this for real-time roster analysis & transaction monitoring")
