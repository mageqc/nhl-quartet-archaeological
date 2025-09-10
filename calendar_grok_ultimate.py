from flask import Flask, jsonify, render_template_string
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
ODDS_API_KEY = "63987f9611c51772932666988d722a3d"
NHL_API = "https://api-web.nhle.com/v1"

# HTML Template intégré
CALENDAR_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Go Habs Go ! NHL Calendar</title>
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
      const [roi, setRoi] = useState({ roi: 0, balance: 100 });

      useEffect(() => {
        axios.get(`/api/schedule/${team}/${view}/${date}`)
          .then(res => setGames(res.data))
          .catch(err => console.error(err));
        axios.get('/api/roi')
          .then(res => setRoi(res.data))
          .catch(err => console.error(err));
      }, [team, view, date]);

      const predictGame = (game_id, game_date, game_team) => {
        axios.get(`/api/predict/${game_date}/${game_id}/${game_team}`)
          .then(res => {
            setGames(games.map(g => g.game_id === game_id ? { ...g, bet: res.data } : g));
          });
      };

      const resetGame = (game_id) => {
        axios.get(`/api/reset/${game_id}`)
          .then(() => {
            setGames(games.map(g => g.game_id === game_id ? { ...g, bet: null } : g));
            alert('Prédiction réinitialisée !');
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
            <span className="text-red-500 mr-2">🏒</span>
            Go Habs Go ! NHL Calendar
          </h1>
          <p className="text-center text-lg mb-4">ROI: {roi.roi.toFixed(1)}% | Balance: ${roi.balance.toFixed(2)}</p>
          <div className="flex flex-wrap justify-center mb-4 gap-2">
            <input
              type="text"
              value={team}
              onChange={e => setTeam(e.target.value.toUpperCase())}
              placeholder="Équipe (ex. MTL)"
              className="p-2 bg-gray-800 rounded text-white"
            />
            <select value={view} onChange={e => setView(e.target.value)} className="p-2 bg-gray-800 rounded text-white">
              <option value="monthly">Mensuel</option>
              <option value="weekly">Hebdomadaire</option>
              <option value="daily">Journalier</option>
            </select>
            <input
              type="date"
              value={date}
              onChange={e => setDate(e.target.value)}
              className="p-2 bg-gray-800 rounded text-white"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {games.map(game => (
              <div key={game.game_id} className={`bg-gray-800 p-4 rounded-lg shadow-lg ${game.bet && game.bet.ev > 0.05 ? 'border-2 border-green-500' : ''}`}>
                <h2 className="text-xl font-semibold">{game.home_team} vs {game.away_team}</h2>
                <p className="text-gray-300">{game.date}, {game.time}</p>
                {!game.bet ? (
                  <button
                    onClick={() => predictGame(game.game_id, game.date, team)}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded mt-2"
                  >
                    🔮 Prédire
                  </button>
                ) : (
                  <>
                    <p>Score Équipe: {game.bet.team_score.toFixed(1)}/100 ({game.bet.team_score > 85 ? 'Bonne' : game.bet.team_score > 75 ? 'Moyenne' : 'Mauvaise'})</p>
                    <p>Probabilité Victoire: {(game.bet.prob * 100).toFixed(1)}%</p>
                    <p>Cote: {game.bet.odds.toFixed(2)}</p>
                    <p className={game.bet.ev > 0.05 ? 'text-green-400' : 'text-red-400'}>
                      EV: {(game.bet.ev * 100).toFixed(1)}% {game.bet.ev > 0.05 ? '✅ PARI RECOMMANDÉ !' : '❌ Skip'}
                    </p>
                    <p>Mise Suggérée: ${game.bet.bet.toFixed(2)}</p>
                    <p>Rumeurs: {game.bet.rumors.length > 0 ? game.bet.rumors.slice(0,2).join(', ') : 'Aucune'}</p>
                    {game.bet.result !== null ? (
                      <p>Résultat: {game.bet.result === 1 ? 'Gagné ✅' : 'Perdu ❌'}</p>
                    ) : (
                      <div className="mt-2">
                        <button
                          onClick={() => addResult(game.game_id, 1)}
                          className="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded mr-2 text-sm"
                        >
                          ✅ Gagné
                        </button>
                        <button
                          onClick={() => addResult(game.game_id, 0)}
                          className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded mr-2 text-sm"
                        >
                          ❌ Perdu
                        </button>
                        <button
                          onClick={() => resetGame(game.game_id)}
                          className="bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded text-sm"
                        >
                          🔄 Re-prédire
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
          </div>
          <div className="text-center mt-8 text-gray-400">
            <p>🏒 NHL Quartet Archaeological - Simulation zéro risque</p>
            <p>Données: NHL API + The Odds API + Rumeurs</p>
          </div>
        </div>
      );
    };

    ReactDOM.render(<App />, document.getElementById('root'));
  </script>
</body>
</html>
'''

class NHLPredictor:
    def __init__(self):
        self.db = sqlite3.connect('nhl_bets_calendar.db', check_same_thread=False)
        self.db.execute('''CREATE TABLE IF NOT EXISTS bets
                         (game_id TEXT PRIMARY KEY, date TEXT, team TEXT, prob REAL, odds REAL, ev REAL, bet REAL, result INTEGER, team_score REAL, rumors TEXT)''')
        self.db.commit()

    def fetch_rumors(self, team):
        # Simulé - remplacer par vrai scraping nhltraderumors.me
        fake_rumors = {
            'MTL': ['Dobson trade rumors heating up', 'Demidov impressing in camp', 'Hutson defensive breakthrough'],
            'TOR': ['Marner extension talks continue', 'Matthews healthy for season'],
            'DET': ['Young core developing fast'],
            'CHI': ['Bedard sophomore season hype'],
            'BOS': ['Veteran leadership strong']
        }
        return fake_rumors.get(team, [])

    def fetch_roster(self, team):
        # Données simulées basées sur les vrais rosters NHL
        rosters = {
            'MTL': [
                {"name": "Cole Caufield", "role": "F", "ovr": 92, "xG": 0.8},
                {"name": "Nick Suzuki", "role": "C", "ovr": 90, "xG": 0.7},
                {"name": "Ivan Demidov", "role": "F", "ovr": 88, "xG": 0.6},
                {"name": "Noah Dobson", "role": "D", "ovr": 92, "xG": 0.3},
                {"name": "Lane Hutson", "role": "D", "ovr": 87, "xG": 0.2},
                {"name": "Kirby Dach", "role": "C", "ovr": 85, "xG": 0.5}
            ],
            'TOR': [
                {"name": "Auston Matthews", "role": "C", "ovr": 98, "xG": 1.2},
                {"name": "Mitch Marner", "role": "F", "ovr": 94, "xG": 0.9},
                {"name": "William Nylander", "role": "F", "ovr": 91, "xG": 0.8}
            ]
        }
        return rosters.get(team, [{"name": "Player", "role": "F", "ovr": 80, "xG": 0.5}] * 20)

    def generate_varied_odds(self, game_id, base_odds=2.0):
        """Génère des cotes variées basées sur l'ID du match pour éviter la répétition"""
        hash_obj = hashlib.md5(game_id.encode())
        hash_int = int(hash_obj.hexdigest()[:8], 16)
        variation = (hash_int % 100) / 1000  # 0.000 à 0.099
        return round(base_odds - 0.25 + variation * 1.0, 2)  # Cotes entre 1.75 et 2.35

    def weight_team(self, team):
        roster = self.fetch_roster(team)
        if not roster:
            return 75
        
        score = 0
        for player in roster:
            weight = 1.0 if player["role"] in ["F", "C"] else 0.8 if player["role"] == "D" else 0.5
            score += player["ovr"] * weight * (1 + player["xG"] / 2)
        
        team_score = min(score / len(roster), 100)
        
        # Bonus pour rumeurs et équipes spécifiques
        rumors = self.fetch_rumors(team)
        if any("dobson" in r.lower() or "demidov" in r.lower() for r in rumors):
            team_score += 5
        if team == "MTL":  # Go Habs Go bonus!
            team_score += 3
            
        return min(team_score, 100)

    def fetch_schedule(self, team, view, date):
        # Calendrier simulé réaliste pour octobre 2025
        fake_schedule = {
            'MTL': [
                {"id": "2025020001", "date": "2025-10-08", "homeTeam": {"abbrev": "TOR"}, "awayTeam": {"abbrev": "MTL"}, "gameTime": {"inLocal": "7:00 PM"}},
                {"id": "2025020002", "date": "2025-10-09", "homeTeam": {"abbrev": "DET"}, "awayTeam": {"abbrev": "MTL"}, "gameTime": {"inLocal": "7:30 PM"}},
                {"id": "2025020003", "date": "2025-10-11", "homeTeam": {"abbrev": "CHI"}, "awayTeam": {"abbrev": "MTL"}, "gameTime": {"inLocal": "8:00 PM"}},
                {"id": "2025020004", "date": "2025-10-13", "homeTeam": {"abbrev": "MTL"}, "awayTeam": {"abbrev": "BOS"}, "gameTime": {"inLocal": "7:00 PM"}},
                {"id": "2025020005", "date": "2025-10-15", "homeTeam": {"abbrev": "MTL"}, "awayTeam": {"abbrev": "NYR"}, "gameTime": {"inLocal": "7:30 PM"}},
                {"id": "2025020006", "date": "2025-10-18", "homeTeam": {"abbrev": "BUF"}, "awayTeam": {"abbrev": "MTL"}, "gameTime": {"inLocal": "7:00 PM"}}
            ]
        }
        
        games = fake_schedule.get(team, [])
        
        if view == "weekly":
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=6)
            games = [g for g in games if start_date <= datetime.strptime(g['date'], "%Y-%m-%d") <= end_date]
        elif view == "daily":
            games = [g for g in games if g['date'] == date]
            
        return games

    def predict(self, game_id, date, team):
        # Vérifier si prédiction existe déjà
        existing = self.get_bet(game_id)
        if existing:
            return existing
            
        # Probabilité de base (à remplacer par quartet_archaeological_simple.py)
        prob = 0.60
        
        # Ajustement basé sur le score de l'équipe
        team_score = self.weight_team(team)
        prob_adj = prob + (team_score - 80) / 500
        
        # Bonus rumeurs
        rumors = self.fetch_rumors(team)
        if any("dobson" in r.lower() or "demidov" in r.lower() for r in rumors):
            prob_adj += 0.05
        if team == "MTL":
            prob_adj += 0.05  # Go Habs Go!
            
        prob_adj = max(0.1, min(prob_adj, 0.9))  # Limiter entre 10% et 90%
        
        # Cotes variées
        odds = self.generate_varied_odds(game_id)
        
        # Expected Value
        ev = (prob_adj * (odds - 1)) - (1 - prob_adj)
        
        # Kelly Criterion avec facteur conservateur
        if ev > 0:
            kelly_fraction = ((prob_adj * (odds - 1) - (1 - prob_adj)) / (odds - 1)) * 0.25  # 25% Kelly
            bet = 100 * kelly_fraction * 0.5  # Facteur 0.5 pour être conservateur
            bet = max(0, min(bet, 100 * 0.02))  # Max 2% du bankroll
        else:
            bet = 0
            
        # Sauvegarder en base
        rumors_str = ', '.join(rumors)
        self.db.execute("""INSERT OR REPLACE INTO bets 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (game_id, date, team, prob_adj, odds, ev, bet, None, team_score, rumors_str))
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
            "team_score": team_score
        }

    def reset_bet(self, game_id):
        self.db.execute("DELETE FROM bets WHERE game_id = ?", (game_id,))
        self.db.commit()
        return {"status": "Prédiction réinitialisée"}

    def get_bet(self, game_id):
        cursor = self.db.execute("SELECT * FROM bets WHERE game_id = ?", (game_id,))
        bet = cursor.fetchone()
        if bet:
            rumors = bet[9].split(', ') if bet[9] else []
            return {
                "game_id": bet[0], "date": bet[1], "team": bet[2], 
                "prob": bet[3], "odds": bet[4], "ev": bet[5], 
                "bet": bet[6], "result": bet[7], "team_score": bet[8],
                "rumors": rumors
            }
        return None

    def add_result(self, game_id, result):
        self.db.execute("UPDATE bets SET result = ? WHERE game_id = ?", (result, game_id))
        self.db.commit()

    def get_roi(self):
        cursor = self.db.execute("SELECT bet, result, odds FROM bets WHERE result IS NOT NULL")
        total_bet, total_win = 0, 0
        for bet, result, odds in cursor:
            total_bet += bet
            if result == 1:
                total_win += bet * odds
        roi = ((total_win - total_bet) / total_bet * 100) if total_bet > 0 else 0
        balance = 100 + (total_win - total_bet)
        return {"roi": roi, "balance": balance}

# Routes API
predictor = NHLPredictor()

@app.route('/')
def index():
    return render_template_string(CALENDAR_HTML)

@app.route('/api/schedule/<team>/<view>/<date>')
def schedule(team, view, date):
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
def predict_endpoint(date, game_id, team):
    return jsonify(predictor.predict(game_id, date, team))

@app.route('/api/reset/<game_id>')
def reset_endpoint(game_id):
    return jsonify(predictor.reset_bet(game_id))

@app.route('/api/result/<game_id>/<int:result>')
def result_endpoint(game_id, result):
    predictor.add_result(game_id, result)
    return jsonify({"status": "Résultat enregistré"})

@app.route('/api/roi')
def roi_endpoint():
    return jsonify(predictor.get_roi())

if __name__ == '__main__':
    print("🏒 NHL Quartet Archaeological Calendar Ultimate")
    print("🔗 Ouvert sur: http://localhost:5006")
    print("🎯 Go Habs Go! - Simulation zéro risque")
    app.run(port=5006, debug=True)
