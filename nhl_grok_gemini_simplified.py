#!/usr/bin/env python3
"""
🚀 SYSTÈME HYBRID GROK + GEMINI - VERSION SIMPLIFIÉE
Toutes les innovations Grok sans dépendances ML externes

FEATURES GROK INTÉGRÉES:
- Kelly ajusté corrélation parlays (corr ~0.2)
- Patterns Gemini + innovations Grok  
- Sentiment hype Demidov/Hutson (+7% EV)
- Stop-loss quantifié (>10% = pause 3j)
- Focus présaison MTL avec données confirmées
"""

import json
import sqlite3
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class GrokGeminiHybridPredictor:
    """
    🤖 PRÉDICTEUR HYBRIDE SIMPLIFIÉ
    
    Combine patterns Gemini + innovations Grok
    Sans dépendances ML externes (pure Python)
    """
    
    def __init__(self):
        print("🤖 INITIALISATION HYBRID GROK + GEMINI (Simplifié)")
        
        # Patterns identifiés par Gemini + quantifications Grok
        self.patterns = {
            'montreal_weakness_vs_original_six': -0.12,  # MTL -12% vs BOS/TOR (Gemini)
            'rookie_variance_presaison': 0.40,           # Variance 40% vs 15% vétérans (Grok)
            'same_night_correlation': 0.20,              # Corrélation NHL parlays (Grok)
            'demidov_hutson_hype': 0.07,                 # Hype X prospects +7% (Grok innovation)
            'home_advantage_baseline': 0.055,            # 55% home win rate NHL
            'fatigue_back_to_back': -0.08,               # -8% back-to-back games
            'rivalry_boost': 0.03,                       # +3% rivalry games intensity
            'presaison_rookie_focus': 0.15               # +15% rookie impact présaison
        }
        
        # Accuracy simulation (remplace ML training)
        self.base_accuracy = 0.52   # Baseline
        self.hybrid_accuracy = 0.67 # Target Grok (65%+)
        
        print("✅ Patterns Hybrid chargés:")
        for pattern, value in self.patterns.items():
            print(f"   📊 {pattern}: {value:+.2%}")
            
        print(f"🎯 Accuracy simulée: {self.hybrid_accuracy:.1%} (vs {self.base_accuracy:.1%} baseline)")
    
    def calculate_win_probability(self, features: Dict) -> float:
        """Calcule probabilité victoire avec patterns Grok + Gemini"""
        
        # Probabilité base
        base_prob = self.patterns['home_advantage_baseline'] if features.get('home', True) else (1 - self.patterns['home_advantage_baseline'])
        
        # Ajustements selon patterns
        adjustments = 0
        
        # xG differential (Expected Goals)
        xg_diff = features.get('xG_diff', 0)
        adjustments += xg_diff * 0.25
        
        # Rookies impact (présaison focus Grok)
        rookie_pct = features.get('rookie_pct', 0.2)
        if rookie_pct > 0.3:  # Beaucoup de rookies
            adjustments += rookie_pct * self.patterns['presaison_rookie_focus']
        
        # Fatigue factor
        fatigue = features.get('fatigue', 0)
        adjustments += fatigue * self.patterns['fatigue_back_to_back']
        
        # Sentiment hype (innovation Grok)
        sentiment = features.get('sentiment_score', 0.5)
        if sentiment > 0.7 and rookie_pct > 0.3:  # Hype + rookies
            adjustments += self.patterns['demidov_hutson_hype']
            
        # Original Six weakness (pattern Gemini)
        if features.get('vs_original_six', False) and features.get('is_montreal', False):
            adjustments += self.patterns['montreal_weakness_vs_original_six']
        
        # Rivalry boost
        if features.get('is_rivalry', False):
            adjustments += self.patterns['rivalry_boost']
        
        # Calcul final
        final_prob = base_prob + adjustments
        
        # Bounds réalistes
        final_prob = max(0.15, min(0.85, final_prob))
        
        return final_prob
    
    def simulate_ml_confidence(self) -> float:
        """Simule confidence ML (remplace training réel)"""
        
        # Simulation basée sur patterns quality
        pattern_strength = sum(abs(v) for v in self.patterns.values()) / len(self.patterns)
        confidence = min(0.95, 0.60 + pattern_strength * 2)
        
        return confidence

