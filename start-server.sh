#!/bin/bash

# How To Autostart Apps In Rasbian LXDE Desktop
# http://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/

echo "Starting Relay Controller server process"
/usr/bin/python3 /home/pi/pi-relay-controller-modmypi/server.py runserver -r