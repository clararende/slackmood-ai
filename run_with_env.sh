#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
./src/run.py >> logs/cron.log 2>&1