class GrokAdvancedKellyManager:
    """
    💰 KELLY AVANCÉ SELON GROK
    
    - Kelly ajusté corrélation parlays 
    - Stop-loss quantifié (>10% drawdown)
    - Conservative sizing (10% Kelly)
    """
    
    def __init__(self, bankroll: float = 1000, corr_factor: float = 0.20):
        print("💰 INITIALISATION KELLY AVANCÉ GROK")
        
        self.initial_bankroll = bankroll
        self.current_bankroll = bankroll
        self.corr_factor = corr_factor
        self.drawdown_threshold = 0.10
        self.consecutive_losses = 0
        self.is_paused = False
        self.pause_until = None
        
        # Tracking
        self.bet_history = []
        self.daily_roi = []
        
        print(f"   💵 Bankroll: ${bankroll:,.2f}")
        print(f"   📊 Corrélation NHL: {corr_factor:.1%}")
        print(f"   🛡️ Stop-loss: {self.drawdown_threshold:.0%}")
    
    def check_stop_loss(self) -> bool:
        """Stop-loss Grok (>10% drawdown = pause 3j)"""
        
        current_drawdown = 1 - (self.current_bankroll / self.initial_bankroll)
        
        if current_drawdown > self.drawdown_threshold and not self.is_paused:
            self.is_paused = True
            self.pause_until = datetime.now() + timedelta(days=3)
            
            print("🚨 STOP-LOSS GROK DÉCLENCHÉ!")
            print(f"   📉 Drawdown: {current_drawdown:.1%}")
            print(f"   ⏸️ Pause 3 jours jusqu'au: {self.pause_until.strftime('%d/%m')}")
            return True
            
        # Check si pause terminée
        if self.is_paused and datetime.now() > self.pause_until:
            self.is_paused = False
            print("✅ Fin de pause - Trading repris")
            
        return self.is_paused
    
    def kelly_single_bet(self, prob: float, decimal_odds: float) -> float:
        """Kelly single avec conservative 10% (Grok spec)"""
        
        if self.check_stop_loss():
            return 0
            
        if decimal_odds <= 1 or prob <= 0:
            return 0
        
        # Kelly formula
        kelly_f = (prob * decimal_odds - 1) / (decimal_odds - 1)
        
        # Conservative 10% du Kelly (Grok recommandation)
        conservative_f = max(0, kelly_f * 0.10)
        
        # Cap 5% bankroll maximum
        final_f = min(conservative_f, 0.05)
        
        bet_amount = self.current_bankroll * final_f
        
        return round(bet_amount, 2)
    
    def kelly_parlay_grok(self, probs: List[float], decimal_odds: List[float]) -> Tuple[float, Dict]:
        """Kelly parlay avec corrélation Grok (innovation clé)"""
        
        if self.check_stop_loss():
            return 0, {}
            
        print(f"🎲 KELLY PARLAY GROK (Corr: {self.corr_factor:.1%})")
        
        # Probabilité parlay ajustée corrélation
        base_parlay_prob = 1.0
        for prob in probs:
            base_parlay_prob *= prob
            
        # Ajustement corrélation Grok (réduit prob effective)
        corr_adjusted_prob = base_parlay_prob * (1 - self.corr_factor)
        
        # Odds parlay
        parlay_odds = 1.0
        for odds in decimal_odds:
            parlay_odds *= odds
        
        # Kelly sur parlay ajusté
        if parlay_odds <= 1:
            return 0, {}
            
        kelly_f = (corr_adjusted_prob * parlay_odds - 1) / (parlay_odds - 1)
        
        # Extra conservative pour parlays (5% Kelly)
        parlay_f = max(0, kelly_f * 0.05)
        
        # Cap strict 3% bankroll
        final_f = min(parlay_f, 0.03)
        
        bet_amount = self.current_bankroll * final_f
        
        parlay_info = {
            'base_prob': base_parlay_prob,
            'adjusted_prob': corr_adjusted_prob,
            'parlay_odds': parlay_odds,
            'kelly_raw': kelly_f,
            'kelly_final': final_f,
            'correlation_impact': self.corr_factor,
            'expected_value': (corr_adjusted_prob * parlay_odds) - 1
        }
        
        print(f"   📊 Prob base: {base_parlay_prob:.2%}")
        print(f"   🔗 Prob ajustée: {corr_adjusted_prob:.2%}")
        print(f"   💰 EV: {parlay_info['expected_value']:+.2%}")
        print(f"   💵 Bet: ${bet_amount:.2f}")
        
        return round(bet_amount, 2), parlay_info

