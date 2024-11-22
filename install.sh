#!/bin/bash

log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/8: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/8: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xserver-xorg x11-xserver-utils xinit git chromium-browser

log "3/8: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/8: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/8: Vytváram predvolený konfiguračný súbor default_config.json..."
cat <<EOL > /opt/tterminal/default_config.json
{
    "kiosk_url": "https://www.example.com",
    "settings_button_timeout": 10,
    "time_format": "HH:mm:ss",
    "timezone": "Europe/Bratislava",
    "language": "en",
    "network": {
        "ethernet_ip": "192.168.1.100",
        "ethernet_gateway": "192.168.1.1",
        "wifi_ssid": "",
        "wifi_password": "",
        "can_baudrate": 500000,
        "can_address": 1
    },
    "display": {
        "resolution": "800x480",
        "rotation": 0,
        "hide_cursor": false
    },
    "vpn": {
        "wireguard_peer": "peer1",
        "wireguard_address": "10.0.0.2"
    },
    "system": {
        "shutdown_time": 1800,
        "auto_restart": true
    }
}
EOL

log "6/8: Vytváram spúšťací skript start_mode.py..."
cat <<EOL > /opt/tterminal/start_mode.py
import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt

CONFIG_FILE = "/opt/tterminal/default_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"kiosk_url": "https://www.example.com", "settings_button_timeout": 10}
    except json.JSONDecodeError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def start_kiosk_mode(url):
    os.system(f"chromium-browser --kiosk --app={url}")
    sys.exit()

def start_tterminal():
    os.system("/usr/bin/python3 /opt/tterminal/main.py")
    sys.exit()

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

        timeout = self.config.get("settings_button_timeout", 10) * 1000
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: start_kiosk_mode(self.config.get("kiosk_url", "https://www.example.com")))
        self.timer.start(timeout)

if __name__ == "__main__":
    config = load_config()
    app = QApplication(sys.argv)
    window = StartModeWindow(config)
    window.show()
    sys.exit(app.exec_())
EOL

log "7/8: Vytváram službu start_mode.service pre automatické spustenie..."
sudo bash -c "cat > /etc/systemd/system/start_mode.service" << 'EOF'
[Unit]
Description=Spúšťací režim TTerminal
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /opt/tterminal/start_mode.py
User=pi
Environment=DISPLAY=:0
Restart=always

[Install]
WantedBy=graphical.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable start_mode

log "8/8: Inštalácia dokončená! Po reštarte sa spustí správny režim podľa tlačidla."
read -p "Chcete reštartovať Raspberry Pi teraz? (y/n): " RESTART
if [[ "$RESTART" == "y" || "$RESTART" == "Y" ]]; then
  sudo reboot
else
  log "Reštart manuálne spustíte pomocou: sudo reboot"
fi

