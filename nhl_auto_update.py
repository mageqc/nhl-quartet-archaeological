#!/usr/bin/env python3
"""
🔄 NHL BETTING AUTO-UPDATE SCRIPT
Met à jour automatiquement les données et dashboard

À lancer quotidiennement 8h00 (crontab)
"""

import subprocess
import sys
from datetime import datetime

def update_nhl_system():
    """Lance mise à jour complète système NHL"""
    
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Début mise à jour NHL...")
    
    try:
        # 1. Charger nouvelles données joueurs
        print("📊 Chargement données NHL...")
        subprocess.run([sys.executable, "nhl_full_roster_analyzer.py"], check=True)
        
        # 2. Calculer nouvelles props
        print("🎯 Calcul props du jour...")
        subprocess.run([sys.executable, "nhl_api_connector.py"], check=True)
        
        # 3. Régénérer dashboard
        print("📊 Mise à jour dashboard...")
        subprocess.run([sys.executable, "nhl_betting_dashboard.py"], check=True)
        
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Mise à jour terminée!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur mise à jour: {e}")

if __name__ == "__main__":
    update_nhl_system()
