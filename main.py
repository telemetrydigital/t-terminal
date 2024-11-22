import sys
import json
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

# Cesta k súboru s konfiguráciou
CONFIG_FILE = "/opt/tterminal/default_config.json"

# Funkcia na načítanie konfigurácie
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Ak súbor neexistuje, vráti predvolenú konfiguráciu
        return {
            "kiosk_url": "https://www.example.com",
            "settings_button_timeout": 10
        }
    except json.JSONDecodeError as e:
        print(f"Chyba pri načítaní konfigurácie: {e}")
        return {}

# Funkcia na uloženie konfigurácie
def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"Chyba pri ukladaní konfigurácie: {e}")

# Sekcia nastavení URL pre kiosk režim
class BrowserSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Zadajte URL pre kiosk režim:", self)
        layout.addWidget(self.label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://example.com")
        layout.addWidget(self.url_input)

        self.save_button = QPushButton("Uložiť URL", self)
        self.save_button.clicked.connect(self.save_url)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_current_url()

    def load_current_url(self):
        config = load_config()
        self.url_input.setText(config.get("kiosk_url", ""))

    def save_url(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Chyba", "URL adresa nemôže byť prázdna!")
            return

        config = load_config()
        config["kiosk_url"] = url
        save_config(config)

        QMessageBox.information(self, "Úspech", "URL adresa bola úspešne uložená.")

# Sekcia nastavení času (príklad ďalšieho modulu)
class TimeSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Nastavenie času a dátumu (príklad)", self)
        layout.addWidget(self.label)

        # Možno pridať ďalšie widgety pre nastavenie času
        self.setLayout(layout)

# Hlavné okno aplikácie
class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TTerminal")
        self.resize(800, 600)

        # Pridanie sekcií ako záložiek
        self.addTab(BrowserSettings(), "Browser")  # Nastavenie URL pre kiosk
        self.addTab(TimeSettings(), "Time")       # Nastavenie času
        # Možno pridať ďalšie sekcie: Network, Display, VPN, About...

# Spu

