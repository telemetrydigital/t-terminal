#!/bin/bash

log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/8: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/8: Inštalujem potrebné balíky pre kiosk mode..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xserver-xorg x11-xserver-utils xinit git matchbox-window-manager

log "3/8: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/8: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/8: Nastavujem oprávnenia pre tty a video..."
sudo usermod -aG tty pi
sudo usermod -aG video pi
sudo chmod 660 /dev/tty0
sudo chown root:tty /dev/tty0

log "6/8: Nastavujem režim kiosk mode..."
cat <<EOL > ~/.xinitrc
#!/bin/bash
xset -dpms        # Vypnutie šetriča obrazovky
xset s off        # Zakázanie úsporného režimu
xset s noblank    # Zakázanie zhasnutia obrazovky
matchbox-window-manager &  # Ľahký správca okien pre kiosk mode
/usr/bin/python3 /opt/tterminal/main.py  # Spustenie aplikácie TTerminal
EOL
chmod +x ~/.xinitrc

sudo bash -c "cat > /etc/systemd/system/kiosk.service" << 'EOF'
[Unit]
Description=Kiosk Mode
After=multi-user.target

[Service]
Environment=DISPLAY=:0
User=pi
Group=tty
ExecStart=/usr/bin/startx
Restart=always
StandardInput=tty
TTYPath=/dev/tty1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable kiosk

log "7/8: Vypínam štandardné desktopové prostredie..."
sudo systemctl set-default multi-user.target
sudo systemctl disable lightdm

log "8/8: Inštalácia dokončená! Po reštarte sa kiosk mode spustí automaticky."
read -p "Chcete reštartovať Raspberry Pi teraz? (y/n): " RESTART
if [[ "$RESTART" == "y" || "$RESTART" == "Y" ]]; then
  sudo reboot
else
  log "Reštart manuálne spustíte pomocou: sudo reboot"
fi
