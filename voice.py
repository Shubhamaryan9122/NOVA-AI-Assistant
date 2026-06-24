# =========================================================
# 🔥 VOICE SYSTEM FINAL (FULL DUPLEX + WAKE WORD FIXED)
# =========================================================

import speech_recognition as sr
import threading
import time
import asyncio
import edge_tts
import pygame
import uuid
import os
import tempfile
import re
from num2words import num2words

# ✅ Naya — do voices
VOICE_EN = "en-IN-NeerjaNeural"  # English ke liye
VOICE_HI = "hi-IN-SwaraNeural"  # Hindi/Hinglish ke liye

pygame.mixer.init()


# =========================================================
# 🔥 GLOBAL STATE
# =========================================================

is_speaking = False

stop_requested = False

last_cmd = ""

last_time = 0

ui_callback = None


# =========================================================
# 🔥 WAKE WORD STATE
# =========================================================

assistant_active = False
wake_timeout = 5
wake_time = 0

WAKE_WORDS = [
    "nova",
    "innova",
    "novaa",
    "nov",
]

# =========================================================
# 🔥 UI CALLBACK
# =========================================================


def set_ui_callback(func):

    global ui_callback

    ui_callback = func


# 🔥 HINDI DETECT
def detect_hindi(text):
    hindi_words = [
        "hai",
        "hain",
        "kya",
        "nahi",
        "mera",
        "tera",
        "aur",
        "yeh",
        "woh",
        "karo",
        "karo",
        "bolo",
        "theek",
        "achha",
        "suno",
        "dekho",
        "batao",
        "mujhe",
        "tumhe",
        "humara",
        "apna",
        "kitna",
        "abhi",
        "baad",
        "pehle",
        "bahut",
        "thoda",
        "band",
        "chalu",
        "kholo",
        "chalao",
        "ruko",
    ]
    text_lower = text.lower()
    count = sum(1 for word in hindi_words if word in text_lower)
    return count >= 4  # 2 ya zyada Hindi words mile toh Hindi voice


def convert_numbers(text):

    def replace(match):

        try:
            num = int(match.group())
            return num2words(num)

        except:
            return match.group()

    return re.sub(r"\b\d+\b", replace, text)


# =========================================================
# 🔥 EDGE TTS SPEAK
# =========================================================


async def speak_async(text):

    global is_speaking
    global stop_requested

    try:

        if not text:
            return

        stop_requested = False

        is_speaking = True

        if ui_callback:
            ui_callback("SYSTEM", "VOICE_START")

        fd, file = tempfile.mkstemp(suffix=".mp3")

        os.close(fd)

        voice = VOICE_HI if detect_hindi(text) else VOICE_EN

        communicate = edge_tts.Communicate(text, voice)

        await communicate.save(file)

        pygame.mixer.music.load(file)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            if stop_requested:

                pygame.mixer.music.stop()

                break

            await asyncio.sleep(0.1)

    except Exception as e:

        print("TTS Error:", e)

    finally:

        try:
            pygame.mixer.music.unload()
        except:
            pass

        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            print("Delete Error:", e)

        is_speaking = False

        stop_requested = False

        if ui_callback:
            ui_callback("SYSTEM", "VOICE_STOP")


def speak(text):

    try:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        loop.run_until_complete(speak_async(text))

        loop.close()

    except Exception as e:
        print("Speak Error:", e)


def say_and_speak(text):

    if not text:
        return

    # 🔥 HUD SPEAKING START
    if ui_callback:
        ui_callback("voice", "VOICE_START")

    # 🔥 CLEAN TEXT
    for ch in ["**", "*", "#", "_", "`"]:
        text = text.replace(ch, "")

    text = " ".join(text.split())

    print("AI:", text)

    if ui_callback:
        ui_callback("AI", text)

    # 🔥 keep UI text full, but speak shorter text
    speak_text = text
    print("TTS TEXT BEFORE:", speak_text)

    speak_text = text

    speak_text = speak_text.replace("₹", "")

    print("TTS TEXT BEFORE:", speak_text)

    # Numbered list remove
    speak_text = re.sub(r"(?m)^\d+\.\s+", "", speak_text)
    print("RAW SPEAK TEXT:", speak_text)

    # Sirf 4+ digit numbers convert
    def replace_large_numbers(match):

        print("MATCH:", match.group())

        try:

            value = match.group()
            value = value.replace(",", "")

            num = int(value)

            if num >= 1000:
                return num2words(num)

            return str(num)

        except:
            return match.group()

    speak_text = re.sub(
        r"\b\d{1,3}(?:,\d{3})+\b|\b\d+\b", replace_large_numbers, speak_text
    )

    print("TTS AFTER CONVERSION:", speak_text)

    # Less pauses for news/articles
    speak_text = speak_text.replace(". ", ", ")
    speak_text = speak_text.replace("? ", ", ")
    speak_text = speak_text.replace("! ", ", ")

    try:
        speak(speak_text)

    except Exception as e:
        print("TTS Error:", e)

    # 🔥 HUD BACK TO ONLINE
    if ui_callback:
        ui_callback("voice", "VOICE_STOP")


# =========================================================
# 🔥 STOP SPEECH
# =========================================================


def stop_speech():

    global stop_requested
    global is_speaking

    stop_requested = True

    try:

        pygame.mixer.music.stop()

    except:
        pass

    is_speaking = False

    if ui_callback:
        ui_callback("SYSTEM", "VOICE_STOP")


