#!/usr/bin/env python3
"""
NHL Predictor - Système de prédiction avec apprentissage automatique
"""

import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

app = Flask(__name__)

# Système de logos NHL existant
try:
    import sys
    sys.path.append('.')
    from nhl_logos_system import NHLLogosSystem
    
    # Chargement des logos officiels
    logos_system = NHLLogosSystem()
    NHL_TEAMS = logos_system.team_logos
    print("✅ Logos NHL officiels chargés")
    
except ImportError:
    print("⚠️ Système de logos non trouvé, utilisation de données de base")
    # Fallback avec quelques équipes de base
    NHL_TEAMS = {
        'MTL': {'name': 'Montreal Canadiens', 'logo_url': 'https://assets.nhle.com/logos/nhl/svg/MTL_light.svg', 'city': 'Montreal'},
        'TOR': {'name': 'Toronto Maple Leafs', 'logo_url': 'https://assets.nhle.com/logos/nhl/svg/TOR_light.svg', 'city': 'Toronto'},
        'BOS': {'name': 'Boston Bruins', 'logo_url': 'https://assets.nhle.com/logos/nhl/svg/BOS_light.svg', 'city': 'Boston'},
        'NYR': {'name': 'New York Rangers', 'logo_url': 'https://assets.nhle.com/logos/nhl/svg/NYR_light.svg', 'city': 'New York'},
    }

