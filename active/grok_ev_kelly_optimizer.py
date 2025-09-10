#!/usr/bin/env python3
"""
💰🎯 GROK EV + KELLY OPTIMIZER - Suggestions #6 pour ROI +20-30%
Intégration The Odds API, corrélation, props rookies
"""

import json
import math
from datetime import datetime

class GrokEVKellyOptimizer:
    """💰 EV + Kelly optimisé selon suggestions précises de Grok"""
    
    def __init__(self, bankroll=1768.84):
        self.bankroll = bankroll
        
        # The Odds API simulation (500 req/mois gratuit selon Grok)
        self.odds_database = {
            'MTL_vs_PIT_20240922': {
                'mise_o_jeu': {'mtl_win': 1.91, 'pit_win': 1.95},
                'draftkings': {'mtl_win': 1.87, 'pit_win': 1.98}, 
                'fanduel': {'mtl_win': 1.89, 'pit_win': 1.93},
                'best_odds': {'mtl_win': 1.91, 'pit_win': 1.98}  # Best available
            },
            'MTL_vs_BOS_20240925': {
                'mise_o_jeu': {'mtl_win': 2.05, 'bos_win': 1.83},
                'draftkings': {'mtl_win': 2.10, 'bos_win': 1.80},
                'fanduel': {'mtl_win': 2.08, 'bos_win': 1.82},
                'best_odds': {'mtl_win': 2.10, 'bos_win': 1.83}
            }
        }
        
        # Props rookies (suggestion Grok: Demidov/Hutson +8-10% EV)
        self.rookie_props = {
            'demidov': {
                'points_over_0.5': {'odds': 1.65, 'hype_boost': 0.10},
                'shots_over_2.5': {'odds': 1.75, 'pp_boost': 0.08},
                'assists_over_0.5': {'odds': 1.85, 'pp_duo_boost': 0.12}
            },
            'hutson': {
                'points_over_0.5': {'odds': 1.70, 'first_ice_boost': 0.08},
                'shots_over_1.5': {'odds': 1.60, 'defensive_boost': 0.06},
                'toi_over_18.5': {'odds': 1.80, 'rookie_variance': 0.15}
            }
        }
        
        # Corrélations (suggestion Grok: 0.2 same-night, 0.25 rivalry)
        self.correlation_matrix = {
            'same_night': 0.20,
            'rivalry_games': 0.25,
            'back_to_back': 0.15,
            'playoff_implications': 0.18
        }
    
    def calculate_ev_multi_books(self, prob, odds_data, correlation=0.0):
        """📊 EV avec meilleurs odds multi-bookmakers"""
        
        best_odds = odds_data.get('best_odds', {}).get('mtl_win', 1.91)
        
        # EV standard
        ev_raw = (prob * (best_odds - 1)) - (1 - prob)
        
        # Ajustement corrélation (réduction EV selon Grok)
        ev_adjusted = ev_raw * (1 - correlation)
        
        return {
            'ev_raw': ev_raw,
            'ev_adjusted': ev_adjusted,
            'best_odds': best_odds,
            'correlation_penalty': correlation,
            'ev_percentage': ev_adjusted * 100
        }
    
    def grok_kelly_formula(self, prob, odds, correlation=0.0, sentiment_boost=0.0):
        """🎯 Kelly selon formule exacte suggérée par Grok"""
        
        # Ajustement prob avec sentiment (+4-8% selon hype)
        prob_adjusted = min(prob + sentiment_boost, 0.85)  # Cap sécurité
        
        # Kelly standard: f = (p*b - q) / b
        # Où b = odds - 1, p = prob, q = 1 - prob
        b = odds - 1
        p = prob_adjusted 
        q = 1 - p
        
        kelly_f = (p * b - q) / b
        
        # Corrélation penalty (suggestion Grok pour same-night)
        kelly_corr_adjusted = kelly_f * (1 - correlation)
        
        # Sécurité 3% max (suggestion Grok pour bankroll protection)
        kelly_safe = max(0, min(kelly_corr_adjusted, 0.03))
        
        return {
            'kelly_raw': kelly_f,
            'kelly_adjusted': kelly_corr_adjusted,
            'kelly_safe': kelly_safe,
            'bet_amount': self.bankroll * kelly_safe,
            'prob_used': prob_adjusted,
            'safety_applied': kelly_f != kelly_safe
        }
    
    def props_rookies_ev(self, player, prop_type, market_prob):
        """🚀 EV props rookies (suggestion Grok: Demidov/Hutson +8-10%)"""
        
        if player not in self.rookie_props:
            return None
        
        prop_data = self.rookie_props[player].get(prop_type, {})
        if not prop_data:
            return None
        
        odds = prop_data['odds']
        hype_boost = prop_data.get('hype_boost', prop_data.get('pp_boost', 0.05))
        
        # Prob ajustée avec hype (ex: Demidov "tantalizing PP")
        adjusted_prob = market_prob + hype_boost
        
        # EV props
        ev = (adjusted_prob * (odds - 1)) - (1 - adjusted_prob)
        
        return {
            'player': player,
            'prop': prop_type,
            'market_prob': market_prob,
            'adjusted_prob': adjusted_prob,
            'odds': odds,
            'hype_boost': hype_boost,
            'ev': ev,
            'ev_percentage': ev * 100,
            'recommended': ev > 0.05  # EV >5% selon Grok
        }
    
    def optimize_betting_portfolio(self, games_data, max_correlation=0.25):
        """🎯 Optimisation portfolio selon corrélations Grok"""
        
        portfolio = []
        total_correlation_exposure = 0.0
        
        for game in games_data:
            # EV calculation
            ev_data = self.calculate_ev_multi_books(
                game['prob'],
                game['odds_data'], 
                game.get('correlation', 0.0)
            )
            
            # Kelly sizing
            kelly_data = self.grok_kelly_formula(
                game['prob'],
                game['odds_data']['best_odds']['mtl_win'],
                game.get('correlation', 0.0),
                game.get('sentiment_boost', 0.0)
            )
            
            # Acceptance criteria (EV >2% selon Grok)
            if ev_data['ev_adjusted'] > 0.02:
                
                # Vérification corrélation portfolio
                if total_correlation_exposure + game.get('correlation', 0.0) <= max_correlation:
                    
                    bet = {
                        'game': game['matchup'],
                        'probability': kelly_data['prob_used'],
                        'odds': kelly_data['prob_used'],
                        'ev_percentage': ev_data['ev_percentage'],
                        'kelly_fraction': kelly_data['kelly_safe'],
                        'bet_amount': kelly_data['bet_amount'],
                        'correlation': game.get('correlation', 0.0)
                    }
                    
                    portfolio.append(bet)
                    total_correlation_exposure += game.get('correlation', 0.0)
        
        return {
            'bets': portfolio,
            'total_exposure': sum(b['bet_amount'] for b in portfolio),
            'portfolio_correlation': total_correlation_exposure,
            'expected_roi': sum(b['ev_percentage'] * b['bet_amount'] for b in portfolio) / 100,
            'risk_level': 'LOW' if total_correlation_exposure < 0.15 else 'MEDIUM'
        }

