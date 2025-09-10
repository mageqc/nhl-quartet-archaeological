#!/usr/bin/env python3
"""
🎨 NHL LOGOS OFFICIELS - SYSTÈME COMPLET
Intégration logos officiels NHL dans dashboard et calendrier

Sources logos:
- NHL.com logos officiels
- SVG vectoriels haute qualité  
- URLs publiques stables
- Fallback vers badges texte
"""

import json
from typing import Dict, Optional

class NHLLogosSystem:
    """
    🎨 GESTIONNAIRE LOGOS OFFICIELS NHL
    
    Fonctionnalités:
    - URLs logos officiels toutes équipes
    - Différentes tailles (petit, moyen, grand)
    - Fallback gracieux si logo indisponible
    - Intégration dashboard et calendrier
    """
    
    def __init__(self):
        print("🎨 NHL LOGOS SYSTEM - INTÉGRATION COMPLÈTE")
        print("=" * 50)
        
        # URLs logos officiels NHL (domaine public NHL.com)
        self.team_logos = self.get_official_nhl_logos()
        
        # Configuration tailles
        self.logo_sizes = {
            'small': '24px',
            'medium': '48px', 
            'large': '64px',
            'xl': '96px'
        }
        
        print(f"✅ {len(self.team_logos)} logos NHL chargés")
    
    def get_official_nhl_logos(self) -> Dict[str, Dict]:
        """URLs logos officiels NHL"""
        
        # Base URL NHL pour logos (domaine public)
        base_url = "https://assets.nhle.com/logos/nhl/svg"
        
        # Mapping équipes avec leurs logos officiels
        logos = {
            # Atlantic Division
            'TOR': {
                'name': 'Toronto Maple Leafs',
                'logo_url': f"{base_url}/TOR_light.svg",
                'colors': {'primary': '#003E7E', 'secondary': '#FFFFFF'},
                'city': 'Toronto'
            },
            'BOS': {
                'name': 'Boston Bruins', 
                'logo_url': f"{base_url}/BOS_light.svg",
                'colors': {'primary': '#FFB81C', 'secondary': '#000000'},
                'city': 'Boston'
            },
            'FLA': {
                'name': 'Florida Panthers',
                'logo_url': f"{base_url}/FLA_light.svg", 
                'colors': {'primary': '#C8102E', 'secondary': '#041E42'},
                'city': 'Sunrise'
            },
            'TBL': {
                'name': 'Tampa Bay Lightning',
                'logo_url': f"{base_url}/TBL_light.svg",
                'colors': {'primary': '#002868', 'secondary': '#FFFFFF'},
                'city': 'Tampa Bay'
            },
            'BUF': {
                'name': 'Buffalo Sabres',
                'logo_url': f"{base_url}/BUF_light.svg",
                'colors': {'primary': '#003087', 'secondary': '#FFB81C'},
                'city': 'Buffalo'
            },
            'MTL': {
                'name': 'Montreal Canadiens',
                'logo_url': f"{base_url}/MTL_light.svg",
                'colors': {'primary': '#AF1E2D', 'secondary': '#192168'},
                'city': 'Montreal'
            },
            'OTT': {
                'name': 'Ottawa Senators',
                'logo_url': f"{base_url}/OTT_light.svg",
                'colors': {'primary': '#C52032', 'secondary': '#000000'},
                'city': 'Ottawa'
            },
            'DET': {
                'name': 'Detroit Red Wings',
                'logo_url': f"{base_url}/DET_light.svg",
                'colors': {'primary': '#CE1126', 'secondary': '#FFFFFF'},
                'city': 'Detroit'
            },
            
            # Metropolitan Division
            'NYR': {
                'name': 'New York Rangers',
                'logo_url': f"{base_url}/NYR_light.svg",
                'colors': {'primary': '#0038A8', 'secondary': '#CE1126'},
                'city': 'New York'
            },
            'CAR': {
                'name': 'Carolina Hurricanes',
                'logo_url': f"{base_url}/CAR_light.svg",
                'colors': {'primary': '#CE1126', 'secondary': '#000000'},
                'city': 'Raleigh'
            },
            'NJD': {
                'name': 'New Jersey Devils',
                'logo_url': f"{base_url}/NJD_light.svg",
                'colors': {'primary': '#CE1126', 'secondary': '#000000'},
                'city': 'Newark'
            },
            'WSH': {
                'name': 'Washington Capitals',
                'logo_url': f"{base_url}/WSH_light.svg",
                'colors': {'primary': '#041E42', 'secondary': '#C8102E'},
                'city': 'Washington'
            },
            'PHI': {
                'name': 'Philadelphia Flyers',
                'logo_url': f"{base_url}/PHI_light.svg",
                'colors': {'primary': '#F74902', 'secondary': '#000000'},
                'city': 'Philadelphia'
            },
            'PIT': {
                'name': 'Pittsburgh Penguins',
                'logo_url': f"{base_url}/PIT_light.svg",
                'colors': {'primary': '#000000', 'secondary': '#FCB514'},
                'city': 'Pittsburgh'
            },
            'NYI': {
                'name': 'New York Islanders',
                'logo_url': f"{base_url}/NYI_light.svg",
                'colors': {'primary': '#00539B', 'secondary': '#F47D30'},
                'city': 'Long Island'
            },
            'CBJ': {
                'name': 'Columbus Blue Jackets',
                'logo_url': f"{base_url}/CBJ_light.svg",
                'colors': {'primary': '#002654', 'secondary': '#CE1126'},
                'city': 'Columbus'
            },
            
            # Central Division
            'COL': {
                'name': 'Colorado Avalanche',
                'logo_url': f"{base_url}/COL_light.svg",
                'colors': {'primary': '#6F263D', 'secondary': '#236192'},
                'city': 'Denver'
            },
            'DAL': {
                'name': 'Dallas Stars',
                'logo_url': f"{base_url}/DAL_light.svg",
                'colors': {'primary': '#006847', 'secondary': '#8F8F8C'},
                'city': 'Dallas'
            },
            'WPG': {
                'name': 'Winnipeg Jets',
                'logo_url': f"{base_url}/WPG_light.svg",
                'colors': {'primary': '#041E42', 'secondary': '#004C97'},
                'city': 'Winnipeg'
            },
            'NSH': {
                'name': 'Nashville Predators',
                'logo_url': f"{base_url}/NSH_light.svg",
                'colors': {'primary': '#FFB81C', 'secondary': '#041E42'},
                'city': 'Nashville'
            },
            'MIN': {
                'name': 'Minnesota Wild',
                'logo_url': f"{base_url}/MIN_light.svg",
                'colors': {'primary': '#154734', 'secondary': '#A6192E'},
                'city': 'Saint Paul'
            },
            'STL': {
                'name': 'St. Louis Blues',
                'logo_url': f"{base_url}/STL_light.svg",
                'colors': {'primary': '#002F87', 'secondary': '#FCB514'},
                'city': 'St. Louis'
            },
            'UTA': {
                'name': 'Utah Hockey Club',
                'logo_url': f"{base_url}/UTA_light.svg",
                'colors': {'primary': '#69BE28', 'secondary': '#000000'},
                'city': 'Salt Lake City'
            },
            'CHI': {
                'name': 'Chicago Blackhawks',
                'logo_url': f"{base_url}/CHI_light.svg",
                'colors': {'primary': '#CE1126', 'secondary': '#000000'},
                'city': 'Chicago'
            },
            
            # Pacific Division
            'EDM': {
                'name': 'Edmonton Oilers',
                'logo_url': f"{base_url}/EDM_light.svg",
                'colors': {'primary': '#041E42', 'secondary': '#FF4C00'},
                'city': 'Edmonton'
            },
            'VEG': {
                'name': 'Vegas Golden Knights',
                'logo_url': f"{base_url}/VGK_light.svg",
                'colors': {'primary': '#B4975A', 'secondary': '#333F42'},
                'city': 'Las Vegas'
            },
            'LAK': {
                'name': 'Los Angeles Kings',
                'logo_url': f"{base_url}/LAK_light.svg",
                'colors': {'primary': '#000000', 'secondary': '#A2AAAD'},
                'city': 'Los Angeles'
            },
            'VAN': {
                'name': 'Vancouver Canucks',
                'logo_url': f"{base_url}/VAN_light.svg",
                'colors': {'primary': '#00205B', 'secondary': '#00843D'},
                'city': 'Vancouver'
            },
            'CGY': {
                'name': 'Calgary Flames',
                'logo_url': f"{base_url}/CGY_light.svg",
                'colors': {'primary': '#C8102E', 'secondary': '#F1BE48'},
                'city': 'Calgary'
            },
            'SEA': {
                'name': 'Seattle Kraken',
                'logo_url': f"{base_url}/SEA_light.svg",
                'colors': {'primary': '#001628', 'secondary': '#99D9D9'},
                'city': 'Seattle'
            },
            'ANA': {
                'name': 'Anaheim Ducks',
                'logo_url': f"{base_url}/ANA_light.svg",
                'colors': {'primary': '#F47A38', 'secondary': '#B9975B'},
                'city': 'Anaheim'
            },
            'SJS': {
                'name': 'San Jose Sharks',
                'logo_url': f"{base_url}/SJS_light.svg",
                'colors': {'primary': '#006D75', 'secondary': '#EA7200'},
                'city': 'San Jose'
            }
        }
        
        return logos
    
    def get_team_logo_html(self, team_abbrev: str, size: str = 'medium', 
                          include_name: bool = False) -> str:
        """Génère HTML pour logo d'équipe"""
        
        team_info = self.team_logos.get(team_abbrev, {})
        
        if not team_info:
            # Fallback badge texte
            return f'''
                <div class="team-badge fallback" style="
                    background: #ccc; color: #333; padding: 4px 8px; 
                    border-radius: 4px; font-weight: bold; font-size: 12px;
                ">
                    {team_abbrev}
                </div>
            '''
        
        logo_url = team_info['logo_url']
        team_name = team_info['name']
        primary_color = team_info['colors']['primary']
        logo_size = self.logo_sizes.get(size, self.logo_sizes['medium'])
        
        # HTML avec logo officiel
        html = f'''
            <div class="team-logo-container" style="display: inline-flex; align-items: center; gap: 8px;">
                <img src="{logo_url}" 
                     alt="{team_name}" 
                     class="team-logo {team_abbrev.lower()}"
                     style="
                        width: {logo_size}; 
                        height: {logo_size}; 
                        border-radius: 4px;
                        background: {primary_color}20;
                        padding: 2px;
                     "
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='inline-block';"
                >
                <span class="team-fallback" style="
                    display: none; 
                    background: {primary_color}; 
                    color: white; 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    font-weight: bold;
                    font-size: 12px;
                ">
                    {team_abbrev}
                </span>
        '''
        
        if include_name:
            html += f'''
                <span class="team-name" style="
                    color: {primary_color}; 
                    font-weight: 600;
                    font-size: 14px;
                ">
                    {team_name}
                </span>
            '''
        
        html += '</div>'
        
        return html
    
    def get_matchup_html(self, away_team: str, home_team: str, 
                        size: str = 'medium', show_vs: bool = True) -> str:
        """Génère HTML pour matchup avec logos"""
        
        away_logo = self.get_team_logo_html(away_team, size)
        home_logo = self.get_team_logo_html(home_team, size)
        
        vs_element = '''
            <span class="vs-separator" style="
                color: #ffd700; 
                font-weight: bold; 
                font-size: 16px;
                margin: 0 8px;
            ">@</span>
        ''' if show_vs else ''
        
        return f'''
            <div class="game-matchup-logos" style="
                display: flex; 
                align-items: center; 
                justify-content: center;
                gap: 4px;
            ">
                {away_logo}
                {vs_element}
                {home_logo}
            </div>
        '''
    
    def export_logos_css(self) -> str:
        """Génère CSS pour tous les logos NHL"""
        
        css = """
        /* 🎨 NHL LOGOS OFFICIELS - CSS */
        
        .team-logo-container {
            transition: all 0.3s ease;
        }
        
        .team-logo-container:hover {
            transform: scale(1.05);
        }
        
        .team-logo {
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            transition: filter 0.3s ease;
        }
        
        .team-logo:hover {
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)) brightness(1.1);
        }
        
        .game-matchup-logos {
            background: rgba(255,255,255,0.05);
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255,215,0,0.3);
        }
        
        .team-fallback {
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Équipes spécifiques */
        """
        
        # Ajouter styles spécifiques par équipe
        for abbrev, team_info in self.team_logos.items():
            primary = team_info['colors']['primary']
            css += f"""
        .team-logo.{abbrev.lower()}:hover {{
            box-shadow: 0 0 12px {primary}40;
        }}
        """
        
        css += "\n"
        
        return css
    
    def save_logos_config(self):
        """Sauvegarde config logos en JSON"""
        
        config = {
            'teams': self.team_logos,
            'sizes': self.logo_sizes,
            'css_classes': {
                'container': 'team-logo-container',
                'logo': 'team-logo',
                'fallback': 'team-fallback',
                'matchup': 'game-matchup-logos'
            },
            'generated_at': '2025-09-09',
            'version': '1.0'
        }
        
        with open('nhl_logos_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Configuration logos sauvée: nhl_logos_config.json")
    
    def test_logo_system(self):
        """Teste le système de logos"""
        
        print("\n🧪 TEST SYSTÈME LOGOS NHL")
        print("=" * 40)
        
        # Test quelques équipes
        test_teams = ['MTL', 'TOR', 'BOS', 'NYR', 'VEG']
        
        for team in test_teams:
            logo_html = self.get_team_logo_html(team, 'medium', include_name=True)
            print(f"✅ {team}: Logo HTML généré ({len(logo_html)} chars)")
        
        # Test matchup
        matchup_html = self.get_matchup_html('MTL', 'TOR', 'large')
        print(f"✅ Matchup MTL @ TOR: HTML généré ({len(matchup_html)} chars)")
        
        # Générer CSS
        css = self.export_logos_css()
        print(f"✅ CSS généré: {len(css)} caractères")
        
        return True

def main():
    """Lance le système logos NHL"""
    
    print("🚀 NHL LOGOS SYSTEM - INITIALISATION")
    
    logos_system = NHLLogosSystem()
    
    # Test système
    logos_system.test_logo_system()
    
    # Sauvegarder config
    logos_system.save_logos_config()
    
    print(f"\n🎨 SYSTÈME LOGOS NHL PRÊT!")
    print(f"✅ 32 équipes avec logos officiels")
    print(f"✅ Fallback automatique si logo indisponible") 
    print(f"✅ CSS et configuration générés")

if __name__ == "__main__":
    main()
