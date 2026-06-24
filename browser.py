# =========================================================
# 🔥 ADVANCED BROWSER AI MODULE
# =========================================================

import undetected_chromedriver as uc
import time
import threading
import random
import io
import pyautogui
import psutil
import subprocess
import re
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from voice import say_and_speak
from bs4 import BeautifulSoup
from ai_chat import ask_ai

driver = None
reader = None
vision_busy = False


def run_browser_task(task):

    threading.Thread(target=task, daemon=True).start()


def get_driver():
    return driver


# =========================================================
# 🔥 HUMAN RANDOM DELAY
# =========================================================
def human_delay(a=0.1, b=0.4):

    time.sleep(random.uniform(a, b))


# =========================================================
# 🔥 HUMAN TYPE
# =========================================================
def human_type(element, text):

    try:

        element.clear()

        human_delay(0.3, 0.7)

        for ch in text:

            element.send_keys(ch)

            # 🔥 realistic typing speed
            time.sleep(random.uniform(0.01, 0.03))

    except Exception as e:

        print("Human typing error:", e)


# =========================================================
# 🔥 HUMAN SCROLL
# =========================================================
def human_scroll(amount=500):

    d = safe_driver()

    if not d:
        return

    try:

        steps = random.randint(5, 12)

        step_amount = amount / steps

        for _ in range(steps):

            d.execute_script(f"window.scrollBy(0,{step_amount});")

            time.sleep(random.uniform(0.05, 0.2))

    except Exception as e:

        print("Human scroll error:", e)


# =========================================================
# 🔥 DYNAMIC CHROME VERSION DETECT
# =========================================================
def get_chrome_version():
    try:
        result = subprocess.run(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            capture_output=True,
            text=True,
            shell=True,
        )
        match = re.search(r"(\d+)\.\d+\.\d+\.\d+", result.stdout)
        if match:
            v = int(match.group(1))
            print(f"Chrome version (BLBeacon): {v}")
            return v
    except:
        pass
    try:
        result = subprocess.run(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Update\ClientState\{8A69D345-D564-463c-AFF1-A69D9E530F96}" /v pv',
            capture_output=True,
            text=True,
            shell=True,
        )
        match = re.search(r"(\d+)\.\d+\.\d+\.\d+", result.stdout)
        if match:
            v = int(match.group(1))
            print(f"Chrome version (Update): {v}")
            return v
    except:
        pass
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(
                    f"powershell -command \"(Get-Item '{path}').VersionInfo.ProductVersion\"",
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                match = re.search(r"(\d+)\.\d+", result.stdout)
                if match:
                    v = int(match.group(1))
                    print(f"Chrome version (exe): {v}")
                    return v
            except:
                continue
    print("⚠️ Chrome version auto-detect failed — using 148")
    return 148


# =========================================================
# 🔥 START BROWSER
# =========================================================
def start_browser():
    global driver

    try:
        if driver:
            driver.current_url
            print("Browser already running")
            return
    except:
        driver = None

    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/148.0 Safari/537.36"
        )

        version = get_chrome_version()
        driver = uc.Chrome(options=options, version_main=version)

        # ✅ Browser initialize hone ka wait karo
        time.sleep(2)

        print(f"✅ Browser started (Chrome {version})")

        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

    except Exception as e:
        print("Browser Error:", e)
        driver = None  # ✅ Failed toh None karo — say_and_speak nahi


# =========================================================
# 🔥 ENSURE BROWSER
# =========================================================
def ensure_browser():

    global driver

    try:

        if driver:

            driver.current_url

            return

    except:

        driver = None

    start_browser()


# =========================================================
# 🔥 SAFE DRIVER
# =========================================================
def safe_driver():
    global driver

    # ✅ Pehle try karo
    try:
        if driver:
            driver.current_url
            return driver
    except:
        driver = None

    # ✅ Browser start karo
    try:
        print("⚡ Starting browser...")
        start_browser()
        time.sleep(2)  # ✅ initialize hone do

        if driver:
            # ✅ Ek baar aur verify karo
            try:
                driver.current_url
                return driver
            except:
                driver = None

    except Exception as e:
        print("Safe driver error:", e)

    # ✅ Sirf ab bolega — jab sach mein fail ho
    say_and_speak("Browser not available")
    return None


