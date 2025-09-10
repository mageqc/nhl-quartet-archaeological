#!/bin/bash

# 🌙 CRON JOB SETUP POUR NIGHTLY UPDATE TRIO
# Setup automatique pour job nocturne 2am quotidien

echo "🌙 Setting up NHL Trio Nightly Job..."

# Répertoire du projet
PROJECT_DIR="/Volumes/Disque Dur/Dev/NHL 2025-2026"
PYTHON_SCRIPT="$PROJECT_DIR/nightly_update_trio.py"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/nightly_updates.log"

# Créer répertoire logs si inexistant
mkdir -p "$LOG_DIR"

# Créer wrapper script pour cron
WRAPPER_SCRIPT="$PROJECT_DIR/run_nightly_cron.sh"

cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash

# Wrapper pour cron job nightly update
cd "/Volumes/Disque Dur/Dev/NHL 2025-2026"

# Log avec timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting nightly update..." >> logs/nightly_updates.log

# Run nightly job avec timeout
timeout 300 python3 nightly_update_trio.py >> logs/nightly_updates.log 2>&1

# Status code
EXIT_CODE=$?
echo "$(date '+%Y-%m-%d %H:%M:%S') - Completed with exit code: $EXIT_CODE" >> logs/nightly_updates.log

# Rotation logs si trop gros (>10MB)
LOG_SIZE=$(stat -f%z logs/nightly_updates.log 2>/dev/null || echo 0)
if [ "$LOG_SIZE" -gt 10485760 ]; then
    mv logs/nightly_updates.log logs/nightly_updates.log.old
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Log rotated" > logs/nightly_updates.log
fi

exit $EXIT_CODE
EOF

# Rendre wrapper exécutable
chmod +x "$WRAPPER_SCRIPT"

# Cron entry (2am quotidien)
CRON_ENTRY="0 2 * * * $WRAPPER_SCRIPT"

echo "📋 Cron job entry:"
echo "$CRON_ENTRY"
echo ""

# Check si cron entry existe déjà
if crontab -l 2>/dev/null | grep -q "$WRAPPER_SCRIPT"; then
    echo "✅ Cron job already exists"
else
    echo "➕ Adding cron job..."
    
    # Backup current crontab
    crontab -l 2>/dev/null > /tmp/current_crontab || touch /tmp/current_crontab
    
    # Add new entry
    echo "$CRON_ENTRY" >> /tmp/current_crontab
    
    # Install new crontab
    crontab /tmp/current_crontab
    
    echo "✅ Cron job added successfully!"
fi

# Vérification
echo ""
echo "📅 Current crontab:"
crontab -l | grep -E "(nightly|NHL)" || echo "No NHL entries found"

echo ""
echo "🧪 Testing nightly job..."
echo "Running test execution..."

# Test run
cd "$PROJECT_DIR"
python3 nightly_update_trio.py "2025-09-22" | head -20

echo ""
echo "✅ Nightly job setup complete!"
echo "📁 Logs location: $LOG_FILE"
echo "⏰ Job runs daily at 2:00 AM"
echo "🔧 Manual run: cd '$PROJECT_DIR' && python3 nightly_update_trio.py"
