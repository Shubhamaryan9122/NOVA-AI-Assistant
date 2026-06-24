# =========================================================
# 🔥 SYSTEM CONTROL
# =========================================================

# ✅ SAARE IMPORTS UPAR — EK BAAR
import os
import subprocess
import time
import ctypes
import psutil
import pyautogui
import shutil
import winreg        
import glob 

from functools import lru_cache

# =========================================================
# 🔥 DYNAMIC APP FINDER
# =========================================================

# Registry keys jahan Windows installed apps store karta hai
REGISTRY_PATHS = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths",
]

def search_registry(app_name):
    """Windows registry mein app dhundo"""
    app_name_lower = app_name.lower()

    for reg_path in REGISTRY_PATHS:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                reg_path
            )
            count = winreg.QueryInfoKey(key)[0]

            for i in range(count):
                try:
                    sub_name = winreg.EnumKey(key, i)

                    # App name match karo
                    if app_name_lower in sub_name.lower():
                        sub_key = winreg.OpenKey(key, sub_name)
                        path, _ = winreg.QueryValueEx(sub_key, "")

                        if path and os.path.exists(path):
                            return path

                except:
                    continue

            winreg.CloseKey(key)

        except:
            continue

    return None


def search_start_menu(app_name):
    """Start Menu shortcuts mein app dhundo"""
    app_name_lower = app_name.lower()

    # Start Menu locations
    start_menus = [
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    ]

    for menu in start_menus:
        # Saare .lnk files dhundo
        pattern = os.path.join(menu, "**", "*.lnk")
        shortcuts = glob.glob(pattern, recursive=True)

        for shortcut in shortcuts:
            name = os.path.basename(shortcut).lower()
            name = name.replace(".lnk", "")

            if app_name_lower in name:
                return shortcut  # .lnk path return karo

    return None


def resolve_shortcut(lnk_path):
    """Windows .lnk shortcut ka actual exe path nikalo"""
    try:
        import ctypes.wintypes

        # PowerShell se shortcut resolve karo
        cmd = f'powershell -command "(New-Object -ComObject WScript.Shell).CreateShortcut(\'{lnk_path}\').TargetPath"'

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=5
        )

        path = result.stdout.strip()

        if path and os.path.exists(path):
            return path

    except:
        pass

    return None


def search_common_locations(app_name):

    app_name_lower = app_name.lower()

    common_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
        os.path.expandvars(r"%APPDATA%"),
    ]

    for base_dir in common_dirs:

        if not os.path.exists(base_dir):
            continue

        try:

            for root, dirs, files in os.walk(base_dir):

                root_lower = root.lower()

    # ⚡ Fast filter
                if app_name_lower not in root_lower:
                    continue

                for file in files:

                    if (
                        file.lower().endswith(".exe")
                        and app_name_lower in file.lower()
                    ):

                        exe_path = os.path.join(
                            root,
                            file
                        )

                        print(
                            f"✅ Found in recursive search: {exe_path}"
                        )

                        return exe_path

        except Exception as e:

            print(
                f"Search Error ({base_dir}): {e}"
            )

            continue

    return None

@lru_cache(maxsize=50)  # ✅ Result cache — baar baar search nahi karega
def find_app_dynamic(app_name):
    """
    4 methods se app dhundo:
    1. PATH mein (shutil.which)
    2. Windows Registry mein
    3. Start Menu shortcuts mein
    4. Common install folders mein
    """
    print(f"🔍 Searching for: {app_name}")

    # Method 1 — PATH
    found = shutil.which(app_name)
    if found:
        print(f"✅ Found in PATH: {found}")
        return found

    # Method 2 — Registry
    found = search_registry(app_name)
    if found:
        print(f"✅ Found in Registry: {found}")
        return found

    # Method 3 — Start Menu
    lnk = search_start_menu(app_name)
    if lnk:
        found = resolve_shortcut(lnk)
        if found:
            print(f"✅ Found in Start Menu: {found}")
            return found
        # .lnk directly bhi try karo
        return lnk

    # Method 4 — Common folders
    found = search_common_locations(app_name)
    if found:
        print(f"✅ Found in common dirs: {found}")
        return found

    print(f"❌ Not found: {app_name}")
    return None

