import requests
from config import CITY, WEATHER_ICONS

def get_weather():
    try:
        data = requests.get(f"https://wttr.in/{CITY}?format=j1&lang=ru", timeout=5).json()
        t = data["current_condition"][0]["temp_C"]
        f = data["current_condition"][0]["FeelsLikeC"]
        desc = data["current_condition"][0]["lang_ru"][0]["value"].lower()
        icon = next((e for k,e in WEATHER_ICONS.items() if k.lower() in desc), "❓")
        return f"{icon} {desc.capitalize()} {t}°C (ощущ. {f}°C)"
    except:
        return None
