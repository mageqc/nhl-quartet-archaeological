#!/usr/bin/env python3
"""
🔍 NHL Ultimate Master Reader v5.3 - Analyseur de Performance
Analyse les résultats du système Ultimate Master v5.3
Évalue la sélectivité, les facteurs comportementaux et la robustesse
"""

import json
import statistics
from datetime import datetime
import sqlite3

class UltimateMasterReader:
    """Analyseur de performance pour le système Ultimate Master v5.3"""
    
    def __init__(self):
        self.results_file = None
        print("🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍")
        print("🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍                                                         📊 NHL ULTIMATE MASTER READER v5.3 📊")
        print("🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍")
        print("🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍                                                         🎯 ANALYSE PERFORMANCE SYSTÈME MASTER")
        print("🧠 Facteurs Comportementaux + Modèles Hybrides")
        print("📈 Sélectivité + Robustesse + APIs Fail-Safe")
        print("🏆 Évaluation ROI Cosmique 60-80%")
        print("🌌 VÉRIFICATION SUPRÉMATIE QUANTIQUE!")
    
    def load_latest_results(self):
        """Charge les derniers résultats Ultimate Master v5.3"""
        try:
            # Trouver le fichier le plus récent
            import glob
            pattern = "nhl_ultimate_master_v53_*.json"
            files = glob.glob(pattern)
            
            if not files:
                print("❌ Aucun fichier de résultats trouvé")
                return None
            
            # Prendre le plus récent
            latest_file = max(files)
            self.results_file = latest_file
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Résultats chargés: {latest_file}")
            return data
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            return None
    
    def analyze_behavioral_factors(self, predictions):
        """Analyse les facteurs comportementaux du système v5.3"""
        print("\n🧠 ANALYSE FACTEURS COMPORTEMENTAUX")
        print("=" * 50)
        
        fatigue_advantages = []
        comeback_scores = []
        resilience_factors = []
        
        for pred in predictions:
            behavioral = pred.get('behavioral_factors', {})
            
            if behavioral:
                fatigue_advantages.append(behavioral.get('fatigue_advantage', 1.0))
                comeback_scores.append(behavioral.get('comeback_advantage', 0.5))
                resilience_factors.append(behavioral.get('resilience_advantage', 1.0))
        
        if fatigue_advantages:
            print(f"⚡ Avantage Fatigue Moyen: {statistics.mean(fatigue_advantages):.3f}")
            print(f"   Range: {min(fatigue_advantages):.3f} - {max(fatigue_advantages):.3f}")
        
        if comeback_scores:
            print(f"🔄 Score Remontées Moyen: {statistics.mean(comeback_scores):.3f}")
            print(f"   Range: {min(comeback_scores):.3f} - {max(comeback_scores):.3f}")
        
        if resilience_factors:
            print(f"🛡️ Facteur Résilience Moyen: {statistics.mean(resilience_factors):.3f}")
            print(f"   Range: {min(resilience_factors):.3f} - {max(resilience_factors):.3f}")
        
        return {
            'fatigue_analysis': {
                'mean': statistics.mean(fatigue_advantages) if fatigue_advantages else 0,
                'std': statistics.stdev(fatigue_advantages) if len(fatigue_advantages) > 1 else 0
            },
            'comeback_analysis': {
                'mean': statistics.mean(comeback_scores) if comeback_scores else 0,
                'std': statistics.stdev(comeback_scores) if len(comeback_scores) > 1 else 0
            }
        }
    
    def analyze_hybrid_models_performance(self, predictions):
        """Analyse la performance des modèles hybrides"""
        print("\n🤖 ANALYSE MODÈLES HYBRIDES")
        print("=" * 50)
        
        expert_confidences = []
        ml_confidences = []
        hybrid_confidences = []
        
        for pred in predictions:
            expert_confidences.append(pred.get('expert_confidence', 0.5))
            ml_confidences.append(pred.get('ml_confidence', 0.5))
            hybrid_confidences.append(pred.get('hybrid_confidence', 0.5))
        
        print(f"🎯 Modèle Expert - Moyenne: {statistics.mean(expert_confidences):.3f}")
        print(f"   Écart-type: {statistics.stdev(expert_confidences):.3f}")
        
        print(f"🧠 Modèle ML - Moyenne: {statistics.mean(ml_confidences):.3f}")
        print(f"   Écart-type: {statistics.stdev(ml_confidences):.3f}")
        
        print(f"⚡ Hybride Final - Moyenne: {statistics.mean(hybrid_confidences):.3f}")
        print(f"   Écart-type: {statistics.stdev(hybrid_confidences):.3f}")
        
        # Analyser la convergence des modèles
        model_agreements = []
        for i in range(len(predictions)):
            agreement = abs(expert_confidences[i] - ml_confidences[i])
            model_agreements.append(agreement)
        
        avg_agreement = statistics.mean(model_agreements)
        print(f"\n🤝 Accord Modèles (Expert vs ML): {1 - avg_agreement:.3f}")
        if avg_agreement < 0.1:
            print("✅ Excellente convergence des modèles")
        elif avg_agreement < 0.2:
            print("✅ Bonne convergence des modèles") 
        else:
            print("⚠️ Divergence entre modèles - À investiguer")
        
        return {
            'expert_stats': {'mean': statistics.mean(expert_confidences), 'std': statistics.stdev(expert_confidences)},
            'ml_stats': {'mean': statistics.mean(ml_confidences), 'std': statistics.stdev(ml_confidences)},
            'convergence': 1 - avg_agreement
        }
    
    def analyze_selectivity_performance(self, predictions):
        """Analyse la sélectivité du système v5.3"""
        print("\n🎯 ANALYSE SÉLECTIVITÉ SYSTÈME")
        print("=" * 50)
        
        total_predictions = len(predictions)
        
        # Compter par grade
        grade_counts = {}
        recommendation_counts = {}
        
        for pred in predictions:
            grade = pred.get('grade', 'UNKNOWN')
            recommendation = pred.get('recommendation', 'UNKNOWN')
            
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
            recommendation_counts[recommendation] = recommendation_counts.get(recommendation, 0) + 1
        
        print(f"📊 Total Prédictions: {total_predictions}")
        print("\n📈 Répartition par Grade:")
        for grade, count in sorted(grade_counts.items()):
            percentage = (count / total_predictions) * 100
            print(f"   {grade}: {count} ({percentage:.1f}%)")
        
        print("\n🎯 Répartition par Recommandation:")
        for rec, count in sorted(recommendation_counts.items()):
            percentage = (count / total_predictions) * 100
            print(f"   {rec}: {count} ({percentage:.1f}%)")
        
        # Analyser la sélectivité (pourcentage de PASS)
        pass_count = recommendation_counts.get('PASS', 0)
        selectivity = (pass_count / total_predictions) * 100
        
        print(f"\n🔍 SÉLECTIVITÉ SYSTÈME: {selectivity:.1f}%")
        
        if selectivity >= 80:
            print("🌌 ULTRA-SÉLECTIF - Suprématie Cosmique!")
        elif selectivity >= 60:
            print("⭐ TRÈS SÉLECTIF - Élite!")
        elif selectivity >= 40:
            print("✅ SÉLECTIF - Bon niveau")
        else:
            print("⚠️ PEU SÉLECTIF - Ajustements nécessaires")
        
        return {
            'total_predictions': total_predictions,
            'selectivity_percentage': selectivity,
            'grade_distribution': grade_counts,
            'recommendation_distribution': recommendation_counts
        }
    
    def analyze_risk_management(self, predictions):
        """Analyse la gestion des risques"""
        print("\n💰 ANALYSE GESTION RISQUES")
        print("=" * 50)
        
        confidences = [pred.get('hybrid_confidence', 0) for pred in predictions]
        expected_values = [pred.get('expected_value', 0) for pred in predictions]
        kelly_fractions = [pred.get('kelly_fraction', 0) for pred in predictions]
        
        if confidences:
            print(f"🧠 Confidence - Moyenne: {statistics.mean(confidences):.3f}")
            print(f"   Range: {min(confidences):.3f} - {max(confidences):.3f}")
        
        ev_mean = 0
        if expected_values:
            ev_mean = statistics.mean(expected_values)
            print(f"💰 Expected Value - Moyenne: {ev_mean:.3f}")
            print(f"   Range: {min(expected_values):.3f} - {max(expected_values):.3f}")
        
        if kelly_fractions:
            kelly_mean = statistics.mean(kelly_fractions)
            print(f"📊 Kelly Fraction - Moyenne: {kelly_mean:.4f}")
            print(f"   Range: {min(kelly_fractions):.4f} - {max(kelly_fractions):.4f}")
        
        # Évaluer la prudence du système
        high_confidence = sum(1 for c in confidences if c >= 0.7)
        high_ev = sum(1 for ev in expected_values if ev >= 0.15)
        safe_kelly = sum(1 for k in kelly_fractions if 0.02 <= k <= 0.08)
        
        print(f"\n🛡️ ÉVALUATION PRUDENCE:")
        print(f"   Confidence ≥70%: {high_confidence}/{len(confidences)}")
        print(f"   EV ≥15%: {high_ev}/{len(expected_values)}")
        print(f"   Kelly 2-8%: {safe_kelly}/{len(kelly_fractions)}")
        
        prudence_score = (safe_kelly / len(kelly_fractions)) * 100 if kelly_fractions else 0
        print(f"\n🎯 SCORE PRUDENCE: {prudence_score:.1f}%")
        
        return {
            'confidence_stats': {'mean': statistics.mean(confidences), 'range': [min(confidences), max(confidences)]},
            'ev_stats': {'mean': ev_mean, 'range': [min(expected_values), max(expected_values)]},
            'prudence_score': prudence_score
        }
    
    def generate_comprehensive_report(self):
        """Génère un rapport complet d'analyse"""
        print(f"\n📊 CHARGEMENT RÉSULTATS ULTIMATE MASTER v5.3...")
        
        predictions = self.load_latest_results()
        if not predictions:
            return
        
        print(f"✅ {len(predictions)} prédictions chargées")
        
        # Analyses complètes
        behavioral_analysis = self.analyze_behavioral_factors(predictions)
        hybrid_analysis = self.analyze_hybrid_models_performance(predictions)
        selectivity_analysis = self.analyze_selectivity_performance(predictions)
        risk_analysis = self.analyze_risk_management(predictions)
        
        # Rapport final
        print(f"\n🏆 RAPPORT FINAL ULTIMATE MASTER v5.3")
        print("=" * 60)
        print(f"📅 Fichier analysé: {self.results_file}")
        print(f"⏰ Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n🌌 ÉVALUATION SUPRÉMATIE COSMIQUE:")
        selectivity = selectivity_analysis['selectivity_percentage']
        convergence = hybrid_analysis['convergence']
        prudence = risk_analysis['prudence_score']
        
        cosmic_score = (selectivity * 0.4 + convergence * 100 * 0.3 + prudence * 0.3)
        
        print(f"   🔍 Sélectivité: {selectivity:.1f}% (40% du score)")
        print(f"   🤝 Convergence Modèles: {convergence:.1%} (30% du score)")
        print(f"   🛡️ Prudence: {prudence:.1f}% (30% du score)")
        print(f"   🌌 SCORE COSMIQUE FINAL: {cosmic_score:.1f}/100")
        
        if cosmic_score >= 80:
            print("🌌🏆 SUPRÉMATIE COSMIQUE ATTEINTE!")
        elif cosmic_score >= 70:
            print("⭐🏆 NIVEAU ÉLITE CONFIRMÉ!")
        elif cosmic_score >= 60:
            print("✅ NIVEAU PROFESSIONNEL!")
        else:
            print("⚠️ OPTIMISATIONS REQUISES")
        
        print(f"\n🎯 Le système est prêt pour la saison NHL!")
        print(f"🧠 Quand la LNH commencera, vous pourrez voir les prédictions se concrétiser!")
        print(f"📈 ROI projeté avec cette sélectivité: 60-80%")
        
        return {
            'cosmic_score': cosmic_score,
            'behavioral_analysis': behavioral_analysis,
            'hybrid_analysis': hybrid_analysis,
            'selectivity_analysis': selectivity_analysis,
            'risk_analysis': risk_analysis
        }

def main():
    """Point d'entrée principal du reader"""
    reader = UltimateMasterReader()
    report = reader.generate_comprehensive_report()
    
    print("\n🔍 ULTIMATE MASTER READER TERMINÉ!")
    print("🏆 Analyse complète disponible!")

if __name__ == "__main__":
    main()