# =========================================================
# 🔥 SEARCH
# =========================================================
def search_in_browser(query):

    def task():

        ensure_browser()

        time.sleep(2)

        print("DEBUG driver:", driver)

        d = safe_driver()

        if not d:
            start_browser()

            time.sleep(2)

            d = safe_driver()

        if not d:
            say_and_speak("Browser not available")
            return

        q = query.replace("search", "").strip()

        if not q:
            q = "latest news"

        d.get(f"https://www.google.com/search?q={q}")

        say_and_speak(f"Searching {q}")

    run_browser_task(task)


# =========================================================
# 🔥 HUMAN MOUSE MOVE
# =========================================================
def human_move(element):

    d = safe_driver()

    if not d:
        return

    try:

        actions = ActionChains(d)

        # 🔥 small pause
        human_delay(0.2, 0.5)

        actions.move_to_element(element)

        actions.pause(random.uniform(0.2, 0.6))

        actions.perform()

    except Exception as e:

        print("Human move error:", e)


# =========================================================
# 🔥 HUMAN CLICK
# =========================================================
def human_click(element):

    d = safe_driver()

    if not d:
        return

    try:

        human_move(element)

        human_delay(0.2, 0.7)

        try:

            element.click()

        except:

            d.execute_script("arguments[0].click();", element)

        human_delay(0.3, 0.8)

    except Exception as e:

        print("Human click error:", e)


