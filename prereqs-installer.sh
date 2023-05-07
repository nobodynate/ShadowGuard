#!/bin/bash

# Install prerequisites
# Taken from mfmjos's fork of chasing_your_tail

# Install Kismet
wget https://www.kismetwireless.net/repos/kismet-release.gpg.key | sudo apt-key add -
echo "deb https://www.kismetwireless.net/repos/apt/release/$(lsb_release -cs) $(lsb_release -cs) main" |sudo tee /etc/apt/sources.list.d/kismet.list
sudo apt-get update
sudo apt-get install kismet

# Add your user to the kismet group
sudo usermod -aG kismet `whoami`

# Add interface capture sources to Kismet config file
kismetSiteConf="/etc/kismet/kismet_site.conf"
echo source=wlan0 | sudo tee -a $kismetSiteConf
echo source=wlan1 | sudo tee -a $kismetSiteConf
echo source=hci0 | sudo tee -a $kismetSiteConf

# Create logging directory
mkdir $HOME/kismet_logs

# Change default Kismet logging directory
echo log_prefix=$HOME/kismet_logs/ | sudo tee -a /etc/kismet/kismet_logging.conf

# Autostart the GUI, Kismet, and enable monitor mode at boot
autostartFile="/etc/xdg/autostart/display.desktop"
echo "[Desktop Entry]" | sudo tee -a $autostartFile
echo "Name=cyt_gui" | sudo tee -a $autostartFile
echo "Exec=$HOME/Desktop/cyt_gui.sh" | sudo tee -a $autostartFile
echo "@reboot sleep 30 && /home/pi/Desktop/cyt/wlan1_to_mon.sh &" | sudo tee -a $autostartFile
echo "@reboot sleep 60 && /usr/bin/kismet &" | sudo tee -a $autostartFile

echo "Prereq installer complete. Please reboot now"