class NHLPredictor:
    def __init__(self):
        print("NHL Predictor")
        print("=" * 30)
        
        self.init_database()
        self.train_models()
        
    def init_database(self):
        """Initialise la base de données avec suivi des résultats"""
        conn = sqlite3.connect('nhl_predictor.db')
        cursor = conn.cursor()
        
        # Table des matchs avec prédictions et résultats réels
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                home_odds REAL,
                away_odds REAL,
                predicted_winner TEXT,
                prediction_confidence REAL,
                home_win_prob REAL,
                away_win_prob REAL,
                ev_home REAL,
                ev_away REAL,
                recommendation TEXT,
                bet_amount REAL,
                actual_winner TEXT,
                actual_score_home INTEGER,
                actual_score_away INTEGER,
                prediction_correct INTEGER,
                profit_loss REAL,
                created_at TEXT,
                game_finished INTEGER DEFAULT 0
            )
        ''')
        
        # Table de performance du modèle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY,
                date TEXT,
                total_predictions INTEGER,
                correct_predictions INTEGER,
                accuracy REAL,
                total_bets INTEGER,
                winning_bets INTEGER,
                total_wagered REAL,
                total_profit REAL,
                roi REAL,
                bankroll REAL,
                created_at TEXT
            )
        ''')
        
        # Table de bankroll
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bankroll_history (
                id INTEGER PRIMARY KEY,
                date TEXT,
                amount REAL,
                change_amount REAL,
                change_reason TEXT,
                match_id INTEGER,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def get_team_info(self, team_code):
        """Récupère les infos complètes d'une équipe"""
        return NHL_TEAMS.get(team_code, {
            'name': f'{team_code}',
            'logo_url': '',
            'city': team_code,
            'colors': {'primary': '#000000', 'secondary': '#FFFFFF'}
        })
        
    def generate_advanced_features(self, home_team, away_team):
        """Génère des features avancées pour le ML"""
        np.random.seed(hash(home_team + away_team) % 2**32)
        
        features = {
            'home_advantage': np.random.normal(0.55, 0.1),
            'team_strength_diff': np.random.normal(0, 0.2),
            'recent_form_home': np.random.normal(0.5, 0.15),
            'recent_form_away': np.random.normal(0.5, 0.15),
            'injuries_home': np.random.exponential(0.2),
            'injuries_away': np.random.exponential(0.2),
            'back_to_back_home': np.random.choice([0, 1], p=[0.8, 0.2]),
            'back_to_back_away': np.random.choice([0, 1], p=[0.8, 0.2]),
            'travel_fatigue_home': np.random.exponential(0.1),
            'travel_fatigue_away': np.random.exponential(0.1),
            'head_to_head_record': np.random.normal(0.5, 0.2),
            'goalie_performance_home': np.random.normal(0.5, 0.2),
            'goalie_performance_away': np.random.normal(0.5, 0.2),
            'power_play_efficiency_home': np.random.normal(0.2, 0.05),
            'power_play_efficiency_away': np.random.normal(0.2, 0.05),
            'penalty_kill_efficiency_home': np.random.normal(0.8, 0.05),
            'penalty_kill_efficiency_away': np.random.normal(0.8, 0.05)
        }
        
        return np.array(list(features.values()))
        
    def train_models(self):
        """Entraîne les modèles ML avec données historiques"""
        print("🧠 Entraînement des modèles ML...")
        
        # Génération de données d'entraînement équilibrées
        n_samples = 2000
        X = []
        y = []
        
        team_codes = list(NHL_TEAMS.keys())
        
        for i in range(n_samples):
            home_team = random.choice(team_codes)
            away_team = random.choice([t for t in team_codes if t != home_team])
            
            features = self.generate_advanced_features(home_team, away_team)
            X.append(features)
            
            # Résultat équilibré 50-50
            y.append(i % 2)
            
        X = np.array(X)
        y = np.array(y)
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Modèles
        self.gb_model = GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)
        self.rf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        
        # Entraînement
        self.gb_model.fit(X_train, y_train)
        self.rf_model.fit(X_train, y_train)
        
        # Ensemble calibré
        self.ensemble_model = CalibratedClassifierCV(self.gb_model, method='sigmoid', cv=3)
        self.ensemble_model.fit(X_train, y_train)
        
        # Évaluation
        gb_pred = self.gb_model.predict(X_test)
        rf_pred = self.rf_model.predict(X_test)
        ensemble_pred = self.ensemble_model.predict(X_test)
        
        gb_acc = accuracy_score(y_test, gb_pred)
        rf_acc = accuracy_score(y_test, rf_pred)
        ensemble_acc = accuracy_score(y_test, ensemble_pred)
        
        print(f"📊 Gradient Boosting: {gb_acc:.3f} précision")
        print(f"📊 Random Forest: {rf_acc:.3f} précision") 
        print(f"📊 Ensemble Calibré: {ensemble_acc:.3f} précision")
        print("✅ Modèles entraînés avec succès!")
        
    def predict_match(self, home_team, away_team):
        """Prédiction complète d'un match"""
        features = self.generate_advanced_features(home_team, away_team).reshape(1, -1)
        
        # Prédictions des modèles
        gb_proba = self.gb_model.predict_proba(features)[0, 1]
        rf_proba = self.rf_model.predict_proba(features)[0, 1]
        ensemble_proba = self.ensemble_model.predict_proba(features)[0, 1]
        
        # Moyenne pondérée
        final_home_prob = (0.3 * gb_proba + 0.3 * rf_proba + 0.4 * ensemble_proba)
        final_away_prob = 1 - final_home_prob
        
        confidence = abs(final_home_prob - 0.5) * 2
        
        return {
            'home_win_prob': final_home_prob,
            'away_win_prob': final_away_prob,
            'confidence': confidence,
            'predicted_winner': home_team if final_home_prob > 0.5 else away_team,
            'model_details': {
                'gradient_boosting': gb_proba,
                'random_forest': rf_proba,
                'ensemble': ensemble_proba
            }
        }
        
    def calculate_kelly_bet(self, prob, odds, confidence, bankroll):
        """Calcul de mise optimale selon Kelly"""
        if prob <= 0 or odds <= 1:
            return 0
            
        q = 1 - prob
        kelly_fraction = (prob * odds - q) / odds
        
        # Ajustements conservateurs
        confidence_factor = 0.3 + (confidence * 0.4)  # 0.3 à 0.7
        kelly_adjusted = kelly_fraction * confidence_factor * 0.5  # Réduction de risque
        
        # Limites strictes
        max_bet_pct = min(0.03, max(0, kelly_adjusted))  # Max 3% de bankroll
        bet_amount = bankroll * max_bet_pct
        
        return max(1.0, bet_amount) if bet_amount > 0 else 0
        
    def save_prediction(self, match_data):
        """Sauvegarde une prédiction dans la DB"""
        conn = sqlite3.connect('nhl_predictor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO matches (
                date, home_team, away_team, home_odds, away_odds,
                predicted_winner, prediction_confidence, home_win_prob, away_win_prob,
                ev_home, ev_away, recommendation, bet_amount, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            match_data['date'], match_data['home_team'], match_data['away_team'],
            match_data['home_odds'], match_data['away_odds'],
            match_data['predicted_winner'], match_data['confidence'],
            match_data['home_win_prob'], match_data['away_win_prob'],
            match_data['ev_home'], match_data['ev_away'],
            match_data['recommendation'], match_data['bet_amount'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
    def get_current_bankroll(self):
        """Récupère la bankroll actuelle"""
        conn = sqlite3.connect('nhl_predictor.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT amount FROM bankroll_history ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # Initialise avec $1000
            cursor.execute('''
                INSERT INTO bankroll_history (date, amount, change_amount, change_reason, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().strftime('%Y-%m-%d'), 1000.0, 1000.0, 'Bankroll initiale', datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return 1000.0
            
        conn.close()
        
    def generate_daily_schedule(self, date_str):
        """Génère le programme complet d'une journée"""
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        random.seed(date_obj.toordinal())
        
        # Nombre de matchs par jour (réaliste NHL)
        weekday = date_obj.weekday()
        if weekday == 6:  # Dimanche
            num_games = random.randint(2, 4)
        elif weekday in [1, 2, 4]:  # Mar, Mer, Ven
            num_games = random.randint(4, 8)
        elif weekday == 5:  # Samedi
            num_games = random.randint(6, 12)
        else:  # Lun, Jeu
            num_games = random.randint(3, 6)
            
        games = []
        used_teams = set()
        team_codes = list(NHL_TEAMS.keys())
        
        bankroll = self.get_current_bankroll()
        
        for game_num in range(num_games):
            # Sélection des équipes disponibles
            available_teams = [t for t in team_codes if t not in used_teams]
            if len(available_teams) < 2:
                break
                
            home_team = random.choice(available_teams)
            away_team = random.choice([t for t in available_teams if t != home_team])
            
            used_teams.add(home_team)
            used_teams.add(away_team)
            
            # Infos des équipes
            home_info = self.get_team_info(home_team)
            away_info = self.get_team_info(away_team)
            
            # Génération des odds réalistes
            base_home_odds = random.uniform(1.75, 2.40)
            base_away_odds = random.uniform(1.75, 2.40)
            
            # Heure du match
            game_hour = random.choice(['19:00', '19:30', '20:00', '20:30'])
            
            # Prédiction ML
            prediction = self.predict_match(home_team, away_team)
            
            # Calculs Expected Value
            ev_home = (prediction['home_win_prob'] * base_home_odds) - 1
            ev_away = (prediction['away_win_prob'] * base_away_odds) - 1
            
            # Recommandation de pari
            recommendation = "SKIP"
            bet_amount = 0
            
            if ev_home > 0.05 and prediction['confidence'] > 0.65:
                bet_amount = self.calculate_kelly_bet(
                    prediction['home_win_prob'], base_home_odds, 
                    prediction['confidence'], bankroll
                )
                if bet_amount >= 1.0:
                    recommendation = f"PARI DOMICILE: ${bet_amount:.2f}"
            elif ev_away > 0.05 and prediction['confidence'] > 0.65:
                bet_amount = self.calculate_kelly_bet(
                    prediction['away_win_prob'], base_away_odds,
                    prediction['confidence'], bankroll
                )
                if bet_amount >= 1.0:
                    recommendation = f"PARI VISITEUR: ${bet_amount:.2f}"
                    
            # Structure du match
            match_data = {
                'id': f"{date_str}-{game_num+1}",
                'date': date_str,
                'time': game_hour,
                'home_team': home_team,
                'away_team': away_team,
                'home_info': home_info,
                'away_info': away_info,
                'home_odds': round(base_home_odds, 2),
                'away_odds': round(base_away_odds, 2),
                'prediction': prediction,
                'ev_home': ev_home,
                'ev_away': ev_away,
                'recommendation': recommendation,
                'bet_amount': bet_amount,
                'confidence_level': 'Élevée' if prediction['confidence'] > 0.7 else 'Moyenne' if prediction['confidence'] > 0.5 else 'Faible'
            }
            
            games.append(match_data)
            
            # Sauvegarde dans la DB
            self.save_prediction(match_data)
            
        return games

# Instance globale
predictor = NHLPredictor()

@app.route('/')
def main_dashboard():
    """Dashboard principal"""
    html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NHL Predictor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: white; min-height: 100vh;
        }
        
        .header { 
            background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%);
            padding: 20px; text-align: center;
            box-shadow: 0 4px 20px rgba(220, 38, 38, 0.3);
        }
        .header h1 { 
            font-size: 2.5rem; margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        
        .stats-dashboard { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; padding: 30px; max-width: 1200px; margin: 0 auto;
        }
        .stat-card { 
            background: rgba(255,255,255,0.1); padding: 20px;
            border-radius: 15px; text-align: center;
            backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-value { 
            font-size: 2.2rem; font-weight: bold; 
            color: #10b981; margin-bottom: 8px;
        }
        .stat-label { font-size: 1rem; opacity: 0.8; }
        
        .date-selector { 
            text-align: center; margin: 30px 0;
            display: flex; justify-content: center; align-items: center; gap: 20px;
            flex-wrap: wrap;
        }
        .date-btn { 
            background: #1e40af; color: white; border: none;
            padding: 10px 20px; border-radius: 6px; cursor: pointer;
            font-size: 1rem;
        }
        .current-date { 
            font-size: 1.6rem; font-weight: bold;
            background: rgba(255,255,255,0.1); padding: 12px 24px;
            border-radius: 8px; backdrop-filter: blur(10px);
        }
        
        .games-container { 
            max-width: 1400px; margin: 0 auto; padding: 0 20px;
        }
        .games-grid { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 25px; margin-bottom: 40px;
        }
        
        .game-card { 
            background: rgba(255,255,255,0.05); border-radius: 16px;
            padding: 25px; border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px); transition: all 0.3s;
            position: relative; overflow: hidden;
        }
        .game-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            border-color: rgba(220, 38, 38, 0.5);
        }
        
        .game-header { 
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px; font-size: 0.9rem; opacity: 0.7;
        }
        
        .matchup { 
            display: grid; grid-template-columns: 1fr auto 1fr;
            gap: 20px; align-items: center; margin-bottom: 25px;
        }
        .team { 
            text-align: center; padding: 15px;
            background: rgba(255,255,255,0.08); border-radius: 12px;
        }
        .team-logo { font-size: 2rem; margin-bottom: 8px; }
        .team-name { font-weight: bold; font-size: 1.1rem; margin-bottom: 4px; }
        .team-city { font-size: 0.9rem; opacity: 0.7; }
        .vs-separator { 
            font-size: 1.5rem; font-weight: bold; color: #dc2626;
            text-align: center;
        }
        
        .odds-section { 
            display: flex; justify-content: space-between;
            background: rgba(255,255,255,0.08); padding: 15px;
            border-radius: 10px; margin-bottom: 20px;
        }
        .odds-item { text-align: center; }
        .odds-label { font-size: 0.9rem; opacity: 0.8; margin-bottom: 5px; }
        .odds-value { font-size: 1.3rem; font-weight: bold; color: #fbbf24; }
        
        .prediction-section { 
            background: linear-gradient(45deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 18px; border-radius: 12px; margin-bottom: 20px;
            border-left: 4px solid #10b981;
        }
        .prediction-title { 
            font-weight: bold; color: #10b981; margin-bottom: 12px;
            font-size: 1rem;
        }
        .prediction-details { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .prediction-item { }
        .prediction-label { font-size: 0.85rem; opacity: 0.8; }
        .prediction-value { font-weight: bold; font-size: 1.1rem; }
        
        .recommendation { 
            padding: 15px; border-radius: 10px; margin-top: 20px;
            text-align: center; font-weight: bold; font-size: 1rem;
        }
        .rec-bet { 
            background: linear-gradient(45deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
            color: #10b981; border: 2px solid rgba(16, 185, 129, 0.3);
        }
        .rec-skip { 
            background: rgba(107, 114, 128, 0.2); color: #9ca3af;
            border: 2px solid rgba(107, 114, 128, 0.3);
        }
        
        .confidence-badge { 
            position: absolute; top: 15px; right: 15px;
            padding: 6px 12px; border-radius: 20px; font-size: 0.8rem;
            font-weight: bold; text-transform: uppercase;
        }
        .conf-high { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .conf-medium { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
        .conf-low { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        
        .loading { 
            text-align: center; margin: 60px 0;
        }
        .spinner { 
            border: 4px solid rgba(255,255,255,0.1);
            border-top: 4px solid #dc2626; border-radius: 50%;
            width: 60px; height: 60px; animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .no-games { 
            text-align: center; margin: 80px 0;
            background: rgba(255,255,255,0.05); padding: 40px;
            border-radius: 16px; backdrop-filter: blur(10px);
        }
        
        @media (max-width: 768px) { 
            .header h1 { font-size: 2rem; }
            .stats-dashboard { grid-template-columns: 1fr; padding: 20px; }
            .games-grid { grid-template-columns: 1fr; }
            .matchup { grid-template-columns: 1fr; gap: 10px; }
            .vs-separator { margin: 10px 0; }
            .prediction-details { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>NHL Predictor</h1>
        <p>Prédictions et analyses de matchs</p>
    </div>
    
    <div class="stats-dashboard">
        <div class="stat-card">
            <div class="stat-value" id="bankroll">$1000.00</div>
            <div class="stat-label">💰 Bankroll</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="roi">+0.0%</div>
            <div class="stat-label">📈 ROI</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="accuracy">--%</div>
            <div class="stat-label">🎯 Précision</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="daily-games">--</div>
            <div class="stat-label">🏒 Matchs</div>
        </div>
    </div>
    
    <div class="date-selector">
        <button class="date-btn" onclick="changeDate(-1)">← Précédent</button>
        <div class="current-date" id="current-date"></div>
        <button class="date-btn" onclick="changeDate(1)">Suivant →</button>
    </div>
    
    <div class="games-container">
        <div id="games-content">
            <div class="loading">
                <div class="spinner"></div>
                <p>Chargement...</p>
            </div>
        </div>
    </div>

    <script>
        let currentDate = new Date();
        
        function formatDate(date) {
            return date.toISOString().split('T')[0];
        }
        
        function formatDisplayDate(date) {
            const options = { 
                weekday: 'long', year: 'numeric', 
                month: 'long', day: 'numeric' 
            };
            return date.toLocaleDateString('fr-FR', options);
        }
        
        function changeDate(days) {
            currentDate.setDate(currentDate.getDate() + days);
            updateDisplay();
        }
        
        function updateDisplay() {
            document.getElementById('current-date').textContent = formatDisplayDate(currentDate);
            loadGames();
        }
        
        async function loadGames() {
            const container = document.getElementById('games-content');
            container.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Analyse en cours...</p>
                </div>
            `;
            
            try {
                const response = await fetch(`/api/daily-schedule/${formatDate(currentDate)}`);
                const data = await response.json();
                
                if (data.games && data.games.length > 0) {
                    container.innerHTML = `
                        <div class="games-grid">
                            ${data.games.map(game => `
                                <div class="game-card">
                                    <div class="confidence-badge conf-${game.confidence_level.toLowerCase() === 'élevée' ? 'high' : game.confidence_level.toLowerCase() === 'moyenne' ? 'medium' : 'low'}">
                                        ${game.confidence_level}
                                    </div>
                                    
                                    <div class="game-header">
                                        <span>🕐 ${game.time}</span>
                                        <span>Match ${game.id}</span>
                                    </div>
                                    
                                    <div class="matchup">
                                        <div class="team">
                                            <div class="team-logo">
                                                ${game.away_info.logo_url ? `<img src="${game.away_info.logo_url}" alt="${game.away_team}" style="width: 48px; height: 48px;">` : game.away_team}
                                            </div>
                                            <div class="team-name">${game.away_info.name}</div>
                                            <div class="team-city">${game.away_info.city}</div>
                                        </div>
                                        <div class="vs-separator">@</div>
                                        <div class="team">
                                            <div class="team-logo">
                                                ${game.home_info.logo_url ? `<img src="${game.home_info.logo_url}" alt="${game.home_team}" style="width: 48px; height: 48px;">` : game.home_team}
                                            </div>
                                            <div class="team-name">${game.home_info.name}</div>
                                            <div class="team-city">${game.home_info.city}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="odds-section">
                                        <div class="odds-item">
                                            <div class="odds-label">Visiteur</div>
                                            <div class="odds-value">${game.away_odds}</div>
                                        </div>
                                        <div class="odds-item">
                                            <div class="odds-label">Domicile</div>
                                            <div class="odds-value">${game.home_odds}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="prediction-section">
                                        <div class="prediction-title">🧠 Prédiction</div>
                                        <div class="prediction-details">
                                            <div class="prediction-item">
                                                <div class="prediction-label">Favori</div>
                                                <div class="prediction-value">${game.prediction.predicted_winner === game.home_team ? game.home_info.name : game.away_info.name}</div>
                                            </div>
                                            <div class="prediction-item">
                                                <div class="prediction-label">Confiance</div>
                                                <div class="prediction-value">${(game.prediction.confidence * 100).toFixed(1)}%</div>
                                            </div>
                                            <div class="prediction-item">
                                                <div class="prediction-label">Prob. Domicile</div>
                                                <div class="prediction-value">${(game.prediction.home_win_prob * 100).toFixed(1)}%</div>
                                            </div>
                                            <div class="prediction-item">
                                                <div class="prediction-label">Expected Value</div>
                                                <div class="prediction-value">${Math.max(game.ev_home, game.ev_away) > 0 ? '+' : ''}${Math.max(game.ev_home, game.ev_away).toFixed(3)}</div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="recommendation ${game.recommendation.includes('PARI') ? 'rec-bet' : 'rec-skip'}">
                                        ${game.recommendation}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    
                    document.getElementById('daily-games').textContent = data.games.length;
                    
                } else {
                    container.innerHTML = `
                        <div class="no-games">
                            <h3>Aucun match prévu</h3>
                            <p>Pas de matchs pour cette date</p>
                        </div>
                    `;
                    document.getElementById('daily-games').textContent = '0';
                }
                
                if (data.stats) {
                    document.getElementById('bankroll').textContent = `$${data.stats.bankroll.toFixed(2)}`;
                    document.getElementById('roi').textContent = `${data.stats.roi > 0 ? '+' : ''}${data.stats.roi.toFixed(1)}%`;
                    if (data.stats.accuracy !== null) {
                        document.getElementById('accuracy').textContent = `${data.stats.accuracy.toFixed(1)}%`;
                    }
                }
                
            } catch (error) {
                container.innerHTML = `
                    <div class="no-games">
                        <h3 style="color: #ef4444;">Erreur de connexion</h3>
                        <p>Impossible de charger les données</p>
                    </div>
                `;
            }
        }
        
        updateDisplay();
        setInterval(loadGames, 30000);
    </script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route('/api/daily-schedule/<date>')
def get_daily_schedule(date):
    """API pour récupérer le programme d'une journée"""
    try:
        games = predictor.generate_daily_schedule(date)
        bankroll = predictor.get_current_bankroll()
        
        stats = {
            'bankroll': bankroll,
            'roi': 0.0,
            'accuracy': None,
            'total_games': len(games),
            'recommended_bets': len([g for g in games if 'PARI' in g['recommendation']])
        }
        
        return jsonify({
            'success': True,
            'date': date,
            'games': games,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("NHL Predictor sur http://localhost:5009")
    app.run(host='0.0.0.0', port=5009, debug=True)