# =========================================================
# 🔥 OPEN SEARCH RESULT (ULTRA FIXED)
# =========================================================
def open_result(index=0):

    d = safe_driver()

    if not d:
        return

    def task():

        try:

            results = d.find_elements(By.CSS_SELECTOR, "a[href]")

            valid = []

            for r in results:

                try:

                    href = r.get_attribute("href")

                    text = r.text.strip()

                    if href and "google" not in href and text:

                        valid.append(r)

                except:
                    continue

            if not valid:
                say_and_speak("No search results found")
                return

            if len(valid) <= index:
                say_and_speak("Result number not available")
                return

            target = valid[index]

            d.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            """,
                target,
            )

            time.sleep(1)

            try:
                human_click(target)

            except:
                d.execute_script("arguments[0].click();", target)

            say_and_speak(f"Opening result {index+1}")

        except Exception as e:
            print("Open result error:", e)
            say_and_speak("Unable to open result")

    run_browser_task(task)


# =========================================================
# 🔥 SCROLL
# =========================================================
def scroll_down():
    d = safe_driver()
    if d:
        human_scroll(600)
        say_and_speak("Scrolling down")


def scroll_up():
    d = safe_driver()
    if d:
        human_scroll(-600)
        say_and_speak("Scrolling up")


def volume_up():
    try:
        for _ in range(10):
            pyautogui.press("volumeup")
            time.sleep(0.03)

        say_and_speak("Volume increased")

    except Exception as e:
        print("Volume up error:", e)


def volume_down():
    try:
        for _ in range(10):
            pyautogui.press("volumedown")
            time.sleep(0.03)

        say_and_speak("Volume decreased")

    except Exception as e:
        print("Volume down error:", e)


# =========================================================
# 🔥 CLICK
# =========================================================
def click_first_button():
    d = safe_driver()
    if not d:
        return

    try:
        btn = d.find_element(By.TAG_NAME, "button")
        human_click(btn)
        say_and_speak("Button clicked")
    except:
        say_and_speak("No button found")


# =========================================================
# 🔥 TYPE
# =========================================================
# =========================================================
# 🔥 SMART TYPING SYSTEM
# =========================================================
def smart_type(cmd):
    d = safe_driver()
    if not d:
        return

    try:
        cmd = cmd.lower().replace("type", "").strip()

        # =================================================
        # 🔥 EXTRACT TARGET FIELD
        # =================================================
        target = None
        text = cmd

        if " in " in cmd:
            parts = cmd.split(" in ")

            text = parts[0].strip()
            target = parts[1].strip()

        # =================================================
        # 🔥 IF TARGET PROVIDED
        # =================================================
        if target:

            xpaths = [
                # placeholder
                f"//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{target}')]",
                # name
                f"//input[contains(translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{target}')]",
                # aria-label
                f"//input[contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{target}')]",
                # textarea
                f"//textarea[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{target}')]",
            ]

            for xpath in xpaths:

                elements = d.find_elements(By.XPATH, xpath)

                for el in elements:
                    try:
                        el.clear()
                        human_type(el, text)

                        say_and_speak("Typing done")
                        return

                    except:
                        continue

        # =================================================
        # 🔥 FALLBACK ACTIVE ELEMENT
        # =================================================
        active = d.switch_to.active_element

        human_type(active, text)

        say_and_speak("Typing done")

    except Exception as e:
        print("Smart typing error:", e)
        say_and_speak("Unable to type")


# =========================================================
# 🔥 CLEAN AI TEXT FOR SPEECH
# =========================================================
def clean_ai_text(text):

    text = text.replace("*", "")
    text = text.replace("+", "")
    text = text.replace("#", "")
    text = text.replace("-", " ")

    # remove extra spaces
    text = " ".join(text.split())

    return text


# =========================================================
# 🔥 NAVIGATION
# =========================================================
def go_back():

    d = safe_driver()

    if not d:
        return

    def task():

        try:
            d.back()
            say_and_speak("Going back")

        except Exception as e:
            print("Back error:", e)

    run_browser_task(task)


def go_forward():

    d = safe_driver()

    if not d:
        return

    def task():

        try:
            d.forward()
            say_and_speak("Going forward")

        except Exception as e:
            print("Forward error:", e)

    run_browser_task(task)


def refresh_page():

    d = safe_driver()

    if not d:
        return

    def task():

        try:
            d.refresh()
            say_and_speak("Page refreshed")

        except Exception as e:
            print("Refresh error:", e)

    run_browser_task(task)


# =========================================================
# 🔥 TAB MANAGEMENT (ADVANCED)
# =========================================================


def new_tab(url="https://www.google.com"):
    d = safe_driver()
    if not d:
        return

    try:
        # 🔥 method 1 (best stable)
        d.switch_to.new_window("tab")
        d.get(url)

        say_and_speak("New tab opened")

    except Exception as e:
        print("New tab error:", e)

        try:
            # 🔥 fallback method
            d.execute_script(f"window.open('{url}');")
            d.switch_to.window(d.window_handles[-1])

            say_and_speak("New tab opened")

        except Exception as e2:
            print("Fallback error:", e2)
            say_and_speak("Failed to open new tab")


def close_tab():
    d = safe_driver()
    if not d:
        return

    try:
        if len(d.window_handles) > 1:
            d.close()
            d.switch_to.window(d.window_handles[-1])
            say_and_speak("Tab closed")
        else:
            say_and_speak("Only one tab open")

    except Exception as e:
        print("Close tab error:", e)


def switch_tab(index=None):

    d = safe_driver()

    if not d:
        return

    try:

        tabs = d.window_handles

        # 🔥 specific tab
        if index is not None:

            if len(tabs) > index:

                d.switch_to.window(tabs[index])

                say_and_speak(f"Switched to tab {index+1}")

            else:

                say_and_speak("No such tab")

            return

        # 🔥 cyclic switch
        current = d.current_window_handle

        current_index = tabs.index(current)

        next_index = (current_index + 1) % len(tabs)

        d.switch_to.window(tabs[next_index])

        say_and_speak(f"Switched to tab {next_index+1}")

    except Exception as e:

        print("Switch tab error:", e)


def open_website(name):

    # ✅ Pehle browser start karo — wait ke saath
    ensure_browser()
    time.sleep(1)  # ✅ ready hone do

    d = driver  # ✅ safe_driver() nahi — seedha use karo

    if not d:
        say_and_speak("Browser not available")
        return

    try:
        name = name.lower().strip()

        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "whatsapp": "https://web.whatsapp.com",
            "chatgpt": "https://chatgpt.com",
            "twitter": "https://www.twitter.com",
            "linkedin": "https://www.linkedin.com",
            "netflix": "https://www.netflix.com",
        }

        for key, url in sites.items():
            if key in name:
                d.get(url)
                say_and_speak(f"Opening {key}")
                return

        # Generic domain
        clean = name.replace("open", "").strip().replace(" ", "")

        blocked = ["user-agent", "mozilla", "chrome", "safari"]
        if any(b in clean for b in blocked):
            say_and_speak("Invalid website")
            return

        d.get(f"https://www.{clean}.com")
        say_and_speak(f"Opening {clean}")

    except Exception as e:
        print("Open website error:", e)
        say_and_speak("Unable to open website")

        # =================================================
        # 🔥 SAFE DOMAIN OPEN
        # =================================================
        clean = name.replace("open", "").strip().replace(" ", "")

        # 🔥 BLOCK INVALID URLS
        blocked = ["user-agent", "mozilla", "chrome", "safari"]

        for b in blocked:

            if b in clean:

                say_and_speak("Invalid website")

                return

        # =================================================
        # 🔥 OPEN DOMAIN
        # =================================================
        url = f"https://www.{clean}.com"

        d.get(url)

        say_and_speak(f"Opening {clean}")

    except Exception as e:

        print("Open website error:", e)

        say_and_speak("Unable to open website")


# =========================================================
# 🔥 CLOSE BROWSER
# =========================================================
def close_browser():
    global driver

    # Step 1 — Selenium driver quit
    try:
        if driver:
            driver.quit()
    except:
        pass

    driver = None

    # Step 2 — Chrome process bhi force kill karo
    try:
        import psutil

        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] in ["chrome.exe", "Chrome.exe"]:
                proc.kill()
    except:
        pass

    return True


# =========================================================
# 🔥 CLOSE APP
# =========================================================


def close_app(app_name):

    app_name = app_name.lower()

    process_map = {
        "chrome": "chrome.exe",
        "vscode": "Code.exe",
        "notepad": "notepad.exe",
        "spotify": "Spotify.exe",
    }

    target = process_map.get(app_name)

    if not target:
        say_and_speak(f"{app_name} not found")
        return False

    for proc in psutil.process_iter():

        try:
            if proc.name().lower() == target.lower():
                proc.kill()
                say_and_speak(f"Closing {app_name}")
                return True
        except:
            pass

    say_and_speak(f"{app_name} is not running")
    return False


# =========================================================
# 🔥 SMART ELEMENT CLICK
# =========================================================
def smart_click(text):
    d = safe_driver()
    if not d:
        return

    try:
        text = text.lower().replace("click", "").replace("button", "").strip()

        # 🔥 possible xpath matches
        xpaths = [
            # exact text
            f"//*[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]]",
            # button text
            f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]",
            # link text
            f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]",
            # input buttons
            f"//input[contains(@value, '{text}')]",
            # aria-label support
            f"//*[contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{text}')]",
        ]

        for xpath in xpaths:
            elements = d.find_elements(By.XPATH, xpath)

            for el in elements:
                try:
                    d.execute_script("arguments[0].scrollIntoView(true);", el)
                    human_click(el)

                    say_and_speak(f"Clicked {text}")
                    return

                except:
                    continue

        say_and_speak(f"{text} not found")

    except Exception as e:
        print("Smart click error:", e)
        say_and_speak("Unable to click")


# =========================================================
# 🔥 WEBSITE UNDERSTANDING AI
# =========================================================
def read_website(mode="summary"):
    d = safe_driver()
    if not d:
        return

    try:
        html = d.page_source

        soup = BeautifulSoup(html, "html.parser")

        # 🔥 remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # 🔥 clean text
        lines = [line.strip() for line in text.splitlines()]
        clean_text = " ".join([l for l in lines if l])

        if not clean_text:
            say_and_speak("I could not read this page")
            return

        # =================================================
        # 🔥 HEADLINE MODE
        # =================================================
        if mode == "headlines":

            headlines = []

            for tag in soup.find_all(["h1", "h2", "h3"]):
                txt = tag.get_text(strip=True)

                if txt and len(txt) > 3:
                    headlines.append(txt)

            if headlines:
                result = "Top headlines are: " + ". ".join(headlines[:5])
            else:
                result = "No headlines found"

        # =================================================
        # 🔥 SUMMARY MODE
        # =================================================
        else:
            short = clean_text[:3000]

            prompt = f"""
            Summarize this website in short simple points:

            {short}
            """

            result = ask_ai(prompt)

        cleaned = clean_ai_text(result)
        say_and_speak(cleaned)

    except Exception as e:
        print("Website read error:", e)
        say_and_speak("Unable to understand this website")


# =========================================================
# 🔥 AI VISION CLICK (ULTRA ADVANCED)
# =========================================================
def vision_click(text):
    import cv2
    import numpy as np

    # from PIL import Image

    global vision_busy

    # 🔥 prevent duplicate execution
    if vision_busy:
        say_and_speak("Vision already running")
        return

    vision_busy = True

    try:

        d = safe_driver()

        if not d:
            vision_busy = False
            return

        # =================================================
        # 🔥 LOAD OCR
        # =================================================
        reader = get_reader()

        # =================================================
        # 🔥 SCREENSHOT
        # =================================================
        screenshot = d.get_screenshot_as_png()

        image = Image.open(io.BytesIO(screenshot))

        # 🔥 resize = faster OCR
        image = image.resize((image.width // 2, image.height // 2))

        image_np = np.array(image)

        # =================================================
        # 🔥 OCR DETECT
        # =================================================
        results = reader.readtext(image_np, detail=1, paragraph=False)

        target = text.lower()

        for r in results:

            bbox, detected, conf = r

            detected = detected.lower()

            detected_text = detected.lower().strip()

            target_text = target.lower().strip()

            print("OCR FOUND:", detected_text)

            # 🔥 SMART MATCH
            # 🔥 SMART FUZZY MATCH

            target_words = target_text.split()

            matched = 0

            for word in target_words:
                if word in detected_text:
                    matched += 1

            if matched >= max(1, len(target_words) // 2):

                x = int((bbox[0][0] + bbox[2][0]) / 2)

                y = int((bbox[0][1] + bbox[2][1]) / 2)

                # 🔥 SAFE JS CLICK
                d.execute_script(f"""
                let el = document.elementFromPoint({x}, {y});

                if(el){{
                    el.click();
                }}
                """)

                say_and_speak(f"Clicked {text}")

                vision_busy = False
                return

        say_and_speak(f"{text} not found")

    except Exception as e:

        print("Vision click error:", e)

        say_and_speak("Vision click failed")

    vision_busy = False


# =========================================================
# 🔥 SCREEN SHOT
# =========================================================


def take_screenshot():

    try:

        path = "screenshot.png"

        img = pyautogui.screenshot()

        img.save(path)

        say_and_speak("Screenshot captured")

        return path

    except Exception as e:

        print("Screenshot error:", e)

        say_and_speak("Unable to take screenshot")


# =========================================================
# 🔥 VISION SCREEN UNDERSTANDING
# =========================================================
def understand_screen():
    # from PIL import Image

    d = safe_driver()

    if not d:
        return

    try:

        path = "vision_read.png"

        d.save_screenshot(path)

        reader = get_reader()

        results = reader.readtext(path)

        texts = []

        for r in results:

            detected = r[1].strip()

            if len(detected) > 2:
                texts.append(detected)

        if not texts:

            say_and_speak("I could not understand this screen")

            return

        combined = " ".join(texts[:40])

        prompt = f"""
        Explain this screen simply:

        {combined}
        """

        answer = ask_ai(prompt)

        cleaned = clean_ai_text(answer)

        say_and_speak(cleaned)

    except Exception as e:

        print("Vision understand error:", e)

        say_and_speak("Unable to understand screen")


# =========================================================
# 🔥 LOAD OCR ONLY WHEN NEEDED
# =========================================================
def get_reader():

    global reader

    if reader is None:
        import easyocr

        print("🔥 Loading Vision AI...")

        reader = easyocr.Reader(["en"], gpu=False)

    return reader


# =========================================================
# 🔥 OPEN FIRST YOUTUBE VIDEO
# =========================================================
def open_first_video():

    d = safe_driver()

    if not d:
        return

    try:

        current = d.current_url.lower()

        # =================================================
        # 🔥 ONLY YOUTUBE
        # =================================================
        if "youtube.com" not in current:

            say_and_speak("You are not on YouTube")

            return

        # =================================================
        # 🔥 WAIT
        # =================================================
        wait = WebDriverWait(d, 15)

        # =================================================
        # 🔥 FIRST VIDEO
        # =================================================
        video = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//ytd-video-renderer//a[@id='thumbnail'])[1]")
            )
        )

        # =================================================
        # 🔥 SCROLL
        # =================================================
        d.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior:'smooth',
                block:'center'
            });
            """,
            video,
        )

        time.sleep(1)

        # =================================================
        # 🔥 SAFE CLICK
        # =================================================
        try:

            human_click(video)

        except:

            d.execute_script("arguments[0].click();", video)

        say_and_speak("Opening first video")

    except Exception as e:

        print("Open video error:", e)

        say_and_speak("Unable to open video")


