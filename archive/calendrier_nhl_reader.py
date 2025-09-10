#!/usr/bin/env python3
"""
📅 EXTRACTEUR CALENDRIER NHL v4.8 OPTIMISÉ
==========================================

Script spécialisé pour lire et afficher le calendrier NHL de façon lisible.
Supporte les formats JSON, CSV et base de données SQLite.

Usage:
    python3 calendrier_nhl_reader.py [fichier]
    
Si aucun fichier spécifié, cherche automatiquement le plus récent.
"""

import sqlite3
import json
import csv
import os
import glob
from datetime import datetime
from typing import Dict, List, Optional

class CalendrierNHLReader:
    """Lecteur optimisé pour calendriers NHL v4.8"""
    
    def __init__(self):
        self.formats_supported = ['.json', '.csv', '.db']
        self.current_dir = os.getcwd()
    
    def find_latest_calendar_file(self) -> Optional[str]:
        """Trouve automatiquement le fichier calendrier le plus récent"""
        patterns = [
            'nhl_calendar_v4.8_simplified_*.json',
            'nhl_calendar_v4.8_complete_*.json',
            'nhl_calendar_v4.8_export_*.csv',
            'nhl_calendar_v4.8_optimized.db'
        ]
        
        latest_file = None
        latest_time = 0
        
        for pattern in patterns:
            files = glob.glob(pattern)
            for file in files:
                file_time = os.path.getmtime(file)
                if file_time > latest_time:
                    latest_time = file_time
                    latest_file = file
        
        return latest_file
    
    def read_json_calendar(self, filename: str) -> Dict:
        """Lit un calendrier JSON (simplifié ou complet)"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Détecter le format (simplifié vs complet)
        if 'nhl_calendar_v48' in data:
            return self.process_simplified_json(data)
        elif 'calendar_summary' in data:
            return self.process_complete_json(data)
        else:
            return {"error": "Format JSON non reconnu"}
    
    def process_simplified_json(self, data: Dict) -> Dict:
        """Traite le JSON simplifié format calendrier"""
        calendar_data = data['nhl_calendar_v48']
        
        result = {
            'format': 'json_simplified',
            'summary': calendar_data['summary'],
            'weeks': []
        }
        
        for week_key, games in calendar_data['weekly_calendar'].items():
            week_num = int(week_key.split('_')[1])
            week_data = {
                'week_number': week_num,
                'games_count': len(games),
                'total_profit': sum(float(g['profit_potential'].replace('$', '')) for g in games),
                'games': games
            }
            result['weeks'].append(week_data)
        
        # Trier par semaine
        result['weeks'].sort(key=lambda x: x['week_number'])
        return result
    
    def process_complete_json(self, data: Dict) -> Dict:
        """Traite le JSON complet avec toutes les données"""
        summary = data['calendar_summary']
        weekly = data.get('weekly_breakdown', {})
        recommendations = data.get('recommendations', [])
        
        result = {
            'format': 'json_complete',
            'summary': {
                'total_games_analyzed': summary['total_games_analyzed'],
                'quality_recommendations': summary['quality_recommendations'],
                'selection_rate': f"{summary['selection_rate']}%",
                'total_potential_profit': f"${summary['total_potential_profit']:.2f}"
            },
            'weeks': []
        }
        
        # Organiser par semaines
        weeks_data = {}
        for rec in recommendations:
            week = rec['week_of_season']
            if week not in weeks_data:
                weeks_data[week] = []
            weeks_data[week].append({
                'date': rec['game_date'],
                'matchup': f"{rec['away_team']} @ {rec['home_team']}",
                'bet': rec['bet_type'],
                'confidence': f"{rec['confidence']:.1%}",
                'expected_value': f"{rec['expected_value']:+.2f}",
                'profit_potential': f"${rec['potential_profit']:.2f}",
                'risk': rec['risk_level'],
                'priority': rec['calendar_priority'],
                'reasoning': rec['reasoning']
            })
        
        for week_num in sorted(weeks_data.keys()):
            games = weeks_data[week_num]
            total_profit = sum(float(g['profit_potential'].replace('$', '')) for g in games)
            
            result['weeks'].append({
                'week_number': week_num,
                'games_count': len(games),
                'total_profit': total_profit,
                'games': games
            })
        
        return result
    
    def read_csv_calendar(self, filename: str) -> Dict:
        """Lit un calendrier CSV"""
        result = {
            'format': 'csv',
            'summary': {'total_recommendations': 0, 'total_potential_profit': 0},
            'weeks': []
        }
        
        weeks_data = {}
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                week = int(row['Semaine'])
                if week not in weeks_data:
                    weeks_data[week] = []
                
                profit = float(row['Profit Potentiel'].replace('$', ''))
                
                weeks_data[week].append({
                    'date': row['Date'],
                    'matchup': f"{row['Équipe Visiteur']} @ {row['Équipe Domicile']}",
                    'bet': row['Type Pari'],
                    'confidence': f"{float(row['Confidence']):.1%}",
                    'expected_value': f"{float(row['Valeur Attendue']):+.2f}",
                    'profit_potential': f"${profit:.2f}",
                    'risk': row['Risque'],
                    'priority': int(row['Priorité']),
                    'reasoning': row['Raisonnement']
                })
                
                result['summary']['total_recommendations'] += 1
                result['summary']['total_potential_profit'] += profit
        
        # Organiser par semaines
        for week_num in sorted(weeks_data.keys()):
            games = weeks_data[week_num]
            total_profit = sum(float(g['profit_potential'].replace('$', '')) for g in games)
            
            result['weeks'].append({
                'week_number': week_num,
                'games_count': len(games),
                'total_profit': total_profit,
                'games': games
            })
        
        return result
    
    def read_db_calendar(self, filename: str) -> Dict:
        """Lit un calendrier depuis la base SQLite"""
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT game_date, week_of_season, home_team, away_team, game_time,
                   bet_type, confidence, expected_value, kelly_fraction,
                   potential_profit, risk_level, reasoning, quality_score,
                   calendar_priority
            FROM nhl_calendar_recommendations
            ORDER BY game_date, quality_score DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {'format': 'db', 'summary': {'total_recommendations': 0}, 'weeks': []}
        
        result = {
            'format': 'database',
            'summary': {'total_recommendations': len(rows), 'total_potential_profit': 0},
            'weeks': []
        }
        
        weeks_data = {}
        
        for row in rows:
            (date, week, home, away, time, bet_type, conf, ev, kelly, 
             profit, risk, reasoning, quality, priority) = row
            
            if week not in weeks_data:
                weeks_data[week] = []
            
            weeks_data[week].append({
                'date': date,
                'matchup': f"{away} @ {home}",
                'bet': bet_type,
                'confidence': f"{conf:.1%}",
                'expected_value': f"{ev:+.2f}",
                'profit_potential': f"${profit:.2f}",
                'risk': risk,
                'priority': priority,
                'reasoning': reasoning,
                'quality_score': quality
            })
            
            result['summary']['total_potential_profit'] += profit
        
        # Organiser par semaines
        for week_num in sorted(weeks_data.keys()):
            games = weeks_data[week_num]
            total_profit = sum(float(g['profit_potential'].replace('$', '')) for g in games)
            
            result['weeks'].append({
                'week_number': week_num,
                'games_count': len(games),
                'total_profit': total_profit,
                'games': games
            })
        
        return result
    
    def display_calendar(self, calendar_data: Dict):
        """Affiche le calendrier de façon lisible"""
        print("🏒" * 80)
        print("📅 CALENDRIER NHL 2025-26 - PARIS RECOMMANDÉS")
        print("🏒" * 80)
        
        if calendar_data.get('error'):
            print(f"❌ ERREUR: {calendar_data['error']}")
            return
        
        # Résumé général
        summary = calendar_data['summary']
        print(f"📊 FORMAT: {calendar_data['format'].upper()}")
        print(f"🎯 TOTAL RECOMMANDATIONS: {summary['total_recommendations']}")
        
        if 'selection_rate' in summary:
            print(f"📈 TAUX SÉLECTION: {summary['selection_rate']}")
        
        total_profit = summary.get('total_potential_profit', 0)
        if isinstance(total_profit, str):
            print(f"💰 PROFIT POTENTIEL TOTAL: {total_profit}")
        else:
            print(f"💰 PROFIT POTENTIEL TOTAL: ${total_profit:.2f}")
        
        print("\\n" + "=" * 80)
        
        # Affichage par semaines
        if not calendar_data['weeks']:
            print("📅 Aucune recommandation trouvée")
            return
        
        for week_data in calendar_data['weeks']:
            week_num = week_data['week_number']
            games_count = week_data['games_count']
            week_profit = week_data['total_profit']
            
            print(f"\\n📅 SEMAINE {week_num}")
            print("─" * 50)
            print(f"🎲 Paris: {games_count} | 💰 Profit potentiel: ${week_profit:.2f}")
            print()
            
            for i, game in enumerate(week_data['games'], 1):
                priority_emoji = ["🔴", "🟡", "🟢"][game['priority'] - 1]
                risk_emoji = {"HIGH": "⚠️", "MEDIUM": "⚡", "LOW": "✅"}[game['risk']]
                
                print(f"   {i}. {priority_emoji} {game['date']} | {game['matchup']}")
                print(f"      🎯 {game['bet']} | Conf: {game['confidence']} | EV: {game['expected_value']}")
                print(f"      💰 {game['profit_potential']} | {risk_emoji} {game['risk']}")
                
                if 'reasoning' in game and game['reasoning']:
                    print(f"      📝 {game['reasoning']}")
                
                print()
        
        print("🏆 FIN DU CALENDRIER")
        print("━" * 80)
        print("📍 LÉGENDE:")
        print("   🟢 Priorité 1 (Haute) | 🟡 Priorité 2 (Moyenne) | 🔴 Priorité 3 (Basse)")
        print("   ✅ Risque Faible | ⚡ Risque Moyen | ⚠️ Risque Élevé")

def main():
    """Fonction principale"""
    import sys
    
    reader = CalendrierNHLReader()
    
    # Déterminer le fichier à lire
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = reader.find_latest_calendar_file()
        if not filename:
            print("❌ Aucun fichier calendrier trouvé")
            print("\\n📁 FICHIERS DISPONIBLES:")
            for f in os.listdir('.'):
                if any(f.endswith(ext) for ext in reader.formats_supported):
                    print(f"   • {f}")
            return
        
        print(f"📄 FICHIER AUTO-DÉTECTÉ: {filename}")
    
    # Vérifier existence
    if not os.path.exists(filename):
        print(f"❌ FICHIER NON TROUVÉ: {filename}")
        return
    
    print(f"📅 LECTURE CALENDRIER NHL: {filename}")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Lire selon l'extension
        if filename.endswith('.json'):
            calendar_data = reader.read_json_calendar(filename)
        elif filename.endswith('.csv'):
            calendar_data = reader.read_csv_calendar(filename)
        elif filename.endswith('.db'):
            calendar_data = reader.read_db_calendar(filename)
        else:
            print(f"❌ FORMAT NON SUPPORTÉ: {filename}")
            return
        
        # Afficher le calendrier
        reader.display_calendar(calendar_data)
        
    except Exception as e:
        print(f"❌ ERREUR LECTURE: {e}")

if __name__ == "__main__":
    main()
