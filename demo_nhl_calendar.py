#!/usr/bin/env python3
"""
🏒 Démonstration NHL Quartet Archaeological Calendar
Test automatique du système de calendrier et prédictions NHL
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:5007/api"

def test_api():
    """Test complet de l'API NHL Calendar"""
    print("🏒 NHL QUARTET ARCHAEOLOGICAL - DÉMONSTRATION")
    print("=" * 50)
    
    # 1. Test du calendrier MTL
    print("\n📅 1. CALENDRIER MTL OCTOBRE 2025:")
    try:
        response = requests.get(f"{API_BASE}/schedule/MTL/monthly/2025-10-01")
        games = response.json()
        
        for i, game in enumerate(games, 1):
            print(f"   {i}. {game['date']} - {game['home_team']} vs {game['away_team']} à {game['time']}")
        
        print(f"\n✅ {len(games)} matchs trouvés pour MTL en octobre")
        
    except Exception as e:
        print(f"❌ Erreur calendrier: {e}")
        return
    
    # 2. Test d'une prédiction
    if games:
        print(f"\n🔮 2. PRÉDICTION POUR LE PREMIER MATCH:")
        game = games[0]
        
        try:
            response = requests.get(f"{API_BASE}/predict/{game['date']}/{game['game_id']}/MTL")
            prediction = response.json()
            
            print(f"   Match: {game['home_team']} vs {game['away_team']} ({game['date']})")
            print(f"   Score équipe MTL: {prediction['team_score']:.1f}/100")
            print(f"   Probabilité victoire: {prediction['prob']*100:.1f}%")
            print(f"   Cote: {prediction['odds']:.2f}")
            print(f"   Expected Value: {prediction['ev']*100:.1f}%")
            print(f"   Mise suggérée: ${prediction['bet']:.2f}")
            
            if prediction['ev'] > 0.05:
                print("   🟢 ✅ PARI RECOMMANDÉ!")
            else:
                print("   🔴 ❌ Skip ce pari")
                
        except Exception as e:
            print(f"❌ Erreur prédiction: {e}")
            return
    
    # 3. Test ROI initial
    print(f"\n💰 3. ROI INITIAL:")
    try:
        response = requests.get(f"{API_BASE}/roi")
        roi = response.json()
        print(f"   ROI: {roi['roi']:.1f}%")
        print(f"   Balance: ${roi['balance']:.2f}")
    except Exception as e:
        print(f"❌ Erreur ROI: {e}")
    
    # 4. Simulation de paris
    print(f"\n🎲 4. SIMULATION DE PARIS:")
    wins = 0
    total_bets = 0
    
    for i, game in enumerate(games[:3]):  # Test sur 3 matchs
        try:
            # Prédiction
            response = requests.get(f"{API_BASE}/predict/{game['date']}/{game['game_id']}/MTL")
            pred = response.json()
            
            if pred['bet'] > 0:  # Seulement si pari recommandé
                total_bets += 1
                
                # Simulation résultat (50% chance de gagner pour la démo)
                import random
                result = 1 if random.random() < pred['prob'] else 0
                wins += result
                
                # Enregistrer le résultat
                requests.get(f"{API_BASE}/result/{game['game_id']}/{result}")
                
                status = "Gagné ✅" if result else "Perdu ❌"
                print(f"   Match {i+1}: ${pred['bet']:.2f} → {status}")
            else:
                print(f"   Match {i+1}: Skip (EV négatif)")
                
        except Exception as e:
            print(f"❌ Erreur simulation match {i+1}: {e}")
    
    # 5. ROI final
    print(f"\n📊 5. RÉSULTATS FINAUX:")
    try:
        response = requests.get(f"{API_BASE}/roi")
        roi = response.json()
        print(f"   Paris placés: {total_bets}")
        print(f"   Paris gagnés: {wins}")
        print(f"   Taux de réussite: {wins/total_bets*100:.1f}%" if total_bets > 0 else "   Aucun pari")
        print(f"   ROI final: {roi['roi']:.1f}%")
        print(f"   Balance finale: ${roi['balance']:.2f}")
        
        if roi['balance'] > 100:
            print("   🟢 Profit! 💰")
        elif roi['balance'] < 100:
            print("   🔴 Perte 📉")
        else:
            print("   ⚪ Break-even")
            
    except Exception as e:
        print(f"❌ Erreur ROI final: {e}")
    
    print(f"\n🏒 DÉMONSTRATION TERMINÉE!")
    print("💡 Ouvre http://localhost:5007 pour l'interface web")
    print("🎯 Go Habs Go! - Simulation zéro risque")

def test_different_teams():
    """Test avec différentes équipes"""
    print(f"\n🔄 TEST ÉQUIPES MULTIPLES:")
    teams = ['MTL', 'TOR', 'BOS']
    
    for team in teams:
        try:
            response = requests.get(f"{API_BASE}/schedule/{team}/weekly/2025-10-08")
            games = response.json()
            print(f"   {team}: {len(games)} matchs cette semaine")
        except:
            print(f"   {team}: Erreur")

if __name__ == "__main__":
    # Attendre que le serveur soit prêt
    print("⏳ Attente du serveur...")
    time.sleep(2)
    
    # Test principal
    test_api()
    
    # Test bonus
    test_different_teams()
    
    print(f"\n🎮 PROCHAINES ÉTAPES:")
    print("1. Ouvre http://localhost:5007 dans ton navigateur")
    print("2. Clique sur 'Actualiser' pour voir le calendrier MTL")
    print("3. Clique '🔮 Prédire' sur un match")
    print("4. Teste '✅ Gagné' / '❌ Perdu' / '🔄 Re-prédire'")
    print("5. Regarde ton ROI évoluer!")
    print("\n🏒 STANLEY CUP DES PARIS! 🚀")
