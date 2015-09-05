from lcd import Lcd
from screens import *

import logging
import Printer
import Hardware
import thread

lcd = Lcd()

screens = {
    "mainScreen": PrintScreen("mainScreen", "mainScreen", "Tricolour Mendel"), 
    "mainMenu": ListScreen("mainScreen", "mainMenu", "Tricolour Mendel"),
    "print": FuncScreen("mainMenu", "print", "Print"),
    "power": ListScreen("mainMenu", "power", "Power"),
    "files": FileScreen("mainMenu", "files", "Files"),
    "temperature": TempScreen("mainMenu", "temperature", "Temperature"),
    "move": ListScreen("mainMenu", "move", "Move"),
    "light": ListScreen("mainMenu", "light", "Light"),
    "camera": ListScreen("mainMenu", "camera", "Camera"),
    "file": FileInfoScreen("files", "file", "File"),
    "temp": TempChangeScreen("temperature", "temp", "Set Temp"),
    "printer": GpioScreen("power", "printer", "Printer Power"),
    "outlet": GpioScreen("power", "outlet", "Outlet Power")
}

curScreen = "mainScreen"
prevScreen = "mainScreen"

mainMenuOptions = [
    ["print", "Print"],
    ["power", "Power"],
    ["files", "Files"],
    ["temperature", "Temerature"],
    ["move", "Move"],
    ["filament", "Filament"],
    ["light", "Light"],
    ["camera", "Camera"]
]

powerOptions = [
    ["printer", "Printer"],
    ["outlet", "Outlet"]
]

printerOptions = [
    [["printer", 0], "On"],
    [["printer", 1], "Off"]
]

outletOptions = [
    [["outlet", 0], "On"],
    [["outlet", 1], "Off"]
]

printerFuntions = [
    [Printer.pprint, "Print"],
    [Printer.cancel, "Cancel"],
    [Printer.pause, "Pause / Resume"],
    [Printer.restart, "Restart"],
]

def start():
    
    logging.info("Starting...")

    global screens
    global curScreen
    global prevScreen
    
    screens["mainMenu"].setOptions(mainMenuOptions)
    screens["power"].setOptions(powerOptions)
    screens["print"].setOptions(printerFuntions)
    screens["printer"].setOptions(printerOptions)
    screens["outlet"].setOptions(outletOptions)

    logging.debug("Clearing LCD")
    lcd.clear()

    logging.debug("Initing Hardware")
    Hardware.init()
    
    logging.debug("Starting checkPrinter thread")
    thread.start_new_thread(checkPrinter, ())
    
    logging.info("Started")

    while(True):
        Hardware.update()
        if not curScreen == prevScreen:
            screens[curScreen].init()
            logging.info("Changing Screen to {}".format(curScreen))
            prevScreen = curScreen
        
        screens[curScreen].update()
        screens[curScreen].draw()
        curScreen = screens[curScreen].nextScreen()

def checkPrinter():

    while(True):
        try:
            Printer.update()
        except:
            logging.exception('Exception in checkPrinter thread')
            raise
