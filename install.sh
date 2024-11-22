#!/bin/bash

# Funkcia na zobrazenie logu
log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/5: Aktualizujem systém..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/5: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 wireguard-tools git wget

log "3/5: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/5: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/5: Nastavujem tterminal službu..."
SERVICE_FILE=/etc/systemd/system/tterminal.service
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=TTerminal Application
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/tterminal/main.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable tterminal.service

log "Pridávam predvolený konfiguračný súbor..."
CONFIG_DIR=/etc/tterminal
if [ ! -d "\$CONFIG_DIR" ]; then
  sudo mkdir -p \$CONFIG_DIR
  sudo cp /opt/tterminal/default_config.json \$CONFIG_DIR/config.json
fi

log "Spúšťam službu tterminal..."
sudo systemctl start tterminal.service

log "Inštalácia dokončená! Reštartujte Raspberry Pi pre kompletné spustenie."