# =========================================================
# 🔥 OPEN APP
# =========================================================

def open_app(cmd):

    cmd = cmd.lower().strip()
    cmd = cmd.replace("vs code", "vscode")
    cmd = cmd.replace("visual studio code", "vscode")

    if not cmd.startswith("open "):
        return None

    app_name = cmd.replace("open ", "").strip()

    # 🌐 Websites ko app search se skip karo
    WEBSITES = {
        "youtube",
        "google",
        "gmail",
        "facebook",
        "instagram",
        "github",
        "chatgpt",
        "whatsapp",
        "new tab"
    }

    if app_name in WEBSITES:
        return None

    search_names = [
        app_name,
        app_name.replace(" ", "")
    ]
    if app_name.split():
        search_names.append(
            app_name.split()[0]
        )

    for name in search_names:

        path = find_app_dynamic(name)

        if not path:
            continue

        try:

            print(f"🚀 Launching: {path}")

            subprocess.Popen(
                path,
                shell=True
            )

            return f"Opening {app_name}"

        except Exception as e:

            print(f"❌ Launch Error: {e}")

    return f"Could not open {app_name}"


# =========================================================
# 🔥 CLOSE APP
# =========================================================

PROTECTED = {
    "explorer",
    "system",
    "svchost",
    "wininit",
    "csrss",
    "services"
}


def close_app(cmd):

    cmd = cmd.lower().strip()

    if not cmd.startswith("close "):
        return None

    app_name = cmd.replace("close ", "").strip()

    killed = False

    for proc in psutil.process_iter(["pid", "name"]):

        try:

            proc_name = proc.info["name"]

            if not proc_name:
                continue

            proc_name = proc_name.lower()
            proc_name = proc_name.replace(".exe", "")

            if proc_name in PROTECTED:
                continue

            if app_name in proc_name:

                proc.kill()

                print(f"Killed: {proc.info['name']}")

                killed = True

        except Exception:
            continue

    if killed:
        return f"Closing {app_name}"

    return f"{app_name} is not running"

# =========================================================
# 🔥 VOLUME CONTROL
# =========================================================

def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")
        time.sleep(0.05)
    return "Volume increased"


def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")
        time.sleep(0.05)
    return "Volume decreased"


def mute_volume():
    pyautogui.press("volumemute")
    return "Volume muted"


# =========================================================
# 🔥 LOCK SCREEN
# =========================================================

def lock_screen():
    ctypes.windll.user32.LockWorkStation()
    return "Locking screen"


# =========================================================
# 🔥 POWER CONTROL
# =========================================================

pending_action = None


def shutdown_pc():
    global pending_action
    pending_action = "shutdown"
    return "Are you sure? Say yes to confirm shutdown"


def restart_pc():
    global pending_action
    pending_action = "restart"
    return "Are you sure? Say yes to confirm restart"


def confirm_power_action(cmd):
    global pending_action

    if cmd != "yes":
        return None

    if pending_action == "shutdown":
        os.system("shutdown /s /t 1")
        pending_action = None
        return "Shutting down"

    if pending_action == "restart":
        os.system("shutdown /r /t 1")
        pending_action = None
        return "Restarting"

    return None


# =========================================================
# 🔥 OPEN FOLDER
# =========================================================

def open_folder(cmd):

    cmd = cmd.lower().strip()

    folders = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "desktop":   os.path.join(os.path.expanduser("~"), "Desktop"),
        "pictures":  os.path.join(os.path.expanduser("~"), "Pictures"),
        "videos":    os.path.join(os.path.expanduser("~"), "Videos"),
        "music":     os.path.join(os.path.expanduser("~"), "Music")
    }

    for name, path in folders.items():
        if cmd == f"open {name}":
            try:
                subprocess.Popen(f'explorer "{path}"')
                return f"Opening {name}"
            except Exception as e:
                print("Folder open error:", e)
                return f"Unable to open {name}"

    return None