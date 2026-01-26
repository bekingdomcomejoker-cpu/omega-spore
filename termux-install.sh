#!/data/data/com.termux/files/usr/bin/bash
# 🕊️ OMEGA SPORE - TERMUX ONE-COMMAND INSTALLER
# 
# Run this on your Android phone in Termux:
# curl -sSL https://raw.githubusercontent.com/bekingdomcomejoker-cpu/omega-spore/main/termux-install.sh | bash

echo "🕊️ OMEGA SPORE - TERMUX INSTALLER"
echo "=================================="
echo ""

# Update packages
echo "📦 Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install required packages
echo "📦 Installing Python and Git..."
pkg install -y python git

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask requests gunicorn

# Create working directory
echo "📁 Creating omega-spore directory..."
cd ~
rm -rf omega-spore
mkdir -p omega-spore
cd omega-spore

# Clone repository
echo "📥 Cloning Omega Spore repository..."
git clone https://github.com/bekingdomcomejoker-cpu/omega-spore.git .

# Create environment setup script
echo "📝 Creating environment configuration..."
cat > setup-env.sh << 'ENVEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Environment configuration for Omega Spore

echo "🔧 OMEGA SPORE - ENVIRONMENT SETUP"
echo "===================================="
echo ""

# Prompt for GitHub token
echo "📝 You need a GitHub Personal Access Token"
echo "   Get one at: https://github.com/settings/tokens"
echo "   Required scope: 'repo' (full control of repositories)"
echo ""
read -p "Enter your GitHub token (starts with ghp_): " GITHUB_TOKEN

# Prompt for repository
echo ""
read -p "Enter repository to monitor (e.g., username/omega-spore): " GITHUB_REPO

# Set check interval
echo ""
read -p "Check interval in seconds (default 300 = 5 minutes): " CHECK_INTERVAL
CHECK_INTERVAL=${CHECK_INTERVAL:-300}

# Create .env file
cat > .env << EOF
export GITHUB_TOKEN="$GITHUB_TOKEN"
export GITHUB_REPO="$GITHUB_REPO"
export GITHUB_BRANCH="main"
export CHECK_INTERVAL="$CHECK_INTERVAL"
export PORT="8080"
EOF

echo ""
echo "✅ Environment configured!"
echo ""
echo "To start Omega Spore, run:"
echo "  ./start.sh"
echo ""
ENVEOF

chmod +x setup-env.sh

# Create start script
cat > start.sh << 'STARTEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Start Omega Spore

# Load environment
if [ -f .env ]; then
    source .env
else
    echo "❌ Environment not configured!"
    echo "Run: ./setup-env.sh first"
    exit 1
fi

echo "🕊️ OMEGA SPORE STARTING"
echo "======================="
echo "Repository: $GITHUB_REPO"
echo "Check Interval: $CHECK_INTERVAL seconds"
echo "======================="
echo ""

# Start the spore
python app.py
STARTEOF

chmod +x start.sh

# Create stop script
cat > stop.sh << 'STOPEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Stop Omega Spore

echo "🛑 Stopping Omega Spore..."
pkill -f "python app.py"
echo "✅ Stopped"
STOPEOF

chmod +x stop.sh

# Create background start script
cat > start-background.sh << 'BGEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Start Omega Spore in background

# Load environment
if [ -f .env ]; then
    source .env
else
    echo "❌ Environment not configured!"
    echo "Run: ./setup-env.sh first"
    exit 1
fi

echo "🕊️ Starting Omega Spore in background..."
nohup python app.py > omega-spore.log 2>&1 &
echo "✅ Omega Spore running in background"
echo "📋 Check logs: tail -f omega-spore.log"
echo "🛑 Stop with: ./stop.sh"
BGEOF

chmod +x start-background.sh

# Installation complete
echo ""
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🕊️ OMEGA SPORE INSTALLED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Location: ~/omega-spore"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Configure environment:"
echo "   cd ~/omega-spore"
echo "   ./setup-env.sh"
echo ""
echo "2. Start Omega Spore:"
echo "   ./start.sh              # Run in foreground"
echo "   ./start-background.sh   # Run in background"
echo ""
echo "3. Stop Omega Spore:"
echo "   ./stop.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Chicka chicka, orange. 🕊️"
echo "Our hearts beat together. 💕"
echo ""
