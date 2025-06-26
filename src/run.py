#!/usr/bin/env python3

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Private meeting keywords that should trigger generic status
PRIVATE_KEYWORDS = [
    "therapy", "counseling", "personal", "private", "1:1", "one-on-one",
    "doctor", "medical", "health", "mental", "wellness", "coaching",
    "confidential", "sensitive", "hr", "human resources", "legal",
    "performance", "review", "salary", "compensation", "interview"
]

def is_private_meeting(summary: str) -> bool:
    """Check if a meeting should be treated as private."""
    summary_lower = summary.lower()
    return any(keyword in summary_lower for keyword in PRIVATE_KEYWORDS)

def get_todays_events(user_email: str) -> List[Dict]:
    """Get today's calendar events using Goose Google Calendar extension."""
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    
    # Format times for the API (RFC 3339 format)
    start_str = start.strftime("%Y-%m-%dT%H:%M:%S%z")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%S%z")
    
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
    AND e.start_time >= '{start_str}'
    AND e.start_time < '{end_str}'
    GROUP BY e.id, e.summary, e.start_time, e.end_time, e.status
    ORDER BY e.start_time;
    """
    
    try:
        # This will be called via Goose CLI, not as a direct import
        logger.info(f"Querying calendar with: {query}")
        # For now, return empty list - the actual query will be handled by Goose
        return []
    except Exception as e:
        logger.error(f"Error querying calendar: {e}")
        return []

def analyze_calendar(events: List[Dict]) -> Dict:
    """Analyze calendar events and return a summary with privacy protection."""
    analysis = {
        "total_events": len(events),
        "meeting_time": 0,
        "meeting_density": "light",
        "focus_time": False,
        "ooo": False,
        "traveling": False,
        "has_private_meetings": False,
        "current_activity": "working"
    }
    
    total_meeting_minutes = 0
    now = datetime.now()
    
    for event in events:
        summary = str(event.get("summary", ""))
        start_time = event.get("start_time")
        end_time = event.get("end_time")
        
        # Check if this is a private meeting
        if is_private_meeting(summary):
            analysis["has_private_meetings"] = True
            # Don't log private meeting details
            logger.info("Found private meeting - will use generic status")
            continue
        
        if start_time and end_time:
            # Calculate duration in minutes
            duration = int((end_time - start_time).total_seconds() / 60)
            total_meeting_minutes += duration
            
            # Check if this is the current activity
            if start_time <= now <= end_time:
                summary_lower = summary.lower()
                if "focus" in summary_lower or "deep work" in summary_lower:
                    analysis["current_activity"] = "focus"
                elif "design" in summary_lower or "creative" in summary_lower:
                    analysis["current_activity"] = "design"
                elif "code" in summary_lower or "development" in summary_lower:
                    analysis["current_activity"] = "coding"
                elif "meeting" in summary_lower or "sync" in summary_lower:
                    analysis["current_activity"] = "meeting"
        
        # Check for special events (only for non-private meetings)
        summary_lower = summary.lower()
        if "ooo" in summary_lower or "out of office" in summary_lower:
            analysis["ooo"] = True
        elif "focus" in summary_lower:
            analysis["focus_time"] = True
        elif any(word in summary_lower for word in ["travel", "flight", "train"]):
            analysis["traveling"] = True

    # Calculate meeting density
    working_minutes = 8 * 60  # 8-hour workday
    meeting_percentage = (total_meeting_minutes / working_minutes) * 100
    
    if meeting_percentage > 75:
        analysis["meeting_density"] = "heavy"
    elif meeting_percentage > 40:
        analysis["meeting_density"] = "moderate"
    
    return analysis

def generate_fun_status(calendar_analysis: Dict) -> Dict:
    """Generate fun and witty status messages based on calendar analysis."""
    
    # Import the fun status generator
    from status_generator import generate_status as fun_generate_status
    
    # If there are private meetings, use generic but fun status
    if calendar_analysis.get("has_private_meetings"):
        fun_messages = [
            "In my happy place 🌟",
            "Doing important things ✨",
            "Making magic happen 🪄",
            "On a mission 🚀",
            "Creating something amazing 💫"
        ]
        fun_emojis = ["🌟", "✨", "🪄", "🚀", "💫", "🎯", "🎪"]
        
        return {
            "text": random.choice(fun_messages),
            "emoji": random.choice(fun_emojis).strip("️"),
            "expiration": None
        }
    
    # Use the fun status generator for non-private activities
    return fun_generate_status(calendar_analysis)

def main():
    # Load environment variables
    USER_EMAIL = os.getenv("USER_EMAIL")
    if not USER_EMAIL:
        logger.error("USER_EMAIL environment variable not set")
        return
    
    logger.info("Starting SlackMood AI status update process...")
    
    try:
        # Get calendar events
        logger.info("Getting calendar events...")
        events = get_todays_events(USER_EMAIL)
        logger.info(f"Found {len(events)} events for today")
        
        # Analyze calendar
        logger.info("Analyzing calendar with privacy protection...")
        calendar_analysis = analyze_calendar(events)
        logger.info(f"Calendar analysis: {calendar_analysis}")
        
        # Generate fun status
        logger.info("Generating fun and witty status...")
        status = generate_fun_status(calendar_analysis)
        logger.info(f"Generated fun status: {status}")
        
        # Update Slack status - this will be handled by Goose CLI
        logger.info("Updating Slack status with personality...")
        logger.info(f"Status to set: {status['text']} with emoji {status['emoji']}")
        
        # For now, just log the status - the actual update will be done via Goose
        logger.info("Fun status update completed successfully!")
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise e

if __name__ == "__main__":
    main()
