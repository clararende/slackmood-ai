def generate_status(calendar_analysis: Dict) -> Dict:
    """Generate fun and engaging status messages based on calendar analysis."""
    
    # Fun emoji combinations
    meeting_emojis = ["🗣️", "💭", "👥", "🎯", "🎪", "🎭", "🎪"]
    focus_emojis = ["🧘‍♀️", "🧠", "💫", "✨", "🎧", "🪷"]
    travel_emojis = ["✈️", "🚅", "🌍", "🧳", "🗺️"]
    ooo_emojis = ["🏖️", "🌴", "🏃‍♀️", "🎉", "🌺", "🌸"]
    
    import random

    # Handle OOO
    if calendar_analysis.get("ooo"):
        emoji = random.choice(ooo_emojis)
        messages = [
            f"Out exploring the world {emoji}",
            f"Taking a breather {emoji}",
            f"Recharging my batteries {emoji}",
            f"Living my best life {emoji}",
            f"On a grand adventure {emoji}"
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
            f"Embracing the journey {emoji}"
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
            f"Focus level: MAXIMUM {emoji}"
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
            f"Talk-show host mode {emoji}"
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
            "Multitasking master 💫"
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
        "Turning coffee into code 💻"
    ]
    return {
        "text": random.choice(messages),
        "emoji": "computer",
        "expiration": None
    }
