from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QComboBox, QMessageBox
)
from backend.network_settings import configure_ethernet, configure_wifi, configure_can

class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("Network Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Ethernet nastavenia
        ethernet_label = QLabel("Ethernet Settings:")
        layout.addWidget(ethernet_label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP Address (e.g., 192.168.1.100)")
        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Subnet Mask (e.g., 255.255.255.0)")
        self.gateway_input = QLineEdit()
        self.gateway_input.setPlaceholderText("Gateway (e.g., 192.168.1.1)")
        self.dhcp_checkbox = QCheckBox("Enable DHCP")
        layout.addWidget(self.ip_input)
        layout.addWidget(self.mask_input)
        layout.addWidget(self.gateway_input)
        layout.addWidget(self.dhcp_checkbox)

        # Wi-Fi nastavenia
        wifi_label = QLabel("Wi-Fi Settings:")
        layout.addWidget(wifi_label)

        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("Wi-Fi SSID")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wi-Fi Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.ssid_input)
        layout.addWidget(self.password_input)

        # CAN nastavenia
        can_label = QLabel("CAN Interface Settings:")
        layout.addWidget(can_label)

        self.can_address_input = QLineEdit()
        self.can_address_input.setPlaceholderText("CAN Address")
        self.can_speed_combo = QComboBox()
        self.can_speed_combo.addItems(["125000", "250000", "500000", "1000000"])  # CAN rýchlosti v bps
        layout.addWidget(self.can_address_input)
        layout.addWidget(self.can_speed_combo)

        # Uložiť tlačidlo
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def save_settings(self):
        try:
            # Ethernet
            ip = self.ip_input.text()
            mask = self.mask_input.text()
            gateway = self.gateway_input.text()
            dhcp_enabled = self.dhcp_checkbox.isChecked()

            configure_ethernet(ip, mask, gateway, dhcp_enabled)

            # Wi-Fi
            ssid = self.ssid_input.text()
            password = self.password_input.text()
            if ssid:
                configure_wifi(ssid, password)

            # CAN
            can_address = self.can_address_input.text()
            can_speed = self.can_speed_combo.currentText()
            if can_address and can_speed:
                configure_can(can_address, can_speed)

            # Zobrazenie potvrdenia
            QMessageBox.information(self, "Success", "Network settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save network settings: {str(e)}")

