# 🎯 Guide Analyseur IA - Paris LNH 2025-26

## 🚀 Utilisation Rapide

### 📱 Workflow Recommandé

1. **Copier les cotes Mise-o-jeu+** depuis le site ou PDF
2. **Les structurer** dans le template JSON (`data/template_cotes_mise_o_jeu.json`)
3. **Lancer l'analyse** : `python mise_o_jeu_main.py --odds-file mes_cotes.json`
4. **Obtenir le plan de mise** structuré (20$ ouverture + 20$ futures)

### 💡 Démonstration Express
```bash
# Test rapide avec cotes d'exemple
python mise_o_jeu_main.py

# Analyse avec vos cotes réelles
python mise_o_jeu_main.py --odds-file data/template_cotes_mise_o_jeu.json --save-report
```

## 📋 Format de Sortie (Comme Demandé)

### 1️⃣ Résumé des Nouvelles Confirmées
- ✅ **Impact POSITIF** : Nouvelles qui améliorent les chances
- ❌ **Impact NÉGATIF** : Nouvelles qui réduisent les chances  
- ⚠️ **RUMEURS** : Informations non confirmées à surveiller

### 2️⃣ Tableau des Meilleures Value Bets
```
Marché                Selection           Cote   P_imp  P_adj  Value  Cat
Hart Trophy           Connor McDavid      3.50   28.6%  40.0%  11.4%  MID
Coupe Stanley         Edmonton Oilers     6.50   15.4%  18.0%  2.6%   SAFE
Division Atlantique   Toronto Maple Leafs 3.25   30.8%  36.0%  5.2%   MID
```

### 3️⃣ Plan de Mise Détaillé

#### 🏒 **OUVERTURE (20$ - Matchs 7-8 octobre)**
- Mises sur les matchs d'ouverture avec value détectée
- Allocation optimale du budget court terme

#### 🏆 **FUTURES (20$ - Saison complète)**
- **SAFE** (40% du budget) : Paris sûrs, variance faible
- **MID** (40% du budget) : Équilibre risque/rendement
- **BOLD** (20% du budget) : Longshots à gros jackpot

### 4️⃣ Gains Potentiels Attendus
- **ROI attendu** pour chaque catégorie
- **Scénarios optimistes** vs **conservateurs**
- **Profil de risque global**

## 🔍 Méthodologie Value Betting

### Calculs Automatiques
- **p_imp = 1/cote** (probabilité implicite)
- **p_adj** = probabilité ajustée (nouvelles + stats + contexte)
- **value = p_adj - p_imp** (positif = opportunité)

### Facteurs Considérés
- 📰 **Nouvelles récentes** (dernières 24-48h)
- 📊 **Statistiques avancées** (forme, performance)
- 🏒 **Contexte équipe** (roster, chimie, motivation)
- 🎯 **Analyse comparative** (cotes vs probabilités réelles)

## 🏆 Compétition IA

### Objectif Final
Comparer les prédictions avec d'autres IA:
- **Gemini** vs **Claude** vs **Grok** vs **ChatGPT**
- Métrique de succès: **ROI réel** à la fin de saison
- Tracking des **taux de réussite** par catégorie

### Format Standardisé
Chaque IA produit:
1. Plan de mise identique (20$ + 20$)
2. Justifications pour chaque choix
3. Prédictions ROI attendu
4. Niveau de confiance

## 📊 Structure des Cotes (Template)

### Format JSON Requis
```json
{
  "stanley_cup": {
    "Edmonton Oilers": 6.50,
    "Toronto Maple Leafs": 8.00
  },
  "divisions": {
    "Atlantique": {
      "Toronto Maple Leafs": 3.25
    }
  },
  "trophees": {
    "Hart Trophy": {
      "Connor McDavid": 3.50
    }
  }
}
```

### Sources Recommandées
- **Site officiel Mise-o-jeu+** (cotes en temps réel)
- **PDF des cotes** (version imprimable)
- **Screenshots** (pour vérification)

## ⚡ Commandes Avancées

### Sauvegarde Automatique
```bash
python mise_o_jeu_main.py --odds-file cotes.json --save-report
# Génère: data/analyse_mise_o_jeu_YYYYMMDD_HHMM.json
```

### Analyse Jupyter Interactive
```bash
jupyter notebook analyse_paris_nhl.ipynb
# Interface graphique avec visualisations
```

### Comparaison Multi-Budgets
```bash
# Test différentes stratégies
python main.py --budget 20 --strategy safe
python main.py --budget 40 --strategy bold
```

## 🎯 Conseils Optimisation

### Timing Idéal
- **Pré-saison** (septembre) : Futures et trophées
- **Début saison** (octobre) : Ajustements rapides
- **Nouvelles importantes** : Recalcul immédiat

### Gestion Risque
- Jamais plus de **25% du bankroll** sur un pari
- Diversification **SAFE/MID/BOLD** obligatoire
- Suivi des **nouvelles de dernière minute**

### Tracking Performance
- Noter tous les paris effectués
- Comparer **ROI prédit vs réel**
- Ajuster la méthodologie selon résultats

---

🏆 **Prêt pour la compétition IA LNH 2025-26!**

*Que la meilleure analyse gagne!* 🤖⚔️
