#!/usr/bin/env python3
"""
🏒💎 MAESTRO GROK + ROSTER ANALYZER - Version Power-Up
Version ultra-simple + analyse joueur par joueur comme demandée
"Pari ou pas ?" avec pondération équipe MTL Demidov/Hutson/Dobson
"""

from flask import Flask, jsonify, render_template_string
import sqlite3
import requests
import sys
import os
from datetime import datetime

# Ajouter le path pour importer 
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026/active')

# Import du roster analyzer + BRIDGE REAL DATA 🚀
try:
    from nhl_roster_analyzer import NHLRosterAnalyzer
    ROSTER_ANALYZER_AVAILABLE = True
    print("🎯 ROSTER ANALYZER LOADED - Power-up activé!")
except ImportError:
    ROSTER_ANALYZER_AVAILABLE = False
    print("⚠️ Roster analyzer not found - mode de base")

# Import du bridge pour vraies données NHL
try:
    from nhl_maestro_bridge import NHLMaestroBridge
    REAL_DATA_BRIDGE_AVAILABLE = True
    print("🔗 NHL REAL DATA BRIDGE LOADED - Vraies données activées!")
except ImportError:
    REAL_DATA_BRIDGE_AVAILABLE = False
    print("⚠️ Real data bridge not found")

app = Flask(__name__)
ODDS_API_KEY = "63987f9611c51772932666988d722a3d"  # Votre vraie clé

