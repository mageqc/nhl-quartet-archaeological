# 🚀 NHL Ultimate API Service v4.0 - Recommandations ChatGPT
# Intégration temps réel du système révolutionnaire avec Grok + ChatGPT

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# FastAPI setup (simulation si pas installé)
try:
    import uvicorn
    from fastapi import FastAPI, Body, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    print("⚠️ FastAPI non installé - Mode simulation activé")
    FASTAPI_AVAILABLE = False
    
    # Simulation classes pour développement
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    class FastAPI:
        def __init__(self, **kwargs):
            self.routes = {}
        def get(self, path): return lambda f: f
        def post(self, path): return lambda f: f

# Import système v4.0
USE_PURE = bool(int(os.getenv("USE_PURE", "1")))

try:
    if USE_PURE:
        from nhl_ultimate_v4_pure import NHLUltimateSystemV4
    else:
        from nhl_ultimate_v4 import NHLUltimateSystemV4
    NHL_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️ Système NHL v4.0 non trouvé - Mode simulation")
    NHL_SYSTEM_AVAILABLE = False

# Modèles Pydantic selon ChatGPT
class GamePayload(BaseModel):
    date: str
    home_team: str
    away_team: str
    market: str = "WIN"
    total_line: Optional[float] = None
    odds: float = 1.80
    context: Dict = {}

class WeekPayload(BaseModel):
    start_date: str
    end_date: str
    games: List[GamePayload]

class RecommendationResponse(BaseModel):
    status: str
    confidence: float
    expected_value: float
    recommended_fraction: float
    risk_metrics: Dict
    grok_enhancements: Dict
    reasoning: List[str]

# Initialisation API
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="NHL Ultimate API v4.0", 
        version="4.0-Grok-ChatGPT",
        description="API temps réel intégrant recommandations Grok + ChatGPT"
    )
else:
    app = FastAPI()

# Initialisation moteur NHL
if NHL_SYSTEM_AVAILABLE:
    engine = NHLUltimateSystemV4()
    print("✅ Moteur NHL Ultimate v4.0 initialisé")
else:
    engine = None
    print("⚠️ Mode simulation - moteur NHL non disponible")