# =========================================================
# 🔥 LISTEN (FULL DUPLEX + SMART FILTER)
# =========================================================


def listen():

    global is_speaking
    global assistant_active
    global wake_time

    # =====================================================
    # 🔥 BLOCK DURING VISION AI
    # =====================================================

    try:

        import browser

        if browser.vision_busy:
            return ""

    except:
        pass

    r = sr.Recognizer()

    # =====================================================
    # ADVANCED SETTINGS
    # =====================================================

    r.energy_threshold = 100

    r.dynamic_energy_threshold = True

    r.pause_threshold = 1.2

    r.phrase_threshold = 0.1

    r.non_speaking_duration = 0.3

    try:

        with sr.Microphone() as source:

            # 🔥 show listening only after wake word
            if assistant_active:

                print("Listening...")

            if ui_callback:

                ui_callback("SYSTEM", "LISTENING")

            # 🔥 fast noise adjustment
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(source, timeout=4, phrase_time_limit=12)

        # =================================================
        # 🔥 SPEECH TO TEXT
        # =================================================

        cmd = r.recognize_google(audio, language="en-IN")

        cmd = cmd.lower().strip()
        print("RAW CMD:", cmd)

        if ui_callback:
            ui_callback("USER", cmd)

        # =================================================
        # 🔥 STOP WORD PRIORITY (WORKS WHILE SPEAKING)
        # =================================================

        STOP_WORDS = [
            "stop",
            "stop Nova",
            "Nova stop",
            "stop noba",
            "band ho ja",
            "chup",
            "bas karo",
            "ruko",
        ]

        if any(stop_word in cmd for stop_word in STOP_WORDS):

            if is_speaking:

                print("🔥 INTERRUPT DETECTED")

                stop_speech()

                # wake_time = time.time()

                return "stop"

        # =================================================
        # 🔥 WAKE WORD LOGIC
        # =================================================

        wake_match = None

        for wake in WAKE_WORDS:

            if cmd.startswith(wake):
                wake_match = wake
                break

        # सिर्फ wake word बोला
        if cmd in WAKE_WORDS:

            assistant_active = True
            wake_time = time.time()

            try:

                ding_path = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "Ding.mp3",  # ← capital D check karo file ka naam
                )
                pygame.mixer.Sound(ding_path).play()
            except:
                pass

            print("AI: Nova activated")

            if ui_callback:
                ui_callback("AI", "Nova activated")

            print("Waiting for command...")

            with sr.Microphone() as source:

                r.adjust_for_ambient_noise(source, duration=0.2)

                audio = r.listen(source, timeout=5, phrase_time_limit=6)

                cmd = r.recognize_google(audio, language="en-IN")

                cmd = cmd.lower().strip()

                print("You:", cmd)

                return cmd

        # wake + command
        if wake_match:

            remaining_cmd = cmd[len(wake_match) :].strip()

            assistant_active = True
            wake_time = time.time()

            # Sirf "nova" bola gaya
            if not remaining_cmd:

                try:
                    ding_path = os.path.join(
                        os.path.abspath(os.path.dirname(__file__)), "Ding.mp3"
                    )

                    if os.path.exists(ding_path):
                        pygame.mixer.Sound(ding_path).play()

                except:
                    pass

                if ui_callback:
                    ui_callback("AI", "Nova activated")

                return ""

            # Nova + command
            print("WAKE CMD:", remaining_cmd)

            return remaining_cmd

        # wake नहीं मिला
        elif not assistant_active:
            return ""

        # 5 second timeout
        if assistant_active:

            if time.time() - wake_time > wake_timeout:
                assistant_active = False
                return ""

        # सिर्फ wake बोला लेकिन command नहीं
        if cmd == "":
            return ""

        # =================================================
        # 🔥 CLEAN INPUT
        # =================================================

        if len(cmd) < 2:
            return ""

        cmd = " ".join(cmd.split())

    # =====================================================
    # 🔥 SAFE ERRORS
    # =====================================================

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except sr.RequestError as e:

        print("Speech API Error:", e)

        return ""

    except Exception as e:

        print("Listen Error:", e)

        return ""


# =========================================================
# 🔥 EXECUTION ENGINE
# =========================================================


def execute_ai(process_func, cmd):

    global last_cmd
    global last_time
    global assistant_active

    if not cmd:
        return

    cmd_clean = cmd.lower().strip()

    # =====================================================
    # 🔥 WAKE WORD SYSTEM
    # =====================================================

    if cmd_clean in WAKE_WORDS:

        assistant_active = True

        # 🔥 HUD popup on wake
        if assistant_active and ui_callback:

            ui_callback("SYSTEM", "LISTENING")

        say_and_speak("Nova activated")

        return

    # =====================================================
    # 🔥 SLEEP MODE
    # =====================================================

    if cmd_clean in ["sleep", "go to sleep", "stop listening"]:

        assistant_active = False

        say_and_speak("Going to sleep")

        return

    current_time = time.time()

    # 🔥 duplicate protection
    if cmd == last_cmd and (current_time - last_time < 2):
        return

    last_cmd = cmd
    last_time = current_time

    if ui_callback and assistant_active:

        ui_callback("SYSTEM", "LISTENING")

    result = process_func(cmd)

    # 🔥 avoid duplicate speaking
    if result and result.strip() and not is_speaking:

        say_and_speak(result)