class MaestroNHLPredictor:
    """🎼 Le maestro simplifié qui dirige l'orchestre IA + ROSTER ANALYSIS"""
    
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
        
        # Initialise le roster analyzer + BRIDGE REAL DATA 🎯
        if ROSTER_ANALYZER_AVAILABLE:
            self.roster_analyzer = NHLRosterAnalyzer()
            print("🏒 Roster Analyzer ACTIVATED - Analyse joueur par joueur!")
        else:
            self.roster_analyzer = None
            
        # Initialise le bridge pour vraies données NHL 🔗
        if REAL_DATA_BRIDGE_AVAILABLE:
            self.real_data_bridge = NHLMaestroBridge()
            print("🔗 Real NHL Data Bridge ACTIVATED - 1,358 joueurs réels!")
        else:
            self.real_data_bridge = None
        
        self.init_database()
    
    def init_database(self):
        """🗄️ Database pour stocker les paris Maestro"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS bets 
                       (id INTEGER PRIMARY KEY, date TEXT, game_id TEXT, team TEXT, 
                        prob REAL, odds REAL, ev REAL, bet_amount REAL, result INTEGER,
                        roster_score REAL, roster_boost REAL, key_players TEXT, created_at TEXT)''')
        
        # Ajoute la colonne bet_amount si elle n'existe pas (compatibilité)
        try:
            conn.execute("SELECT bet_amount FROM bets LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE bets ADD COLUMN bet_amount REAL DEFAULT 0")
        conn.commit()
        conn.close()
        print("💾 Database initialized")
    
    def get_odds_from_api(self, team):
        """💰 Récupère les vraies cotes via The Odds API"""
        try:
            url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds"
            params = {
                'apiKey': ODDS_API_KEY,
                'regions': 'us',
                'markets': 'h2h',
                'oddsFormat': 'decimal'
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Simulate finding team odds
                for game in data[:3]:  # Check first 3 games
                    for bookmaker in game.get('bookmakers', []):
                        for market in bookmaker.get('markets', []):
                            for outcome in market.get('outcomes', []):
                                if team.upper() in outcome.get('name', '').upper():
                                    print(f"💰 {team} odds: {outcome['price']}")
                                    return float(outcome['price'])
                
            print(f"⚠️ No specific odds found for {team}, using average")
            return 1.95  # Reasonable default
            
        except Exception as e:
            print(f"⚠️ Odds API error: {e}")
            return 1.91  # Fallback comme Grok l'a dit
    
    def predict_game_with_roster(self, date, game_id, team):
        """🔮 PRÉDICTION ULTIME: Quartet + Roster Analysis"""
        
        # 1. ANALYSE ROSTER avec VRAIES DONNÉES NHL 🎯
        roster_boost = 0
        roster_info = {}
        
        # Priorité au bridge avec vraies données
        if self.real_data_bridge:
            try:
                roster_analysis = self.real_data_bridge.get_real_team_analysis(team, date)
                # Convertit score roster (0-100) en boost probabilité (-10% à +10%)
                roster_boost = (roster_analysis["roster_score"] - 80) / 200  # Score 90 = +5%, Score 70 = -5%
                roster_info = {
                    "score": roster_analysis["roster_score"],
                    "tier": roster_analysis["tier_description"],
                    "key_players": roster_analysis["key_players"][:2],  # Top 2 seulement
                    "rumors": roster_analysis["active_rumors"],
                    "boost_pct": round(roster_boost * 100, 1),  # En %
                    "data_source": roster_analysis["data_source"],
                    "avg_age": roster_analysis.get("avg_age", 0),
                    "roster_size": roster_analysis.get("roster_size", 0)
                }
                print(f"🔗 {team} REAL DATA: {roster_analysis['roster_score']}/100 {roster_analysis['tier_description']}")
                print(f"⭐ Stars: {', '.join(roster_analysis['key_players'][:2])}")
                print(f"📊 {roster_analysis['roster_size']} joueurs, âge: {roster_analysis.get('avg_age', 0)} ans")
                if roster_analysis['active_rumors']:
                    print(f"📰 Hype: {', '.join(roster_analysis['active_rumors'])}")
            except Exception as e:
                print(f"⚠️ Real data bridge error: {e}")
                roster_boost = 0
        
        # Fallback vers roster analyzer simulé
        elif self.roster_analyzer:
            try:
                roster_analysis = self.roster_analyzer.analyze_team_performance(team, date)
                # Convertit score roster (0-100) en boost probabilité (-10% à +10%)
                roster_boost = (roster_analysis["roster_score"] - 80) / 200  # Score 90 = +5%, Score 70 = -5%
                roster_info = {
                    "score": roster_analysis["roster_score"],
                    "tier": roster_analysis["tier_description"],
                    "key_players": roster_analysis["key_players"][:2],  # Top 2 seulement
                    "rumors": roster_analysis["active_rumors"],
                    "boost_pct": round(roster_boost * 100, 1),  # En %
                    "data_source": "SIMULATED"
                }
                print(f"🏒 {team} Roster (SIM): {roster_analysis['roster_score']}/100 {roster_analysis['tier_description']}")
                print(f"⭐ Stars: {', '.join(roster_analysis['key_players'][:2])}")
                if roster_analysis['active_rumors']:
                    print(f"📰 Hype: {', '.join(roster_analysis['active_rumors'])}")
            except Exception as e:
                print(f"⚠️ Roster analyzer error: {e}")
                roster_boost = 0
        
        # 2. PRÉDICTION BASE - Quartet ou simulation
        if self.using_quartet and self.quartet:
            try:
                # Utilise le quartet existant
                prediction = self.quartet.fusion_predict(game_id, team, date)
                prob = prediction.get('probability', 0.52)
                confidence = prediction.get('confidence', 0.75)
                print(f"🤖 Quartet prediction: {prob:.1%} (confidence: {confidence:.1%})")
            except Exception as e:
                print(f"⚠️ Quartet error: {e}")
                prob, confidence = 0.52, 0.60
        else:
            # Simulation basique mais réaliste selon les forces d'équipes
            base_probs = {
                'MTL': 0.58,  # Boost Demidov/Hutson hype présaison
                'TOR': 0.55,  # Talents mais problèmes récurrents
                'BOS': 0.54,  # Solide mais vieillissante  
                'PIT': 0.48,  # Core vieillissant
                'FLA': 0.62, # Defending champs
                'NYR': 0.56,  # Shesterkin factor
                'EDM': 0.64,  # McDavid/Draisaitl
            }
            prob = base_probs.get(team.upper(), 0.50)
            confidence = 0.65
        
        # 3. APPLIQUE LE BOOST ROSTER 🚀
        prob_final = max(0.15, min(0.85, prob + roster_boost))
        
        print(f"📊 Probabilité finale: {prob:.1%} + roster({roster_boost*100:+.1f}%) = {prob_final:.1%}")
        
        # 4. RÉCUPÈRE LES COTES
        odds = self.get_odds_from_api(team)
        
        # 5. CALCUL EV ET MISE KELLY
        ev = (prob_final * (odds - 1)) - (1 - prob_final)
        
        # Kelly Criterion avec factor de sécurité 0.25 (très conservateur selon Grok)
        kelly_fraction = ((prob_final * odds - 1) / (odds - 1)) * 0.25
        bet_amount = max(0, min(kelly_fraction * self.bankroll, self.bankroll * 0.03))  # Max 3%
        
        return {
            "date": date,
            "game_id": game_id,
            "team": team.upper(),
            "probability": round(prob_final, 3),
            "base_prob": round(prob, 3),
            "roster_boost": round(roster_boost, 3),
            "odds": round(odds, 2),
            "ev": round(ev, 4),
            "ev_pct": round(ev * 100, 1),
            "bet_amount": round(bet_amount, 2),
            "confidence": round(confidence, 2),
            "roster_info": roster_info,
            "recommendation": "🚀 PARI RECOMMANDÉ!" if ev > 0.05 else "🤔 Pari risqué" if ev > 0 else "❌ SKIP ce pari"
        }
    
    def save_bet(self, prediction_data):
        """💾 Sauvegarde le pari en DB"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''INSERT INTO bets 
                       (date, game_id, team, prob, odds, ev, bet_amount, roster_score, roster_boost, key_players, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (prediction_data["date"], 
                     prediction_data["game_id"], 
                     prediction_data["team"],
                     prediction_data["probability"], 
                     prediction_data["odds"], 
                     prediction_data["ev"],
                     prediction_data["bet_amount"],
                     prediction_data["roster_info"].get("score", 0),
                     prediction_data["roster_boost"],
                     ",".join(prediction_data["roster_info"].get("key_players", [])),
                     datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_roi(self):
        """📈 ROI calculation - format exact Grok"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT bet_amount, result, odds FROM bets WHERE result IS NOT NULL")
        
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
    """🏠 Interface Maestro + ROSTER ANALYSIS - style Grok avec logo MTL"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎼 Maestro NHL + Roster Analysis</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <style>
    body { background: linear-gradient(135deg, #1e3a8a 0%, #7c2d12 100%); }
    .pari-recommande { 
      background: linear-gradient(45deg, #059669, #0d9488); 
      animation: pulse 2s infinite;
    }
    .mtl-glow { box-shadow: 0 0 20px #ef4444; }
  </style>
</head>
<body class="text-white min-h-screen font-mono">
  <div class="container mx-auto p-6 max-w-4xl">
    
    <!-- Header MTL Style -->
    <div class="text-center mb-8">
      <div class="flex items-center justify-center mb-4">
        <img src="https://www-league.nhlstatic.com/nhl.com/builds/site-core/d5e66e4bf277b8a8f8e8b157c9e4a496e6c8c753_0/images/logos/team/current/team-10-dark.svg" 
             alt="MTL" class="w-16 h-16 mr-4 mtl-glow">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-red-400 to-blue-400 bg-clip-text text-transparent">
          MAESTRO NHL + ROSTER ANALYZER
        </h1>
      </div>
      <p class="text-xl text-gray-300">🎼 Direction d'orchestre: Grok + Vraies Données NHL</p>
      <p class="text-lg text-blue-400">🏒 Focus: 1,358 joueurs réels analysés en temps réel</p>
      <div id="stats" class="text-xl mt-4 font-bold"></div>
    </div>

    <!-- Input Form -->
    <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-600">
      <h3 class="text-2xl font-bold mb-4 text-center">🤔 Question Simple de Grok:</h3>
      <h2 class="text-3xl font-bold text-center mb-6 text-yellow-400">PARI OU PAS ?</h2>
      
      <div class="grid md:grid-cols-3 gap-4 mb-4">
        <input type="date" id="date" value="2025-09-22" 
               class="p-3 bg-gray-700 rounded border border-gray-500 text-white focus:border-blue-400">
        <input type="text" id="game_id" placeholder="Game ID (ex: 2025020001)" 
               class="p-3 bg-gray-700 rounded border border-gray-500 text-white focus:border-blue-400">
        <input type="text" id="team" placeholder="Équipe (ex: MTL)" 
               class="p-3 bg-gray-700 rounded border border-gray-500 text-white focus:border-blue-400">
      </div>
      
      <button onclick="getPrediction()" 
              class="w-full bg-gradient-to-r from-blue-600 to-red-600 hover:from-blue-700 hover:to-red-700 text-white font-bold py-4 px-6 rounded-lg text-xl transition-all transform hover:scale-105">
        🎼 MAESTRO, PARI OU PAS ?
      </button>
    </div>

    <!-- Résultat Prédiction -->
    <div id="prediction-result"></div>

    <!-- Guide Grok -->
    <div class="grid md:grid-cols-2 gap-6 mt-8">
      <div class="bg-gray-800 rounded-lg p-4 border border-gray-600">
        <h4 class="font-bold text-blue-400 mb-2">🎯 Règles Maestro + Roster:</h4>
        <ul class="list-disc list-inside space-y-1 text-gray-300 text-sm">
          <li>Roster Score >85 = 🏆 Équipe playoffs</li>
          <li>Demidov/Hutson hype = 🚀 Boost MTL</li>
          <li>EV >5% = 💚 PARI RECOMMANDÉ</li>
          <li>Max 3% bankroll (${{ "%.2f"|format(maestro.bankroll * 0.03) }})</li>
        </ul>
      </div>
      <div class="bg-gray-800 rounded-lg p-4 border border-gray-600">
        <h4 class="font-bold text-yellow-400 mb-2">⭐ Joueurs Clés MTL:</h4>
        <ul class="list-disc list-inside space-y-1 text-gray-300 text-sm">
          <li>🔥 Demidov (hype présaison)</li>
          <li>🎯 Caufield + Suzuki (proven)</li>
          <li>💎 Hutson (breakout rookie D)</li>
          <li>📰 Dobson rumor (trade boost)</li>
        </ul>
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
            '<span class="text-blue-400">ROI: -- | Balance: ${{ "%.2f"|format(maestro.bankroll) }}</span>';
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
      button.textContent = '🎼 L\\'orchestre + roster analysis...';
      button.disabled = true;
      
      axios.get(`/api/predict/${date}/${game_id}/${team}`)
        .then(res => {
          const pred = res.data;
          const isGoodBet = pred.ev > 0.05;
          const cardClass = isGoodBet ? 'pari-recommande' : pred.ev > 0 ? 'bg-yellow-600' : 'bg-red-600';
          
          let rosterHtml = '';
          if (pred.roster_info && pred.roster_info.score) {
            rosterHtml = `
              <div class="mt-4 p-3 bg-gray-700 rounded">
                <h5 class="font-bold text-blue-300">🏒 Analyse Roster:</h5>
                <p>📊 Score équipe: ${pred.roster_info.score}/100 ${pred.roster_info.tier}</p>
                <p>⭐ Stars: ${pred.roster_info.key_players.join(', ')}</p>
                <p>🚀 Boost roster: ${pred.roster_info.boost_pct > 0 ? '+' : ''}${pred.roster_info.boost_pct}%</p>
                ${pred.roster_info.rumors.length > 0 ? `<p>📰 Hype: ${pred.roster_info.rumors.join(', ')}</p>` : ''}
              </div>
            `;
          }
          
          document.getElementById('prediction-result').innerHTML = `
            <div class="${cardClass} rounded-lg p-6 text-white shadow-2xl">
              <h3 class="text-2xl font-bold mb-4">${pred.team} - ${pred.date}</h3>
              
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <p class="text-lg">🎯 Probabilité: <span class="font-bold">${(pred.probability * 100).toFixed(1)}%</span></p>
                  <p>💰 Cote: ${pred.odds}</p>
                  <p>📈 EV: <span class="font-bold ${pred.ev > 0 ? 'text-green-300' : 'text-red-300'}">${pred.ev_pct}%</span></p>
                  <p>💵 Mise suggérée: <span class="font-bold">$${pred.bet_amount}</span></p>
                </div>
                <div class="text-right">
                  <p class="text-3xl font-bold mb-2">${pred.recommendation}</p>
                  <p class="text-sm">Confiance: ${(pred.confidence * 100).toFixed(0)}%</p>
                </div>
              </div>
              
              ${rosterHtml}
              
              <div class="mt-6 text-center">
                <button onclick="addResult('${pred.game_id}', 1)" 
                        class="bg-green-500 hover:bg-green-600 px-4 py-2 rounded mr-4">✅ Gagné</button>
                <button onclick="addResult('${pred.game_id}', 0)" 
                        class="bg-red-500 hover:bg-red-600 px-4 py-2 rounded">❌ Perdu</button>
              </div>
            </div>
          `;
        })
        .catch(err => {
          document.getElementById('prediction-result').innerHTML = 
            '<div class="bg-red-600 rounded-lg p-4 text-white">❌ Erreur: ' + err.message + '</div>';
        })
        .finally(() => {
          button.textContent = '🎼 MAESTRO, PARI OU PAS ?';
          button.disabled = false;
        });
    }

    function addResult(game_id, result) {
      axios.get(`/api/result/${game_id}/${result}`)
        .then(() => {
          alert(result ? '🎉 Victoire enregistrée!' : '😔 Défaite enregistrée');
          updateStats();
        });
    }

    // Initial load
    updateStats();
  </script>
</body>
</html>
    ''', maestro=maestro)

@app.route('/api/predict/<date>/<game_id>/<team>')
def predict(date, game_id, team):
    """🔮 API de prédiction avec roster analysis"""
    try:
        prediction = maestro.predict_game_with_roster(date, game_id, team)
        maestro.save_bet(prediction)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/result/<game_id>/<int:result>')
def update_result(game_id, result):
    """📊 Enregistre le résultat d'un pari"""
    conn = sqlite3.connect(maestro.db_path)
    conn.execute("UPDATE bets SET result = ? WHERE game_id = ?", (result, game_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/roi')
def get_roi():
    """💰 Retourne les stats ROI"""
    return jsonify(maestro.get_roi())

@app.route('/api/status')
def status():
    """📊 Status de l'orchestre"""
    return jsonify({
        "maestro_version": "2.0_roster_analyzer",
        "quartet_loaded": maestro.using_quartet,
        "roster_analyzer": ROSTER_ANALYZER_AVAILABLE,
        "bankroll": maestro.bankroll,
        "odds_api": "active"
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎼 MAESTRO NHL + ROSTER ANALYZER LAUNCHED")
    print("="*60)
    print("🤖 Orchestre IA: Grok + Gemini + ChatGPT + Copilot")
    print("🏒 Roster Analysis: Joueur par joueur pondération")
    print("💰 The Odds API:", ODDS_API_KEY[:10] + "...")
    print("🎯 Question simple: PARI OU PAS ?")
    print("💎 Focus MTL: Demidov/Hutson hype + Dobson rumors")
    print(f"💳 Bankroll: ${maestro.bankroll}")
    print("🌐 Interface: http://localhost:5004")
    print("="*60)
    if REAL_DATA_BRIDGE_AVAILABLE:
        print("🎵 Comme dit Grok: 'Maintenant avec 1,358 joueurs NHL RÉELS!' 😂")
    else:
        print("🎵 Comme dit Grok: 'Mode simulation pour le moment!' 😂")
    print()
    
    app.run(host='0.0.0.0', port=5004, debug=True)
