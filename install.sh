#!/bin/bash

# Funkcia na zobrazenie logu
log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/7: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/7: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xinit xserver-xorg libqt5gui5 libqt5widgets5 libqt5x11extras5 git

log "3/7: Klonujem repozitár tterminal..."
if [ ! -d "/opt/tterminal" ]; then
  sudo git clone https://github.com/telemetrydigital/tterminal.git /opt/tterminal
else
  log "Repozitár už existuje. Aktualizujem..."
  cd /opt/tterminal && sudo git pull
fi

log "4/7: Inštalujem Python závislosti..."
sudo pip3 install -r /opt/tterminal/requirements.txt

log "5/7: Nastavujem prostredie Xorg pre Qt aplikáciu..."

# Nastavenie premenných prostredia pre Qt
echo "export DISPLAY=:0" >> ~/.bashrc
source ~/.bashrc

# Vytvorenie súboru .Xauthority, ak neexistuje
if [ ! -f ~/.Xauthority ]; then
  touch ~/.Xauthority
  sudo chown $USER:$USER ~/.Xauthority
fi

log "6/7: Nastavujem systémovú službu tterminal..."
SERVICE_FILE=/etc/systemd/system/tterminal.service
sudo bash -c "cat > $SERVICE_FILE <<EOL
[Unit]
Description=TTerminal Application
After=network.target

[Service]
ExecStart=/usr/bin/xinit /usr/bin/python3 /opt/tterminal/main.py -- :0
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL
"

log "Povoľujem službu tterminal..."
sudo systemctl daemon-reload
sudo systemctl enable tterminal
sudo systemctl start tterminal

log "7/7: Inštalácia dokončená! Po reštarte sa aplikácia spustí automaticky."

