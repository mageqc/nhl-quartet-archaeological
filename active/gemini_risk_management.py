#!/usr/bin/env python3
"""
🛡️⚡ GEMINI RISK MANAGEMENT - Stop-Loss + Black Swan Detection
Implémentation protection bankroll et événements rares selon Gemini
"""

import json
import math
from datetime import datetime, timedelta

class GeminiRiskManagement:
    """🛡️ Risk Management avancé selon suggestions Gemini"""
    
    def __init__(self, initial_bankroll=1768.84):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        
        # Stop-loss parameters (suggestion Gemini)
        self.stop_loss_config = {
            'daily_loss_limit': 0.05,      # 5% max perte/jour
            'weekly_loss_limit': 0.15,     # 15% max perte/semaine  
            'drawdown_limit': 0.25,        # 25% max drawdown total
            'consecutive_loss_limit': 5,    # 5 paris perdants consécutifs
            'volatility_threshold': 0.30   # Seuil volatilité anormale
        }
        
        # Black Swan events detection (suggestion Gemini)
        self.black_swan_indicators = {
            'injury_severity': {
                'star_player_out': {'impact': -0.20, 'rarity': 0.05},
                'goalie_injury_game_day': {'impact': -0.15, 'rarity': 0.03}, 
                'multiple_key_injuries': {'impact': -0.25, 'rarity': 0.02},
                'covid_outbreak': {'impact': -0.30, 'rarity': 0.01}
            },
            'performance_anomalies': {
                'goalie_meltdown': {'impact': -0.35, 'rarity': 0.02},
                'offensive_explosion': {'impact': 0.25, 'rarity': 0.03},
                'referee_bias': {'impact': -0.10, 'rarity': 0.08},
                'weather_extreme': {'impact': -0.08, 'rarity': 0.04}
            },
            'market_anomalies': {
                'odds_manipulation': {'impact': -0.15, 'rarity': 0.01},
                'insider_betting': {'impact': -0.20, 'rarity': 0.005},
                'line_movement_extreme': {'impact': -0.12, 'rarity': 0.02}
            }
        }
        
        # Historique pour monitoring
        self.betting_history = []
        self.drawdown_history = []
        self.stop_loss_triggers = []
    
    def calculate_current_drawdown(self):
        """📉 Calcul drawdown actuel"""
        peak_bankroll = max([entry.get('bankroll', self.initial_bankroll) 
                           for entry in self.betting_history] + [self.initial_bankroll])
        
        current_drawdown = (peak_bankroll - self.current_bankroll) / peak_bankroll
        return current_drawdown
    
    def check_stop_loss_conditions(self, recent_bets):
        """🛑 Vérification conditions stop-loss selon Gemini"""
        
        stop_loss_status = {
            'should_stop': False,
            'triggered_conditions': [],
            'risk_level': 'LOW'
        }
        
        # 1. Drawdown global
        current_drawdown = self.calculate_current_drawdown()
        if current_drawdown >= self.stop_loss_config['drawdown_limit']:
            stop_loss_status['should_stop'] = True
            stop_loss_status['triggered_conditions'].append(f"Drawdown {current_drawdown:.1%} >= {self.stop_loss_config['drawdown_limit']:.1%}")
        
        # 2. Pertes consécutives
        if len(recent_bets) >= self.stop_loss_config['consecutive_loss_limit']:
            recent_outcomes = [bet.get('outcome', 0) for bet in recent_bets[-5:]]
            if all(outcome == 0 for outcome in recent_outcomes):  # 5 pertes d'affilée
                stop_loss_status['should_stop'] = True
                stop_loss_status['triggered_conditions'].append("5 pertes consécutives")
        
        # 3. Perte journalière excessive
        today = datetime.now().date()
        today_bets = [bet for bet in recent_bets if 
                     datetime.fromisoformat(bet.get('date', '2024-01-01')).date() == today]
        
        if today_bets:
            today_pnl = sum(bet.get('pnl', 0) for bet in today_bets)
            daily_loss_pct = abs(today_pnl) / self.current_bankroll
            
            if today_pnl < 0 and daily_loss_pct >= self.stop_loss_config['daily_loss_limit']:
                stop_loss_status['should_stop'] = True
                stop_loss_status['triggered_conditions'].append(f"Perte journalière {daily_loss_pct:.1%}")
        
        # 4. Volatilité anormale
        if len(recent_bets) >= 10:
            recent_pnls = [bet.get('pnl', 0) for bet in recent_bets[-10:]]
            volatility = self._calculate_volatility(recent_pnls)
            
            if volatility >= self.stop_loss_config['volatility_threshold']:
                stop_loss_status['risk_level'] = 'HIGH'
                stop_loss_status['triggered_conditions'].append(f"Volatilité élevée {volatility:.1%}")
        
        return stop_loss_status
    
    def detect_black_swan_events(self, game_context, market_data, news_feed):
        """🦢⚫ Détection Black Swan events selon Gemini"""
        
        black_swan_score = 0.0
        detected_events = []
        
        # 1. Analyse blessures (injury_severity)
        injuries = game_context.get('injuries', [])
        for injury in injuries:
            for event_type, event_data in self.black_swan_indicators['injury_severity'].items():
                if self._match_injury_pattern(injury, event_type):
                    black_swan_score += abs(event_data['impact']) * (1 / event_data['rarity'])
                    detected_events.append({
                        'type': 'injury',
                        'event': event_type,
                        'impact': event_data['impact'],
                        'rarity': event_data['rarity']
                    })
        
        # 2. Anomalies performance
        performance_indicators = game_context.get('performance_flags', [])
        for indicator in performance_indicators:
            if indicator in self.black_swan_indicators['performance_anomalies']:
                event_data = self.black_swan_indicators['performance_anomalies'][indicator]
                black_swan_score += abs(event_data['impact']) * (1 / event_data['rarity'])
                detected_events.append({
                    'type': 'performance',
                    'event': indicator, 
                    'impact': event_data['impact'],
                    'rarity': event_data['rarity']
                })
        
        # 3. Anomalies marché
        line_movement = market_data.get('line_movement_pct', 0.0)
        if abs(line_movement) > 0.15:  # Mouvement >15%
            event_data = self.black_swan_indicators['market_anomalies']['line_movement_extreme']
            black_swan_score += abs(event_data['impact']) * (1 / event_data['rarity'])
            detected_events.append({
                'type': 'market',
                'event': 'line_movement_extreme',
                'impact': event_data['impact'],
                'line_movement': line_movement
            })
        
        # Classification risque Black Swan
        risk_classification = 'LOW'
        if black_swan_score > 5.0:
            risk_classification = 'EXTREME'
        elif black_swan_score > 2.0:
            risk_classification = 'HIGH' 
        elif black_swan_score > 0.5:
            risk_classification = 'MEDIUM'
        
        return {
            'black_swan_score': black_swan_score,
            'risk_level': risk_classification,
            'detected_events': detected_events,
            'recommendation': 'AVOID_BETTING' if black_swan_score > 2.0 else 
                           'REDUCE_STAKES' if black_swan_score > 0.5 else 'NORMAL_BETTING'
        }
    
    def _match_injury_pattern(self, injury_description, pattern):
        """🤕 Pattern matching blessures"""
        patterns = {
            'star_player_out': ['C1', 'star', 'top_scorer'],
            'goalie_injury_game_day': ['G1', 'goalie', 'same_day'],
            'multiple_key_injuries': ['multiple', 'key_players'],
            'covid_outbreak': ['covid', 'protocol', 'outbreak']
        }
        
        return any(keyword in injury_description.lower() for keyword in patterns.get(pattern, []))
    
    def _calculate_volatility(self, pnl_series):
        """📊 Calcul volatilité série P&L"""
        if len(pnl_series) < 2:
            return 0.0
        
        mean_pnl = sum(pnl_series) / len(pnl_series)
        variance = sum((pnl - mean_pnl) ** 2 for pnl in pnl_series) / len(pnl_series)
        std_dev = math.sqrt(variance)
        
        return std_dev / abs(mean_pnl) if mean_pnl != 0 else 0.0
    
    def risk_adjusted_bet_sizing(self, base_kelly, risk_factors):
        """⚖️ Sizing ajusté selon risques détectés"""
        
        # Facteurs de réduction selon risques
        risk_multipliers = {
            'drawdown_high': 0.5,      # Réduction 50% si drawdown élevé
            'volatility_high': 0.7,    # Réduction 30% si volatilité haute
            'black_swan_medium': 0.6,  # Réduction 40% si Black Swan medium
            'black_swan_high': 0.2,    # Réduction 80% si Black Swan high
            'consecutive_losses': 0.4   # Réduction 60% après pertes consécutives
        }
        
        adjusted_kelly = base_kelly
        applied_reductions = []
        
        for risk_factor, is_present in risk_factors.items():
            if is_present and risk_factor in risk_multipliers:
                reduction = risk_multipliers[risk_factor]
                adjusted_kelly *= reduction
                applied_reductions.append(f"{risk_factor}: {reduction}x")
        
        return {
            'original_kelly': base_kelly,
            'adjusted_kelly': adjusted_kelly,
            'total_reduction': base_kelly - adjusted_kelly,
            'reduction_factors': applied_reductions,
            'final_bet_pct': adjusted_kelly
        }

