#!/usr/bin/env python3
"""
🔍 DÉMO VALIDATION CALENDRIER NHL
Simule validation automatique de prédictions pour montrer le système
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

def simulate_validation_demo():
    """Simule validation complète des prédictions d'hier"""
    
    print("🔍 DÉMO VALIDATION PRÉDICTIONS NHL")
    print("=" * 50)
    
    conn = sqlite3.connect("nhl_calendar_predictions.db")
    cursor = conn.cursor()
    
    # Récupérer prédictions d'aujourd'hui pour simulation
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT prediction_id, game_id, home_team, away_team, 
               predicted_winner, predicted_home_score, predicted_away_score,
               home_win_probability, prediction_confidence
        FROM game_predictions 
        WHERE game_date = ? AND actual_winner IS NULL
    ''', (today,))
    
    predictions = cursor.fetchall()
    
    print(f"📊 Validation de {len(predictions)} prédictions pour {today}")
    print()
    
    validated_count = 0
    correct_winners = 0
    
    for pred in predictions:
        (pred_id, game_id, home_team, away_team, predicted_winner, 
         pred_home_score, pred_away_score, home_win_prob, confidence) = pred
        
        # Simuler résultat réaliste (75% précision pour démo)
        prediction_correct = random.random() < 0.75
        
        if prediction_correct:
            # Prédiction correcte - ajuster légèrement le score
            actual_winner = predicted_winner
            actual_home = pred_home_score + random.randint(-1, 1)
            actual_away = pred_away_score + random.randint(-1, 1)
            correct_winners += 1
        else:
            # Prédiction incorrecte
            actual_winner = away_team if predicted_winner == home_team else home_team  
            actual_home = pred_home_score + random.randint(-2, 2)
            actual_away = pred_away_score + random.randint(-2, 2)
        
        # S'assurer scores positifs
        actual_home = max(0, actual_home)
        actual_away = max(0, actual_away)
        
        # Ajuster vainqueur selon scores
        if actual_home > actual_away:
            actual_winner = home_team
        elif actual_away > actual_home:
            actual_winner = away_team
        else:
            # Overtime - ajouter 1 but au vainqueur prédit
            if predicted_winner == home_team:
                actual_home += 1
                actual_winner = home_team
            else:
                actual_away += 1
                actual_winner = away_team
        
        actual_total = actual_home + actual_away
        
        # Calculer précision
        winner_correct = (actual_winner == predicted_winner)
        score_exact = (actual_home == pred_home_score and actual_away == pred_away_score)
        total_correct = (actual_total == pred_home_score + pred_away_score)
        
        accuracy = 0.0
        if winner_correct:
            accuracy += 0.6
        if score_exact:
            accuracy += 0.3
        if total_correct:
            accuracy += 0.1
        
        # Mettre à jour base
        cursor.execute('''
            UPDATE game_predictions SET
                actual_winner = ?, actual_home_score = ?, actual_away_score = ?,
                actual_total_goals = ?, winner_correct = ?, score_exact = ?,
                total_goals_correct = ?, prediction_accuracy = ?, validated_at = ?
            WHERE prediction_id = ?
        ''', (
            actual_winner, actual_home, actual_away, actual_total,
            winner_correct, score_exact, total_correct, accuracy,
            datetime.now().isoformat(), pred_id
        ))
        
        # Mettre à jour match
        cursor.execute('''
            UPDATE nhl_games SET
                home_score = ?, away_score = ?, game_status = 'FINAL'
            WHERE game_id = ?
        ''', (actual_home, actual_away, game_id))
        
        # Afficher résultat
        status_icon = "✅" if winner_correct else "❌"
        confidence_text = f"{confidence*100:.0f}%" 
        
        print(f"{status_icon} {away_team} {actual_away} - {actual_home} {home_team}")
        print(f"   🎯 Prédit: {predicted_winner} ({confidence_text} confiance)")
        print(f"   🏒 Résultat: {actual_winner} gagne")
        print(f"   📊 Précision: {accuracy*100:.0f}%")
        print()
        
        validated_count += 1
    
    conn.commit()
    conn.close()
    
    # Stats finales
    success_rate = (correct_winners / validated_count * 100) if validated_count > 0 else 0
    
    print(f"📈 RÉSULTATS VALIDATION:")
    print(f"   ✅ {correct_winners}/{validated_count} vainqueurs corrects ({success_rate:.1f}%)")
    print(f"   🎯 Performance: {'Excellente' if success_rate >= 70 else 'Bonne' if success_rate >= 60 else 'Correcte' if success_rate >= 50 else 'À améliorer'}")
    
    return validated_count

def main():
    """Lance démo validation"""
    validated = simulate_validation_demo()
    
    if validated > 0:
        print(f"\n🔄 Régénération calendrier avec résultats...")
        
        # Relancer générateur calendrier pour voir résultats
        import subprocess
        subprocess.run(["python3", "nhl_calendar_predictor.py"], cwd=".")
        
        print(f"✅ Calendrier mis à jour avec validations!")
        print(f"🌐 Ouvre 'nhl_calendar_interactive.html' pour voir les résultats!")
    else:
        print(f"ℹ️  Aucune prédiction à valider pour le moment.")

if __name__ == "__main__":
    main()
