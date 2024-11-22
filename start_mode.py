import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt

# Funkcia na načítanie konfigurácie
def load_config():
    try:
        with open("/opt/tterminal/default_config.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Chyba pri načítaní konfigurácie: {e}")
        return {}

# Funkcia na spustenie Chromium v kiosk režime
def start_kiosk_mode(url):
    os.system(f"chromium-browser --kiosk --app={url}")
    sys.exit()

# Funkcia na spustenie aplikácie tterminal
def start_tterminal():
    os.system("/usr/bin/python3 /opt/tterminal/main.py")
    sys.exit()

# Hlavné okno pre tlačidlo Settings
class StartModeWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TTerminal")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Stlačte 'Settings' na konfiguráciu", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton("Settings", self)
        self.button.clicked.connect(start_tterminal)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # Časovač na automatické spustenie kiosk režimu
        timeout = self.config.get("settings_button_timeout", 10) * 1000
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: start_kiosk_mode(self.config.get("kiosk_url", "https://www.example.com")))
        self.timer.start(timeout)

# Hlavný spúšťač
if __name__ == "__main__":
    config = load_config()
    app = QApplication(sys.argv)
    window = StartModeWindow(config)
    window.show()
    sys.exit(app.exec_())
