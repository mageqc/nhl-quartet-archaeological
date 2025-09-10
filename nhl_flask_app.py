#!/usr/bin/env python3
"""
🏒🚀 NHL FLASK APP - Intégration Complete avec Quartet Archaeological
Version améliorée de votre app.py avec toutes les améliorations Grok + Gemini
"""

from flask import Flask, jsonify, render_template_string, request
import sqlite3
import requests
import json
import os
from datetime import datetime, timedelta

# Import des améliorations IA
try:
    from quartet_archaeological_simple import QuartetArchaeologicalSimple
    from grok_sentiment_enhancer import GrokSentimentEnhancer
    from gemini_ensemble_learning import GeminiEnsembleLearning
    from gemini_risk_management import GeminiRiskManagement
    ENHANCED_AI_AVAILABLE = True
except ImportError:
    ENHANCED_AI_AVAILABLE = False
    print("⚠️ Enhanced AI modules not found, using basic simulation")

app = Flask(__name__)

class EnhancedQuartetNHLEngine:
    """🎯 Version améliorée avec toutes les suggestions Grok + Gemini"""
    
    def __init__(self, db_file="nhl_enhanced.db"):
        self.db_file = db_file
        self.init_database()
        
        # Intégration modules IA avancés
        if ENHANCED_AI_AVAILABLE:
            self.quartet_engine = QuartetArchaeologicalSimple(db_path=db_file)
            self.grok_enhancer = GrokSentimentEnhancer()
            self.gemini_ml = GeminiEnsembleLearning()
            self.gemini_risk = GeminiRiskManagement()
        
        # Configuration
        self.api_key_odds = os.getenv('ODDS_API_KEY', 'demo_key')
        self.bankroll = float(os.getenv('BANKROLL', '1768.84'))
        
        # Cache pour performance
        self.cache = {}
        
    def init_database(self):
        """🗄️ Initialize enhanced database schema"""
        conn = sqlite3.connect(self.db_file)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT UNIQUE,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                quartet_prob REAL,
                grok_sentiment_boost REAL,
                gemini_ensemble_prob REAL,
                final_probability REAL,
                odds REAL,
                ev_percentage REAL,
                kelly_bet_amount REAL,
                black_swan_score REAL,
                recommendation TEXT,
                actual_result INTEGER,
                pnl REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_tracking (
                date TEXT PRIMARY KEY,
                total_bets INTEGER,
                wins INTEGER,
                win_rate REAL,
                total_staked REAL,
                total_return REAL,
                roi_percentage REAL,
                bankroll_balance REAL
            )
        ''')
        
        conn.commit()
        conn.close()

    def fetch_nhl_games(self, date):
        """🏒 Fetch NHL games with enhanced error handling"""
        cache_key = f"games_{date}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        formatted_date = date.replace('-', '')
        url = f"https://api-web.nhle.com/v1/schedule/{formatted_date}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            games = []
            if 'gameWeek' in data and data['gameWeek']:
                for day in data['gameWeek']:
                    if 'games' in day:
                        games.extend(day['games'])
            
            self.cache[cache_key] = games
            return games
            
        except Exception as e:
            print(f"⚠️ NHL API Error: {e}")
            # Fallback avec données simulées
            return self._get_simulated_games(date)
    
    def _get_simulated_games(self, date):
        """🎯 Fallback simulated games for demo"""
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

    def get_enhanced_prediction(self, game_id, date, home_team, away_team):
        """🚀 Enhanced prediction avec toutes les améliorations IA"""
        
        # 1. Base quartet prediction
        if ENHANCED_AI_AVAILABLE:
            quartet_result = self.quartet_engine.quartet_ultimate_prediction(home_team, away_team, date)
            base_prob = quartet_result.get('quartet_final_prob', 0.55)
        else:
            base_prob = 0.55  # Simulation
        
        # 2. Grok sentiment enhancement
        if ENHANCED_AI_AVAILABLE and home_team == 'MTL':
            grok_result = self.grok_enhancer.grok_enhanced_prediction(base_prob, home_team, date, away_team)
            sentiment_boost = grok_result['sentiment_boost']
            enhanced_prob = grok_result['enhanced_prob']
        else:
            sentiment_boost = 0.0
            enhanced_prob = base_prob
        
        # 3. Gemini ensemble ML
        if ENHANCED_AI_AVAILABLE:
            team_features = {'xG': 2.6, 'PDO': 1.02, 'rookie_impact': 0.3 if home_team == 'MTL' else 0.0}
            opponent_features = {'xG': 2.4, 'PDO': 0.98, 'rookie_impact': 0.0}
            game_context = {'home': True, 'b2b': False, 'rivalry': away_team in ['BOS', 'TOR'], 'sentiment_boost': sentiment_boost}
            
            gemini_result = self.gemini_ml.ensemble_prediction(team_features, opponent_features, game_context, enhanced_prob)
            final_prob = gemini_result['ensemble_probability']
        else:
            final_prob = enhanced_prob
        
        # 4. Get odds (simulation or real)
        odds = self._get_odds(game_id, home_team)
        
        # 5. Calculate EV and Kelly
        ev_percentage = (final_prob * (odds - 1)) - (1 - final_prob)
        kelly_fraction = self._calculate_kelly(final_prob, odds)
        kelly_bet_amount = self.bankroll * kelly_fraction
        
        # 6. Black Swan risk assessment
        if ENHANCED_AI_AVAILABLE:
            black_swan_result = self.gemini_risk.detect_black_swan_events(
                {'injuries': [], 'performance_flags': []},
                {'line_movement_pct': 0.0},
                {}
            )
            black_swan_score = black_swan_result['black_swan_score']
            recommendation = black_swan_result['recommendation']
        else:
            black_swan_score = 0.0
            recommendation = 'NORMAL_BETTING' if ev_percentage > 0.05 else 'PASS'
        
        # 7. Store prediction
        prediction = {
            'game_id': game_id,
            'date': date,
            'home_team': home_team,
            'away_team': away_team,
            'quartet_prob': base_prob,
            'grok_sentiment_boost': sentiment_boost,
            'gemini_ensemble_prob': final_prob,
            'final_probability': final_prob,
            'odds': odds,
            'ev_percentage': ev_percentage * 100,
            'kelly_bet_amount': kelly_bet_amount,
            'black_swan_score': black_swan_score,
            'recommendation': recommendation
        }
        
        self._store_prediction(prediction)
        return prediction
    
    def _get_odds(self, game_id, team):
        """💰 Get odds (simulation or The Odds API)"""
        # Simulation pour demo
        if team == 'MTL':
            return 1.91  # -110 odds
        return 1.95
    
    def _calculate_kelly(self, prob, odds, correlation=0.2):
        """🎯 Kelly Criterion with correlation adjustment"""
        f = ((prob * odds - 1) / (odds - 1))
        f_adjusted = f * (1 - correlation)
        return max(0, min(f_adjusted, 0.03))  # Cap at 3%
    
    def _store_prediction(self, prediction):
        """💾 Store prediction in database"""
        conn = sqlite3.connect(self.db_file)
        conn.execute('''
            INSERT OR REPLACE INTO enhanced_predictions 
            (game_id, date, home_team, away_team, quartet_prob, grok_sentiment_boost, 
             gemini_ensemble_prob, final_probability, odds, ev_percentage, 
             kelly_bet_amount, black_swan_score, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            prediction['game_id'], prediction['date'], prediction['home_team'], prediction['away_team'],
            prediction['quartet_prob'], prediction['grok_sentiment_boost'], prediction['gemini_ensemble_prob'],
            prediction['final_probability'], prediction['odds'], prediction['ev_percentage'],
            prediction['kelly_bet_amount'], prediction['black_swan_score'], prediction['recommendation']
        ))
        conn.commit()
        conn.close()
    
    def update_result(self, game_id, result):
        """📊 Update game result and calculate P&L"""
        conn = sqlite3.connect(self.db_file)
        
        # Get prediction
        cursor = conn.execute("SELECT kelly_bet_amount, odds FROM enhanced_predictions WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        
        if row:
            bet_amount, odds = row
            if result == 1:  # Win
                pnl = bet_amount * (odds - 1)
            else:  # Loss
                pnl = -bet_amount
            
            # Update result
            conn.execute("UPDATE enhanced_predictions SET actual_result = ?, pnl = ? WHERE game_id = ?", 
                        (result, pnl, game_id))
            
            # Update bankroll
            self.bankroll += pnl
        
        conn.commit()
        conn.close()
    
    def get_performance_stats(self):
        """📈 Calculate comprehensive performance statistics"""
        conn = sqlite3.connect(self.db_file)
        
        # Overall stats
        cursor = conn.execute('''
            SELECT 
                COUNT(*) as total_predictions,
                COUNT(CASE WHEN actual_result IS NOT NULL THEN 1 END) as completed_games,
                COUNT(CASE WHEN actual_result = 1 THEN 1 END) as wins,
                SUM(CASE WHEN actual_result IS NOT NULL THEN kelly_bet_amount ELSE 0 END) as total_staked,
                SUM(CASE WHEN pnl IS NOT NULL THEN pnl ELSE 0 END) as total_pnl,
                AVG(final_probability) as avg_confidence
            FROM enhanced_predictions
        ''')
        
        stats = cursor.fetchone()
        
        if stats and stats[1] > 0:  # completed_games > 0
            total_predictions, completed_games, wins, total_staked, total_pnl, avg_confidence = stats
            win_rate = (wins / completed_games) * 100 if completed_games > 0 else 0
            roi_percentage = (total_pnl / total_staked) * 100 if total_staked > 0 else 0
        else:
            total_predictions = completed_games = wins = 0
            total_staked = total_pnl = win_rate = roi_percentage = avg_confidence = 0
        
        conn.close()
        
        return {
            'total_predictions': total_predictions,
            'completed_games': completed_games,
            'wins': wins,
            'win_rate': win_rate,
            'total_staked': total_staked,
            'total_pnl': total_pnl,
            'roi_percentage': roi_percentage,
            'current_bankroll': self.bankroll,
            'avg_confidence': avg_confidence or 0
        }

# Initialize engine
engine = EnhancedQuartetNHLEngine()

# Routes
@app.route('/')
def index():
    """🏠 Main dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏒 NHL Quartet Archaeological Predictions</title>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #1e3a8a 0%, #991b1b 100%); }
        .card-hover:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    </style>
</head>
<body class="bg-gray-100">
    <div id="root"></div>
    
    <script type="text/babel">
        const { useState, useEffect } = React;
        
        function App() {
            const [predictions, setPredictions] = useState([]);
            const [performance, setPerformance] = useState({});
            const [selectedDate, setSelectedDate] = useState('2024-09-22');
            const [loading, setLoading] = useState(false);
            
            const fetchPredictions = async (date) => {
                setLoading(true);
                try {
                    const response = await fetch(`/api/predictions/${date}`);
                    const data = await response.json();
                    setPredictions(data);
                } catch (error) {
                    console.error('Error fetching predictions:', error);
                } finally {
                    setLoading(false);
                }
            };
            
            const fetchPerformance = async () => {
                try {
                    const response = await fetch('/api/performance');
                    const data = await response.json();
                    setPerformance(data);
                } catch (error) {
                    console.error('Error fetching performance:', error);
                }
            };
            
            const updateResult = async (gameId, result) => {
                try {
                    await fetch(`/api/results/${gameId}/${result}`, { method: 'POST' });
                    fetchPerformance();
                    fetchPredictions(selectedDate);
                } catch (error) {
                    console.error('Error updating result:', error);
                }
            };
            
            useEffect(() => {
                fetchPredictions(selectedDate);
                fetchPerformance();
            }, [selectedDate]);
            
            return (
                <div className="min-h-screen bg-gray-50">
                    {/* Header */}
                    <div className="gradient-bg text-white py-6">
                        <div className="container mx-auto px-4">
                            <h1 className="text-3xl font-bold flex items-center">
                                🏒 NHL Quartet Archaeological Predictions
                                <span className="ml-4 text-sm bg-white bg-opacity-20 px-3 py-1 rounded-full">
                                    Grok + Gemini + ChatGPT + Copilot
                                </span>
                            </h1>
                        </div>
                    </div>
                    
                    {/* Performance Stats */}
                    <div className="container mx-auto px-4 py-6">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div className="bg-white p-4 rounded-lg shadow card-hover">
                                <h3 className="text-sm font-medium text-gray-500">Win Rate</h3>
                                <p className="text-2xl font-bold text-green-600">{performance.win_rate?.toFixed(1) || 0}%</p>
                            </div>
                            <div className="bg-white p-4 rounded-lg shadow card-hover">
                                <h3 className="text-sm font-medium text-gray-500">ROI</h3>
                                <p className={`text-2xl font-bold ${(performance.roi_percentage || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    {performance.roi_percentage?.toFixed(1) || 0}%
                                </p>
                            </div>
                            <div className="bg-white p-4 rounded-lg shadow card-hover">
                                <h3 className="text-sm font-medium text-gray-500">Bankroll</h3>
                                <p className="text-2xl font-bold text-blue-600">${performance.current_bankroll?.toFixed(2) || 0}</p>
                            </div>
                            <div className="bg-white p-4 rounded-lg shadow card-hover">
                                <h3 className="text-sm font-medium text-gray-500">Completed Games</h3>
                                <p className="text-2xl font-bold text-gray-700">{performance.completed_games || 0}</p>
                            </div>
                        </div>
                        
                        {/* Date Selection */}
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Select Date:</label>
                            <input
                                type="date"
                                value={selectedDate}
                                onChange={(e) => setSelectedDate(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        
                        {/* Predictions */}
                        <div className="space-y-4">
                            {loading ? (
                                <div className="text-center py-8">
                                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                                    <p className="mt-2 text-gray-600">Loading predictions...</p>
                                </div>
                            ) : predictions.length === 0 ? (
                                <div className="text-center py-8 text-gray-500">
                                    No games found for selected date
                                </div>
                            ) : (
                                predictions.map((pred) => (
                                    <div key={pred.game_id} className="bg-white rounded-lg shadow-md p-6 card-hover">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className="text-xl font-bold text-gray-800">
                                                    {pred.home_team} vs {pred.away_team}
                                                </h3>
                                                <p className="text-gray-600">Game ID: {pred.game_id}</p>
                                            </div>
                                            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                                                pred.recommendation === 'NORMAL_BETTING' ? 'bg-green-100 text-green-800' :
                                                pred.recommendation === 'REDUCE_STAKES' ? 'bg-yellow-100 text-yellow-800' :
                                                'bg-red-100 text-red-800'
                                            }`}>
                                                {pred.recommendation}
                                            </div>
                                        </div>
                                        
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                                            <div>
                                                <p className="text-sm text-gray-500">Final Probability</p>
                                                <p className="text-lg font-bold text-blue-600">{(pred.final_probability * 100).toFixed(1)}%</p>
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Expected Value</p>
                                                <p className={`text-lg font-bold ${pred.ev_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                                    {pred.ev_percentage.toFixed(1)}%
                                                </p>
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Suggested Bet</p>
                                                <p className="text-lg font-bold text-purple-600">${pred.kelly_bet_amount.toFixed(2)}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Black Swan Risk</p>
                                                <p className={`text-lg font-bold ${
                                                    pred.black_swan_score < 1 ? 'text-green-600' : 
                                                    pred.black_swan_score < 2 ? 'text-yellow-600' : 'text-red-600'
                                                }`}>
                                                    {pred.black_swan_score.toFixed(1)}
                                                </p>
                                            </div>
                                        </div>
                                        
                                        {pred.actual_result === null && (
                                            <div className="flex space-x-2">
                                                <button
                                                    onClick={() => updateResult(pred.game_id, 1)}
                                                    className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
                                                >
                                                    ✅ Won
                                                </button>
                                                <button
                                                    onClick={() => updateResult(pred.game_id, 0)}
                                                    className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                                                >
                                                    ❌ Lost
                                                </button>
                                            </div>
                                        )}
                                        
                                        {pred.actual_result !== null && (
                                            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                                                pred.actual_result === 1 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                            }`}>
                                                {pred.actual_result === 1 ? '✅ Won' : '❌ Lost'}
                                                {pred.pnl && (
                                                    <span className="ml-2">
                                                        P&L: ${pred.pnl.toFixed(2)}
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            );
        }
        
        ReactDOM.render(<App />, document.getElementById('root'));
    </script>
</body>
</html>
    ''')

@app.route('/api/predictions/<date>')
def get_predictions(date):
    """📊 Get predictions for specific date"""
    games = engine.fetch_nhl_games(date)
    predictions = []
    
    for game in games:
        home_team = game['homeTeam']['abbrev']
        away_team = game['awayTeam']['abbrev']
        
        prediction = engine.get_enhanced_prediction(
            game['id'], date, home_team, away_team
        )
        predictions.append(prediction)
    
    return jsonify(predictions)

@app.route('/api/results/<game_id>/<int:result>', methods=['POST'])
def update_result(game_id, result):
    """📝 Update game result"""
    engine.update_result(game_id, result)
    return jsonify({"status": "success", "game_id": game_id, "result": result})

@app.route('/api/performance')
def get_performance():
    """📈 Get performance statistics"""
    return jsonify(engine.get_performance_stats())

if __name__ == '__main__':
    print("🚀 Starting NHL Quartet Archaeological Flask App...")
    print("📊 Enhanced with Grok + Gemini + ChatGPT + Copilot")
    print("🌐 Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
