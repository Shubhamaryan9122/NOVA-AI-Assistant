# =========================================================
# 🔥 IMPORTS
# =========================================================

import threading
import time
import json
import os

from voice import *
from memory import *
from browser import *
from weather import *
from time_utils import *
from ai_chat import *
from worldmonitor import *
from browser import safe_driver
from selenium.webdriver.common.by import By
from maps_analyzer import get_best_place
from navigation import (
    navigate_to,
    extract_destination,
    is_navigation_query,
    search_nearby,
)
from youtube import play_on_youtube, handle_youtube_controls
from language_processor import process_text
from product_search import product_search
from system_control import (
    open_app,
    close_app,
    volume_up,
    volume_down,
    mute_volume,
    lock_screen,
    shutdown_pc,
    restart_pc,
    confirm_power_action,
    open_folder,
)

bridge = None

NEWS_WORDS = [
    "news",
    "update",
    "breaking",
    "headlines",
    "happened",
    "today news",
    "current affairs",
]


# ==================================================
# 🔥 MEMORY SYSTEM
# ==================================================

MEMORY_FILE = "memory.json"


# =========================================================
# 🔥 HELPER
# =========================================================

COMMAND_KEYWORDS = [
    "open",
    "close",
    "play",
    "search",
    "weather",
    "volume",
    "mute",
    "lock",
    "shutdown",
    "restart",
    "time",
    "remember",
    "what",
    "tell",
    "show",
    "kholo",
    "band",
    "chalao",
    "mausam",
    "batao",
]


def clean_name(name):
    return name.replace("my name is", "").strip().title()


def is_valid_command(text):
    text = text.strip().lower()
    # ✅ Sirf tab valid maano jab command keyword se shuru ho
    return any(text.startswith(kw) for kw in COMMAND_KEYWORDS)


def handle_multi_command(cmd):
    # ✅ "and" nahi hai toh turant return
    if " and " not in cmd:
        return False

    parts = cmd.split(" and ", 1)  # sirf pehla "and" pe split

    part1 = parts[0].strip()
    part2 = parts[1].strip()

    # ✅ Dono parts valid commands hain tabhi split karo
    if is_valid_command(part1) and is_valid_command(part2):
        print(f"MULTI CMD: '{part1}' + '{part2}'")
        process(part1)
        process(part2)
        return True

    # ✅ Warna normal command maano — split mat karo
    return False


def smart_reply(text):
    if not text:
        return ""
    if len(text) > 200:
        return text[:200] + "..."
    return text


# =========================================================
# 🔥 PROCESS
# =========================================================


