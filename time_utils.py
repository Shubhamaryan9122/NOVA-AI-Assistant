# =========================================================
# 🔥 TIME SYSTEM (ACCURATE FIXED)
# =========================================================

from datetime import datetime
import pytz
from voice import say_and_speak


def get_country_time(place):
    try:
        place = place.lower().strip()

        timezone_map = {
    # Asia
            "india": "Asia/Kolkata",
            "pakistan": "Asia/Karachi",
            "bangladesh": "Asia/Dhaka",
            "nepal": "Asia/Kathmandu",
            "philippines": "Asia/Manila",
            "japan": "Asia/Tokyo",
            "uae": "Asia/Dubai",
            "dubai": "Asia/Dubai",
            "china": "Asia/Shanghai",
            "singapore": "Asia/Singapore",
            "thailand": "Asia/Bangkok",
            "indonesia": "Asia/Jakarta",
            "korea": "Asia/Seoul",
            "israel": "Asia/Jerusalem",

    # Europe
            "france": "Europe/Paris",
            "paris": "Europe/Paris",
            "uk": "Europe/London",
            "england": "Europe/London",
            "london": "Europe/London",
            "germany": "Europe/Berlin",
            "berlin": "Europe/Berlin",
            "italy": "Europe/Rome",
            "spain": "Europe/Madrid",
            "russia": "Europe/Moscow",
            "moscow": "Europe/Moscow",
            "turkey": "Europe/Istanbul",

    # Americas
            "usa": "America/New_York",
            "new york": "America/New_York",
            "canada": "America/Toronto",
            "toronto": "America/Toronto",
            "brazil": "America/Sao_Paulo",   # ← YEH ADD KARO
            "sao paulo": "America/Sao_Paulo",
            "mexico": "America/Mexico_City",
            "argentina": "America/Argentina/Buenos_Aires",
            "los angeles": "America/Los_Angeles",
            "chicago": "America/Chicago",

    # Africa / Oceania
            "australia": "Australia/Sydney",
            "sydney": "Australia/Sydney",
            "new zealand": "Pacific/Auckland",
            "egypt": "Africa/Cairo",
            "nigeria": "Africa/Lagos",
            "south africa": "Africa/Johannesburg",
        }

        if place in timezone_map:
            tz = pytz.timezone(timezone_map[place])
        else:
            try:
                tz = pytz.timezone(place.title())
            except:
                return "Location not found"

        time_now = datetime.now(tz).strftime("%I:%M %p")

        return f"The current time in {place.title()} is {time_now}"

    except:
        return "Unable to fetch time"