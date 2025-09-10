#!/bin/bash
# 🏛️💎 Script de déploiement GitHub pour NHL Quartet Archaeological System

echo "🚀 DÉPLOIEMENT GITHUB EN COURS..."
echo "🏛️ Système Quartet Archéologique -> GitHub"

# Remplace [TON-USERNAME] par ton vrai username GitHub !
GITHUB_USERNAME="[TON-USERNAME]"
REPO_NAME="nhl-quartet-archaeological"

echo "📡 Configuration remote GitHub..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

echo "🌟 Configuration de la branche principale..."
git branch -M main

echo "🚀 Premier push vers GitHub..."
git push -u origin main

echo "✅ SUCCÈS ! Ton système quartet archéologique est maintenant sur GitHub !"
echo "🌐 URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "🏛️💎 263 fichiers avec mine d'or déployés ! 🚀✨"
