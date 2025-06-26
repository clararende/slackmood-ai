from datetime import datetime, timedelta
import pytz
import os
from typing import Dict, List

class CalendarHandler:
    def __init__(self):
        self.timezone = "Europe/Amsterdam"
        self.user_email = os.getenv("USER_EMAIL", "")

    def get_todays_events(self) -> List[Dict]:
        """Get today's calendar events using the Google Calendar API."""
        now = datetime.now(pytz.timezone(self.timezone))
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        # Format times for the API
        start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Query the calendar
        query = f"""
        SELECT 
            e.summary,
            e.start_time,
            e.end_time,
            e.status,
            e.description,
            COUNT(ea.email) as attendee_count
        FROM events e
        LEFT JOIN event_attendees ea ON e.id = ea.event_id
        WHERE e.calendar_id = '{self.user_email}'
        AND e.start_time >= '{start_str}'
        AND e.end_time <= '{end_str}'
        GROUP BY e.id, e.summary, e.start_time, e.end_time, e.status, e.description
        ORDER BY e.start_time;
        """
        
        # Execute query and process results
        # We'll implement this using the actual API
        return []

    def analyze_calendar(self) -> Dict:
        """Analyze calendar events and return a summary."""
        events = self.get_todays_events()
        
        # Initialize analysis
        analysis = {
            "total_events": len(events),
            "meeting_time": 0,  # total minutes in meetings
            "meeting_density": "light",  # light, moderate, heavy
            "focus_time": False,
            "ooo": False,
            "traveling": False,
            "location_changes": [],
            "special_events": []
        }
        
        # Analyze events
        for event in events:
            # Calculate event duration
            start = event.get("start_time")
            end = event.get("end_time")
            if start and end:
                duration = (end - start).total_seconds() / 60  # duration in minutes
                analysis["meeting_time"] += duration
            
            # Check for special events
            summary = event.get("summary", "").lower()
            description = event.get("description", "").lower()
            
            # Check for OOO
            if "ooo" in summary or "out of office" in summary:
                analysis["ooo"] = True
                analysis["special_events"].append("OOO")
            
            # Check for focus time
            if "focus" in summary or "do not disturb" in summary:
                analysis["focus_time"] = True
                analysis["special_events"].append("Focus Time")
            
            # Check for travel
            if any(word in summary for word in ["travel", "flight", "train"]):
                analysis["traveling"] = True
                analysis["special_events"].append("Traveling")
        
        # Determine meeting density
        daily_minutes = 8 * 60  # 8 working hours in minutes
        meeting_percentage = (analysis["meeting_time"] / daily_minutes) * 100
        
        if meeting_percentage > 75:
            analysis["meeting_density"] = "heavy"
        elif meeting_percentage > 40:
            analysis["meeting_density"] = "moderate"
        else:
            analysis["meeting_density"] = "light"
        
        return analysis
