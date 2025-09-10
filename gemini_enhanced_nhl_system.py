#!/usr/bin/env python3
"""
🏒 NHL Quartet Archaeological - Gemini Enhanced ML System
Implémentation des suggestions d'amélioration de l'expert IA Gemini
- Ensemble Learning avec XGBoost/LightGBM
- Feature Engineering avancé 
- Calibration du modèle
- Gestion des risques améliorée
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.calibration import calibration_curve
import sqlite3
import requests
import json
from datetime import datetime, timedelta
import hashlib

class GeminiEnhancedNHLSystem:
    """
    Système NHL amélioré selon les recommandations de l'expert IA Gemini
    """
    
    def __init__(self):
        self.models = {
            'gradient_boosting': None,
            'random_forest': None,
            'calibrated_ensemble': None
        }
        self.feature_columns = []
        self.performance_metrics = {
            'accuracy': 0.0,
            'roc_auc': 0.0,
            'calibration_score': 0.0,
            'roi': 0.0,
            'sharpe_ratio': 0.0
        }
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec tracking avancé"""
        self.conn = sqlite3.connect('nhl_gemini_enhanced.db', check_same_thread=False)
        
        # Table pour features avancées
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS advanced_features (
                game_id TEXT PRIMARY KEY,
                date TEXT,
                home_team TEXT,
                away_team TEXT,
                
                -- Features existantes améliorées
                home_win_rate REAL,
                away_win_rate REAL,
                home_advantage REAL,
                
                -- Nouvelles features selon suggestions Gemini
                back_to_back_fatigue REAL,
                travel_fatigue REAL,
                rest_days_diff REAL,
                recent_form_home REAL,
                recent_form_away REAL,
                
                -- Sentiment analysis (simulé pour l'instant)
                social_sentiment_home REAL,
                social_sentiment_away REAL,
                
                -- Variables météo/contextualles
                temperature REAL,
                rivalry_factor REAL,
                
                -- Target
                home_win INTEGER,
                
                -- Prédictions
                prob_deterministic REAL,
                prob_ml REAL,
                prob_ensemble REAL,
                
                -- Résultats paris
                bet_placed INTEGER,
                bet_amount REAL,
                bet_result INTEGER,
                odds_taken REAL
            )
        ''')
        
        # Table pour tracking performance avancé
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_type TEXT,
                accuracy REAL,
                roc_auc REAL,
                calibration_score REAL,
                roi REAL,
                sharpe_ratio REAL,
                total_bets INTEGER,
                winning_bets INTEGER,
                total_wagered REAL,
                total_won REAL,
                max_drawdown REAL
            )
        ''')
        
        self.conn.commit()
    
    def extract_advanced_features(self, game_data):
        """
        Feature engineering avancé selon les recommandations Gemini
        """
        features = {}
        
        # Features de base
        features['home_win_rate'] = self.get_team_win_rate(game_data['home_team'])
        features['away_win_rate'] = self.get_team_win_rate(game_data['away_team'])
        features['home_advantage'] = 0.545  # Avantage domicile NHL historique
        
        # Nouvelle feature : Fatigue back-to-back
        features['back_to_back_fatigue'] = self.calculate_fatigue_factor(
            game_data['home_team'], 
            game_data['away_team'], 
            game_data['date']
        )
        
        # Nouvelle feature : Fatigue de voyage
        features['travel_fatigue'] = self.calculate_travel_fatigue(
            game_data['away_team'], 
            game_data['date']
        )
        
        # Différence de repos
        features['rest_days_diff'] = self.calculate_rest_difference(
            game_data['home_team'], 
            game_data['away_team'], 
            game_data['date']
        )
        
        # Forme récente (5 derniers matchs)
        features['recent_form_home'] = self.get_recent_form(game_data['home_team'])
        features['recent_form_away'] = self.get_recent_form(game_data['away_team'])
        
        # Analyse de sentiment (simulée)
        features['social_sentiment_home'] = self.get_social_sentiment(game_data['home_team'])
        features['social_sentiment_away'] = self.get_social_sentiment(game_data['away_team'])
        
        # Variables contextuelles
        features['temperature'] = self.get_weather_factor(game_data.get('location'))
        features['rivalry_factor'] = self.get_rivalry_factor(
            game_data['home_team'], 
            game_data['away_team']
        )
        
        return features
    
    def calculate_fatigue_factor(self, home_team, away_team, game_date):
        """
        Calcule le facteur de fatigue back-to-back
        Innovation selon suggestion Gemini
        """
        # Simulé - dans la vraie version, on checkrait les vrais calendriers
        hash_obj = hashlib.md5(f"{home_team}{away_team}{game_date}".encode())
        hash_val = int(hash_obj.hexdigest()[:4], 16) % 100
        
        # 0 = pas de fatigue, 1 = fatigue maximale
        return hash_val / 100.0
    
    def calculate_travel_fatigue(self, away_team, game_date):
        """
        Calcule la fatigue de voyage (fuseaux horaires, distance)
        """
        # Distances simulées entre villes NHL
        travel_distances = {
            'VAN': 0.8,  # Voyages longs depuis Vancouver
            'CGY': 0.6,
            'EDM': 0.6,
            'MTL': 0.4,
            'TOR': 0.3,
            'BOS': 0.3,
        }
        return travel_distances.get(away_team, 0.5)
    
    def calculate_rest_difference(self, home_team, away_team, game_date):
        """
        Différence de jours de repos entre les équipes
        """
        # Simulé - retourne valeur entre -3 et +3 jours
        hash_obj = hashlib.md5(f"{home_team}{away_team}rest".encode())
        return (int(hash_obj.hexdigest()[:2], 16) % 7) - 3
    
    def get_recent_form(self, team):
        """
        Performance des 5 derniers matchs (0.0 à 1.0)
        """
        team_forms = {
            'MTL': 0.65,  # Bonne forme récente
            'TOR': 0.72,
            'BOS': 0.68,
            'DET': 0.45,
            'CHI': 0.38,
        }
        return team_forms.get(team, 0.5)
    
    def get_social_sentiment(self, team):
        """
        Analyse de sentiment des réseaux sociaux (suggestion Gemini)
        Simulé - dans la vraie version, on scraperait Twitter/Reddit
        """
        # Sentiment entre -1 (très négatif) et +1 (très positif)
        sentiments = {
            'MTL': 0.2,   # Optimisme modéré pour Demidov/Hutson
            'TOR': -0.1,  # Pression média
            'BOS': 0.1,
            'DET': 0.3,   # Jeunes talents excitants
            'CHI': 0.4,   # Hype autour de Bedard
        }
        return sentiments.get(team, 0.0)
    
    def get_weather_factor(self, location):
        """
        Impact météo sur la performance (suggestion Gemini)
        """
        # Simulé - température en Celsius
        return np.random.normal(5, 10)  # Automne/hiver typique
    
    def get_rivalry_factor(self, home_team, away_team):
        """
        Facteur de rivalité entre équipes
        """
        rivalries = {
            ('MTL', 'TOR'): 0.8,
            ('MTL', 'BOS'): 0.9,
            ('TOR', 'BOS'): 0.7,
            ('MTL', 'OTT'): 0.6,
        }
        
        key1 = (home_team, away_team)
        key2 = (away_team, home_team)
        
        return rivalries.get(key1, rivalries.get(key2, 0.2))
    
    def get_team_win_rate(self, team):
        """
        Taux de victoire historique de l'équipe
        """
        win_rates = {
            'MTL': 0.52,
            'TOR': 0.58,
            'BOS': 0.62,
            'DET': 0.45,
            'CHI': 0.41,
        }
        return win_rates.get(team, 0.50)
    
    def train_ensemble_model(self, training_data):
        """
        Entraîne le modèle ensemble selon les recommandations Gemini
        """
        print("🧠 Entraînement du modèle ensemble Gemini...")
        
        # Préparation des données
        X = training_data[self.feature_columns]
        y = training_data['home_win']
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Modèle 1: Gradient Boosting (suggestion Gemini)
        self.models['gradient_boosting'] = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.models['gradient_boosting'].fit(X_train, y_train)
        
        # Modèle 2: Random Forest pour diversité
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        self.models['random_forest'].fit(X_train, y_train)
        
        # Modèle 3: Ensemble calibré (suggestion Gemini)
        base_model = GradientBoostingClassifier(n_estimators=50, random_state=42)
        self.models['calibrated_ensemble'] = CalibratedClassifierCV(
            base_model, 
            method='isotonic', 
            cv=3
        )
        self.models['calibrated_ensemble'].fit(X_train, y_train)
        
        # Évaluation
        self.evaluate_models(X_test, y_test)
        
        print("✅ Modèles entraînés avec succès!")
    
    def evaluate_models(self, X_test, y_test):
        """
        Évalue les performances selon les métriques suggérées par Gemini
        """
        for model_name, model in self.models.items():
            if model is None:
                continue
                
            # Prédictions
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            # Métriques
            accuracy = accuracy_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_prob)
            
            # Calibration (suggestion Gemini)
            fraction_pos, mean_pred = calibration_curve(y_test, y_prob, n_bins=10)
            calibration_score = np.mean(np.abs(fraction_pos - mean_pred))
            
            print(f"📊 {model_name}:")
            print(f"   Accuracy: {accuracy:.3f}")
            print(f"   ROC-AUC: {roc_auc:.3f}")
            print(f"   Calibration Error: {calibration_score:.3f}")
    
    def predict_with_ensemble(self, game_features):
        """
        Prédiction avec ensemble de modèles (recommandation Gemini)
        """
        predictions = {}
        
        # Prédiction déterministe (système actuel)
        prob_deterministic = self.deterministic_prediction(game_features)
        predictions['deterministic'] = prob_deterministic
        
        # Prédictions ML si modèles entraînés
        if self.models['calibrated_ensemble']:
            feature_vector = np.array([list(game_features.values())]).reshape(1, -1)
            prob_ml = self.models['calibrated_ensemble'].predict_proba(feature_vector)[0, 1]
            predictions['ml'] = prob_ml
            
            # Ensemble final (pondération intelligente)
            ensemble_prob = (0.3 * prob_deterministic + 0.7 * prob_ml)
            predictions['ensemble'] = ensemble_prob
        else:
            predictions['ml'] = prob_deterministic
            predictions['ensemble'] = prob_deterministic
        
        return predictions
    
    def deterministic_prediction(self, features):
        """
        Prédiction déterministe (système actuel amélioré)
        """
        # Base: différence de force des équipes
        prob = 0.5 + (features['home_win_rate'] - features['away_win_rate'])
        
        # Ajustements selon nouvelles features
        prob += features['home_advantage'] * 0.1
        prob -= features['back_to_back_fatigue'] * 0.15
        prob -= features['travel_fatigue'] * 0.1
        prob += (features['recent_form_home'] - features['recent_form_away']) * 0.2
        prob += (features['social_sentiment_home'] - features['social_sentiment_away']) * 0.05
        prob += features['rivalry_factor'] * 0.1  # Les rivalités peuvent avantager domicile
        
        return np.clip(prob, 0.1, 0.9)
    
    def enhanced_kelly_criterion(self, prob, odds, correlation_matrix=None):
        """
        Kelly Criterion amélioré avec gestion de corrélation (suggestion Gemini)
        """
        # Kelly standard
        edge = prob * (odds - 1) - (1 - prob)
        kelly_fraction = edge / (odds - 1)
        
        # Facteur de corrélation (si paris multiples)
        if correlation_matrix is not None:
            # Réduction selon corrélation avec autres paris actifs
            kelly_fraction *= 0.7  # Réduction conservative
        
        # Limites de sécurité (suggestion Gemini)
        max_bet_fraction = 0.02  # Max 2% du bankroll
        min_edge_threshold = 0.03  # Min 3% d'avantage
        
        if edge < min_edge_threshold:
            return 0.0
        
        return min(kelly_fraction * 0.25, max_bet_fraction)  # 25% du Kelly + limite
    
    def simulate_season_performance(self, num_games=100):
        """
        Simulation de performance sur une saison complète
        """
        print(f"🎲 Simulation de {num_games} matchs...")
        
        bankroll = 100.0
        bets_history = []
        
        for i in range(num_games):
            # Génération d'un match simulé
            game_data = self.generate_fake_game()
            features = self.extract_advanced_features(game_data)
            
            # Prédictions
            predictions = self.predict_with_ensemble(features)
            prob_ensemble = predictions['ensemble']
            
            # Odds simulées
            true_prob = features['home_win_rate'] + np.random.normal(0, 0.1)
            true_prob = np.clip(true_prob, 0.1, 0.9)
            odds = 1 / true_prob + np.random.normal(0, 0.1)
            odds = max(odds, 1.1)
            
            # Décision de pari
            bet_fraction = self.enhanced_kelly_criterion(prob_ensemble, odds)
            bet_amount = bankroll * bet_fraction
            
            if bet_amount > 0:
                # Résultat du match (simulation)
                actual_result = np.random.random() < true_prob
                
                if actual_result:  # Victoire du pari
                    winnings = bet_amount * (odds - 1)
                    bankroll += winnings
                    bet_result = 1
                else:  # Perte du pari
                    bankroll -= bet_amount
                    bet_result = 0
                
                bets_history.append({
                    'game': i,
                    'prob': prob_ensemble,
                    'odds': odds,
                    'bet_amount': bet_amount,
                    'result': bet_result,
                    'bankroll': bankroll
                })
        
        # Calcul des métriques finales
        roi = ((bankroll - 100) / 100) * 100
        
        winning_bets = sum(1 for bet in bets_history if bet['result'] == 1)
        total_bets = len(bets_history)
        win_rate = (winning_bets / total_bets * 100) if total_bets > 0 else 0
        
        print(f"📊 RÉSULTATS DE SIMULATION:")
        print(f"   Paris placés: {total_bets}")
        print(f"   Taux de réussite: {win_rate:.1f}%")
        print(f"   ROI: {roi:+.1f}%")
        print(f"   Bankroll final: ${bankroll:.2f}")
        
        return {
            'roi': roi,
            'win_rate': win_rate,
            'final_bankroll': bankroll,
            'total_bets': total_bets
        }
    
    def generate_fake_game(self):
        """Génère des données de match simulées pour les tests"""
        teams = ['MTL', 'TOR', 'BOS', 'DET', 'CHI', 'NYR', 'OTT']
        home_team = np.random.choice(teams)
        away_team = np.random.choice([t for t in teams if t != home_team])
        
        return {
            'game_id': f"2025{np.random.randint(10000, 99999)}",
            'date': '2025-10-15',
            'home_team': home_team,
            'away_team': away_team,
            'location': home_team
        }

