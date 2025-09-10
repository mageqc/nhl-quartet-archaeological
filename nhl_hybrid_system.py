#!/usr/bin/env python3
"""
🏒 NHL CALENDAR HYBRID - API OFFICIELLE + SIMULATION
Système intelligent qui:
- Utilise l'API NHL officielle pendant la saison (Oct-Juin)
- Utilise des matchs simulés hors saison (Juillet-Sept) 
- Détecte automatiquement la période
"""

import sqlite3
from datetime import datetime, timedelta
from nhl_official_api import NHLOfficialAPI
from nhl_calendar_predictor import NHLCalendarPredictor

class NHLHybridSystem:
    """
    🏒 SYSTÈME HYBRIDE NHL
    
    Intelligence:
    - Saison NHL (Oct-Juin) → API Officielle
    - Hors saison (Juillet-Sept) → Simulation réaliste
    - Détection automatique période
    - Transition transparente
    """
    
    def __init__(self):
        print("🏒 NHL HYBRID SYSTEM - CALENDRIER INTELLIGENT")
        print("=" * 60)
        
        self.nhl_api = NHLOfficialAPI()
        self.calendar_predictor = NHLCalendarPredictor()
        
        # Détection période NHL
        self.current_period = self.detect_nhl_period()
        print(f"📅 Période détectée: {self.current_period}")
    
    def detect_nhl_period(self) -> str:
        """Détecte si on est en saison NHL ou hors saison"""
        
        now = datetime.now()
        month = now.month
        
        # Saison NHL: Octobre à Juin
        if month >= 10 or month <= 6:
            return "SAISON_NHL"
        else:
            return "HORS_SAISON"  # Juillet-Septembre
    
    def get_official_games_count(self, days: int = 3) -> int:
        """Teste combien de matchs officiels on peut récupérer"""
        
        print("🔍 Test disponibilité matchs officiels...")
        
        official_count = 0
        today = datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            games = self.nhl_api.get_schedule_for_date(date_str)
            official_count += len(games)
        
        print(f"📊 {official_count} matchs officiels trouvés sur {days} jours")
        return official_count
    
    def generate_hybrid_schedule(self, days: int = 7) -> dict:
        """Génère calendrier hybride intelligent"""
        
        print(f"\n🎯 GÉNÉRATION CALENDRIER HYBRIDE ({days} jours)")
        
        # Tenter API officielle d'abord
        official_games_count = self.get_official_games_count(days=3)
        
        if official_games_count > 0:
            # On a des matchs officiels → Utiliser API
            print("✅ MATCHS OFFICIELS DÉTECTÉS - Mode API NHL")
            return self.use_official_api_schedule(days)
        
        elif self.current_period == "SAISON_NHL":
            # Saison NHL mais pas de matchs → Peut-être pause/break
            print("⚠️  SAISON NHL mais pas de matchs → Pause/All-Star break")
            return self.use_simulation_with_note(days, "Pause NHL - Simulation active")
        
        else:
            # Hors saison → Simulation normale
            print("🎮 HORS SAISON NHL - Mode simulation réaliste")
            return self.use_simulation_with_note(days, "Hors saison - Calendrier simulé")
    
    def use_official_api_schedule(self, days: int) -> dict:
        """Utilise l'API NHL officielle"""
        
        print("🌐 Récupération calendrier officiel NHL...")
        
        official_schedule = self.nhl_api.get_current_schedule(days)
        
        # Sauvegarder en base avec marqueur "officiel"
        conn = sqlite3.connect("nhl_calendar_predictions.db")
        cursor = conn.cursor()
        
        # Nettoyer anciens matchs simulés
        cursor.execute("DELETE FROM nhl_games WHERE official_api != 1 OR official_api IS NULL")
        
        games_added = 0
        
        for date_str, games in official_schedule.items():
            for game in games:
                if not game:
                    continue
                
                cursor.execute('''
                    INSERT OR REPLACE INTO nhl_games 
                    (game_id, game_date, home_team, away_team, start_time, venue,
                     home_score, away_score, game_status, api_game_id, official_api)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    game['game_id'], date_str, game['home_team'], game['away_team'],
                    game['start_time'], game['venue'], game.get('home_score'),
                    game.get('away_score'), game['game_status'], 
                    game['api_game_id'], True
                ))
                
                games_added += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ {games_added} matchs officiels intégrés")
        
        return {
            'source': 'API_OFFICIELLE',
            'games_count': games_added,
            'schedule': official_schedule
        }
    
    def use_simulation_with_note(self, days: int, note: str) -> dict:
        """Utilise simulation avec note explicative"""
        
        print(f"🎮 {note}")
        
        # Générer calendrier simulé réaliste
        start_date = datetime.now()
        simulated_schedule = self.calendar_predictor.simulate_nhl_schedule(start_date, days)
        
        # Sauvegarder avec marqueur simulation
        self.calendar_predictor.save_schedule_to_db(simulated_schedule)
        
        # Ajouter note explicative en base
        conn = sqlite3.connect("nhl_calendar_predictions.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calendar_notes (
                    date TEXT PRIMARY KEY,
                    note TEXT,
                    source_type TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT OR REPLACE INTO calendar_notes (date, note, source_type)
                VALUES (?, ?, ?)
            ''', (today, note, 'SIMULATION'))
            
            conn.commit()
        except Exception as e:
            print(f"⚠️  Note explicative: {e}")
        finally:
            conn.close()
        
        return {
            'source': 'SIMULATION',
            'note': note,
            'games_count': len(simulated_schedule),
            'schedule': simulated_schedule
        }
    
    def get_calendar_status(self) -> dict:
        """Retourne le statut du calendrier"""
        
        conn = sqlite3.connect("nhl_calendar_predictions.db")
        cursor = conn.cursor()
        
        # Ajouter colonne official_api si pas déjà fait
        try:
            cursor.execute('ALTER TABLE nhl_games ADD COLUMN official_api BOOLEAN DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Colonne déjà existante
        
        # Compter matchs officiels vs simulés
        cursor.execute('SELECT COUNT(*) FROM nhl_games WHERE official_api = 1')
        official_count = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM nhl_games WHERE official_api != 1 OR official_api IS NULL')
        simulated_count = cursor.fetchone()[0] or 0
        
        # Récupérer note si existe
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT note, source_type FROM calendar_notes WHERE date = ?', (today,))
        note_result = cursor.fetchone()
        
        conn.close()
        
        return {
            'period': self.current_period,
            'official_games': official_count,
            'simulated_games': simulated_count,
            'note': note_result[0] if note_result else None,
            'source_type': note_result[1] if note_result else None
        }
    
    def run_complete_hybrid_system(self):
        """Lance le système hybride complet"""
        
        print(f"\n🚀 LANCEMENT SYSTÈME HYBRIDE COMPLET")
        
        # 1. Générer calendrier approprié
        schedule_result = self.generate_hybrid_schedule(days=14)
        
        # 2. Lancer prédictions 
        cycle_results = self.calendar_predictor.run_daily_prediction_cycle()
        
        # 3. Générer calendrier HTML avec info source
        calendar_file = self.generate_enhanced_html()
        
        # 4. Statut final
        status = self.get_calendar_status()
        
        print(f"\n🏆 SYSTÈME HYBRIDE OPÉRATIONNEL!")
        print(f"📅 Période: {status['period']}")
        print(f"🏒 Matchs officiels: {status['official_games']}")
        print(f"🎮 Matchs simulés: {status['simulated_games']}")
        if status['note']:
            print(f"💡 Note: {status['note']}")
        print(f"📊 Interface: {calendar_file}")
        
        return calendar_file
    
    def generate_enhanced_html(self) -> str:
        """Génère HTML avec info source des données"""
        
        # Générer calendrier normal
        calendar_file = self.calendar_predictor.generate_calendar_html()
        
        # Ajouter badge source dans l'en-tête
        status = self.get_calendar_status()
        
        source_badge = ""
        if status['official_games'] > 0:
            source_badge = f'''
                <div style="background:#4CAF50;color:white;padding:8px 15px;border-radius:20px;margin:10px 0;display:inline-block;">
                    ✅ API NHL Officielle - {status['official_games']} matchs réels
                </div>
            '''
        else:
            source_badge = f'''
                <div style="background:#ff9800;color:white;padding:8px 15px;border-radius:20px;margin:10px 0;display:inline-block;">
                    🎮 Mode Simulation - {status['simulated_games']} matchs simulés
                </div>
            '''
            if status['note']:
                source_badge += f'''
                    <div style="color:#ffd700;font-style:italic;margin-top:5px;">
                        {status['note']}
                    </div>
                '''
        
        # Lire fichier existant
        with open(calendar_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Injecter badge après l'en-tête
        injection_point = '<p>Matchs quotidiens • Prédictions automatiques • Validation résultats</p>'
        if injection_point in html_content:
            html_content = html_content.replace(
                injection_point,
                injection_point + source_badge
            )
        
        # Sauvegarder version améliorée
        with open(calendar_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Calendrier HTML amélioré généré")
        return calendar_file

def main():
    """Lance le système hybride NHL"""
    
    print("🚀 NHL HYBRID SYSTEM - DÉMARRAGE")
    
    hybrid_system = NHLHybridSystem()
    calendar_file = hybrid_system.run_complete_hybrid_system()
    
    print(f"\n✅ CALENDRIER HYBRIDE PRÊT: {calendar_file}")
    print(f"🏒 Ouvre le fichier pour voir tes matchs (officiels ou simulés)!")

if __name__ == "__main__":
    main()
