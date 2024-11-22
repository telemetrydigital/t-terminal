from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QPushButton, QMessageBox
)
from backend.display_settings import set_resolution, set_rotation, toggle_cursor

class DisplayPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("Display Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Nastavenie rozlíšenia
        resolution_label = QLabel("Resolution:")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "480x272", "800x480", "1024x600", "1280x800"
        ])
        layout.addWidget(resolution_label)
        layout.addWidget(self.resolution_combo)

        # Nastavenie rotácie
        rotation_label = QLabel("Rotation:")
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems([
            "0°", "90°", "180°", "270°"
        ])
        layout.addWidget(rotation_label)
        layout.addWidget(self.rotation_combo)

        # Skrytie/zobrazenie kurzora
        self.cursor_checkbox = QCheckBox("Hide Cursor")
        layout.addWidget(self.cursor_checkbox)

        # Tlačidlo na uloženie nastavení
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def save_settings(self):
        try:
            # Získať nastavenia z widgetov
            resolution = self.resolution_combo.currentText()
            rotation = self.rotation_combo.currentText()
            hide_cursor = self.cursor_checkbox.isChecked()

            # Volanie backend funkcií
            set_resolution(resolution)
            set_rotation(rotation)
            toggle_cursor(hide_cursor)

            # Zobrazenie potvrdenia
            QMessageBox.information(self, "Success", "Display settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save display settings: {str(e)}")

