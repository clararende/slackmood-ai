from typing import Dict

def generate_status(calendar_analysis: Dict) -> Dict:
    """Generate fun and engaging status messages based on calendar analysis."""
    
    # Fun emoji combinations
    meeting_emojis = ["🗣️", "💭", "👥", "🎯", "🎪", "🎭", "🎪", "🎨", "🚀", "✨"]
    focus_emojis = ["🧘‍♀️", "🧠", "💫", "✨", "🎧", "🪷", "🔮", "🌟", "💎", "🎯"]
    travel_emojis = ["✈️", "🚅", "🌍", "🧳", "🗺️", "🎒", "🌎", "🚁", "⛵", "🏔️"]
    ooo_emojis = ["🏖️", "🌴", "🏃‍♀️", "🎉", "🌺", "🌸", "🍹", "🌅", "🎊", "🌈"]
    design_emojis = ["🎨", "✨", "🚀", "💡", "🌟", "🎭", "🪄", "💫", "🎪", "🔮"]
    coding_emojis = ["💻", "⚡", "🚀", "🔧", "🎯", "💡", "⚙️", "🎪", "✨", "🌟"]
    
    import random

    # Handle OOO
    if calendar_analysis.get("ooo"):
        emoji = random.choice(ooo_emojis)
        messages = [
            f"Out exploring the world {emoji}",
            f"Taking a breather {emoji}",
            f"Recharging my batteries {emoji}",
            f"Living my best life {emoji}",
            f"On a grand adventure {emoji}",
            f"Collecting sunshine {emoji}",
            f"Embracing the good vibes {emoji}",
            f"Making memories {emoji}",
            f"Living the dream {emoji}",
            f"On a wellness journey {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),  # Remove variation selector
            "expiration": None
        }
    
    # Handle traveling
    if calendar_analysis.get("traveling"):
        emoji = random.choice(travel_emojis)
        messages = [
            f"Up in the clouds {emoji}",
            f"On the move {emoji}",
            f"Adventure mode: ON {emoji}",
            f"Somewhere between here and there {emoji}",
            f"Embracing the journey {emoji}",
            f"Exploring new horizons {emoji}",
            f"Jet-setting around {emoji}",
            f"On a mission to somewhere {emoji}",
            f"Collecting passport stamps {emoji}",
            f"Living the nomadic life {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),
            "expiration": None
        }
    
    # Handle focus time
    if calendar_analysis.get("focus_time"):
        emoji = random.choice(focus_emojis)
        messages = [
            f"Deep work mode {emoji}",
            f"In the zone {emoji}",
            f"Brain.exe is running {emoji}",
            f"Channeling my inner genius {emoji}",
            f"Focus level: MAXIMUM {emoji}",
            f"Unleashing creativity {emoji}",
            f"Deep dive in progress {emoji}",
            f"Concentration station {emoji}",
            f"Flow state activated {emoji}",
            f"Mind palace exploration {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),
            "expiration": None
        }
    
    # Handle design/creative activities
    if calendar_analysis.get("current_activity") == "design":
        emoji = random.choice(design_emojis)
        messages = [
            f"Designing the future {emoji}",
            f"Creating magic {emoji}",
            f"Sketching dreams {emoji}",
            f"Building beautiful things {emoji}",
            f"Making pixels dance {emoji}",
            f"Design wizard at work {emoji}",
            f"Creating user joy {emoji}",
            f"Sketching possibilities {emoji}",
            f"Design thinking in action {emoji}",
            f"Making interfaces sing {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),
            "expiration": None
        }
    
    # Handle coding/development activities
    if calendar_analysis.get("current_activity") == "coding":
        emoji = random.choice(coding_emojis)
        messages = [
            f"Crafting digital wonders {emoji}",
            f"Making bits and bytes behave {emoji}",
            f"Code whisperer at work {emoji}",
            f"Dancing with algorithms {emoji}",
            f"Turning coffee into code {emoji}",
            f"Debugging the matrix {emoji}",
            f"Building the future {emoji}",
            f"Code poetry in progress {emoji}",
            f"Stack overflow survivor {emoji}",
            f"Git commit wizard {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),
            "expiration": None
        }
    
    # Handle meeting density
    if calendar_analysis["meeting_density"] == "heavy":
        emoji = random.choice(meeting_emojis)
        messages = [
            f"Meeting marathon in progress {emoji}",
            f"Back-to-back adventures {emoji}",
            f"Professional social butterfly {emoji}",
            f"Meeting all the humans {emoji}",
            f"Talk-show host mode {emoji}",
            f"Conference room warrior {emoji}",
            f"Meeting maestro {emoji}",
            f"Calendar conqueror {emoji}",
            f"Sync session superstar {emoji}",
            f"Meeting marathon runner {emoji}"
        ]
        return {
            "text": random.choice(messages),
            "emoji": emoji.strip("️"),
            "expiration": None
        }
    elif calendar_analysis["meeting_density"] == "moderate":
        emoji = "💫"
        messages = [
            "Balancing chats and code 💫",
            "Half social, half focused 💫",
            "Mixing meetings with magic 💫",
            "Juggling tasks like a pro 💫",
            "Multitasking master 💫",
            "Switching between worlds 💫",
            "Meeting and creating 💫",
            "Social coding time 💫",
            "Collaboration station 💫",
            "Team player mode 💫"
        ]
        return {
            "text": random.choice(messages),
            "emoji": "sparkles",
            "expiration": None
        }
    
    # Default status - working
    messages = [
        "Crafting digital wonders 💻",
        "Making bits and bytes behave 💻",
        "Code whisperer at work 💻",
        "Dancing with algorithms 💻",
        "Turning coffee into code 💻",
        "Building something awesome 💻",
        "Creating digital magic 💻",
        "Problem-solving ninja 💻",
        "Innovation in progress 💻",
        "Making the world better 💻"
    ]
    return {
        "text": random.choice(messages),
        "emoji": "computer",
        "expiration": None
    }
