#!/usr/bin/env python3
"""
🏒🚀 NHL FLASK APP ENHANCED - Version intégrée avec votre app.py
Combines votre code avec les améliorations Grok + Gemini + ChatGPT
"""

from flask import Flask, jsonify, render_template_string, request, send_from_directory
import sqlite3
import requests
import json
import os
import random
import math
from datetime import datetime, timedelta

app = Flask(__name__)

class EnhancedQuartetNHLEngine:
    def __init__(self, db_file="nhl_enhanced.db"):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.api_key = "fake_key"  # Remplacer par The Odds API key
        self.bankroll = 1768.84
        self.create_enhanced_tables()
        
        # Grok X hype data (from your analysis)
        self.grok_x_hype = {
            'MTL': {
                'demidov_hype': 0.85,  # "rare talent", "tantalizing PP"
                'hutson_hype': 0.80,   # "first on ice", "waiting for Demidov" 
                'rookie_showdown': 0.90, # "blow up Prospect Showdown?"
                'pp_duo': 0.88         # "practising together"
            },
            'TOR': {'playoff_pressure': 0.6}, 'WPG': {'young_core': 0.5},
            'PIT': {'aging_core': -0.2}, 'PHI': {'rebuild': 0.3}
        }

    def create_enhanced_tables(self):
        """Enhanced database schema"""
        self.db.execute('''CREATE TABLE IF NOT EXISTS enhanced_predictions
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           game_id TEXT UNIQUE,
                           date TEXT,
                           home_team TEXT,
                           away_team TEXT,
                           quartet_prob REAL,
                           grok_sentiment REAL,
                           gemini_ensemble REAL,
                           final_prob REAL,
                           odds REAL,
                           ev REAL,
                           kelly_bet REAL,
                           black_swan_risk REAL,
                           recommendation TEXT,
                           result INTEGER,
                           pnl REAL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.db.commit()

    def fetch_nhl_data(self, date):
        """Fetch NHL games with enhanced error handling"""
        url = f"https://api-web.nhle.com/v1/schedule/{date.replace('-', '')}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            games = []
            if 'gameWeek' in data and data['gameWeek']:
                for day in data['gameWeek']:
                    if 'games' in day:
                        games.extend(day['games'])
            return games
        except:
            # Fallback simulation for demo
            return [
                {
                    'id': f'sim_{date}_mtl_pit',
                    'homeTeam': {'abbrev': 'MTL', 'placeName': {'default': 'Montreal'}},
                    'awayTeam': {'abbrev': 'PIT', 'placeName': {'default': 'Pittsburgh'}},
                    'gameDate': date,
                    'gameState': 'FUT'
                },
                {
                    'id': f'sim_{date}_mtl_bos', 
                    'homeTeam': {'abbrev': 'MTL', 'placeName': {'default': 'Montreal'}},
                    'awayTeam': {'abbrev': 'BOS', 'placeName': {'default': 'Boston'}},
                    'gameDate': date,
                    'gameState': 'FUT'
                }
            ]

    def fetch_odds(self, game_id, team='MTL'):
        """Simulé The Odds API"""
        base_odds = {"MTL": 1.91, "BOS": 1.85, "TOR": 1.88, "PIT": 1.95, "WPG": 1.93}
        return {"home_team": team, "odds": base_odds.get(team, 1.90)}

    def grok_sentiment_boost(self, team, date, opponent=None):
        """🔥 Grok sentiment analysis enhancement"""
        base_hype = self.grok_x_hype.get(team, {})
        if not base_hype:
            return 0.0
        
        # Calculate sentiment score
        sentiment_score = sum(base_hype.values()) / len(base_hype)
        
        # Date-specific bonuses (Prospect Showdown, etc.)
        date_bonus = 1.0
        if '2024-09-13' in date or '2024-09-14' in date:
            date_bonus = 1.2  # Prospect Showdown hype
        
        # Rivalry bonus
        rivalry_bonus = 1.15 if opponent in ['BOS', 'TOR'] and team == 'MTL' else 1.0
        
        # Final boost (cap at +10%)
        boost = min(sentiment_score * date_bonus * rivalry_bonus * 0.08, 0.10)
        return boost

    def gemini_ensemble_prediction(self, base_prob, team_features):
        """🔮 Gemini Ensemble ML simulation"""
        # Simulate XGBoost features
        xg_diff = team_features.get('xG_diff', 0.0)
        momentum = team_features.get('momentum', 0.5)
        travel_fatigue = team_features.get('travel_fatigue', 0.0)
        
        # Ensemble: 70% ML + 30% rules (Gemini suggestion)
        ml_prob = base_prob + (xg_diff * 0.12) + (momentum - 0.5) * 0.08 - travel_fatigue
        ml_prob = max(0.1, min(0.9, ml_prob))  # Constrain
        
        ensemble_prob = (ml_prob * 0.7) + (base_prob * 0.3)
        return ensemble_prob

    def gemini_risk_assessment(self, game_context):
        """🛡️ Gemini Black Swan risk assessment"""
        risk_score = 0.0
        
        # Check for risk factors
        injuries = game_context.get('injuries', [])
        if 'G1' in str(injuries):  # Goalie injury
            risk_score += 5.0
        if 'C1' in str(injuries):  # Star player
            risk_score += 4.0
        
        # Performance anomalies
        if game_context.get('line_movement_extreme', False):
            risk_score += 2.0
        
        # Classification
        if risk_score > 5.0:
            recommendation = 'AVOID_BETTING'
        elif risk_score > 2.0:
            recommendation = 'REDUCE_STAKES' 
        else:
            recommendation = 'NORMAL_BETTING'
        
        return risk_score, recommendation

    def predict_game_enhanced(self, game_id, date, home_team, away_team):
        """🚀 Enhanced prediction with all AI integrations"""
        
        # 1. Base quartet prediction (your original logic)
        base_prob = 0.55 + random.uniform(-0.1, 0.1)  # Simulate quartet
        
        # 2. Grok sentiment enhancement
        grok_boost = self.grok_sentiment_boost(home_team, date, away_team)
        sentiment_prob = base_prob + grok_boost
        
        # 3. Gemini ensemble ML
        team_features = {
            'xG_diff': random.uniform(-0.3, 0.3),
            'momentum': random.uniform(0.3, 0.7),
            'travel_fatigue': random.uniform(0.0, 0.05)
        }
        ensemble_prob = self.gemini_ensemble_prediction(sentiment_prob, team_features)
        
        # 4. Get odds and calculate metrics
        odds_data = self.fetch_odds(game_id, home_team)
        odds = odds_data["odds"]
        
        # 5. EV and Kelly
        ev = (ensemble_prob * (odds - 1)) - (1 - ensemble_prob)
        kelly_bet = self.kelly_bet_enhanced(ensemble_prob, odds)
        
        # 6. Gemini risk assessment
        game_context = {'injuries': [], 'line_movement_extreme': False}
        black_swan_risk, recommendation = self.gemini_risk_assessment(game_context)
        
        # 7. Store prediction
        prediction = {
            'game_id': game_id,
            'date': date,
            'home_team': home_team,
            'away_team': away_team,
            'quartet_prob': base_prob,
            'grok_sentiment': grok_boost,
            'gemini_ensemble': ensemble_prob,
            'final_prob': ensemble_prob,
            'odds': odds,
            'ev': ev * 100,  # Percentage
            'kelly_bet': kelly_bet,
            'black_swan_risk': black_swan_risk,
            'recommendation': recommendation
        }
        
        self.store_prediction(prediction)
        return prediction

    def kelly_bet_enhanced(self, prob, odds, correlation=0.2):
        """💰 Enhanced Kelly with correlation (Grok + Gemini suggestions)"""
        f = 0.5 * ((prob * (odds - 1) - (1 - prob)) / (odds - 1))
        f_adjusted = f * (1 - correlation)  # Correlation penalty
        return max(0, min(self.bankroll * f_adjusted, self.bankroll * 0.03))  # Cap 3%

    def store_prediction(self, prediction):
        """💾 Store enhanced prediction"""
        self.db.execute("""INSERT OR REPLACE INTO enhanced_predictions 
                          (game_id, date, home_team, away_team, quartet_prob, grok_sentiment, 
                           gemini_ensemble, final_prob, odds, ev, kelly_bet, black_swan_risk, recommendation)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (prediction['game_id'], prediction['date'], prediction['home_team'], 
                         prediction['away_team'], prediction['quartet_prob'], prediction['grok_sentiment'],
                         prediction['gemini_ensemble'], prediction['final_prob'], prediction['odds'],
                         prediction['ev'], prediction['kelly_bet'], prediction['black_swan_risk'], 
                         prediction['recommendation']))
        self.db.commit()

    def update_result(self, game_id, result):
        """📊 Update result with P&L calculation"""
        cursor = self.db.execute("SELECT kelly_bet, odds FROM enhanced_predictions WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        
        if row:
            bet_amount, odds = row
            if result == 1:  # Win
                pnl = bet_amount * (odds - 1)
            else:  # Loss
                pnl = -bet_amount
            
            self.db.execute("UPDATE enhanced_predictions SET result = ?, pnl = ? WHERE game_id = ?", 
                           (result, pnl, game_id))
            self.db.commit()
            
            # Update bankroll
            self.bankroll += pnl

    def calculate_enhanced_roi(self):
        """📈 Enhanced ROI calculation"""
        cursor = self.db.execute("""SELECT 
                                   COUNT(*) as total_games,
                                   COUNT(CASE WHEN result = 1 THEN 1 END) as wins,
                                   SUM(kelly_bet) as total_staked,
                                   SUM(CASE WHEN pnl IS NOT NULL THEN pnl ELSE 0 END) as total_pnl,
                                   AVG(final_prob) as avg_confidence
                                   FROM enhanced_predictions WHERE result IS NOT NULL""")
        
        stats = cursor.fetchone()
        if stats and stats[0] > 0:
            total_games, wins, total_staked, total_pnl, avg_confidence = stats
            win_rate = (wins / total_games) * 100 if total_games > 0 else 0
            roi = (total_pnl / total_staked) * 100 if total_staked > 0 else 0
            return {
                'total_games': total_games,
                'wins': wins,
                'win_rate': win_rate,
                'total_staked': total_staked or 0,
                'total_pnl': total_pnl or 0,
                'roi': roi,
                'balance': self.bankroll,
                'avg_confidence': avg_confidence or 0
            }
        return {'total_games': 0, 'wins': 0, 'win_rate': 0, 'roi': 0, 'balance': self.bankroll}

# Initialize enhanced engine
engine = EnhancedQuartetNHLEngine()

@app.route('/')
def index():
    """🏠 Enhanced Dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🏒 NHL Quartet Archaeological - Enhanced</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #1e3a8a 0%, #991b1b 100%); }
        .card-hover:hover { transform: translateY(-2px); transition: all 0.3s; }
    </style>
</head>
<body class="bg-gray-100">
    <div class="gradient-bg text-white py-6">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">🏒 NHL Quartet Archaeological System</h1>
            <p class="text-xl opacity-90">Grok + Gemini + ChatGPT + Copilot Fusion</p>
        </div>
    </div>
    
    <div class="container mx-auto px-4 py-6">
        <div id="app">
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Select Date:</label>
                <input type="date" id="dateInput" value="2024-09-22" 
                       class="px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
                <button onclick="fetchPredictions()" 
                        class="ml-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    Load Predictions
                </button>
            </div>
            
            <div id="performance" class="grid grid-cols-4 gap-4 mb-6"></div>
            <div id="predictions" class="space-y-4"></div>
        </div>
    </div>

    <script>
        async function fetchPredictions() {
            const date = document.getElementById('dateInput').value;
            
            try {
                // Fetch predictions
                const predResponse = await fetch(`/api/predictions/${date}`);
                const predictions = await predResponse.json();
                
                // Fetch performance
                const perfResponse = await fetch('/api/performance');
                const performance = await perfResponse.json();
                
                displayPerformance(performance);
                displayPredictions(predictions);
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function displayPerformance(perf) {
            document.getElementById('performance').innerHTML = `
                <div class="bg-white p-4 rounded shadow card-hover">
                    <h3 class="text-sm text-gray-500">Win Rate</h3>
                    <p class="text-2xl font-bold text-green-600">${perf.win_rate.toFixed(1)}%</p>
                </div>
                <div class="bg-white p-4 rounded shadow card-hover">
                    <h3 class="text-sm text-gray-500">ROI</h3>
                    <p class="text-2xl font-bold ${perf.roi >= 0 ? 'text-green-600' : 'text-red-600'}">
                        ${perf.roi.toFixed(1)}%
                    </p>
                </div>
                <div class="bg-white p-4 rounded shadow card-hover">
                    <h3 class="text-sm text-gray-500">Bankroll</h3>
                    <p class="text-2xl font-bold text-blue-600">$${perf.balance.toFixed(2)}</p>
                </div>
                <div class="bg-white p-4 rounded shadow card-hover">
                    <h3 class="text-sm text-gray-500">Games</h3>
                    <p class="text-2xl font-bold text-gray-700">${perf.total_games}</p>
                </div>
            `;
        }
        
        function displayPredictions(predictions) {
            const html = predictions.map(pred => `
                <div class="bg-white rounded-lg shadow p-6 card-hover">
                    <div class="flex justify-between mb-4">
                        <h3 class="text-xl font-bold">${pred.home_team} vs ${pred.away_team}</h3>
                        <span class="px-3 py-1 rounded-full text-sm ${
                            pred.recommendation === 'NORMAL_BETTING' ? 'bg-green-100 text-green-800' :
                            pred.recommendation === 'REDUCE_STAKES' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                        }">${pred.recommendation}</span>
                    </div>
                    
                    <div class="grid grid-cols-4 gap-4 mb-4">
                        <div>
                            <p class="text-sm text-gray-500">Final Probability</p>
                            <p class="text-lg font-bold text-blue-600">${(pred.final_prob * 100).toFixed(1)}%</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-500">Expected Value</p>
                            <p class="text-lg font-bold ${pred.ev >= 0 ? 'text-green-600' : 'text-red-600'}">
                                ${pred.ev.toFixed(1)}%
                            </p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-500">Kelly Bet</p>
                            <p class="text-lg font-bold text-purple-600">$${pred.kelly_bet.toFixed(2)}</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-500">Risk Score</p>
                            <p class="text-lg font-bold ${pred.black_swan_risk < 1 ? 'text-green-600' : 'text-red-600'}">
                                ${pred.black_swan_risk.toFixed(1)}
                            </p>
                        </div>
                    </div>
                    
                    <div class="text-xs text-gray-500 mb-3">
                        Quartet: ${(pred.quartet_prob * 100).toFixed(1)}% | 
                        Grok Sentiment: +${(pred.grok_sentiment * 100).toFixed(1)}% | 
                        Gemini Ensemble: ${(pred.gemini_ensemble * 100).toFixed(1)}%
                    </div>
                    
                    ${pred.result === null ? `
                        <div class="flex space-x-2">
                            <button onclick="updateResult('${pred.game_id}', 1)"
                                    class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                                ✅ Won
                            </button>
                            <button onclick="updateResult('${pred.game_id}', 0)"
                                    class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
                                ❌ Lost
                            </button>
                        </div>
                    ` : `
                        <div class="inline-flex items-center px-3 py-1 rounded-full text-sm ${
                            pred.result === 1 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }">
                            ${pred.result === 1 ? '✅ Won' : '❌ Lost'}
                            ${pred.pnl ? ` - P&L: $${pred.pnl.toFixed(2)}` : ''}
                        </div>
                    `}
                </div>
            `).join('');
            
            document.getElementById('predictions').innerHTML = html;
        }
        
        async function updateResult(gameId, result) {
            try {
                await fetch(`/api/results/${gameId}/${result}`, { method: 'POST' });
                fetchPredictions(); // Refresh
            } catch (error) {
                console.error('Error updating result:', error);
            }
        }
        
        // Load initial data
        fetchPredictions();
    </script>
</body>
</html>
    ''')

@app.route('/api/predictions/<date>', methods=['GET'])
def get_enhanced_predictions(date):
    """📊 Get enhanced predictions"""
    games = engine.fetch_nhl_data(date)
    predictions = []
    
    for game in games:
        home_team = game['homeTeam']['abbrev']
        away_team = game['awayTeam']['abbrev']
        
        prediction = engine.predict_game_enhanced(game['id'], date, home_team, away_team)
        predictions.append(prediction)
    
    return jsonify(predictions)

@app.route('/api/results/<game_id>/<result>', methods=['POST'])
def post_enhanced_result(game_id, result):
    """📝 Update result"""
    engine.update_result(game_id, int(result))
    return jsonify({"status": "updated", "game_id": game_id, "result": int(result)})

@app.route('/api/performance', methods=['GET'])
def get_enhanced_performance():
    """📈 Get enhanced performance stats"""
    return jsonify(engine.calculate_enhanced_roi())

if __name__ == '__main__':
    print("🚀 Starting Enhanced NHL Quartet Archaeological Flask App...")
    print("🔥 Grok Sentiment Analysis: Active")
    print("🔮 Gemini Ensemble ML: Active") 
    print("🛡️ Gemini Risk Management: Active")
    print("🌐 Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
