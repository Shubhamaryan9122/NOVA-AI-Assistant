# =========================================================
# 🔥 YOUTUBE MODULE (FULL FIXED + SAFE + NO FEATURE LOSS)
# =========================================================

import time
import browser
from voice import say_and_speak
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import human_click
from browser import get_driver, ensure_browser


# =========================================================
# 🔥 ENSURE YOUTUBE OPEN
# =========================================================
def ensure_youtube():
    ensure_browser()
    driver = get_driver()

    if driver and "youtube.com" not in driver.current_url:
        driver.get("https://www.youtube.com")


# =========================================================
# 🔥 PLAY VIDEO (FIXED + FALLBACK)
# =========================================================
def play_on_youtube(cmd):
    try:
        ensure_browser()
        driver = get_driver()

        if not driver:
            print("Driver not available")
            return

        query = cmd.lower()

# 🔥 remove command words only
        for word in ["play", "youtube", "open", "search"]:
            query = query.replace(word, "")

        query = query.strip()

# 🔥 ensure only ONE "song"
        if "song" not in query:
            query += " song"


# 🔥 FORCE SONG SEARCH (VERY IMPORTANT)
        if "song" not in query:
            query = query + " song"   

        if not query:
            query = "latest song"

        if not query:
            query = "latest song"

        url = f"https://www.youtube.com/results?search_query={query}"
        driver.get(url)

        time.sleep(2)

        wait = WebDriverWait(driver, 15)

        try:
            # 🔥 PRIMARY CLICK
            video = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//ytd-video-renderer//a[@id='thumbnail'])[1]")
                )
            )

            human_click(video)

        except Exception as e:
            print("Primary click failed:", e)

            try:
                # 🔥 FALLBACK METHOD 1 (href open)
                video_links = driver.find_elements(By.XPATH, "//ytd-video-renderer//a[@id='thumbnail']")

                if video_links:
                    href = video_links[0].get_attribute("href")
                    if href:
                        driver.get(href)
                        return

            except Exception as e2:
                print("Fallback method 1 failed:", e2)

            # 🔥 FINAL FALLBACK
            print("Fallback search reload")
            driver.get(url)

    except Exception as e:
        print("YouTube Error:", e)


# =========================================================
# 🔥 SAFE DRIVER EXECUTION
# =========================================================
def safe_exec(script):
    driver = get_driver()
    if driver:
        try:
            return driver.execute_script(script)
        except Exception as e:
            print("JS Error:", e)


# =========================================================
# 🔥 CONTROLS (SAFE)
# =========================================================
def youtube_play_pause():
    safe_exec(
        "let v=document.querySelector('video'); if(v){v.paused?v.play():v.pause();}"
    )


def youtube_mute():
    safe_exec(
        "let v=document.querySelector('video'); if(v){v.muted=!v.muted;}"
    )


def is_muted():
    return safe_exec(
        "let v=document.querySelector('video'); return v?v.muted:false;"
    )


def youtube_volume_up():
    safe_exec(
        "let v=document.querySelector('video'); if(v){v.volume=Math.min(1,v.volume+0.1);}"
    )


def youtube_volume_down():
    safe_exec(
        "let v=document.querySelector('video'); if(v){v.volume=Math.max(0,v.volume-0.1);}"
    )


def youtube_next_video():
    safe_exec(
        "let btn=document.querySelector('.ytp-next-button'); if(btn){btn.click();}"
    )


def youtube_skip_ad():
    safe_exec(
        "let btn=document.querySelector('.ytp-ad-skip-button'); if(btn){btn.click();}"
    )


# =====================================================
# 🔥 OPEN VIDEO BY INDEX
# =====================================================

def open_video(index=0):

    driver = browser.driver

    try:

        videos = driver.find_elements(
            By.XPATH,
            '//ytd-video-renderer//a[@id="thumbnail"]'
        )

        if len(videos) > index:

            # 🔥 scroll to video
            driver.execute_script(
                "arguments[0].scrollIntoView();",
                videos[index]
            )

            time.sleep(1)

            # 🔥 click video
            driver.execute_script(
                "arguments[0].click();",
                videos[index]
            )

            return True

        else:

            say_and_speak("Video not found")

            return False

    except Exception as e:

        print("Open video error:", e)

        say_and_speak("Failed to open video")

        return False

# =========================================================
# 🔥 COMMAND HANDLER (UNCHANGED LOGIC)
# =========================================================
def handle_youtube_controls(cmd):
    if "pause" in cmd or "resume" in cmd:
        youtube_play_pause()
        return "Toggled video"

    if "mute" in cmd or "unmute" in cmd:
        current = is_muted()
        youtube_mute()
        return "Unmuted" if current else "Muted"

    if "volume up" in cmd:
        youtube_volume_up()
        return "Volume increased"

    if "volume down" in cmd:
        youtube_volume_down()
        return "Volume decreased"

    if "next video" in cmd:
        youtube_next_video()
        return "Playing next video"

    if "skip ad" in cmd:
        youtube_skip_ad()
        return "Ad skipped"

    return None