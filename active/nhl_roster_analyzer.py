#!/usr/bin/env python3
"""
🎼 NHL ROSTER ANALYZER - MAESTRO ÉDITION
===============================================
🤖 Analyse joueur par joueur pour pondération équipe
🏒 Focus MTL: Demidov/Hutson hype + Dobson rumors
💎 Intégration quartet IA pour prédictions premium
🎯 Score équipe 0-100 → Performance playoffs/flop
"""

import requests
import sqlite3
from datetime import datetime
import json

class NHLRosterAnalyzer:
    def __init__(self):
        self.db_path = "maestro_roster_analysis.db"
        self.init_database()
        self.nhl_api = "https://api-web.nhle.com/v1"
        
    def init_database(self):
        """🗄️ Base de données pour analyse roster"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS team_analysis (
                team_code TEXT,
                date TEXT,
                roster_score REAL,
                performance_tier TEXT,
                key_players TEXT,
                rumors TEXT,
                hype_factor REAL,
                updated_at TEXT,
                PRIMARY KEY (team_code, date)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                player_id TEXT,
                name TEXT,
                team TEXT,
                position TEXT,
                ovr_rating REAL,
                xg_rating REAL,
                role_weight REAL,
                hype_boost REAL,
                updated_at TEXT,
                PRIMARY KEY (player_id, team)
            )
        ''')
        conn.commit()
        conn.close()

    def get_mtl_2025_roster(self):
        """🏒 Roster MTL 2025-26 avec hype Demidov/Hutson + Dobson rumors"""
        return [
            # FORWARDS - Elite Tier 🔥
            {"name": "Cole Caufield", "position": "RW", "ovr": 92, "xg": 0.85, "hype": 1.0, "role": "sniper"},
            {"name": "Nick Suzuki", "position": "C", "ovr": 90, "xg": 0.72, "hype": 1.0, "role": "captain"},
            {"name": "Ivan Demidov", "position": "RW", "ovr": 88, "xg": 0.68, "hype": 1.15, "role": "prospect_elite"},  # HYPE! 🚀
            {"name": "Juraj Slafkovsky", "position": "LW", "ovr": 86, "xg": 0.65, "hype": 1.05, "role": "power_forward"},
            
            # DEFENSE - Game Changer Addition 💎
            {"name": "Noah Dobson", "position": "D", "ovr": 92, "xg": 0.35, "hype": 1.10, "role": "qb_defense"},  # RUMOR BOOST! 
            {"name": "Lane Hutson", "position": "D", "ovr": 87, "xg": 0.28, "hype": 1.12, "role": "prospect_defense"},  # HYPE! 🌟
            {"name": "Mike Matheson", "position": "D", "ovr": 85, "xg": 0.25, "hype": 1.0, "role": "veteran"},
            
            # GOALIE
            {"name": "Sam Montembeault", "position": "G", "ovr": 83, "xg": 0.0, "hype": 1.0, "role": "starter"},
            
            # DEPTH
            {"name": "Brendan Gallagher", "position": "RW", "ovr": 82, "xg": 0.45, "hype": 1.0, "role": "veteran"},
            {"name": "Christian Dvorak", "position": "C", "ovr": 79, "xg": 0.42, "hype": 1.0, "role": "depth"},
        ]

    def get_team_roster(self, team_code):
        """🎯 Fetch roster pour n'importe quelle équipe (avec fallback MTL)"""
        if team_code.upper() == "MTL":
            return self.get_mtl_2025_roster()
        
        # Pour autres équipes, simulation basée sur strengths connues
        team_presets = {
            "TOR": {"avg_ovr": 87, "strength": "offense", "weakness": "goalie"},
            "BOS": {"avg_ovr": 86, "strength": "defense", "weakness": "age"},
            "PIT": {"avg_ovr": 84, "strength": "veterans", "weakness": "defense"},
            "NYR": {"avg_ovr": 88, "strength": "goalie", "weakness": "depth"},
            "FLA": {"avg_ovr": 89, "strength": "balance", "weakness": "none"},
        }
        
        preset = team_presets.get(team_code.upper(), {"avg_ovr": 82, "strength": "average", "weakness": "unknown"})
        
        # Génère roster simulé
        roster = []
        for i in range(10):  # 10 joueurs clés
            pos = ["C", "LW", "RW", "D", "G"][i % 5]
            ovr = preset["avg_ovr"] + ((-3 + (i % 6)) if i < 6 else -5)  # Top 6 meilleurs
            roster.append({
                "name": f"Player_{i+1}",
                "position": pos,
                "ovr": max(75, ovr),
                "xg": 0.5 if pos != "G" else 0.0,
                "hype": 1.0,
                "role": "regular"
            })
        
        return roster

    def calculate_position_weight(self, position):
        """⚖️ Poids par position pour score équipe"""
        weights = {
            "C": 1.0,    # Centre = impact max
            "LW": 0.95,  # Ailiers 
            "RW": 0.95,
            "D": 0.85,   # Défense importante mais moins que offense
            "G": 0.70    # Gardien impact mais échantillon plus petit
        }
        return weights.get(position, 0.8)

    def get_rumors_boost(self, team_code):
        """📰 Boost basé sur rumeurs/hype actuelles"""
        rumors = {
            "MTL": {
                "dobson_trade": {"boost": 5.0, "prob": 0.7, "source": "insider"},
                "demidov_hype": {"boost": 3.0, "prob": 0.9, "source": "prospect_camp"},
                "hutson_breakout": {"boost": 2.0, "prob": 0.8, "source": "preseason"}
            },
            "TOR": {
                "marner_extension": {"boost": 2.0, "prob": 0.6, "source": "media"}
            }
        }
        
        team_rumors = rumors.get(team_code.upper(), {})
        total_boost = 0
        active_rumors = []
        
        for rumor, data in team_rumors.items():
            if data["prob"] > 0.5:  # Rumeur crédible
                total_boost += data["boost"] * data["prob"]
                active_rumors.append(rumor)
        
        return total_boost, active_rumors

    def analyze_team_performance(self, team_code, date=None):
        """🎯 ANALYSE PRINCIPALE: Score équipe + performance tier"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Récupère roster
        roster = self.get_team_roster(team_code)
        
        # 2. Calcul score base
        total_score = 0
        key_players = []
        
        for player in roster:
            # Score joueur = OVR * poids_position * (1 + xG/2) * hype_factor
            pos_weight = self.calculate_position_weight(player["position"])
            xg_bonus = 1 + (player["xg"] / 2)
            hype_multiplier = player.get("hype", 1.0)
            
            player_score = player["ovr"] * pos_weight * xg_bonus * hype_multiplier
            total_score += player_score
            
            # Identifie joueurs clés (score > 85)
            if player_score > 85:
                key_players.append({
                    "name": player["name"],
                    "score": player_score,
                    "role": player.get("role", "regular")
                })
        
        # 3. Normalise score (0-100)
        base_score = min(total_score / len(roster), 100)
        
        # 4. Ajoute boost rumeurs
        rumors_boost, active_rumors = self.get_rumors_boost(team_code)
        final_score = min(base_score + rumors_boost, 100)
        
        # 5. Détermine performance tier
        if final_score >= 85:
            performance_tier = "ELITE_PLAYOFFS"
            tier_desc = "🏆 Playoffs garantis"
        elif final_score >= 78:
            performance_tier = "GOOD_WILDCARD"  
            tier_desc = "🎯 Wildcard battle"
        elif final_score >= 70:
            performance_tier = "AVERAGE_MIDDLING"
            tier_desc = "📊 Milieu de pack"
        else:
            performance_tier = "WEAK_LOTTERY"
            tier_desc = "🎰 Draft lottery"
        
        # 6. Sauvegarde en DB
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT OR REPLACE INTO team_analysis 
            (team_code, date, roster_score, performance_tier, key_players, rumors, hype_factor, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            team_code.upper(),
            date,
            final_score,
            performance_tier,
            json.dumps([p["name"] for p in key_players[:3]]),  # Top 3
            json.dumps(active_rumors),
            rumors_boost,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        return {
            "team": team_code.upper(),
            "date": date,
            "roster_score": round(final_score, 1),
            "base_score": round(base_score, 1),
            "rumors_boost": round(rumors_boost, 1),
            "performance_tier": performance_tier,
            "tier_description": tier_desc,
            "key_players": [p["name"] for p in sorted(key_players, key=lambda x: x["score"], reverse=True)[:3]],
            "active_rumors": active_rumors,
            "roster_size": len(roster),
            "confidence": 0.85 if team_code.upper() == "MTL" else 0.70  # Plus confiant pour MTL
        }

    def compare_teams(self, team1, team2, date=None):
        """⚔️ Compare 2 équipes pour prédiction H2H"""
        analysis1 = self.analyze_team_performance(team1, date)
        analysis2 = self.analyze_team_performance(team2, date)
        
        score_diff = analysis1["roster_score"] - analysis2["roster_score"]
        
        # Conversion score diff → probabilité
        # Score diff de +10 = ~+15% de chances de gagner
        prob_adjustment = score_diff * 0.015
        base_prob = 0.50  # 50-50 de base
        team1_prob = max(0.15, min(0.85, base_prob + prob_adjustment))
        
        return {
            "team1": analysis1,
            "team2": analysis2,
            "score_difference": round(score_diff, 1),
            "team1_win_prob": round(team1_prob, 3),
            "team2_win_prob": round(1 - team1_prob, 3),
            "confidence": min(analysis1["confidence"], analysis2["confidence"]),
            "edge": "STRONG" if abs(score_diff) > 8 else "MODERATE" if abs(score_diff) > 4 else "WEAK"
        }

# Test rapide
if __name__ == "__main__":
    analyzer = NHLRosterAnalyzer()
    
    print("🎼 MAESTRO ROSTER ANALYZER - Test MTL")
    print("=" * 50)
    
    # Test MTL
    mtl_analysis = analyzer.analyze_team_performance("MTL")
    print(f"🏒 {mtl_analysis['team']}: {mtl_analysis['roster_score']}/100")
    print(f"🎯 Tier: {mtl_analysis['tier_description']}")
    print(f"⭐ Joueurs clés: {', '.join(mtl_analysis['key_players'])}")
    print(f"📰 Rumeurs actives: {mtl_analysis['active_rumors']}")
    print(f"🚀 Boost hype: +{mtl_analysis['rumors_boost']}")
    
    print("\n⚔️ MTL vs PIT Comparison:")
    comparison = analyzer.compare_teams("MTL", "PIT")
    print(f"📊 MTL: {comparison['team1']['roster_score']} vs PIT: {comparison['team2']['roster_score']}")
    print(f"🎯 MTL win prob: {comparison['team1_win_prob']*100:.1f}%")
    print(f"💪 Edge: {comparison['edge']}")
