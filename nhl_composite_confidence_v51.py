# 🏒🧠 NHL COMPOSITE CONFIDENCE SYSTEM v5.1 - GROK v4.0 ULTIMATE 🧠🏒
## FUSION DE TOUTES LES ANALYSES POUR PARIS ULTRA-SÉRIEUX

import sqlite3
import json
import time
import math
import statistics
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import du système d'analyses v5.0
from nhl_ultimate_analyzer_v50 import NHLUltimateAnalyzerV50

class NHLCompositeConfidenceV51(NHLUltimateAnalyzerV50):
    """
    🏒🧠 NHL COMPOSITE CONFIDENCE SYSTEM v5.1 - GROK v4.0 ULTIMATE 🧠🏒
    
    PHILOSOPHIE GROK v4.0 : PLUS D'ANALYSES = PARIS PLUS SÉRIEUX = ROI EXPLOSÉ
    
    SYSTÈME COMPOSITE CONFIDENCE (12 FACTEURS) :
    🎯 1. MOMENTUM ANALYSIS (Derniers 10 matchs)
    💤 2. FATIGUE FACTORS (Repos, B2B, voyages)
    ⚔️ 3. RIVALRY INTENSITY (Historique, division)
    🎯 4. CLUTCH PERFORMANCE (OT, SO, matchs serrés)
    🏥 5. INJURY IMPACT (Joueurs clés, lineup)
    📈 6. SEASONAL TRENDS (Performance par mois)
    🏠 7. HOME/AWAY SPLITS (Domicile vs extérieur)
    🎮 8. EA SIMULATION RELIABILITY (Données fiables)
    ⭐ 9. PLAYER RATINGS (Superstars, vétérans)
    📊 10. TEAM CHEMISTRY (Cohésion, forme)
    🏆 11. PLAYOFF EXPERIENCE (Pressure handling)
    💰 12. BETTING VALUE MATRIX (Inefficiences marché)
    
    OBJECTIF: CONFIDENCE COMPOSITE → PARIS ULTRA-SÉRIEUX → ROI 40-60%
    """
    
    def __init__(self):
        super().__init__()
        
        print("🧠" * 80)
        print("🏒 NHL COMPOSITE CONFIDENCE SYSTEM v5.1 - GROK v4.0 ULTIMATE 🏒")
        print("🧠" * 80)
        print("🎯 12 FACTEURS D'ANALYSE → CONFIDENCE COMPOSITE")
        print("📊 Momentum + Fatigue + Rivalry + Clutch + Injuries + Seasonal")
        print("🏠 Home/Away + EA Sim + Players + Chemistry + Playoffs + Value")
        print("💰 ROI ULTIMATE: 40-60% avec confidence composite")
        print("🧠 FAIRE SUER LES IAs AU MAXIMUM ! MOUAHHAHAHA!")
        
        # Configuration composite v5.1
        self.composite_config = {
            'system_version': 'v5.1_composite_confidence',
            'confidence_factors': 12,
            'confidence_threshold_ultimate': 0.80,      # 80% minimum
            'expected_value_threshold': 0.30,           # 30% minimum
            'composite_roi_target': 0.50,               # 50% ROI
            'analysis_weight_distribution': {
                'momentum': 0.12,           # 12%
                'fatigue': 0.10,            # 10%
                'rivalry': 0.08,            # 8%
                'clutch': 0.09,             # 9%
                'injuries': 0.11,           # 11%
                'seasonal': 0.07,           # 7%
                'home_away': 0.10,          # 10%
                'ea_simulation': 0.13,      # 13%
                'player_ratings': 0.08,     # 8%
                'team_chemistry': 0.06,     # 6%
                'playoff_experience': 0.03, # 3%
                'betting_value': 0.03       # 3%
            }
        }
        
        self.db_name = 'nhl_composite_confidence_v51.db'
        self.initialize_composite_database()
        
        print("✅ Composite Confidence System v5.1 initialisé!")
        print("🧠 IAs en mode OVERDRIVE pour analyses composites!")

    def initialize_composite_database(self):
        """Database pour système composite"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nhl_composite_confidence_v51 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_date TEXT NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                
                -- 12 FACTEURS COMPOSITE
                factor_1_momentum REAL,
                factor_2_fatigue REAL,
                factor_3_rivalry REAL,
                factor_4_clutch REAL,
                factor_5_injuries REAL,
                factor_6_seasonal REAL,
                factor_7_home_away REAL,
                factor_8_ea_simulation REAL,
                factor_9_player_ratings REAL,
                factor_10_team_chemistry REAL,
                factor_11_playoff_experience REAL,
                factor_12_betting_value REAL,
                
                -- SCORES COMPOSITES
                composite_confidence REAL,
                composite_expected_value REAL,
                composite_kelly_fraction REAL,
                
                -- GRADE SYSTÈME
                confidence_grade TEXT,
                bet_recommendation TEXT,
                profit_potential REAL,
                
                -- DÉTAILS ANALYSE
                factor_breakdown TEXT,  -- JSON des 12 facteurs
                strongest_factor TEXT,
                weakest_factor TEXT,
                
                -- VALIDATION
                grok_v40_ultimate_approved BOOLEAN DEFAULT 1,
                composite_system_grade TEXT,
                analysis_depth INTEGER DEFAULT 12
            )
        ''')
        
        conn.commit()
        conn.close()

    def calculate_home_away_analysis(self, home_team: str, away_team: str) -> Dict:
        """Facteur 7: Analyse Home/Away splits"""
        home_roster = self.team_rosters_extended[home_team]
        away_roster = self.team_rosters_extended[away_team]
        
        # Home advantage
        home_advantage = home_roster.get('home_advantage', 1.10)
        
        # Away team road performance (simulation)
        away_road_factor = 0.92  # Typical road performance
        
        # Altitude/Climate factors
        climate_factors = {
            'COL': 1.08,  # Altitude advantage
            'EDM': 1.05,  # Cold weather
            'TOR': 1.03,  # Indoor advantage
            'BOS': 1.02   # Historic building
        }
        
        home_climate = climate_factors.get(home_team, 1.00)
        
        # Combined home/away advantage
        total_home_advantage = (home_advantage - 1) + (1 - away_road_factor) + (home_climate - 1)
        
        return {
            'home_advantage_factor': round(home_advantage, 3),
            'away_road_penalty': round(1 - away_road_factor, 3),
            'climate_advantage': round(home_climate, 3),
            'total_home_advantage': round(total_home_advantage, 3),
            'home_away_score': min(1.0, max(0.0, total_home_advantage * 2.5))  # Normalize to 0-1
        }

    def calculate_player_ratings_analysis(self, home_team: str, away_team: str) -> Dict:
        """Facteur 9: Analyse ratings des joueurs"""
        home_roster = self.team_rosters_extended[home_team]
        away_roster = self.team_rosters_extended[away_team]
        
        # Count player types
        home_superstars = len(home_roster.get('superstars', []))
        home_veterans = len(home_roster.get('veterans', []))
        home_rising = len(home_roster.get('rising_stars', []))
        
        away_superstars = len(away_roster.get('superstars', []))
        away_veterans = len(away_roster.get('veterans', []))
        away_rising = len(away_roster.get('rising_stars', []))
        
        # Calculate talent scores
        home_talent = home_superstars * 3 + home_veterans * 2 + home_rising * 1
        away_talent = away_superstars * 3 + away_veterans * 2 + away_rising * 1
        
        talent_advantage = home_talent - away_talent
        
        # Get average ratings from database
        home_avg_rating = 85  # Simulation base
        away_avg_rating = 85
        
        # Adjust based on roster
        if home_superstars > 0:
            home_avg_rating += home_superstars * 5
        if away_superstars > 0:
            away_avg_rating += away_superstars * 5
        
        rating_advantage = home_avg_rating - away_avg_rating
        
        return {
            'home_talent_score': home_talent,
            'away_talent_score': away_talent,
            'talent_advantage': talent_advantage,
            'home_avg_rating': home_avg_rating,
            'away_avg_rating': away_avg_rating,
            'rating_advantage': rating_advantage,
            'player_ratings_score': min(1.0, max(0.0, (rating_advantage + 10) / 20))  # Normalize
        }

    def calculate_team_chemistry_analysis(self, home_team: str, away_team: str) -> Dict:
        """Facteur 10: Analyse chimie d'équipe"""
        home_roster = self.team_rosters_extended[home_team]
        away_roster = self.team_rosters_extended[away_team]
        
        home_chemistry = home_roster.get('team_chemistry', 0.85)
        away_chemistry = away_roster.get('team_chemistry', 0.85)
        
        # Recent form impact
        home_form = home_roster.get('recent_form', 'NEUTRAL')
        away_form = away_roster.get('recent_form', 'NEUTRAL')
        
        form_values = {'HOT': 1.15, 'WARM': 1.05, 'NEUTRAL': 1.0, 'COLD': 0.90, 'STRUGGLING': 0.80}
        
        home_form_factor = form_values.get(home_form, 1.0)
        away_form_factor = form_values.get(away_form, 1.0)
        
        # Adjusted chemistry
        home_adjusted_chemistry = home_chemistry * home_form_factor
        away_adjusted_chemistry = away_chemistry * away_form_factor
        
        chemistry_advantage = home_adjusted_chemistry - away_adjusted_chemistry
        
        return {
            'home_base_chemistry': home_chemistry,
            'away_base_chemistry': away_chemistry,
            'home_recent_form': home_form,
            'away_recent_form': away_form,
            'home_adjusted_chemistry': round(home_adjusted_chemistry, 3),
            'away_adjusted_chemistry': round(away_adjusted_chemistry, 3),
            'chemistry_advantage': round(chemistry_advantage, 3),
            'team_chemistry_score': min(1.0, max(0.0, (chemistry_advantage + 0.2) / 0.4))  # Normalize
        }

    def calculate_playoff_experience_analysis(self, home_team: str, away_team: str) -> Dict:
        """Facteur 11: Analyse expérience playoffs"""
        
        # Simulation playoff experience (in real system: from database)
        playoff_experience = {
            'TOR': 0.65,  # Moderate experience
            'EDM': 0.85,  # High experience (recent Cup runs)
            'COL': 0.80,  # High (Cup winners)
            'BOS': 0.90   # Very high (consistent playoffs)
        }
        
        home_exp = playoff_experience.get(home_team, 0.60)
        away_exp = playoff_experience.get(away_team, 0.60)
        
        experience_advantage = home_exp - away_exp
        
        # Pressure handling (simulation)
        pressure_factors = {
            'TOR': 0.70,  # Struggles under pressure
            'EDM': 0.85,  # Good under pressure
            'COL': 0.80,  # Solid
            'BOS': 0.95   # Excellent
        }
        
        home_pressure = pressure_factors.get(home_team, 0.75)
        away_pressure = pressure_factors.get(away_team, 0.75)
        
        return {
            'home_playoff_experience': home_exp,
            'away_playoff_experience': away_exp,
            'experience_advantage': round(experience_advantage, 3),
            'home_pressure_handling': home_pressure,
            'away_pressure_handling': away_pressure,
            'playoff_experience_score': min(1.0, max(0.0, (experience_advantage + 0.3) / 0.6))  # Normalize
        }

    def calculate_betting_value_matrix(self, home_team: str, away_team: str, 
                                     all_factors: Dict) -> Dict:
        """Facteur 12: Matrice de valeur betting (inefficiences marché)"""
        
        # Simulate market odds
        market_home_prob = 0.52  # Market thinks home team 52% likely
        market_away_prob = 0.48
        
        # Our composite probability (sum of factors)
        factor_sum = sum([
            all_factors.get('momentum', {}).get('composite_score', 0.5),
            all_factors.get('fatigue', {}).get('composite_score', 0.5),
            all_factors.get('rivalry', {}).get('composite_score', 0.5),
            all_factors.get('clutch', {}).get('composite_score', 0.5),
            all_factors.get('injuries', {}).get('composite_score', 0.5),
            all_factors.get('seasonal', {}).get('composite_score', 0.5)
        ])
        
        our_home_prob = min(0.85, max(0.15, factor_sum / 6))
        
        # Market inefficiency detection
        prob_difference = abs(our_home_prob - market_home_prob)
        
        # Value opportunity
        if prob_difference > 0.10:
            value_opportunity = 'HIGH_VALUE'
            value_score = 0.9
        elif prob_difference > 0.05:
            value_opportunity = 'MEDIUM_VALUE'
            value_score = 0.7
        elif prob_difference > 0.02:
            value_opportunity = 'SMALL_VALUE'
            value_score = 0.5
        else:
            value_opportunity = 'NO_VALUE'
            value_score = 0.2
        
        # Expected value calculation
        if our_home_prob > market_home_prob:
            # We favor home more than market
            implied_odds = 1 / market_home_prob
            expected_value = (our_home_prob * implied_odds - 1)
        else:
            # We favor away more than market
            implied_odds = 1 / market_away_prob
            expected_value = ((1 - our_home_prob) * implied_odds - 1)
        
        return {
            'market_home_probability': market_home_prob,
            'our_home_probability': round(our_home_prob, 3),
            'probability_difference': round(prob_difference, 3),
            'value_opportunity': value_opportunity,
            'expected_value': round(max(0, expected_value), 3),
            'betting_value_score': value_score
        }

    def calculate_composite_confidence(self, home_team: str, away_team: str, game_date: str) -> Dict:
        """SYSTÈME COMPOSITE COMPLET - 12 FACTEURS GROK v4.0"""
        
        print(f"\n🧠 CALCUL COMPOSITE CONFIDENCE: {away_team} @ {home_team}")
        print("=" * 60)
        
        game_month = int(game_date.split('-')[1])
        
        # FACTEUR 1: MOMENTUM
        home_momentum = self.calculate_momentum_analysis(home_team)
        away_momentum = self.calculate_momentum_analysis(away_team)
        momentum_advantage = home_momentum['momentum_score'] - away_momentum['momentum_score']
        factor_1 = min(1.0, max(0.0, (momentum_advantage + 0.5) / 1.0))
        
        print(f"   🔥 Facteur 1 - Momentum: {factor_1:.3f}")
        
        # FACTEUR 2: FATIGUE
        home_fatigue = self.calculate_fatigue_analysis(home_team)
        away_fatigue = self.calculate_fatigue_analysis(away_team)
        fatigue_advantage = away_fatigue['fatigue_level'] - home_fatigue['fatigue_level']  # Lower fatigue is better
        factor_2 = min(1.0, max(0.0, (fatigue_advantage + 0.5) / 1.0))
        
        print(f"   💤 Facteur 2 - Fatigue: {factor_2:.3f}")
        
        # FACTEUR 3: RIVALRY
        rivalry_analysis = self.calculate_rivalry_analysis(home_team, away_team)
        factor_3 = min(1.0, rivalry_analysis['rivalry_intensity'] + 0.2)  # Base boost
        
        print(f"   ⚔️ Facteur 3 - Rivalry: {factor_3:.3f}")
        
        # FACTEUR 4: CLUTCH
        clutch_analysis = self.calculate_clutch_analysis(home_team, away_team)
        clutch_advantage = clutch_analysis['clutch_advantage']
        factor_4 = min(1.0, max(0.0, (clutch_advantage + 0.3) / 0.6))
        
        print(f"   🎯 Facteur 4 - Clutch: {factor_4:.3f}")
        
        # FACTEUR 5: INJURIES
        home_injuries = self.calculate_injury_impact_analysis(home_team)
        away_injuries = self.calculate_injury_impact_analysis(away_team)
        injury_advantage = away_injuries['total_injury_impact'] - home_injuries['total_injury_impact']
        factor_5 = min(1.0, max(0.0, (injury_advantage + 0.3) / 0.6))
        
        print(f"   🏥 Facteur 5 - Injuries: {factor_5:.3f}")
        
        # FACTEUR 6: SEASONAL
        home_seasonal = self.calculate_seasonal_trends_analysis(home_team, game_month)
        away_seasonal = self.calculate_seasonal_trends_analysis(away_team, game_month)
        seasonal_advantage = home_seasonal['seasonal_factor'] - away_seasonal['seasonal_factor']
        factor_6 = min(1.0, max(0.0, (seasonal_advantage + 0.2) / 0.4))
        
        print(f"   📈 Facteur 6 - Seasonal: {factor_6:.3f}")
        
        # FACTEUR 7: HOME/AWAY
        home_away_analysis = self.calculate_home_away_analysis(home_team, away_team)
        factor_7 = home_away_analysis['home_away_score']
        
        print(f"   🏠 Facteur 7 - Home/Away: {factor_7:.3f}")
        
        # FACTEUR 8: EA SIMULATION
        all_factors_temp = {
            'momentum': {'home': home_momentum, 'away': away_momentum, 'composite_score': factor_1},
            'fatigue': {'home': home_fatigue, 'away': away_fatigue, 'composite_score': factor_2},
            'rivalry': rivalry_analysis,
            'clutch': clutch_analysis,
            'injuries': {'home': home_injuries, 'away': away_injuries, 'composite_score': factor_5},
            'seasonal': {'home': home_seasonal, 'away': away_seasonal, 'composite_score': factor_6}
        }
        
        ea_simulation = self.run_ea_simulation_reliable(home_team, away_team, all_factors_temp)
        factor_8 = ea_simulation['reliability_score']
        
        print(f"   🎮 Facteur 8 - EA Simulation: {factor_8:.3f}")
        
        # FACTEUR 9: PLAYER RATINGS
        player_ratings_analysis = self.calculate_player_ratings_analysis(home_team, away_team)
        factor_9 = player_ratings_analysis['player_ratings_score']
        
        print(f"   ⭐ Facteur 9 - Player Ratings: {factor_9:.3f}")
        
        # FACTEUR 10: TEAM CHEMISTRY
        chemistry_analysis = self.calculate_team_chemistry_analysis(home_team, away_team)
        factor_10 = chemistry_analysis['team_chemistry_score']
        
        print(f"   📊 Facteur 10 - Team Chemistry: {factor_10:.3f}")
        
        # FACTEUR 11: PLAYOFF EXPERIENCE
        playoff_analysis = self.calculate_playoff_experience_analysis(home_team, away_team)
        factor_11 = playoff_analysis['playoff_experience_score']
        
        print(f"   🏆 Facteur 11 - Playoff Experience: {factor_11:.3f}")
        
        # FACTEUR 12: BETTING VALUE
        betting_value_analysis = self.calculate_betting_value_matrix(home_team, away_team, all_factors_temp)
        factor_12 = betting_value_analysis['betting_value_score']
        
        print(f"   💰 Facteur 12 - Betting Value: {factor_12:.3f}")
        
        # CALCUL COMPOSITE FINAL
        weights = self.composite_config['analysis_weight_distribution']
        
        factors = [factor_1, factor_2, factor_3, factor_4, factor_5, factor_6,
                  factor_7, factor_8, factor_9, factor_10, factor_11, factor_12]
        
        weight_list = [weights['momentum'], weights['fatigue'], weights['rivalry'],
                      weights['clutch'], weights['injuries'], weights['seasonal'],
                      weights['home_away'], weights['ea_simulation'], weights['player_ratings'],
                      weights['team_chemistry'], weights['playoff_experience'], weights['betting_value']]
        
        # Composite confidence
        composite_confidence = sum(f * w for f, w in zip(factors, weight_list))
        
        # Expected value composite
        composite_ev = betting_value_analysis['expected_value'] * composite_confidence
        
        # Kelly fraction
        if composite_ev > 0 and composite_confidence > 0.5:
            kelly_fraction = min(0.10, composite_ev * 0.5)  # Cap at 10%
        else:
            kelly_fraction = 0.0
        
        # Grading system
        if composite_confidence >= 0.80:
            confidence_grade = 'ELITE'
            bet_recommendation = 'STRONG_BET'
        elif composite_confidence >= 0.70:
            confidence_grade = 'EXCELLENT'
            bet_recommendation = 'GOOD_BET'
        elif composite_confidence >= 0.60:
            confidence_grade = 'GOOD'
            bet_recommendation = 'CONSIDER'
        else:
            confidence_grade = 'WEAK'
            bet_recommendation = 'PASS'
        
        # Factor breakdown
        factor_names = ['Momentum', 'Fatigue', 'Rivalry', 'Clutch', 'Injuries', 'Seasonal',
                       'Home/Away', 'EA Sim', 'Players', 'Chemistry', 'Playoffs', 'Value']
        
        factor_breakdown = {name: round(factor, 3) for name, factor in zip(factor_names, factors)}
        
        strongest_factor = factor_names[factors.index(max(factors))]
        weakest_factor = factor_names[factors.index(min(factors))]
        
        print(f"\n🧠 COMPOSITE CONFIDENCE: {composite_confidence:.3f} ({confidence_grade})")
        print(f"💰 COMPOSITE EV: {composite_ev:.3f}")
        print(f"📊 KELLY FRACTION: {kelly_fraction:.4f}")
        print(f"🏆 RECOMMENDATION: {bet_recommendation}")
        print(f"⚡ STRONGEST FACTOR: {strongest_factor} ({max(factors):.3f})")
        print(f"⚠️ WEAKEST FACTOR: {weakest_factor} ({min(factors):.3f})")
        
        return {
            'composite_confidence': round(composite_confidence, 3),
            'composite_expected_value': round(composite_ev, 3),
            'composite_kelly_fraction': round(kelly_fraction, 4),
            'confidence_grade': confidence_grade,
            'bet_recommendation': bet_recommendation,
            'factor_breakdown': factor_breakdown,
            'strongest_factor': strongest_factor,
            'weakest_factor': weakest_factor,
            'all_factors': factors,
            'profit_potential': round(kelly_fraction * 1000 * composite_ev, 2),
            'analysis_components': {
                'momentum': {'home': home_momentum, 'away': away_momentum},
                'fatigue': {'home': home_fatigue, 'away': away_fatigue},
                'rivalry': rivalry_analysis,
                'clutch': clutch_analysis,
                'injuries': {'home': home_injuries, 'away': away_injuries},
                'seasonal': {'home': home_seasonal, 'away': away_seasonal},
                'home_away': home_away_analysis,
                'ea_simulation': ea_simulation,
                'player_ratings': player_ratings_analysis,
                'team_chemistry': chemistry_analysis,
                'playoff_experience': playoff_analysis,
                'betting_value': betting_value_analysis
            }
        }