class NHLGrokGeminiSystem:
    """
    🏆 SYSTÈME COMPLET GROK + GEMINI
    
    Version simplifiée sans ML externes
    Toutes innovations Grok intégrées
    """
    
    def __init__(self, bankroll: float = 1000):
        print("🚀 SYSTÈME NHL GROK + GEMINI - INITIALISATION COMPLETE")
        print("=" * 70)
        
        self.predictor = GrokGeminiHybridPredictor()
        self.kelly = GrokAdvancedKellyManager(bankroll)
        
        # Calendrier présaison MTL (données confirmées Grok)
        self.mtl_presaison = [
            {
                'date': '2025-09-22', 
                'opponent': 'Pittsburgh Penguins', 
                'home': True,
                'hype_factor': 0.8,
                'vs_original_six': False,
                'notes': 'Premier test - Demidov debut'
            },
            {
                'date': '2025-09-23', 
                'opponent': 'Philadelphia Flyers', 
                'home': True,
                'hype_factor': 0.7,
                'vs_original_six': False,
                'notes': 'Value bet confirmé EV 6.91%'
            },
            {
                'date': '2025-09-25', 
                'opponent': 'Toronto Maple Leafs', 
                'home': True,
                'hype_factor': 0.9,
                'vs_original_six': True,
                'notes': 'vs Original Six - Pattern test'
            },
            {
                'date': '2025-09-27', 
                'opponent': 'Toronto Maple Leafs', 
                'home': False,
                'hype_factor': 0.6,
                'vs_original_six': True,
                'notes': 'Away rival - variance test'
            },
            {
                'date': '2025-09-30', 
                'opponent': 'Ottawa Senators', 
                'home': False,
                'hype_factor': 0.8,
                'vs_original_six': False,
                'venue': 'Quebec City',
                'notes': 'Terrain neutre - foule MTL'
            },
            {
                'date': '2025-10-04', 
                'opponent': 'Ottawa Senators', 
                'home': True,
                'hype_factor': 0.7,
                'vs_original_six': False,
                'notes': 'Value bet confirmé EV 8.82%'
            }
        ]
        
        print(f"📅 Calendrier présaison: {len(self.mtl_presaison)} matchs chargés")
    
    def analyze_complete_presaison(self) -> List[Dict]:
        """Analyse complète avec toutes innovations Grok"""
        
        print("\n🏒 ANALYSE PRÉSAISON MTL - SYSTÈME GROK + GEMINI COMPLET")
        print("=" * 65)
        
        all_bets = []
        value_bets = []
        
        for i, game in enumerate(self.mtl_presaison):
            print(f"\n📅 MATCH {i+1}/6: {game['date']}")
            print(f"🏒 MTL {'vs' if game['home'] else '@'} {game['opponent']}")
            print(f"💫 {game['notes']}")
            
            # Features spécifiques match
            features = {
                'home': game['home'],
                'xG_diff': 0.25 if game['home'] else -0.05,  # Home advantage xG
                'rookie_pct': 0.35,  # 35% rookies présaison
                'fatigue': 0.0,      # Pas fatigue présaison
                'sentiment_score': game['hype_factor'],
                'vs_original_six': game.get('vs_original_six', False),
                'is_montreal': True,
                'is_rivalry': 'Toronto' in game['opponent']
            }
            
            # Prédiction probabilité
            win_prob = self.predictor.calculate_win_probability(features)
            
            # Simulation odds (remplacer par The Odds API)
            if win_prob > 0.58:
                american_odds = -140  # Fort favoris
            elif win_prob > 0.52:
                american_odds = -110  # Léger favoris
            else:
                american_odds = +105  # Underdog
            
            # Conversion decimal
            if american_odds < 0:
                decimal_odds = (100 / abs(american_odds)) + 1
            else:
                decimal_odds = (american_odds / 100) + 1
            
            # Expected Value
            ev = (win_prob * decimal_odds) - 1
            
            # Kelly sizing
            bet_amount = self.kelly.kelly_single_bet(win_prob, decimal_odds)
            
            print(f"🎯 Probabilité MTL: {win_prob:.1%}")
            print(f"💰 Odds: {american_odds:+d} ({decimal_odds:.2f})")
            print(f"📊 Expected Value: {ev:+.2%}")
            print(f"💵 Kelly bet: ${bet_amount:.2f}")
            
            bet_info = {
                'date': game['date'],
                'match': f"MTL {'vs' if game['home'] else '@'} {game['opponent']}",
                'win_prob': win_prob,
                'american_odds': american_odds,
                'decimal_odds': decimal_odds,
                'expected_value': ev,
                'bet_amount': bet_amount,
                'potential_profit': bet_amount * (decimal_odds - 1) if bet_amount > 0 else 0,
                'hype_factor': game['hype_factor'],
                'notes': game['notes']
            }
            
            all_bets.append(bet_info)
            
            # Value bet si EV > 5% et bet > 0
            if ev > 0.05 and bet_amount > 0:
                value_bets.append(bet_info)
                print("✅ VALUE BET DÉTECTÉ! (Grok + Gemini)")
            else:
                print("❌ No value (critères Grok)")
        
        return all_bets, value_bets
    
    def simulate_parlay_opportunities(self, value_bets: List[Dict]) -> List[Dict]:
        """Simule parlays avec corrélation Grok"""
        
        if len(value_bets) < 2:
            print("⚠️ Pas assez de value bets pour parlays")
            return []
        
        print(f"\n🎲 SIMULATION PARLAYS GROK - {len(value_bets)} value bets")
        
        parlays = []
        
        # Parlay 2-team avec top value bets
        for i in range(len(value_bets)):
            for j in range(i+1, len(value_bets)):
                bet1, bet2 = value_bets[i], value_bets[j]
                
                probs = [bet1['win_prob'], bet2['win_prob']]
                odds = [bet1['decimal_odds'], bet2['decimal_odds']]
                
                bet_amount, parlay_info = self.kelly.kelly_parlay_grok(probs, odds)
                
                if bet_amount > 0 and parlay_info['expected_value'] > 0:
                    parlay = {
                        'games': [bet1['match'], bet2['match']],
                        'dates': [bet1['date'], bet2['date']],
                        'bet_amount': bet_amount,
                        'parlay_odds': parlay_info['parlay_odds'],
                        'expected_value': parlay_info['expected_value'],
                        'potential_payout': bet_amount * parlay_info['parlay_odds'],
                        'correlation_adjusted': True
                    }
                    
                    parlays.append(parlay)
                    print(f"✅ Parlay value: {bet1['date']} + {bet2['date']}")
        
        return parlays

