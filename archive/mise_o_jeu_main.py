"""
Script principal pour l'analyse spécialisée Mise-o-jeu+

Point d'entrée optimisé pour analyser les cotes officielles et générer
le plan de mise exact demandé (20$ ouverture + 20$ futures).
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.analyzers.mise_o_jeu_analyzer import analyze_mise_o_jeu_odds
import argparse
import json


def main():
    """
    Analyseur principal Mise-o-jeu+ avec format de sortie spécialisé
    """
    parser = argparse.ArgumentParser(description='Analyseur spécialisé Mise-o-jeu+ LNH 2025-26')
    parser.add_argument('--odds-file', type=str, help='Fichier JSON avec les cotes extraites')
    parser.add_argument('--save-report', action='store_true', help='Sauvegarder le rapport')
    
    args = parser.parse_args()
    
    # Charger les cotes si fichier fourni
    odds_data = {}
    if args.odds_file and os.path.exists(args.odds_file):
        with open(args.odds_file, 'r', encoding='utf-8') as f:
            odds_data = json.load(f)
        print(f"📁 Cotes chargées depuis: {args.odds_file}")
    else:
        print("📊 Utilisation des cotes d'exemple (format Mise-o-jeu+)")
    
    print()
    
    # Effectuer l'analyse complète
    analysis_report = analyze_mise_o_jeu_odds(odds_data)
    
    # Sauvegarder si demandé
    if args.save_report:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_file = f"data/analyse_mise_o_jeu_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 Rapport sauvegardé: {report_file}")
    
    print()
    print("🤖 ANALYSE COMPLÉTÉE - PRÊT POUR COMPÉTITION IA")
    print("=" * 45)
    print("Comparaison possible avec Gemini, Claude, Grok")
    print("Métrique de succès: ROI réel vs prédit à la fin de saison")


def quick_demo():
    """
    Démonstration rapide du système d'analyse
    """
    print("🎯 DÉMONSTRATION ANALYSEUR MISE-O-JEU+")
    print("=" * 45)
    
    # Exécuter l'analyse avec les données d'exemple
    analysis_report = analyze_mise_o_jeu_odds()
    
    print()
    print("✅ Démonstration terminée!")
    print("💡 Pour utiliser avec vos cotes:")
    print("   1. Extraire les cotes du PDF Mise-o-jeu+ en JSON")
    print("   2. Exécuter: python mise_o_jeu_main.py --odds-file cotes.json")
    
    return analysis_report


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Aucun argument = démonstration
        quick_demo()
    else:
        # Arguments fournis = analyse complète
        main()