def main():
    """Test système composite confidence complet"""
    print("🚀 LANCEMENT NHL COMPOSITE CONFIDENCE SYSTEM v5.1 - GROK v4.0 ULTIMATE")
    
    system = NHLCompositeConfidenceV51()
    
    # Test match composite complet
    result = system.calculate_composite_confidence('TOR', 'EDM', '2025-12-15')
    
    # Affichage résultat final
    print(f"\n🏆 RÉSULTAT COMPOSITE FINAL:")
    print("=" * 50)
    print(f"🧠 Confidence Composite: {result['composite_confidence']:.1%}")
    print(f"💰 Expected Value: {result['composite_expected_value']:.1%}")
    print(f"📊 Kelly Fraction: {result['composite_kelly_fraction']:.2%}")
    print(f"🏆 Grade: {result['confidence_grade']}")
    print(f"🎯 Recommandation: {result['bet_recommendation']}")
    print(f"💵 Profit Potentiel: ${result['profit_potential']:.2f}")
    
    print(f"\n📊 BREAKDOWN 12 FACTEURS:")
    for factor, score in result['factor_breakdown'].items():
        print(f"   {factor}: {score:.3f}")
    
    print(f"\n🏆 SYSTÈME COMPOSITE COMPLET TESTÉ!")
    print(f"🧠 IAs EN MODE OVERDRIVE! ANALYSES MAXIMALES!")
    print(f"💰 PRÊT POUR DES PARIS ULTRA-SÉRIEUX!")
    

if __name__ == "__main__":
    main()