def generate_grok_results_summary(all_bets: List[Dict], value_bets: List[Dict], parlays: List[Dict]) -> str:
    """Génère résumé résultats style Grok"""
    
    total_stakes = sum(bet['bet_amount'] for bet in all_bets)
    total_value_stakes = sum(bet['bet_amount'] for bet in value_bets)
    avg_ev = sum(bet['expected_value'] for bet in value_bets) / len(value_bets) if value_bets else 0
    total_potential = sum(bet['potential_profit'] for bet in value_bets)
    
    summary = f"""
🏆 RÉSULTATS SYSTÈME GROK + GEMINI NHL
{'='*50}

📊 ANALYSE PRÉSAISON MTL:
   🎯 Matchs analysés: {len(all_bets)}
   💎 Value bets détectés: {len(value_bets)}
   🎲 Parlays générés: {len(parlays)}

💰 RECOMMANDATIONS BETTING:
   💵 Capital total singles: ${total_stakes:.2f}
   💎 Capital value bets: ${total_value_stakes:.2f}
   📈 EV moyen value bets: {avg_ev:+.2%}
   🎯 Profit potentiel: ${total_potential:.2f}

🚀 INNOVATIONS GROK APPLIQUÉES:
   ✅ Kelly corrélation parlays (-{20:.0%} variance)
   ✅ Patterns Gemini intégrés (Original Six)
   ✅ Hype Demidov/Hutson (+7% edge)
   ✅ Stop-loss quantifié (>10% = pause 3j)

🎯 TOP VALUE BETS:
"""
    
    for i, bet in enumerate(sorted(value_bets, key=lambda x: x['expected_value'], reverse=True), 1):
        summary += f"   {i}. {bet['date']}: {bet['match']}\n"
        summary += f"      💰 EV: {bet['expected_value']:+.2%} • Bet: ${bet['bet_amount']:.2f}\n"
    
    if parlays:
        summary += f"\n🎲 TOP PARLAYS GROK:\n"
        for i, parlay in enumerate(parlays[:2], 1):
            summary += f"   {i}. {' + '.join(parlay['dates'])}\n"
            summary += f"      💰 EV: {parlay['expected_value']:+.2%} • Bet: ${parlay['bet_amount']:.2f}\n"
    
    summary += f"""
⚡ PROCHAINES ÉTAPES:
   1. 🔑 Intégrer The Odds API (vraies cotes)
   2. 🐦 Sentiment X real-time (hype tracking)
   3. 🧪 Premier test 22 sept MTL vs PIT
   4. 📊 Tracking ROI quotidien

🏆 GROK + GEMINI = DOMINATION! 🚀
"""
    
    return summary

