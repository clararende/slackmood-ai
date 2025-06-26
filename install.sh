#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}SlackMood AI Installation Script${NC}"
echo -e "${BLUE}==============================${NC}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Python version $PYTHON_VERSION is too old. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3.8+ is installed${NC}"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << EOF
USER_EMAIL=""
TIMEZONE="Europe/Amsterdam"
LOCATION="Amsterdam,NL"
EOF
    echo -e "${YELLOW}⚠️  Please edit .env file and set your USER_EMAIL${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create logs directory
mkdir -p logs

# Create run_with_env.sh script
echo -e "${BLUE}Creating run script...${NC}"
cat > run_with_env.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
source .env
export PATH="$HOME/.local/bin:$PATH"
python3 src/run.py
EOF

chmod +x run_with_env.sh

# Set up cron job
echo -e "${BLUE}Setting up automatic updates...${NC}"
CRON_JOB="0 7 * * * $(pwd)/run_with_env.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_with_env.sh"; then
    echo -e "${GREEN}✓ Cron job already exists${NC}"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo -e "${GREEN}✓ Cron job added (runs daily at 7 AM)${NC}"
fi

echo ""
echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Edit .env file and set your USER_EMAIL"
echo -e "2. Install Goose CLI: ${BLUE}curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
echo -e "3. Configure Goose extensions: ${BLUE}goose configure${NC}"
echo -e "4. Enable 'googlecalendar' and 'slack' extensions"
echo -e "5. Test the setup by running: ${BLUE}goose run --text \"Run SlackMood AI\"${NC}"
echo ""
echo -e "${GREEN}Happy status updating! 🎉${NC}"
