#!/usr/bin/env python3
"""
🔮📊 GROK HYBRID ML + CALIBRATION - Implémentation Random Forest + Genetic
Cible: Accuracy 80% (vs 73.2%), Brier <0.18, ROI +20-30%
"""

import json
import math
import random
from datetime import datetime, timedelta

class GrokHybridML:
    """🔮 ML hybride selon suggestions Grok (RF + Genetic)"""
    
    def __init__(self):
        # Weights génétiques optimisés (simulation avancée)
        self.genetic_weights = {
            'xG_differential': 0.25,
            'pdo_trend': 0.20,
            'b2b_fatigue': 0.15,
            'home_advantage': 0.10,
            'rivalry_boost': 0.12,
            'rookie_variance': 0.08,
            'sentiment_hype': 0.10
        }
        
        # Historique Brier pour calibration (suggestion Grok)
        self.brier_history = []
        self.calibration_target = 0.18  # <0.18 selon Grok
        
        # Facteurs rookies (variance 40% vs 15% vétérans)
        self.rookie_factors = {
            'MTL': {
                'demidov': {'variance': 0.42, 'upside': 0.15, 'pp_boost': 0.08},
                'hutson': {'variance': 0.38, 'upside': 0.12, 'defensive_risk': -0.05}
            }
        }
    
    def simulate_random_forest_prediction(self, features):
        """🌲 Simulation Random Forest (pour rookies avec variance 40%)"""
        # Features standardisées
        xg_diff = features.get('xg_differential', 0.0)
        pdo = features.get('pdo', 1.0)
        b2b = features.get('back_to_back', False)
        home = features.get('home_advantage', True)
        rivalry = features.get('rivalry', False)
        rookie_impact = features.get('rookie_factor', 0.0)
        
        # Calcul probabilité base (simulation RF avec 100 trees)
        base_prob = 0.5
        
        # Ajustements selon features
        base_prob += xg_diff * 0.12  # xG impact fort
        base_prob += (pdo - 1.0) * 0.08  # PDO régression
        base_prob -= 0.04 if b2b else 0.0  # Fatigue B2B
        base_prob += 0.03 if home else -0.03  # Home ice
        base_prob += 0.05 if rivalry else 0.0  # Rivalry boost
        
        # Variance rookies (40% selon Grok)
        if rookie_impact > 0:
            rookie_variance = random.uniform(-0.2, 0.2) * rookie_impact
            base_prob += rookie_variance
        
        # Contraintes 10%-90%
        return min(max(base_prob, 0.1), 0.9)
    
    def genetic_optimization(self, rf_prob, features, sentiment_boost=0.0):
        """🧬 Optimisation génétique selon suggestions Grok"""
        
        # Combinaison RF + genetic weights
        optimized_prob = rf_prob * 0.6  # 60% RF selon Grok
        
        # Ajustements génétiques
        for feature, weight in self.genetic_weights.items():
            feature_value = features.get(feature.replace('_', ''), 0.0)
            if isinstance(feature_value, bool):
                feature_value = 1.0 if feature_value else 0.0
            optimized_prob += feature_value * weight * 0.4  # 40% genetic
        
        # Boost sentiment (suggestion #1 Grok)
        optimized_prob += sentiment_boost
        
        return min(max(optimized_prob, 0.1), 0.9)
    
    def calculate_brier_score(self, predictions, outcomes):
        """📊 Calcul Brier score pour calibration"""
        if not predictions or not outcomes:
            return 0.5
        
        brier_sum = sum((pred - outcome) ** 2 for pred, outcome in zip(predictions, outcomes))
        return brier_sum / len(predictions)
    
    def nightly_calibration(self, recent_predictions, recent_outcomes):
        """🌙 Job nightly calibration (suggestion ChatGPT/Grok)"""
        
        # Calcul Brier récent
        current_brier = self.calculate_brier_score(recent_predictions, recent_outcomes)
        self.brier_history.append({
            'date': datetime.now().isoformat(),
            'brier_score': current_brier,
            'n_predictions': len(recent_predictions)
        })
        
        # Ajustement si Brier > 0.18
        calibration_needed = current_brier > self.calibration_target
        
        if calibration_needed:
            # Réduction genetic weights si overconfident
            for key in self.genetic_weights:
                self.genetic_weights[key] *= 0.95  # Réduction 5%
        
        return {
            'brier_score': current_brier,
            'calibration_target': self.calibration_target,
            'adjustment_made': calibration_needed,
            'status': 'WELL_CALIBRATED' if current_brier <= self.calibration_target else 'NEEDS_ADJUSTMENT'
        }
    
    def grok_hybrid_predict(self, team_features, opponent_features, game_context):
        """🚀 Prédiction hybride complète (RF + Genetic + Calibration)"""
        
        # Features combinées
        combined_features = {
            'xg_differential': team_features.get('xG', 2.5) - opponent_features.get('xG', 2.5),
            'pdo': team_features.get('PDO', 1.0),
            'back_to_back': game_context.get('b2b', False),
            'home_advantage': game_context.get('home', True),
            'rivalry': game_context.get('rivalry', False),
            'rookie_factor': team_features.get('rookie_impact', 0.0),
            'sentiment_hype': game_context.get('sentiment_boost', 0.0)
        }
        
        # 1. Random Forest prediction
        rf_prob = self.simulate_random_forest_prediction(combined_features)
        
        # 2. Genetic optimization  
        genetic_prob = self.genetic_optimization(
            rf_prob, 
            combined_features, 
            combined_features['sentiment_hype']
        )
        
        # 3. Calibration adjustment (si historique disponible)
        if self.brier_history:
            recent_brier = self.brier_history[-1]['brier_score']
            if recent_brier > self.calibration_target:
                genetic_prob *= 0.95  # Réduction confiance si mal calibré
        
        return {
            'rf_probability': rf_prob,
            'genetic_probability': genetic_prob, 
            'final_probability': genetic_prob,
            'brier_adjusted': len(self.brier_history) > 0,
            'confidence': 1.0 - (abs(genetic_prob - 0.5) * 0.5)  # Confiance basée distance 50%
        }

