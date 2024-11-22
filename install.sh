#!/bin/bash

# Funkcia na zobrazenie logu
log() {
  echo -e "[\033[1;32mINFO\033[0m] $1"
}

log "1/8: Aktualizujem systémové balíky..."
sudo apt-get update -y && sudo apt-get upgrade -y

log "2/8: Inštalujem potrebné balíky..."
sudo apt-get install -y python3 python3-pip python3-pyqt5 xorg xinit xserver-xorg libqt5gui5 libqt5widgets5 libqt5x11extras5 git

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
# Pridanie používateľa pi do potrebných skupín
sudo usermod -aG tty pi
sudo usermod -aG video pi

# Nastavenie oprávnení pre /dev/tty0
sudo chmod 660 /dev/tty0
sudo chown root:tty /dev/tty0

log "6/8: Nastavujem prostredie Xorg pre Qt aplikáciu..."
# Nastavenie premenných prostredia pre Qt
echo "export DISPLAY=:0" >> ~/.bashrc
source ~/.bashrc

# Vytvorenie súboru .Xauthority, ak neexistuje
if [ ! -f ~/.Xauthority ]; then
  touch ~/.Xauthority
  sudo chown $USER:$USER ~/.Xauthority
fi

log "7/8: Nastavujem systémovú službu tterminal..."
SERVICE_FILE=/etc/systemd/system/tterminal.service
sudo bash -c "cat > $SERVICE_FILE" << 'EOF'
[Unit]
Description=TTerminal Application
After=network.target

[Service]
ExecStart=/usr/bin/xinit /usr/bin/python3 /opt/tterminal/main.py -- :0 vt1
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

log "Povoľujem službu tterminal..."
sudo systemctl daemon-reload
sudo systemctl enable tterminal
sudo systemctl start tterminal

log "8/8: Inštalácia dokončená! Po reštarte sa aplikácia spustí automaticky."
