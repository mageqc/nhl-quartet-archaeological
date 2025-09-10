# 🏒 NHL Quartet Archaeological - Complete Betting Analysis System

## 🎯 Overview
Advanced NHL betting prediction system with real-time data integration, featuring multiple interfaces and comprehensive analytics.

## ✅ Key Features

### 🔗 Real Data Integration
- **1,358 real NHL players** from official NHL API
- **31 teams** complete roster analysis  
- **Live odds** via The Odds API
- **Trade rumors** monitoring

### 🎮 Applications Available

#### 📅 Grok Calendar Ultimate (Port 5006) - LATEST
```bash
python grok_calendar_ultimate.py
```
- Interactive calendar (Monthly/Weekly/Daily views)
- Varied realistic odds (1.75-2.35)
- Expected Value calculations
- Kelly Criterion bet sizing
- Re-predict and Reset functionality

#### 🎯 Maestro Complex System (Port 5004)
```bash
python maestro_grok_roster_ultimate.py  
```
- Full NHL data bridge integration
- Complex analytics and predictions
- Comprehensive team analysis

#### 🎲 Simple Grok Interface (Port 5005)  
```bash
python grok_style_real_data.py
```
- Clean minimalist design
- Real NHL data backend
- Quick predictions

## 🚀 Quick Start

### Prerequisites
```bash
pip install flask requests beautifulsoup4
```

### Launch Application
```bash
# Latest Grok Calendar system
python grok_calendar_ultimate.py

# Open browser to: http://localhost:5006
```

### Usage
1. Select team (MTL, TOR, BOS, etc.)
2. Choose view (Monthly/Weekly/Daily)  
3. Click "🔮 Prédire" for predictions
4. Use "🔄 Re-prédire" to test variations
5. Track results with "✅ Gagné" / "❌ Perdu"

## 📊 Technical Features

- **Expected Value (EV)** calculations
- **Kelly Criterion** bet sizing  
- **ROI tracking** and simulation
- **Real-time odds** variation (1.75-2.35)
- **Team strength** analysis (0-100 score)
- **Conservative betting** (max 2% bankroll)

## 🔧 Architecture

### Core Components
- `grok_calendar_ultimate.py` - Latest calendar interface
- `active/nhl_maestro_bridge.py` - Real data integration
- `active/nhl_complete_roster_system.py` - Player database
- `active/nhl_roster_analyzer.py` - Team analysis engine

### Data Sources  
- **NHL API** - Official player data
- **The Odds API** - Live betting odds
- **NHL Trade Rumors** - Market sentiment

## 🎯 Betting Features

### Risk Management
- Conservative Kelly sizing (25% + 0.5 factor)
- Maximum 2% per bet
- EV threshold recommendations
- Automatic $0 bets for negative EV

### Analysis Metrics
- Team strength scores (0-100)
- Win probability adjustments  
- Rumor sentiment integration
- Historical performance tracking

## 🏆 Success Metrics

System generates recommendations like:
- **47.2% EV** ✅ PARI RECOMMANDÉ
- **-2.3% EV** ❌ Skip
- **Varied odds** 1.77 to 2.25
- **Smart sizing** $0.00 to $2.00

## 📱 Interface Design

- **Dark theme** optimized for extended use
- **Responsive design** for all devices  
- **Real-time updates** without page refresh
- **Intuitive controls** for easy navigation

## ⚠️ Disclaimer

This is a **simulation and analysis tool**. Always:
- Test extensively before real betting
- Follow local gambling regulations
- Bet responsibly within your means
- Understand that sports betting involves risk

## 🔗 API Integration

### The Odds API Setup
```python
ODDS_API_KEY = "your_key_here"  # Get from theoddsapi.com
```

### NHL API Usage  
- Automatic roster downloads
- Real-time player statistics
- Team performance metrics

---

**🏒 Built for NHL fans who want data-driven betting analysis**

*Last updated: September 2025*