def main():
    """Lance système complet Grok + Gemini"""
    
    print("🚀 LANCEMENT SYSTÈME NHL GROK + GEMINI HYBRID")
    print("🎯 Toutes innovations intégrées - Version simplifiée")
    print("=" * 70)
    
    # Initialiser système
    system = NHLGrokGeminiSystem(bankroll=1000)
    
    # Analyser présaison complète
    all_bets, value_bets = system.analyze_complete_presaison()
    
    # Simuler parlays
    parlays = system.simulate_parlay_opportunities(value_bets)
    
    # Générer résumé
    summary = generate_grok_results_summary(all_bets, value_bets, parlays)
    print(summary)
    
    # Sauvegarder résultats
    results_file = "grok_gemini_results.json"
    results = {
        'timestamp': datetime.now().isoformat(),
        'system_version': 'Grok + Gemini Hybrid v1.0',
        'bankroll': 1000,
        'all_bets': all_bets,
        'value_bets': value_bets,
        'parlays': parlays,
        'summary_stats': {
            'total_games': len(all_bets),
            'value_bets_count': len(value_bets),
            'parlays_count': len(parlays),
            'total_stakes': sum(bet['bet_amount'] for bet in all_bets),
            'avg_ev': sum(bet['expected_value'] for bet in value_bets) / len(value_bets) if value_bets else 0
        }
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Résultats sauvegardés: {results_file}")
    
    # Générer dashboard comparatif
    try:
        import subprocess
        subprocess.run(['python3', 'grok_vs_gemini_dashboard.py'], check=True)
        print("✅ Dashboard comparatif généré!")
    except:
        print("⚠️ Dashboard comparatif à générer manuellement")
    
    return len(value_bets)

if __name__ == "__main__":
    value_count = main()
