# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import serial

serialPort = "/dev/ttyAMA0"

lcd = serial.Serial(serialPort)

class LcdController(octoprint.plugin.StartupPlugin):
	def on_after_startup(self):
		self._logger.info("Lcd Controller starting")
		lcd.write("?f")
		lcd.write("Octoprint Started")

__plugin_implementation__ = LcdCOntroller()
