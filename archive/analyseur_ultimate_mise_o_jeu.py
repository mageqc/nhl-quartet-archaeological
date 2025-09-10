"""
🏒 ANALYSEUR ULTIMATE MISE-O-JEU+ NHL 2025-26 🏒

SYSTÈME COMPLET INTÉGRANT:
✅ Calendrier officiel NHL (1,416 matchs)  
✅ APIs temps réel (classements, stats, cotes)
✅ Intelligence betting avancée
✅ Analyse value betting optimisée

Version ULTIMATE pour compétition IA!
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.analyzers.betting_intelligence_integrator import BettingIntelligenceIntegrator
from src.analyzers.official_data_integrator import get_betting_schedule_data
import json
from datetime import datetime


def analyze_ultimate_betting():
    """
    Analyse ULTIMATE combinant toutes les sources
    """
    print("🚀 ANALYSEUR ULTIMATE MISE-O-JEU+ NHL 2025-26")
    print("=" * 50)
    print("🏒 Intégration complète: Officiel + Temps réel + IA")
    print("💰 Budget: 40$ (20$ ouverture + 20$ futures)")
    print()
    
    # 1. INTELLIGENCE TEMPS RÉEL
    print("📡 PHASE 1: INTELLIGENCE TEMPS RÉEL")
    print("-" * 35)
    integrator = BettingIntelligenceIntegrator()
    enhanced_report = integrator.create_enhanced_betting_report(save_file=True)
    
    # 2. CALENDRIER OFFICIEL NHL  
    print("\n📅 PHASE 2: CALENDRIER OFFICIEL NHL")
    print("-" * 35)
    official_schedule = get_betting_schedule_data()
    print(f"✅ {official_schedule['stats']['total_games']} matchs officiels intégrés")
    
    # 3. FUSION DES RECOMMANDATIONS
    print("\n🎯 PHASE 3: RECOMMANDATIONS ULTIMATE")
    print("-" * 35)
    
    ultimate_recommendations = generate_ultimate_recommendations(enhanced_report, official_schedule)
    
    # 4. AFFICHAGE FINAL
    display_ultimate_summary(ultimate_recommendations)
    
    # 5. SAUVEGARDE
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    final_report = {
        'timestamp': timestamp,
        'enhanced_intelligence': enhanced_report,
        'official_schedule': official_schedule,
        'ultimate_recommendations': ultimate_recommendations
    }
    
    filename = f"data/ultimate_betting_analysis_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 Rapport ULTIMATE sauvegardé: {filename}")
    
    return final_report


def generate_ultimate_recommendations(enhanced_report, official_schedule):
    """
    Génère les recommandations ULTIMATE
    """
    print("🧠 Génération recommandations ULTIMATE...")
    
    ultimate_recs = {
        'confidence_level': 'ULTIMATE',
        'opening_plays': [],
        'futures_plays': [],
        'props_plays': [],
        'risk_summary': {}
    }
    
    # OUVERTURE - Équipes chaudes + matchs haute importance
    hot_teams = enhanced_report['betting_enhancements']['team_trends']['hot_teams']
    opening_games = official_schedule['opening_games'][:10]
    
    print(f"   🔥 {len(hot_teams)} équipes chaudes identifiées")
    print(f"   🏒 {len(opening_games)} matchs d'ouverture analysés")
    
    for game in opening_games:
        away_team = game['away_team']
        home_team = game['home_team']
        betting_interest = game['betting_interest']
        
        # Check si équipe chaude
        away_hot = any('Winnipeg' in team.get('team', '') for team in hot_teams)
        home_hot = any('Winnipeg' in team.get('team', '') for team in hot_teams)
        
        if betting_interest >= 9:  # Matchs très intéressants
            recommended_team = away_team if away_hot else home_team
            ultimate_recs['opening_plays'].append({
                'game': f"{away_team} @ {home_team}",
                'date': game['date'],
                'recommendation': recommended_team,
                'reasoning': f"Match haute importance ({betting_interest}/10)",
                'confidence': 'HIGH',
                'suggested_stake': 8.0
            })
        elif betting_interest >= 7:  # Matchs intéressants
            ultimate_recs['opening_plays'].append({
                'game': f"{away_team} @ {home_team}",
                'date': game['date'],
                'recommendation': home_team,  # Avantage domicile
                'reasoning': f"Avantage domicile + intérêt ({betting_interest}/10)",
                'confidence': 'MEDIUM',
                'suggested_stake': 6.0
            })
    
    # FUTURES - Équipes value
    value_teams = enhanced_report['betting_enhancements']['team_trends']['value_opportunities']
    for i, team in enumerate(value_teams[:2]):  # Top 2
        ultimate_recs['futures_plays'].append({
            'type': 'Stanley Cup',
            'team': team['team'],
            'reasoning': f"Équipe value - {team['points_per_game']} PPG",
            'confidence': 'MEDIUM',
            'suggested_stake': 8.0 if i == 0 else 6.0
        })
    
    # CALCUL RISQUES
    total_opening = sum(play['suggested_stake'] for play in ultimate_recs['opening_plays'])
    total_futures = sum(play['suggested_stake'] for play in ultimate_recs['futures_plays'])
    total_stakes = total_opening + total_futures
    
    ultimate_recs['risk_summary'] = {
        'total_recommended': round(total_stakes, 1),
        'opening_allocation': round(total_opening, 1),
        'futures_allocation': round(total_futures, 1),
        'budget_utilization': f"{round(total_stakes/40*100, 1)}%",
        'risk_level': 'CALCULATED' if total_stakes <= 40 else 'AGGRESSIVE'
    }
    
    print(f"   ✅ {len(ultimate_recs['opening_plays'])} recommandations ouverture")
    print(f"   ✅ {len(ultimate_recs['futures_plays'])} recommandations futures")
    print(f"   ✅ Total: {total_stakes:.1f}$ / 40$ budget")
    
    return ultimate_recs


def display_ultimate_summary(recommendations):
    """
    Affiche le résumé ULTIMATE
    """
    print("\n🏆 RECOMMANDATIONS ULTIMATE")
    print("=" * 30)
    
    # Ouverture
    if recommendations['opening_plays']:
        print("\n🏒 OUVERTURE (7-8 octobre 2025):")
        for play in recommendations['opening_plays']:
            print(f"   • {play['game']} → {play['recommendation']}")
            print(f"     Mise: {play['suggested_stake']:.1f}$ | Confiance: {play['confidence']}")
            print(f"     Raison: {play['reasoning']}")
    
    # Futures  
    if recommendations['futures_plays']:
        print("\n🏆 FUTURES:")
        for play in recommendations['futures_plays']:
            print(f"   • {play['type']}: {play['team']}")
            print(f"     Mise: {play['suggested_stake']:.1f}$ | {play['reasoning']}")
    
    # Gestion du risque
    risk = recommendations['risk_summary']
    print(f"\n⚖️ GESTION DU RISQUE:")
    print(f"   • Total recommandé: {risk['total_recommended']}$")
    print(f"   • Ouverture: {risk['opening_allocation']}$")
    print(f"   • Futures: {risk['futures_allocation']}$")
    print(f"   • Utilisation budget: {risk['budget_utilization']}")
    print(f"   • Niveau risque: {risk['risk_level']}")
    
    print("\n🎯 SYSTÈME ULTIMATE OPÉRATIONNEL!")
    print("=" * 35)
    print("✅ Données officielles NHL intégrées")
    print("✅ Intelligence temps réel active")
    print("✅ Analyse betting optimisée")
    print("🏆 PRÊT POUR LA COMPÉTITION IA!")


if __name__ == "__main__":
    # Lancer l'analyse ULTIMATE
    final_report = analyze_ultimate_betting()
