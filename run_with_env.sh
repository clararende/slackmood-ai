#!/bin/bash
cd "/Users/clararende/slack-calendar-status"
source venv/bin/activate
/Users/clararende/slack-calendar-status/venv/bin/python /Users/clararende/slack-calendar-status/src/run.py >> logs/cron.log 2>&1
