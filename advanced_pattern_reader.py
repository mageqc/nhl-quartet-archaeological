#!/usr/bin/env python3
"""
🧠🏒 LECTEUR PATTERNS AVANCÉS - NHL v5.0
========================================

Script spécialisé pour analyser les patterns furieux du système NHL v5.0.
Affiche momentum, fatigue, rivalités, clutch situations, et blessures.

Usage:
    python3 advanced_pattern_reader.py [fichier.json]
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

class AdvancedPatternReader:
    """Lecteur spécialisé pour patterns furieux NHL v5.0"""
    
    def __init__(self):
        self.pattern_emojis = {
            'momentum': '📊', 'fatigue': '😴', 'rivalry': '🔥',
            'clutch': '⚡', 'injury': '🏥', 'furious': '🧠'
        }
        
    def find_latest_pattern_file(self) -> Optional[str]:
        """Trouve le dernier fichier patterns généré"""
        try:
            pattern_files = [f for f in os.listdir('.') if f.startswith('nhl_advanced_patterns_v5_') and f.endswith('.json')]
            if not pattern_files:
                return None
            return max(pattern_files, key=lambda x: os.path.getctime(x))
        except:
            return None
    
    def load_pattern_data(self, filename: str) -> Optional[Dict]:
        """Charge les données patterns"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture {filename}: {e}")
            return None
    
    def display_pattern_header(self, pattern_data: Dict):
        """Affiche header système patterns"""
        system_info = pattern_data.get('system_info', {})
        
        print("🧠" * 80)
        print("🏒 NHL ADVANCED PATTERN ANALYZER v5.0 - ANALYSE PATTERNS FURIEUX 🏒")
        print("🧠" * 80)
        
        print(f"📊 Version: {system_info.get('version', 'v5.0')}")
        print(f"⏰ Généré: {system_info.get('generation_timestamp', 'N/A')}")
        print(f"🔥 Patterns furieux: {'✅ ACTIVÉ' if system_info.get('furious_patterns_enabled') else '❌ DÉSACTIVÉ'}")
    
    def display_pattern_summary(self, pattern_data: Dict):
        """Affiche résumé patterns"""
        summary = pattern_data.get('pattern_summary', {})
        
        print(f"\\n🎯 RÉSUMÉ PATTERNS FURIEUX:")
        print("=" * 50)
        print(f"📊 Matchs analysés: {summary.get('total_games_analyzed', 0)}")
        print(f"🔥 Patterns furieux détectés: {summary.get('furious_patterns_detected', 0)}")
        
        if summary.get('total_games_analyzed', 0) > 0:
            furious_rate = (summary.get('furious_patterns_detected', 0) / summary.get('total_games_analyzed', 1)) * 100
            print(f"📈 Taux patterns furieux: {furious_rate:.1f}%")
        
        print(f"⭐ Qualité moyenne: {summary.get('average_quality_score', 0):.3f}")
        print(f"📈 Boost confidence moyen: {summary.get('average_confidence_boost', 0):.3f}")
    
    def display_momentum_analysis(self, momentum_data: Dict, team_name: str):
        """Affiche analyse momentum détaillée"""
        home = momentum_data.get('home', {})
        away = momentum_data.get('away', {})
        diff = momentum_data.get('differential', 0)
        
        print(f"    📊 MOMENTUM ANALYSIS:")
        print(f"       🏠 Domicile: {home.get('momentum_score', 0):.3f} ({home.get('trend', 'N/A')})")
        print(f"          • Win%: {home.get('win_percentage', 0):.1%}")
        print(f"          • Goal Diff: {home.get('goal_differential', 0):+d}")
        print(f"       ✈️  Visiteur: {away.get('momentum_score', 0):.3f} ({away.get('trend', 'N/A')})")
        print(f"          • Win%: {away.get('win_percentage', 0):.1%}")
        print(f"          • Goal Diff: {away.get('goal_differential', 0):+d}")
        print(f"       ⚖️  Différentiel: {diff:+.3f}")
    
    def display_fatigue_analysis(self, fatigue_data: Dict):
        """Affiche analyse fatigue détaillée"""
        home = fatigue_data.get('home', {})
        away = fatigue_data.get('away', {})
        diff = fatigue_data.get('differential', 0)
        
        print(f"    😴 FATIGUE ANALYSIS:")
        print(f"       🏠 Domicile: {home.get('fatigue_score', 0):.3f}")
        print(f"          • B2B: {'✅' if home.get('b2b_detected') else '❌'}")
        print(f"          • Voyage: {home.get('travel_hours', 0)}h")
        print(f"          • Intensité: {home.get('schedule_intensity', 0)} matchs/5j")
        print(f"       ✈️  Visiteur: {away.get('fatigue_score', 0):.3f}")
        print(f"          • B2B: {'✅' if away.get('b2b_detected') else '❌'}")
        print(f"          • Voyage: {away.get('travel_hours', 0)}h")
        print(f"          • Intensité: {away.get('schedule_intensity', 0)} matchs/5j")
        print(f"       ⚖️  Avantage: {diff:+.3f}")
    
    def display_rivalry_analysis(self, rivalry_data: Dict):
        """Affiche analyse rivalité"""
        if rivalry_data.get('rivalry_detected'):
            print(f"    🔥 RIVALITÉ DÉTECTÉE!")
            print(f"       • Catégorie: {rivalry_data.get('category', 'N/A')}")
            print(f"       • Intensité: {rivalry_data.get('intensity', 0):.1%}")
            print(f"       • Facteur historique: {rivalry_data.get('historical_factor', 0):.1%}")
            print(f"       • Boost: +{rivalry_data.get('boost_factor', 0):.3f}")
        else:
            print(f"    🔥 Rivalité: Aucune détectée")
    
    def display_clutch_analysis(self, clutch_data: Dict):
        """Affiche analyse clutch"""
        if clutch_data.get('clutch_situation_detected'):
            print(f"    ⚡ SITUATION CLUTCH DÉTECTÉE!")
            factors = clutch_data.get('clutch_factors', [])
            print(f"       • Facteurs: {', '.join(factors) if factors else 'N/A'}")
            print(f"       • Boost total: +{clutch_data.get('total_clutch_boost', 0):.3f}")
            print(f"       • Rating clutch domicile: {clutch_data.get('home_clutch_rating', 0):.2f}")
            print(f"       • Rating clutch visiteur: {clutch_data.get('away_clutch_rating', 0):.2f}")
        else:
            print(f"    ⚡ Clutch: Situation normale")
    
    def display_injury_analysis(self, injury_data: Dict):
        """Affiche analyse blessures"""
        home = injury_data.get('home', {})
        away = injury_data.get('away', {})
        diff = injury_data.get('differential', 0)
        
        print(f"    🏥 INJURY ANALYSIS:")
        print(f"       🏠 Domicile: Impact {home.get('injury_impact', 0):.3f} ({home.get('severity', 'none')})")
        print(f"          • Joueurs clés out: {home.get('key_players_out', 0)}")
        print(f"          • Positions: {', '.join(home.get('positions_affected', [])[:2]) if home.get('positions_affected') else 'Aucune'}")
        print(f"       ✈️  Visiteur: Impact {away.get('injury_impact', 0):.3f} ({away.get('severity', 'none')})")
        print(f"          • Joueurs clés out: {away.get('key_players_out', 0)}")
        print(f"          • Positions: {', '.join(away.get('positions_affected', [])[:2]) if away.get('positions_affected') else 'Aucune'}")
        print(f"       ⚖️  Avantage: {diff:+.3f}")
    
    def display_detailed_analyses(self, pattern_data: Dict):
        """Affiche analyses détaillées pour chaque match"""
        analyses = pattern_data.get('detailed_analyses', [])
        
        if not analyses:
            print("\\n❌ Aucune analyse détaillée trouvée")
            return
        
        print(f"\\n🧠 ANALYSES PATTERNS DÉTAILLÉES:")
        print("=" * 80)
        
        for i, analysis in enumerate(analyses, 1):
            home_team = analysis.get('home_team', 'N/A')
            away_team = analysis.get('away_team', 'N/A')
            game_date = analysis.get('game_date', 'N/A')
            
            # Header match
            print(f"\\n🏒 MATCH {i}: {away_team} @ {home_team} ({game_date})")
            print("-" * 60)
            
            # Résultats patterns
            base_conf = analysis.get('base_confidence', 0)
            adj_conf = analysis.get('adjusted_confidence', 0)
            conf_adj = analysis.get('confidence_adjustment', 0)
            ev_adj = analysis.get('ev_adjustment', 0)
            
            print(f"📊 Confidence: {base_conf:.3f} → {adj_conf:.3f} ({conf_adj:+.3f})")
            print(f"💰 EV ajustement: {ev_adj:+.3f}")
            
            # Pattern furieux
            furious = analysis.get('furious_pattern_detected', False)
            quality = analysis.get('pattern_quality_score', 0)
            factors = analysis.get('pattern_factors', [])
            
            status_emoji = "🔥" if furious else "🔘"
            print(f"{status_emoji} Pattern furieux: {'OUI' if furious else 'Non'} (Qualité: {quality:.2f})")
            if factors:
                print(f"🎯 Facteurs: {', '.join(factors[:3])}{'...' if len(factors) > 3 else ''}")
            
            # Analyses détaillées
            self.display_momentum_analysis(analysis.get('momentum_analysis', {}), home_team)
            self.display_fatigue_analysis(analysis.get('fatigue_analysis', {}))
            self.display_rivalry_analysis(analysis.get('rivalry_analysis', {}))
            self.display_clutch_analysis(analysis.get('clutch_analysis', {}))
            self.display_injury_analysis(analysis.get('injury_analysis', {}))
    
    def display_top_patterns(self, pattern_data: Dict):
        """Affiche le top des patterns furieux"""
        analyses = pattern_data.get('detailed_analyses', [])
        furious_patterns = [a for a in analyses if a.get('furious_pattern_detected', False)]
        
        if not furious_patterns:
            print("\\n🔘 Aucun pattern furieux détecté")
            return
        
        print(f"\\n🏆 TOP PATTERNS FURIEUX:")
        print("=" * 50)
        
        # Trier par qualité
        top_patterns = sorted(furious_patterns, key=lambda x: x.get('pattern_quality_score', 0), reverse=True)
        
        for i, pattern in enumerate(top_patterns[:5], 1):
            home = pattern.get('home_team', 'N/A')
            away = pattern.get('away_team', 'N/A')
            quality = pattern.get('pattern_quality_score', 0)
            conf_adj = pattern.get('confidence_adjustment', 0)
            factors = len(pattern.get('pattern_factors', []))
            
            print(f"  {i}. 🔥 {away} @ {home}")
            print(f"     • Qualité: {quality:.2f} | Confidence: {conf_adj:+.3f} | Facteurs: {factors}")
    
    def display_pattern_statistics(self, pattern_data: Dict):
        """Affiche statistiques patterns"""
        analyses = pattern_data.get('detailed_analyses', [])
        
        if not analyses:
            return
        
        print(f"\\n📈 STATISTIQUES PATTERNS:")
        print("=" * 40)
        
        # Compteurs par type
        momentum_patterns = sum(1 for a in analyses if 'momentum' in ' '.join(a.get('pattern_factors', [])))
        fatigue_patterns = sum(1 for a in analyses if 'fatigue' in ' '.join(a.get('pattern_factors', [])))
        rivalry_patterns = sum(1 for a in analyses if a.get('rivalry_analysis', {}).get('rivalry_detected', False))
        clutch_patterns = sum(1 for a in analyses if a.get('clutch_analysis', {}).get('clutch_situation_detected', False))
        injury_patterns = sum(1 for a in analyses if 'injury' in ' '.join(a.get('pattern_factors', [])))
        
        print(f"📊 Momentum: {momentum_patterns}/{len(analyses)} ({momentum_patterns/len(analyses)*100:.1f}%)")
        print(f"😴 Fatigue: {fatigue_patterns}/{len(analyses)} ({fatigue_patterns/len(analyses)*100:.1f}%)")
        print(f"🔥 Rivalités: {rivalry_patterns}/{len(analyses)} ({rivalry_patterns/len(analyses)*100:.1f}%)")
        print(f"⚡ Clutch: {clutch_patterns}/{len(analyses)} ({clutch_patterns/len(analyses)*100:.1f}%)")
        print(f"🏥 Blessures: {injury_patterns}/{len(analyses)} ({injury_patterns/len(analyses)*100:.1f}%)")
        
        # Moyennes
        avg_confidence_adj = sum(abs(a.get('confidence_adjustment', 0)) for a in analyses) / len(analyses)
        avg_quality = sum(a.get('pattern_quality_score', 0) for a in analyses) / len(analyses)
        
        print(f"\\n📊 Moyennes:")
        print(f"• Ajustement confidence: ±{avg_confidence_adj:.3f}")
        print(f"• Qualité pattern: {avg_quality:.2f}/1.00")
    
    def display_pattern_analysis(self, pattern_data: Dict):
        """Affiche analyse complète patterns"""
        self.display_pattern_header(pattern_data)
        self.display_pattern_summary(pattern_data)
        self.display_detailed_analyses(pattern_data)
        self.display_top_patterns(pattern_data)
        self.display_pattern_statistics(pattern_data)
        
        print("\\n🧠" * 80)
        print("🏆 ANALYSE PATTERNS FURIEUX COMPLÉTÉE! Fun transcendant niveau 15/10! 🧠🔥⭐")
        print("🧠" * 80)

def main():
    """Fonction principale"""
    reader = AdvancedPatternReader()
    
    # Déterminer fichier à analyser
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = reader.find_latest_pattern_file()
        if filename:
            print(f"🔍 Fichier auto-détecté: {filename}")
        else:
            print("❌ Aucun fichier patterns trouvé!")
            print("💡 Usage: python3 advanced_pattern_reader.py [fichier.json]")
            return
    
    # Charger et analyser
    if not os.path.exists(filename):
        print(f"❌ Fichier non trouvé: {filename}")
        return
    
    print(f"📖 Lecture patterns: {filename}")
    pattern_data = reader.load_pattern_data(filename)
    
    if not pattern_data:
        print(f"❌ Erreur lecture fichier patterns")
        return
    
    # Affichage
    reader.display_pattern_analysis(pattern_data)

if __name__ == "__main__":
    main()
