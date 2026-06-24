# =========================================================
# 🔥 Nova HOLOGRAM FINAL
# =========================================================

import sys
import os
import threading
import time
import psutil
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QUrl
from PyQt6.QtWebEngineCore import QWebEngineProfile
from browser import start_browser


from main_ai import process
import main_ai

from voice import set_ui_callback, listen, say_and_speak, stop_speech, is_speaking

# =========================================================
# 🔥 BRIDGE
# =========================================================


class Bridge(QObject):

    send_signal = pyqtSignal(str)
    system_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.view = None

        self.send_signal.connect(self._sendToUI)

        self.system_signal.connect(self._updateSystemUI)

    # =====================================================
    # 🔥 UI → PYTHON
    # =====================================================

    @pyqtSlot(str)
    def sendCommand(self, cmd):

        print("UI:", cmd)

        def run():

            try:

                result = process(cmd)

                # 🔥 voice.py already handles UI
                pass

            except Exception as e:

                self.send_signal.emit(f"Error: {e}")

        threading.Thread(target=run, daemon=True).start()

    # =====================================================
    # 🔥 SAFE UI SEND
    # =====================================================

    def sendToUI(self, msg):

        self.send_signal.emit(msg)

    # =====================================================
    # 🔥 MAIN THREAD UI UPDATE
    # =====================================================

    def _sendToUI(self, msg):

        if not self.view:
            return

        if msg == "LISTENING":

            self.view.page().runJavaScript("setListeningMode()")

            return

        if msg == "PROCESSING":

            self.view.page().runJavaScript("setProcessingMode()")

            return

        # 🔥 VOICE START
        if msg == "VOICE_START":

            self.view.page().runJavaScript("setSpeakingMode()")

            return

        # 🔥 VOICE STOP
        if msg == "VOICE_STOP":

            self.view.page().runJavaScript("setIdleMode()")

            return

        # 🔥 NORMAL MESSAGE
        if msg in ["LISTENING", "PROCESSING", "VOICE_START", "VOICE_STOP"]:
            return

        safe = msg.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")

        self.view.page().runJavaScript(f"addMessage('{safe}')")

    # =====================================================
    # 🔥 SYSTEM MONITOR
    # =====================================================

    def _updateSystemUI(self, data):

        if self.view:

            self.view.page().runJavaScript(f"updateSystemStats('{data}')")

    # =====================================================
    # 🔥 BACKGROUND MONITOR
    # =====================================================

    def start_system_monitor(self):

        def run():

            while True:

                try:

                    cpu = psutil.cpu_percent()

                    ram = psutil.virtual_memory().percent

                    try:

                        battery = psutil.sensors_battery()

                        battery = battery.percent if battery else "N/A"

                    except:

                        battery = "N/A"

                    data = f"{cpu}|{ram}|{battery}"

                    self.system_signal.emit(data)

                except:
                    pass

                time.sleep(1)

        threading.Thread(target=run, daemon=True).start()


# =========================================================
# 🔥 APP
# =========================================================

app = QApplication(sys.argv)

# 🔥 CLEAR WEB CACHE
profile = QWebEngineProfile.defaultProfile()

profile.clearHttpCache()

profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)

view = QWebEngineView()

view.setWindowTitle("Nova")

view.resize(1200, 700)


# =========================================================
# 🔥 Nova FLOATING HUD
# =========================================================

status_popup = QLabel()

status_popup.setGeometry(60, 18, 240, 52)

status_popup.setText("🟢 Nova ONLINE")

status_popup.setStyleSheet("""
QLabel{
    background: rgba(5, 10, 30, 190);
    color: #00F5FF;
    font-size: 18px;
    font-weight: bold;
    border: 2px solid #00F5FF;
    border-radius: 18px;
    padding: 12px 18px;
}
""")

status_popup.setAlignment(Qt.AlignmentFlag.AlignCenter)

status_popup.setWindowFlags(
    Qt.WindowType.FramelessWindowHint
    | Qt.WindowType.WindowStaysOnTopHint
    | Qt.WindowType.Tool
)

status_popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

status_popup.show()
status_popup.raise_()

# =========================================================
# 🔥 BRIDGE SETUP
# =========================================================

channel = QWebChannel()

bridge = Bridge()

bridge.view = view
main_ai.bridge = bridge

channel.registerObject("bridge", bridge)

view.page().setWebChannel(channel)


def show_status(text):

    status_popup.setText(text)

    if not status_popup.isVisible():

        status_popup.show()


# =========================================================
# 🔥 LOAD HTML
# =========================================================

path = os.path.abspath("index.html")

if not os.path.exists(path):

    print("❌ index.html not found")

    sys.exit()

view.load(QUrl.fromLocalFile(path))


# =========================================================
# 🔥 UI LOADED
# =========================================================


def on_load_finished():

    print("✅ UI Loaded")

    bridge.start_system_monitor()

    # =========================================================
    # 🔥 START VOICE THREAD
    # =========================================================

    threading.Thread(target=voice_loop, daemon=True).start()


view.loadFinished.connect(on_load_finished)


# =========================================================
# 🔥 UI CALLBACK
# =========================================================


def ui_callback(sender, msg):

    bridge.sendToUI(msg)

    # =====================================================
    # 🔥 FLOATING HUD STATUS
    # =====================================================

    if msg == "LISTENING":

        if status_popup.text() != "🎤 LISTENING":
            show_status("🎤 LISTENING")

    elif msg == "PROCESSING":

        if status_popup.text() != "⚡ PROCESSING":
            show_status("⚡ PROCESSING")

    elif msg == "VOICE_START":

        if status_popup.text() != "🗣️ SPEAKING":
            show_status("🗣️ SPEAKING")

    elif msg == "VOICE_STOP":

        show_status("🟢 Nova ONLINE")


set_ui_callback(ui_callback)


# =========================================================
# 🔥 WAKE WORDS
# =========================================================

WAKE_WORDS = ["nova", "innova", "novaa", "nov", "noba", "no va"]


# =========================================================
# 🔥 VOICE LOOP
# =========================================================

# =========================================================
# 🔥 VOICE LOOP
# =========================================================


def voice_loop():

    bridge.sendToUI("Waiting for wake word...")

    while True:

        cmd = listen()

        # ✅ Empty — skip
        if not cmd:
            continue

        print("VOICE:", cmd)

        # ✅ Interrupt — stop speech aur skip
        if any(
            x in cmd
            for x in [
                "stop",
                "stop speaking",
                "shut up",
                "bas",
                "chup",
                "stop nova",
                "ruko",
            ]
        ):
            print("🔥 INTERRUPT DETECTED")
            stop_speech()
            continue

        # ✅ Seedha process karo — wake word
        #    listen() already handle kar chuka hai
        def run(c=cmd):
            try:
                process(c)
            except Exception as e:
                print("PROCESS ERROR:", e)

        threading.Thread(target=run, daemon=True).start()


# =========================================================
# 🔥 RUN APP
# =========================================================

view.show()

sys.exit(app.exec())
