#!/usr/bin/env python3
"""
🚀 DÉMARRAGE RAPIDE NHL - LANCEUR UNIVERSEL
Script unique pour lancer tous les outils NHL développés

Outils disponibles:
1. 📊 Dashboard Unifié (API + Logos)
2. 📅 Calendrier avec Logos
3. 🎨 Système Logos NHL seul
4. 🔮 Prédicteur Calendrier Avancé
5. 📡 API NHL Officielle
6. 🎮 Mode Simulation/Hybride
"""

import os
import sys
import subprocess
from datetime import datetime

class NHLQuickLauncher:
    """
    🚀 LANCEUR RAPIDE NHL
    
    Interface unifiée pour tous les outils NHL:
    - Menu interactif
    - Lancement automatique
    - Ouverture navigateur
    - Logs temps réel
    """
    
    def __init__(self):
        print("🚀 NHL DÉMARRAGE RAPIDE - LANCEUR UNIVERSEL")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.tools = {
            '1': {
                'name': '📊 Dashboard NHL Unifié',
                'description': 'Interface complète - API officielle + Logos + Stats temps réel',
                'script': 'nhl_unified_dashboard.py',
                'html_output': 'nhl_unified_dashboard.html',
                'icon': '🚀'
            },
            '2': {
                'name': '📅 Calendrier avec Logos NHL', 
                'description': 'Calendrier visuel - Matchs + Prédictions + Logos officiels',
                'script': 'nhl_calendar_with_logos.py',
                'html_output': 'nhl_calendar_enhanced_logos.html',
                'icon': '📅'
            },
            '3': {
                'name': '🎨 Système Logos NHL',
                'description': 'Générateur logos - 32 équipes + CSS + HTML exports',
                'script': 'nhl_logos_system.py',
                'html_output': 'nhl_logos_showcase.html',
                'icon': '🎨'
            },
            '4': {
                'name': '🔮 Prédicteur NHL Avancé',
                'description': 'IA Prédictions - Algorithmes + Validation + Performance',
                'script': 'nhl_calendar_predictor.py', 
                'html_output': 'nhl_calendar_interactive.html',
                'icon': '🔮'
            },
            '5': {
                'name': '📡 Test API NHL Officielle',
                'description': 'Connexion API - Test endpoints + Données temps réel',
                'script': 'nhl_official_api.py',
                'html_output': None,  # Pas d'output HTML
                'icon': '📡'
            },
            '6': {
                'name': '🎮 Système Hybride',
                'description': 'Mode intelligent - API/Simulation selon disponibilité',
                'script': 'nhl_hybrid_system.py',
                'html_output': 'nhl_hybrid_dashboard.html',
                'icon': '🎮'
            }
        }
        
    def show_menu(self):
        """Affiche menu principal"""
        
        print("\n🏒 OUTILS NHL DISPONIBLES:")
        print("-" * 60)
        
        for key, tool in self.tools.items():
            icon = tool['icon']
            name = tool['name']
            desc = tool['description']
            
            # Vérifier si le script existe
            script_exists = os.path.exists(tool['script'])
            status = "✅" if script_exists else "❌"
            
            print(f"{key}. {status} {icon} {name}")
            print(f"   └─ {desc}")
            
            if not script_exists:
                print(f"   └─ ⚠️  Script manquant: {tool['script']}")
            print()
        
        print("🔧 OPTIONS SPÉCIALES:")
        print("a. 🚀 Lancer TOUT (Dashboard + Calendrier + Logos)")
        print("b. 🌐 Ouvrir tous les HTML dans le navigateur")
        print("c. 🧹 Nettoyer fichiers temporaires")
        print("q. 🚪 Quitter")
        print("-" * 60)
        
    def get_user_choice(self) -> str:
        """Demande choix utilisateur"""
        
        while True:
            choice = input("\n👉 Votre choix (1-6, a, b, c, q): ").strip().lower()
            
            valid_choices = list(self.tools.keys()) + ['a', 'b', 'c', 'q']
            
            if choice in valid_choices:
                return choice
            else:
                print(f"❌ Choix invalide. Utilisez: {', '.join(valid_choices)}")
    
    def run_script(self, script_name: str, tool_name: str) -> bool:
        """Execute un script Python"""
        
        if not os.path.exists(script_name):
            print(f"❌ Script introuvable: {script_name}")
            return False
        
        print(f"\n🚀 Lancement: {tool_name}")
        print(f"📄 Script: {script_name}")
        print("-" * 40)
        
        try:
            # Lancer script avec python3
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=False,  # Afficher output en temps réel
                text=True
            )
            
            if result.returncode == 0:
                print(f"\n✅ {tool_name} - Terminé avec succès!")
                return True
            else:
                print(f"\n❌ {tool_name} - Erreur (code {result.returncode})")
                return False
                
        except Exception as e:
            print(f"\n💥 Erreur exécution {tool_name}: {str(e)}")
            return False
    
    def open_html_files(self):
        """Ouvre tous les fichiers HTML générés"""
        
        print("\n🌐 OUVERTURE FICHIERS HTML")
        print("-" * 40)
        
        html_files = []
        
        # Collecter fichiers HTML existants
        for tool in self.tools.values():
            if tool['html_output'] and os.path.exists(tool['html_output']):
                html_files.append(tool['html_output'])
        
        if not html_files:
            print("❌ Aucun fichier HTML trouvé")
            print("💡 Lancez d'abord un outil pour générer des interfaces")
            return
        
        # Ouvrir chaque fichier
        for html_file in html_files:
            try:
                print(f"🌐 Ouverture: {html_file}")
                
                if sys.platform.startswith('darwin'):  # macOS
                    subprocess.run(['open', html_file])
                elif sys.platform.startswith('win'):   # Windows
                    os.startfile(html_file)
                else:  # Linux
                    subprocess.run(['xdg-open', html_file])
                    
            except Exception as e:
                print(f"❌ Erreur ouverture {html_file}: {str(e)}")
        
        print(f"\n✅ {len(html_files)} fichiers ouverts dans le navigateur!")
    
    def clean_temp_files(self):
        """Nettoie fichiers temporaires"""
        
        print("\n🧹 NETTOYAGE FICHIERS TEMPORAIRES")
        print("-" * 40)
        
        temp_patterns = [
            '*.pyc',
            '__pycache__',
            '*.log',
            '*.tmp',
            '.DS_Store'
        ]
        
        cleaned = 0
        
        try:
            import glob
            
            for pattern in temp_patterns:
                files = glob.glob(pattern, recursive=True)
                for file in files:
                    try:
                        if os.path.isfile(file):
                            os.remove(file)
                            print(f"🗑️  Supprimé: {file}")
                            cleaned += 1
                        elif os.path.isdir(file):
                            import shutil
                            shutil.rmtree(file)
                            print(f"📁 Dossier supprimé: {file}")
                            cleaned += 1
                    except Exception as e:
                        print(f"⚠️  Impossible de supprimer {file}: {str(e)}")
        
        except Exception as e:
            print(f"❌ Erreur nettoyage: {str(e)}")
        
        print(f"\n✅ Nettoyage terminé - {cleaned} éléments supprimés")
    
    def launch_all_main_tools(self):
        """Lance les 3 outils principaux"""
        
        print("\n🚀 LANCEMENT COMPLET NHL")
        print("=" * 40)
        
        main_tools = ['1', '2', '3']  # Dashboard, Calendrier, Logos
        results = []
        
        for tool_key in main_tools:
            tool = self.tools[tool_key]
            
            print(f"\n{tool['icon']} {tool['name']}")
            print("=" * 30)
            
            success = self.run_script(tool['script'], tool['name'])
            results.append((tool['name'], success))
        
        # Résumé final
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ LANCEMENT COMPLET")
        print("=" * 50)
        
        for name, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {name}")
        
        successful = sum(1 for _, success in results if success)
        print(f"\n🎯 Succès: {successful}/{len(results)} outils")
        
        if successful > 0:
            print("\n🌐 Ouverture automatique des interfaces...")
            self.open_html_files()
    
    def run(self):
        """Boucle principale du lanceur"""
        
        try:
            while True:
                self.show_menu()
                choice = self.get_user_choice()
                
                if choice == 'q':
                    print("\n👋 Au revoir! Bonne analyse NHL!")
                    break
                
                elif choice == 'a':
                    self.launch_all_main_tools()
                
                elif choice == 'b':
                    self.open_html_files()
                
                elif choice == 'c':
                    self.clean_temp_files()
                
                elif choice in self.tools:
                    tool = self.tools[choice]
                    success = self.run_script(tool['script'], tool['name'])
                    
                    # Si succès et fichier HTML existe, proposer ouverture
                    if success and tool['html_output'] and os.path.exists(tool['html_output']):
                        open_choice = input(f"\n🌐 Ouvrir {tool['html_output']} ? (y/n): ").strip().lower()
                        if open_choice == 'y':
                            try:
                                if sys.platform.startswith('darwin'):
                                    subprocess.run(['open', tool['html_output']])
                                elif sys.platform.startswith('win'):
                                    os.startfile(tool['html_output'])
                                else:
                                    subprocess.run(['xdg-open', tool['html_output']])
                                print("✅ Interface ouverte!")
                            except Exception as e:
                                print(f"❌ Erreur ouverture: {str(e)}")
                
                # Pause avant retour menu
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
                print("\n" * 2)  # Espace visuel
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption utilisateur")
            print("👋 Au revoir!")
        except Exception as e:
            print(f"\n💥 Erreur inattendue: {str(e)}")
        finally:
            print(f"\n🏁 Session terminée - {datetime.now().strftime('%H:%M:%S')}")

def main():
    """Point d'entrée principal"""
    
    # Changer vers répertoire script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Lancer interface
    launcher = NHLQuickLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
