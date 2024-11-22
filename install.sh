#!/bin/bash

# Funkcia na zobrazenie logu
log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/7: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/7: Inštalujem potrebné balíky pre kiosk mode..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xserver-xorg x11-xserver-utils xinit git matchbox-window-manager

log "3/7: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/7: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/7: Nastavujem kiosk mode..."

# Vytvorenie `.xinitrc` pre kiosk mode
cat <<EOL > ~/.xinitrc
#!/bin/bash
xset -dpms        # Vypnutie šetriča obrazovky
xset s off        # Zakázanie úsporného režimu
xset s noblank    # Zakázanie zhasnutia obrazovky
matchbox-window-manager &  # Ľahký správca okien pre kiosk mode
/usr/bin/python3 /opt/tterminal/main.py  # Spustenie aplikácie TTerminal
EOL
chmod +x ~/.xinitrc

log "6/7: Nastavujem automatické spúšťanie Xorg..."
# Úprava služby pre automatické spúšťanie Xorg
sudo bash -c "cat > /etc/systemd/system/kiosk.service" << 'EOF'
[Unit]
Description=Kiosk Mode
After=multi-user.target

[Service]
Environment=DISPLAY=:0
User=pi
ExecStart=/usr/bin/startx
Restart=always

[Install]
WantedBy=graphical.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable kiosk.service

log "7/7: Inštalácia dokončená! Po reštarte sa kiosk mode spustí automaticky."

# Ponuka na reštart
read -p "Chcete reštartovať Raspberry Pi teraz? (y/n): " RESTART
if [[ "$RESTART" == "y" || "$RESTART" == "Y" ]]; then
  sudo reboot
else
  log "Reštart manuálne spustíte pomocou: sudo reboot"
fi
