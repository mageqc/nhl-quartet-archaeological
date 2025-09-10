#!/usr/bin/env python3
"""
🎼 GROK STYLE + REAL NHL DATA - Version Simplifiée
Version inspirée de Grok mais avec les 1,358 joueurs réels
"Simple is better" avec vraies données NHL
"""

from flask import Flask, jsonify, render_template_string
import sqlite3
import requests
from bs4 import BeautifulSoup
import sys
import os

# Import du bridge pour vraies données
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026/active')
try:
    from nhl_maestro_bridge import NHLMaestroBridge
    REAL_DATA_AVAILABLE = True
    print("🔗 Real NHL Data Bridge loaded - 1,358 joueurs!")
except ImportError:
    REAL_DATA_AVAILABLE = False
    print("⚠️ Using simulated data")

app = Flask(__name__)
ODDS_API_KEY = "63987f9611c51772932666988d722a3d"

class NHLPredictorGrokStyle:
    def __init__(self):
        self.db = sqlite3.connect('nhl_bets_grok.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS bets
                         (game_id TEXT, date TEXT, team TEXT, prob REAL, odds REAL, 
                          ev REAL, bet REAL, result INTEGER, team_score REAL)''')
        self.db.commit()
        
        # Initialize real data bridge
        if REAL_DATA_AVAILABLE:
            self.bridge = NHLMaestroBridge()
        else:
            self.bridge = None

    def fetch_rumors(self, team):
        """📰 Fetch rumors - Grok style simple"""
        url = "https://www.nhltraderumors.me"
        try:
            response = requests.get(url, timeout=5).text
            soup = BeautifulSoup(response, 'html.parser')
            rumors = soup.find_all('a', text=lambda t: team.lower() in t.lower() if t else False)
            return [r.text for r in rumors[:3]]  # Max 3 rumors
        except:
            # Fallback rumors for popular teams
            team_rumors = {
                "MTL": ["Demidov hype présaison", "Hutson breakout potential"],
                "TOR": ["Marner extension talks"],
                "EDM": ["McDavid dynasty mode"]
            }
            return team_rumors.get(team.upper(), [])

    def get_team_analysis(self, team):
        """🎯 Team analysis - Real data if available, fallback if not"""
        if self.bridge:
            # Use REAL NHL data
            try:
                analysis = self.bridge.get_real_team_analysis(team)
                return {
                    "team_score": analysis["roster_score"],
                    "tier": analysis["tier_description"],
                    "key_players": analysis["key_players"][:2],
                    "data_source": "NHL_API_REAL"
                }
            except:
                pass
        
        # Fallback - Grok's original approach but improved
        if team.upper() == "MTL":
            roster = [
                {"name": "Cole Caufield", "role": "F", "ovr": 92, "xG": 0.8},
                {"name": "Nick Suzuki", "role": "C", "ovr": 90, "xG": 0.7},
                {"name": "Ivan Demidov", "role": "F", "ovr": 88, "xG": 0.6},  # Hype
                {"name": "Lane Hutson", "role": "D", "ovr": 87, "xG": 0.2}   # Hype
            ]
        else:
            # Generic roster for other teams
            roster = [{"name": "Player", "role": "F", "ovr": 80, "xG": 0.5}] * 20
        
        # Calculate team score - Grok's formula
        score = 0
        for player in roster:
            weight = 1.0 if player["role"] in ["F", "C"] else 0.8 if player["role"] == "D" else 0.5
            score += player["ovr"] * weight * (1 + player["xG"] / 2)
        
        team_score = min(score / len(roster), 100)
        
        # Boost for MTL (Grok style)
        if team.upper() == "MTL":
            team_score += 5  # Demidov/Hutson hype
            
        return {
            "team_score": min(team_score, 100),
            "tier": "🎯 Battle wildcard" if team_score > 75 else "📊 Milieu de pack",
            "key_players": ["Cole Caufield", "Nick Suzuki"] if team.upper() == "MTL" else ["Star 1", "Star 2"],
            "data_source": "SIMULATED_GROK"
        }

    def fetch_odds(self, game_id):
        """💰 Fetch odds - Grok's approach"""
        url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds?apiKey={ODDS_API_KEY}&regions=us&markets=h2h"
        try:
            data = requests.get(url, timeout=5).json()
            game = next((g for g in data if g['id'] == game_id), {})
            return game.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[0].get('price', 1.91)
        except:
            return 1.91  # Grok's fallback

    def predict(self, game_id, date, team):
        """🔮 Main prediction - Grok style with real data enhancement"""
        
        # Get team analysis (real or simulated)
        team_analysis = self.get_team_analysis(team)
        team_score = team_analysis["team_score"]
        
        # Base probability - Grok's approach
        prob = 0.59  # Base prob
        
        # Adjust probability based on team strength - Grok's formula
        prob_adj = prob + (team_score - 80) / 500  # +5% if score 90
        
        # Get rumors and apply boosts - Grok style
        rumors = self.fetch_rumors(team)
        if any("dobson" in r.lower() for r in rumors):
            prob_adj += 0.05  # Dobson trade boost
        if team.upper() == "MTL":
            prob_adj += 0.05  # MTL hype boost
            
        # Get odds
        odds = self.fetch_odds(game_id)
        
        # Calculate EV - Grok's formula
        ev = (prob_adj * (odds - 1)) - (1 - prob_adj)
        
        # Kelly Criterion bet sizing - Grok's approach
        bankroll = 1768.84
        bet = bankroll * 0.5 * ((prob_adj * (odds - 1) - (1 - prob_adj)) / (odds - 1)) * 0.8
        bet = max(0, min(bet, bankroll * 0.03))  # Max 3%
        
        # Save to database
        self.db.execute("INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (game_id, date, team, prob_adj, odds, ev, bet, None, team_score))
        self.db.commit()
        
        return {
            "game_id": game_id, 
            "date": date, 
            "team": team, 
            "prob": prob_adj, 
            "odds": odds, 
            "ev": ev, 
            "bet": bet, 
            "rumors": rumors, 
            "team_score": team_score,
            "key_players": team_analysis["key_players"],
            "data_source": team_analysis["data_source"]
        }

    def add_result(self, game_id, result):
        """📊 Add result - Grok style"""
        self.db.execute("UPDATE bets SET result = ? WHERE game_id = ?", (result, game_id))
        self.db.commit()

    def get_roi(self):
        """💰 Calculate ROI - Grok's formula"""
        cursor = self.db.execute("SELECT bet, result, odds FROM bets WHERE result IS NOT NULL")
        total_bet, total_win = 0, 0
        for bet, result, odds in cursor:
            total_bet += bet
            if result == 1:
                total_win += bet * (odds - 1)
        roi = (total_win - total_bet) / total_bet * 100 if total_bet > 0 else 0
        return {"roi": roi, "balance": 1768.84 + total_win - total_bet}

# Grok's simple routes
@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Go Habs Go ! NHL Betting App (Grok Style + Real Data)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body class="bg-gray-900 text-white font-sans">
  <div class="container mx-auto p-4">
    <h1 class="text-4xl font-bold text-center mb-4 flex items-center justify-center">
      <img src="https://www-league.nhlstatic.com/nhl.com/builds/site-core/d5e66e4bf277b8a8f8e8b157c9e4a496e6c8c753_0/images/logos/team/current/team-10-dark.svg" alt="MTL Logo" class="w-12 h-12 mr-2" />
      Go Habs Go ! (Grok + Real Data)
    </h1>
    <div class="text-center mb-4">
      <p class="text-lg text-blue-400">🎼 Grok's simple approach + {{ "1,358 joueurs NHL réels" if real_data else "données simulées" }}</p>
      <div id="stats" class="text-lg mt-2"></div>
    </div>
    
    <input id="date" type="date" value="2025-09-22" class="mb-4 p-2 bg-gray-800 rounded text-white w-full" />
    <input id="game_id" type="text" placeholder="Game ID (ex. 2025020001)" class="mb-4 p-2 bg-gray-800 rounded text-white w-full" />
    <input id="team" type="text" placeholder="Équipe (ex. MTL)" class="mb-4 p-2 bg-gray-800 rounded text-white w-full" />
    <button onclick="getPrediction()" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded w-full">Voir Prédiction (Style Grok)</button>
    <div id="predictions" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4"></div>
  </div>
  
  <script>
    function updateStats() {
      axios.get('/api/roi')
        .then(res => {
          document.getElementById('stats').innerHTML = `ROI: ${res.data.roi.toFixed(1)}% | Balance: $${res.data.balance.toFixed(2)}`;
        });
    }

    function getPrediction() {
      const date = document.getElementById('date').value;
      const game_id = document.getElementById('game_id').value;
      const team = document.getElementById('team').value;
      
      axios.get(`/api/predict/${date}/${game_id}/${team}`)
        .then(res => {
          const pred = res.data;
          const rumors = pred.rumors.length > 0 ? pred.rumors.join(', ') : 'Aucune rumeur';
          const perf = pred.team_score > 85 ? 'Bonne (playoffs !)' : pred.team_score > 75 ? 'Moyenne' : 'Mauvaise';
          const dataSource = pred.data_source === 'NHL_API_REAL' ? '🔗 Vraies données NHL' : '🎲 Simulé';
          
          const card = `
            <div class="bg-gray-800 p-4 rounded-lg shadow-lg ${pred.ev > 0.05 ? 'border-2 border-green-500' : ''}">
              <h2 class="text-xl font-semibold">${pred.team} vs Adversaire (${pred.date})</h2>
              <p>Score Équipe: ${pred.team_score.toFixed(1)}/100 (${perf}) ${dataSource}</p>
              <p>⭐ Stars: ${pred.key_players.join(', ')}</p>
              <p>Probabilité Victoire: ${(pred.prob * 100).toFixed(1)}%</p>
              <p>Cote: ${pred.odds.toFixed(2)} (The Odds API)</p>
              <p>EV: ${(pred.ev * 100).toFixed(1)}% ${pred.ev > 0.05 ? '✅ Pari recommandé !' : ''}</p>
              <p>Mise Suggérée: $${pred.bet.toFixed(2)}</p>
              <p>Rumeurs: ${rumors}</p>
              <button onclick="addResult('${pred.game_id}', 1)" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded mr-2 mt-2">Gagné</button>
              <button onclick="addResult('${pred.game_id}', 0)" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded mt-2">Perdu</button>
            </div>`;
          document.getElementById('predictions').innerHTML = card;
          updateStats();
        });
    }

    function addResult(game_id, result) {
      axios.get(`/api/result/${game_id}/${result}`)
        .then(() => {
          alert('Résultat enregistré !');
          updateStats();
        });
    }

    updateStats();
  </script>
</body>
</html>
    ''', real_data=REAL_DATA_AVAILABLE)

@app.route('/api/predict/<date>/<game_id>/<team>')
def predict(date, game_id, team):
    predictor = NHLPredictorGrokStyle()
    return jsonify(predictor.predict(game_id, date, team))

@app.route('/api/result/<game_id>/<result>')
def result(game_id, result):
    predictor = NHLPredictorGrokStyle()
    predictor.add_result(game_id, int(result))
    return jsonify({"status": "Résultat enregistré"})

@app.route('/api/roi')
def roi():
    predictor = NHLPredictorGrokStyle()
    return jsonify(predictor.get_roi())

if __name__ == '__main__':
    print("🎼 GROK STYLE NHL PREDICTOR")
    print("=" * 40)
    if REAL_DATA_AVAILABLE:
        print("🔗 Powered by 1,358 real NHL players")
    else:
        print("🎲 Running in simulation mode")
    print("🏒 Simple is better - Grok's philosophy")
    print("🌐 Running on http://localhost:5005")
    print()
    
    app.run(host='0.0.0.0', port=5005, debug=True)
