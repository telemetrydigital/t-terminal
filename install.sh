#!/bin/bash

# Funkcia na zobrazenie logu
log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/6: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/6: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xinit xserver-xorg libqt5gui5 libqt5widgets5 libqt5x11extras5 git

log "3/6: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/6: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/6: Nastavujem automatické prihlásenie a spustenie aplikácie..."

# Povolenie automatického prihlásenia
sudo raspi-config nonint do_boot_behaviour B4  # Desktop Autologin

# Vytvorenie priečinka pre autostart
mkdir -p ~/.config/autostart

# Vytvorenie autostart súboru pre aplikáciu
AUTOSTART_FILE=~/.config/autostart/tterminal.desktop
cat <<EOL > $AUTOSTART_FILE
[Desktop Entry]
Type=Application
Name=TTerminal
Exec=/usr/bin/python3 /opt/tterminal/main.py
X-GNOME-Autostart-enabled=true
EOL

log "6/6: Inštalácia dokončená! Po reštarte sa aplikácia spustí automaticky."

# Reštart systému
read -p "Chcete reštartovať Raspberry Pi teraz? (y/n): " RESTART
if [[ "$RESTART" == "y" || "$RESTART" == "Y" ]]; then
  sudo reboot
else
  log "Reštart manuálne spustíte pomocou: sudo reboot"
fi