# =========================================================
# 🔥 NEXT SONG
# =========================================================
def next_video():

    d = safe_driver()

    if not d:
        return

    try:

        btn = d.find_element(By.CSS_SELECTOR, "a.ytp-next-button")

        human_click(btn)

        say_and_speak("Playing next video")

    except Exception as e:

        print("Next video error:", e)

        say_and_speak("Unable to play next video")

        # =================================================
        # 🔥 SWITCH TAB (SMART)
        # =================================================


def switch_to_tab_by_name(name):

    d = safe_driver()

    if not d:
        return

    try:

        name = name.lower()

        tabs = d.window_handles

        for tab in tabs:

            d.switch_to.window(tab)

            title = d.title.lower()

            url = d.current_url.lower()

            if name in title or name in url:

                say_and_speak(f"Switched to {name}")

                return

        say_and_speak(f"{name} tab not found")

    except Exception as e:

        print("Tab switch error:", e)


# =========================================================
# 🔥 SMART SEARCH
# =========================================================
def smart_search(cmd):

    d = safe_driver()

    if not d:
        return

    try:

        current = d.current_url.lower()

        # =================================================
        # 🔥 YOUTUBE SEARCH
        # =================================================
        if "youtube" in current:

            query = cmd.replace("search", "").replace("on youtube", "").strip()

            if not query:
                query = "latest songs"

            # 🔥 search directly on youtube
            d.get(f"https://www.youtube.com/results?search_query={query}")

            say_and_speak(f"Searching {query} on YouTube")

            return

        # =================================================
        # 🔥 NORMAL GOOGLE SEARCH
        # =================================================
        search_in_browser(cmd)

    except Exception as e:

        print("Smart search error:", e)

        search_in_browser(cmd)


