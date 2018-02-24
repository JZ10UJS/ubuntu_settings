#!/bin/sh

# remove liboffice
sudo apt-get remove -y libreoffice*.*
# remove amazon 
sudo apt purge -y ubuntu-web-launchers

sudo apt-get update
sudo apt-get install -y python-dev python-pip python3-dev git openssh-server vim libsodium-dev


# set the proxy 
export SS_DIR=/etc/shadowsocksr/shadowsocks
sudo cp -r shadow-socks/shadowsocksr /etc

sudo cp shadow-socks/shadowsocks.service /lib/systemd/system/
sudo systemctl enable shadowsocks.service
sudo systemctl start shadowsocks.service

gsettings set org.gnome.system.proxy mode 'auto'
gsettings set org.gnome.system.proxy autoconfig-url file://${SS_DIR}/auto.pac
echo 'Set Proxy auto'