class NHLAPIService:
    """
    Service API NHL Ultimate v4.0
    Implémentant recommandations ChatGPT + algorithmes Grok
    """
    
    def __init__(self):
        self.engine = engine
        self.request_count = 0
        self.performance_cache = {}
        
        # Configuration selon ChatGPT
        self.calibration_config = {
            'confidence_threshold': 0.68,    # ChatGPT: 0.75 → 0.68-0.70
            'ev_minimal': 0.015,             # ChatGPT: 0.02 → 0.015
            'correlation_max': 0.70,         # ChatGPT: 0.60 → 0.70
            'var_gate_medium_risk': True,    # ChatGPT: autoriser medium risk si hedge
            'webhook_ev_threshold': 0.03,    # ChatGPT: alertes si EV > 0.03
            'webhook_fraction_threshold': 0.12  # ChatGPT: alertes si fraction > 0.12
        }
    
    def analyze_game_enhanced(self, game_data: Dict) -> Dict:
        """
        Analyse de match avec calibration ChatGPT + algorithmes Grok
        """
        start_time = time.time()
        
        if not self.engine:
            return self.simulate_analysis(game_data)
        
        try:
            # Analyse avec moteur v4.0 (Grok algorithms)
            base_analysis = self.engine.analyze_single_game_enhanced(game_data)
            
            # Application calibration ChatGPT
            calibrated_result = self.apply_chatgpt_calibration(base_analysis)
            
            # Ajout métriques temps réel
            execution_time = time.time() - start_time
            calibrated_result['performance'] = {
                'execution_time': execution_time,
                'grok_algorithms_active': True,
                'chatgpt_calibration_applied': True,
                'request_id': self.request_count
            }
            
            self.request_count += 1
            return calibrated_result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'fallback': self.simulate_analysis(game_data)
            }
    
    def apply_chatgpt_calibration(self, base_analysis: Dict) -> Dict:
        """
        Application des ajustements de seuils recommandés par ChatGPT
        """
        config = self.calibration_config
        
        # Ajustement seuil confiance (ChatGPT: 0.75 → 0.68-0.70)
        original_confidence = base_analysis.get('confidence', 0)
        adjusted_confidence = max(0, original_confidence - 0.05)  # Plus permissif
        
        # Ajustement EV minimal (ChatGPT: 0.02 → 0.015)
        original_ev = base_analysis.get('expected_value', 0)
        ev_meets_threshold = original_ev >= config['ev_minimal']
        
        # Gestion risque médium si hedge disponible (ChatGPT)
        hedge_available = base_analysis.get('hedging_opportunities', [])
        allow_medium_risk = len(hedge_available) > 0 and config['var_gate_medium_risk']
        
        # Décision finale selon calibration ChatGPT
        recommendation_status = "PASS"
        if adjusted_confidence >= config['confidence_threshold'] and ev_meets_threshold:
            recommendation_status = "RECOMMEND"
        elif allow_medium_risk and adjusted_confidence >= 0.60:
            recommendation_status = "CONDITIONAL_RECOMMEND"
        
        # Webhook alertes selon ChatGPT
        webhook_triggered = (
            original_ev > config['webhook_ev_threshold'] or
            base_analysis.get('recommended_fraction', 0) > config['webhook_fraction_threshold']
        )
        
        return {
            'status': recommendation_status,
            'confidence': adjusted_confidence,
            'original_confidence': original_confidence,
            'expected_value': original_ev,
            'recommended_fraction': base_analysis.get('recommended_fraction', 0),
            'risk_metrics': base_analysis.get('risk_metrics', {}),
            'hedging_opportunities': hedge_available,
            'grok_enhancements': base_analysis.get('grok_features', {}),
            'chatgpt_calibration': {
                'confidence_adjustment': -0.05,
                'ev_threshold_lowered': True,
                'medium_risk_allowed': allow_medium_risk,
                'webhook_triggered': webhook_triggered
            },
            'reasoning': self.generate_reasoning(base_analysis, adjusted_confidence, ev_meets_threshold)
        }
    
    def simulate_analysis(self, game_data: Dict) -> Dict:
        """
        Simulation pour développement sans moteur
        """
        import random
        
        confidence = random.uniform(0.60, 0.90)
        ev = random.uniform(0.005, 0.05)
        
        return {
            'status': 'SIMULATED',
            'confidence': confidence,
            'expected_value': ev,
            'recommended_fraction': ev * 0.25,
            'risk_metrics': {'var_99': random.uniform(0.05, 0.15)},
            'grok_enhancements': {'patterns_discovered': random.randint(5, 15)},
            'reasoning': [f"Simulation pour {game_data.get('home_team', 'HOME')} vs {game_data.get('away_team', 'AWAY')}"]
        }
    
    def generate_reasoning(self, analysis: Dict, confidence: float, ev_meets: bool) -> List[str]:
        """
        Génération de raisonnement selon algorithmes Grok + calibration ChatGPT
        """
        reasons = []
        
        # Grok features
        if analysis.get('grok_features', {}).get('variational_bayesian_active'):
            reasons.append("✅ Pondération bayésienne variationnelle active (Grok)")
        
        if analysis.get('grok_features', {}).get('patterns_discovered', 0) > 0:
            count = analysis['grok_features']['patterns_discovered']
            reasons.append(f"🔍 {count} patterns auto-découverts (Grok)")
        
        # ChatGPT calibration
        if confidence >= 0.68:
            reasons.append("📈 Confiance ajustée selon calibration ChatGPT (0.68+)")
        
        if ev_meets:
            reasons.append("💰 Expected Value supérieur au seuil ChatGPT (0.015+)")
        
        # Risk management
        var_risk = analysis.get('risk_metrics', {}).get('var_99', 0)
        if var_risk < 0.12:
            reasons.append(f"🛡️ Risque VaR acceptable ({var_risk:.3f})")
        
        return reasons

# Instance service
api_service = NHLAPIService()

# Routes API selon ChatGPT
@app.get("/health")
def health():
    """Health check avec status système"""
    return {
        "status": "ok",
        "model_version": "v4.0_grok_chatgpt",
        "pure_python": USE_PURE,
        "grok_algorithms": engine is not None,
        "time": datetime.now().isoformat(),
        "requests_processed": api_service.request_count
    }

