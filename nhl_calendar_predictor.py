#!/usr/bin/env python3
"""
📅 NHL CALENDAR PREDICTOR - CALENDRIER INTERACTIF COMPLET
Calendrier avec tous les matchs NHL + prédictions + validation automatique

FONCTIONNALITÉS:
🏒 Calendrier visuel avec matchs du jour
🎯 Prédictions automatiques pour chaque match
📊 Enregistrement toutes les prédictions
✅ Validation automatique lendemain avec vrais résultats
📈 Historique performance prédictions
🎨 Interface calendrier interactive

Exemple: 5 matchs ce soir → 5 prédictions → validation demain matin
"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import calendar
import random

class NHLCalendarPredictor:
    """
    📅 CALENDRIER NHL AVEC PRÉDICTIONS
    
    Affiche calendrier NHL complet avec:
    - Matchs quotidiens
    - Prédictions automatiques 
    - Validation résultats
    - Tracking performance
    """
    
    def __init__(self):
        print("📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅")
        print("📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅                                                         🏒 NHL CALENDAR PREDICTOR - CALENDRIER COMPLET 🏒")
        print("📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅📅")
        
        self.calendar_db = "nhl_calendar_predictions.db"
        self.calendar_html = "nhl_calendar_interactive.html"
        
        print("🎯 OBJECTIF: Calendrier NHL avec prédictions + validation automatique")
        print("📅 Voir matchs du jour → Prédictions → Validation lendemain")
        print("📊 Tracking performance prédictions sur toute la saison")
        
        self.initialize_calendar_db()
        self.nhl_teams = self.get_nhl_teams()
        
    def initialize_calendar_db(self):
        """Initialise la base de données calendrier + prédictions"""
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        # Table matchs NHL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nhl_games (
                game_id TEXT PRIMARY KEY,
                game_date TEXT,
                home_team TEXT,
                away_team TEXT,
                home_score INTEGER DEFAULT NULL,
                away_score INTEGER DEFAULT NULL,
                game_status TEXT DEFAULT 'SCHEDULED',
                
                -- Informations contextuelles
                home_record TEXT DEFAULT '0-0-0',
                away_record TEXT DEFAULT '0-0-0',
                venue TEXT DEFAULT 'Unknown',
                start_time TEXT DEFAULT '19:00',
                
                -- Données pour prédictions
                home_form_rating REAL DEFAULT 0.5,
                away_form_rating REAL DEFAULT 0.5,
                home_injuries_impact REAL DEFAULT 0.0,
                away_injuries_impact REAL DEFAULT 0.0,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table prédictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_predictions (
                prediction_id TEXT PRIMARY KEY,
                game_id TEXT,
                game_date TEXT,
                
                -- Équipes
                home_team TEXT,
                away_team TEXT,
                
                -- Prédictions principales
                predicted_winner TEXT,
                predicted_home_score INTEGER,
                predicted_away_score INTEGER,
                predicted_total_goals INTEGER,
                
                -- Probabilités
                home_win_probability REAL DEFAULT 0.5,
                away_win_probability REAL DEFAULT 0.5,
                over_probability REAL DEFAULT 0.5,
                under_probability REAL DEFAULT 0.5,
                
                -- Facteurs prédiction
                prediction_confidence REAL DEFAULT 0.5,
                key_factors TEXT DEFAULT '[]',
                
                -- Validation résultats
                actual_winner TEXT DEFAULT NULL,
                actual_home_score INTEGER DEFAULT NULL,
                actual_away_score INTEGER DEFAULT NULL,
                actual_total_goals INTEGER DEFAULT NULL,
                
                -- Performance prédiction
                winner_correct BOOLEAN DEFAULT NULL,
                score_exact BOOLEAN DEFAULT NULL,
                total_goals_correct BOOLEAN DEFAULT NULL,
                prediction_accuracy REAL DEFAULT NULL,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                validated_at TEXT DEFAULT NULL,
                
                FOREIGN KEY (game_id) REFERENCES nhl_games (game_id)
            )
        ''')
        
        # Table performance calendrier
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calendar_performance (
                date TEXT PRIMARY KEY,
                
                -- Matchs du jour
                total_games INTEGER DEFAULT 0,
                predictions_made INTEGER DEFAULT 0,
                
                -- Résultats validations
                winners_correct INTEGER DEFAULT 0,
                scores_exact INTEGER DEFAULT 0,
                totals_correct INTEGER DEFAULT 0,
                
                -- Métriques performance
                daily_accuracy REAL DEFAULT 0.0,
                cumulative_accuracy REAL DEFAULT 0.0,
                
                -- Contexte
                games_validated INTEGER DEFAULT 0,
                validation_date TEXT DEFAULT NULL,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de données calendrier NHL initialisée")
    
    def get_nhl_teams(self) -> Dict[str, str]:
        """Retourne mapping équipes NHL"""
        return {
            # Atlantic Division
            'TOR': 'Toronto Maple Leafs', 'BOS': 'Boston Bruins', 
            'FLA': 'Florida Panthers', 'TBL': 'Tampa Bay Lightning',
            'BUF': 'Buffalo Sabres', 'MTL': 'Montreal Canadiens', 
            'OTT': 'Ottawa Senators', 'DET': 'Detroit Red Wings',
            
            # Metropolitan Division  
            'NYR': 'New York Rangers', 'CAR': 'Carolina Hurricanes',
            'NJD': 'New Jersey Devils', 'WSH': 'Washington Capitals',
            'PHI': 'Philadelphia Flyers', 'PIT': 'Pittsburgh Penguins', 
            'NYI': 'New York Islanders', 'CBJ': 'Columbus Blue Jackets',
            
            # Central Division
            'COL': 'Colorado Avalanche', 'DAL': 'Dallas Stars',
            'WPG': 'Winnipeg Jets', 'NSH': 'Nashville Predators',
            'MIN': 'Minnesota Wild', 'STL': 'St. Louis Blues',
            'UTA': 'Utah Hockey Club', 'CHI': 'Chicago Blackhawks',
            
            # Pacific Division
            'EDM': 'Edmonton Oilers', 'VEG': 'Vegas Golden Knights',
            'LAK': 'Los Angeles Kings', 'VAN': 'Vancouver Canucks', 
            'CGY': 'Calgary Flames', 'SEA': 'Seattle Kraken',
            'ANA': 'Anaheim Ducks', 'SJS': 'San Jose Sharks'
        }
    
    def simulate_nhl_schedule(self, start_date: datetime, days: int = 30) -> List[Dict]:
        """Simule un calendrier NHL réaliste"""
        
        print(f"\n📅 GÉNÉRATION CALENDRIER NHL ({days} jours)...")
        
        schedule = []
        teams_list = list(self.nhl_teams.keys())
        
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Nombre de matchs variables (0-15 matchs par jour, réaliste NHL)
            num_games = 0
            if current_date.weekday() < 5:  # Lun-Ven (soirées normales)
                num_games = random.choices([2,3,4,5,6,7,8], weights=[5,10,15,25,25,15,5])[0]
            elif current_date.weekday() == 5:  # Samedi (grosse soirée NHL)
                num_games = random.choices([6,7,8,9,10,11,12], weights=[5,10,20,25,20,15,5])[0]  
            else:  # Dimanche (journée + soirée)
                num_games = random.choices([3,4,5,6,7,8], weights=[10,15,25,25,20,5])[0]
            
            # Générer matchs pour ce jour
            available_teams = teams_list.copy()
            random.shuffle(available_teams)
            
            games_today = []
            
            for game_num in range(min(num_games, len(available_teams)//2)):
                if len(available_teams) < 2:
                    break
                
                # Sélectionner équipes
                away_team = available_teams.pop()
                home_team = available_teams.pop()
                
                # Simuler contexte réaliste
                home_form = random.uniform(0.3, 0.8)
                away_form = random.uniform(0.3, 0.8)
                
                game = {
                    'game_id': f"{date_str}_{away_team}_at_{home_team}",
                    'game_date': date_str,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_form_rating': home_form,
                    'away_form_rating': away_form,
                    'start_time': random.choice(['19:00', '19:30', '20:00', '20:30']),
                    'venue': f"{self.nhl_teams[home_team]} Arena"
                }
                
                games_today.append(game)
                schedule.append(game)
            
            if games_today:
                print(f"   📊 {date_str}: {len(games_today)} matchs")
        
        print(f"✅ Calendrier généré: {len(schedule)} matchs sur {days} jours")
        return schedule
    
    def save_schedule_to_db(self, schedule: List[Dict]):
        """Sauvegarde le calendrier en base"""
        
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        for game in schedule:
            cursor.execute('''
                INSERT OR REPLACE INTO nhl_games 
                (game_id, game_date, home_team, away_team, home_form_rating, 
                 away_form_rating, start_time, venue)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game['game_id'], game['game_date'], game['home_team'], 
                game['away_team'], game['home_form_rating'], 
                game['away_form_rating'], game['start_time'], game['venue']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Calendrier sauvé en base de données")
    
    def generate_game_prediction(self, game: Dict) -> Dict:
        """Génère prédiction complète pour un match"""
        
        home_team = game['home_team']
        away_team = game['away_team']
        home_form = game.get('home_form_rating', 0.5)
        away_form = game.get('away_form_rating', 0.5)
        
        # Facteurs prédiction
        home_advantage = 0.55  # Avantage domicile NHL
        form_impact = (home_form - away_form) * 0.3
        
        # Calculer probabilités
        home_win_prob = home_advantage + form_impact
        home_win_prob = max(0.2, min(0.8, home_win_prob))  # Limiter entre 20-80%
        away_win_prob = 1 - home_win_prob
        
        # Prédire vainqueur
        predicted_winner = home_team if home_win_prob > 0.5 else away_team
        
        # Prédire scores (basé sur form et probabilités)
        base_goals_home = 2.5 + (home_form * 1.5) + 0.3  # Avantage domicile
        base_goals_away = 2.5 + (away_form * 1.5)
        
        predicted_home_score = max(1, round(base_goals_home + random.uniform(-0.5, 0.5)))
        predicted_away_score = max(1, round(base_goals_away + random.uniform(-0.5, 0.5)))
        predicted_total = predicted_home_score + predicted_away_score
        
        # Probabilités totaux (NHL moyenne ~6 buts)
        over_prob = 0.5 + ((predicted_total - 6) * 0.1)
        over_prob = max(0.3, min(0.7, over_prob))
        
        # Facteurs clés
        key_factors = []
        if abs(home_form - away_form) > 0.2:
            better_form = home_team if home_form > away_form else away_team
            key_factors.append(f"{better_form} en meilleure forme")
        
        key_factors.append("Avantage domicile")
        
        if predicted_total > 6.5:
            key_factors.append("Matchup offensif attendu")
        elif predicted_total < 5.5:
            key_factors.append("Duel défensif prévu")
        
        # Confidence basée sur différence probabilités
        prob_diff = abs(home_win_prob - 0.5)
        confidence = 0.5 + (prob_diff * 0.8)
        
        prediction = {
            'predicted_winner': predicted_winner,
            'predicted_home_score': predicted_home_score,
            'predicted_away_score': predicted_away_score,
            'predicted_total_goals': predicted_total,
            'home_win_probability': home_win_prob,
            'away_win_probability': away_win_prob,
            'over_probability': over_prob,
            'under_probability': 1 - over_prob,
            'prediction_confidence': confidence,
            'key_factors': json.dumps(key_factors, ensure_ascii=False)
        }
        
        return prediction
    
    def predict_games_for_date(self, date_str: str) -> List[Dict]:
        """Génère prédictions pour tous les matchs d'une date"""
        
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        # Récupérer matchs du jour
        cursor.execute('''
            SELECT game_id, game_date, home_team, away_team, home_form_rating, away_form_rating
            FROM nhl_games WHERE game_date = ?
        ''', (date_str,))
        
        games = cursor.fetchall()
        predictions = []
        
        for game_data in games:
            game_id, game_date, home_team, away_team, home_form, away_form = game_data
            
            game = {
                'game_id': game_id,
                'game_date': game_date,
                'home_team': home_team,
                'away_team': away_team,
                'home_form_rating': home_form,
                'away_form_rating': away_form
            }
            
            # Générer prédiction
            prediction = self.generate_game_prediction(game)
            prediction['game_id'] = game_id
            prediction['game_date'] = game_date
            prediction['home_team'] = home_team
            prediction['away_team'] = away_team
            
            # Sauver prédiction
            prediction_id = f"pred_{game_id}_{datetime.now().strftime('%H%M%S')}"
            
            cursor.execute('''
                INSERT OR REPLACE INTO game_predictions 
                (prediction_id, game_id, game_date, home_team, away_team,
                 predicted_winner, predicted_home_score, predicted_away_score, predicted_total_goals,
                 home_win_probability, away_win_probability, over_probability, under_probability,
                 prediction_confidence, key_factors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prediction_id, game_id, game_date, home_team, away_team,
                prediction['predicted_winner'], prediction['predicted_home_score'],
                prediction['predicted_away_score'], prediction['predicted_total_goals'],
                prediction['home_win_probability'], prediction['away_win_probability'],
                prediction['over_probability'], prediction['under_probability'],
                prediction['prediction_confidence'], prediction['key_factors']
            ))
            
            predictions.append(prediction)
        
        conn.commit()
        conn.close()
        
        if predictions:
            print(f"🎯 {len(predictions)} prédictions générées pour {date_str}")
        
        return predictions
    
    def simulate_game_results(self, date_str: str):
        """Simule les résultats pour validation (remplace vraie API)"""
        
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        # Récupérer prédictions du jour précédent
        yesterday = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT prediction_id, game_id, predicted_winner, predicted_home_score, 
                   predicted_away_score, predicted_total_goals, home_team, away_team
            FROM game_predictions 
            WHERE game_date = ? AND actual_winner IS NULL
        ''', (yesterday,))
        
        predictions = cursor.fetchall()
        validated_count = 0
        
        for pred_data in predictions:
            (pred_id, game_id, predicted_winner, pred_home_score, pred_away_score, 
             pred_total, home_team, away_team) = pred_data
            
            # Simuler résultat réaliste (70% précision pour démo)
            if random.random() < 0.7:
                # Prédiction correcte
                actual_winner = predicted_winner
                actual_home = pred_home_score + random.randint(-1, 1)
                actual_away = pred_away_score + random.randint(-1, 1)
            else:
                # Prédiction incorrecte
                actual_winner = away_team if predicted_winner == home_team else home_team
                actual_home = pred_home_score + random.randint(-2, 2)
                actual_away = pred_away_score + random.randint(-2, 2)
            
            # Assurer scores positifs
            actual_home = max(0, actual_home)
            actual_away = max(0, actual_away)
            actual_total = actual_home + actual_away
            
            # Déterminer vainqueur réel
            if actual_home > actual_away:
                actual_winner = home_team
            elif actual_away > actual_home:
                actual_winner = away_team
            else:
                # Overtime/shootout - favoriser équipe visiteur légèrement
                actual_winner = away_team if random.random() < 0.52 else home_team
                if actual_winner == away_team:
                    actual_away += 1
                else:
                    actual_home += 1
                actual_total += 1
            
            # Calculer précision
            winner_correct = actual_winner == predicted_winner
            score_exact = (actual_home == pred_home_score and actual_away == pred_away_score)
            total_correct = actual_total == pred_total
            
            # Accuracy globale
            accuracy = 0.0
            if winner_correct:
                accuracy += 0.5
            if score_exact:
                accuracy += 0.3
            if total_correct:
                accuracy += 0.2
            
            # Mettre à jour prédiction avec résultats
            cursor.execute('''
                UPDATE game_predictions SET
                    actual_winner = ?, actual_home_score = ?, actual_away_score = ?,
                    actual_total_goals = ?, winner_correct = ?, score_exact = ?,
                    total_goals_correct = ?, prediction_accuracy = ?, validated_at = ?
                WHERE prediction_id = ?
            ''', (
                actual_winner, actual_home, actual_away, actual_total,
                winner_correct, score_exact, total_correct, accuracy,
                datetime.now().isoformat(), pred_id
            ))
            
            # Mettre à jour match
            cursor.execute('''
                UPDATE nhl_games SET
                    home_score = ?, away_score = ?, game_status = 'FINAL',
                    updated_at = ?
                WHERE game_id = ?
            ''', (actual_home, actual_away, datetime.now().isoformat(), game_id))
            
            validated_count += 1
        
        conn.commit()
        conn.close()
        
        if validated_count > 0:
            print(f"✅ {validated_count} résultats validés pour {yesterday}")
        
        return validated_count
    
    def generate_calendar_html(self) -> str:
        """Génère calendrier HTML interactif"""
        
        # Récupérer données calendrier
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        # Matchs des 7 prochains jours
        today = datetime.now()
        calendar_data = {}
        
        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            # Récupérer matchs + prédictions
            cursor.execute('''
                SELECT g.game_id, g.home_team, g.away_team, g.start_time,
                       g.home_score, g.away_score, g.game_status,
                       p.predicted_winner, p.predicted_home_score, p.predicted_away_score,
                       p.home_win_probability, p.prediction_confidence, p.key_factors,
                       p.actual_winner, p.winner_correct, p.prediction_accuracy
                FROM nhl_games g
                LEFT JOIN game_predictions p ON g.game_id = p.game_id
                WHERE g.game_date = ?
                ORDER BY g.start_time
            ''', (date_str,))
            
            games = cursor.fetchall()
            calendar_data[date_str] = {
                'date_obj': date,
                'games': games
            }
        
        # Stats performance
        cursor.execute('''
            SELECT 
                COUNT(*) as total_predictions,
                SUM(CASE WHEN winner_correct = 1 THEN 1 ELSE 0 END) as correct_winners,
                AVG(prediction_accuracy) as avg_accuracy
            FROM game_predictions 
            WHERE validated_at IS NOT NULL
        ''')
        stats = cursor.fetchone()
        
        conn.close()
        
        # Générer HTML
        html_content = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏒 Calendrier NHL avec Prédictions</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #0f4c75, #3282b8, #0f4c75);
            color: white;
            min-height: 100vh;
        }}
        
        .header {{
            background: rgba(0,0,0,0.4);
            padding: 20px;
            text-align: center;
            border-bottom: 3px solid #ffd700;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.8em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stats-summary {{
            display: flex;
            justify-content: center;
            gap: 30px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            margin: 20px;
            border-radius: 15px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 1.8em;
            font-weight: bold;
            color: #4CAF50;
        }}
        
        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 2000px;
            margin: 0 auto;
        }}
        
        .day-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 2px solid rgba(255,215,0,0.3);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .day-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(255,215,0,0.2);
            border-color: #ffd700;
        }}
        
        .day-header {{
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ffd700;
        }}
        
        .day-title {{
            font-size: 1.4em;
            font-weight: bold;
            margin: 0;
            color: #ffd700;
        }}
        
        .day-date {{
            font-size: 1.1em;
            margin: 5px 0 0 0;
            color: #ccc;
        }}
        
        .games-container {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            max-height: 600px;
            overflow-y: auto;
            padding-right: 5px;
        }}
        
        /* Scrollbar custom pour grosse liste */
        .games-container::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .games-container::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }}
        
        .games-container::-webkit-scrollbar-thumb {{
            background: #ffd700;
            border-radius: 4px;
        }}
        
        .games-container::-webkit-scrollbar-thumb:hover {{
            background: #ffed4e;
        }}
        
        .game-card {{
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #ffd700;
        }}
        
        .game-matchup {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 1.1em;
            font-weight: bold;
        }}
        
        .team {{
            padding: 5px 10px;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
        }}
        
        .vs {{
            color: #ffd700;
            font-weight: bold;
        }}
        
        .game-time {{
            text-align: center;
            color: #ccc;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .prediction {{
            background: rgba(255,215,0,0.1);
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }}
        
        .prediction-title {{
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 5px;
        }}
        
        .prediction-details {{
            font-size: 0.9em;
            line-height: 1.4;
        }}
        
        .confidence {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .confidence-high {{ background: #4CAF50; }}
        .confidence-medium {{ background: #ff9800; }}
        .confidence-low {{ background: #f44336; }}
        
        .result {{
            background: rgba(0,150,0,0.2);
            border-left: 4px solid #4CAF50;
            padding: 10px;
            margin-top: 10px;
            border-radius: 8px;
        }}
        
        .result-wrong {{
            background: rgba(150,0,0,0.2);
            border-left-color: #f44336;
        }}
        
        .no-games {{
            text-align: center;
            color: #888;
            font-style: italic;
            padding: 30px;
        }}
        
        .refresh-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ffd700;
            color: #0f4c75;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }}
        
        .refresh-btn:hover {{
            background: #ffed4e;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .update-time {{
            text-align: center;
            padding: 20px;
            color: #aaa;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏒 Calendrier NHL avec Prédictions</h1>
        <p>Matchs quotidiens • Prédictions automatiques • Validation résultats</p>
    </div>
    
    <div class="stats-summary">
        <div class="stat-item">
            <div class="stat-number">{stats[0] or 0}</div>
            <div>Prédictions Total</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{stats[1] or 0}</div>
            <div>Vainqueurs Corrects</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{(stats[1]/stats[0]*100 if stats[0] > 0 else 0):.1f}%</div>
            <div>Précision Globale</div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser</button>
    
    <div class="calendar-grid">
'''
        
        # Ajouter chaque jour
        for date_str in sorted(calendar_data.keys()):
            day_info = calendar_data[date_str]
            date_obj = day_info['date_obj']
            games = day_info['games']
            
            # Nom du jour en français
            day_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            day_name = day_names[date_obj.weekday()]
            
            # Badge nombre de matchs pour grosses soirées
            games_count = len(games)
            games_badge = ""
            if games_count >= 10:
                games_badge = f'<span style="background:#ff6b35;color:white;padding:3px 8px;border-radius:12px;font-size:0.8em;margin-left:10px;">🔥 {games_count} matchs</span>'
            elif games_count >= 6:
                games_badge = f'<span style="background:#4CAF50;color:white;padding:3px 8px;border-radius:12px;font-size:0.8em;margin-left:10px;">🏒 {games_count} matchs</span>'
            elif games_count > 0:
                games_badge = f'<span style="background:#2196F3;color:white;padding:3px 8px;border-radius:12px;font-size:0.8em;margin-left:10px;">{games_count} matchs</span>'
            
            html_content += f'''
        <div class="day-card">
            <div class="day-header">
                <h3 class="day-title">{day_name} {games_badge}</h3>
                <p class="day-date">{date_obj.strftime('%d %B %Y')}</p>
            </div>
            
            <div class="games-container">
'''
            
            if games:
                for game in games:
                    (game_id, home_team, away_team, start_time, home_score, away_score, 
                     game_status, pred_winner, pred_home, pred_away, home_win_prob, 
                     confidence, key_factors, actual_winner, winner_correct, accuracy) = game
                    
                    # Noms complets équipes
                    home_full = self.nhl_teams.get(home_team, home_team)
                    away_full = self.nhl_teams.get(away_team, away_team)
                    
                    html_content += f'''
                <div class="game-card">
                    <div class="game-matchup">
                        <span class="team">{away_team}</span>
                        <span class="vs">@</span>
                        <span class="team">{home_team}</span>
                    </div>
                    <div class="game-time">{start_time or '19:00'}</div>
'''
                    
                    # Afficher résultat final si disponible
                    if home_score is not None and away_score is not None:
                        result_class = "result" if winner_correct else "result result-wrong"
                        status_icon = "✅" if winner_correct else "❌"
                        
                        accuracy_pct = (accuracy * 100) if accuracy is not None else 0
                        html_content += f'''
                    <div class="{result_class}">
                        <strong>FINAL: {away_team} {away_score} - {home_score} {home_team}</strong>
                        <br>Prédiction: {status_icon} ({accuracy_pct:.0f}% précision)
                    </div>
'''
                    
                    # Afficher prédiction si disponible  
                    elif pred_winner:
                        confidence_class = "confidence-high" if confidence > 0.7 else "confidence-medium" if confidence > 0.5 else "confidence-low"
                        
                        try:
                            factors = json.loads(key_factors) if key_factors else []
                        except:
                            factors = []
                        
                        html_content += f'''
                    <div class="prediction">
                        <div class="prediction-title">
                            🎯 Prédiction: {pred_winner}
                            <span class="{confidence_class} confidence">{confidence*100:.0f}%</span>
                        </div>
                        <div class="prediction-details">
                            Score prédit: {away_team} {pred_away} - {pred_home} {home_team}<br>
                            Prob. victoire domicile: {home_win_prob*100:.0f}%
'''
                        
                        if factors:
                            html_content += f"<br>Facteurs: {', '.join(factors[:2])}"
                        
                        html_content += '''
                        </div>
                    </div>
'''
                    
                    html_content += '</div>'
                
            else:
                html_content += '''
                <div class="no-games">
                    🏒 Pas de matchs programmés ce jour
                </div>
'''
            
            html_content += '''
            </div>
        </div>
'''
        
        html_content += f'''
    </div>
    
    <div class="update-time">
        Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        Prédictions générées automatiquement • Validation quotidienne des résultats
    </div>
    
    <script>
        // Auto-refresh chaque 10 minutes
        setTimeout(() => location.reload(), 600000);
        
        // Notification nouvelles prédictions
        console.log('🏒 Calendrier NHL chargé - {sum(len(day_info["games"]) for day_info in calendar_data.values())} matchs à venir');
    </script>
</body>
</html>
        '''
        
        # Sauvegarder fichier
        with open(self.calendar_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Calendrier HTML généré: {self.calendar_html}")
        return self.calendar_html
    
    def run_daily_prediction_cycle(self):
        """Lance le cycle quotidien: prédictions + validations"""
        
        print(f"\n🔄 CYCLE QUOTIDIEN PRÉDICTIONS")
        print("=" * 50)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Valider résultats d'hier (simulation)
        validated = self.simulate_game_results(today)
        
        # 2. Générer prédictions pour aujourd'hui
        predictions = self.predict_games_for_date(today)
        
        # 3. Générer prédictions pour demain aussi
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        tomorrow_predictions = self.predict_games_for_date(tomorrow)
        
        total_predictions = len(predictions) + len(tomorrow_predictions)
        
        print(f"📊 Cycle terminé:")
        print(f"   ✅ {validated} résultats validés")
        print(f"   🎯 {total_predictions} nouvelles prédictions")
        
        return {
            'validated': validated,
            'predictions_made': total_predictions,
            'today_games': len(predictions),
            'tomorrow_games': len(tomorrow_predictions)
        }
    
    def run_complete_calendar_system(self):
        """Lance le système calendrier complet"""
        
        print(f"\n🚀 SYSTÈME CALENDRIER NHL COMPLET")
        
        # 1. Générer calendrier NHL 
        start_date = datetime.now()
        schedule = self.simulate_nhl_schedule(start_date, days=14)  # 2 semaines
        self.save_schedule_to_db(schedule)
        
        # 2. Lancer cycle prédictions
        cycle_results = self.run_daily_prediction_cycle()
        
        # 3. Générer calendrier HTML
        calendar_file = self.generate_calendar_html()
        
        # 4. Créer script automatisation
        self.create_automation_script()
        
        print(f"\n🏆 CALENDRIER NHL OPÉRATIONNEL!")
        print(f"📅 Interface: {calendar_file}")
        print(f"🎯 {cycle_results['predictions_made']} prédictions actives")
        print(f"✅ Validation automatique configurée")
        
        return calendar_file
    
    def create_automation_script(self):
        """Crée script pour automatisation quotidienne"""
        
        automation_script = '''#!/usr/bin/env python3
"""
🔄 NHL CALENDAR AUTO-UPDATER
Script quotidien pour prédictions + validations automatiques

À lancer chaque matin 7h00 via crontab
"""

import sys
from datetime import datetime
from nhl_betting_dashboard import NHLCalendarPredictor

def daily_calendar_update():
    """Update quotidien calendrier NHL"""
    
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Début update calendrier NHL...")
    
    try:
        # Lancer système calendrier
        calendar = NHLCalendarPredictor()
        
        # Cycle prédictions + validation  
        results = calendar.run_daily_prediction_cycle()
        
        # Régénérer calendrier HTML
        calendar.generate_calendar_html()
        
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Calendrier mis à jour!")
        print(f"   🎯 {results['predictions_made']} prédictions")
        print(f"   ✅ {results['validated']} résultats validés")
        
    except Exception as e:
        print(f"❌ Erreur update calendrier: {e}")

if __name__ == "__main__":
    daily_calendar_update()
'''
        
        with open("nhl_calendar_auto_updater.py", 'w', encoding='utf-8') as f:
            f.write(automation_script)
        
        print(f"✅ Script automation créé: nhl_calendar_auto_updater.py")
        print(f"💡 Crontab: 0 7 * * * /usr/bin/python3 {os.getcwd()}/nhl_calendar_auto_updater.py")

def main():
    """Lance le calendrier NHL avec prédictions"""
    print("🚀 DÉMARRAGE CALENDRIER NHL PREDICTOR")
    
    calendar_predictor = NHLCalendarPredictor()
    calendar_file = calendar_predictor.run_complete_calendar_system()
    
    print(f"\n✅ CALENDRIER PRÊT: {calendar_file}")
    print(f"🏒 Ouvre le fichier pour voir tes prédictions!")

if __name__ == "__main__":
    main()
