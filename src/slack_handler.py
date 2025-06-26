from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SlackStatusManager:
    def __init__(self):
        self.last_status = None

    def update_status(self, status_text: str, emoji: str, expiration: Optional[int] = None) -> bool:
        """Update Slack status using the Slack API."""
        try:
            # Prepare the status
            status_emoji = emoji if emoji.startswith(':') else f":{emoji}:"
            
            # Call Slack API to update status
            response = self._update_slack_status(status_text, status_emoji, expiration)
            
            if response.get("ok", False):
                self.last_status = {
                    "text": status_text,
                    "emoji": emoji,
                    "expiration": expiration
                }
                logger.info(f"Successfully updated Slack status to: {status_text} {emoji}")
                return True
            else:
                logger.error(f"Failed to update Slack status: {response.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating Slack status: {e}")
            return False

    def _update_slack_status(self, text: str, emoji: str, expiration: Optional[int] = None) -> dict:
        """Internal method to make the actual Slack API call."""
        try:
            # Create the profile update
            profile = {
                "status_text": text,
                "status_emoji": emoji
            }
            
            if expiration:
                profile["status_expiration"] = expiration
            
            # Make the API call using the Slack tools
            return {"ok": True}  # Placeholder for actual API response
            
        except Exception as e:
            logger.error(f"Error in Slack API call: {e}")
            return {"ok": False, "error": str(e)}
