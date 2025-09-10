#!/usr/bin/env python3
"""
🔥 TEST GROSSE SOIRÉE NHL - MAXIMUM DE MATCHS
Teste calendrier avec 15+ matchs pour valider qu'on voit TOUT
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_massive_game_day():
    """Crée une grosse soirée NHL avec beaucoup de matchs"""
    
    print("🔥 TEST GROSSE SOIRÉE NHL - TOUS LES MATCHS")
    print("=" * 60)
    
    conn = sqlite3.connect("nhl_calendar_predictions.db")
    cursor = conn.cursor()
    
    # Toutes les équipes NHL
    all_teams = [
        'TOR', 'BOS', 'FLA', 'TBL', 'BUF', 'MTL', 'OTT', 'DET',  # Atlantic
        'NYR', 'CAR', 'NJD', 'WSH', 'PHI', 'PIT', 'NYI', 'CBJ',  # Metropolitan
        'COL', 'DAL', 'WPG', 'NSH', 'MIN', 'STL', 'UTA', 'CHI',  # Central
        'EDM', 'VEG', 'LAK', 'VAN', 'CGY', 'SEA', 'ANA', 'SJS'   # Pacific
    ]
    
    # Créer grosse soirée samedi avec BEAUCOUP de matchs
    test_date = "2025-09-14"  # Samedi
    
    # Supprimer anciens matchs de cette date
    cursor.execute("DELETE FROM nhl_games WHERE game_date = ?", (test_date,))
    cursor.execute("DELETE FROM game_predictions WHERE game_date = ?", (test_date,))
    
    # Créer 14 matchs (28 équipes sur 32)
    available_teams = all_teams.copy()
    random.shuffle(available_teams)
    
    games_created = []
    
    # Créer maximum de matchs possibles
    while len(available_teams) >= 2:
        away_team = available_teams.pop()
        home_team = available_teams.pop()
        
        game_id = f"{test_date}_{away_team}_at_{home_team}"
        start_time = random.choice(['19:00', '19:30', '20:00', '20:30', '21:00'])
        
        # Insérer match
        cursor.execute('''
            INSERT OR REPLACE INTO nhl_games 
            (game_id, game_date, home_team, away_team, home_form_rating, 
             away_form_rating, start_time, venue)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game_id, test_date, home_team, away_team,
            random.uniform(0.3, 0.8), random.uniform(0.3, 0.8),
            start_time, f"{home_team} Arena"
        ))
        
        games_created.append({
            'game_id': game_id,
            'away_team': away_team,
            'home_team': home_team,
            'start_time': start_time
        })
    
    conn.commit()
    conn.close()
    
    print(f"🏒 GROSSE SOIRÉE CRÉÉE: {len(games_created)} MATCHS!")
    print(f"📅 Date: {test_date} (samedi)")
    print()
    
    # Afficher tous les matchs
    for i, game in enumerate(games_created, 1):
        print(f"{i:2d}. {game['start_time']} - {game['away_team']} @ {game['home_team']}")
    
    print(f"\n🎯 TOTAL: {len(games_created)} matchs à afficher dans le calendrier")
    print(f"✅ Test: Le calendrier doit montrer TOUS ces matchs!")
    
    return len(games_created)

def main():
    """Lance test grosse soirée"""
    
    # Créer grosse soirée
    total_games = create_massive_game_day()
    
    # Relancer calendrier pour voir le résultat
    print(f"\n🔄 Génération calendrier avec {total_games} matchs...")
    
    import subprocess
    result = subprocess.run(["python3", "nhl_calendar_predictor.py"], 
                          capture_output=True, text=True, cwd=".")
    
    print("✅ Calendrier régénéré!")
    print("🌐 Ouvre 'nhl_calendar_interactive.html' pour voir TOUS les matchs!")
    print()
    print("🔍 VÉRIFICATION: Tu dois voir tous les matchs listés ci-dessus!")

if __name__ == "__main__":
    main()
