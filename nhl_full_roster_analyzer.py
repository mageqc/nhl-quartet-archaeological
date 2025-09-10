#!/usr/bin/env python3
"""
🏒 NHL FULL ROSTER ANALYZER - EXPANSION COMPLÈTE JOUEURS
Étend le système pour analyser TOUS les joueurs NHL (700+ joueurs)
Architecture: 32 équipes × 23 joueurs = ~736 joueurs minimum

OBJECTIFS:
✅ Charger roster complet de chaque équipe (forwards, défenseurs, gardiens)
✅ Statistiques détaillées par joueur (carrière + saison actuelle)
✅ Analyse props individuelles (buts, assists, points, tirs, etc.)
✅ Impact injuries précis par joueur
✅ Chemistry lines et powerplay units
✅ Prêt pour connexion NHL API réelle
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any

class NHLFullRosterAnalyzer:
    """
    🏆 ANALYSEUR ROSTER COMPLET NHL
    
    Charge et analyse 700+ joueurs NHL organisés par:
    - 32 équipes
    - 23 joueurs par équipe minimum
    - Toutes positions (F/D/G)
    - Stats carrière + actuelles
    - Props betting individuelles
    """
    
    def __init__(self):
        self.db_name = "nhl_full_roster_database.db"
        
        print("🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒")
        print("🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒                                                         🏒 NHL FULL ROSTER ANALYZER - EXPANSION COMPLÈTE 🏒")
        print("🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒")
        print("🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒🏒                                                         🎯 OBJECTIF: CHARGER 700+ JOUEURS NHL")
        print("📊 32 équipes × 23 joueurs = ~736 joueurs minimum")
        print("⚡ Stats complètes: Carrière + Saison actuelle")
        print("🎯 Props individuelles: Buts, Assists, Points, Tirs, TOI")
        print("💰 Prêt pour betting props précises sur chaque joueur")
        
        self.initialize_full_database()
        self.load_complete_nhl_rosters()
        
    def initialize_full_database(self):
        """Initialise la base de données pour 700+ joueurs"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Table équipes complète (32 équipes NHL)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nhl_teams (
                team_id TEXT PRIMARY KEY,
                team_name TEXT,
                city TEXT,
                conference TEXT,
                division TEXT,
                
                -- Roster info
                total_players INTEGER DEFAULT 23,
                forwards_count INTEGER DEFAULT 12,
                defensemen_count INTEGER DEFAULT 6,
                goalies_count INTEGER DEFAULT 2,
                
                -- Team stats
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                
                -- Metadonnées
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table joueurs complète (700+ joueurs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nhl_players (
                player_id TEXT PRIMARY KEY,
                team_id TEXT,
                player_name TEXT,
                jersey_number INTEGER,
                position TEXT,
                
                -- Données personnelles
                age INTEGER,
                height_inches INTEGER,
                weight_lbs INTEGER,
                shoots_catches TEXT,
                birth_country TEXT,
                
                -- Statistiques carrière
                career_seasons INTEGER DEFAULT 0,
                career_games INTEGER DEFAULT 0,
                career_goals INTEGER DEFAULT 0,
                career_assists INTEGER DEFAULT 0,
                career_points INTEGER DEFAULT 0,
                career_plus_minus INTEGER DEFAULT 0,
                career_pim INTEGER DEFAULT 0,
                
                -- Statistiques saison actuelle
                current_games INTEGER DEFAULT 0,
                current_goals INTEGER DEFAULT 0,
                current_assists INTEGER DEFAULT 0,
                current_points INTEGER DEFAULT 0,
                current_plus_minus INTEGER DEFAULT 0,
                current_pim INTEGER DEFAULT 0,
                current_shots INTEGER DEFAULT 0,
                current_toi_avg REAL DEFAULT 0.0,
                
                -- Stats spéciales gardiens
                career_wins INTEGER DEFAULT 0,
                career_losses INTEGER DEFAULT 0,
                career_gaa REAL DEFAULT 0.0,
                career_sv_pct REAL DEFAULT 0.0,
                career_shutouts INTEGER DEFAULT 0,
                
                -- Props betting metrics
                goals_per_game REAL DEFAULT 0.0,
                assists_per_game REAL DEFAULT 0.0,
                points_per_game REAL DEFAULT 0.0,
                shots_per_game REAL DEFAULT 0.0,
                toi_per_game REAL DEFAULT 0.0,
                
                -- Tendances performance
                hot_streak INTEGER DEFAULT 0,
                cold_streak INTEGER DEFAULT 0,
                injury_status TEXT DEFAULT 'HEALTHY',
                line_assignment TEXT DEFAULT 'UNKNOWN',
                pp_unit INTEGER DEFAULT 0,
                
                -- Facteurs prédictifs
                consistency_rating REAL DEFAULT 0.5,
                clutch_performance REAL DEFAULT 0.5,
                home_away_split REAL DEFAULT 1.0,
                
                FOREIGN KEY (team_id) REFERENCES nhl_teams (team_id)
            )
        ''')
        
        # Table matchups (chemistry entre joueurs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_chemistry (
                chemistry_id TEXT PRIMARY KEY,
                player1_id TEXT,
                player2_id TEXT,
                team_id TEXT,
                
                -- Chemistry metrics
                games_together INTEGER DEFAULT 0,
                points_together INTEGER DEFAULT 0,
                chemistry_rating REAL DEFAULT 0.5,
                line_effectiveness REAL DEFAULT 0.5,
                
                -- Contexte
                line_type TEXT DEFAULT 'UNKNOWN',
                last_game_together TEXT,
                
                FOREIGN KEY (player1_id) REFERENCES nhl_players (player_id),
                FOREIGN KEY (player2_id) REFERENCES nhl_players (player_id),
                FOREIGN KEY (team_id) REFERENCES nhl_teams (team_id)
            )
        ''')
        
        # Table props betting (pour chaque joueur)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_props (
                prop_id TEXT PRIMARY KEY,
                player_id TEXT,
                game_date TEXT,
                
                -- Props disponibles
                goals_line REAL DEFAULT 0.5,
                assists_line REAL DEFAULT 0.5,
                points_line REAL DEFAULT 0.5,
                shots_line REAL DEFAULT 2.5,
                toi_line REAL DEFAULT 15.0,
                
                -- Probabilités calculées
                goals_over_prob REAL DEFAULT 0.5,
                assists_over_prob REAL DEFAULT 0.5,
                points_over_prob REAL DEFAULT 0.5,
                shots_over_prob REAL DEFAULT 0.5,
                toi_over_prob REAL DEFAULT 0.5,
                
                -- Recommandations
                best_prop TEXT DEFAULT 'NONE',
                confidence_rating REAL DEFAULT 0.0,
                expected_value REAL DEFAULT 0.0,
                
                FOREIGN KEY (player_id) REFERENCES nhl_players (player_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de données Full Roster créée (prête pour 700+ joueurs)")
        
    def load_complete_nhl_rosters(self):
        """Charge les rosters complets des 32 équipes NHL"""
        print("\n🏒 CHARGEMENT ROSTERS COMPLETS NHL...")
        
        # D'abord charger les 32 équipes
        self.load_all_nhl_teams()
        
        # Ensuite charger tous les joueurs par équipe
        self.load_all_players_by_team()
        
        print("✅ Chargement complet terminé!")
        
    def load_all_nhl_teams(self):
        """Charge les 32 équipes NHL avec informations complètes"""
        nhl_teams = {
            # Atlantic Division
            'TOR': {'name': 'Toronto Maple Leafs', 'city': 'Toronto', 'conference': 'Eastern', 'division': 'Atlantic'},
            'BOS': {'name': 'Boston Bruins', 'city': 'Boston', 'conference': 'Eastern', 'division': 'Atlantic'},
            'FLA': {'name': 'Florida Panthers', 'city': 'Sunrise', 'conference': 'Eastern', 'division': 'Atlantic'},
            'TBL': {'name': 'Tampa Bay Lightning', 'city': 'Tampa Bay', 'conference': 'Eastern', 'division': 'Atlantic'},
            'BUF': {'name': 'Buffalo Sabres', 'city': 'Buffalo', 'conference': 'Eastern', 'division': 'Atlantic'},
            'MTL': {'name': 'Montreal Canadiens', 'city': 'Montreal', 'conference': 'Eastern', 'division': 'Atlantic'},
            'OTT': {'name': 'Ottawa Senators', 'city': 'Ottawa', 'conference': 'Eastern', 'division': 'Atlantic'},
            'DET': {'name': 'Detroit Red Wings', 'city': 'Detroit', 'conference': 'Eastern', 'division': 'Atlantic'},
            
            # Metropolitan Division
            'NYR': {'name': 'New York Rangers', 'city': 'New York', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'CAR': {'name': 'Carolina Hurricanes', 'city': 'Raleigh', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'NJD': {'name': 'New Jersey Devils', 'city': 'Newark', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'WSH': {'name': 'Washington Capitals', 'city': 'Washington', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'PHI': {'name': 'Philadelphia Flyers', 'city': 'Philadelphia', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'PIT': {'name': 'Pittsburgh Penguins', 'city': 'Pittsburgh', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'NYI': {'name': 'New York Islanders', 'city': 'Elmont', 'conference': 'Eastern', 'division': 'Metropolitan'},
            'CBJ': {'name': 'Columbus Blue Jackets', 'city': 'Columbus', 'conference': 'Eastern', 'division': 'Metropolitan'},
            
            # Central Division
            'COL': {'name': 'Colorado Avalanche', 'city': 'Denver', 'conference': 'Western', 'division': 'Central'},
            'DAL': {'name': 'Dallas Stars', 'city': 'Dallas', 'conference': 'Western', 'division': 'Central'},
            'WPG': {'name': 'Winnipeg Jets', 'city': 'Winnipeg', 'conference': 'Western', 'division': 'Central'},
            'NSH': {'name': 'Nashville Predators', 'city': 'Nashville', 'conference': 'Western', 'division': 'Central'},
            'MIN': {'name': 'Minnesota Wild', 'city': 'Saint Paul', 'conference': 'Western', 'division': 'Central'},
            'STL': {'name': 'St. Louis Blues', 'city': 'St. Louis', 'conference': 'Western', 'division': 'Central'},
            'UTA': {'name': 'Utah Hockey Club', 'city': 'Salt Lake City', 'conference': 'Western', 'division': 'Central'},
            'CHI': {'name': 'Chicago Blackhawks', 'city': 'Chicago', 'conference': 'Western', 'division': 'Central'},
            
            # Pacific Division
            'EDM': {'name': 'Edmonton Oilers', 'city': 'Edmonton', 'conference': 'Western', 'division': 'Pacific'},
            'VEG': {'name': 'Vegas Golden Knights', 'city': 'Las Vegas', 'conference': 'Western', 'division': 'Pacific'},
            'LAK': {'name': 'Los Angeles Kings', 'city': 'Los Angeles', 'conference': 'Western', 'division': 'Pacific'},
            'VAN': {'name': 'Vancouver Canucks', 'city': 'Vancouver', 'conference': 'Western', 'division': 'Pacific'},
            'CGY': {'name': 'Calgary Flames', 'city': 'Calgary', 'conference': 'Western', 'division': 'Pacific'},
            'SEA': {'name': 'Seattle Kraken', 'city': 'Seattle', 'conference': 'Western', 'division': 'Pacific'},
            'ANA': {'name': 'Anaheim Ducks', 'city': 'Anaheim', 'conference': 'Western', 'division': 'Pacific'},
            'SJS': {'name': 'San Jose Sharks', 'city': 'San Jose', 'conference': 'Western', 'division': 'Pacific'}
        }
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for team_id, info in nhl_teams.items():
            cursor.execute('''
                INSERT OR REPLACE INTO nhl_teams 
                (team_id, team_name, city, conference, division, total_players, forwards_count, defensemen_count, goalies_count)
                VALUES (?, ?, ?, ?, ?, 23, 12, 6, 2)
            ''', (team_id, info['name'], info['city'], info['conference'], info['division']))
        
        conn.commit()
        conn.close()
        print(f"✅ 32 équipes NHL chargées dans la base de données")
        
    def load_all_players_by_team(self):
        """Charge tous les joueurs pour chaque équipe (700+ joueurs total)"""
        
        # Ici on simule le chargement complet - dans la vraie vie, ceci viendrait de l'API NHL
        # Pour la démo, on va charger ~23 joueurs par équipe pour quelques équipes clés
        
        teams_to_load = ['TOR', 'EDM', 'BOS', 'COL', 'NYR', 'FLA', 'VEG', 'CAR']  # Exemple de 8 équipes
        total_players = 0
        
        for team_id in teams_to_load:
            players_loaded = self.load_team_full_roster(team_id)
            total_players += players_loaded
            print(f"   📊 {team_id}: {players_loaded} joueurs chargés")
        
        print(f"\n🏆 TOTAL JOUEURS CHARGÉS: {total_players}")
        print(f"🎯 Projection complète: 32 équipes × 23 joueurs = 736 joueurs")
        print(f"📈 Couverture actuelle: {total_players}/{736} = {(total_players/736)*100:.1f}%")
        
        return total_players
        
    def load_team_full_roster(self, team_id: str) -> int:
        """Charge le roster complet d'une équipe (23 joueurs)"""
        
        # Base de données simulée réaliste (à remplacer par vraie API NHL)
        sample_rosters = {
            'TOR': {
                'forwards': [
                    {'name': 'Auston Matthews', 'number': 34, 'pos': 'C', 'age': 27, 'goals': 40, 'assists': 35, 'games': 70},
                    {'name': 'Mitch Marner', 'number': 16, 'pos': 'RW', 'age': 27, 'goals': 25, 'assists': 55, 'games': 75},
                    {'name': 'William Nylander', 'number': 88, 'pos': 'RW', 'age': 28, 'goals': 35, 'assists': 45, 'games': 72},
                    {'name': 'John Tavares', 'number': 91, 'pos': 'C', 'age': 34, 'goals': 30, 'assists': 40, 'games': 68},
                    {'name': 'Matthew Knies', 'number': 23, 'pos': 'LW', 'age': 22, 'goals': 20, 'assists': 25, 'games': 65},
                    {'name': 'Max Domi', 'number': 11, 'pos': 'C', 'age': 29, 'goals': 15, 'assists': 30, 'games': 70},
                    {'name': 'Bobby McMann', 'number': 74, 'pos': 'LW', 'age': 27, 'goals': 12, 'assists': 18, 'games': 60},
                    {'name': 'Nicholas Robertson', 'number': 89, 'pos': 'LW', 'age': 23, 'goals': 10, 'assists': 15, 'games': 45},
                    {'name': 'Pontus Holmberg', 'number': 26, 'pos': 'C', 'age': 25, 'goals': 8, 'assists': 12, 'games': 55},
                    {'name': 'Connor Dewar', 'number': 17, 'pos': 'C', 'age': 25, 'goals': 6, 'assists': 10, 'games': 50},
                    {'name': 'Steven Lorentz', 'number': 18, 'pos': 'C', 'age': 28, 'goals': 5, 'assists': 8, 'games': 45},
                    {'name': 'David Kampf', 'number': 64, 'pos': 'C', 'age': 29, 'goals': 4, 'assists': 12, 'games': 60}
                ],
                'defensemen': [
                    {'name': 'Morgan Rielly', 'number': 44, 'pos': 'D', 'age': 30, 'goals': 8, 'assists': 45, 'games': 75},
                    {'name': 'Oliver Ekman-Larsson', 'number': 23, 'pos': 'D', 'age': 33, 'goals': 6, 'assists': 25, 'games': 70},
                    {'name': 'Jake McCabe', 'number': 22, 'pos': 'D', 'age': 31, 'goals': 4, 'assists': 20, 'games': 68},
                    {'name': 'Chris Tanev', 'number': 8, 'pos': 'D', 'age': 34, 'goals': 2, 'assists': 18, 'games': 72},
                    {'name': 'Timothy Liljegren', 'number': 37, 'pos': 'D', 'age': 25, 'goals': 3, 'assists': 15, 'games': 55},
                    {'name': 'Conor Timmins', 'number': 25, 'pos': 'D', 'age': 26, 'goals': 2, 'assists': 12, 'games': 40}
                ],
                'goalies': [
                    {'name': 'Joseph Woll', 'number': 60, 'pos': 'G', 'age': 26, 'wins': 25, 'losses': 15, 'gaa': 2.45, 'sv_pct': 0.920},
                    {'name': 'Anthony Stolarz', 'number': 41, 'pos': 'G', 'age': 30, 'wins': 20, 'losses': 12, 'gaa': 2.65, 'sv_pct': 0.915}
                ]
            },
            
            'EDM': {
                'forwards': [
                    {'name': 'Connor McDavid', 'number': 97, 'pos': 'C', 'age': 27, 'goals': 50, 'assists': 75, 'games': 76},
                    {'name': 'Leon Draisaitl', 'number': 29, 'pos': 'C', 'age': 29, 'goals': 45, 'assists': 65, 'games': 78},
                    {'name': 'Ryan Nugent-Hopkins', 'number': 93, 'pos': 'C', 'age': 31, 'goals': 25, 'assists': 50, 'games': 75},
                    {'name': 'Zach Hyman', 'number': 18, 'pos': 'LW', 'age': 32, 'goals': 35, 'assists': 30, 'games': 72},
                    {'name': 'Evander Kane', 'number': 91, 'pos': 'LW', 'age': 33, 'goals': 20, 'assists': 25, 'games': 55},
                    {'name': 'Jeff Skinner', 'number': 53, 'pos': 'LW', 'age': 32, 'goals': 28, 'assists': 22, 'games': 68},
                    {'name': 'Viktor Arvidsson', 'number': 33, 'pos': 'RW', 'age': 31, 'goals': 18, 'assists': 28, 'games': 65},
                    {'name': 'Adam Henrique', 'number': 14, 'pos': 'C', 'age': 34, 'goals': 15, 'assists': 25, 'games': 70},
                    {'name': 'Vasily Podkolzin', 'number': 92, 'pos': 'RW', 'age': 23, 'goals': 8, 'assists': 12, 'games': 45},
                    {'name': 'Connor Brown', 'number': 28, 'pos': 'RW', 'age': 30, 'goals': 10, 'assists': 18, 'games': 60},
                    {'name': 'Mattias Janmark', 'number': 13, 'pos': 'C', 'age': 31, 'goals': 12, 'assists': 15, 'games': 65},
                    {'name': 'Derek Ryan', 'number': 10, 'pos': 'C', 'age': 37, 'goals': 5, 'assists': 10, 'games': 50}
                ],
                'defensemen': [
                    {'name': 'Darnell Nurse', 'number': 25, 'pos': 'D', 'age': 29, 'goals': 6, 'assists': 35, 'games': 76},
                    {'name': 'Mattias Ekholm', 'number': 14, 'pos': 'D', 'age': 34, 'goals': 4, 'assists': 30, 'games': 78},
                    {'name': 'Evan Bouchard', 'number': 2, 'pos': 'D', 'age': 25, 'goals': 12, 'assists': 55, 'games': 75},
                    {'name': 'Brett Kulak', 'number': 27, 'pos': 'D', 'age': 30, 'goals': 3, 'assists': 20, 'games': 70},
                    {'name': 'Troy Stecher', 'number': 22, 'pos': 'D', 'age': 30, 'goals': 2, 'assists': 15, 'games': 60},
                    {'name': 'Ty Emberson', 'number': 5, 'pos': 'D', 'age': 24, 'goals': 1, 'assists': 8, 'games': 35}
                ],
                'goalies': [
                    {'name': 'Stuart Skinner', 'number': 74, 'pos': 'G', 'age': 26, 'wins': 30, 'losses': 20, 'gaa': 2.75, 'sv_pct': 0.910},
                    {'name': 'Calvin Pickard', 'number': 30, 'pos': 'G', 'age': 32, 'wins': 15, 'losses': 10, 'gaa': 2.90, 'sv_pct': 0.905}
                ]
            }
        }
        
        # Autres équipes avec rosters simulés (pour économiser l'espace)
        if team_id not in sample_rosters:
            # Générer roster simulé pour les autres équipes
            return self.generate_simulated_roster(team_id)
        
        roster = sample_rosters[team_id]
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        players_added = 0
        
        # Ajouter forwards
        for player in roster['forwards']:
            self.insert_player(cursor, team_id, player)
            players_added += 1
        
        # Ajouter defensemen
        for player in roster['defensemen']:
            self.insert_player(cursor, team_id, player)
            players_added += 1
            
        # Ajouter goalies
        for player in roster['goalies']:
            self.insert_player(cursor, team_id, player)
            players_added += 1
        
        conn.commit()
        conn.close()
        
        return players_added
    
    def insert_player(self, cursor, team_id: str, player_data: dict):
        """Insère un joueur dans la base de données avec stats complètes"""
        
        # Calculer les métriques par match
        games = player_data.get('games', 1)
        goals_per_game = player_data.get('goals', 0) / games if games > 0 else 0
        assists_per_game = player_data.get('assists', 0) / games if games > 0 else 0
        points_per_game = (player_data.get('goals', 0) + player_data.get('assists', 0)) / games if games > 0 else 0
        
        # Estimer shots per game basé sur position et performance
        if player_data['pos'] == 'G':
            shots_per_game = 0
            toi_per_game = 60.0 if games > 10 else 0  # Temps de jeu gardien
        elif player_data['pos'] == 'D':
            shots_per_game = max(1.5, goals_per_game * 8)  # Défenseurs tirent moins
            toi_per_game = 20.0 + (assists_per_game * 2)  # Plus d'assists = plus de TOI
        else:
            shots_per_game = max(2.0, goals_per_game * 5)  # Forwards tirent plus
            toi_per_game = 12.0 + (points_per_game * 3)  # Performance impact TOI
        
        # Player ID unique
        player_id = f"{team_id}_{player_data['name'].replace(' ', '_').replace('-', '_')}"
        
        cursor.execute('''
            INSERT OR REPLACE INTO nhl_players (
                player_id, team_id, player_name, jersey_number, position, age,
                current_games, current_goals, current_assists, current_points,
                goals_per_game, assists_per_game, points_per_game, shots_per_game, toi_per_game,
                
                -- Stats carrière simulées (à remplacer par vraies données)
                career_seasons, career_games, career_goals, career_assists, career_points,
                
                -- Stats gardiens si applicable
                career_wins, career_losses, career_gaa, career_sv_pct,
                
                -- Facteurs prédictifs
                consistency_rating, clutch_performance, injury_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_id, team_id, player_data['name'], player_data.get('number', 0), 
            player_data['pos'], player_data.get('age', 25),
            
            # Stats actuelles
            games, player_data.get('goals', 0), player_data.get('assists', 0),
            player_data.get('goals', 0) + player_data.get('assists', 0),
            
            # Métriques par match
            goals_per_game, assists_per_game, points_per_game, shots_per_game, toi_per_game,
            
            # Stats carrière simulées (âge - 18 = saisons approximatives)
            max(1, player_data.get('age', 25) - 18), 
            games * max(1, player_data.get('age', 25) - 18),
            player_data.get('goals', 0) * max(1, player_data.get('age', 25) - 18),
            player_data.get('assists', 0) * max(1, player_data.get('age', 25) - 18),
            (player_data.get('goals', 0) + player_data.get('assists', 0)) * max(1, player_data.get('age', 25) - 18),
            
            # Stats gardiens
            player_data.get('wins', 0), player_data.get('losses', 0),
            player_data.get('gaa', 0.0), player_data.get('sv_pct', 0.0),
            
            # Facteurs prédictifs
            0.7 if points_per_game > 0.8 else 0.5,  # Consistency basée sur performance
            0.8 if player_data.get('age', 25) > 28 else 0.6,  # Clutch basé sur expérience
            'HEALTHY'
        ))
    
    def generate_simulated_roster(self, team_id: str) -> int:
        """Génère un roster simulé réaliste pour équipes non détaillées"""
        
        # Roster template avec noms génériques mais stats réalistes
        forwards_template = [
            {'pos': 'C', 'goals': 35, 'assists': 45}, {'pos': 'LW', 'goals': 25, 'assists': 35},
            {'pos': 'RW', 'goals': 30, 'assists': 40}, {'pos': 'C', 'goals': 20, 'assists': 30},
            {'pos': 'LW', 'goals': 18, 'assists': 25}, {'pos': 'RW', 'goals': 15, 'assists': 28},
            {'pos': 'C', 'goals': 12, 'assists': 20}, {'pos': 'LW', 'goals': 10, 'assists': 15},
            {'pos': 'RW', 'goals': 8, 'assists': 18}, {'pos': 'C', 'goals': 6, 'assists': 12},
            {'pos': 'LW', 'goals': 5, 'assists': 10}, {'pos': 'RW', 'goals': 4, 'assists': 8}
        ]
        
        defensemen_template = [
            {'pos': 'D', 'goals': 8, 'assists': 40}, {'pos': 'D', 'goals': 6, 'assists': 30},
            {'pos': 'D', 'goals': 4, 'assists': 25}, {'pos': 'D', 'goals': 3, 'assists': 18},
            {'pos': 'D', 'goals': 2, 'assists': 15}, {'pos': 'D', 'goals': 1, 'assists': 10}
        ]
        
        goalies_template = [
            {'pos': 'G', 'wins': 28, 'losses': 18, 'gaa': 2.65, 'sv_pct': 0.915},
            {'pos': 'G', 'wins': 15, 'losses': 10, 'gaa': 2.85, 'sv_pct': 0.905}
        ]
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        players_added = 0
        
        # Générer forwards
        for i, template in enumerate(forwards_template):
            player_data = {
                'name': f"{team_id} Forward {i+1}",
                'number': i + 10,
                'pos': template['pos'],
                'age': 25 + (i % 10),  # Âges variés
                'goals': template['goals'],
                'assists': template['assists'],
                'games': 70 + (i % 10)
            }
            self.insert_player(cursor, team_id, player_data)
            players_added += 1
        
        # Générer défenseurs
        for i, template in enumerate(defensemen_template):
            player_data = {
                'name': f"{team_id} Defenseman {i+1}",
                'number': i + 2,
                'pos': template['pos'],
                'age': 26 + (i % 8),
                'goals': template['goals'],
                'assists': template['assists'],
                'games': 72 + (i % 8)
            }
            self.insert_player(cursor, team_id, player_data)
            players_added += 1
        
        # Générer gardiens
        for i, template in enumerate(goalies_template):
            player_data = {
                'name': f"{team_id} Goalie {i+1}",
                'number': 30 + i,
                'pos': template['pos'],
                'age': 27 + i * 3,
                'wins': template['wins'],
                'losses': template['losses'],
                'gaa': template['gaa'],
                'sv_pct': template['sv_pct'],
                'games': template['wins'] + template['losses']
            }
            self.insert_player(cursor, team_id, player_data)
            players_added += 1
        
        conn.commit()
        conn.close()
        
        return players_added
    
    def analyze_player_props(self, player_id: str, upcoming_opponent: str = None) -> dict:
        """Analyse des props individuelles pour un joueur spécifique"""
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Récupérer stats du joueur
        cursor.execute('''
            SELECT player_name, position, goals_per_game, assists_per_game, 
                   points_per_game, shots_per_game, consistency_rating, 
                   clutch_performance, injury_status, current_games
            FROM nhl_players WHERE player_id = ?
        ''', (player_id,))
        
        player_data = cursor.fetchone()
        if not player_data:
            return {'error': f'Joueur {player_id} non trouvé'}
        
        name, pos, gpg, apg, ppg, spg, consistency, clutch, injury, games = player_data
        
        # Analyser chaque type de prop
        props_analysis = {
            'player_name': name,
            'position': pos,
            'games_played': games,
            'injury_status': injury,
            
            'goals_analysis': {
                'season_average': round(gpg, 2),
                'recommended_line': max(0.5, round(gpg - 0.1, 1)),  # Légèrement sous moyenne
                'over_probability': min(0.95, consistency * 0.6 + gpg * 0.4),
                'confidence': 'HIGH' if consistency > 0.7 else 'MEDIUM'
            },
            
            'assists_analysis': {
                'season_average': round(apg, 2),
                'recommended_line': max(0.5, round(apg - 0.1, 1)),
                'over_probability': min(0.95, consistency * 0.5 + apg * 0.5),
                'confidence': 'HIGH' if pos in ['C', 'D'] and apg > 0.6 else 'MEDIUM'
            },
            
            'points_analysis': {
                'season_average': round(ppg, 2),
                'recommended_line': max(0.5, round(ppg - 0.2, 1)),
                'over_probability': min(0.95, (gpg + apg) * 0.6 + consistency * 0.4),
                'confidence': 'HIGH' if ppg > 1.0 else 'MEDIUM'
            },
            
            'shots_analysis': {
                'season_average': round(spg, 1),
                'recommended_line': max(1.5, round(spg - 0.5, 1)),
                'over_probability': min(0.95, spg * 0.3 + consistency * 0.7),
                'confidence': 'HIGH' if pos in ['C', 'LW', 'RW'] else 'LOW'
            }
        }
        
        # Déterminer meilleure prop
        best_prop = 'goals'
        best_confidence = props_analysis['goals_analysis']['over_probability']
        
        for prop_type in ['assists', 'points', 'shots']:
            prob = props_analysis[f'{prop_type}_analysis']['over_probability']
            if prob > best_confidence:
                best_confidence = prob
                best_prop = prop_type
        
        props_analysis['recommendation'] = {
            'best_prop': f"{best_prop}_over",
            'confidence': round(best_confidence, 3),
            'expected_value': max(0, (best_confidence - 0.52) * 2),  # EV vs ligne -110
            'bet_size': 'SMALL' if best_confidence < 0.65 else 'MEDIUM' if best_confidence < 0.75 else 'LARGE'
        }
        
        conn.close()
        return props_analysis
    
    def get_team_roster_summary(self, team_id: str) -> dict:
        """Résumé complet du roster d'une équipe"""
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Stats équipe globales
        cursor.execute('''
            SELECT COUNT(*) as total_players,
                   SUM(CASE WHEN position IN ('C', 'LW', 'RW') THEN 1 ELSE 0 END) as forwards,
                   SUM(CASE WHEN position = 'D' THEN 1 ELSE 0 END) as defensemen,
                   SUM(CASE WHEN position = 'G' THEN 1 ELSE 0 END) as goalies,
                   AVG(goals_per_game) as avg_goals_per_game,
                   AVG(assists_per_game) as avg_assists_per_game,
                   AVG(points_per_game) as avg_points_per_game
            FROM nhl_players WHERE team_id = ?
        ''', (team_id,))
        
        team_stats = cursor.fetchone()
        
        # Top scorers
        cursor.execute('''
            SELECT player_name, position, points_per_game, goals_per_game, assists_per_game
            FROM nhl_players WHERE team_id = ?
            ORDER BY points_per_game DESC LIMIT 5
        ''', (team_id,))
        
        top_scorers = cursor.fetchall()
        
        # Joueurs blessés
        cursor.execute('''
            SELECT player_name, position, injury_status
            FROM nhl_players WHERE team_id = ? AND injury_status != 'HEALTHY'
        ''', (team_id,))
        
        injured_players = cursor.fetchall()
        
        conn.close()
        
        return {
            'team_id': team_id,
            'roster_size': team_stats[0],
            'forwards': team_stats[1],
            'defensemen': team_stats[2],
            'goalies': team_stats[3],
            'team_averages': {
                'goals_per_game': round(team_stats[4] or 0, 2),
                'assists_per_game': round(team_stats[5] or 0, 2),
                'points_per_game': round(team_stats[6] or 0, 2)
            },
            'top_scorers': [
                {'name': player[0], 'pos': player[1], 'ppg': round(player[2], 2),
                 'gpg': round(player[3], 2), 'apg': round(player[4], 2)}
                for player in top_scorers
            ],
            'injuries': [
                {'name': player[0], 'pos': player[1], 'status': player[2]}
                for player in injured_players
            ]
        }
    
    def run_full_roster_analysis(self):
        """Lance une analyse complète du système full roster"""
        
        print(f"\n🏆 ANALYSE COMPLÈTE SYSTÈME FULL ROSTER")
        print("=" * 60)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Statistiques globales
        cursor.execute('SELECT COUNT(*) FROM nhl_teams')
        total_teams = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM nhl_players')
        total_players = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT position, COUNT(*) 
            FROM nhl_players 
            GROUP BY position
        ''')
        position_counts = dict(cursor.fetchall())
        
        print(f"📊 STATISTIQUES GLOBALES:")
        print(f"   🏒 Équipes chargées: {total_teams}/32")
        print(f"   👤 Joueurs chargés: {total_players}")
        print(f"   ⚡ Attaquants: {position_counts.get('C', 0) + position_counts.get('LW', 0) + position_counts.get('RW', 0)}")
        print(f"   🛡️ Défenseurs: {position_counts.get('D', 0)}")
        print(f"   🥅 Gardiens: {position_counts.get('G', 0)}")
        
        # Analyse par équipe
        print(f"\n📋 ANALYSE PAR ÉQUIPE:")
        cursor.execute('SELECT team_id FROM nhl_teams ORDER BY team_id')
        teams = cursor.fetchall()
        
        for (team_id,) in teams[:5]:  # Montrer 5 premières équipes
            summary = self.get_team_roster_summary(team_id)
            print(f"   🏒 {team_id}: {summary['roster_size']} joueurs "
                  f"({summary['forwards']}F, {summary['defensemen']}D, {summary['goalies']}G)")
            if summary['top_scorers']:
                top_player = summary['top_scorers'][0]
                print(f"      ⭐ Top scorer: {top_player['name']} ({top_player['ppg']} PPG)")
        
        # Exemples d'analyse props
        print(f"\n🎯 EXEMPLES ANALYSE PROPS:")
        cursor.execute('''
            SELECT player_id, player_name, points_per_game 
            FROM nhl_players 
            WHERE points_per_game > 1.0 
            ORDER BY points_per_game DESC 
            LIMIT 3
        ''')
        
        top_players = cursor.fetchall()
        
        for player_id, name, ppg in top_players:
            props = self.analyze_player_props(player_id)
            if 'recommendation' in props:
                rec = props['recommendation']
                print(f"   ⭐ {name}: Meilleur prop = {rec['best_prop']} "
                      f"(Conf: {rec['confidence']:.1%}, EV: {rec['expected_value']:.1%})")
        
        conn.close()
        
        # Projection complète
        print(f"\n🚀 PROJECTION COMPLÈTE NHL:")
        print(f"   🎯 Objectif: 32 équipes × 23 joueurs = 736 joueurs")
        print(f"   📈 Actuel: {total_players} joueurs ({(total_players/736)*100:.1f}%)")
        print(f"   🔗 Prêt connexion API NHL pour expansion complète")
        print(f"   💰 Props betting individuelles: {total_players} joueurs analysables")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"nhl_full_roster_analysis_{timestamp}.json"
        
        analysis_data = {
            'total_teams': total_teams,
            'total_players': total_players,
            'position_breakdown': position_counts,
            'completion_percentage': round((total_players/736)*100, 1),
            'timestamp': timestamp,
            'ready_for_api_expansion': True
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvé: {filename}")
        print(f"🏆 SYSTÈME FULL ROSTER ANALYSÉ!")
        
        return analysis_data

def main():
    """Point d'entrée principal du système full roster"""
    print("🚀 DÉMARRAGE NHL FULL ROSTER ANALYZER")
    
    try:
        analyzer = NHLFullRosterAnalyzer()
        results = analyzer.run_full_roster_analysis()
        
        print(f"\n✅ NHL FULL ROSTER ANALYZER TESTÉ!")
        print(f"🎯 Prêt pour expansion vers 700+ joueurs NHL!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
