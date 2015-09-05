#!/bin/sh

cd /home/pi/lcdcontroller

echo "start.sh" > out.txt

/home/pi/octoprint/venv/bin/python lcdController.py