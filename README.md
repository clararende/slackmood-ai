# SlackMood AI

Automatically update your Slack status with fun, context-aware messages based on your Google Calendar events.

## Prerequisites

- Python 3.8 or higher
- Goose CLI or Goose Desktop installed and configured
- `uvx` package manager (required for MCP servers)
- Access to Google Calendar
- Access to Slack

## Required Goose Extensions

This project requires the following Goose extensions to be enabled:

1. **Google Calendar Extension** (`mcp_gcal@latest`)
   - Provides calendar integration
   - Handles calendar queries and event analysis
   - Manages timezone conversions

2. **Slack Extension** (`mcp_slack`)
   - Manages Slack status updates
   - Handles emoji and status text
   - Provides workspace integration

## Installation

### 1. Install uvx (Required for MCP servers)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### 2. Configure Goose Extensions

#### For Goose CLI:
```bash
goose configure
```

#### For Goose Desktop:
1. Open Goose Desktop
2. Go to Settings → Extensions
3. Enable "googlecalendar" and "slack" extensions
4. Save the configuration

In the configuration interface:
- Navigate to "Toggle Extensions"
- Enable "googlecalendar" and "slack" extensions
- Save the configuration

### 3. Clone and Setup Project

```bash
git clone https://github.com/clararende/slackmood-ai.git
cd slackmood-ai
```

### 4. Run Installation Script

```bash
chmod +x install.sh
./install.sh
```

The installation script will:
- Create a Python virtual environment
- Install required dependencies
- Set up configuration files
- Configure automatic updates via cron
- Create necessary directories for logs

## Configuration

### Environment Variables
The following variables are configured in `.env`:

```ini
USER_EMAIL="your-email@example.com"  # REQUIRED: Must be set for the script to work
TIMEZONE="Your/Timezone"
LOCATION="City,Country"
```

**Important:**
- Before running the project, you must edit the `.env` file and set a valid `USER_EMAIL` (your email address for calendar access). The script will not work until this is set.

## Usage

### Running with Goose CLI (Recommended)

The project is designed to work with Goose CLI and its extensions. To run:

```bash
export PATH="$HOME/.local/bin:$PATH"
goose run --text "Run SlackMood AI: Get calendar context, query events, analyze schedule, and update Slack status"
```

Or create an instruction file:

```bash
echo "Run SlackMood AI project with calendar analysis and Slack status update" > instructions.txt
goose run -i instructions.txt
```

### Running with Goose Desktop

1. Open Goose Desktop
2. In the chat interface, type:
   ```
   Run SlackMood AI: Get calendar context, query events, analyze schedule, and update Slack status
   ```
3. Goose Desktop will use the same extensions to update your Slack status

### Manual Execution

You can also run the Python script directly:

```bash
export PATH="$HOME/.local/bin:$PATH"
USER_EMAIL="your-email@example.com" TIMEZONE="Europe/Amsterdam" LOCATION="Amsterdam,NL" python3 src/run.py
```

### Automatic Updates
The script runs automatically every morning at 7 AM to set your status for the day.

### Logs
Check the logs at any time:
```bash
tail -f logs/cron.log
```

## Project Structure

```
slackmood-ai/
├── src/
│   ├── run.py              # Main script
│   ├── slack_handler.py    # Slack API integration (placeholder for direct API calls)
│   └── status_generator.py # Status message generation
├── config/
│   └── config.yml         # Configuration
├── logs/
│   └── cron.log          # Execution logs
├── venv/                 # Python virtual environment
├── install.sh           # Installation script
├── run_with_env.sh     # Wrapper script for execution
└── README.md          # This documentation
```

## Troubleshooting

### Common Issues

1. **Extensions Not Working**
   - Ensure `uvx` is installed: `which uvx`
   - Check extension configuration: `goose configure` (CLI) or Settings → Extensions (Desktop)
   - Verify PATH includes `$HOME/.local/bin`

2. **Status Not Updating**
   - Check if required extensions are enabled
   - Check logs: `tail -f logs/cron.log`
   - Verify cron job: `crontab -l`
   - For Desktop: Ensure you're logged into the correct Slack workspace

3. **Wrong Status**
   - Verify Goose extensions are working
   - Check your calendar events
   - Verify timezone settings

4. **Script Errors**
   - Ensure all dependencies are installed
   - Check Goose extension status
   - Verify network connectivity

### Getting Help

1. Check the logs in `logs/cron.log`
2. Verify Goose extensions are enabled and working
3. Review your calendar events
4. Check Slack permissions

## Customization

### Modifying Status Messages

Edit the status patterns in `src/status_generator.py`:

```python
def generate_status(calendar_analysis: Dict) -> Dict:
    # Customize status messages and emojis here
    ...
```

### Changing Update Schedule

Edit your cron schedule:
```bash
crontab -e
```

Current schedule (7 AM daily):
```
0 7 * * * /path/to/slackmood-ai/run_with_env.sh
```

## Future Enhancements

### 1. Smart Context Integration
- **Weather Integration**: Add local weather conditions to status messages (e.g., "☔ Brainstorming while it rains" or "☀️ Coding in the sunshine")
- **Time-of-day Awareness**: Different message styles for morning/afternoon/evening
- **Location-based Messages**: Customize messages based on whether you're working from home, office, or a different location

### 2. Enhanced Calendar Intelligence
- **Meeting Preparation Mode**: Set special statuses 5-10 minutes before meetings (e.g., "🎯 Preparing for the design review")
- **Post-meeting Recovery**: Add brief "decompress" statuses after long meetings
- **Smart Duration**: Vary messages based on meeting length (quick sync vs. long workshop)
- **Participant-aware Messages**: Customize based on who you're meeting with (e.g., "1:1 with team" vs. "Client presentation")

### 3. Productivity Integration
- **Pomodoro Mode**: Integrate with popular productivity techniques
- **Focus Time Defender**: Special statuses during focus blocks that indicate urgency level for interruptions
- **Task Integration**: Connect with todo apps (like Todoist or Asana) to show current focus area

### 4. Team Coordination Features
- **Lunch Buddy System**: Special statuses for lunch time that can help coordinate team lunches
- **Team Sync**: Allow team members to opt-in to shared status themes
- **Meeting Availability**: Show when you're approaching your maximum meeting load for the day

### 5. Wellness & Work-Life Balance
- **Break Reminders**: Incorporate regular break reminders into status messages
- **Working Hours Respect**: Smart end-of-day status changes
- **Wellness Mode**: Integration with health apps to show when you're taking a walking meeting or exercise break

### 6. AI Enhancements
- **Sentiment Analysis**: Analyze meeting titles/descriptions to set more contextual moods
- **Pattern Learning**: Learn from your calendar patterns to predict and set more accurate statuses
- **Custom Personality**: Allow users to define their status message "personality" (professional, playful, minimal, etc.)

## Security

- API keys are stored locally in `.env`
- Credentials are never logged or transmitted
- All API calls use HTTPS
- Logs don't contain sensitive information

## Contributing

Feel free to:
- Submit issues
- Propose new features
- Add more fun status messages
- Send pull requests

## License

MIT License - feel free to modify and use as needed.