def process(cmd):
    cmd, lang = process_text(cmd)
    print("DEBUG CMD:", cmd)

    memory = load_memory()

    cmd_lower = cmd.lower()

    if (
        cmd_lower == "screenshot"
        or "take screenshot" in cmd_lower
        or "take a screenshot" in cmd_lower
        or "capture screen" in cmd_lower
    ):

        from browser import take_screenshot

        path = take_screenshot()

        return f"Screenshot saved as {path}"

    # 🔥 OPEN SCREENSHOT
    if "open screenshot" in cmd_lower:

        import os

        screenshot_path = os.path.join(os.getcwd(), "screenshot.png")

        if os.path.exists(screenshot_path):

            os.startfile(screenshot_path)

            return "Opening screenshot"

        return "Screenshot not found"

    # 🔥 CREATE FILE
    if cmd_lower.startswith("create file"):

        filename = cmd_lower.replace("create file", "").strip()

        create_file(filename)

        return f"{filename} created"

    # 🔥 READ FILE
    if cmd_lower.startswith("read file"):

        filename = cmd_lower.replace("read file", "").strip()

        return read_file(filename)

    if "my name is" in cmd_lower:

        name = cmd_lower.replace("my name is", "").strip()

        memory["name"] = name

        save_memory(memory)

        return f"I'll remember that. Your name is {name}"

    if "what is my name" in cmd_lower:

        if "name" in memory:
            return f"Your name is {memory['name']}"

        return "I don't know your name yet"

    # =====================================================
    # 🔥 1. MULTI COMMAND (FIRST)
    # =====================================================
    if handle_multi_command(cmd):
        return smart_reply("Multiple commands executed")

    # ==========================================
    # BROWSER CLOSE FIX (PUT ABOVE APP CONTROL)
    # ==========================================

    if (
        "close browser" in cmd_lower
        or "browser close" in cmd_lower
        or "close chrome" in cmd_lower
    ):

        from browser import close_browser

        close_browser()

        return "Browser closed"

    if "close youtube" in cmd_lower:

        from browser import close_tab

        close_tab()

        return "YouTube closed"

    # ==========================================
    # APP CONTROL
    # ==========================================

    app_result = open_app(cmd)

    if app_result:
        return app_result

    folder_result = open_folder(cmd)

    if folder_result:
        return folder_result

    close_result = close_app(cmd)

    if close_result:
        return close_result

    if "volume up" in cmd:
        return volume_up()

    if "volume down" in cmd:
        return volume_down()

    if "mute" in cmd:
        return mute_volume()

    if "lock screen" in cmd:
        return lock_screen()

    if "shutdown pc" in cmd:
        return shutdown_pc()

    if "restart pc" in cmd:
        return restart_pc()

    confirm_result = None

    if cmd.strip() == "yes":
        confirm_result = confirm_power_action(cmd)

    if confirm_result:
        return confirm_result

    # ==========================================
    # MAPS ANALYZER COMMAND
    # ==========================================

    if cmd_lower.startswith("search best"):

        print("SEARCH BEST HANDLER HIT")

        best = get_best_place()

        if not best:

            say_and_speak("I could not analyze Google Maps results.")

            return ""

        d = safe_driver()

        if d and best.get("index", -1) >= 0:

            try:

                articles = d.find_elements(By.CSS_SELECTOR, "div[role='article']")

                print("CLICKING INDEX:", best["index"])

                articles[best["index"]].click()

                time.sleep(2)

            except Exception as e:

                print("CLICK ERROR:", e)

        print("BEST PLACE:", best)

        if not best:

            say_and_speak("I could not analyze Google Maps results.")

            return ""

        response = (
            f"The best nearby place is "
            f"{best['name']}. "
            f"It has a rating of "
            f"{best['rating']} stars from "
            f"{best['reviews']} reviews."
        )

        say_and_speak(response)

        return ""

    # ==========================================
    # BROWSER COMMANDS
    # ==========================================
    if handle_browser_commands(cmd):
        return ""

    # ==========================================
    # PRODUCT SEARCH
    # ==========================================
    product_result = product_search(cmd)

    if product_result:
        say_and_speak(product_result)
        return ""

    # ==========================================
    # NEARBY PLACES
    # ==========================================

    if "nearby" in cmd_lower or "near me" in cmd_lower:

        places = [
            # Food
            "restaurant",
            "restaurants",
            "cafe",
            "coffee shop",
            "tea stall",
            "dhaba",
            "bakery",
            "pizza",
            "burger",
            "food court",
            # Hotels
            "hotel",
            "hotels",
            "resort",
            "hostel",
            "guest house",
            "homestay",
            "lodge",
            # Health
            "hospital",
            "hospitals",
            "clinic",
            "doctor",
            "dentist",
            "medical store",
            "pharmacy",
            "chemist",
            "blood bank",
            # Travel
            "bus station",
            "bus stop",
            "railway station",
            "metro station",
            "airport",
            "taxi stand",
            "cab",
            "car rental",
            # Fuel
            "petrol pump",
            "gas station",
            "charging station",
            "ev charging",
            # Banking
            "atm",
            "bank",
            "post office",
            # Shopping
            "mall",
            "shopping mall",
            "supermarket",
            "grocery store",
            "electronics store",
            "mobile shop",
            "clothing store",
            "book store",
            # Government
            "police station",
            "court",
            "government office",
            "passport office",
            # Education
            "school",
            "college",
            "university",
            "library",
            "coaching center",
            # Religious
            "temple",
            "church",
            "mosque",
            "gurudwara",
            "ashram",
            # Entertainment
            "cinema",
            "movie theater",
            "park",
            "museum",
            "zoo",
            "stadium",
            "gym",
            # Emergency
            "fire station",
            "ambulance",
            # Tourist
            "tourist attraction",
            "waterfall",
            "beach",
            "trek",
            "camping site",
            "adventure park",
        ]
        for place in places:

            if place in cmd_lower:

                search_nearby(place)

                save_context(context_type=place, query=cmd, results=[])

                response = f"Opening nearby {place} on Google Maps."

                say_and_speak(response)

                return ""

    # ==========================================
    # CONTEXT FOLLOW UP
    # ==========================================

    if "which is best" in cmd_lower:

        print("WHICH IS BEST HIT")
        context = get_context()

        context_type = context.get("type")
        print("CONTEXT:", context)

        if not context_type:

            say_and_speak("Please search for a place first.")

            return ""

        response = (
            f"I opened nearby {context_type} results "
            f"on Google Maps. "
            f"Use search best {context_type} "
            f"to analyze them."
        )

        say_and_speak(response)

        return ""

    # ==========================================
    # SMART NAVIGATION ROUTER
    # ==========================================

    if is_navigation_query(cmd_lower):

        destination = extract_destination(cmd_lower)

        if destination:

            navigate_to(destination)

            response = (
                f"I found the route to " f"{destination}. " f"Opening Google Maps now."
            )

            say_and_speak(response)

            return ""

    # ==========================================
    # WORLDMONITOR COMMANDS
    # ==========================================

    if (
        "latest news" in cmd_lower
        or "world news" in cmd_lower
        or "world update" in cmd_lower
        or "what's happening" in cmd_lower
        or "what happening" in cmd_lower
        or "happening in the world" in cmd_lower
        or "world today" in cmd_lower
        or "world status" in cmd_lower
    ):

        try:
            open_world_monitor()
        except Exception as e:
            print("WorldMonitor Error:", e)

        news = get_world_news()

        print("NEWS:")
        print(news)

        summary = ask_ai(f"""
            Summarize these world news headlines.

            {news}

            Mention only the most important events.

            No numbering.
            No bullet points.

            Keep under 4 sentences.
            """)

        say_and_speak(summary)

        return ""

    # ==========================================
    # NEWS SEARCH ROUTER
    # ==========================================

    if any(word in cmd_lower for word in NEWS_WORDS):

        results = get_live_search(cmd)

        if results:

            summary = ask_ai(f"""
                Summarize these news headlines.

                Speak naturally.

                No numbering.
                No bullet points.

                {results}
                """)

            say_and_speak(summary)

            return ""

        return "No recent news found"

    # =====================================================
    # 🔥 TAB COMMANDS (ADD THIS)
    # =====================================================

    if "close current tab" in cmd or "close tab" in cmd:

        close_tab()

        say_and_speak("Tab closed")

        return ""

    elif "open new tab" in cmd or "new tab" in cmd:

        new_tab()

        say_and_speak("New tab opened")

        return ""

    elif "switch tab" in cmd or "next tab" in cmd:

        switch_tab()

        say_and_speak("Switched tab")

        return ""

    # =====================================================
    # 🔥 STOP
    # =====================================================
    if "stop" in cmd:
        from voice import stop_speech

        stop_speech()
        return smart_reply("Stopped")

    # =====================================================
    # 🔥 OPEN SEARCH RESULTS
    # =====================================================

    if "first song" in cmd or "first video" in cmd:

        from youtube import open_video

        open_video(0)

        response = "Playing first video"

        say_and_speak(response)

        return smart_reply(response)

    elif "second song" in cmd or "second video" in cmd:

        from youtube import open_video

        open_video(1)

        response = "Playing second video"

        say_and_speak(response)

        return smart_reply(response)

    elif "third song" in cmd or "third video" in cmd:

        from youtube import open_video

        open_video(2)

        response = "Playing third video"

        say_and_speak(response)

        return smart_reply(response)

    # =====================================================
    # 🔥 YOUTUBE PLAY (SAFE)
    # =====================================================
    if "play" in cmd and "browser" not in cmd:
        play_on_youtube(cmd)
        response = "Playing on YouTube"
        say_and_speak(response)
        return smart_reply(response)

    # =====================================================
    # 🔥 MEMORY
    # =====================================================
    elif "remember that" in cmd:
        try:
            text = cmd.replace("remember that", "").strip()

            if "my name is" in text:
                value = clean_name(text)
                remember("name", value)
                response = f"I will remember that your name is {value}"

            elif " is " in text:
                key, value = text.split(" is ", 1)
                remember(key.strip(), value.strip())
                response = f"I saved that {key} is {value}"

            else:
                response = "I couldn't understand what to remember"

        except:
            response = "I couldn't save that"

    elif "what is my name" in cmd:
        name = recall("name")
        response = f"Your name is {name}" if name else "I don't know your name"

    # =====================================================
    # 🔥 YOUTUBE CONTROLS
    # =====================================================
    yt_response = handle_youtube_controls(cmd)
    if yt_response:
        say_and_speak(yt_response)
        return smart_reply(yt_response)

    # =====================================================
    # 🔥 TIME (VOICE FIXED)
    # =====================================================
    elif "time" in cmd:
        place = cmd.split(" in ")[-1] if " in " in cmd else "india"

        result = get_country_time(place)

        if result:
            say_and_speak(result)
            return ""
        else:
            say_and_speak("Sorry, I couldn't get the time")
            return ""

    # =====================================================
    # 🔥 WEATHER (FIXED - NO DUPLICATE VOICE)
    # =====================================================
    elif "weather" in cmd or "temperature" in cmd:
        city = extract_city_smart(cmd)
        get_weather(city)
        return ""

    # =====================================================
    # 🔥 EXIT
    # =====================================================
    elif "exit" in cmd:
        response = "Goodbye"

    # main_ai.py mein "clear history" command add karo
    if "clear history" in cmd or "bhool jao sab" in cmd:
        from ai_chat import clear_history

        clear_history()
        response = "Conversation history cleared"

    # =====================================================
    # 🔥 DEFAULT AI (SMART FILTER)
    # =====================================================
    else:
        if any(x in cmd for x in ["open", "click", "scroll", "type"]):
            return ""  # browser intent ignore AI

        response = ask_ai(cmd) or ""
        response = response[:500]
        remember("last_question", cmd)
        remember("last_answer", response)

    # =====================================================
    # 🔥 FINAL SPEAK
    # =====================================================
    say_and_speak(response)
    return smart_reply(response)
