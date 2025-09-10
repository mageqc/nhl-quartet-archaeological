#!/usr/bin/env python3
"""
🎯 DEMO PREDICTIONS GENERATOR
Génère prédictions demo pour tester le système trio complet
"""

import sqlite3
from datetime import datetime

def create_demo_predictions():
    """Créé prédictions demo pour présaison MTL"""
    
    conn = sqlite3.connect('nhl_trio_system.db')
    cursor = conn.cursor()
    
    # Assure que table existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_predictions (
            game_id TEXT PRIMARY KEY,
            predicted_winner TEXT,
            prediction_confidence REAL,
            predicted_home_score INTEGER,
            predicted_away_score INTEGER,
            key_factors TEXT,
            actual_winner TEXT,
            winner_correct INTEGER,
            prediction_accuracy REAL,
            validated_at TEXT,
            ml_method TEXT,
            sentiment_score REAL
        )
    ''')
    
    # Prédictions présaison MTL
    demo_predictions = [
        {
            'game_id': 'pit_mtl_20250922',
            'predicted_winner': 'home',  # MTL
            'prediction_confidence': 0.65,
            'predicted_home_score': 3,
            'predicted_away_score': 2,
            'key_factors': 'Home advantage, Caufield line chemistry, preseason momentum',
            'ml_method': 'Trio Fusion (Grok+Gemini+ChatGPT)',
            'sentiment_score': 0.7
        },
        {
            'game_id': 'phi_mtl_20250923', 
            'predicted_winner': 'away',  # PHI
            'prediction_confidence': 0.58,
            'predicted_home_score': 2,
            'predicted_away_score': 3,
            'key_factors': 'Philly back-to-back rest advantage, MTL fatigue',
            'ml_method': 'Trio Fusion (Grok+Gemini+ChatGPT)',
            'sentiment_score': 0.45
        },
        {
            'game_id': 'mtl_tor_20250925',
            'predicted_winner': 'away',  # TOR  
            'prediction_confidence': 0.72,
            'predicted_home_score': 2,
            'predicted_away_score': 4,
            'key_factors': 'Toronto superior depth, Matthews factor, away revenge',
            'ml_method': 'Trio Fusion (Grok+Gemini+ChatGPT)', 
            'sentiment_score': 0.3
        },
        {
            'game_id': 'mtl_ott_20250927',
            'predicted_winner': 'home',  # MTL
            'prediction_confidence': 0.61,
            'predicted_home_score': 3,
            'predicted_away_score': 1,
            'key_factors': 'Home finale preseason, Tkachuk injury concerns Ottawa',
            'ml_method': 'Trio Fusion (Grok+Gemini+ChatGPT)',
            'sentiment_score': 0.68
        }
    ]
    
    # Insert predictions
    for pred in demo_predictions:
        cursor.execute('''
            INSERT OR REPLACE INTO game_predictions
            (game_id, predicted_winner, prediction_confidence, 
             predicted_home_score, predicted_away_score, key_factors,
             ml_method, sentiment_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pred['game_id'],
            pred['predicted_winner'],
            pred['prediction_confidence'],
            pred['predicted_home_score'],
            pred['predicted_away_score'],
            pred['key_factors'],
            pred['ml_method'],
            pred['sentiment_score']
        ))
    
    conn.commit()
    conn.close()
    
    print("✅ Demo predictions created:")
    for pred in demo_predictions:
        confidence_pct = pred['prediction_confidence'] * 100
        print(f"   🎯 {pred['game_id']}: {pred['predicted_winner']} ({confidence_pct:.0f}%)")

if __name__ == "__main__":
    create_demo_predictions()
