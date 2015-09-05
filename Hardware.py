import logging
import RPi.GPIO as gpio

buttons = {"up": False, "down": False, "left": False, "right": False, "enter": False, "back": False}
outputs = {"red": False, "green": False, "printer": False, "outlet": False}

bPins = {"up": 15, "down": 21, "left": 19, "right": 12, "enter": 13, "back": 16}
oPins = {"red": 22, "green": 18, "printer": 7, "outlet": 11}

def init():

    logging.info("Setting up GPIO...")
    gpio.setwarnings(False)

    gpio.setmode(gpio.BOARD)

    gpio.setup(bPins["up"], gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(bPins["down"], gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(bPins["left"], gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(bPins["right"], gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(bPins["enter"], gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(bPins["back"], gpio.IN, pull_up_down=gpio.PUD_UP)

    gpio.setup(oPins["red"], gpio.OUT)
    gpio.setup(oPins["green"], gpio.OUT)
    gpio.setup(oPins["printer"], gpio.OUT)
    gpio.setup(oPins["outlet"], gpio.OUT)

    gpio.add_event_detect(bPins["up"], gpio.RISING)
    gpio.add_event_detect(bPins["down"], gpio.RISING)
    gpio.add_event_detect(bPins["left"], gpio.RISING)
    gpio.add_event_detect(bPins["right"], gpio.RISING)
    gpio.add_event_detect(bPins["enter"], gpio.RISING)
    gpio.add_event_detect(bPins["back"], gpio.RISING)
    
    logging.info("Done setting up GPIO")

def update():
    pin = "up"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    pin = "down"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    pin = "left"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    pin = "right"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    pin = "enter"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    pin = "back"
    if gpio.event_detected(bPins[pin]):
        buttons[pin] = True
    else:
        buttons[pin] = False

    outputs["green"] = not outputs["printer"]    
    outputs["red"] = not outputs["outlet"]

    pin = "red"
    gpio.output(oPins[pin], outputs[pin])

    pin = "green"
    gpio.output(oPins[pin], outputs[pin])
    
    f = open("/home/pi/lcdcontroller/printerPower", "r+")
    p = f.read()

    if p.find("1") > -1:
        outputs["printer"] = True
        f.seek(0)
        f.write(" ")
    elif p.find("0") > -1:
        outputs["printer"] = False
        f.seek(0)
        f.write(" ")
    
    pin = "printer"
    gpio.output(oPins[pin], outputs[pin])

    pin = "outlet"
    gpio.output(oPins[pin], outputs[pin])
