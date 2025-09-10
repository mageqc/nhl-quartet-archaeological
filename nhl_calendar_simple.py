#!/usr/bin/env python3
"""
🏒 NHL Quartet Archaeological - Calendar Grok Ultimate 
Version simplifiée et fonctionnelle pour démonstration
"""

from flask import Flask, jsonify, render_template_string
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

# HTML simplifié mais fonctionnel
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🏒 Go Habs Go! NHL Calendar</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .game-card { transition: all 0.3s ease; }
    .game-card:hover { transform: translateY(-2px); }
    .recommended { border-left: 4px solid #10B981; }
    .skip { border-left: 4px solid #EF4444; }
  </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">
  <div class="container mx-auto p-4 max-w-6xl">
    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold mb-2 flex items-center justify-center">
        <span class="text-red-500 mr-2">🏒</span>
        Go Habs Go! NHL Calendar
      </h1>
      <p class="text-gray-300">NHL Quartet Archaeological - Simulation zéro risque</p>
      <div id="roi-display" class="text-lg mt-2">
        <span class="text-yellow-400">ROI: 0.0%</span> | 
        <span class="text-green-400">Balance: $100.00</span>
      </div>
    </div>

    <!-- Controls -->
    <div class="bg-gray-800 p-4 rounded-lg mb-6">
      <div class="flex flex-wrap gap-4 justify-center">
        <div>
          <label class="block text-sm mb-1">Équipe:</label>
          <input type="text" id="team-input" value="MTL" 
                 class="p-2 bg-gray-700 rounded text-white w-20 text-center" 
                 placeholder="MTL">
        </div>
        <div>
          <label class="block text-sm mb-1">Vue:</label>
          <select id="view-select" class="p-2 bg-gray-700 rounded text-white">
            <option value="monthly">Mensuel</option>
            <option value="weekly">Hebdomadaire</option>
            <option value="daily">Journalier</option>
          </select>
        </div>
        <div>
          <label class="block text-sm mb-1">Date:</label>
          <input type="date" id="date-input" value="2025-10-01" 
                 class="p-2 bg-gray-700 rounded text-white">
        </div>
        <div class="flex items-end">
          <button onclick="loadSchedule()" 
                  class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
            🔄 Actualiser
          </button>
        </div>
      </div>
    </div>

    <!-- Games Container -->
    <div id="games-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="text-center text-gray-400">
        Cliquez sur "🔄 Actualiser" pour charger le calendrier...
      </div>
    </div>

    <!-- Footer -->
    <div class="text-center mt-8 text-gray-500">
      <p>🎯 Données: NHL API simulé + The Odds API + Rumeurs</p>
      <p>⚠️ Simulation uniquement - Pariez responsable</p>
    </div>
  </div>

  <script>
    let currentGames = [];

    // Charger le calendrier
    async function loadSchedule() {
      const team = document.getElementById('team-input').value.toUpperCase();
      const view = document.getElementById('view-select').value;
      const date = document.getElementById('date-input').value;
      
      try {
        const response = await fetch(`/api/schedule/${team}/${view}/${date}`);
        const games = await response.json();
        currentGames = games;
        displayGames(games);
        updateROI();
      } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('games-container').innerHTML = 
          '<div class="text-red-400 text-center">Erreur lors du chargement des matchs</div>';
      }
    }

    // Afficher les matchs
    function displayGames(games) {
      const container = document.getElementById('games-container');
      
      if (games.length === 0) {
        container.innerHTML = '<div class="text-center text-gray-400">Aucun match trouvé pour cette période</div>';
        return;
      }

      container.innerHTML = games.map(game => {
        const bet = game.bet;
        const isRecommended = bet && bet.ev > 0.05;
        const cardClass = bet ? (isRecommended ? 'recommended' : 'skip') : '';
        
        return `
          <div class="game-card bg-gray-800 p-4 rounded-lg shadow-lg ${cardClass}">
            <div class="mb-3">
              <h3 class="text-xl font-semibold">${game.home_team} vs ${game.away_team}</h3>
              <p class="text-gray-300">${game.date} à ${game.time}</p>
            </div>
            
            ${!bet ? `
              <button onclick="predictGame('${game.game_id}', '${game.date}', '${document.getElementById('team-input').value}')"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                🔮 Prédire
              </button>
            ` : `
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span>Score Équipe:</span>
                  <span class="font-semibold">${bet.team_score.toFixed(1)}/100</span>
                </div>
                <div class="flex justify-between">
                  <span>Probabilité:</span>
                  <span class="font-semibold">${(bet.prob * 100).toFixed(1)}%</span>
                </div>
                <div class="flex justify-between">
                  <span>Cote:</span>
                  <span class="font-semibold">${bet.odds.toFixed(2)}</span>
                </div>
                <div class="flex justify-between">
                  <span>EV:</span>
                  <span class="font-semibold ${bet.ev > 0.05 ? 'text-green-400' : 'text-red-400'}">
                    ${(bet.ev * 100).toFixed(1)}%
                  </span>
                </div>
                <div class="flex justify-between">
                  <span>Mise:</span>
                  <span class="font-semibold">$${bet.bet.toFixed(2)}</span>
                </div>
                
                ${bet.ev > 0.05 ? 
                  '<div class="bg-green-600 text-center py-1 px-2 rounded text-sm">✅ PARI RECOMMANDÉ!</div>' :
                  '<div class="bg-red-600 text-center py-1 px-2 rounded text-sm">❌ Skip</div>'
                }
                
                ${bet.result !== null ? `
                  <div class="text-center py-2">
                    Résultat: ${bet.result === 1 ? '✅ Gagné' : '❌ Perdu'}
                  </div>
                ` : `
                  <div class="flex gap-2 mt-3">
                    <button onclick="addResult('${game.game_id}', 1)" 
                            class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm flex-1">
                      ✅ Gagné
                    </button>
                    <button onclick="addResult('${game.game_id}', 0)" 
                            class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm flex-1">
                      ❌ Perdu
                    </button>
                  </div>
                  <button onclick="resetGame('${game.game_id}')" 
                          class="w-full bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm mt-2">
                    🔄 Re-prédire
                  </button>
                `}
              </div>
            `}
          </div>
        `;
      }).join('');
    }

    // Prédire un match
    async function predictGame(gameId, date, team) {
      try {
        const response = await fetch(`/api/predict/${date}/${gameId}/${team}`);
        const prediction = await response.json();
        
        // Mettre à jour le match dans la liste
        const gameIndex = currentGames.findIndex(g => g.game_id === gameId);
        if (gameIndex >= 0) {
          currentGames[gameIndex].bet = prediction;
          displayGames(currentGames);
        }
      } catch (error) {
        console.error('Erreur prédiction:', error);
      }
    }

    // Ajouter un résultat
    async function addResult(gameId, result) {
      try {
        await fetch(`/api/result/${gameId}/${result}`);
        loadSchedule(); // Recharger pour voir le changement
      } catch (error) {
        console.error('Erreur résultat:', error);
      }
    }

    // Reset prédiction
    async function resetGame(gameId) {
      try {
        await fetch(`/api/reset/${gameId}`);
        loadSchedule(); // Recharger
      } catch (error) {
        console.error('Erreur reset:', error);
      }
    }

    // Mettre à jour le ROI
    async function updateROI() {
      try {
        const response = await fetch('/api/roi');
        const roi = await response.json();
        document.getElementById('roi-display').innerHTML = 
          `<span class="text-yellow-400">ROI: ${roi.roi.toFixed(1)}%</span> | 
           <span class="text-green-400">Balance: $${roi.balance.toFixed(2)}</span>`;
      } catch (error) {
        console.error('Erreur ROI:', error);
      }
    }

    // Auto-load au démarrage
    window.onload = () => {
      loadSchedule();
    };
  </script>
</body>
</html>
'''

class NHLCalendar:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialise la base de données"""
        self.conn = sqlite3.connect('nhl_calendar.db', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                game_id TEXT PRIMARY KEY,
                date TEXT,
                team TEXT,
                prob REAL,
                odds REAL,
                ev REAL,
                bet_amount REAL,
                result INTEGER,
                team_score REAL
            )
        ''')
        self.conn.commit()
    
    def get_fake_schedule(self, team, view, date):
        """Calendrier simulé pour démonstration"""
        mtl_games = [
            {"id": "2025020001", "date": "2025-10-08", "home": "TOR", "away": "MTL", "time": "19:00"},
            {"id": "2025020002", "date": "2025-10-09", "home": "DET", "away": "MTL", "time": "19:30"},
            {"id": "2025020003", "date": "2025-10-11", "home": "CHI", "away": "MTL", "time": "20:00"},
            {"id": "2025020004", "date": "2025-10-13", "home": "MTL", "away": "BOS", "time": "19:00"},
            {"id": "2025020005", "date": "2025-10-15", "home": "MTL", "away": "NYR", "time": "19:30"},
            {"id": "2025020006", "date": "2025-10-18", "home": "BUF", "away": "MTL", "time": "19:00"}
        ]
        
        # Filtrer selon la vue
        if view == "weekly":
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=6)
            mtl_games = [g for g in mtl_games 
                        if start_date <= datetime.strptime(g['date'], "%Y-%m-%d") <= end_date]
        elif view == "daily":
            mtl_games = [g for g in mtl_games if g['date'] == date]
        
        return mtl_games
    
    def generate_odds(self, game_id):
        """Génère des cotes variées basées sur l'ID"""
        hash_obj = hashlib.md5(game_id.encode())
        hash_int = int(hash_obj.hexdigest()[:8], 16)
        variation = (hash_int % 60) / 100  # 0.00 à 0.60
        return round(1.75 + variation, 2)  # Entre 1.75 et 2.35
    
    def calculate_team_strength(self, team):
        """Calcule la force de l'équipe"""
        strengths = {
            'MTL': 82,  # Go Habs Go!
            'TOR': 88,
            'BOS': 85,
            'DET': 78,
            'CHI': 75,
            'NYR': 83,
            'BUF': 76
        }
        return strengths.get(team, 80)
    
    def make_prediction(self, game_id, date, team):
        """Génère une prédiction pour un match"""
        # Vérifier si existe déjà
        cursor = self.conn.execute("SELECT * FROM predictions WHERE game_id = ?", (game_id,))
        existing = cursor.fetchone()
        if existing:
            return {
                'game_id': existing[0], 'date': existing[1], 'team': existing[2],
                'prob': existing[3], 'odds': existing[4], 'ev': existing[5],
                'bet': existing[6], 'result': existing[7], 'team_score': existing[8]
            }
        
        # Nouvelle prédiction
        team_score = self.calculate_team_strength(team)
        base_prob = 0.60
        prob = base_prob + (team_score - 80) / 500
        
        # Bonus MTL
        if team == 'MTL':
            prob += 0.05  # Go Habs Go!
        
        prob = max(0.1, min(prob, 0.9))  # Entre 10% et 90%
        
        odds = self.generate_odds(game_id)
        ev = (prob * (odds - 1)) - (1 - prob)
        
        # Kelly Criterion conservateur
        if ev > 0:
            kelly = ((prob * (odds - 1) - (1 - prob)) / (odds - 1)) * 0.25
            bet_amount = min(100 * kelly * 0.5, 2.0)  # Max $2
        else:
            bet_amount = 0.0
        
        # Sauvegarder
        self.conn.execute('''
            INSERT INTO predictions 
            (game_id, date, team, prob, odds, ev, bet_amount, result, team_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_id, date, team, prob, odds, ev, bet_amount, None, team_score))
        self.conn.commit()
        
        return {
            'game_id': game_id, 'date': date, 'team': team,
            'prob': prob, 'odds': odds, 'ev': ev,
            'bet': bet_amount, 'result': None, 'team_score': team_score
        }
    
    def get_prediction(self, game_id):
        """Récupère une prédiction existante"""
        cursor = self.conn.execute("SELECT * FROM predictions WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        if row:
            return {
                'game_id': row[0], 'date': row[1], 'team': row[2],
                'prob': row[3], 'odds': row[4], 'ev': row[5],
                'bet': row[6], 'result': row[7], 'team_score': row[8]
            }
        return None
    
    def add_result(self, game_id, result):
        """Ajoute le résultat d'un match"""
        self.conn.execute("UPDATE predictions SET result = ? WHERE game_id = ?", 
                         (result, game_id))
        self.conn.commit()
    
    def reset_prediction(self, game_id):
        """Supprime une prédiction"""
        self.conn.execute("DELETE FROM predictions WHERE game_id = ?", (game_id,))
        self.conn.commit()
    
    def get_roi(self):
        """Calcule le ROI actuel"""
        cursor = self.conn.execute('''
            SELECT bet_amount, result, odds 
            FROM predictions 
            WHERE result IS NOT NULL
        ''')
        
        total_bet = 0
        total_win = 0
        
        for bet, result, odds in cursor:
            total_bet += bet
            if result == 1:
                total_win += bet * odds
        
        if total_bet > 0:
            roi = ((total_win - total_bet) / total_bet) * 100
            balance = 100 + (total_win - total_bet)
        else:
            roi = 0.0
            balance = 100.0
        
        return {"roi": roi, "balance": balance}

# Instance globale
nhl = NHLCalendar()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/schedule/<team>/<view>/<date>')
def api_schedule(team, view, date):
    games = nhl.get_fake_schedule(team, view, date)
    result = []
    
    for game in games:
        prediction = nhl.get_prediction(game['id'])
        result.append({
            'game_id': game['id'],
            'date': game['date'],
            'home_team': game['home'],
            'away_team': game['away'],
            'time': game['time'],
            'bet': prediction
        })
    
    return jsonify(result)

@app.route('/api/predict/<date>/<game_id>/<team>')
def api_predict(date, game_id, team):
    prediction = nhl.make_prediction(game_id, date, team.upper())
    return jsonify(prediction)

@app.route('/api/result/<game_id>/<int:result>')
def api_result(game_id, result):
    nhl.add_result(game_id, result)
    return jsonify({"status": "OK"})

@app.route('/api/reset/<game_id>')
def api_reset(game_id):
    nhl.reset_prediction(game_id)
    return jsonify({"status": "Reset OK"})

@app.route('/api/roi')
def api_roi():
    return jsonify(nhl.get_roi())

if __name__ == '__main__':
    print("🏒 NHL Quartet Archaeological Calendar")
    print("🔗 Ouvrir: http://localhost:5007")
    print("🎯 Go Habs Go! - Simulation zéro risque")
    print("🚀 Système opérationnel!")
    app.run(host='0.0.0.0', port=5007, debug=False)
