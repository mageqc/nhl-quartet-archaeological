"""
Analyseur principal pour les paris LNH 2025-26 sur Mise-o-jeu+

Ce module orchestre l'analyse complète des opportunités de paris
en combinant les données de nouvelles, les cotes et les calculs de valeur.
"""

import argparse
from datetime import datetime
from src.scrapers.news_scraper import NHLNewsScraper
from src.analyzers.value_analyzer import ValueAnalyzer
from src.calculators.odds_calculator import OddsCalculator
from src.calculators.portfolio_manager import PortfolioManager


def main():
    """
    Point d'entrée principal pour l'analyse des paris LNH
    """
    parser = argparse.ArgumentParser(description='Analyseur de paris LNH Mise-o-jeu+')
    parser.add_argument('--budget', type=float, default=20.0, 
                       help='Budget disponible pour les paris (défaut: 20$)')
    parser.add_argument('--strategy', choices=['safe', 'mixed', 'bold'], 
                       default='mixed', help='Stratégie de mise')
    parser.add_argument('--update-news', action='store_true', 
                       help='Mettre à jour les nouvelles avant analyse')
    
    args = parser.parse_args()
    
    print("🏒 ANALYSEUR PARIS LNH 2025-26 - MISE-O-JEU+ 🏒")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"💰 Budget: {args.budget}$")
    print(f"📊 Stratégie: {args.strategy.upper()}")
    print()
    
    # 1. Scraper les nouvelles récentes si demandé
    if args.update_news:
        print("📰 Mise à jour des nouvelles LNH...")
        news_scraper = NHLNewsScraper()
        news_scraper.scrape_recent_news()
        print("✅ Nouvelles mises à jour")
        print()
    
    # 2. Analyser les valeurs
    print("🔍 Analyse des opportunités de value betting...")
    value_analyzer = ValueAnalyzer()
    opportunities = value_analyzer.find_value_bets()
    print(f"✅ {len(opportunities)} opportunités identifiées")
    print()
    
    # 3. Calculer les recommandations de mise
    print("💡 Génération des recommandations...")
    portfolio_manager = PortfolioManager(budget=args.budget, strategy=args.strategy)
    recommendations = portfolio_manager.generate_recommendations(opportunities)
    
    # 4. Afficher les résultats
    print("🎯 RECOMMANDATIONS FINALES")
    print("=" * 30)
    portfolio_manager.display_recommendations(recommendations)
    
    print()
    print("🏆 Bonne chance avec vos paris!")


if __name__ == "__main__":
    main()
