import requests
from voice import say_and_speak


def extract_city_smart(cmd):
    ignore = [
        # English
        "what",
        "is",
        "the",
        "temperature",
        "weather",
        "in",
        "today",
        "now",
        "current",
        "tell",
        "me",
        # Hindi
        "ka",
        "ki",
        "ke",
        "kya",
        "hai",
        "aaj",
        "batao",
        "mausam",
        "vedar",
        "veder",
        "abhi",
        "bata",
    ]

    words = cmd.split()
    city = [w for w in words if w not in ignore]

    return " ".join(city).title() if city else "Delhi"


def get_weather(city="Delhi"):
    try:
        url = f"https://wttr.in/{city}?format=%t+%C"
        data = requests.get(url).text.strip()

        temp, *cond = data.split(" ")
        condition = " ".join(cond)

        say_and_speak(f"{city} ka temperature hai {temp}, condition {condition}")
    except:
        say_and_speak("Weather abhi available nahi hai")
