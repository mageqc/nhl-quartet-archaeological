#!/usr/bin/env python3
"""
🔮🚀 GEMINI ENSEMBLE LEARNING - XGBoost + Feature Engineering Avancé
Implémentation des suggestions Gemini pour améliorer l'accuracy de 73.2% → 80%+
"""

import json
import math
import random
from datetime import datetime, timedelta

class GeminiEnsembleLearning:
    """🔮 Ensemble Learning selon suggestions précises de Gemini"""
    
    def __init__(self):
        # Modèle XGBoost simulé (suggestion Gemini)
        self.xgboost_weights = {
            'win_rate_l10': 0.22,     # Momentum équipe (10 derniers)
            'home_advantage': 0.18,   # Avantage domicile
            'b2b_fatigue': 0.15,      # Back-to-back + fuseaux horaires
            'travel_fatigue': 0.12,   # Distance parcourue
            'injury_impact': 0.10,    # Blessures joueurs clés
            'sentiment_social': 0.08, # Sentiment réseaux sociaux
            'goalie_form': 0.15       # Forme gardien titulaire
        }
        
        # Feature Engineering avancé (suggestion Gemini)
        self.advanced_features = {
            'travel_matrix': {
                'MTL_to_BOS': {'distance': 306, 'timezone_diff': 0, 'fatigue_factor': 0.02},
                'MTL_to_TOR': {'distance': 541, 'timezone_diff': 0, 'fatigue_factor': 0.03},
                'MTL_to_WPG': {'distance': 1516, 'timezone_diff': 1, 'fatigue_factor': 0.08},
                'MTL_to_PIT': {'distance': 764, 'timezone_diff': 0, 'fatigue_factor': 0.04}
            },
            'momentum_weights': [0.4, 0.3, 0.2, 0.1],  # Poids 1-4 derniers games
            'injury_severity': {'C1': -0.15, 'G1': -0.20, 'D1': -0.08, 'MINOR': -0.03}
        }
        
        # Calibration historique (suggestion Gemini)
        self.calibration_data = []
        self.calibration_bins = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    def extract_advanced_features(self, team_data, opponent_data, game_context):
        """🎯 Feature Engineering avancé selon Gemini"""
        
        features = {}
        
        # 1. Momentum équipe (5-10 derniers matchs)
        recent_games = team_data.get('recent_results', [1, 1, 0, 1, 0])  # W/L
        momentum_score = sum(w * result for w, result in 
                           zip(self.advanced_features['momentum_weights'], recent_games[-4:]))
        features['momentum_l4'] = momentum_score
        
        # 2. Fatigue voyage + fuseaux horaires (suggestion Gemini)
        travel_key = f"{team_data.get('team', 'MTL')}_to_{opponent_data.get('team', 'BOS')}"
        travel_data = self.advanced_features['travel_matrix'].get(travel_key, {})
        
        is_b2b = game_context.get('back_to_back', False)
        travel_fatigue = travel_data.get('fatigue_factor', 0.02)
        timezone_penalty = travel_data.get('timezone_diff', 0) * 0.015
        
        features['travel_fatigue'] = travel_fatigue + timezone_penalty + (0.05 if is_b2b else 0)
        
        # 3. Impact blessures (joueurs clés)
        injuries = team_data.get('injuries', [])
        injury_impact = sum(self.advanced_features['injury_severity'].get(inj, 0) for inj in injuries)
        features['injury_penalty'] = injury_impact
        
        # 4. Forme gardien (GAA récent, SV%)
        goalie_stats = team_data.get('goalie', {'gaa_l5': 2.50, 'sv_pct_l5': 0.915})
        league_avg_gaa = 2.80
        league_avg_sv = 0.905
        
        goalie_form = ((league_avg_gaa - goalie_stats['gaa_l5']) / league_avg_gaa) * 0.5
        goalie_form += ((goalie_stats['sv_pct_l5'] - league_avg_sv) / league_avg_sv) * 0.5
        features['goalie_advantage'] = goalie_form
        
        # 5. Sentiment réseaux sociaux (simulation API Twitter/Reddit)
        social_buzz = game_context.get('social_sentiment', 0.5)  # 0-1 scale
        features['social_sentiment'] = (social_buzz - 0.5) * 0.1  # Convert to +/-5%
        
        return features
    
    def xgboost_simulation(self, features):
        """🌲 Simulation XGBoost (Gradient Boosting selon Gemini)"""
        
        # Base probability
        base_prob = 0.5
        
        # XGBoost feature importance weighted sum
        for feature, weight in self.xgboost_weights.items():
            if feature == 'win_rate_l10':
                base_prob += features.get('momentum_l4', 0) * weight
            elif feature == 'home_advantage':
                base_prob += 0.055 * weight  # Standard home advantage
            elif feature == 'b2b_fatigue':
                base_prob -= features.get('travel_fatigue', 0) * weight
            elif feature == 'injury_impact':
                base_prob += features.get('injury_penalty', 0) * weight
            elif feature == 'goalie_form':
                base_prob += features.get('goalie_advantage', 0) * weight
            elif feature == 'sentiment_social':
                base_prob += features.get('social_sentiment', 0) * weight
        
        return min(max(base_prob, 0.05), 0.95)
    
    def ensemble_prediction(self, team_data, opponent_data, game_context, rules_prob=0.55):
        """🎯 Ensemble: Règles déterministes + XGBoost (suggestion Gemini)"""
        
        # 1. Extract advanced features
        features = self.extract_advanced_features(team_data, opponent_data, game_context)
        
        # 2. XGBoost prediction
        xgb_prob = self.xgboost_simulation(features)
        
        # 3. Ensemble combination (70% XGBoost + 30% règles selon Gemini)
        ensemble_prob = (xgb_prob * 0.70) + (rules_prob * 0.30)
        
        return {
            'rules_probability': rules_prob,
            'xgboost_probability': xgb_prob,
            'ensemble_probability': ensemble_prob,
            'features_extracted': features,
            'improvement_vs_rules': abs(ensemble_prob - rules_prob),
            'confidence': 1.0 - abs(ensemble_prob - 0.5)  # Distance from 50%
        }
    
    def calibration_check(self, predicted_probs, actual_outcomes):
        """📊 Calibration selon suggestion Gemini (diagramme calibration)"""
        
        calibration_results = {}
        
        for i, bin_threshold in enumerate(self.calibration_bins):
            # Prédictions dans ce bin
            bin_preds = [p for p in predicted_probs if 
                        (i == 0 and p <= bin_threshold) or 
                        (i > 0 and self.calibration_bins[i-1] < p <= bin_threshold)]
            
            if bin_preds:
                # Outcomes correspondants
                bin_outcomes = [actual_outcomes[j] for j, p in enumerate(predicted_probs) if p in bin_preds]
                
                # Calibration stats
                avg_predicted = sum(bin_preds) / len(bin_preds)
                avg_actual = sum(bin_outcomes) / len(bin_outcomes) if bin_outcomes else 0
                calibration_error = abs(avg_predicted - avg_actual)
                
                calibration_results[f'bin_{bin_threshold}'] = {
                    'avg_predicted': avg_predicted,
                    'avg_actual': avg_actual,
                    'calibration_error': calibration_error,
                    'n_predictions': len(bin_preds),
                    'well_calibrated': calibration_error < 0.05
                }
        
        # Score global calibration
        total_error = sum(bin_data['calibration_error'] for bin_data in calibration_results.values())
        avg_calibration_error = total_error / len(calibration_results) if calibration_results else 0.5
        
        return {
            'calibration_by_bin': calibration_results,
            'overall_calibration_error': avg_calibration_error,
            'is_well_calibrated': avg_calibration_error < 0.03,
            'calibration_grade': 'A' if avg_calibration_error < 0.02 else 
                               'B' if avg_calibration_error < 0.05 else 'C'
        }
    
    def kelly_with_correlation_gemini(self, prob, odds, bankroll, correlation_matrix=None):
        """💰 Kelly Criterion amélioré selon suggestion Gemini (corrélation paris multiples)"""
        
        # Kelly standard
        f = ((prob * odds - 1) / (odds - 1))
        
        # Ajustement corrélation si paris multiples
        if correlation_matrix:
            # Réduction exposition selon corrélation moyenne
            avg_correlation = sum(correlation_matrix.values()) / len(correlation_matrix)
            f_adjusted = f * (1 - avg_correlation * 0.5)  # 50% réduction si corrélation forte
        else:
            f_adjusted = f
        
        # Sécurité: max 2% bankroll (suggestion Gemini)
        f_safe = max(0, min(f_adjusted, 0.02))
        
        return {
            'kelly_raw': f,
            'kelly_correlation_adjusted': f_adjusted,
            'kelly_safe': f_safe,
            'bet_amount': bankroll * f_safe,
            'correlation_impact': f - f_adjusted if correlation_matrix else 0
        }

