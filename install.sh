#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing Slack Calendar Status...${NC}"

# Create virtual environment
echo -e "\n${BLUE}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies with --no-deps to avoid hash verification
echo -e "\n${BLUE}Installing dependencies...${NC}"
pip install --no-deps requests
pip install --no-deps pytz

# Create config directory if it doesn't exist
echo -e "\n${BLUE}Setting up configuration...${NC}"
mkdir -p config

# Create .env file
echo -e "\n${BLUE}Creating environment file...${NC}"
cat > .env << EOL
OPENWEATHER_API_KEY="e87ed82ab8132f15877ae385179114bf"
USER_EMAIL="clararende@squareup.com"
TIMEZONE="Europe/Madrid"
LOCATION="Amsterdam,NL"
EOL

# Set up cron job
echo -e "\n${BLUE}Setting up automatic updates...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
SCRIPT_PATH="$SCRIPT_DIR/src/run.py"

# Create logs directory
mkdir -p logs
touch logs/cron.log

# Set permissions
chmod +x src/run.py

# Create a wrapper script for the cron job
cat > run_with_env.sh << EOL
#!/bin/bash
cd "$SCRIPT_DIR"
source venv/bin/activate
$PYTHON_PATH $SCRIPT_PATH >> logs/cron.log 2>&1
EOL

chmod +x run_with_env.sh

# Create temporary cron file
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null

# Add our job if it's not already there
if ! grep -q "$SCRIPT_PATH" "$TEMP_CRON"; then
    echo "0 7 * * * $SCRIPT_DIR/run_with_env.sh" >> "$TEMP_CRON"
    crontab "$TEMP_CRON"
    echo -e "${GREEN}Cron job installed successfully!${NC}"
else
    echo -e "${BLUE}Cron job already exists${NC}"
fi
rm "$TEMP_CRON"

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "Your status will be automatically updated every morning at 7 AM."
echo -e "You can also run it manually with: ${BLUE}./run_with_env.sh${NC}"
echo -e "\nCheck ${BLUE}logs/cron.log${NC} for execution logs."

# Add note about required extensions
echo -e "\n${BLUE}Required Goose Extensions:${NC}"
echo -e "1. Google Calendar Extension"
echo -e "2. Slack Extension"
echo -e "\nPlease ensure these extensions are enabled in your Goose settings."