@app.post("/analyze/game")
def analyze_game(payload: GamePayload):
    """
    Analyse de match unique selon recommandations ChatGPT + Grok
    """
    game_data = {
        "date": payload.date,
        "home_team": payload.home_team,
        "away_team": payload.away_team,
        "market": payload.market,
        "total_line": payload.total_line,
        "odds": payload.odds,
        **payload.context
    }
    
    result = api_service.analyze_game_enhanced(game_data)
    
    return {
        "ok": True,
        "input": payload.model_dump(),
        "result": result,
        "api_version": "v4.0-ChatGPT-Grok",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze/week")
def analyze_week(payload: WeekPayload):
    """
    Analyse semaine complète selon recommandations ChatGPT
    """
    games = [g.model_dump() for g in payload.games]
    results = []
    recommendations = []
    
    for game_data in games:
        game_payload = GamePayload(**game_data)
        result = analyze_game(game_payload)
        results.append(result["result"])
        
        # Collecte recommandations selon ChatGPT
        if result["result"]["status"] in ["RECOMMEND", "CONDITIONAL_RECOMMEND"]:
            recommendations.append({
                "game": f"{game_data['away_team']} @ {game_data['home_team']}",
                "market": game_data.get('market', 'WIN'),
                "confidence": result["result"]["confidence"],
                "expected_value": result["result"]["expected_value"],
                "reasoning": result["result"]["reasoning"]
            })
    
    # Webhook simulation selon ChatGPT
    high_value_picks = [r for r in recommendations if r["expected_value"] > 0.03]
    
    return {
        "ok": True,
        "window": {"from": payload.start_date, "to": payload.end_date},
        "total_games": len(results),
        "recommendations_count": len(recommendations),
        "high_value_picks": len(high_value_picks),
        "results": results,
        "recommendations": recommendations,
        "chatgpt_features": {
            "calibration_applied": True,
            "webhook_candidates": len(high_value_picks),
            "api_timestamp": datetime.now().isoformat()
        }
    }

@app.get("/calibration/status")
def calibration_status():
    """
    Status de la calibration ChatGPT
    """
    return {
        "calibration_config": api_service.calibration_config,
        "chatgpt_improvements": {
            "confidence_threshold_lowered": "0.75 → 0.68",
            "ev_threshold_lowered": "0.02 → 0.015", 
            "correlation_max_increased": "0.60 → 0.70",
            "medium_risk_hedge_enabled": True
        },
        "performance": {
            "requests_processed": api_service.request_count,
            "cache_entries": len(api_service.performance_cache)
        }
    }

def main():
    """
    Lancement service selon recommandations ChatGPT
    """
    print("🚀 NHL Ultimate API v4.0 - Grok + ChatGPT")
    print("=" * 50)
    print(f"🧠 Grok algorithms: {'✅ Active' if engine else '⚠️ Simulation'}")
    print(f"⚡ ChatGPT calibration: ✅ Active")
    print(f"🐍 Pure Python mode: {'✅' if USE_PURE else '❌'}")
    print(f"🌐 FastAPI available: {'✅' if FASTAPI_AVAILABLE else '⚠️ Simulation'}")
    
    if FASTAPI_AVAILABLE:
        port = int(os.getenv("PORT", "8000"))
        print(f"\n🌍 Démarrage serveur sur http://0.0.0.0:{port}")
        print("📡 Endpoints disponibles:")
        print(f"   GET  /health - Status système")
        print(f"   POST /analyze/game - Match unique")
        print(f"   POST /analyze/week - Semaine complète")
        print(f"   GET  /calibration/status - Config ChatGPT")
        
        try:
            uvicorn.run(app, host="0.0.0.0", port=port)
        except ImportError:
            print("⚠️ uvicorn non installé - utiliser: pip install uvicorn")
    else:
        print("\n📋 Mode développement - Tests disponibles:")
        
        # Tests en mode simulation
        test_game = GamePayload(
            date="2025-10-08",
            home_team="TOR", 
            away_team="MTL",
            market="TOTAL",
            total_line=6.5,
            odds=1.85,
            context={"rivalry_factor": 10}
        )
        
        print("\n🧪 Test analyse match:")
        result = analyze_game(test_game)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
