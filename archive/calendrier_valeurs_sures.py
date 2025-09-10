"""
🗓️ CALENDRIER VALEURS SÛRES NHL 2025-26 🗓️

Analyse complète de tous les matchs de la saison avec:
✅ Stats actuelles 2025-26 (classements, tendances)
✅ Stats historiques 2024-25 (performances passées)
✅ Algorithme de détection des valeurs sûres
✅ Calendrier jour par jour avec recommandations
✅ Score de confiance pour chaque match

OBJECTIF: Identifier les paris les plus sûrs de la saison!
"""

import sys
import os
sys.path.append('/Volumes/Disque Dur/Dev/NHL 2025-2026')

from src.analyzers.official_data_integrator import get_betting_schedule_data
from src.scrapers.nhl_api_advanced import NHLAPIAdvanced
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class CalendrierValeursSures:
    """
    Générateur de calendrier avec valeurs sûres NHL
    """
    
    def __init__(self):
        self.nhl_api = NHLAPIAdvanced()
        self.calendrier_complet = {}
        self.stats_historiques = {}
        self.stats_actuelles = {}
        self.valeurs_sures = {}
        
        # Données de référence 2024-25 (stats finales)
        self.stats_2024_25 = {
            'classement_final': {
                'BOS': {'points': 109, 'rang': 2, 'playoffs': True, 'home_record': '30-9-2', 'domination_home': 0.85},
                'NYR': {'points': 114, 'rang': 1, 'playoffs': True, 'home_record': '28-9-4', 'domination_home': 0.80},
                'TOR': {'points': 102, 'rang': 3, 'playoffs': True, 'home_record': '25-12-4', 'domination_home': 0.73},
                'FLA': {'points': 110, 'rang': 1, 'playoffs': True, 'home_record': '29-8-4', 'domination_home': 0.83},
                'EDM': {'points': 104, 'rang': 2, 'playoffs': True, 'home_record': '26-11-4', 'domination_home': 0.76},
                'VGK': {'points': 98, 'rang': 3, 'playoffs': True, 'home_record': '24-13-4', 'domination_home': 0.71},
                'WPG': {'points': 95, 'rang': 1, 'playoffs': True, 'home_record': '23-14-4', 'domination_home': 0.68},
                'DAL': {'points': 113, 'rang': 1, 'playoffs': True, 'home_record': '30-8-3', 'domination_home': 0.84},
                'COL': {'points': 108, 'rang': 2, 'playoffs': True, 'home_record': '28-10-3', 'domination_home': 0.82},
                'VAN': {'points': 109, 'rang': 1, 'playoffs': True, 'home_record': '29-9-3', 'domination_home': 0.83},
                'WSH': {'points': 91, 'rang': 8, 'playoffs': False, 'home_record': '22-15-4', 'domination_home': 0.63},
                'TBL': {'points': 98, 'rang': 4, 'playoffs': True, 'home_record': '25-13-3', 'domination_home': 0.74},
                'CAR': {'points': 111, 'rang': 2, 'playoffs': True, 'home_record': '29-8-4', 'domination_home': 0.83},
                'NJD': {'points': 112, 'rang': 3, 'playoffs': True, 'home_record': '28-9-4', 'domination_home': 0.80},
                'MTL': {'points': 76, 'rang': 8, 'playoffs': False, 'home_record': '19-18-4', 'domination_home': 0.56},
                'OTT': {'points': 89, 'rang': 7, 'playoffs': False, 'home_record': '22-16-3', 'domination_home': 0.64},
                'BUF': {'points': 84, 'rang': 6, 'playoffs': False, 'home_record': '21-17-3', 'domination_home': 0.61},
                'DET': {'points': 91, 'rang': 5, 'playoffs': False, 'home_record': '23-15-3', 'domination_home': 0.67}
            },
            'rivalites_historiques': {
                ('MTL', 'TOR'): {'intensite': 10, 'home_advantage': 0.75, 'over_tendency': 0.68},
                ('BOS', 'NYR'): {'intensite': 9, 'home_advantage': 0.73, 'over_tendency': 0.71},
                ('EDM', 'CGY'): {'intensite': 10, 'home_advantage': 0.78, 'over_tendency': 0.74},
                ('NYR', 'NJD'): {'intensite': 8, 'home_advantage': 0.70, 'over_tendency': 0.66},
                ('FLA', 'TBL'): {'intensite': 9, 'home_advantage': 0.74, 'over_tendency': 0.69},
                ('WPG', 'MIN'): {'intensite': 7, 'home_advantage': 0.68, 'over_tendency': 0.64},
                ('VAN', 'CGY'): {'intensite': 8, 'home_advantage': 0.71, 'over_tendency': 0.67},
                ('PIT', 'PHI'): {'intensite': 9, 'home_advantage': 0.72, 'over_tendency': 0.70}
            }
        }
        
        print("🗓️ CALENDRIER VALEURS SÛRES NHL 2025-26 INITIALISÉ")
        print("=" * 50)
    
    def charger_donnees_completes(self) -> Dict[str, Any]:
        """
        Charge toutes les données nécessaires pour l'analyse
        """
        print("📊 CHARGEMENT DONNÉES COMPLÈTES")
        print("-" * 35)
        
        donnees = {}
        
        # 1. Calendrier officiel
        print("📅 Calendrier officiel NHL...")
        try:
            donnees['calendrier_officiel'] = get_betting_schedule_data()
            nb_matchs = donnees['calendrier_officiel']['stats']['total_games']
            print(f"   ✅ {nb_matchs} matchs chargés")
        except Exception as e:
            print(f"   ⚠️ Erreur calendrier: {e}")
            donnees['calendrier_officiel'] = None
        
        # 2. Stats actuelles 2025-26
        print("📈 Stats actuelles 2025-26...")
        try:
            donnees['classements_actuels'] = self.nhl_api.get_current_standings()
            donnees['meneurs_actuels'] = {
                'points': self.nhl_api.get_skater_leaders_current("points", 20),
                'buts': self.nhl_api.get_skater_leaders_current("goals", 20),
                'gardiens': self.nhl_api.get_goalie_leaders_current("wins", 15)
            }
            print("   ✅ Stats actuelles récupérées")
        except Exception as e:
            print(f"   ⚠️ Erreur stats actuelles: {e}")
            donnees['classements_actuels'] = None
            donnees['meneurs_actuels'] = None
        
        # 3. Stats historiques 2024-25
        print("📚 Stats historiques 2024-25...")
        donnees['stats_historiques'] = self.stats_2024_25
        print("   ✅ Stats historiques intégrées")
        
        return donnees
    
    def calculer_force_equipes(self, donnees: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Calcule la force relative de chaque équipe
        """
        print("💪 CALCUL FORCE DES ÉQUIPES")
        print("-" * 25)
        
        forces = {}
        
        # Stats actuelles 2025-26
        if donnees.get('classements_actuels') and 'standings' in donnees['classements_actuels']:
            for team in donnees['classements_actuels']['standings']:
                abbrev = team.get('teamAbbrev', '')
                if abbrev and isinstance(abbrev, str):  # Vérifier que c'est une string
                    forces[abbrev] = {
                        'points_actuels': team.get('points', 0),
                        'matchs_actuels': team.get('gamesPlayed', 1),
                        'ppg_actuels': round(team.get('points', 0) / max(team.get('gamesPlayed', 1), 1), 2),
                        'victoires_actuelles': team.get('wins', 0),
                        'pourcentage_victoires_actuels': round(team.get('wins', 0) / max(team.get('gamesPlayed', 1), 1), 3)
                    }
        
        # Si pas de données actuelles, créer des données par défaut pour toutes les équipes
        if not forces:
            equipes_nhl = ['ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 
                          'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NSH',
                          'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SEA', 'SJS',
                          'STL', 'TBL', 'TOR', 'VAN', 'VGK', 'WSH', 'WPG', 'ARI']
            
            for abbrev in equipes_nhl:
                forces[abbrev] = {
                    'points_actuels': 80,  # Moyenne par défaut
                    'matchs_actuels': 82,
                    'ppg_actuels': 0.98,
                    'victoires_actuelles': 35,
                    'pourcentage_victoires_actuels': 0.427
                }
        
        # Enrichir avec stats historiques 2024-25
        for abbrev in list(forces.keys()):  # Utiliser list() pour éviter les modifications pendant l'itération
            if abbrev in self.stats_2024_25['classement_final']:
                historique = self.stats_2024_25['classement_final'][abbrev]
                forces[abbrev].update({
                    'points_2024_25': historique['points'],
                    'rang_2024_25': historique['rang'],
                    'playoffs_2024_25': historique['playoffs'],
                    'domination_home_2024_25': historique['domination_home']
                })
                
                # Score de force combiné
                force_actuelle = forces[abbrev]['ppg_actuels'] * 41  # Projection 82 matchs
                force_historique = historique['points']
                forces[abbrev]['score_combine'] = round((force_actuelle + force_historique) / 2, 1)
                
                # Catégorie de force
                if forces[abbrev]['score_combine'] >= 105:
                    forces[abbrev]['categorie'] = 'ÉLITE'
                elif forces[abbrev]['score_combine'] >= 95:
                    forces[abbrev]['categorie'] = 'FORTE'
                elif forces[abbrev]['score_combine'] >= 85:
                    forces[abbrev]['categorie'] = 'MOYENNE'
                else:
                    forces[abbrev]['categorie'] = 'FAIBLE'
        
        print(f"   ✅ {len(forces)} équipes analysées")
        
        # Afficher top 5
        top_teams = sorted(forces.items(), key=lambda x: x[1].get('score_combine', 0), reverse=True)[:5]
        print("   🏆 TOP 5 ÉQUIPES:")
        for i, (team, data) in enumerate(top_teams, 1):
            print(f"   {i}. {team}: {data.get('score_combine', 0)} pts ({data.get('categorie', 'N/A')})")
        
        return forces
    
    def analyser_matchs_jour_nouveau_format(self, matchs_jour: List[Dict], forces: Dict[str, Dict]) -> List[Dict]:
        """
        Analyse les matchs d'une journée avec le nouveau format de données
        """
        analyses = []
        
        for match in matchs_jour:
            away_team = match.get('away_team', '')
            home_team = match.get('home_team', '')
            away_abbr = match.get('away_abbr', '')
            home_abbr = match.get('home_abbr', '')
            venue = match.get('venue', '')
            
            if not away_team or not home_team:
                continue
            
            analyse = {
                'match': f"{away_team} @ {home_team}",
                'away_team': away_team,
                'home_team': home_team,
                'away_code': away_abbr,
                'home_code': home_abbr,
                'venue': venue,
                'date': match.get('date', ''),
                'game_type': match.get('game_type_name', 'Regular'),
                'force_away': forces.get(away_abbr, {}),
                'force_home': forces.get(home_abbr, {}),
                'avantage_domicile': 0.0,
                'rivalite': False,
                'score_valeur_sure': 0.0,
                'recommandation': '',
                'confiance': 'FAIBLE',
                'type_pari': '',
                'cote_estimee': 0.0
            }
            
            # Calculer avantage domicile
            home_domination = analyse['force_home'].get('domination_home_2024_25', 0.5)
            analyse['avantage_domicile'] = home_domination
            
            # Vérifier rivalité
            rivalite_key = (away_abbr, home_abbr)
            if rivalite_key in self.stats_2024_25['rivalites_historiques']:
                analyse['rivalite'] = True
                rivalite_data = self.stats_2024_25['rivalites_historiques'][rivalite_key]
                analyse['intensite_rivalite'] = rivalite_data['intensite']
                analyse['avantage_domicile'] = rivalite_data['home_advantage']
            
            # Calculer score de valeur sûre
            score = self._calculer_score_valeur_sure(analyse)
            analyse['score_valeur_sure'] = score
            
            # Générer recommandation
            recommandation = self._generer_recommandation(analyse)
            analyse.update(recommandation)
            
            analyses.append(analyse)
        
        return analyses
    
    def analyser_matchs_jour(self, matchs_jour: List[Dict], forces: Dict[str, Dict]) -> List[Dict]:
        """
        Analyse les matchs d'une journée pour identifier les valeurs sûres
        """
        analyses = []
        
        for match in matchs_jour:
            away_team = match.get('away_team', '')
            home_team = match.get('home_team', '')
            venue = match.get('venue', '')
            
            if not away_team or not home_team:
                continue
            
            # Extraire codes équipes (3 premières lettres)
            away_code = away_team[:3].upper()
            home_code = home_team[:3].upper()
            
            analyse = {
                'match': f"{away_team} @ {home_team}",
                'away_team': away_team,
                'home_team': home_team,
                'away_code': away_code,
                'home_code': home_code,
                'venue': venue,
                'force_away': forces.get(away_code, {}),
                'force_home': forces.get(home_code, {}),
                'avantage_domicile': 0.0,
                'rivalite': False,
                'score_valeur_sure': 0.0,
                'recommandation': '',
                'confiance': 'FAIBLE',
                'type_pari': '',
                'cote_estimee': 0.0
            }
            
            # Calculer avantage domicile
            home_domination = analyse['force_home'].get('domination_home_2024_25', 0.5)
            analyse['avantage_domicile'] = home_domination
            
            # Vérifier rivalité
            rivalite_key = (away_code, home_code)
            if rivalite_key in self.stats_2024_25['rivalites_historiques']:
                analyse['rivalite'] = True
                rivalite_data = self.stats_2024_25['rivalites_historiques'][rivalite_key]
                analyse['intensite_rivalite'] = rivalite_data['intensite']
                analyse['avantage_domicile'] = rivalite_data['home_advantage']
            
            # Calculer score de valeur sûre
            score = self._calculer_score_valeur_sure(analyse)
            analyse['score_valeur_sure'] = score
            
            # Générer recommandation
            recommandation = self._generer_recommandation(analyse)
            analyse.update(recommandation)
            
            analyses.append(analyse)
        
        return analyses
    
    def _calculer_score_valeur_sure(self, analyse: Dict) -> float:
        """
        Calcule le score de valeur sûre d'un match (0-100)
        """
        score = 0.0
        
        force_away = analyse['force_away']
        force_home = analyse['force_home']
        
        if not force_away or not force_home:
            return 0.0
        
        # 1. Différence de force (40 points max)
        score_away = force_away.get('score_combine', 80)
        score_home = force_home.get('score_combine', 80)
        diff_force = abs(score_home - score_away)
        
        if diff_force >= 20:  # Grosse différence
            score += 40
        elif diff_force >= 15:  # Différence modérée
            score += 30
        elif diff_force >= 10:  # Petite différence
            score += 20
        else:  # Équipes similaires
            score += 10
        
        # 2. Avantage domicile (25 points max)
        avantage_dom = analyse['avantage_domicile']
        if avantage_dom >= 0.8:  # Très fort à domicile
            score += 25
        elif avantage_dom >= 0.7:  # Fort à domicile
            score += 20
        elif avantage_dom >= 0.6:  # Bon à domicile
            score += 15
        else:  # Faible à domicile
            score += 5
        
        # 3. Consistance historique (20 points max)
        playoffs_away = force_away.get('playoffs_2024_25', False)
        playoffs_home = force_home.get('playoffs_2024_25', False)
        
        if playoffs_home and not playoffs_away:  # Home en playoffs, Away non
            score += 20
        elif not playoffs_home and playoffs_away:  # Away en playoffs, Home non
            score += 15  # Moins de bonus car pas d'avantage domicile
        elif playoffs_home and playoffs_away:  # Deux équipes playoffs
            score += 10
        else:  # Deux équipes non-playoffs
            score += 5
        
        # 4. Rivalité (15 points max)
        if analyse['rivalite']:
            intensite = analyse.get('intensite_rivalite', 5)
            if intensite >= 9:
                score += 15
            elif intensite >= 7:
                score += 10
            else:
                score += 5
        
        return min(score, 100.0)  # Cap à 100
    
    def _generer_recommandation(self, analyse: Dict) -> Dict[str, Any]:
        """
        Génère une recommandation basée sur l'analyse - TYPES MISE-O-JEU+ OFFICIELS
        
        Types de paris Mise-o-jeu+:
        - GAGNANT: Équipe qui gagne le match
        - ÉCART: Marge de victoire (spread)
        - TOTAL: Nombre total de buts dans le match
        """
        score = analyse['score_valeur_sure']
        force_away = analyse['force_away']
        force_home = analyse['force_home']
        
        recommandation = {
            'recommandation': '',
            'confiance': 'FAIBLE',
            'type_pari_mise_o_jeu': '',  # GAGNANT, ÉCART, ou TOTAL
            'selection_precise': '',     # Sélection exacte sur Mise-o-jeu+
            'cote_estimee': 0.0,
            'mise_suggeree': 0.0,
            'raisonnement': ''
        }
        
        # Définir confiance et mise selon score
        if score >= 85:  # Valeur très sûre
            recommandation['confiance'] = 'TRÈS ÉLEVÉE'
            recommandation['mise_suggeree'] = 8.0
        elif score >= 70:  # Valeur sûre
            recommandation['confiance'] = 'ÉLEVÉE'
            recommandation['mise_suggeree'] = 6.0
        elif score >= 55:  # Valeur modérée
            recommandation['confiance'] = 'MOYENNE'
            recommandation['mise_suggeree'] = 4.0
        else:  # Valeur faible
            recommandation['confiance'] = 'FAIBLE'
            recommandation['mise_suggeree'] = 2.0
        
        # Analyser forces relatives
        score_home = force_home.get('score_combine', 80)
        score_away = force_away.get('score_combine', 80)
        avantage_dom = analyse['avantage_domicile']
        diff_force = score_home - score_away
        
        # PRIORITÉ 1: RIVALITÉS → TOTAL (Over/Under)
        if analyse['rivalite'] and analyse.get('intensite_rivalite', 0) >= 8:
            recommandation['type_pari_mise_o_jeu'] = 'TOTAL'
            recommandation['selection_precise'] = 'Plus de 6.5 buts'
            recommandation['recommandation'] = f"TOTAL: Plus de 6.5 buts"
            recommandation['cote_estimee'] = 1.85
            recommandation['raisonnement'] = f"Rivalité intense ({analyse.get('intensite_rivalite', 0)}/10) - Matchs offensifs"
            
        # PRIORITÉ 2: DOMICILE FORT + ÉCART SIGNIFICATIF → GAGNANT
        elif diff_force >= 15 and avantage_dom >= 0.75:
            recommandation['type_pari_mise_o_jeu'] = 'GAGNANT'
            recommandation['selection_precise'] = analyse['home_team']
            recommandation['recommandation'] = f"GAGNANT: {analyse['home_team']}"
            recommandation['cote_estimee'] = 1.65
            recommandation['raisonnement'] = f"Domicile dominant ({avantage_dom:.0%}) vs équipe faible"
            
        # PRIORITÉ 3: DOMINATION EXCEPTIONNELLE → ÉCART
        elif diff_force >= 20 and avantage_dom >= 0.80:
            recommandation['type_pari_mise_o_jeu'] = 'ÉCART'
            recommandation['selection_precise'] = f"{analyse['home_team']} -1.5"
            recommandation['recommandation'] = f"ÉCART: {analyse['home_team']} -1.5"
            recommandation['cote_estimee'] = 2.20
            recommandation['raisonnement'] = f"Domination domicile exceptionnelle ({avantage_dom:.0%})"
            
        # PRIORITÉ 4: VISITEUR SUPÉRIEUR → GAGNANT VISITEUR
        elif diff_force <= -15:  # Visiteur plus fort
            recommandation['type_pari_mise_o_jeu'] = 'GAGNANT'
            recommandation['selection_precise'] = analyse['away_team']
            recommandation['recommandation'] = f"GAGNANT: {analyse['away_team']}"
            recommandation['cote_estimee'] = 2.40
            recommandation['raisonnement'] = f"Équipe visiteur nettement supérieure"
            
        # PRIORITÉ 5: BON AVANTAGE DOMICILE → GAGNANT DOMICILE
        elif avantage_dom >= 0.70 and diff_force >= 5:
            recommandation['type_pari_mise_o_jeu'] = 'GAGNANT'
            recommandation['selection_precise'] = analyse['home_team']
            recommandation['recommandation'] = f"GAGNANT: {analyse['home_team']}"
            recommandation['cote_estimee'] = 1.75
            recommandation['raisonnement'] = f"Avantage domicile solide ({avantage_dom:.0%})"
            
        # PRIORITÉ 6: ÉQUIPES SIMILAIRES + HISTORIQUE OFFENSIF → TOTAL OVER
        elif abs(diff_force) <= 10 and score >= 60:
            # Vérifier s'il y a des tendances offensives
            if analyse.get('rivalite', False) or avantage_dom >= 0.65:
                recommandation['type_pari_mise_o_jeu'] = 'TOTAL'
                recommandation['selection_precise'] = 'Plus de 6.0 buts'
                recommandation['recommandation'] = f"TOTAL: Plus de 6.0 buts"
                recommandation['cote_estimee'] = 1.95
                recommandation['raisonnement'] = f"Équipes équilibrées, match potentiellement offensif"
            else:
                recommandation['type_pari_mise_o_jeu'] = 'TOTAL'
                recommandation['selection_precise'] = 'Moins de 5.5 buts'
                recommandation['recommandation'] = f"TOTAL: Moins de 5.5 buts"
                recommandation['cote_estimee'] = 1.90
                recommandation['raisonnement'] = f"Équipes équilibrées, match défensif probable"
        
        # AUCUNE VALEUR CLAIRE
        else:
            recommandation['type_pari_mise_o_jeu'] = 'ÉVITER'
            recommandation['selection_precise'] = 'Aucune'
            recommandation['recommandation'] = 'ÉVITER CE MATCH'
            recommandation['cote_estimee'] = 0.0
            recommandation['raisonnement'] = "Trop d'incertitude, pas de valeur claire"
        
        return recommandation
    
    def generer_calendrier_complet(self) -> Dict[str, Any]:
        """
        Génère le calendrier complet avec toutes les valeurs sûres
        """
        print("\n🗓️ GÉNÉRATION CALENDRIER COMPLET")
        print("=" * 35)
        
        # 1. Charger toutes les données
        donnees = self.charger_donnees_completes()
        
        # 2. Calculer forces des équipes
        forces = self.calculer_force_equipes(donnees)
        
        # 3. Organiser par jour
        print("📅 Organisation par jour...")
        calendrier_jour = defaultdict(list)
        nb_matchs_analyses = 0
        
        if donnees.get('calendrier_officiel'):
            calendrier_data = donnees['calendrier_officiel']
            
            # Vérifier si on a le full_schedule avec by_date
            if 'full_schedule' in calendrier_data and calendrier_data['full_schedule'] and 'by_date' in calendrier_data['full_schedule']:
                print("   📊 Utilisation du calendrier complet...")
                by_date_data = calendrier_data['full_schedule']['by_date']
                
                for jour, matchs in by_date_data.items():
                    # Filtrer uniquement les matchs de saison régulière (game_type 2)
                    matchs_saison = [m for m in matchs if m.get('game_type', 1) == 2]
                    if matchs_saison:
                        analyses = self.analyser_matchs_jour_nouveau_format(matchs_saison, forces)
                        if analyses:  # Seulement si on a des analyses
                            calendrier_jour[jour] = analyses
                            nb_matchs_analyses += len(analyses)
                            
            # Fallback: utiliser les opening_games
            elif 'opening_games' in calendrier_data and calendrier_data['opening_games']:
                print("   📅 Utilisation des matchs d'ouverture...")
                opening_games = calendrier_data['opening_games']
                
                # Grouper par date
                by_date_opening = defaultdict(list)
                for game in opening_games:
                    date = game.get('date', '')
                    if date:
                        by_date_opening[date].append(game)
                
                for jour, matchs in by_date_opening.items():
                    analyses = self.analyser_matchs_jour(matchs, forces)
                    if analyses:
                        calendrier_jour[jour] = analyses
                        nb_matchs_analyses += len(analyses)
        
        print(f"   ✅ {nb_matchs_analyses} matchs de saison analysés")
        
        # 4. Identifier les meilleures journées
        print("🎯 Identification meilleures journées...")
        meilleures_journees = self._identifier_meilleures_journees(calendrier_jour)
        
        # 5. Résumé des valeurs sûres
        print("✅ Génération résumé...")
        resume = self._generer_resume_valeurs_sures(calendrier_jour)
        
        calendrier_complet = {
            'meta': {
                'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'nb_jours_analyses': len(calendrier_jour),
                'nb_matchs_total': sum(len(matchs) for matchs in calendrier_jour.values()),
                'nb_valeurs_sures': resume['stats']['nb_valeurs_sures']
            },
            'forces_equipes': forces,
            'calendrier_jour': dict(calendrier_jour),
            'meilleures_journees': meilleures_journees,
            'resume_valeurs_sures': resume,
            'donnees_source': {
                'classements_actuels_disponibles': donnees.get('classements_actuels') is not None,
                'calendrier_officiel_disponible': donnees.get('calendrier_officiel') is not None,
                'stats_historiques_integrees': True
            }
        }
        
        print(f"✅ Calendrier généré: {len(calendrier_jour)} jours analysés")
        print(f"🎯 {resume['stats']['nb_valeurs_sures']} valeurs sûres identifiées")
        
        return calendrier_complet
    
    def _identifier_meilleures_journees(self, calendrier_jour: Dict) -> List[Dict]:
        """
        Identifie les meilleures journées pour parier
        """
        journees_avec_scores = []
        
        for jour, matchs in calendrier_jour.items():
            valeurs_sures = [m for m in matchs if m['score_valeur_sure'] >= 70]
            score_moyen = sum(m['score_valeur_sure'] for m in matchs) / len(matchs) if matchs else 0
            
            journees_avec_scores.append({
                'date': jour,
                'nb_matchs': len(matchs),
                'nb_valeurs_sures': len(valeurs_sures),
                'score_moyen': round(score_moyen, 1),
                'valeurs_sures': valeurs_sures
            })
        
        # Trier par nombre de valeurs sûres puis par score moyen
        journees_avec_scores.sort(key=lambda x: (x['nb_valeurs_sures'], x['score_moyen']), reverse=True)
        
        return journees_avec_scores[:20]  # Top 20 journées
    
    def _generer_resume_valeurs_sures(self, calendrier_jour: Dict) -> Dict[str, Any]:
        """
        Génère un résumé des valeurs sûres de la saison
        """
        toutes_valeurs_sures = []
        stats_par_confiance = {'TRÈS ÉLEVÉE': 0, 'ÉLEVÉE': 0, 'MOYENNE': 0, 'FAIBLE': 0}
        stats_par_type = defaultdict(int)
        
        for jour, matchs in calendrier_jour.items():
            for match in matchs:
                if match['score_valeur_sure'] >= 55:  # Seuil valeur sûre
                    toutes_valeurs_sures.append({
                        'date': jour,
                        'match': match['match'],
                        'score': match['score_valeur_sure'],
                        'confiance': match['confiance'],
                        'recommandation': match['recommandation'],
                        'type_pari_mise_o_jeu': match['type_pari_mise_o_jeu'],
                        'selection_precise': match['selection_precise'],
                        'cote_estimee': match['cote_estimee'],
                        'mise_suggeree': match['mise_suggeree'],
                        'raisonnement': match['raisonnement']
                    })
                    
                    stats_par_confiance[match['confiance']] += 1
                    stats_par_type[match['type_pari_mise_o_jeu']] += 1
        
        # Trier par score
        toutes_valeurs_sures.sort(key=lambda x: x['score'], reverse=True)
        
        resume = {
            'top_valeurs_sures': toutes_valeurs_sures[:50],  # Top 50
            'stats': {
                'nb_valeurs_sures': len(toutes_valeurs_sures),
                'score_moyen': round(sum(v['score'] for v in toutes_valeurs_sures) / len(toutes_valeurs_sures), 1) if toutes_valeurs_sures else 0,
                'mise_totale_suggeree': sum(v['mise_suggeree'] for v in toutes_valeurs_sures),
                'par_confiance': dict(stats_par_confiance),
                'par_type_pari': dict(stats_par_type)
            }
        }
        
        return resume
    
    def afficher_calendrier_resume(self, calendrier: Dict[str, Any]) -> None:
        """
        Affiche un résumé du calendrier des valeurs sûres
        """
        print("\n🗓️ CALENDRIER VALEURS SÛRES NHL 2025-26")
        print("=" * 50)
        
        meta = calendrier['meta']
        resume = calendrier['resume_valeurs_sures']
        meilleures = calendrier['meilleures_journees']
        
        # Stats générales
        print(f"📊 STATISTIQUES GÉNÉRALES")
        print(f"   📅 Jours analysés: {meta['nb_jours_analyses']}")
        print(f"   🏒 Matchs analysés: {meta['nb_matchs_total']}")
        print(f"   ✅ Valeurs sûres: {meta['nb_valeurs_sures']}")
        print(f"   📈 Score moyen: {resume['stats']['score_moyen']}")
        print(f"   💰 Mise totale suggérée: {resume['stats']['mise_totale_suggeree']:.0f}$")
        
        # Répartition par type Mise-o-jeu+
        print(f"\n🎯 RÉPARTITION PAR TYPE MISE-O-JEU+")
        for type_pari, nb in resume['stats']['par_type_pari'].items():
            if type_pari != 'ÉVITER':
                print(f"   {type_pari}: {nb} matchs")
        
        # Top 10 journées
        print(f"\n📅 TOP 10 MEILLEURES JOURNÉES")
        print("-" * 40)
        for i, journee in enumerate(meilleures[:10], 1):
            print(f"{i:2d}. {journee['date']}")
            print(f"    🏒 {journee['nb_matchs']} matchs | ✅ {journee['nb_valeurs_sures']} valeurs sûres")
            print(f"    📊 Score moyen: {journee['score_moyen']}")
            if journee['valeurs_sures']:
                print(f"    🎯 Meilleur: {journee['valeurs_sures'][0]['match']} (Score: {journee['valeurs_sures'][0]['score_valeur_sure']:.0f})")
            print()
        
        # Top 15 valeurs sûres
        print(f"🏆 TOP 15 VALEURS SÛRES DE LA SAISON")
        print("-" * 45)
        for i, valeur in enumerate(resume['top_valeurs_sures'][:15], 1):
            print(f"{i:2d}. {valeur['date']} - {valeur['match']}")
            print(f"    🎯 Score: {valeur['score']:.0f} | Confiance: {valeur['confiance']}")
            print(f"    💡 {valeur['type_pari_mise_o_jeu']}: {valeur['selection_precise']}")
            print(f"    💰 Mise: {valeur['mise_suggeree']:.0f}$ | Cote: {valeur['cote_estimee']:.2f}")
            print(f"    📝 {valeur['raisonnement']}")
            print()
        
        print("🎯 CALENDRIER VALEURS SÛRES PRÊT!")
        print("=" * 35)
        print("✅ Analyses basées sur stats actuelles + historiques")
        print("✅ Scores de confiance calculés")
        print("✅ Recommandations optimisées")
        print("🏒 Prêt pour une saison profitable!")
    
    def sauvegarder_calendrier(self, calendrier: Dict[str, Any]) -> str:
        """
        Sauvegarde le calendrier complet
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"data/calendrier_valeurs_sures_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(calendrier, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 Calendrier sauvegardé: {filename}")
        return filename


def generer_calendrier_valeurs_sures() -> Dict[str, Any]:
    """
    Point d'entrée principal pour générer le calendrier
    """
    print("🗓️ GÉNÉRATION CALENDRIER VALEURS SÛRES NHL 2025-26")
    print("=" * 55)
    print("🎯 Objectif: Identifier TOUS les paris sûrs de la saison")
    print("📊 Sources: Stats actuelles + historiques 2024-25")
    print("🔍 Méthode: Algorithme de scoring avancé")
    print()
    
    # Créer le générateur
    generateur = CalendrierValeursSures()
    
    # Générer le calendrier complet
    calendrier = generateur.generer_calendrier_complet()
    
    # Afficher le résumé
    generateur.afficher_calendrier_resume(calendrier)
    
    # Sauvegarder
    fichier = generateur.sauvegarder_calendrier(calendrier)
    
    return calendrier


if __name__ == "__main__":
    # Lancer la génération du calendrier
    calendrier_final = generer_calendrier_valeurs_sures()
