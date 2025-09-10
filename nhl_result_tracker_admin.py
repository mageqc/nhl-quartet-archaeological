#!/usr/bin/env python3
"""
MISE-O-JEU+ NHL RESULT TRACKER
🎯 Système d'enregistrement des résultats réels
📊 Amélioration continue du Machine Learning
"""

import sqlite3
from datetime import datetime, timedelta
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

class NHLResultTracker:
    def __init__(self):
        print("📊 NHL Result Tracker - Système d'apprentissage")
        
    def simulate_game_results(self, date_str, num_days_back=7):
        """Simule des résultats de matchs pour les X derniers jours"""
        conn = sqlite3.connect('miseojeunhl_predictor.db')
        cursor = conn.cursor()
        
        # Récupère les matchs des derniers jours sans résultats
        cursor.execute('''
            SELECT id, home_team, away_team, predicted_winner, home_win_prob, 
                   bet_amount, recommendation
            FROM matches 
            WHERE game_finished = 0 AND date >= ? 
            ORDER BY date DESC
        ''', (date_str,))
        
        pending_games = cursor.fetchall()
        print(f"🎮 Simulation de {len(pending_games)} résultats de matchs...")
        
        results_updated = 0
        total_profit = 0
        
        for game in pending_games:
            game_id, home_team, away_team, predicted_winner, home_win_prob, bet_amount, recommendation = game
            
            # Simulation du résultat (avec biais léger vers les prédictions pour réalisme)
            random_factor = random.random()
            prediction_bias = 0.1  # 10% de biais vers les prédictions
            
            if random_factor < (home_win_prob + prediction_bias):
                actual_winner = home_team
                home_score = random.randint(2, 6)
                away_score = random.randint(0, home_score-1)
            else:
                actual_winner = away_team  
                away_score = random.randint(2, 6)
                home_score = random.randint(0, away_score-1)
                
            # Vérifie si la prédiction était correcte
            prediction_correct = 1 if actual_winner == predicted_winner else 0
            
            # Calcul du profit/perte
            profit_loss = 0
            if 'PARI' in recommendation and bet_amount > 0:
                if prediction_correct:
                    # Odds simulées entre 1.8 et 2.2
                    odds = random.uniform(1.8, 2.2)
                    profit_loss = bet_amount * (odds - 1)
                else:
                    profit_loss = -bet_amount
                    
            total_profit += profit_loss
            
            # Met à jour la base de données
            cursor.execute('''
                UPDATE matches SET
                    actual_winner = ?,
                    actual_score_home = ?,
                    actual_score_away = ?,
                    prediction_correct = ?,
                    profit_loss = ?,
                    game_finished = 1
                WHERE id = ?
            ''', (actual_winner, home_score, away_score, prediction_correct, profit_loss, game_id))
            
            results_updated += 1
            
        # Met à jour la bankroll
        if total_profit != 0:
            cursor.execute('''
                INSERT INTO bankroll_history (date, amount, change_amount, change_reason, created_at)
                SELECT ?, 
                       COALESCE((SELECT amount FROM bankroll_history ORDER BY id DESC LIMIT 1), 500) + ?, 
                       ?, 
                       'Résultats matchs simulés', 
                       ?
            ''', (date_str, total_profit, total_profit, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {results_updated} résultats mis à jour")
        print(f"💰 Profit/Perte total: ${total_profit:+.2f}")
        
        return results_updated, total_profit
        
    def calculate_model_performance(self):
        """Calcule les performances actuelles du modèle"""
        conn = sqlite3.connect('miseojeunhl_predictor.db')
        cursor = conn.cursor()
        
        # Statistiques globales
        cursor.execute('''
            SELECT 
                COUNT(*) as total_predictions,
                SUM(prediction_correct) as correct_predictions,
                COUNT(CASE WHEN bet_amount > 0 THEN 1 END) as total_bets,
                SUM(CASE WHEN bet_amount > 0 AND prediction_correct = 1 THEN 1 ELSE 0 END) as winning_bets,
                SUM(bet_amount) as total_wagered,
                SUM(profit_loss) as total_profit
            FROM matches 
            WHERE game_finished = 1
        ''')
        
        stats = cursor.fetchone()
        
        if stats[0] > 0:  # Si on a des données
            total_pred, correct_pred, total_bets, winning_bets, total_wagered, total_profit = stats
            
            accuracy = (correct_pred / total_pred) * 100 if total_pred > 0 else 0
            bet_success_rate = (winning_bets / total_bets) * 100 if total_bets > 0 else 0
            roi = (total_profit / total_wagered) * 100 if total_wagered > 0 else 0
            
            # Bankroll actuelle
            cursor.execute('SELECT amount FROM bankroll_history ORDER BY id DESC LIMIT 1')
            current_bankroll = cursor.fetchone()[0] if cursor.fetchone() else 500
            
            performance = {
                'total_predictions': total_pred,
                'accuracy': accuracy,
                'total_bets': total_bets,
                'bet_success_rate': bet_success_rate,
                'total_wagered': total_wagered,
                'total_profit': total_profit,
                'roi': roi,
                'current_bankroll': current_bankroll
            }
            
            # Enregistre les performances
            cursor.execute('''
                INSERT INTO model_performance (
                    date, total_predictions, correct_predictions, accuracy,
                    total_bets, winning_bets, total_wagered, total_profit, roi, bankroll, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d'), total_pred, correct_pred, accuracy,
                total_bets, winning_bets, total_wagered, total_profit, roi, current_bankroll,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            
        else:
            performance = {
                'total_predictions': 0,
                'accuracy': 0,
                'total_bets': 0, 
                'bet_success_rate': 0,
                'total_wagered': 0,
                'total_profit': 0,
                'roi': 0,
                'current_bankroll': 500
            }
        
        conn.close()
        return performance
        
    def get_recent_results(self, limit=20):
        """Récupère les résultats récents"""
        conn = sqlite3.connect('miseojeunhl_predictor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                date, home_team, away_team, predicted_winner, actual_winner,
                prediction_correct, bet_amount, profit_loss, 
                actual_score_home, actual_score_away
            FROM matches 
            WHERE game_finished = 1 
            ORDER BY date DESC, id DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results

# Instance du tracker
tracker = NHLResultTracker()

@app.route('/')
def admin_dashboard():
    """Dashboard administrateur pour le suivi des résultats"""
    html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 NHL Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: white; min-height: 100vh; padding: 20px;
        }
        
        .header { 
            text-align: center; margin-bottom: 40px;
            background: rgba(255,255,255,0.1); padding: 30px;
            border-radius: 16px; backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; color: #10b981; }
        .header p { font-size: 1.1rem; opacity: 0.8; }
        
        .actions { 
            display: flex; justify-content: center; gap: 20px;
            margin-bottom: 40px; flex-wrap: wrap;
        }
        .action-btn { 
            background: linear-gradient(45deg, #10b981, #059669);
            color: white; border: none; padding: 15px 30px;
            border-radius: 8px; font-size: 1rem; cursor: pointer;
            transition: all 0.3s;
        }
        .action-btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
        
        .performance-grid { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px; margin-bottom: 40px; max-width: 1200px; margin: 0 auto 40px;
        }
        .perf-card { 
            background: rgba(255,255,255,0.1); padding: 25px;
            border-radius: 12px; text-align: center; backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .perf-value { 
            font-size: 2.5rem; font-weight: bold; margin-bottom: 8px;
        }
        .perf-label { font-size: 1rem; opacity: 0.8; }
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        .neutral { color: #fbbf24; }
        
        .results-section { 
            max-width: 1400px; margin: 0 auto;
            background: rgba(255,255,255,0.05); padding: 30px;
            border-radius: 16px; backdrop-filter: blur(10px);
        }
        .section-title { 
            font-size: 1.5rem; margin-bottom: 20px; color: #10b981;
        }
        
        .results-table { 
            width: 100%; border-collapse: collapse;
            background: rgba(255,255,255,0.08); border-radius: 8px;
            overflow: hidden;
        }
        .results-table th { 
            background: rgba(16, 185, 129, 0.2); padding: 15px;
            text-align: left; font-weight: bold;
        }
        .results-table td { 
            padding: 12px 15px; border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .results-table tr:hover { background: rgba(255,255,255,0.05); }
        
        .result-correct { color: #10b981; font-weight: bold; }
        .result-incorrect { color: #ef4444; font-weight: bold; }
        .profit { color: #10b981; }
        .loss { color: #ef4444; }
        
        .status-message { 
            padding: 15px; margin: 20px 0; border-radius: 8px;
            text-align: center; font-weight: bold;
        }
        .status-success { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .status-info { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        
        @media (max-width: 768px) { 
            .performance-grid { grid-template-columns: 1fr; }
            .results-table { font-size: 0.9rem; }
            .results-table th, .results-table td { padding: 8px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 NHL Admin</h1>
        <p>Suivi des résultats et performance</p>
    </div>
    
    <div class="actions">
        <button class="action-btn" onclick="simulateResults()">🎮 Simuler Résultats (7 jours)</button>
        <button class="action-btn" onclick="updatePerformance()">📈 Calculer Performance</button>
        <button class="action-btn" onclick="refreshData()">🔄 Actualiser Données</button>
    </div>
    
    <div id="status-area"></div>
    
    <div class="performance-grid">
        <div class="perf-card">
            <div class="perf-value positive" id="accuracy">--%</div>
            <div class="perf-label">Précision Prédictions</div>
        </div>
        <div class="perf-card">
            <div class="perf-value neutral" id="total-bets">--</div>
            <div class="perf-label">Total Paris Placés</div>
        </div>
        <div class="perf-card">
            <div class="perf-value" id="roi">--</div>
            <div class="perf-label">ROI Global</div>
        </div>
        <div class="perf-card">
            <div class="perf-value positive" id="bankroll">$500.00</div>
            <div class="perf-label">Bankroll Actuelle</div>
        </div>
    </div>
    
    <div class="results-section">
        <div class="section-title">🎯 Résultats Récents</div>
        <div id="results-content">
            <p style="text-align: center; opacity: 0.7; padding: 40px;">
                Chargement des données...
            </p>
        </div>
    </div>

    <script>
        function showStatus(message, type = 'info') {
            const statusArea = document.getElementById('status-area');
            statusArea.innerHTML = `
                <div class="status-message status-${type}">
                    ${message}
                </div>
            `;
            
            // Auto-hide après 5 secondes
            setTimeout(() => {
                statusArea.innerHTML = '';
            }, 5000);
        }
        
        async function simulateResults() {
            showStatus('🎮 Simulation des résultats en cours...', 'info');
            
            try {
                const response = await fetch('/api/simulate-results', {
                    method: 'POST'
                });
                const data = await response.json();
                
                if (data.success) {
                    showStatus(
                        `✅ ${data.results_updated} résultats simulés - Profit/Perte: $${data.total_profit.toFixed(2)}`, 
                        'success'
                    );
                    updatePerformance();
                } else {
                    showStatus(`❌ Erreur: ${data.error}`, 'error');
                }
            } catch (error) {
                showStatus('❌ Erreur de connexion', 'error');
            }
        }
        
        async function updatePerformance() {
            try {
                const response = await fetch('/api/performance');
                const data = await response.json();
                
                if (data.success) {
                    const perf = data.performance;
                    
                    document.getElementById('accuracy').textContent = `${perf.accuracy.toFixed(1)}%`;
                    document.getElementById('total-bets').textContent = perf.total_bets;
                    document.getElementById('bankroll').textContent = `$${perf.current_bankroll.toFixed(2)}`;
                    
                    const roiEl = document.getElementById('roi');
                    roiEl.textContent = `${perf.roi > 0 ? '+' : ''}${perf.roi.toFixed(1)}%`;
                    roiEl.className = `perf-value ${perf.roi > 0 ? 'positive' : perf.roi < 0 ? 'negative' : 'neutral'}`;
                    
                    loadRecentResults();
                }
            } catch (error) {
                showStatus('❌ Erreur lors du calcul des performances', 'error');
            }
        }
        
        async function loadRecentResults() {
            try {
                const response = await fetch('/api/recent-results');
                const data = await response.json();
                
                if (data.success && data.results.length > 0) {
                    const resultsHtml = `
                        <table class="results-table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Match</th>
                                    <th>Prédiction</th>
                                    <th>Résultat</th>
                                    <th>Score</th>
                                    <th>Pari</th>
                                    <th>P&L</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.results.map(result => `
                                    <tr>
                                        <td>${result[0]}</td>
                                        <td>${result[2]} @ ${result[1]}</td>
                                        <td>${result[3]}</td>
                                        <td class="${result[5] ? 'result-correct' : 'result-incorrect'}">
                                            ${result[4]} ${result[5] ? '✓' : '✗'}
                                        </td>
                                        <td>${result[8]}-${result[9]}</td>
                                        <td>$${result[6].toFixed(2)}</td>
                                        <td class="${result[7] >= 0 ? 'profit' : 'loss'}">
                                            ${result[7] >= 0 ? '+' : ''}$${result[7].toFixed(2)}
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                    
                    document.getElementById('results-content').innerHTML = resultsHtml;
                } else {
                    document.getElementById('results-content').innerHTML = `
                        <p style="text-align: center; opacity: 0.7; padding: 40px;">
                            Aucun résultat disponible. Simulez d'abord quelques matchs.
                        </p>
                    `;
                }
            } catch (error) {
                document.getElementById('results-content').innerHTML = `
                    <p style="text-align: center; color: #ef4444; padding: 40px;">
                        Erreur lors du chargement des résultats
                    </p>
                `;
            }
        }
        
        function refreshData() {
            updatePerformance();
            showStatus('🔄 Données actualisées', 'success');
        }
        
        // Initialisation
        updatePerformance();
        
        // Auto-refresh toutes les 30 secondes
        setInterval(updatePerformance, 30000);
    </script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route('/api/simulate-results', methods=['POST'])
def simulate_results_api():
    """API pour simuler des résultats de matchs"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        results_updated, total_profit = tracker.simulate_game_results(seven_days_ago)
        
        return jsonify({
            'success': True,
            'results_updated': results_updated,
            'total_profit': total_profit
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/performance')
def performance_api():
    """API pour récupérer les performances du modèle"""
    try:
        performance = tracker.calculate_model_performance()
        return jsonify({
            'success': True,
            'performance': performance
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recent-results')
def recent_results_api():
    """API pour récupérer les résultats récents"""
    try:
        results = tracker.get_recent_results(20)
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("📊 NHL Admin sur http://localhost:5010")
    app.run(host='0.0.0.0', port=5010, debug=True)
