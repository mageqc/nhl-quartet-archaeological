#!/usr/bin/env python3
"""
🔄 NHL CALENDAR AUTO-UPDATER
Script quotidien pour prédictions + validations automatiques

À lancer chaque matin 7h00 via crontab
"""

import sys
from datetime import datetime
from nhl_betting_dashboard import NHLCalendarPredictor

def daily_calendar_update():
    """Update quotidien calendrier NHL"""
    
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Début update calendrier NHL...")
    
    try:
        # Lancer système calendrier
        calendar = NHLCalendarPredictor()
        
        # Cycle prédictions + validation  
        results = calendar.run_daily_prediction_cycle()
        
        # Régénérer calendrier HTML
        calendar.generate_calendar_html()
        
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Calendrier mis à jour!")
        print(f"   🎯 {results['predictions_made']} prédictions")
        print(f"   ✅ {results['validated']} résultats validés")
        
    except Exception as e:
        print(f"❌ Erreur update calendrier: {e}")

if __name__ == "__main__":
    daily_calendar_update()
