#!/usr/bin/env python3
"""
💰 QUICK PROFIT LAUNCHER - Système Profit NHL
Lancement immédiat du système basé sur recommandations IA expertes

Usage: python quick_profit_launcher.py
"""

import subprocess
import sys
import os
from datetime import datetime

def print_banner():
    """Banner profit system"""
    print("\n" + "="*70)
    print("💰 NHL PROFIT SYSTEM - QUICK LAUNCHER")
    print("🤖 Basé sur analyses Gemini & Grok")
    print("🎯 Objectif: Machine à cash IA + value bets")
    print("="*70)

def check_requirements():
    """Vérifie environnement"""
    
    print("🔍 Vérification environnement...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requis")
        return False
    
    print("✅ Python OK")
    
    # Check file existence
    required_files = [
        'nhl_profit_system.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Fichier manquant: {file}")
            return False
    
    print("✅ Fichiers système OK")
    return True

def run_profit_system():
    """Lance système profit"""
    
    print("\n🚀 LANCEMENT SYSTÈME PROFIT...")
    print("-" * 40)
    
    try:
        # Exécuter système profit
        result = subprocess.run([
            sys.executable, 
            'nhl_profit_system.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Système profit exécuté avec succès!")
            
            # Afficher output
            if result.stdout:
                print("\n📋 OUTPUT:")
                print(result.stdout)
            
            return True
        else:
            print("❌ Erreur lors de l'exécution:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - système prend plus de 30s")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def open_dashboard():
    """Ouvre dashboard profit"""
    
    dashboard_file = "nhl_profit_dashboard.html"
    
    if os.path.exists(dashboard_file):
        print(f"\n🌐 Ouverture dashboard: {dashboard_file}")
        
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", dashboard_file])
            elif sys.platform == "win32":  # Windows
                os.startfile(dashboard_file)
            else:  # Linux
                subprocess.run(["xdg-open", dashboard_file])
            
            print("✅ Dashboard ouvert dans navigateur")
            
        except Exception as e:
            print(f"⚠️ Impossible d'ouvrir automatiquement: {str(e)}")
            print(f"💡 Ouvrez manuellement: {os.path.abspath(dashboard_file)}")
    else:
        print("❌ Dashboard non trouvé - vérifier exécution système")

def show_next_steps():
    """Affiche prochaines étapes"""
    
    print("\n" + "="*50)
    print("🎯 PROCHAINES ÉTAPES RECOMMANDÉES")
    print("="*50)
    
    print("\n1. 🔑 INTÉGRATION THE ODDS API:")
    print("   • Créer compte: https://the-odds-api.com/")
    print("   • Free tier: 500 requêtes/mois")
    print("   • Remplacer 'demo_key' dans nhl_profit_system.py")
    
    print("\n2. 🧪 TEST PRÉSAISON MTL:")
    print("   • 22 sept: MTL vs Pittsburgh (premier match)")
    print("   • Calibrer algorithmes sur 6 matchs")
    print("   • Valider précision 65%+ pour ROI durable")
    
    print("\n3. 💰 OPTIMISATIONS CRITIQUES:")
    print("   • Implémenter Sharpe ratio pour risk-adjusted returns")
    print("   • Ajouter ML features spécifiques présaison")
    print("   • Monitoring temps réel bankroll")
    
    print("\n4. 📊 TRACKING PERFORMANCE:")
    print("   • ROI quotidien/hebdomadaire")
    print("   • Win rate par type bet")
    print("   • Max drawdown protection")
    
    print("\n💡 OBJECTIF: 5-10% ROI mensuel via value betting IA")

def main():
    """Main launcher"""
    
    print_banner()
    
    # Check environment
    if not check_requirements():
        print("\n❌ Environnement non compatible")
        return
    
    # Run profit system
    success = run_profit_system()
    
    if success:
        # Open dashboard
        open_dashboard()
        
        # Show next steps
        show_next_steps()
        
        print("\n✅ SYSTÈME PROFIT OPÉRATIONNEL!")
        print(f"⏰ Lancé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    else:
        print("\n❌ Échec lancement système")
        print("💡 Vérifier logs pour diagnostique")

if __name__ == "__main__":
    main()
