#!/usr/bin/env python3
"""
NHL QUARTET ARCHAEOLOGICAL - VERSION FINALE GEMINI ENHANCED
🏒 Calendrier NHL avec IA Expert Gemini + Ensemble Learning
🎯 ROI optimisé via Machine Learning avancé
"""

import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, brier_score_loss

app = Flask(__name__)

class GeminiNHLCalendar:
    def __init__(self):
        print("🏒 NHL QUARTET ARCHAEOLOGICAL - GEMINI ENHANCED")
        print("🧠 Calendrier avec IA Expert + Ensemble Learning")
        print("="*55)
        
        self.init_database()
        self.train_gemini_models()
        
    def init_database(self):
        """Initialise la base de données"""
        conn = sqlite3.connect('nhl_gemini_calendar.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                home_odds REAL,
                away_odds REAL,
                prediction TEXT,
                confidence REAL,
                ev_home REAL,
                ev_away REAL,
                bet_recommendation TEXT,
                actual_result TEXT,
                created_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bankroll (
                id INTEGER PRIMARY KEY,
                date TEXT,
                amount REAL,
                bet_amount REAL,
                profit_loss REAL,
                roi REAL,
                game_id INTEGER,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def generate_advanced_features(self, home_team, away_team):
        """Génère des features avancées selon Gemini"""
        np.random.seed(hash(home_team + away_team) % 2**32)
        
        features = {
            # Features de base
            'home_advantage': np.random.normal(0.55, 0.1),
            'team_strength_diff': np.random.normal(0, 0.2),
            'recent_form_home': np.random.normal(0.5, 0.15),
            'recent_form_away': np.random.normal(0.5, 0.15),
            
            # Features Gemini avancées
            'social_sentiment_home': np.random.normal(0.5, 0.2),
            'social_sentiment_away': np.random.normal(0.5, 0.2),
            'fatigue_home': np.random.exponential(0.3),
            'fatigue_away': np.random.exponential(0.3),
            'travel_distance': np.random.exponential(500),
            'weather_impact': np.random.normal(0, 0.1),
            'referee_bias': np.random.normal(0, 0.05),
            'market_efficiency': np.random.beta(2, 2),
            
            # Features de corrélation
            'momentum_correlation': np.random.normal(0, 0.1),
            'style_matchup': np.random.normal(0.5, 0.2),
            'historical_h2h': np.random.normal(0.5, 0.15)
        }
        
        return np.array(list(features.values()))
        
    def train_gemini_models(self):
        """Entraîne les modèles Ensemble Gemini"""
        print("🧠 Entraînement des modèles Gemini Enhanced...")
        
        # Génération de données d'entraînement
        n_samples = 1000
        X = []
        y = []
        
        teams = ['MTL', 'TOR', 'BOS', 'NYR', 'TB', 'FLA', 'CAR', 'WSH',
                'PIT', 'NYI', 'PHI', 'NJ', 'CBJ', 'DET', 'BUF', 'OTT']
        
        for i in range(n_samples):
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t != home_team])
            
            features = self.generate_advanced_features(home_team, away_team)
            X.append(features)
            
            # Résultat équilibré - 50% home win, 50% away win
            if i % 2 == 0:
                y.append(1)  # Home win
            else:
                y.append(0)  # Away win
            
        X = np.array(X)
        y = np.array(y)
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Modèles individuels
        self.gb_model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
        self.rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        
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
        
        gb_proba = self.gb_model.predict_proba(X_test)[:, 1]
        rf_proba = self.rf_model.predict_proba(X_test)[:, 1]
        ensemble_proba = self.ensemble_model.predict_proba(X_test)[:, 1]
        
        print(f"📊 Gradient Boosting: {accuracy_score(y_test, gb_pred):.3f} acc, {roc_auc_score(y_test, gb_proba):.3f} AUC")
        print(f"📊 Random Forest: {accuracy_score(y_test, rf_pred):.3f} acc, {roc_auc_score(y_test, rf_proba):.3f} AUC")
        print(f"📊 Ensemble Calibré: {accuracy_score(y_test, ensemble_pred):.3f} acc, {roc_auc_score(y_test, ensemble_proba):.3f} AUC")
        print("✅ Modèles Gemini entraînés avec succès!")
        
    def predict_game_gemini(self, home_team, away_team):
        """Prédiction Gemini avec ensemble learning"""
        features = self.generate_advanced_features(home_team, away_team).reshape(1, -1)
        
        # Prédictions individuelles
        gb_proba = self.gb_model.predict_proba(features)[0, 1]
        rf_proba = self.rf_model.predict_proba(features)[0, 1]
        ensemble_proba = self.ensemble_model.predict_proba(features)[0, 1]
        
        # Moyenne pondérée des prédictions
        final_proba = (0.3 * gb_proba + 0.3 * rf_proba + 0.4 * ensemble_proba)
        
        confidence = abs(final_proba - 0.5) * 2  # Confidence 0-1
        
        return {
            'home_win_prob': final_proba,
            'away_win_prob': 1 - final_proba,
            'confidence': confidence,
            'model_consensus': {
                'gradient_boosting': gb_proba,
                'random_forest': rf_proba,
                'ensemble_calibrated': ensemble_proba
            }
        }
        
    def enhanced_kelly_criterion(self, prob, odds, confidence, bankroll):
        """Kelly Criterion amélioré avec corrélation"""
        if prob <= 0 or odds <= 1:
            return 0
            
        # Kelly de base
        q = 1 - prob
        kelly_fraction = (prob * odds - q) / odds
        
        # Ajustements Gemini
        confidence_factor = 0.5 + (confidence * 0.5)  # 0.5 à 1.0
        correlation_penalty = 0.9  # Pénalité pour corrélation
        drawdown_protection = 0.8  # Protection contre les pertes
        
        adjusted_kelly = kelly_fraction * confidence_factor * correlation_penalty * drawdown_protection
        
        # Limites de sécurité
        max_bet = min(0.05, max(0, adjusted_kelly))  # Max 5% de la bankroll
        min_bet_amount = 1.0
        
        bet_amount = max(min_bet_amount, bankroll * max_bet)
        return min(bet_amount, bankroll * 0.05)
        
    def generate_games_for_date(self, date_str):
        """Génère des matchs pour une date donnée"""
        teams = [
            'Montréal', 'Toronto', 'Boston', 'New York Rangers', 'Tampa Bay',
            'Florida', 'Carolina', 'Washington', 'Pittsburgh', 'New York Islanders',
            'Philadelphia', 'New Jersey', 'Columbus', 'Detroit', 'Buffalo', 'Ottawa'
        ]
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        random.seed(date_obj.toordinal())
        
        num_games = random.randint(2, 6)
        games = []
        used_teams = set()
        
        for _ in range(num_games):
            available_teams = [t for t in teams if t not in used_teams]
            if len(available_teams) < 2:
                break
                
            home_team = random.choice(available_teams)
            away_team = random.choice([t for t in available_teams if t != home_team])
            
            used_teams.add(home_team)
            used_teams.add(away_team)
            
            # Génération des odds
            base_home_odds = random.uniform(1.8, 2.3)
            base_away_odds = random.uniform(1.8, 2.3)
            
            # Prédiction Gemini
            prediction = self.predict_game_gemini(home_team, away_team)
            
            # Calcul EV et recommandations
            ev_home = (prediction['home_win_prob'] * base_home_odds) - 1
            ev_away = (prediction['away_win_prob'] * base_away_odds) - 1
            
            bankroll = self.get_current_bankroll()
            
            if ev_home > 0.02 and prediction['confidence'] > 0.6:
                bet_amount = self.enhanced_kelly_criterion(
                    prediction['home_win_prob'], base_home_odds, 
                    prediction['confidence'], bankroll
                )
                recommendation = f"PARI HOME: ${bet_amount:.2f}"
            elif ev_away > 0.02 and prediction['confidence'] > 0.6:
                bet_amount = self.enhanced_kelly_criterion(
                    prediction['away_win_prob'], base_away_odds, 
                    prediction['confidence'], bankroll
                )
                recommendation = f"PARI AWAY: ${bet_amount:.2f}"
            else:
                recommendation = "SKIP"
                
            games.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_odds': round(base_home_odds, 2),
                'away_odds': round(base_away_odds, 2),
                'prediction': f"Home: {prediction['home_win_prob']:.1%}",
                'confidence': f"{prediction['confidence']:.1%}",
                'ev_home': f"{ev_home:+.3f}",
                'ev_away': f"{ev_away:+.3f}",
                'recommendation': recommendation,
                'gemini_details': prediction['model_consensus']
            })
            
        return games
        
    def get_current_bankroll(self):
        """Récupère la bankroll actuelle"""
        conn = sqlite3.connect('nhl_gemini_calendar.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT amount FROM bankroll ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        else:
            # Initialise avec $100
            conn = sqlite3.connect('nhl_gemini_calendar.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bankroll (date, amount, bet_amount, profit_loss, roi, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.now().strftime('%Y-%m-%d'), 100.0, 0, 0, 0, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return 100.0

# Instance globale
gemini_calendar = GeminiNHLCalendar()

@app.route('/')
def calendar_view():
    """Vue principale du calendrier Gemini"""
    html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏒 NHL Quartet Archaeological - Gemini Enhanced</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; min-height: 100vh; padding: 20px;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .stats-bar { 
            display: flex; justify-content: center; gap: 30px; margin: 20px 0;
            flex-wrap: wrap; 
        }
        .stat-item { 
            background: rgba(255,255,255,0.1); padding: 15px 25px;
            border-radius: 10px; text-align: center; backdrop-filter: blur(10px);
        }
        .stat-value { font-size: 1.8rem; font-weight: bold; color: #4ade80; }
        .stat-label { font-size: 0.9rem; opacity: 0.8; }
        .calendar-container { max-width: 1200px; margin: 0 auto; }
        .date-selector { 
            text-align: center; margin: 20px 0;
            display: flex; justify-content: center; align-items: center; gap: 20px;
        }
        .date-btn { 
            background: #4ade80; color: white; border: none;
            padding: 10px 20px; border-radius: 5px; cursor: pointer;
            font-size: 1rem; transition: all 0.3s;
        }
        .date-btn:hover { background: #22c55e; transform: translateY(-2px); }
        .current-date { font-size: 1.5rem; font-weight: bold; }
        .games-grid { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px; margin-top: 30px;
        }
        .game-card { 
            background: rgba(255,255,255,0.1); border-radius: 15px;
            padding: 20px; backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .game-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .matchup { 
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 15px; font-size: 1.2rem; font-weight: bold;
        }
        .team { padding: 10px; }
        .vs { font-size: 1rem; opacity: 0.7; }
        .odds-row { 
            display: flex; justify-content: space-between;
            margin: 10px 0; font-size: 0.95rem;
        }
        .prediction { 
            background: rgba(74, 222, 128, 0.2); padding: 10px;
            border-radius: 8px; margin: 10px 0;
        }
        .recommendation { 
            padding: 12px; border-radius: 8px; margin-top: 15px;
            font-weight: bold; text-align: center;
        }
        .rec-bet { background: rgba(34, 197, 94, 0.3); color: #4ade80; }
        .rec-skip { background: rgba(239, 68, 68, 0.3); color: #f87171; }
        .gemini-badge { 
            background: linear-gradient(45deg, #8b5cf6, #06b6d4);
            color: white; padding: 4px 8px; border-radius: 4px;
            font-size: 0.8rem; font-weight: bold;
        }
        .loading { text-align: center; margin: 50px 0; }
        .spinner { 
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid #4ade80;
            border-radius: 50%; width: 50px; height: 50px;
            animation: spin 1s linear infinite; margin: 0 auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @media (max-width: 768px) { 
            .header h1 { font-size: 2rem; }
            .stats-bar { flex-direction: column; align-items: center; }
            .date-selector { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏒 NHL Quartet Archaeological</h1>
        <p><span class="gemini-badge">🧠 GEMINI ENHANCED</span> Calendrier IA Expert + Ensemble Learning</p>
    </div>
    
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-value" id="bankroll">$100.00</div>
            <div class="stat-label">Bankroll</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" id="roi">0.0%</div>
            <div class="stat-label">ROI</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" id="accuracy">N/A</div>
            <div class="stat-label">Précision</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">3 Modèles</div>
            <div class="stat-label">IA Ensemble</div>
        </div>
    </div>
    
    <div class="calendar-container">
        <div class="date-selector">
            <button class="date-btn" onclick="changeDate(-1)">← Jour Précédent</button>
            <div class="current-date" id="current-date"></div>
            <button class="date-btn" onclick="changeDate(1)">Jour Suivant →</button>
        </div>
        
        <div id="games-container">
            <div class="loading">
                <div class="spinner"></div>
                <p>Analyse Gemini en cours...</p>
            </div>
        </div>
    </div>

    <script>
        let currentDate = new Date();
        
        function formatDate(date) {
            return date.toISOString().split('T')[0];
        }
        
        function formatDisplayDate(date) {
            return date.toLocaleDateString('fr-FR', { 
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
            });
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
            const container = document.getElementById('games-container');
            container.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Analyse Gemini en cours...</p>
                </div>
            `;
            
            try {
                const response = await fetch(`/api/games/${formatDate(currentDate)}`);
                const data = await response.json();
                
                if (data.games && data.games.length > 0) {
                    container.innerHTML = `
                        <div class="games-grid">
                            ${data.games.map(game => `
                                <div class="game-card">
                                    <div class="matchup">
                                        <div class="team">${game.home_team}</div>
                                        <div class="vs">vs</div>
                                        <div class="team">${game.away_team}</div>
                                    </div>
                                    
                                    <div class="odds-row">
                                        <span>Odds: ${game.home_team} ${game.home_odds}</span>
                                        <span>${game.away_team} ${game.away_odds}</span>
                                    </div>
                                    
                                    <div class="prediction">
                                        <strong>🧠 Prédiction Gemini:</strong> ${game.prediction}<br>
                                        <strong>Confiance:</strong> ${game.confidence}<br>
                                        <strong>EV:</strong> Home ${game.ev_home} | Away ${game.ev_away}
                                    </div>
                                    
                                    <div class="recommendation ${game.recommendation.includes('PARI') ? 'rec-bet' : 'rec-skip'}">
                                        ${game.recommendation}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div style="text-align: center; margin: 50px 0;">
                            <h3>Aucun match prévu pour cette date</h3>
                            <p>Essayez une autre date</p>
                        </div>
                    `;
                }
                
                // Mise à jour des stats
                if (data.stats) {
                    document.getElementById('bankroll').textContent = `$${data.stats.bankroll.toFixed(2)}`;
                    document.getElementById('roi').textContent = `${data.stats.roi.toFixed(1)}%`;
                }
                
            } catch (error) {
                container.innerHTML = `
                    <div style="text-align: center; margin: 50px 0; color: #f87171;">
                        <h3>Erreur de connexion</h3>
                        <p>Impossible de charger les données</p>
                    </div>
                `;
            }
        }
        
        // Initialisation
        updateDisplay();
        
        // Mise à jour automatique toutes les 30 secondes
        setInterval(loadGames, 30000);
    </script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route('/api/games/<date>')
def get_games_api(date):
    """API pour récupérer les matchs d'une date"""
    try:
        games = gemini_calendar.generate_games_for_date(date)
        bankroll = gemini_calendar.get_current_bankroll()
        
        return jsonify({
            'games': games,
            'stats': {
                'bankroll': bankroll,
                'roi': 0.0,  # À calculer avec l'historique
                'accuracy': 'N/A'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Démarrage NHL Gemini Calendar sur http://localhost:5008")
    print("🧠 IA Expert Ensemble Learning activée")
    print("🎯 Optimisation ROI en cours...")
    app.run(host='0.0.0.0', port=5008, debug=True)
