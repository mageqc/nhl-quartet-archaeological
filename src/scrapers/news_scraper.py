"""
Scraper de nouvelles LNH pour analyser l'impact sur les cotes

Ce module collecte les dernières nouvelles de la LNH depuis plusieurs sources
pour identifier les facteurs qui peuvent affecter les probabilités des paris.
"""

# import requests
# from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os


class NHLNewsScraper:
    """
    Collecteur de nouvelles LNH depuis plusieurs sources fiables
    """
    
    def __init__(self):
        self.sources = {
            'tsn': 'https://www.tsn.ca/nhl',
            'sportsnet': 'https://www.sportsnet.ca/hockey/nhl/',
            'rds': 'https://www.rds.ca/hockey'
        }
        self.keywords_impact = [
            'trade', 'échange', 'blessure', 'injury', 'suspended', 'suspendu',
            'lineup', 'formation', 'starter', 'partant', 'backup', 'auxiliaire',
            'scratched', 'retiré', 'activated', 'activé', 'waived', 'ballotté'
        ]
    
    def scrape_recent_news(self, hours_back=24):
        """
        Collecte les nouvelles des dernières heures
        
        Args:
            hours_back (int): Nombre d'heures à examiner (défaut: 24h)
            
        Returns:
            list: Liste des nouvelles avec impact potentiel
        """
        print(f"🔍 Recherche des nouvelles des {hours_back} dernières heures...")
        
        all_news = []
        
        # Simuler la collecte de nouvelles (en réalité, on scraperait les sites)
        sample_news = [
            {
                'title': 'Connor McDavid questionable pour le match d\'ouverture',
                'source': 'TSN',
                'timestamp': datetime.now() - timedelta(hours=2),
                'impact': 'HIGH',
                'teams_affected': ['EDM'],
                'category': 'injury',
                'summary': 'Blessure mineure au poignet, statut incertain'
            },
            {
                'title': 'Échange majeur: Winnipeg acquiert un défenseur',
                'source': 'Sportsnet',
                'timestamp': datetime.now() - timedelta(hours=6),
                'impact': 'MEDIUM',
                'teams_affected': ['WPG'],
                'category': 'trade',
                'summary': 'Renforcement défensif avant le début de saison'
            },
            {
                'title': 'Carey Price annonce sa retraite officielle',
                'source': 'RDS',
                'timestamp': datetime.now() - timedelta(hours=12),
                'impact': 'LOW',
                'teams_affected': ['MTL'],
                'category': 'retirement',
                'summary': 'Impact déjà reflété dans les cotes'
            }
        ]
        
        # Filtrer par impact et récence
        filtered_news = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for news in sample_news:
            if news['timestamp'] >= cutoff_time and news['impact'] in ['HIGH', 'MEDIUM']:
                filtered_news.append(news)
        
        self._save_news_data(filtered_news)
        
        print(f"✅ {len(filtered_news)} nouvelles importantes collectées")
        return filtered_news
    
    def _save_news_data(self, news_data):
        """
        Sauvegarde les données de nouvelles
        """
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"data/news_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2, default=str)
    
    def get_team_impact_score(self, team_code):
        """
        Calcule un score d'impact basé sur les nouvelles récentes
        
        Args:
            team_code (str): Code de l'équipe (ex: 'MTL', 'TOR')
            
        Returns:
            float: Score d'impact (0.0 = aucun impact, 1.0 = impact majeur)
        """
        # En réalité, on analyserait les nouvelles sauvegardées
        impact_scores = {
            'EDM': 0.8,  # McDavid questionable
            'WPG': 0.4,  # Trade défenseur
            'MTL': 0.1,  # Price retraite (déjà connu)
            'TOR': 0.0,  # Pas de nouvelles
        }
        
        return impact_scores.get(team_code, 0.0)