def demo_gemini_risk_management():
    """🛡️ DEMO Risk Management selon Gemini"""
    print("🛡️⚡ GEMINI RISK MANAGEMENT - STOP-LOSS + BLACK SWAN !\n")
    
    risk_manager = GeminiRiskManagement(initial_bankroll=1768.84)
    
    # Simulation historique récente (pertes)
    recent_betting_history = [
        {'date': '2024-09-05', 'outcome': 0, 'pnl': -50, 'bankroll': 1718.84},
        {'date': '2024-09-06', 'outcome': 0, 'pnl': -45, 'bankroll': 1673.84}, 
        {'date': '2024-09-07', 'outcome': 1, 'pnl': 30, 'bankroll': 1703.84},
        {'date': '2024-09-08', 'outcome': 0, 'pnl': -40, 'bankroll': 1663.84},
        {'date': '2024-09-09', 'outcome': 0, 'pnl': -35, 'bankroll': 1628.84}
    ]
    
    risk_manager.betting_history = recent_betting_history
    risk_manager.current_bankroll = 1628.84
    
    print("🛑 STOP-LOSS ANALYSIS:")
    
    # Check stop-loss conditions
    stop_loss_result = risk_manager.check_stop_loss_conditions(recent_betting_history)
    
    print(f"   🚨 Should stop betting: {'YES' if stop_loss_result['should_stop'] else 'NO'}")
    print(f"   📊 Risk level: {stop_loss_result['risk_level']}")
    
    if stop_loss_result['triggered_conditions']:
        print(f"   ⚠️  Conditions déclenchées:")
        for condition in stop_loss_result['triggered_conditions']:
            print(f"     • {condition}")
    
    # Black Swan detection test
    print(f"\n🦢⚫ BLACK SWAN DETECTION:")
    
    test_game_context = {
        'injuries': ['G1_same_day', 'C1_star'],  # Gardien + joueur vedette blessés
        'performance_flags': ['referee_bias'],
        'news_alerts': ['line_movement_suspicious']
    }
    
    test_market_data = {
        'line_movement_pct': -0.18,  # Mouvement ligne -18%
        'volume_anomaly': True,
        'sharp_money_indicator': 'HEAVY_OPPOSING'
    }
    
    black_swan_result = risk_manager.detect_black_swan_events(
        test_game_context, test_market_data, {}
    )
    
    print(f"   🎯 Black Swan Score: {black_swan_result['black_swan_score']:.2f}")
    print(f"   📊 Risk Level: {black_swan_result['risk_level']}")
    print(f"   💡 Recommendation: {black_swan_result['recommendation']}")
    
    if black_swan_result['detected_events']:
        print(f"   🚨 Events détectés:")
        for event in black_swan_result['detected_events']:
            print(f"     • {event['type'].upper()}: {event['event']} (impact: {event['impact']:.1%})")
    
    # Risk-adjusted bet sizing
    print(f"\n⚖️  RISK-ADJUSTED BET SIZING:")
    
    base_kelly = 0.025  # 2.5% Kelly normal
    
    risk_factors = {
        'drawdown_high': risk_manager.calculate_current_drawdown() > 0.10,
        'volatility_high': stop_loss_result['risk_level'] == 'HIGH',
        'black_swan_medium': black_swan_result['risk_level'] in ['MEDIUM', 'HIGH'],
        'black_swan_high': black_swan_result['risk_level'] == 'HIGH',
        'consecutive_losses': len([b for b in recent_betting_history[-3:] if b['outcome'] == 0]) >= 2
    }
    
    sizing_result = risk_manager.risk_adjusted_bet_sizing(base_kelly, risk_factors)
    
    print(f"   📊 Kelly original: {sizing_result['original_kelly']:.1%}")
    print(f"   🛡️ Kelly ajusté: {sizing_result['adjusted_kelly']:.1%}")
    print(f"   📉 Réduction totale: {sizing_result['total_reduction']:.1%}")
    print(f"   💵 Bet final: ${risk_manager.current_bankroll * sizing_result['adjusted_kelly']:.2f}")
    
    if sizing_result['reduction_factors']:
        print(f"   ⚠️  Facteurs réduction:")
        for factor in sizing_result['reduction_factors']:
            print(f"     • {factor}")
    
    print(f"\n🏆 GEMINI RISK PROTECTION ACTIVÉE:")
    print(f"   ✅ Stop-loss automatisé (drawdown, pertes consécutives)")
    print(f"   ✅ Black Swan detection (blessures, anomalies)")
    print(f"   ✅ Bet sizing dynamique ajusté aux risques")
    print(f"   🎯 Protection bankroll: ${risk_manager.current_bankroll:.2f}")

if __name__ == "__main__":
    demo_gemini_risk_management()
