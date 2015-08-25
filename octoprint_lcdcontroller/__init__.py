# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import serial
from .lcd import Lcd

serialPort = "/dev/ttyAMA0"

#lcd = serial.Serial(serialPort)

lcd = Lcd()

class LcdController(octoprint.plugin.StartupPlugin):
	def on_after_startup(self):
		self._logger.info("Lcd Controller starting")
		lcd.clear()
		lcd.write("OctoPrint Started")

__plugin_implementation__ = LcdController()