# =========================================================
# 🔥 MASTER HANDLER (FIXED)
# =========================================================
def handle_browser_commands(cmd):

    cmd = cmd.lower()

    # =====================================================
    # 🔥 OPEN BROWSER
    # =====================================================
    if "open browser" in cmd or "browser open" in cmd:
        start_browser()
        return True

    # CLOSE YOUTUBE
    if "close youtube" in cmd:

        close_tab()

        return True

    # CLOSE BROWSER
    if "close browser" in cmd or "browser close" in cmd or "close chrome" in cmd:

        close_browser()

        return True
    # =====================================================
    # 🔥 TAB MANAGEMENT (HIGH PRIORITY)
    # =====================================================
    if "open new tab" in cmd or cmd.strip() == "new tab":
        new_tab()
        return True

    if "close tab" in cmd:
        close_tab()
        return True

    if "switch to second tab" in cmd:
        switch_tab(1)
        return True

    if "switch to third tab" in cmd:
        switch_tab(2)
        return True

    if "switch tab" in cmd:
        switch_tab()
        return True

    # =====================================================
    # 🔥 WEBSITE OPEN (SAFE)
    # =====================================================
    if "open youtube" in cmd or "youtube open" in cmd or "youtube" in cmd:
        open_website("youtube")
        return True

    if "open google" in cmd:
        open_website("google")
        return True

    if "open facebook" in cmd:
        open_website("facebook")
        return True

    if "open instagram" in cmd:
        open_website("instagram")
        return True

    # =========================================================
    # 🔥 AI VISION COMMANDS
    # =========================================================

    if "vision click" in cmd:

        target = cmd.replace("vision click", "").strip()

        vision_click(target)

        return True

    if "what is on screen" in cmd:

        understand_screen()

        return True

    # =====================================================
    # 🔥 SEARCH RESULT CONTROL
    # =====================================================
    if "open first website" in cmd or "open first result" in cmd:
        open_result(0)
        return True

    if "open second website" in cmd or "open second result" in cmd:
        open_result(1)
        return True

    # =========================================================
    # 🔥 OPEN FIRST VIDEO
    # =========================================================
    if (
        "open first video" in cmd
        or "play first video" in cmd
        or "click on first video" in cmd
    ):
        open_first_video()
        return True

    # =========================================================
    # 🔥 NEXT VIDEO
    # =========================================================
    if "play next video" in cmd:
        next_video()
        return True

    # =========================================================
    # 🔥 SWITCH TAB (SMART)
    # =========================================================

    if "switch to" in cmd and "tab" in cmd:

        target = cmd.replace("switch to", "").replace("tab", "").strip()

        switch_to_tab_by_name(target)

        return True

    # =====================================================
    # 🔥 SMART SEARCH
    # =====================================================
    if "search" in cmd:

        smart_search(cmd)

        return True

    if "volume up" in cmd:
        volume_up()
        return True

    if "volume down" in cmd:
        volume_down()
        return True

    # =====================================================
    # 🔥 SCROLL
    # =====================================================
    if "scroll down" in cmd:
        scroll_down()
        return True

    if "scroll up" in cmd:
        scroll_up()
        return True

    # =====================================================
    # 🔥 CLICK / TYPE
    # =====================================================
    if "click" in cmd:
        smart_click(cmd)
        return True

    if "type" in cmd:
        smart_type(cmd)
        return True

    # =====================================================
    # 🔥 GENERIC OPEN (FIXED)
    # =====================================================
    if cmd.startswith("open "):

        site = cmd.replace("open", "", 1).strip()

        blocked = [
            "browser",
            "chrome",
            "new tab",
            "first website",
            "second website",
            "first result",
            "second result",
            "first video",
        ]

        if site and site not in blocked:
            open_website(site)
            return True

    # =====================================================
    # 🔥 WEBSITE UNDERSTANDING
    # =====================================================
    if "summarize this page" in cmd:
        read_website("summary")
        return True

    if "read this website" in cmd:
        read_website("summary")
        return True

    if "what is written" in cmd:
        read_website("summary")
        return True

    if "read headlines" in cmd:
        read_website("headlines")
        return True

    return False


def create_file(filename):

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("")

        return True

    except Exception as e:
        print("Create file error:", e)
        return False


def read_file(filename):

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        print("Read file error:", e)
        return "Unable to read file"
