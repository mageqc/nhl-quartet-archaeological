#!/usr/bin/env python3
"""
🎨 INTÉGRATION LOGOS NHL - CALENDRIER ENHANCED
Mise à jour calendrier existant avec logos officiels NHL
"""

import sqlite3
from datetime import datetime, timedelta
from nhl_logos_system import NHLLogosSystem

class NHLCalendarWithLogos:
    """
    🎨 CALENDRIER NHL AVEC LOGOS OFFICIELS
    
    Améliore le calendrier existant:
    - Logos équipes dans matchups
    - Couleurs officielles équipes  
    - Design professionnel NHL
    - Fallback gracieux
    """
    
    def __init__(self):
        print("🎨 INTÉGRATION LOGOS NHL AU CALENDRIER")
        print("=" * 50)
        
        self.logos_system = NHLLogosSystem()
        self.calendar_db = "nhl_calendar_predictions.db"
        self.enhanced_html = "nhl_calendar_enhanced_logos.html"
        
    def generate_enhanced_calendar_html(self) -> str:
        """Génère calendrier HTML avec logos officiels"""
        
        print("🎨 Génération calendrier avec logos NHL...")
        
        # Récupérer données calendrier
        conn = sqlite3.connect(self.calendar_db)
        cursor = conn.cursor()
        
        # Matchs des 7 prochains jours
        today = datetime.now()
        calendar_data = {}
        
        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            # Récupérer matchs + prédictions
            cursor.execute('''
                SELECT g.game_id, g.home_team, g.away_team, g.start_time,
                       g.home_score, g.away_score, g.game_status,
                       p.predicted_winner, p.predicted_home_score, p.predicted_away_score,
                       p.home_win_probability, p.prediction_confidence, p.key_factors,
                       p.actual_winner, p.winner_correct, p.prediction_accuracy
                FROM nhl_games g
                LEFT JOIN game_predictions p ON g.game_id = p.game_id
                WHERE g.game_date = ?
                ORDER BY g.start_time
            ''', (date_str,))
            
            games = cursor.fetchall()
            calendar_data[date_str] = {
                'date_obj': date,
                'games': games
            }
        
        # Stats performance
        cursor.execute('''
            SELECT 
                COUNT(*) as total_predictions,
                SUM(CASE WHEN winner_correct = 1 THEN 1 ELSE 0 END) as correct_winners,
                AVG(prediction_accuracy) as avg_accuracy
            FROM game_predictions 
            WHERE validated_at IS NOT NULL
        ''')
        stats = cursor.fetchone()
        
        conn.close()
        
        # Génération HTML avec logos
        html_content = self._generate_html_with_logos(calendar_data, stats)
        
        # Sauvegarder
        with open(self.enhanced_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Calendrier avec logos généré: {self.enhanced_html}")
        return self.enhanced_html
    
    def _generate_html_with_logos(self, calendar_data: dict, stats: tuple) -> str:
        """Génère HTML complet avec logos NHL"""
        
        # CSS amélioré avec logos
        logos_css = self.logos_system.export_logos_css()
        
        html_content = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏒 Calendrier NHL avec Logos Officiels</title>
    <style>
        {self._get_enhanced_css()}
        {logos_css}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏒 Calendrier NHL avec Logos Officiels</h1>
        <p>Matchs quotidiens • Prédictions automatiques • Logos équipes authentiques</p>
        
        <!-- Badge source données -->
        <div class="source-badge">
            🎮 Mode Simulation - Calendrier d'entraînement (Hors saison NHL)
        </div>
    </div>
    
    <div class="stats-summary">
        <div class="stat-item">
            <div class="stat-number">{stats[0] or 0}</div>
            <div>Prédictions Total</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{stats[1] or 0}</div>
            <div>Vainqueurs Corrects</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{(stats[1]/stats[0]*100 if stats[0] > 0 else 0):.1f}%</div>
            <div>Précision Globale</div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser</button>
    
    <div class="calendar-grid">
'''
        
        # Ajouter chaque jour avec logos
        from datetime import timedelta
        for date_str in sorted(calendar_data.keys()):
            day_info = calendar_data[date_str]
            date_obj = day_info['date_obj']
            games = day_info['games']
            
            # Nom du jour en français
            day_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            day_name = day_names[date_obj.weekday()]
            
            # Badge nombre matchs
            games_count = len(games)
            games_badge = ""
            if games_count >= 10:
                games_badge = f'<span class="games-badge mega">🔥 {games_count} matchs</span>'
            elif games_count >= 6:
                games_badge = f'<span class="games-badge many">🏒 {games_count} matchs</span>'
            elif games_count > 0:
                games_badge = f'<span class="games-badge normal">{games_count} matchs</span>'
            
            html_content += f'''
        <div class="day-card">
            <div class="day-header">
                <h3 class="day-title">{day_name} {games_badge}</h3>
                <p class="day-date">{date_obj.strftime('%d %B %Y')}</p>
            </div>
            
            <div class="games-container">
'''
            
            if games:
                for game in games:
                    (game_id, home_team, away_team, start_time, home_score, away_score, 
                     game_status, pred_winner, pred_home, pred_away, home_win_prob, 
                     confidence, key_factors, actual_winner, winner_correct, accuracy) = game
                    
                    # Génération matchup avec logos
                    matchup_html = self.logos_system.get_matchup_html(
                        away_team, home_team, size='medium', show_vs=True
                    )
                    
                    html_content += f'''
                <div class="game-card">
                    <div class="game-matchup-enhanced">
                        {matchup_html}
                    </div>
                    <div class="game-time">{start_time or '19:00'}</div>
'''
                    
                    # Afficher résultat final si disponible
                    if home_score is not None and away_score is not None:
                        result_class = "result correct" if winner_correct else "result incorrect"
                        status_icon = "✅" if winner_correct else "❌"
                        accuracy_pct = (accuracy * 100) if accuracy is not None else 0
                        
                        html_content += f'''
                    <div class="{result_class}">
                        <strong>FINAL: {away_team} {away_score} - {home_score} {home_team}</strong>
                        <br>Prédiction: {status_icon} ({accuracy_pct:.0f}% précision)
                    </div>
'''
                    
                    # Afficher prédiction si disponible  
                    elif pred_winner:
                        confidence_class = "high" if confidence > 0.7 else "medium" if confidence > 0.5 else "low"
                        
                        try:
                            import json
                            factors = json.loads(key_factors) if key_factors else []
                        except:
                            factors = []
                        
                        html_content += f'''
                    <div class="prediction">
                        <div class="prediction-title">
                            🎯 Prédiction: {pred_winner}
                            <span class="confidence {confidence_class}">{confidence*100:.0f}%</span>
                        </div>
                        <div class="prediction-details">
                            Score prédit: {away_team} {pred_away} - {pred_home} {home_team}<br>
                            Prob. victoire domicile: {home_win_prob*100:.0f}%
'''
                        
                        if factors:
                            html_content += f"<br>Facteurs: {', '.join(factors[:2])}"
                        
                        html_content += '''
                        </div>
                    </div>
'''
                    
                    html_content += '</div>'
                
            else:
                html_content += '''
                <div class="no-games">
                    🏒 Pas de matchs programmés ce jour
                </div>
'''
            
            html_content += '''
            </div>
        </div>
'''
        
        html_content += f'''
    </div>
    
    <div class="update-time">
        Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        🎨 Logos NHL officiels • Prédictions automatiques • Design authentique
    </div>
    
    <script>
        // Auto-refresh chaque 10 minutes
        setTimeout(() => location.reload(), 600000);
        
        // Animation logos au survol
        document.addEventListener('DOMContentLoaded', function() {{
            const logos = document.querySelectorAll('.team-logo');
            logos.forEach(logo => {{
                logo.addEventListener('mouseenter', function() {{
                    this.style.transform = 'scale(1.1) rotate(5deg)';
                }});
                logo.addEventListener('mouseleave', function() {{
                    this.style.transform = 'scale(1) rotate(0deg)';
                }});
            }});
        }});
        
        console.log('🏒 Calendrier NHL avec logos officiels chargé!');
    </script>
</body>
</html>
        '''
        
        return html_content
    
    def _get_enhanced_css(self) -> str:
        """CSS amélioré pour calendrier avec logos"""
        
        return '''
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #0f4c75, #3282b8, #0f4c75);
            color: white;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(0,0,0,0.4);
            padding: 20px;
            text-align: center;
            border-bottom: 3px solid #ffd700;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.8em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .source-badge {
            background: linear-gradient(45deg, #ff9800, #ff7043);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            margin: 15px auto;
            display: inline-block;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255,152,0,0.3);
        }
        
        .stats-summary {
            display: flex;
            justify-content: center;
            gap: 30px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            margin: 20px;
            border-radius: 15px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.8em;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 2200px;
            margin: 0 auto;
        }
        
        .day-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 2px solid rgba(255,215,0,0.3);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .day-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(255,215,0,0.2);
            border-color: #ffd700;
        }
        
        .day-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ffd700;
        }
        
        .day-title {
            font-size: 1.4em;
            font-weight: bold;
            margin: 0;
            color: #ffd700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .games-badge {
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .games-badge.normal { background: #2196F3; }
        .games-badge.many { background: #4CAF50; }
        .games-badge.mega { background: #ff6b35; }
        
        .day-date {
            font-size: 1.1em;
            margin: 5px 0 0 0;
            color: #ccc;
        }
        
        .games-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            max-height: 600px;
            overflow-y: auto;
            padding-right: 5px;
        }
        
        .games-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .games-container::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        
        .games-container::-webkit-scrollbar-thumb {
            background: #ffd700;
            border-radius: 4px;
        }
        
        .game-card {
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 15px;
            border-left: 4px solid #ffd700;
            transition: all 0.3s ease;
        }
        
        .game-card:hover {
            background: rgba(0,0,0,0.3);
            border-left-width: 6px;
            transform: translateX(5px);
        }
        
        .game-matchup-enhanced {
            margin-bottom: 10px;
        }
        
        .game-time {
            text-align: center;
            color: #ccc;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .prediction {
            background: rgba(255,215,0,0.1);
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid rgba(255,215,0,0.3);
        }
        
        .prediction-title {
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 5px;
        }
        
        .confidence {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .confidence.high { background: #4CAF50; color: white; }
        .confidence.medium { background: #ff9800; color: white; }
        .confidence.low { background: #f44336; color: white; }
        
        .result {
            background: rgba(0,150,0,0.2);
            border-left: 4px solid #4CAF50;
            padding: 10px;
            margin-top: 10px;
            border-radius: 8px;
        }
        
        .result.incorrect {
            background: rgba(150,0,0,0.2);
            border-left-color: #f44336;
        }
        
        .refresh-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ffd700;
            color: #0f4c75;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        
        .refresh-btn:hover {
            background: #ffed4e;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .update-time {
            text-align: center;
            padding: 20px;
            color: #aaa;
            font-size: 0.9em;
        }
        
        .no-games {
            text-align: center;
            color: #888;
            font-style: italic;
            padding: 30px;
        }
        '''

def main():
    """Lance calendrier NHL avec logos officiels"""
    
    print("🚀 CALENDRIER NHL AVEC LOGOS - GÉNÉRATION")
    
    calendar_with_logos = NHLCalendarWithLogos()
    enhanced_calendar = calendar_with_logos.generate_enhanced_calendar_html()
    
    print(f"\n✅ CALENDRIER AVEC LOGOS PRÊT!")
    print(f"🎨 Interface: {enhanced_calendar}")
    print(f"🏒 32 équipes avec logos NHL officiels intégrés!")

if __name__ == "__main__":
    main()