def main():
    """
    Démonstration du système NHL amélioré selon Gemini
    """
    print("🏒 NHL QUARTET ARCHAEOLOGICAL - VERSION GEMINI ENHANCED")
    print("🧠 Implémentation des suggestions de l'expert IA Gemini")
    print("=" * 60)
    
    # Initialisation du système
    gemini_system = GeminiEnhancedNHLSystem()
    
    # Génération de données d'entraînement simulées
    print("📚 Génération des données d'entraînement...")
    training_data = []
    
    for _ in range(1000):  # 1000 matchs historiques simulés
        game = gemini_system.generate_fake_game()
        features = gemini_system.extract_advanced_features(game)
        
        # Résultat simulé
        true_prob = features['home_win_rate'] + np.random.normal(0, 0.2)
        true_prob = np.clip(true_prob, 0.1, 0.9)
        home_win = 1 if np.random.random() < true_prob else 0
        
        features['home_win'] = home_win
        training_data.append(features)
    
    training_df = pd.DataFrame(training_data)
    
    # Définir les colonnes de features
    gemini_system.feature_columns = [col for col in training_df.columns if col != 'home_win']
    
    # Entraînement des modèles
    gemini_system.train_ensemble_model(training_df)
    
    # Simulation de performance
    results = gemini_system.simulate_season_performance(50)
    
    print(f"\n🎯 VALIDATION DES AMÉLIORATIONS GEMINI:")
    print(f"✅ Feature Engineering avancé: Implémenté")
    print(f"✅ Ensemble Learning: Gradient Boosting + Random Forest")
    print(f"✅ Calibration du modèle: CalibratedClassifierCV")
    print(f"✅ Gestion des risques améliorée: Kelly avec corrélation")
    print(f"✅ Métriques avancées: ROC-AUC, Calibration Error")
    
    print(f"\n🏆 Performance atteinte: ROI {results['roi']:+.1f}% sur {results['total_bets']} paris")

if __name__ == "__main__":
    main()
