#!/bin/bash

log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/7: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/7: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xserver-xorg x11-xserver-utils xinit git chromium-browser

log "3/7: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/7: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/7: Vytváram súbor s URL pre kiosk mód..."
echo "https://example.com" > /opt/tterminal/kiosk_url.txt

log "6/7: Vytváram spúšťaciu službu..."
sudo bash -c "cat > /etc/systemd/system/start_mode.service" << 'EOF'
[Unit]
Description=TTerminal Start Mode
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

log "7/7: Inštalácia dokončená! Po reštarte sa spustí výber režimu."
read -p "Chcete reštartovať Raspberry Pi teraz? (y/n): " RESTART
if [[ "$RESTART" == "y" || "$RESTART" == "Y" ]]; then
  sudo reboot
else
  log "Reštart manuálne spustíte pomocou: sudo reboot"
fi
