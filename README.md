# Slack Calendar Status

Automatically update your Slack status with fun, context-aware messages based on your Google Calendar events and local weather conditions.

## Required Goose Extensions

This project requires the following Goose extensions to be enabled:

1. **Google Calendar Extension**
   - Provides calendar integration
   - Handles calendar queries and event analysis
   - Manages timezone conversions

2. **Slack Extension**
   - Manages Slack status updates
   - Handles emoji and status text
   - Provides workspace integration

To enable these extensions:
1. Open Goose Desktop
2. Go to Settings (top right menu)
3. Navigate to the Extensions section
4. Enable both Google Calendar and Slack extensions

## Features

- 🎭 **Fun Status Messages**: Dynamic, context-aware status updates with personality
- 🔄 **Automatic Updates**: Updates your Slack status every morning at 7 AM
- 📅 **Smart Calendar Analysis**: Detects meeting patterns, focus time, and special events
- 🎯 **Custom Emoji**: Contextual emoji selection based on your activities
- 📊 **Intelligent Analysis**: Adapts status based on your schedule
- 🔔 **Detailed Logging**: Keeps track of all updates

## Status Message Examples

| Situation | Example Status |
|-----------|---------------|
| Heavy Meetings | "Meeting marathon in progress 🎪" |
| Focus Time | "In the zone 🧘‍♀️" |
| Regular Work | "Turning coffee into code 💻" |
| Travel | "Up in the clouds ✈️" |
| OOO | "Living my best life 🌺" |

## Prerequisites

- Python 3.8 or higher
- Goose Desktop with required extensions enabled
- Access to Google Calendar
- Access to Slack
- OpenWeather API key (already configured)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd slack-calendar-status
   ```

2. Run the installation script:
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
OPENWEATHER_API_KEY="your-api-key"
USER_EMAIL="your-email@squareup.com"
TIMEZONE="Your/Timezone"
LOCATION="City,Country"
```

## Usage

### Automatic Updates
The script runs automatically every morning at 7 AM to set your status for the day.

### Manual Updates
You can manually update your status at any time:

```bash
./run_with_env.sh
```

### Logs
Check the logs at any time:
```bash
tail -f logs/cron.log
```

## Project Structure

```
slack-calendar-status/
├── src/
│   ├── run.py              # Main script
│   └── status_generator.py # Status message generation
├── config/
│   └── .env               # Configuration
├── logs/
│   └── cron.log          # Execution logs
├── venv/                 # Python virtual environment
├── install.sh           # Installation script
├── run_with_env.sh     # Wrapper script for execution
└── README.md          # This documentation
```

## Troubleshooting

### Common Issues

1. **Status Not Updating**
   - Check if required extensions are enabled
   - Check logs: `tail -f logs/cron.log`
   - Verify cron job: `crontab -l`

2. **Wrong Status**
   - Verify Goose extensions are working
   - Check your calendar events
   - Verify timezone settings

3. **Script Errors**
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
0 7 * * * /path/to/slack-calendar-status/run_with_env.sh
```

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
