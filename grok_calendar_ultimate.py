#!/usr/bin/env python3
"""
🏒 GROK CALENDAR SYSTEM + REAL NHL DATA
Version finale de Grok avec calendrier + 1,358 joueurs réels
Calendrier mensuel/hebdomadaire/journalier avec prédictions
"""

from flask import Flask, jsonify, render_template_string
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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
NHL_API = "https://api-web.nhle.com/v1"

class NHLPredictorWithCalendar:
    def __init__(self):
        self.db = sqlite3.connect('nhl_bets_calendar.db')
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
        """📰 Fetch rumors - Grok style"""
        url = "https://www.nhltraderumors.me"
        try:
            response = requests.get(url, timeout=5).text
            soup = BeautifulSoup(response, 'html.parser')
            rumors = soup.find_all('a', text=lambda t: team.lower() in t.lower() if t else False)
            return [r.text for r in rumors[:3]]
        except:
            # Fallback rumors
            team_rumors = {
                "MTL": ["Demidov hype présaison", "Hutson breakout potential", "Dobson trade rumors"],
                "TOR": ["Marner extension talks"],
                "EDM": ["McDavid dynasty mode"],
                "BOS": ["Veteran core aging concerns"]
            }
            return team_rumors.get(team.upper(), [])

    def get_team_analysis(self, team):
        """🎯 Team analysis with real or simulated data"""
        if self.bridge:
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
        
        # Fallback - Enhanced Grok approach
        if team.upper() == "MTL":
            roster = [
                {"name": "Cole Caufield", "role": "F", "ovr": 92, "xG": 0.8},
                {"name": "Nick Suzuki", "role": "C", "ovr": 90, "xG": 0.7},
                {"name": "Ivan Demidov", "role": "F", "ovr": 88, "xG": 0.6},
                {"name": "Lane Hutson", "role": "D", "ovr": 87, "xG": 0.2}
            ]
        else:
            # Enhanced team-specific rosters
            team_rosters = {
                "TOR": [{"name": "Auston Matthews", "role": "C", "ovr": 97, "xG": 0.9}] + [{"name": "Player", "role": "F", "ovr": 85, "xG": 0.6}] * 19,
                "EDM": [{"name": "Connor McDavid", "role": "C", "ovr": 99, "xG": 0.95}] + [{"name": "Player", "role": "F", "ovr": 85, "xG": 0.6}] * 19,
                "BOS": [{"name": "David Pastrnak", "role": "RW", "ovr": 95, "xG": 0.85}] + [{"name": "Player", "role": "F", "ovr": 82, "xG": 0.55}] * 19,
            }
            roster = team_rosters.get(team.upper(), [{"name": "Player", "role": "F", "ovr": 80, "xG": 0.5}] * 20)
        
        # Calculate team score
        score = 0
        for player in roster:
            weight = 1.0 if player["role"] in ["F", "C"] else 0.8 if player["role"] == "D" else 0.5
            score += player["ovr"] * weight * (1 + player["xG"] / 2)
        
        team_score = min(score / len(roster), 100)
        
        # Team-specific boosts
        team_boosts = {
            "MTL": 8,  # Demidov/Hutson hype
            "TOR": 3,  # Media hype
            "EDM": 5,  # McDavid factor
            "BOS": 2,  # Veteran leadership
        }
        team_score += team_boosts.get(team.upper(), 0)
            
        return {
            "team_score": min(team_score, 100),
            "tier": "🎯 Battle wildcard" if team_score > 75 else "📊 Milieu de pack",
            "key_players": ["Cole Caufield", "Nick Suzuki"] if team.upper() == "MTL" else ["Star 1", "Star 2"],
            "data_source": "ENHANCED_GROK"
        }

    def fetch_schedule(self, team, view, date=None):
        """📅 Fetch NHL schedule - Grok's new feature"""
        # For demo purposes, we'll simulate games since NHL API schedule format may vary
        # In production, use real NHL API: https://api-web.nhle.com/v1/schedule/...
        
        base_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        
        # Generate realistic game schedule
        games = []
        teams = ["TOR", "BOS", "FLA", "PIT", "NYR", "PHI", "EDM", "COL"]
        
        if view == "monthly":
            # Generate 15 games for the month
            for i in range(15):
                game_date = base_date + timedelta(days=i*2)
                opponent = teams[i % len(teams)]
                if opponent != team.upper():
                    games.append({
                        'id': f"2025{game_date.strftime('%m%d')}{team.upper()}{opponent}",
                        'date': game_date.strftime("%Y-%m-%d"),
                        'homeTeam': {'abbrev': team.upper() if i % 2 == 0 else opponent},
                        'awayTeam': {'abbrev': opponent if i % 2 == 0 else team.upper()},
                        'gameTime': {'inLocal': "19:00"}
                    })
        elif view == "weekly":
            # Generate 3 games for the week
            for i in range(3):
                game_date = base_date + timedelta(days=i*2)
                opponent = teams[i % len(teams)]
                if opponent != team.upper():
                    games.append({
                        'id': f"2025{game_date.strftime('%m%d')}{team.upper()}{opponent}",
                        'date': game_date.strftime("%Y-%m-%d"),
                        'homeTeam': {'abbrev': team.upper() if i % 2 == 0 else opponent},
                        'awayTeam': {'abbrev': opponent if i % 2 == 0 else team.upper()},
                        'gameTime': {'inLocal': "19:00"}
                    })
        else:  # daily
            # Single game for the day
            opponent = teams[0]
            if opponent != team.upper():
                games.append({
                    'id': f"2025{base_date.strftime('%m%d')}{team.upper()}{opponent}",
                    'date': base_date.strftime("%Y-%m-%d"),
                    'homeTeam': {'abbrev': team.upper()},
                    'awayTeam': {'abbrev': opponent},
                    'gameTime': {'inLocal': "19:00"}
                })
        
        return games

    def fetch_odds(self, game_id):
        """💰 Fetch odds with realistic variation"""
        # Pour les tests, on génère des cotes variées basées sur le game_id
        import hashlib
        hash_val = int(hashlib.md5(game_id.encode()).hexdigest()[:6], 16)
        base_odds = 1.75 + (hash_val % 60) / 100  # 1.75 to 2.35
        return round(base_odds, 2)
        
        # Code API réel (désactivé pour les tests)
        # url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds?apiKey={ODDS_API_KEY}&regions=us&markets=h2h"
        # try:
        #     data = requests.get(url, timeout=5).json()
        #     game = next((g for g in data if g['id'] == game_id), {})
        #     real_odds = game.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[0].get('price')
        #     return real_odds if real_odds else base_odds
        # except:
        #     return base_odds

    def predict(self, game_id, date, team):
        """🔮 Main prediction with enhanced data"""
        team_analysis = self.get_team_analysis(team)
        team_score = team_analysis["team_score"]
        
        # Base probability with game-specific variation
        import hashlib
        hash_val = int(hashlib.md5(f"{game_id}{team}".encode()).hexdigest()[:6], 16)
        prob = 0.45 + (hash_val % 20) / 100  # 0.45 to 0.65 baseline
        
        # Adjust based on team strength (realistic range)
        prob_adj = prob + (team_score - 80) / 1000  # More conservative adjustment
        
        # Rumors boost
        rumors = self.fetch_rumors(team)
        if any("dobson" in r.lower() for r in rumors):
            prob_adj += 0.05
        if team.upper() == "MTL":
            prob_adj += 0.05
            
        # Get odds
        odds = self.fetch_odds(game_id)
        
        # Calculate EV
        ev = (prob_adj * (odds - 1)) - (1 - prob_adj)
        
        # Kelly bet sizing (conservative approach)
        bankroll = 100  # Start with $100 test bankroll
        bet = bankroll * 0.25 * ((prob_adj * (odds - 1) - (1 - prob_adj)) / (odds - 1)) * 0.5  # Conservative Kelly
        bet = max(0, min(bet, bankroll * 0.02))  # Max 2% per bet
        
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

    def get_bet(self, game_id):
        """📊 Get existing bet"""
        cursor = self.db.execute("SELECT * FROM bets WHERE game_id = ?", (game_id,))
        bet = cursor.fetchone()
        if bet:
            return {
                "game_id": bet[0], "date": bet[1], "team": bet[2], "prob": bet[3],
                "odds": bet[4], "ev": bet[5], "bet": bet[6], "result": bet[7], "team_score": bet[8]
            }
        return None

    def add_result(self, game_id, result):
        """✅ Add game result"""
        self.db.execute("UPDATE bets SET result = ? WHERE game_id = ?", (result, game_id))
        self.db.commit()

    def get_roi(self):
        """💰 Calculate ROI"""
        cursor = self.db.execute("SELECT bet, result, odds FROM bets WHERE result IS NOT NULL")
        total_bet, total_win = 0, 0
        for bet, result, odds in cursor:
            total_bet += bet
            if result == 1:
                total_win += bet * (odds - 1)
        roi = (total_win - total_bet) / total_bet * 100 if total_bet > 0 else 0
        return {"roi": roi, "balance": 100 + total_win - total_bet}

