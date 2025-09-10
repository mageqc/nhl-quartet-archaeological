#!/usr/bin/env python3
"""
🚀 ANALYSEUR NHL OPTIMISÉ - Version Expert v2.0
Implémentation des recommandations de l'IA expert pour maximiser performance
"""

import sys
import os
import json
import time
import math
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict, deque

# Configuration optimisée selon recommandations expert
ENHANCED_CONFIG = {
    "bankroll_total": 1076,
    "max_drawdown_pct": 0.15,  # Stop-loss à 15% comme recommandé
    "kelly_factors": {
        "high_confidence": 0.7,    # Moins conservateur pour haute confiance
        "medium_confidence": 0.6,  # Standard
        "low_confidence": 0.5      # Plus conservateur
    },
    "weights_dynamic": {
        "early_season": {
            "home_advantage": 0.35,
            "recent_form": 0.25,
            "head_to_head": 0.20,
            "external_factors": 0.15,
            "advanced_analytics": 0.05
        },
        "late_season": {
            "home_advantage": 0.25,
            "recent_form": 0.25,
            "head_to_head": 0.20,
            "external_factors": 0.15,
            "advanced_analytics": 0.15
        }
    },
    "correlation_threshold": 0.6,  # Limite corrélation entre paris
    "confidence_thresholds": {
        "elite": 75,
        "standard": 50,
        "minimum": 40
    }
}

