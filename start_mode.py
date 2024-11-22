import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt

# Funkcia na spustenie Chromium v kiosk režime
def start_kiosk_mode():
    try:
        with open("/opt/tterminal/kiosk_url.txt", "r") as file:
            url = file.read().strip()
        os.system(f"chromium-browser --kiosk --app={url}")
    except Exception as e:
        print(f"Chyba pri načítaní URL: {e}")
    sys.exit()

# Funkcia na spustenie aplikácie tterminal
def start_tterminal():
    os.system("/usr/bin/python3 /opt/tterminal/main.py")
    sys.exit()

# Hlavné okno pre tlačidlo Settings
class StartModeWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        self.timer = QTimer(self)
        self.timer.timeout.connect(start_kiosk_mode)
        self.timer.start(10000)  # 10 sekúnd

# Hlavný spúšťač
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartModeWindow()
    window.show()
    sys.exit(app.exec_())