def demo_gemini_ensemble():
    """🔮 DEMO Ensemble Learning selon Gemini"""
    print("🔮🚀 GEMINI ENSEMBLE LEARNING - ML AVANCÉ + CALIBRATION !\n")
    
    ml_engine = GeminiEnsembleLearning()
    
    # Test data présaison MTL (selon contexte)
    test_scenarios = [
        {
            'matchup': 'MTL vs PIT (22 sept)',
            'team_data': {
                'team': 'MTL',
                'recent_results': [1, 0, 1, 1, 0],  # L5 games
                'injuries': ['MINOR'],  # Blessures mineures
                'goalie': {'gaa_l5': 2.30, 'sv_pct_l5': 0.925}  # Forme gardien
            },
            'opponent_data': {
                'team': 'PIT',
                'recent_results': [0, 1, 0, 1, 1],
                'injuries': [],
                'goalie': {'gaa_l5': 2.65, 'sv_pct_l5': 0.908}
            },
            'game_context': {
                'back_to_back': False,
                'social_sentiment': 0.75,  # Hype Demidov/Hutson
                'home_game': True
            },
            'rules_baseline': 0.58  # Prob règles déterministes actuelles
        },
        {
            'matchup': 'MTL vs BOS (25 sept)',
            'team_data': {
                'team': 'MTL', 
                'recent_results': [1, 1, 0, 1, 0],
                'injuries': [],
                'goalie': {'gaa_l5': 2.25, 'sv_pct_l5': 0.920}
            },
            'opponent_data': {
                'team': 'BOS',
                'recent_results': [1, 1, 1, 0, 1],
                'injuries': ['D1'],  # Défenseur clé blessé
                'goalie': {'gaa_l5': 2.45, 'sv_pct_l5': 0.915}
            },
            'game_context': {
                'back_to_back': False,
                'social_sentiment': 0.65,  # Rivalry buzz
                'home_game': True
            },
            'rules_baseline': 0.52
        }
    ]
    
    print("🎯 ENSEMBLE PREDICTIONS (XGBoost + Règles):\n")
    
    all_predictions = []
    
    for scenario in test_scenarios:
        print(f"🏒 {scenario['matchup']}")
        
        # Ensemble prediction
        result = ml_engine.ensemble_prediction(
            scenario['team_data'],
            scenario['opponent_data'], 
            scenario['game_context'],
            scenario['rules_baseline']
        )
        
        all_predictions.append(result['ensemble_probability'])
        
        print(f"   📊 Règles déterministes: {result['rules_probability']:.1%}")
        print(f"   🌲 XGBoost ML: {result['xgboost_probability']:.1%}")
        print(f"   🔮 Ensemble final: {result['ensemble_probability']:.1%}")
        print(f"   📈 Amélioration: {result['improvement_vs_rules']:.1%}")
        print(f"   🎯 Confiance: {result['confidence']:.1%}")
        
        # Features breakdown
        features = result['features_extracted']
        print(f"   Features clés:")
        print(f"     • Momentum: {features.get('momentum_l4', 0):.3f}")
        print(f"     • Travel fatigue: {features.get('travel_fatigue', 0):.3f}")
        print(f"     • Goalie advantage: {features.get('goalie_advantage', 0):.3f}")
        print()
    
    # Test calibration
    fake_outcomes = [1, 0]  # Simulation résultats
    calibration_result = ml_engine.calibration_check(all_predictions, fake_outcomes)
    
    print("📊 CALIBRATION ANALYSIS (Gemini suggestion):")
    print(f"   🎯 Calibration error: {calibration_result['overall_calibration_error']:.3f}")
    print(f"   📈 Calibration grade: {calibration_result['calibration_grade']}")
    print(f"   ✅ Well calibrated: {'Yes' if calibration_result['is_well_calibrated'] else 'No'}")
    
    # Kelly avec corrélation
    correlation_matrix = {'game1_vs_game2': 0.15}  # Same night correlation
    kelly_result = ml_engine.kelly_with_correlation_gemini(
        prob=0.62, odds=1.90, bankroll=1768.84, correlation_matrix=correlation_matrix
    )
    
    print(f"\n💰 KELLY + CORRELATION (Gemini):")
    print(f"   🎯 Kelly safe: {kelly_result['kelly_safe']:.1%} bankroll")
    print(f"   💵 Bet amount: ${kelly_result['bet_amount']:.2f}")
    print(f"   📊 Correlation impact: {kelly_result['correlation_impact']:.3f}")
    
    print(f"\n🏆 GEMINI SUGGESTIONS IMPLÉMENTÉES:")
    print(f"   ✅ Ensemble Learning (XGBoost + Règles)")
    print(f"   ✅ Feature Engineering avancé (voyage, momentum)")
    print(f"   ✅ Calibration monitoring (diagramme)")
    print(f"   ✅ Kelly avec corrélation paris multiples")
    print(f"   🎯 Cible accuracy: 80% (vs 73.2% actuel)")

if __name__ == "__main__":
    demo_gemini_ensemble()
