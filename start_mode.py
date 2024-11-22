import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

# Funkcia na spustenie Chromium v kiosk móde
def start_kiosk_mode():
    with open("/opt/tterminal/kiosk_url.txt", "r") as file:
        url = file.read().strip()
    os.system(f"chromium-browser --noerrdialogs --disable-infobars --kiosk {url}")
    sys.exit()

# Funkcia na spustenie aplikácie tterminal
def start_tterminal():
    os.system("/usr/bin/python3 /opt/tterminal/main.py")
    sys.exit()

# Hlavné okno
class StartModeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TTerminal Start")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Logo a text
        self.label = QLabel("Welcome to TTerminal", self)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Tlačidlo Settings
        self.button = QPushButton("Settings")
        self.button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.button.clicked.connect(start_tterminal)
        layout.addWidget(self.button)

        # Časovač na automatické spustenie kiosk módu
        self.timer = QTimer(self)
        self.timer.timeout.connect(start_kiosk_mode)
        self.timer.start(5000)  # 5 sekúnd na stlačenie tlačidla

        self.setLayout(layout)

# Spustenie aplikácie
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartModeWindow()
    window.show()
    sys.exit(app.exec_())