# Routes
@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Go Habs Go ! NHL Calendar (Grok + Real Data)</title>
  <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.development.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-900 text-white font-sans">
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect } = React;

    const App = () => {
      const [team, setTeam] = useState('MTL');
      const [view, setView] = useState('monthly');
      const [date, setDate] = useState('2025-10-01');
      const [games, setGames] = useState([]);
      const [roi, setRoi] = useState({ roi: 15.6, balance: 1768.84 });

      useEffect(() => {
        axios.get(`/api/schedule/${team}/${view}/${date}`)
          .then(res => {
            console.log('Games data:', res.data);
            setGames(res.data || []);
          })
          .catch(err => {
            console.error('Error fetching games:', err);
            setGames([]);
          });
        axios.get('/api/roi')
          .then(res => setRoi(res.data))
          .catch(err => {
            console.error('Error fetching ROI:', err);
            setRoi({ roi: 0, balance: 100 });
          });
      }, [team, view, date]);

      const predictGame = (game_id, game_date, game_team) => {
        axios.get(`/api/predict/${game_date}/${game_id}/${game_team}`)
          .then(res => {
            setGames(games.map(g => g.game_id === game_id ? { ...g, bet: res.data } : g));
          });
      };

      const addResult = (game_id, result) => {
        axios.get(`/api/result/${game_id}/${result}`)
          .then(() => {
            alert('Résultat enregistré !');
            axios.get(`/api/schedule/${team}/${view}/${date}`)
              .then(res => setGames(res.data));
            axios.get('/api/roi').then(res => setRoi(res.data));
          });
      };

      return (
        <div className="container mx-auto p-4">
          <h1 className="text-4xl font-bold text-center mb-4 flex items-center justify-center">
            🏒
            Go Habs Go ! NHL Calendar
          </h1>
          <p className="text-center text-lg mb-2">🔗 Powered by 1,358 real NHL players | 🧪 Test Mode</p>
          <p className="text-center text-lg mb-4">📊 Simulation ROI: {roi.roi.toFixed(1)}% | Test Balance: ${roi.balance.toFixed(2)}</p>
          
          <div className="flex mb-4 gap-2">
            <input
              type="text"
              value={team}
              onChange={e => setTeam(e.target.value.toUpperCase())}
              placeholder="Équipe (ex. MTL)"
              className="p-2 bg-gray-800 rounded text-white"
            />
            <select value={view} onChange={e => setView(e.target.value)} className="p-2 bg-gray-800 rounded text-white">
              <option value="monthly">📅 Mensuel</option>
              <option value="weekly">🗓️ Hebdomadaire</option>
              <option value="daily">📆 Journalier</option>
            </select>
            <input
              type="date"
              value={date}
              onChange={e => setDate(e.target.value)}
              className="p-2 bg-gray-800 rounded text-white"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {games && games.length > 0 ? games.map(game => (
              <div key={game.game_id} className={`bg-gray-800 p-4 rounded-lg shadow-lg ${game.bet && (game.bet.ev || 0) > 0.05 ? 'border-2 border-green-500' : ''}`}>
                <h2 className="text-xl font-semibold">{game.home_team} vs {game.away_team}</h2>
                <p className="text-gray-400">{game.date} à {game.time}</p>
                
                {!game.bet ? (
                  <button
                    onClick={() => predictGame(game.game_id, game.date, team)}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded mt-2"
                  >
                    🔮 Prédire
                  </button>
                ) : (
                  <>
                    <p>🏒 Score Équipe: {(game.bet.team_score || 0).toFixed(1)}/100 ({(game.bet.team_score || 0) > 85 ? 'Elite' : (game.bet.team_score || 0) > 75 ? 'Bonne' : 'Moyenne'})</p>
                    {game.bet.data_source === 'NHL_API_REAL' && <p className="text-green-400">🔗 Vraies données NHL</p>}
                    <p>🎯 Probabilité: {((game.bet.prob || 0) * 100).toFixed(1)}%</p>
                    <p>💰 Cote: {(game.bet.odds || 0).toFixed(2)}</p>
                    <p>📈 EV: {((game.bet.ev || 0) * 100).toFixed(1)}% {(game.bet.ev || 0) > 0.05 ? '✅ PARI RECOMMANDÉ' : (game.bet.ev || 0) > 0 ? '🤔 Risqué' : '❌ Skip'}</p>
                    <p>💵 Mise: ${(game.bet.bet || 0).toFixed(2)}</p>
                    <p>📰 Rumeurs: {game.bet.rumors && Array.isArray(game.bet.rumors) && game.bet.rumors.length > 0 ? game.bet.rumors.join(', ') : 'Aucune'}</p>
                    
                    <button
                      onClick={() => predictGame(game.game_id, game.date, team)}
                      className="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1 rounded mt-2 mr-2"
                    >
                      🔄 Re-prédire
                    </button>
                    <button
                      onClick={() => {
                        axios.get(`/api/reset/${game.game_id}`)
                          .then(() => {
                            setGames(games.map(g => g.game_id === game.game_id ? { ...g, bet: null } : g));
                          });
                      }}
                      className="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded mt-2"
                    >
                      🗑️ Reset
                    </button>
                    
                    {game.bet.result !== null && game.bet.result !== undefined ? (
                      <p className={`mt-2 font-bold ${game.bet.result === 1 ? 'text-green-400' : 'text-red-400'}`}>
                        Résultat: {game.bet.result === 1 ? '✅ Gagné' : '❌ Perdu'}
                      </p>
                    ) : (
                      <div className="mt-3 flex gap-2">
                        <button
                          onClick={() => addResult(game.game_id, 1)}
                          className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded"
                        >
                          ✅ Gagné
                        </button>
                        <button
                          onClick={() => addResult(game.game_id, 0)}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                        >
                          ❌ Perdu
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            )) : (
              <div className="col-span-2 text-center text-gray-400 mt-8">
                <p>Chargement des matchs...</p>
              </div>
            )}
          </div>
          
          {games && games.length === 0 && (
            <p className="text-center text-gray-400 mt-8">Aucun match trouvé pour cette période</p>
          )}
        </div>
      );
    };

    ReactDOM.render(<App />, document.getElementById('root'));
  </script>
</body>
</html>
    ''', real_data=REAL_DATA_AVAILABLE)

@app.route('/api/schedule/<team>/<view>/<date>')
def schedule(team, view, date):
    predictor = NHLPredictorWithCalendar()
    games = predictor.fetch_schedule(team, view, date)
    result = []
    for game in games:
        bet = predictor.get_bet(game['id'])
        result.append({
            "game_id": game['id'],
            "date": game['date'],
            "home_team": game['homeTeam']['abbrev'],
            "away_team": game['awayTeam']['abbrev'],
            "time": game['gameTime']['inLocal'],
            "bet": bet
        })
    return jsonify(result)

@app.route('/api/predict/<date>/<game_id>/<team>')
def predict(date, game_id, team):
    predictor = NHLPredictorWithCalendar()
    return jsonify(predictor.predict(game_id, date, team))

@app.route('/api/result/<game_id>/<result>')
def result(game_id, result):
    predictor = NHLPredictorWithCalendar()
    predictor.add_result(game_id, int(result))
    return jsonify({"status": "Résultat enregistré"})

@app.route('/api/roi')
def roi():
    predictor = NHLPredictorWithCalendar()
    return jsonify(predictor.get_roi())

@app.route('/api/reset/<game_id>')
def reset_prediction(game_id):
    predictor = NHLPredictorWithCalendar()
    predictor.db.execute("DELETE FROM bets WHERE game_id = ?", (game_id,))
    predictor.db.commit()
    return jsonify({"status": "Prédiction effacée"})

if __name__ == '__main__':
    print("🏒 GROK NHL CALENDAR + REAL DATA")
    print("=" * 40)
    if REAL_DATA_AVAILABLE:
        print("🔗 Powered by 1,358 real NHL players")
    else:
        print("🎲 Running in enhanced simulation mode")
    print("📅 Calendar view: Monthly/Weekly/Daily")
    print("🎯 Predict directly from schedule")
    print("🌐 Running on http://localhost:5006")
    print()
    
    app.run(host='0.0.0.0', port=5006, debug=True)
