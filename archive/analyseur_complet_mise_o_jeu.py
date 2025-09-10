"""
ANALYSEUR COMPLET MISE-O-JEU+ avec CALENDRIER OFFICIEL NHL

Script final qui combine:
- Calendrier officiel NHL (1416 matchs)
- Analyse value betting
- Plan de mise optimisé (20$ ouverture + 20$ futures)
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.analyzers.mise_o_jeu_analyzer import analyze_mise_o_jeu_odds
from src.analyzers.official_data_integrator import get_betting_schedule_data
import argparse
import json
from datetime import datetime


def main():
    """
    Analyseur COMPLET avec données officielles NHL
    """
    parser = argparse.ArgumentParser(description='Analyseur COMPLET Mise-o-jeu+ NHL 2025-26')
    parser.add_argument('--odds-file', type=str, help='Fichier JSON avec les cotes extraites')
    parser.add_argument('--save-report', action='store_true', help='Sauvegarder le rapport')
    parser.add_argument('--show-official-schedule', action='store_true', help='Afficher calendrier officiel')
    
    args = parser.parse_args()
    
    print("🏒 ANALYSEUR COMPLET MISE-O-JEU+ NHL 2025-26")
    print("=" * 55)
    print("📊 Calendrier officiel + Analyse value betting")
    print("💰 Plan de mise: 20$ ouverture + 20$ futures")
    print()
    
    # 1. CALENDRIER OFFICIEL
    print("📡 Chargement données officielles NHL...")
    betting_data = get_betting_schedule_data()
    
    print(f"✅ {betting_data['stats']['total_games']} matchs officiels chargés")
    print(f"🎯 {len(betting_data['opening_games'])} matchs d'ouverture identifiés")
    print()
    
    if args.show_official_schedule:
        print("🏒 TOP MATCHS D'OUVERTURE OFFICIELS:")
        print("-" * 40)
        for i, game in enumerate(betting_data['opening_games'][:10], 1):
            rivalry = "🥊" if game['rivalry_level'] == 'INTENSE' else ("⚔️" if game['rivalry_level'] == 'MODERATE' else "🏒")
            print(f"{i:2d}. {rivalry} {game['date']} - {game['away_team']} @ {game['home_team']}")
            print(f"     Intérêt: {game['betting_interest']}/10 | {game['venue']}")
        print()
    
    # 2. ANALYSE COTES MISE-O-JEU+
    print("🎯 ANALYSE COTES MISE-O-JEU+")
    print("-" * 30)
    
    # Charger les cotes si fichier fourni
    odds_data = {}
    if args.odds_file and os.path.exists(args.odds_file):
        with open(args.odds_file, 'r', encoding='utf-8') as f:
            odds_data = json.load(f)
        print(f"📁 Cotes chargées depuis: {args.odds_file}")
    else:
        print("📊 Utilisation des cotes d'exemple")
    
    # Enrichir les cotes avec les données officielles
    enriched_odds = enrich_odds_with_official_data(odds_data, betting_data)
    
    # Effectuer l'analyse complète
    analysis_report = analyze_mise_o_jeu_odds(enriched_odds)
    
    # 3. RECOMMANDATIONS FINALES
    print("\n🎯 RECOMMANDATIONS ENRICHIES")
    print("=" * 35)
    
    # Ajouter contexte des matchs officiels
    add_official_context_to_recommendations(analysis_report, betting_data)
    
    # Sauvegarder si demandé
    if args.save_report:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_file = f"data/analyse_complete_mise_o_jeu_{timestamp}.json"
        
        complete_report = {
            'analysis': analysis_report,
            'official_data': betting_data['stats'],
            'opening_games': betting_data['opening_games'][:20]  # Top 20
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(complete_report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 Rapport complet sauvegardé: {report_file}")
    
    print("\n🏆 ANALYSE COMPLÈTE TERMINÉE!")
    print("=" * 35)
    print("✅ Calendrier officiel NHL intégré")
    print("✅ Analyse value betting effectuée")
    print("✅ Plan de mise optimisé généré")
    print("🤖 Prêt pour la compétition IA!")


def enrich_odds_with_official_data(odds_data: dict, betting_data: dict) -> dict:
    """
    Enrichit les cotes avec les données officielles
    """
    enriched = odds_data.copy() if odds_data else {}
    
    # Ajouter les matchs d'ouverture officiels
    if 'opening_games' not in enriched:
        enriched['opening_games'] = {}
    
    # Convertir les matchs officiels en format cotes
    for game in betting_data['opening_games'][:10]:  # Top 10 matchs d'ouverture
        game_key = f"{game['away_team']} @ {game['home_team']} ({game['date'][:5]})"
        
        # Générer des cotes réalistes basées sur l'intérêt
        if game['betting_interest'] >= 8:
            # Matchs très intéressants = cotes plus serrées
            away_odds = 2.10
            home_odds = 1.75
        elif game['betting_interest'] >= 6:
            # Matchs moyennement intéressants
            away_odds = 2.30
            home_odds = 1.65
        else:
            # Autres matchs
            away_odds = 2.50
            home_odds = 1.60
        
        # Format correct attendu par l'analyseur
        enriched['opening_games'][game_key] = {
            game['away_team']: away_odds,
            game['home_team']: home_odds,
            'market': 'Vainqueur du match'
        }
        
        # Stocker les données officielles séparément pour référence
        if 'official_context' not in enriched:
            enriched['official_context'] = {}
        
        enriched['official_context'][game_key] = {
            'venue': game['venue'],
            'betting_interest': game['betting_interest'],
            'rivalry_level': game['rivalry_level'],
            'market_importance': game['market_importance']
        }
    
    return enriched


def add_official_context_to_recommendations(analysis_report: dict, betting_data: dict):
    """
    Ajoute le contexte officiel aux recommandations
    """
    print("📈 CONTEXTE OFFICIEL AJOUTÉ:")
    
    # Matchs d'ouverture recommandés
    opening_plan = analysis_report.get('opening_plan', {})
    if opening_plan.get('bets'):
        print("\n🏒 MATCHS D'OUVERTURE (avec données officielles):")
        for bet in opening_plan['bets']:
            # Trouver le match correspondant dans les données officielles
            for official_game in betting_data['opening_games']:
                game_teams = f"{official_game['away_team']} @ {official_game['home_team']}"
                if (bet['selection'] in official_game['away_team'] or 
                    bet['selection'] in official_game['home_team'] or
                    bet['selection'] in game_teams):
                    
                    rivalry = "🥊" if official_game['rivalry_level'] == 'INTENSE' else "⚔️" if official_game['rivalry_level'] == 'MODERATE' else "🏒"
                    print(f"   {rivalry} {bet['market']}: {bet['selection']}")
                    print(f"      Cote: {bet['odds']:.2f} | Mise: {bet['stake']:.2f}$")
                    print(f"      Venue: {official_game['venue']}")
                    print(f"      Intérêt officiel: {official_game['betting_interest']}/10")
                    break
    
    # Statistiques enrichies
    stats = betting_data['stats']
    print(f"\n📊 DONNÉES OFFICIELLES INTÉGRÉES:")
    print(f"   • Total matchs saison: {stats['total_games']}")
    print(f"   • Matchs saison régulière: {stats['by_type']['regular']}")
    print(f"   • Période: {stats['date_range']['start']} → {stats['date_range']['end']}")
    print(f"   • Top matchs d'ouverture analysés: {len(betting_data['opening_games'])}")

def quick_demo():
    """
    Démonstration rapide du système complet
    """
    print("🎯 DÉMONSTRATION ANALYSEUR COMPLET")
    print("=" * 40)
    
    # Données officielles
    betting_data = get_betting_schedule_data()
    print(f"✅ {betting_data['stats']['total_games']} matchs officiels chargés")
    
    # Analyse avec données enrichies
    enriched_odds = enrich_odds_with_official_data({}, betting_data)
    analysis_report = analyze_mise_o_jeu_odds(enriched_odds)
    
    print(f"✅ Analyse terminée - {len(betting_data['opening_games'])} matchs d'ouverture analysés")
    
    return {'analysis': analysis_report, 'official_data': betting_data}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Aucun argument = démonstration
        quick_demo()
    else:
        # Arguments fournis = analyse complète
        main()
