# OctoPrint-LcdController

Control your OCtoprint Enabled 3d printer through an LCD and buttons!

This uses Octoprint's REST API to interface with Octoprint, Modern Device serial LCD, some buttons, and some leds, and a relay board. 

# Features
- Monitor current print status and time remaining
- Start / Stop / Pause / Restart prints
- Turn the power to the printer and a sperate outlet on and off through relays
- List files stored on the Pi and the printer's sd card
 - Load, Print, and Delete files
- Monitor and set bed and tool temperatures (Even for multiple tools!)

# Hardware

Requires
- [Modern Device serial LCD] (https://moderndevice.com/product/lcd117-serial-lcd-kit/)
- 6 buttons (Up, down, left, right, enter, back)
- 2 LEDs with resistors
- 2 Relay board for printer and outlet power(Optional)
- Wiring
- 3d printed mount (will be on Thingiverse)

Wire the LCD to +5v, ground, and serial TX on the Pi

Wire each of the buttons from their GPIO pin to ground as follows:

  up: 15
  down: 21
  left: 19
  right: 12
  enter: 13
  back: 16

Wire the LEDs through the resistors to their GPIO pin and ground, and wire the relay like [this](https://github.com/foosel/OctoPrint/wiki/Controlling-a-relay-board-from-your-RPi), but to the following pins:

led1: 22
led2: 18
printer relay: 7
outlet relay: 11

All pins can be changed in `Hardware.py`

# Usage & Installation

Install dependancies:
<pre>
sudo ~/OctoPrint/venv/bin/pip install hurry
</pre>

Clone from github
<pre>
cd ~
git clone https://github.com/chickenchuck040/OctoPrint-LcdController
</pre>

If it is not installed in `/home/pi/OctoPrint-LcdController`, you wil need to change the paths in `lcdController.py`, `Hardware.py`, and `lcd` appropriately

To run use `sudo ./lcd start`
To stop use `sudo ./lcd stop`

To run at startup
<pre>
sudo ./install.sh
</pre>

To turn the printer on or off from another program, write a `1` or `0` to `printerPower`.
For example,
<pre>
echo 1 > printerPower
</pre>

By default, a log is stored in `log.txt`. It can be changed in `lcdContoller.py`
By default, the serial port `/dev/ttyAMA0` is used for the display. It can be changed in `Lcd.py`
