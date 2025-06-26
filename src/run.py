#!/usr/bin/env python3

import os
import logging
from datetime import datetime, timedelta
import json
import random
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_weather(location: str, api_key: str) -> Dict:
    """Get weather data from OpenWeather API."""
    import urllib.request
    import urllib.parse
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return {}

def get_todays_events(user_email: str) -> List[Dict]:
    """Get today's calendar events."""
    now = datetime.utcnow()
    start = now.strftime("%Y-%m-%dT00:00:00Z")
    end = (now + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    
    query = f"""
    SELECT 
        e.summary,
        e.start_time,
        e.end_time,
        e.status,
        COUNT(ea.email) as attendee_count
    FROM events e
    LEFT JOIN event_attendees ea ON e.id = ea.event_id
    WHERE e.calendar_id = '{user_email}'
    AND e.start_time >= '{start}'
    AND e.start_time < '{end}'
    GROUP BY e.id, e.summary, e.start_time, e.end_time, e.status
    ORDER BY e.start_time;
    """
    
    try:
        from googlecalendar__query_calendar_database import query_calendar_database
        result = query_calendar_database(query=query, time_min=start, time_max=end)
        return result
    except Exception as e:
        logger.error(f"Error querying calendar: {e}")
        return []

def analyze_calendar(events: List[Dict]) -> Dict:
    """Analyze calendar events and return a summary."""
    analysis = {
        "total_events": len(events),
        "meeting_time": 0,
        "meeting_density": "light",
        "focus_time": False,
        "ooo": False,
        "traveling": False
    }
    
    total_meeting_minutes = 0
    
    for event in events:
        summary = str(event.get("summary", "")).lower()
        start_time = event.get("start_time")
        end_time = event.get("end_time")
        
        # Check for special events
        if "ooo" in summary or "out of office" in summary:
            analysis["ooo"] = True
        elif "focus" in summary:
            analysis["focus_time"] = True
        elif any(word in summary for word in ["travel", "flight", "train"]):
            analysis["traveling"] = True
        
        # Count meeting time (assume 30 min if duration can't be calculated)
        if start_time and end_time:
            try:
                duration = (end_time - start_time).total_seconds() / 60
                total_meeting_minutes += duration
            except:
                total_meeting_minutes += 30

    # Calculate meeting density
    working_minutes = 8 * 60  # 8-hour workday
    meeting_percentage = (total_meeting_minutes / working_minutes) * 100
    
    if meeting_percentage > 75:
        analysis["meeting_density"] = "heavy"
    elif meeting_percentage > 40:
        analysis["meeting_density"] = "moderate"
    
    return analysis

def generate_status(calendar_analysis: Dict, weather_data: Dict) -> Dict:
    """Generate fun and engaging status messages."""
    from status_generator import generate_fun_status
    return generate_fun_status(calendar_analysis, weather_data)

def main():
    # Configuration
    OPENWEATHER_API_KEY = "e87ed82ab8132f15877ae385179114bf"
    USER_EMAIL = "clararende@squareup.com"
    LOCATION = "Amsterdam,NL"
    
    logger.info("Starting status update process...")
    
    try:
        # Initialize Google Calendar context
        from googlecalendar__get_user_and_calendar_context import get_user_and_calendar_context
        get_user_and_calendar_context()
        
        # Get calendar events
        logger.info("Getting calendar events...")
        events = get_todays_events(USER_EMAIL)
        logger.info(f"Found {len(events)} events for today")
        
        # Analyze calendar
        logger.info("Analyzing calendar...")
        calendar_analysis = analyze_calendar(events)
        logger.info(f"Calendar analysis: {calendar_analysis}")
        
        # Get weather
        logger.info("Fetching weather...")
        weather_data = get_weather(LOCATION, OPENWEATHER_API_KEY)
        logger.info(f"Weather data: {weather_data}")
        
        # Generate status
        logger.info("Generating status...")
        status = generate_status(calendar_analysis, weather_data)
        logger.info(f"Generated status: {status}")
        
        # Update Slack status
        from slack__manage_user_status import manage_user_status
        logger.info("Updating Slack status...")
        result = manage_user_status(
            action="set",
            status_text=status["text"],
            status_emoji=status["emoji"],
            duration_minutes=720  # 12 hours
        )
        
        if result.get("ok"):
            logger.info("Successfully updated Slack status!")
        else:
            logger.error(f"Failed to update Slack status: {result}")
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise e

if __name__ == "__main__":
    main()