def demo_grok_hybrid_ml():
    """🎯 DEMO Hybrid ML selon suggestions Grok"""
    print("🔮🧬 GROK HYBRID ML - RF + GENETIC + CALIBRATION !\n")
    
    ml_engine = GrokHybridML()
    
    # Test scenarios présaison MTL (selon analyse Grok)
    test_games = [
        {
            'matchup': 'MTL vs PIT (22 sept)',
            'team_features': {'xG': 2.7, 'PDO': 1.02, 'rookie_impact': 0.3},
            'opponent_features': {'xG': 2.4, 'PDO': 0.98, 'rookie_impact': 0.0},
            'game_context': {'home': True, 'b2b': False, 'rivalry': False, 'sentiment_boost': 0.08}
        },
        {
            'matchup': 'MTL vs BOS (25 sept)', 
            'team_features': {'xG': 2.6, 'PDO': 1.01, 'rookie_impact': 0.35},
            'opponent_features': {'xG': 2.8, 'PDO': 1.03, 'rookie_impact': 0.0},
            'game_context': {'home': True, 'b2b': False, 'rivalry': True, 'sentiment_boost': 0.06}
        },
        {
            'matchup': 'MTL Prospect Showdown (13 sept)',
            'team_features': {'xG': 2.2, 'PDO': 1.0, 'rookie_impact': 0.5},
            'opponent_features': {'xG': 2.0, 'PDO': 1.0, 'rookie_impact': 0.2}, 
            'game_context': {'home': True, 'b2b': False, 'rivalry': False, 'sentiment_boost': 0.12}
        }
    ]
    
    print("🎯 PRÉDICTIONS HYBRID ML (RF + GENETIC):\n")
    
    predictions_for_calibration = []
    
    for game in test_games:
        print(f"🏒 {game['matchup']}")
        
        # Prédiction hybride
        result = ml_engine.grok_hybrid_predict(
            game['team_features'],
            game['opponent_features'], 
            game['game_context']
        )
        
        predictions_for_calibration.append(result['final_probability'])
        
        print(f"   🌲 Random Forest: {result['rf_probability']:.1%}")
        print(f"   🧬 Genetic Optim: {result['genetic_probability']:.1%}")
        print(f"   🎯 Final Prob: {result['final_probability']:.1%}")
        print(f"   📊 Confidence: {result['confidence']:.1%}")
        print()
    
    # Simulation calibration nightly
    fake_outcomes = [1, 0, 1]  # Simulation résultats
    calibration_result = ml_engine.nightly_calibration(
        predictions_for_calibration, fake_outcomes
    )
    
    print("🌙 NIGHTLY CALIBRATION RESULTS:")
    print(f"   📊 Brier Score: {calibration_result['brier_score']:.3f}")
    print(f"   🎯 Target: <{calibration_result['calibration_target']}")
    print(f"   ⚙️  Status: {calibration_result['status']}")
    print(f"   🔧 Adjustment: {'Yes' if calibration_result['adjustment_made'] else 'No'}")
    
    avg_prob = sum(predictions_for_calibration) / len(predictions_for_calibration)
    print(f"\n🏆 AMÉLIORATION HYBRID ML:")
    print(f"   • Prob moyenne: {avg_prob:.1%}")
    print(f"   • Cible accuracy: 80% (vs 73.2% actuel)")
    print(f"   • Brier target: <0.18 (calibration)")
    print(f"   • ROI attendu: +20-30% (suggestions Grok)")

if __name__ == "__main__":
    demo_grok_hybrid_ml()