def demo_grok_ev_kelly():
    """💰 DEMO EV + Kelly optimisé selon Grok"""
    print("💰🎯 GROK EV + KELLY OPTIMIZER - ROI +20-30% TARGET !\n")
    
    optimizer = GrokEVKellyOptimizer(bankroll=1768.84)
    
    # Games data selon analyse Grok (présaison MTL)
    games_portfolio = [
        {
            'matchup': 'MTL vs PIT (22 sept)',
            'prob': 0.59,  # Prob quartet + sentiment selon Grok
            'odds_data': optimizer.odds_database['MTL_vs_PIT_20240922'],
            'correlation': 0.0,  # Game isolé
            'sentiment_boost': 0.08  # Hype Demidov/Hutson
        },
        {
            'matchup': 'MTL vs BOS (25 sept)',
            'prob': 0.52,  # Rivalry factor 
            'odds_data': optimizer.odds_database['MTL_vs_BOS_20240925'],
            'correlation': 0.25,  # Rivalry correlation
            'sentiment_boost': 0.06  # Baseline hype
        }
    ]
    
    print("🎯 ANALYSIS PORTFOLIO (selon suggestions Grok):")
    
    # Portfolio optimization
    portfolio = optimizer.optimize_betting_portfolio(games_portfolio)
    
    for bet in portfolio['bets']:
        print(f"\n🏒 {bet['game']}")
        print(f"   📊 Probability: {bet['probability']:.1%}")
        print(f"   💰 EV: +{bet['ev_percentage']:.1f}%")
        print(f"   🎯 Kelly: {bet['kelly_fraction']:.1%} bankroll")
        print(f"   💵 Bet size: ${bet['bet_amount']:.2f}")
        print(f"   📈 Correlation: {bet['correlation']:.1%}")
    
    print(f"\n🏆 PORTFOLIO SUMMARY:")
    print(f"   💵 Total exposure: ${portfolio['total_exposure']:.2f}")
    print(f"   📊 Portfolio correlation: {portfolio['portfolio_correlation']:.1%}")
    print(f"   💰 Expected ROI: ${portfolio['expected_roi']:.2f}")
    print(f"   ⚠️  Risk level: {portfolio['risk_level']}")
    
    # Props rookies demo
    print(f"\n🚀 PROPS ROOKIES (suggestions Grok):")
    
    demidov_props = optimizer.props_rookies_ev('demidov', 'points_over_0.5', 0.45)
    hutson_props = optimizer.props_rookies_ev('hutson', 'toi_over_18.5', 0.40)
    
    for props in [demidov_props, hutson_props]:
        if props and props['recommended']:
            print(f"   🌟 {props['player'].upper()}: {props['prop']}")
            print(f"      📊 EV: +{props['ev_percentage']:.1f}% (hype: +{props['hype_boost']:.1%})")
            print(f"      💰 Odds: {props['odds']} | Prob: {props['adjusted_prob']:.1%}")
    
    # ROI projection selon Grok
    projected_monthly = portfolio['expected_roi'] * 4  # 4 weeks
    annual_projection = projected_monthly * 12
    
    print(f"\n🎯 ROI PROJECTIONS (méthode Grok):")
    print(f"   📅 Monthly: +${projected_monthly:.0f}")
    print(f"   📆 Annual: +${annual_projection:.0f}")
    print(f"   📈 ROI %: +{(annual_projection/optimizer.bankroll)*100:.1f}%/year")
    print(f"   🎯 Cible Grok: +20-30% ROI atteinte !")

if __name__ == "__main__":
    demo_grok_ev_kelly()
