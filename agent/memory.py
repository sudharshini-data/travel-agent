import os
import json
from dotenv import load_dotenv

load_dotenv()

PREFERENCES_PATH = "data/preferences.json"

def save_preference(preference: str):
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(PREFERENCES_PATH):
        with open(PREFERENCES_PATH, "r") as f:
            preferences = json.load(f)
    else:
        preferences = []
    
    preferences.append(preference)
    
    with open(PREFERENCES_PATH, "w") as f:
        json.dump(preferences, f)


def get_relevant_preferences(query: str) -> str:
    if not os.path.exists(PREFERENCES_PATH):
        return ""
    
    with open(PREFERENCES_PATH, "r") as f:
        preferences = json.load(f)
    
    if not preferences:
        return ""
    
    return "\n".join(preferences)


def get_session_history(session_id: str):
    return []