class NHLAnalyzerEnhanced:
    """
    Analyseur NHL optimisé selon recommandations IA expert.
    Focus sur améliorations les plus impactantes.
    """
    
    def __init__(self):
        self.config = ENHANCED_CONFIG
        self.current_drawdown = 0
        self.performance_buffer = deque(maxlen=50)
        self.correlation_matrix = {}
        self.db_path = "nhl_enhanced.db"
        
        self.init_enhanced_database()
        print("🚀 Analyseur NHL Enhanced v2.0 initialisé")

    def init_enhanced_database(self):
        """Initialise base de données optimisée pour performance."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            
            # Table stats équipes avec métriques avancées
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS team_advanced_stats (
                    team_id TEXT,
                    season TEXT,
                    home_win_rate REAL,
                    away_win_rate REAL,
                    goals_for_avg REAL,
                    goals_against_avg REAL,
                    xg_for_pct REAL DEFAULT 0.5,
                    corsi_for_pct REAL DEFAULT 0.5,
                    fenwick_for_pct REAL DEFAULT 0.5,
                    pdo REAL DEFAULT 1.0,
                    faceoff_win_pct REAL DEFAULT 0.5,
                    sv_pct REAL DEFAULT 0.9,
                    PRIMARY KEY (team_id, season)
                )
            ''')
            
            # Table résultats pour backtesting
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS betting_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    matchup TEXT,
                    prediction_type TEXT,
                    confidence_score REAL,
                    bet_amount REAL,
                    actual_outcome INTEGER,
                    roi REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("✅ Base de données enhanced initialisée")
            
        except Exception as e:
            print(f"⚠️ Erreur DB: {e}")

    def calculate_confidence_enhanced(self, match_data, season_progress=None):
        """
        ALGORITHME DE CONFIANCE OPTIMISÉ selon recommandations expert.
        
        Améliorations:
        - Pondération dynamique selon saison
        - Intégration métriques avancées
        - Gestion variance et incertitude
        """
        
        if season_progress is None:
            season_progress = self.calculate_season_progress(match_data.get('date', datetime.now()))
        
        # Sélection poids selon progression saison
        if season_progress < 0.3:  # Début saison
            weights = self.config["weights_dynamic"]["early_season"]
        else:  # Fin saison
            weights = self.config["weights_dynamic"]["late_season"]
        
        score_components = {}
        
        # 1. AVANTAGE DOMICILE (ajusté dynamiquement)
        home_advantage = self.calculate_home_advantage_enhanced(match_data)
        score_components['home_advantage'] = weights['home_advantage'] * 100 * home_advantage
        
        # 2. FORME RÉCENTE avec momentum
        recent_form = self.analyze_recent_form_enhanced(match_data)
        score_components['recent_form'] = weights['recent_form'] * 100 * recent_form
        
        # 3. HEAD-TO-HEAD historique
        h2h_score = self.analyze_h2h_enhanced(match_data)
        score_components['head_to_head'] = weights['head_to_head'] * 100 * h2h_score
        
        # 4. FACTEURS EXTERNES (blessures, repos, etc.)
        external_factors = self.analyze_external_factors_enhanced(match_data)
        score_components['external_factors'] = weights['external_factors'] * 100 * external_factors
        
        # 5. ANALYTICS AVANCÉES (xG, Corsi, etc.)
        advanced_score = self.calculate_advanced_analytics_enhanced(match_data)
        score_components['advanced_analytics'] = weights['advanced_analytics'] * 100 * advanced_score
        
        # Score total
        total_score = sum(score_components.values())
        
        # Normalisation 0-100
        final_score = min(100, max(0, total_score))
        
        return {
            'confidence_score': final_score,
            'components': score_components,
            'weights_used': weights,
            'season_progress': season_progress
        }

    def calculate_home_advantage_enhanced(self, match_data):
        """Calcul avantage domicile avec facteurs contextuels."""
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Stats de base (simulation avec données historiques)
        home_stats = self.get_team_stats_enhanced(home_team)
        away_stats = self.get_team_stats_enhanced(away_team)
        
        # Différentiel performance
        home_win_rate = home_stats.get('home_win_rate', 0.6)
        away_win_rate = away_stats.get('away_win_rate', 0.4)
        
        performance_gap = home_win_rate - away_win_rate
        
        # Facteurs contextuels additionnels
        context_bonus = 0
        
        # Facteur altitude (Colorado, Calgary)
        if home_team in ['COL', 'CGY']:
            context_bonus += 0.05
        
        # Facteur voyage (simulation fatigue)
        if self.is_long_travel(away_team, match_data):
            context_bonus += 0.03
        
        # Normalisation avec sigmoid optimisé
        base_advantage = self.sigmoid_optimized((performance_gap + context_bonus) * 2)
        
        return base_advantage

    def analyze_recent_form_enhanced(self, match_data):
        """Analyse forme récente avec momentum."""
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Simulation forme récente (10 derniers matchs)
        home_form = self.simulate_recent_form(home_team)
        away_form = self.simulate_recent_form(away_team)
        
        # Calcul différentiel avec momentum
        form_differential = home_form['win_rate'] - away_form['win_rate']
        momentum_factor = home_form['momentum'] - away_form['momentum']
        
        # Score combiné
        combined_score = 0.5 + (form_differential * 0.6) + (momentum_factor * 0.4)
        
        return min(1.0, max(0.0, combined_score))

    def analyze_h2h_enhanced(self, match_data):
        """Analyse historique tête-à-tête."""
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Vérification rivalité spéciale
        rivalry_bonus = self.get_rivalry_bonus(home_team, away_team)
        
        # Simulation H2H historique
        h2h_win_rate = self.simulate_h2h_history(home_team, away_team)
        
        return min(1.0, h2h_win_rate + rivalry_bonus)

    def analyze_external_factors_enhanced(self, match_data):
        """Facteurs externes selon recommandations expert."""
        external_score = 0.5  # Base neutre
        
        # Facteur repos/fatigue
        rest_advantage = self.calculate_rest_advantage(match_data)
        external_score += rest_advantage * 0.2
        
        # Facteur blessures (simulation)
        injury_impact = self.simulate_injury_impact(match_data)
        external_score += injury_impact * 0.15
        
        # Facteur actualités (simulation sentiment)
        news_impact = self.simulate_news_sentiment(match_data)
        external_score += news_impact * 0.1
        
        return min(1.0, max(0.0, external_score))

    def calculate_advanced_analytics_enhanced(self, match_data):
        """Analytics avancées selon pondération expert."""
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Récupération stats avancées
        home_advanced = self.get_advanced_stats(home_team)
        away_advanced = self.get_advanced_stats(away_team)
        
        # Calcul différentiels selon pondération recommandée
        xg_diff = home_advanced['xg_for_pct'] - away_advanced['xg_for_pct']
        corsi_diff = home_advanced['corsi_for_pct'] - away_advanced['corsi_for_pct']
        fenwick_diff = home_advanced['fenwick_for_pct'] - away_advanced['fenwick_for_pct']
        pdo_diff = home_advanced['pdo'] - away_advanced['pdo']
        faceoff_diff = home_advanced['faceoff_win_pct'] - away_advanced['faceoff_win_pct']
        
        # Score pondéré selon recommandations expert
        advanced_score = (
            xg_diff * 0.40 +      # 40% xG comme recommandé
            corsi_diff * 0.25 +   # 25% Corsi
            fenwick_diff * 0.20 + # 20% Fenwick
            pdo_diff * 0.10 +     # 10% PDO
            faceoff_diff * 0.05   # 5% Faceoffs
        )
        
        # Normalisation
        return self.sigmoid_optimized(advanced_score * 3)

    def kelly_criterion_enhanced(self, win_probability, odds):
        """
        Kelly Criterion optimisé selon recommandations expert.
        
        Améliorations:
        - Facteurs ajustés selon confiance
        - Stop-loss automatique
        - Gestion corrélation
        """
        
        # Vérification stop-loss (15% max drawdown)
        if self.current_drawdown > (self.config["bankroll_total"] * self.config["max_drawdown_pct"]):
            return {
                'amount': 0,
                'reason': 'STOP-LOSS ACTIVÉ',
                'drawdown_pct': (self.current_drawdown / self.config["bankroll_total"]) * 100
            }
        
        # Kelly de base
        b = odds - 1
        p = win_probability
        q = 1 - p
        
        kelly_raw = (b * p - q) / b
        
        # Facteur conservateur selon confiance
        if win_probability >= 0.80:
            adjustment = self.config["kelly_factors"]["high_confidence"]
        elif win_probability >= 0.65:
            adjustment = self.config["kelly_factors"]["medium_confidence"]
        else:
            adjustment = self.config["kelly_factors"]["low_confidence"]
        
        # Kelly ajusté
        kelly_adjusted = max(0, kelly_raw * adjustment)
        
        # Limitation sécurité (5% max bankroll)
        final_fraction = min(0.05, kelly_adjusted)
        bet_amount = self.config["bankroll_total"] * final_fraction
        
        return {
            'amount': round(bet_amount, 2),
            'fraction': final_fraction,
            'kelly_raw': kelly_raw,
            'adjustment_factor': adjustment,
            'confidence_level': self.categorize_confidence(win_probability)
        }

    def generate_recommendation_enhanced(self, match_data):
        """Génère recommandation optimisée."""
        
        # 1. Calcul confiance avec algorithme amélioré
        confidence_analysis = self.calculate_confidence_enhanced(match_data)
        confidence_score = confidence_analysis['confidence_score']
        
        # 2. Filtrage selon seuils
        if confidence_score < self.config["confidence_thresholds"]["minimum"]:
            return None
        
        # 3. Détermination type de pari optimal
        bet_recommendation = self.determine_optimal_bet_type(match_data, confidence_score)
        
        if not bet_recommendation:
            return None
        
        # 4. Calcul mise avec Kelly enhanced
        win_probability = confidence_score / 100
        bet_sizing = self.kelly_criterion_enhanced(win_probability, bet_recommendation['expected_odds'])
        
        if bet_sizing['amount'] == 0:
            return None
        
        # 5. Recommandation finale
        return {
            'date': match_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'matchup': f"{match_data.get('away_team', 'TBD')} @ {match_data.get('home_team', 'TBD')}",
            'type': bet_recommendation['type'],
            'selection': bet_recommendation['selection'],
            'expected_odds': bet_recommendation['expected_odds'],
            'confidence_score': confidence_score,
            'bet_amount': bet_sizing['amount'],
            'reasoning': bet_recommendation['reasoning'],
            'kelly_info': bet_sizing,
            'confidence_analysis': confidence_analysis,
            'version': 'ENHANCED_V2'
        }

    def determine_optimal_bet_type(self, match_data, confidence_score):
        """Détermine type de pari optimal selon patterns."""
        
        home_team = match_data.get('home_team', '')
        away_team = match_data.get('away_team', '')
        
        # Pattern 1: Rivalité MTL-TOR = TOTAL
        if self.is_intense_rivalry(home_team, away_team):
            return {
                'type': 'TOTAL',
                'selection': 'Plus de 6.5 buts',
                'expected_odds': 1.85,
                'reasoning': f'Rivalité intense {home_team}-{away_team}'
            }
        
        # Pattern 2: Montreal visiteur = GAGNANT domicile
        if away_team == 'MTL' and self.is_strong_home_team(home_team):
            return {
                'type': 'GAGNANT',
                'selection': home_team,
                'expected_odds': 1.65,
                'reasoning': 'Pattern Montreal faiblesse visiteur'
            }
        
        # Pattern 3: Domicile dominant général
        home_advantage = self.calculate_home_advantage_enhanced(match_data)
        if home_advantage > 0.7:
            return {
                'type': 'GAGNANT',
                'selection': home_team,
                'expected_odds': self.calculate_dynamic_odds(home_advantage),
                'reasoning': f'Domicile dominant ({home_advantage*100:.0f}%)'
            }
        
        return None

    def analyze_complete_season_enhanced(self):
        """
        Analyse complète saison avec optimisations expert.
        """
        
        print("🚀 ANALYSE COMPLÈTE SAISON NHL 2025-26 - VERSION ENHANCED")
        print("=" * 70)
        
        start_time = time.time()
        
        # Simulation calendrier complet
        all_recommendations = []
        total_matches = 1312
        
        print(f"📊 Analyse de {total_matches} matchs avec algorithmes optimisés...")
        
        # Simulation analyse match par match
        for i in range(total_matches):
            # Simulation données match
            match_data = self.simulate_match_data(i)
            
            # Analyse avec algorithme enhanced
            recommendation = self.generate_recommendation_enhanced(match_data)
            
            if recommendation:
                all_recommendations.append(recommendation)
            
            # Progress
            if (i + 1) % 100 == 0:
                print(f"  ✅ {i + 1}/{total_matches} matchs analysés")
        
        # Filtrage corrélation selon recommandations expert
        filtered_recommendations = self.filter_correlated_bets(all_recommendations)
        
        # Calcul métriques finales
        final_metrics = self.calculate_final_metrics(filtered_recommendations)
        
        execution_time = time.time() - start_time
        
        # Rapport final
        print("\n📈 RÉSULTATS ANALYSE ENHANCED:")
        print(f"⏱️  Temps exécution: {execution_time:.1f}s")
        print(f"🎯 Valeurs sûres identifiées: {len(filtered_recommendations)}")
        print(f"📊 Taux opportunités: {len(filtered_recommendations)/total_matches*100:.1f}%")
        print(f"💰 Budget total recommandé: {final_metrics['total_budget']}$")
        print(f"📈 ROI projeté: {final_metrics['projected_roi']:.1f}%")
        print(f"🛡️  Drawdown maximum: {final_metrics['max_drawdown']:.1f}%")
        
        # Répartition par type
        type_distribution = self.analyze_bet_type_distribution(filtered_recommendations)
        print(f"\n🎲 RÉPARTITION PAR TYPE:")
        for bet_type, count in type_distribution.items():
            print(f"  {bet_type}: {count} paris ({count/len(filtered_recommendations)*100:.1f}%)")
        
        return {
            'recommendations': filtered_recommendations,
            'metrics': final_metrics,
            'execution_time': execution_time,
            'version': 'ENHANCED_V2'
        }

    # FONCTIONS UTILITAIRES

    def sigmoid_optimized(self, x, steepness=1.0, midpoint=0.0):
        """Sigmoid optimisé pour normalisation."""
        try:
            return 1 / (1 + math.exp(-steepness * (x - midpoint)))
        except OverflowError:
            return 1.0 if x > midpoint else 0.0

    def calculate_season_progress(self, date):
        """Calcule progression saison (0-1)."""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        # Saison NHL: Octobre à Avril
        if date.month >= 10:  # Oct-Dec
            progress = (date.month - 10) / 6
        else:  # Jan-Avril
            progress = 0.5 + (date.month / 4) / 2
        
        return min(1.0, max(0.0, progress))

    def get_team_stats_enhanced(self, team_id):
        """Récupère stats équipe de la DB."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM team_advanced_stats 
                WHERE team_id = ? AND season = '2024-25'
            ''', (team_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'home_win_rate': result[2] or 0.6,
                    'away_win_rate': result[3] or 0.4,
                    'goals_for_avg': result[4] or 3.0,
                    'goals_against_avg': result[5] or 3.0
                }
        except:
            pass
        
        # Valeurs par défaut selon équipe
        return self.get_default_team_stats(team_id)

    def get_advanced_stats(self, team_id):
        """Récupère stats avancées."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT xg_for_pct, corsi_for_pct, fenwick_for_pct, pdo, faceoff_win_pct
                FROM team_advanced_stats 
                WHERE team_id = ? AND season = '2024-25'
            ''', (team_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'xg_for_pct': result[0] or 0.5,
                    'corsi_for_pct': result[1] or 0.5,
                    'fenwick_for_pct': result[2] or 0.5,
                    'pdo': result[3] or 1.0,
                    'faceoff_win_pct': result[4] or 0.5
                }
        except:
            pass
        
        # Valeurs par défaut
        return {
            'xg_for_pct': 0.5,
            'corsi_for_pct': 0.5,
            'fenwick_for_pct': 0.5,
            'pdo': 1.0,
            'faceoff_win_pct': 0.5
        }

    def get_default_team_stats(self, team_id):
        """Stats par défaut selon équipe (simulation données réelles)."""
        
        # Équipes élite
        if team_id in ['BOS', 'DAL', 'COL', 'FLA']:
            return {
                'home_win_rate': 0.82,
                'away_win_rate': 0.45,
                'goals_for_avg': 3.5,
                'goals_against_avg': 2.3
            }
        
        # Équipes moyennes
        elif team_id in ['VAN', 'NYR', 'CAR', 'NJD']:
            return {
                'home_win_rate': 0.68,
                'away_win_rate': 0.42,
                'goals_for_avg': 3.0,
                'goals_against_avg': 2.8
            }
        
        # Équipes faibles (Montreal inclus)
        else:
            return {
                'home_win_rate': 0.45,
                'away_win_rate': 0.25,
                'goals_for_avg': 2.5,
                'goals_against_avg': 3.5
            }

    def simulate_match_data(self, match_index):
        """Simule données match pour testing."""
        
        teams = ['BOS', 'TOR', 'MTL', 'NYR', 'FLA', 'COL', 'DAL', 'VAN', 'CAR', 'NJD', 
                'CGY', 'EDM', 'VGK', 'MIN', 'STL', 'WPG', 'ANA', 'CHI', 'DET', 'OTT']
        
        import random
        random.seed(match_index)  # Reproductible
        
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t != home_team])
        
        # Date simulation (saison 2025-26)
        start_date = datetime(2025, 10, 8)
        game_date = start_date + timedelta(days=match_index // 10)
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'date': game_date.strftime('%Y-%m-%d'),
            'game_id': f"2025{match_index:04d}"
        }

    def is_intense_rivalry(self, home_team, away_team):
        """Détecte rivalités intenses."""
        rivalries = [
            ('MTL', 'TOR'), ('MTL', 'BOS'), ('NYR', 'NJD'), 
            ('EDM', 'CGY'), ('LA', 'ANA')
        ]
        
        matchup = tuple(sorted([home_team, away_team]))
        return matchup in [(tuple(sorted(r))) for r in rivalries]

    def is_strong_home_team(self, team_id):
        """Vérifie si équipe domicile forte."""
        strong_home_teams = ['BOS', 'DAL', 'COL', 'FLA', 'NYR', 'CAR', 'NJD', 'VGK']
        return team_id in strong_home_teams

    def filter_correlated_bets(self, recommendations):
        """Filtre paris corrélés selon seuil expert."""
        
        filtered = []
        daily_counts = defaultdict(int)
        
        for rec in recommendations:
            date = rec['date']
            
            # Limite 3 paris par jour selon recommandations
            if daily_counts[date] >= 3:
                continue
            
            # Vérification corrélation (simulation)
            correlation_score = self.calculate_correlation_score(rec, filtered)
            
            if correlation_score < self.config["correlation_threshold"]:
                filtered.append(rec)
                daily_counts[date] += 1
        
        return filtered

    def calculate_correlation_score(self, new_rec, existing_recs):
        """Calcule score corrélation simplifié."""
        if not existing_recs:
            return 0.0
        
        # Vérification même date
        same_date_count = sum(1 for r in existing_recs 
                             if r['date'] == new_rec['date'])
        
        if same_date_count >= 2:
            return 0.8  # Corrélation élevée
        
        return 0.3  # Corrélation faible

    def calculate_final_metrics(self, recommendations):
        """Calcule métriques finales."""
        
        if not recommendations:
            return {
                'total_budget': 0,
                'projected_roi': 0,
                'max_drawdown': 0
            }
        
        total_budget = sum(r['bet_amount'] for r in recommendations)
        
        # Projection ROI (simulation 75% réussite)
        expected_wins = len(recommendations) * 0.75
        expected_losses = len(recommendations) * 0.25
        
        total_returns = sum(r['bet_amount'] * r['expected_odds'] for r in recommendations) * 0.75
        total_losses = sum(r['bet_amount'] for r in recommendations) * 0.25
        
        net_profit = total_returns - total_budget
        projected_roi = (net_profit / total_budget) * 100 if total_budget > 0 else 0
        
        # Drawdown maximum estimé
        max_drawdown = 15.0  # Conservative selon recommandations
        
        return {
            'total_budget': round(total_budget, 2),
            'projected_roi': round(projected_roi, 1),
            'max_drawdown': max_drawdown,
            'expected_profit': round(net_profit, 2)
        }

    def analyze_bet_type_distribution(self, recommendations):
        """Analyse répartition types de paris."""
        distribution = defaultdict(int)
        
        for rec in recommendations:
            distribution[rec['type']] += 1
        
        return dict(distribution)

    # Fonctions simulation pour testing
    def simulate_recent_form(self, team_id):
        """Simule forme récente équipe."""
        if team_id == 'MTL':
            return {'win_rate': 0.3, 'momentum': -0.2}
        elif team_id in ['BOS', 'DAL', 'COL']:
            return {'win_rate': 0.7, 'momentum': 0.1}
        else:
            return {'win_rate': 0.5, 'momentum': 0.0}

    def simulate_h2h_history(self, home_team, away_team):
        """Simule historique H2H."""
        if home_team in ['BOS', 'DAL', 'COL'] and away_team == 'MTL':
            return 0.75
        return 0.55

    def get_rivalry_bonus(self, home_team, away_team):
        """Bonus rivalité."""
        if self.is_intense_rivalry(home_team, away_team):
            return 0.1
        return 0.0

    def calculate_rest_advantage(self, match_data):
        """Simule avantage repos."""
        return 0.0  # Neutral par défaut

    def simulate_injury_impact(self, match_data):
        """Simule impact blessures."""
        return 0.0  # Neutral par défaut

    def simulate_news_sentiment(self, match_data):
        """Simule sentiment actualités."""
        return 0.0  # Neutral par défaut

    def is_long_travel(self, team_id, match_data):
        """Simule voyage long."""
        return False  # Par défaut

    def calculate_dynamic_odds(self, advantage):
        """Calcule cotes dynamiques."""
        base_odds = 1.65
        if advantage > 0.8:
            return 1.55
        elif advantage > 0.6:
            return 1.60
        return base_odds

    def categorize_confidence(self, probability):
        """Catégorise confiance."""
        if probability >= 0.80:
            return 'TRÈS_ÉLEVÉE'
        elif probability >= 0.65:
            return 'ÉLEVÉE'
        elif probability >= 0.55:
            return 'MOYENNE'
        return 'FAIBLE'

def main():
    """Fonction principale enhanced."""
    
    print("🏒 DÉMARRAGE ANALYSEUR NHL ENHANCED V2.0")
    print("Implémentation recommandations IA expert")
    print("=" * 60)
    
    # Initialisation analyseur enhanced
    analyzer = NHLAnalyzerEnhanced()
    
    # Analyse complète saison
    results = analyzer.analyze_complete_season_enhanced()
    
    # Sauvegarde résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"analyse_enhanced_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Conversion datetime pour JSON
        results_serializable = {}
        for key, value in results.items():
            if key == 'recommendations':
                results_serializable[key] = value
            else:
                results_serializable[key] = value
        
        json.dump(results_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés: {filename}")
    print("🚀 Analyse Enhanced terminée avec succès!")
    
    return results

if __name__ == "__main__":
    main()
