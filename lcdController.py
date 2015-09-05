#!/home/pi/octoprint/venv/bin/python

from lcd import Lcd
from screens import *

import sys
import logging
import signal
import ScreenController

def handleKill(signum, frame):
    logging.critical("Killed!")
    sys.exit(130)

logging.basicConfig(format='[%(asctime)s][%(module)s][%(levelname)s]:%(message)s', level=logging.DEBUG, filename="/home/pi/lcdcontroller/log.txt")

logging.info("Starting ScreenController...")

signal.signal(signal.SIGINT, handleKill)
signal.signal(signal.SIGQUIT, handleKill)

try:
    ScreenController.start()
except:
   logging.exception('Got exception on main handler')
   raise
