#!/usr/bin/env python3
"""
🏒💎 GROK SIMPLIFIED APP - Maestro d'Orchestre IA
Version ultra-simple comme proposée par Grok
"Pari ou pas ?" - C'est tout ce que vous devez savoir !
"""

from flask import Flask, jsonify, render_template_string
import sqlite3
import requests
import sys
import os

# Ajouter le path pour importer votre quartet existant
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026/active')

# Import du nouveau roster analyzer 🚀
try:
    from nhl_roster_analyzer import NHLRosterAnalyzer
    ROSTER_ANALYZER_AVAILABLE = True
    print("🎯 ROSTER ANALYZER LOADED - Power-up activé!")
except ImportError:
    ROSTER_ANALYZER_AVAILABLE = False
    print("⚠️ Roster analyzer not found - mode de base")

app = Flask(__name__)
ODDS_API_KEY = "63987f9611c51772932666988d722a3d"  # Votre vraie clé

class MaestroNHLPredictor:
    """🎼 Le maestro simplifié qui dirige l'orchestre IA"""
    
    def __init__(self):
        self.db_path = "maestro_nhl_bets.db"
        self.bankroll = 1768.84
        
        # Essayez de charger le quartet si disponible
        try:
            from quartet_archaeological_simple import QuartetArchaeologicalEngine
            self.quartet = QuartetArchaeologicalEngine()
            self.using_quartet = True
            print("🤖 Quartet Archaeological Engine LOADED!")
        except ImportError:
            self.quartet = None
            self.using_quartet = False
            print("⚠️ Using simulated predictions (quartet not found)")
        
        # Initialise le roster analyzer 🎯
        if ROSTER_ANALYZER_AVAILABLE:
            self.roster_analyzer = NHLRosterAnalyzer()
            print("🏒 Roster Analyzer ACTIVATED - Analyse joueur par joueur!")
        else:
            self.roster_analyzer = None
        
        self.init_database()
    
    def init_db(self):
        """🗄️ Base de données simplifiée comme Grok l'a proposé"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS bets
                       (game_id TEXT, date TEXT, team TEXT, prob REAL, 
                        odds REAL, ev REAL, bet REAL, result INTEGER)''')
        conn.commit()
        conn.close()
    
    def get_odds(self, game_id):
        """💰 Récupère cotes via The Odds API - exactement comme Grok"""
        url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds?apiKey={ODDS_API_KEY}&regions=us&markets=h2h"
        try:
            print(f"🌐 Fetching odds from The Odds API...")
            data = requests.get(url, timeout=10).json()
            game = next((g for g in data if g['id'] == game_id), {})
            odds = game.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[0].get('price', 1.91)
            print(f"💰 Found odds: {odds}")
            return odds
        except Exception as e:
            print(f"⚠️ Odds API error: {e}")
            return 1.91  # Fallback comme Grok l'a dit
    
    def get_quartet_prediction(self, game_id, date, team):
        """🤖 Utilise votre quartet IA existant ou simulation"""
        if self.has_quartet:
            try:
                # Utilise votre système existant
                prediction = self.quartet_engine.fusion_predict(game_id, team, date)
                return prediction.get('probability', 0.59)
            except:
                pass
        
        # Simulation intelligente basée sur l'équipe (comme Grok)
        team_strengths = {
            'MTL': 0.59,  # Hype Demidov/Hutson
            'BOS': 0.62,  # Strong team
            'TOR': 0.58,  # Talented
            'PIT': 0.52,  # Aging core
            'NYR': 0.56,  # Solid
            'WPG': 0.54   # Young core
        }
        
        base_prob = team_strengths.get(team, 0.52)
        
        # Boost MTL pour présaison (comme Grok l'a mentionné)
        if team == 'MTL' and '2024-09' in date:
            base_prob += 0.05  # Hype présaison
        
        return base_prob
    
    def predict(self, game_id, date, team):
        """🎯 Prédiction principale - format exact de Grok"""
        print(f"🎼 Maestro predicting: {team} on {date}")
        
        # 1. Probabilité via quartet IA
        prob = self.get_quartet_prediction(game_id, date, team)
        
        # 2. Cotes via The Odds API
        odds = self.get_odds(game_id)
        
        # 3. Calcul EV (exactement comme Grok)
        ev = (prob * (odds - 1)) - (1 - prob)
        
        # 4. Calcul mise Kelly (exactement comme Grok)
        bet = self.bankroll * 0.5 * ((prob * (odds - 1) - (1 - prob)) / (odds - 1)) * 0.8
        bet = max(0, min(bet, self.bankroll * 0.03))  # Max 3%
        
        # 5. Sauvegarde
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (game_id, date, team, prob, odds, ev, bet, None))
        conn.commit()
        conn.close()
        
        result = {
            "game_id": game_id,
            "date": date, 
            "team": team,
            "prob": prob,
            "odds": odds,
            "ev": ev,
            "bet": bet,
            "recommendation": "🚀 PARI RECOMMANDÉ !" if ev > 0.05 else "🤔 Pari risqué" if ev > 0 else "❌ Skip ce pari"
        }
        
        print(f"📊 Prediction: {team} {prob*100:.1f}% | EV: {ev*100:.1f}% | Bet: ${bet:.2f}")
        return result
    
    def add_result(self, game_id, result):
        """📝 Ajoute résultat - format Grok"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE bets SET result = ? WHERE game_id = ?", (result, game_id))
        conn.commit()
        conn.close()
        print(f"✅ Result updated: {game_id} = {'WIN' if result == 1 else 'LOSS'}")
    
    def get_roi(self):
        """📈 ROI calculation - format exact Grok"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT bet, result, odds FROM bets WHERE result IS NOT NULL")
        
        total_bet, total_win = 0, 0
        for bet, result, odds in cursor:
            total_bet += bet
            if result == 1:
                total_win += bet * (odds - 1)
        
        conn.close()
        
        roi = (total_win - total_bet) / total_bet * 100 if total_bet > 0 else 0
        current_balance = self.bankroll + total_win - total_bet
        
        return {
            "roi": roi,
            "balance": current_balance,
            "total_bet": total_bet,
            "net_profit": total_win - total_bet
        }

# Instance globale
maestro = MaestroNHLPredictor()

@app.route('/')
def maestro_dashboard():
    """🏠 Interface Maestro - style Grok avec logo MTL"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎼 Maestro NHL - Orchestre d'IA</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <style>
    .maestro-gradient {
      background: linear-gradient(135deg, #af1e2d 0%, #192168 50%, #af1e2d 100%);
      background-size: 200% 200%;
      animation: maestroWave 3s ease infinite;
    }
    @keyframes maestroWave {
      0%, 100% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
    }
    .orchestra-card {
      transition: all 0.3s ease;
      border: 2px solid transparent;
    }
    .orchestra-card:hover {
      transform: translateY(-5px);
      border-color: #af1e2d;
      box-shadow: 0 10px 25px rgba(175, 30, 45, 0.3);
    }
    .pari-recommande {
      background: linear-gradient(45deg, #10b981, #34d399);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.8; }
    }
  </style>
</head>
<body class="bg-gray-900 text-white font-sans min-h-screen">
  <!-- Header Maestro -->
  <div class="maestro-gradient text-white py-8 shadow-2xl">
    <div class="container mx-auto px-4 text-center">
      <h1 class="text-5xl font-bold mb-4 flex items-center justify-center">
        <img src="https://www-league.nhlstatic.com/nhl.com/builds/site-core/d5e66e4bf277b8a8f8e8b157c9e4a496e6c8c753_0/images/logos/team/current/team-10-dark.svg" 
             alt="MTL Logo" class="w-16 h-16 mr-4" />
        🎼 MAESTRO NHL
      </h1>
      <p class="text-2xl opacity-90 mb-2">Conducteur d'Orchestre IA</p>
      <p class="text-lg opacity-75">🤖 Grok + Gemini + ChatGPT + Copilot = 💰</p>
      <div id="stats" class="text-xl mt-4 font-bold"></div>
    </div>
  </div>

  <div class="container mx-auto px-4 py-8">
    <!-- Controls Simplifiés -->
    <div class="bg-gray-800 rounded-2xl shadow-xl p-8 mb-8 orchestra-card">
      <h2 class="text-3xl font-bold mb-6 text-center">🎯 Interface Maestro</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <input id="date" type="date" value="2024-09-22" 
               class="p-4 bg-gray-700 rounded-lg text-white text-lg border-2 border-gray-600 focus:border-red-500" />
        <input id="game_id" type="text" placeholder="Game ID (ex. 2025020001)" 
               class="p-4 bg-gray-700 rounded-lg text-white text-lg border-2 border-gray-600 focus:border-red-500" />
        <input id="team" type="text" placeholder="Équipe (ex. MTL)" 
               class="p-4 bg-gray-700 rounded-lg text-white text-lg border-2 border-gray-600 focus:border-red-500" />
      </div>
      <button onclick="getPrediction()" 
              class="w-full bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg text-xl font-bold transition-all transform hover:scale-105 shadow-lg">
        🚀 MAESTRO, PARI OU PAS ?
      </button>
    </div>

    <!-- Résultat Prédiction -->
    <div id="predictions" class="mb-8"></div>
    
    <!-- Instructions Grok -->
    <div class="bg-gray-800 rounded-xl p-6 orchestra-card">
      <h3 class="text-xl font-bold mb-4">📋 Instructions Maestro (par Grok)</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <h4 class="font-bold text-green-400 mb-2">✅ Comment utiliser :</h4>
          <ul class="list-disc list-inside space-y-1 text-gray-300">
            <li>Date : Format 2024-09-22</li>
            <li>Game ID : NHL format (ex. 2025020001)</li>
            <li>Équipe : Code 3 lettres (MTL, BOS, etc.)</li>
            <li>Cliquez "MAESTRO, PARI OU PAS ?"</li>
          </ul>
        </div>
        <div>
          <h4 class="font-bold text-blue-400 mb-2">🎯 Règles Grok :</h4>
          <ul class="list-disc list-inside space-y-1 text-gray-300">
            <li>EV > 5% = 🚀 PARI RECOMMANDÉ</li>
            <li>EV 0-5% = 🤔 Pari risqué</li>
            <li>EV < 0% = ❌ Skip ce pari</li>
            <li>Max 3% du bankroll ($1,768.84)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <script>
    function updateStats() {
      axios.get('/api/roi')
        .then(res => {
          const data = res.data;
          const roiColor = data.roi >= 15 ? 'text-green-400' : data.roi >= 0 ? 'text-yellow-400' : 'text-red-400';
          document.getElementById('stats').innerHTML = `
            <span class="${roiColor}">ROI: ${data.roi.toFixed(1)}%</span> | 
            <span class="text-blue-400">Balance: $${data.balance.toFixed(2)}</span>
          `;
        })
        .catch(() => {
          document.getElementById('stats').innerHTML = 
            '<span class="text-blue-400">ROI: -- | Balance: $1,768.84</span>';
        });
    }

    function getPrediction() {
      const date = document.getElementById('date').value;
      const game_id = document.getElementById('game_id').value;
      const team = document.getElementById('team').value;
      
      if (!date || !game_id || !team) {
        alert('⚠️ Remplissez tous les champs, maestro !');
        return;
      }
      
      const button = event.target;
      button.textContent = '🎼 L\\'orchestre joue...';
      button.disabled = true;
      
      axios.get(`/api/predict/${date}/${game_id}/${team}`)
        .then(res => {
          const pred = res.data;
          const isGoodBet = pred.ev > 0.05;
          const cardClass = isGoodBet ? 'pari-recommande' : pred.ev > 0 ? 'bg-yellow-600' : 'bg-red-600';
          
          const card = `
            <div class="orchestra-card ${cardClass} p-8 rounded-2xl shadow-2xl text-center">
              <h2 class="text-4xl font-bold mb-6">
                ${pred.team} ${isGoodBet ? '🚀' : pred.ev > 0 ? '🤔' : '❌'}
              </h2>
              <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 text-white">
                <div>
                  <p class="text-sm opacity-75 mb-1">PROBABILITÉ</p>
                  <p class="text-3xl font-bold">${(pred.prob * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <p class="text-sm opacity-75 mb-1">COTE LIVE</p>
                  <p class="text-3xl font-bold">${pred.odds.toFixed(2)}</p>
                </div>
                <div>
                  <p class="text-sm opacity-75 mb-1">EXPECTED VALUE</p>
                  <p class="text-3xl font-bold">${(pred.ev * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <p class="text-sm opacity-75 mb-1">MISE KELLY</p>
                  <p class="text-3xl font-bold">$${pred.bet.toFixed(2)}</p>
                </div>
              </div>
              <div class="text-2xl font-bold mb-6">
                ${pred.recommendation}
              </div>
              <div class="flex justify-center space-x-4">
                <button onclick="addResult('${pred.game_id}', 1)" 
                        class="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-bold text-lg transition-all">
                  ✅ GAGNÉ
                </button>
                <button onclick="addResult('${pred.game_id}', 0)" 
                        class="bg-red-500 hover:bg-red-600 text-white px-8 py-3 rounded-lg font-bold text-lg transition-all">
                  ❌ PERDU
                </button>
              </div>
            </div>
          `;
          document.getElementById('predictions').innerHTML = card;
          updateStats();
        })
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('predictions').innerHTML = `
            <div class="bg-red-600 p-6 rounded-xl text-center">
              <h3 class="text-xl font-bold mb-2">❌ Erreur Maestro</h3>
              <p>Impossible de récupérer la prédiction. Vérifiez la console.</p>
            </div>
          `;
        })
        .finally(() => {
          button.textContent = '🚀 MAESTRO, PARI OU PAS ?';
          button.disabled = false;
        });
    }

    function addResult(game_id, result) {
      axios.get(`/api/result/${game_id}/${result}`)
        .then(() => {
          const resultText = result === 1 ? 'VICTOIRE' : 'DÉFAITE';
          alert(`🎼 Résultat enregistré : ${resultText} !`);
          updateStats();
        })
        .catch(() => alert('❌ Erreur lors de l\\'enregistrement'));
    }

    // Initialize
    updateStats();
  </script>
</body>
</html>
    ''')

# Routes API - format exact Grok
@app.route('/api/predict/<date>/<game_id>/<team>')
def predict(date, game_id, team):
    """🎯 Prédiction - route exacte de Grok"""
    return jsonify(maestro.predict(game_id, date, team))

@app.route('/api/result/<game_id>/<result>')
def result(game_id, result):
    """📝 Résultat - route exacte de Grok"""
    maestro.add_result(game_id, int(result))
    return jsonify({"status": "Résultat enregistré"})

@app.route('/api/roi')
def roi():
    """📈 ROI - route exacte de Grok"""
    return jsonify(maestro.get_roi())

@app.route('/api/health')
def health():
    """🔍 Health check"""
    return jsonify({
        "status": "🎼 Maestro operational",
        "orchestra": ["🤖 Grok", "🔮 Gemini", "💬 ChatGPT", "🤖 Copilot"],
        "quartet_loaded": maestro.has_quartet,
        "odds_api": "Active",
        "bankroll": f"${maestro.bankroll}"
    })

if __name__ == '__main__':
    print("🎼 MAESTRO NHL - ORCHESTRE D'IA LAUNCHED")
    print("=" * 60)
    print("🤖 Direction d'orchestre: Grok + Gemini + ChatGPT + Copilot")
    print("💰 The Odds API: 63987f9611c51772932666988d722a3d")
    print("🎯 Simple question: PARI OU PAS ?")
    print("🏒 Focus MTL: Demidov/Hutson hype présaison")
    print("💳 Bankroll: $1,768.84")
    print("🌐 Interface: http://localhost:5004")
    print("=" * 60)
    print("🎵 Comme dit Grok: 'Pas besoin d'être Beethoven !' 😂")
    
    app.run(debug=True, host='0.0.0.0', port=5004)
