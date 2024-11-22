from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QMessageBox
)
from backend.system_settings import set_settings_button_timeout

class SystemPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("System Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Timeout pre tlačidlo Settings
        timeout_label = QLabel("Settings Button Timeout (in seconds):")
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(3, 10)  # Povolené hodnoty: 3 až 10 sekúnd
        self.timeout_spinbox.setValue(self.get_current_timeout())
        layout.addWidget(timeout_label)
        layout.addWidget(self.timeout_spinbox)

        # Tlačidlo na uloženie nastavení
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def get_current_timeout(self):
        """
        Načítanie aktuálneho timeoutu zo systému (napojené na backend).
        """
        try:
            from backend.system_settings import get_settings_button_timeout
            return get_settings_button_timeout()
        except Exception:
            return 3  # Predvolená hodnota, ak sa niečo pokazí

    def save_settings(self):
        """
        Uloženie timeoutu pre tlačidlo Settings.
        """
        try:
            timeout = self.timeout_spinbox.value()
            set_settings_button_timeout(timeout)

            # Zobrazenie potvrdenia
            QMessageBox.information(self, "Success", "System settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save system settings: {str(e)}")

