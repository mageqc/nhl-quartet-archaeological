# 🏒 Guide d'Utilisation - Analyseur Paris LNH

## 🚀 Démarrage Rapide

### Interface en Ligne de Commande
```bash
# Analyse standard (budget 20$, stratégie mixte)
python main.py

# Analyse personnalisée
python main.py --budget 40 --strategy bold --update-news

# Options disponibles:
# --budget: 20, 40, etc. (budget en dollars)
# --strategy: safe, mixed, bold
# --update-news: met à jour les nouvelles avant analyse
```

### Interface Jupyter Notebook
```bash
# Ouvrir le notebook interactif
jupyter notebook analyse_paris_nhl.ipynb
```

## 📊 Types d'Analyse

### Stratégies de Mise
- **SAFE**: Favoris solides, variance faible (ROI ~20-40%)
- **MID**: Équilibre risque/rendement (ROI ~30-60%)  
- **BOLD**: Longshots, gros jackpots (ROI ~50-100%+)

### Marchés Analysés
- 🏆 **Vainqueurs de division** (Atlantique, Métropolitaine, etc.)
- 🎯 **Props de joueurs** (buts, points, assists)
- 🏒 **Coupe Stanley** (tous les favoris et longshots)
- 🥇 **Trophées individuels** (Hart, Calder, Norris, etc.)

## 🔍 Méthodologie

### Calcul de Value Betting
1. **Probabilité implicite**: `p_imp = 1/cote`
2. **Probabilité ajustée**: Analyse nouvelles + stats + contexte
3. **Value**: `p_adj - p_imp` (positif = opportunité)

### Facteurs Considérés
- 📰 **Nouvelles récentes**: Trades, blessures, rumeurs confirmées
- 📈 **Statistiques avancées**: Performance historique
- 🏒 **Contexte équipe**: Roster, chimie, momentum
- 💰 **Gestion bankroll**: Critère de Kelly modifié

## 💡 Conseils d'Utilisation

### Budget Recommandé
- **Débutant**: 20$ (stratégie SAFE/MID)
- **Intermédiaire**: 40$ (stratégie MIXED)
- **Avancé**: 2x20$ (diversification temporelle)

### Timing Optimal
- **Pré-saison**: Futures et trophées
- **Début saison**: Ajustements rapides sur props joueurs
- **Mi-saison**: Recalibrage based nouvelles performances

### Gestion des Risques
- ✅ Ne jamais dépasser 25% du bankroll sur un pari
- ✅ Diversifier entre catégories SAFE/MID/BOLD
- ✅ Tenir compte des nouvelles de dernière minute
- ✅ Réajuster selon les performances

## 📱 Fonctionnalités Avancées

### Suivi en Temps Réel
- Surveillance automatique des nouvelles
- Recalcul des probabilités ajustées
- Alertes sur nouvelles opportunités

### Export des Données
- Sauvegarde automatique des analyses
- Historique des recommandations
- Tracking de performance

## 🎯 Objectifs de Performance

### Cibles ROI par Stratégie
- **SAFE**: 15-25% (probabilité succès ~70%)
- **MID**: 25-40% (probabilité succès ~50%)
- **BOLD**: 50%+ (probabilité succès ~20-30%)

### Métriques de Succès
- ROI global > 20% sur la saison
- Taux de réussite > 40% des paris
- Préservation du capital (max drawdown < 30%)

---
💡 **Rappel**: Cet outil est conçu pour l'analyse et l'éducation. Pariez toujours de manière responsable!
