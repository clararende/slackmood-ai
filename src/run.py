#!/usr/bin/env python3

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def query_calendar_database(query: str, time_min: str, time_max: str):
    """Helper function to query the calendar database."""
    from googlecalendar__query_calendar_database import query_calendar_database
    return query_calendar_database(query=query, time_min=time_min, time_max=time_max)

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
        result = query_calendar_database(query, start, end)
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
        
        if start_time and end_time:
            # Calculate duration in minutes
            duration = int((end_time - start_time).total_seconds() / 60)
            total_meeting_minutes += duration
        
        # Check for special events
        if "ooo" in summary or "out of office" in summary:
            analysis["ooo"] = True
        elif "focus" in summary:
            analysis["focus_time"] = True
        elif any(word in summary for word in ["travel", "flight", "train"]):
            analysis["traveling"] = True

    # Calculate meeting density
    working_minutes = 8 * 60  # 8-hour workday
    meeting_percentage = (total_meeting_minutes / working_minutes) * 100
    
    if meeting_percentage > 75:
        analysis["meeting_density"] = "heavy"
    elif meeting_percentage > 40:
        analysis["meeting_density"] = "moderate"
    
    return analysis

def generate_status(calendar_analysis: Dict) -> Dict:
    """Generate status based on calendar analysis."""
    
    # Handle OOO
    if calendar_analysis.get("ooo"):
        return {
            "text": "OOO today",
            "emoji": "palm_tree",
            "expiration": None
        }
    
    # Handle traveling
    if calendar_analysis.get("traveling"):
        return {
            "text": "Traveling",
            "emoji": "airplane",
            "expiration": None
        }
    
    # Handle focus time
    if calendar_analysis.get("focus_time"):
        return {
            "text": "Focus time",
            "emoji": "headphones",
            "expiration": None
        }
    
    # Handle meeting density
    if calendar_analysis["meeting_density"] == "heavy":
        return {
            "text": "In meetings today",
            "emoji": "calendar",
            "expiration": None
        }
    elif calendar_analysis["meeting_density"] == "moderate":
        return {
            "text": "Meetings & work",
            "emoji": "computer",
            "expiration": None
        }
    
    # Default status
    return {
        "text": "Working",
        "emoji": "computer",
        "expiration": None
    }

def main():
    # Load environment variables
    USER_EMAIL = os.getenv("USER_EMAIL")
    if not USER_EMAIL:
        logger.error("USER_EMAIL environment variable not set")
        return
    
    logger.info("Starting status update process...")
    
    try:
        # Get calendar events
        logger.info("Getting calendar events...")
        events = get_todays_events(USER_EMAIL)
        logger.info(f"Found {len(events)} events for today")
        
        # Analyze calendar
        logger.info("Analyzing calendar...")
        calendar_analysis = analyze_calendar(events)
        logger.info(f"Calendar analysis: {calendar_analysis}")
        
        # Generate status
        logger.info("Generating status...")
        status = generate_status(calendar_analysis)
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
