from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from backend.vpn_settings import apply_vpn_config, disable_vpn

class VPNPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("VPN Settings (WireGuard)")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Input pre cestu ku konfiguračnému súboru
        config_label = QLabel("VPN Configuration File:")
        self.config_path_input = QLineEdit()
        self.config_path_input.setPlaceholderText("Path to WireGuard configuration file (e.g., wg0.conf)")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_config_file)
        layout.addWidget(config_label)
        layout.addWidget(self.config_path_input)
        layout.addWidget(browse_button)

        # Tlačidlo na aplikáciu VPN konfigurácie
        apply_button = QPushButton("Apply VPN Configuration")
        apply_button.clicked.connect(self.apply_vpn)
        layout.addWidget(apply_button)

        # Tlačidlo na deaktiváciu VPN
        disable_button = QPushButton("Disable VPN")
        disable_button.clicked.connect(self.disable_vpn)
        layout.addWidget(disable_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def browse_config_file(self):
        # Dialóg na výber súboru
        config_file, _ = QFileDialog.getOpenFileName(self, "Select VPN Configuration File", "", "Config Files (*.conf)")
        if config_file:
            self.config_path_input.setText(config_file)

    def apply_vpn(self):
        try:
            config_path = self.config_path_input.text()
            if not config_path:
                raise ValueError("Please provide a valid configuration file path.")

            # Volanie backend funkcie na aplikovanie VPN
            apply_vpn_config(config_path)

            # Zobrazenie potvrdenia
            QMessageBox.information(self, "Success", "VPN configuration applied successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply VPN configuration: {str(e)}")

    def disable_vpn(self):
        try:
            # Volanie backend funkcie na vypnutie VPN
            disable_vpn()

            # Zobrazenie potvrdenia
            QMessageBox.information(self, "Success", "VPN disabled successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to disable VPN: {str(e)}")

