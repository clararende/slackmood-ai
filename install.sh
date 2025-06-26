#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing SlackMood AI...${NC}"

# Check if uvx is installed
if ! command -v uvx &> /dev/null; then
    echo -e "\n${BLUE}Installing uvx (required for MCP servers)...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo -e "${GREEN}uvx installed successfully!${NC}"
else
    echo -e "\n${BLUE}uvx is already installed${NC}"
fi

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
if [ ! -f .env ]; then
    cat > .env << EOL
OPENWEATHER_API_KEY=""
USER_EMAIL=""
TIMEZONE="Europe/Amsterdam"
LOCATION="Amsterdam,NL"
EOL
    echo -e "${GREEN}Created .env file. Please edit it with your settings.${NC}"
else
    echo -e "${BLUE}.env file already exists${NC}"
fi

# Create logs directory
mkdir -p logs
touch logs/cron.log

# Set permissions
chmod +x src/run.py

# Create a wrapper script for the cron job
cat > run_with_env.sh << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
./src/run.py >> logs/cron.log 2>&1
EOL

chmod +x run_with_env.sh

# Create temporary cron file
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null

# Add our job if it's not already there
if ! grep -q "slackmood-ai" "$TEMP_CRON"; then
    echo "0 7 * * * $(pwd)/run_with_env.sh" >> "$TEMP_CRON"
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
echo -e "1. Google Calendar Extension (mcp_gcal@latest)"
echo -e "2. Slack Extension (mcp_slack)"
echo -e "\nPlease ensure these extensions are enabled in your Goose settings:"
echo -e "  ${BLUE}goose configure${NC}"

echo -e "\n${BLUE}Next steps:${NC}"
echo -e "1. Configure Goose extensions: ${BLUE}goose configure${NC}"
echo -e "2. Edit .env file with your settings:"
echo -e "   - Add your email"
echo -e "   - Update timezone if needed"
echo -e "   - Update location if needed"
echo -e "3. Test the setup by running: ${BLUE}goose run --text \"Run SlackMood AI\"${NC}"
