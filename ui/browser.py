from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from backend.browser_settings import set_browser_url, get_browser_url

class BrowserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("Browser Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # URL Input
        url_label = QLabel("Kiosk Browser URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter the URL (e.g., https://example.com)")
        self.url_input.setText(get_browser_url())  # Načítanie aktuálneho nastavenia
        layout.addWidget(url_label)
        layout.addWidget(self.url_input)

        # Uložiť tlačidlo
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def save_settings(self):
        try:
            # Získať zadanú URL adresu
            url = self.url_input.text()
            if not url.startswith("http://") and not url.startswith("https://"):
                raise ValueError("Please enter a valid URL starting with http:// or https://")

            # Uložiť URL do backendu
            set_browser_url(url)

            # Zobraziť potvrdenie
            QMessageBox.information(self, "Success", "Browser URL saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save browser URL: {str(e)}")

