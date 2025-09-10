"""
🗓️ CALENDRIER SIMPLIFIÉ - TEST DES VALEURS SÛRES NHL 2025-26 🗓️

Version test pour valider la logique de base
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.analyzers.official_data_integrator import get_betting_schedule_data
import json
from datetime import datetime
from collections import defaultdict


def tester_calendrier_simple():
    """
    Test simple du calendrier pour identifier le problème
    """
    print("🗓️ TEST CALENDRIER SIMPLIFIÉ")
    print("=" * 35)
    
    # 1. Charger le calendrier
    print("📅 Chargement calendrier...")
    try:
        calendrier = get_betting_schedule_data()
        print(f"   ✅ Calendrier chargé")
        
        if 'by_date' in calendrier:
            print(f"   📊 Format: by_date avec {len(calendrier['by_date'])} jours")
            
            # Compter les matchs par type
            matchs_par_type = defaultdict(int)
            matchs_saison_reguliere = []
            
            for jour, matchs in calendrier['by_date'].items():
                for match in matchs:
                    game_type = match.get('game_type', 0)
                    matchs_par_type[game_type] += 1
                    
                    if game_type == 2:  # Saison régulière
                        matchs_saison_reguliere.append({
                            'date': jour,
                            'match': f"{match.get('away_team', '')} @ {match.get('home_team', '')}",
                            'away_abbr': match.get('away_abbr', ''),
                            'home_abbr': match.get('home_abbr', ''),
                            'venue': match.get('venue', '')
                        })
            
            print(f"\n📊 RÉPARTITION DES MATCHS:")
            for game_type, count in matchs_par_type.items():
                type_name = {1: 'Preseason', 2: 'Regular Season', 3: 'Playoffs'}.get(game_type, f'Type {game_type}')
                print(f"   {type_name}: {count} matchs")
            
            print(f"\n🏒 MATCHS SAISON RÉGULIÈRE: {len(matchs_saison_reguliere)}")
            
            if matchs_saison_reguliere:
                print(f"\n📅 PREMIERS MATCHS SAISON RÉGULIÈRE:")
                for i, match in enumerate(matchs_saison_reguliere[:10], 1):
                    print(f"   {i:2d}. {match['date']}: {match['match']}")
                    print(f"       Codes: {match['away_abbr']} @ {match['home_abbr']}")
                    print(f"       Venue: {match['venue']}")
                
                # Analyser les dates d'ouverture
                dates_ouverture = set()
                for match in matchs_saison_reguliere[:20]:
                    dates_ouverture.add(match['date'])
                
                print(f"\n🏁 DATES D'OUVERTURE:")
                for date in sorted(dates_ouverture):
                    matchs_ce_jour = [m for m in matchs_saison_reguliere if m['date'] == date]
                    print(f"   {date}: {len(matchs_ce_jour)} matchs")
                    for match in matchs_ce_jour[:3]:  # Max 3 par jour
                        print(f"      • {match['match']}")
                
                # Stats historiques simples pour test
                stats_test = {
                    'BOS': {'strength': 95, 'home_adv': 0.75},
                    'NYR': {'strength': 90, 'home_adv': 0.72},
                    'TOR': {'strength': 88, 'home_adv': 0.70},
                    'EDM': {'strength': 92, 'home_adv': 0.76},
                    'CGY': {'strength': 82, 'home_adv': 0.68},
                    'FLA': {'strength': 94, 'home_adv': 0.78},
                    'CHI': {'strength': 75, 'home_adv': 0.62},
                    'WSH': {'strength': 85, 'home_adv': 0.70},
                    'MTL': {'strength': 70, 'home_adv': 0.65},
                    'DAL': {'strength': 90, 'home_adv': 0.74}
                }
                
                print(f"\n🎯 ANALYSE VALEURS SÛRES (TOP 10):")
                valeurs_sures = []
                
                for match in matchs_saison_reguliere[:50]:  # Analyser les 50 premiers
                    away = match['away_abbr']
                    home = match['home_abbr']
                    
                    away_strength = stats_test.get(away, {'strength': 80, 'home_adv': 0.65})['strength']
                    home_strength = stats_test.get(home, {'strength': 80, 'home_adv': 0.65})['strength']
                    home_adv = stats_test.get(home, {'strength': 80, 'home_adv': 0.65})['home_adv']
                    
                    # Score simple
                    diff_strength = abs(home_strength - away_strength)
                    home_total = home_strength + (home_adv * 20)  # Bonus domicile
                    
                    score = diff_strength + (home_adv * 30)
                    
                    if score >= 15:  # Seuil valeur sûre
                        valeurs_sures.append({
                            'date': match['date'],
                            'match': match['match'],
                            'away_strength': away_strength,
                            'home_strength': home_strength,
                            'home_advantage': home_adv,
                            'score': round(score, 1),
                            'recommended': home if home_total > away_strength else 'EVEN'
                        })
                
                # Trier par score
                valeurs_sures.sort(key=lambda x: x['score'], reverse=True)
                
                for i, v in enumerate(valeurs_sures[:10], 1):
                    print(f"   {i:2d}. {v['date']}: {v['match']}")
                    print(f"       Score: {v['score']} | Recommandé: {v['recommended']}")
                    print(f"       Force: {v['away_strength']} vs {v['home_strength']} (Dom: {v['home_advantage']:.2f})")
                
                print(f"\n✅ {len(valeurs_sures)} valeurs sûres identifiées!")
            
            else:
                print("   ⚠️ Aucun match de saison régulière trouvé")
        
        else:
            print("   ⚠️ Format by_date non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎯 TEST TERMINÉ!")


if __name__ == "__main__":
    tester_calendrier_simple()
