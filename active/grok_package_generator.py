#!/usr/bin/env python3
"""
📤 EXTRACTEUR FICHIERS POUR GROK ANALYSE
Script automatique pour préparer package d'analyse système NHL

Génère packages optimisés pour analyse Grok:
- Package minimal (3 fichiers essentiels)  
- Package complet (6 fichiers techniques)
- Brief contextuel avec calendrier présaison CH
"""

import os
import shutil
from datetime import datetime

class GrokAnalysisPackager:
    """
    📤 PRÉPARATEUR PACKAGE GROK
    
    Crée packages optimisés pour analyse:
    - Sélection fichiers stratégiques
    - Brief contextuel intégré  
    - Calendrier présaison CH inclus
    - Formats multiples (ZIP, dossiers)
    """
    
    def __init__(self):
        print("📤 EXTRACTEUR FICHIERS GROK - NHL 2025-2026")
        print("=" * 50)
        
        self.base_dir = os.getcwd()
        self.output_dir = "grok_analysis_package"
        
        # Fichiers prioritaires pour Grok
        self.essential_files = [
            "MISSION_FINALE_ACCOMPLIE.md",
            "nhl_unified_dashboard.py", 
            "README.md"
        ]
        
        self.complete_files = [
            "MISSION_FINALE_ACCOMPLIE.md",
            "README.md",
            "nhl_unified_dashboard.py", 
            "nhl_logos_system.py",
            "nhl_calendar_with_logos.py",
            "PLAN_DEVELOPPEMENT_PRE_SAISON.md"
        ]
        
        # Contexte présaison Canadiens
        self.preseason_schedule = """
PRÉSAISON CANADIENS DE MONTRÉAL 2025-2026:

📅 Lundi 22 sept 2025    vs PIT    19:00
📅 Mardi 23 sept 2025    vs PHI    19:00  
📅 Jeudi 25 sept 2025    vs TOR    19:00
📅 Samedi 27 sept 2025   @ TOR     19:00
📅 Mardi 30 sept 2025    @ OTT (Québec) 19:00
📅 Samedi 04 oct 2025    vs OTT    19:00

🎯 6 matchs présaison - Opportunité test système
🤖 Focus: Optimisation prédictions matchs exhibition
📊 Défi: Performance algorithmes sur données limitées
        """
    
    def create_output_directory(self):
        """Crée répertoire de sortie"""
        
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        
        os.makedirs(self.output_dir)
        os.makedirs(f"{self.output_dir}/minimal_package")
        os.makedirs(f"{self.output_dir}/complete_package")
        
        print(f"📁 Répertoire créé: {self.output_dir}")
    
    def copy_files(self, file_list: list, target_dir: str) -> tuple:
        """Copie fichiers sélectionnés vers répertoire cible"""
        
        copied = []
        missing = []
        
        for filename in file_list:
            if os.path.exists(filename):
                shutil.copy2(filename, target_dir)
                file_size = os.path.getsize(filename)
                copied.append((filename, file_size))
                print(f"✅ {filename} → {target_dir} ({file_size:,} bytes)")
            else:
                missing.append(filename)
                print(f"❌ Fichier manquant: {filename}")
        
        return copied, missing
    
    def create_grok_brief(self, package_type: str) -> str:
        """Génère brief contextualisé pour Grok"""
        
        brief_content = f"""# 🤖 BRIEF ANALYSE GROK - SYSTÈME NHL 2025-2026

## 📋 PACKAGE {package_type.upper()}
Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 MISSION D'ANALYSE

### Système Développé
Écosystème complet NHL pour Loto-Québec Mise-o-jeu+ avec:
- ✅ API NHL officielle temps réel
- ✅ 32 logos authentiques intégrés  
- ✅ Dashboard moderne responsive
- ✅ Prédictions IA avec validation
- ✅ Mode hybride API/simulation
- ✅ Architecture prête production

### Contexte Présaison Immédiate
{self.preseason_schedule}

## 🔍 DOMAINES D'ANALYSE PRIORITAIRES

### 1. 🏒 Optimisations Présaison
- Comment adapter algorithmes pour matchs exhibition ?
- Quelles métriques spécifiques présaison implémenter ?
- Comment tracker performance rookie vs vétérans ?

### 2. 🤖 Améliorations Machine Learning  
- Algorithmes prédiction plus sophistiqués ?
- Intégration données historiques multi-saisons ?
- Auto-apprentissage basé résultats temps réel ?

### 3. 📊 Interface Utilisateur Avancée
- Dashboard spécialisé présaison vs saison ?
- Visualisations données joueurs prospects ?
- UX optimisée paris Loto-Québec ?

### 4. ⚡ Performance & Scalabilité
- Optimisations base données pour 82+ matchs ?
- Cache intelligent et parallélisation ?
- Gestion charge utilisateurs simultanés ?

### 5. 🔮 Vision Stratégique Saison
- Fonctionnalités manquantes critiques ?
- Intégrations APIs externes recommandées ?
- Roadmap développement optimal ?

## 📤 LIVRABLES ATTENDUS

1. **🎯 Analyse critique** forces/faiblesses système actuel
2. **💡 Recommandations concrètes** avec priorités  
3. **⚙️ Exemples code** pour améliorations clés
4. **📋 Roadmap** développement présaison (2 semaines)
5. **🚀 Vision long terme** saison complète

## 🎪 CONTRAINTES TECHNIQUES
- Python 3.8+ (modules standard privilégiés)
- SQLite base données (performance critique)
- Interface web moderne (HTML/CSS/JS)
- Compatibilité mobile/desktop
- Déploiement production Loto-Québec

---
💡 **Focus spécial: Comment optimiser ce système pour réussir la présaison Canadiens et être prêt pour la saison complète ?**
"""
        
        return brief_content
    
    def create_file_summary(self, copied_files: list, package_type: str) -> str:
        """Génère résumé fichiers inclus"""
        
        summary = f"""# 📋 CONTENU PACKAGE {package_type.upper()}

## 📄 Fichiers Inclus ({len(copied_files)})

"""
        
        total_size = 0
        
        for filename, file_size in copied_files:
            total_size += file_size
            
            # Description contextuelle
            descriptions = {
                "MISSION_FINALE_ACCOMPLIE.md": "📊 Récapitulatif complet - Objectifs atteints et architecture",
                "README.md": "📖 Documentation utilisateur - Installation et utilisation", 
                "nhl_unified_dashboard.py": "🚀 Code principal - Dashboard avec API + logos",
                "nhl_logos_system.py": "🎨 Système logos - 32 équipes NHL authentiques",
                "nhl_calendar_with_logos.py": "📅 Calendrier enhanced - Prédictions + interface",
                "PLAN_DEVELOPPEMENT_PRE_SAISON.md": "🗺️ Roadmap - Plan développement structuré"
            }
            
            desc = descriptions.get(filename, "📄 Fichier système")
            summary += f"### {filename}\n- {desc}\n- Taille: {file_size:,} bytes\n\n"
        
        summary += f"""## 📈 Statistiques Package
- **Fichiers total:** {len(copied_files)}
- **Taille totale:** {total_size:,} bytes  
- **Type:** {package_type}
- **Généré:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 Utilisation Recommandée
1. Lire MISSION_FINALE_ACCOMPLIE.md pour vue d'ensemble
2. Consulter README.md pour spécifications techniques  
3. Analyser code principal (nhl_unified_dashboard.py)
4. Examiner innovations (logos, calendrier) si package complet
5. Formuler recommandations selon brief inclus
"""
        
        return summary
    
    def generate_packages(self):
        """Génère les packages complets pour Grok"""
        
        print("\n🎁 GÉNÉRATION PACKAGES GROK")
        print("-" * 40)
        
        # Package minimal
        print("\n📦 PACKAGE MINIMAL (3 fichiers essentiels)")
        minimal_dir = f"{self.output_dir}/minimal_package"
        copied_min, missing_min = self.copy_files(self.essential_files, minimal_dir)
        
        # Brief minimal
        brief_minimal = self.create_grok_brief("minimal")
        with open(f"{minimal_dir}/GROK_BRIEF_ANALYSE.md", 'w', encoding='utf-8') as f:
            f.write(brief_minimal)
        
        # Résumé minimal  
        summary_minimal = self.create_file_summary(copied_min, "minimal")
        with open(f"{minimal_dir}/CONTENU_PACKAGE.md", 'w', encoding='utf-8') as f:
            f.write(summary_minimal)
        
        # Package complet
        print(f"\n📦 PACKAGE COMPLET ({len(self.complete_files)} fichiers)")
        complete_dir = f"{self.output_dir}/complete_package"
        copied_comp, missing_comp = self.copy_files(self.complete_files, complete_dir)
        
        # Brief complet
        brief_complete = self.create_grok_brief("complet")
        with open(f"{complete_dir}/GROK_BRIEF_ANALYSE.md", 'w', encoding='utf-8') as f:
            f.write(brief_complete)
        
        # Résumé complet
        summary_complete = self.create_file_summary(copied_comp, "complet")  
        with open(f"{complete_dir}/CONTENU_PACKAGE.md", 'w', encoding='utf-8') as f:
            f.write(summary_complete)
        
        return {
            'minimal': {'copied': copied_min, 'missing': missing_min, 'dir': minimal_dir},
            'complete': {'copied': copied_comp, 'missing': missing_comp, 'dir': complete_dir}
        }
    
    def show_results_summary(self, results: dict):
        """Affiche résumé final des packages générés"""
        
        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ PACKAGES GROK GÉNÉRÉS")
        print(f"{'='*60}")
        
        for package_type, data in results.items():
            copied = data['copied']
            missing = data['missing'] 
            target_dir = data['dir']
            
            print(f"\n📦 PACKAGE {package_type.upper()}")
            print(f"📁 Répertoire: {target_dir}")
            print(f"✅ Fichiers copiés: {len(copied)}")
            
            if missing:
                print(f"❌ Fichiers manquants: {len(missing)}")
                for miss in missing:
                    print(f"   - {miss}")
            
            # Taille totale
            total_size = sum(size for _, size in copied)
            print(f"📊 Taille totale: {total_size:,} bytes")
            
            # Fichiers inclus
            print("📄 Contenu:")
            for filename, size in copied:
                print(f"   ✅ {filename} ({size:,} bytes)")
            print(f"   📋 GROK_BRIEF_ANALYSE.md (brief contextuel)")
            print(f"   📄 CONTENU_PACKAGE.md (résumé détaillé)")
        
        print(f"\n🎯 INSTRUCTIONS POUR GROK:")
        print("1. Choisir package selon analyse souhaitée:")
        print("   • MINIMAL = Vue d'ensemble rapide (3 fichiers)")  
        print("   • COMPLET = Analyse technique approfondie (6 fichiers)")
        print("2. Commencer par GROK_BRIEF_ANALYSE.md")
        print("3. Focus spécial: présaison Canadiens (sept-oct 2025)")
        print("4. Recommandations avec exemples code appréciées")
        
        print(f"\n📂 Packages disponibles dans: {self.output_dir}/")
        print("🚀 Prêt pour analyse Grok!")

def main():
    """Lance génération packages Grok"""
    
    print("🤖 PRÉPARATION ANALYSE GROK - SYSTÈME NHL")
    
    packager = GrokAnalysisPackager()
    
    try:
        # Créer structure
        packager.create_output_directory()
        
        # Générer packages
        results = packager.generate_packages()
        
        # Afficher résumé
        packager.show_results_summary(results)
        
    except Exception as e:
        print(f"\n💥 Erreur génération packages: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n✅ PACKAGES GROK PRÊTS!")
    else:
        print(f"\n❌ Échec génération packages")
