from lcd import Lcd
from hurry import filesize

import logging
import math
import time
import datetime
import Printer
import Hardware

class Screen():
    'Base screen'
    
    lcd = Lcd()
    
    lines = [[" " for i in range(0, 20)] for k in range(0, 4)]

    screenId = "mainScreen"
    previousId = "mainScreen"

    title = ""

    def __init__(self, pid, sid, t):
        self.previousId = pid
        self.screenId = sid
        self.title = t
        self.lines = [[" " for i in range(0, 20)] for k in range(0, 4)]
    
    def init(self):
        self.lcd.clear()
    
    def update(self):
        self.lines[0] = list(str(self.title).center(self.lcd.width))
        self.lines[1] = list(str(time.strftime("%I:%M:%S")))
    
    def nextScreen(self):
        return self.screenId

    def draw(self):
        for line in range(0, self.lcd.height):
            self.lcd.setCur(0, line)
            self.lcd.write("".join(self.lines[line]))

class PrintScreen(Screen):
    'Screen to display print info'
    
    lines = [[" " for i in range(0, 20)] for k in range(0, 4)]

    def update(self):
        self.lines[0] = list(str(self.title).center(self.lcd.width))
        self.lines[1] = list(str(Printer.state).ljust(self.lcd.width))
        
        if not Printer.cfile == None:
            self.lines[2] = list(str(Printer.cfile).ljust(self.lcd.width))
        else:
            self.lines[2] = list("                    ")
    
        if not Printer.printTimeLeft == None:
            m, s = divmod(int(Printer.printTimeLeft), 60)
            h, m = divmod(m, 60)
            self.lines[3] = list(str("%02d:%02d:%02d" % (h, m, s)).ljust(self.lcd.width))
        else:
            self.lines[3] = list("                    ")
    
    def nextScreen(self):
        if Hardware.buttons["enter"]:
            return "mainMenu"
        else:
            return self.screenId

class ListScreen(Screen):
    'A list of options'
    
    lines = [[" " for i in range(0, 20)] for k in range(0, 4)]
    
    options = [[]]
    
    curPos = 0
    scrPos = 0
    selPos = 0

    def init(self):
        self.curPos = 0
        self.scrPos = 0
        self.selPos = 0
        Screen.init(self)

    def setOptions(self, options):
        self.options = options
    
    def update(self):
        self.lines[0] = list(str(self.title).center(self.lcd.width))
        
        if Hardware.buttons["up"] and self.curPos > 0:
            self.curPos = self.curPos - 1
            if self.curPos < self.scrPos:
                self.scrPos = self.scrPos - 1
            else:
                self.selPos = self.selPos - 1
        if Hardware.buttons["down"] and self.curPos < len(self.options)-1:
            self.curPos = self.curPos + 1
            if self.curPos > self.scrPos + self.lcd.height - 2:
                self.scrPos = self.scrPos + 1
            else:
                self.selPos = self.selPos + 1
        
        for i in range(0, self.lcd.height-1):
            if i+self.scrPos <= len(self.options)-1:
                if i == self.selPos:
                    self.lines[i+1] = (">%s" % self.options[i+self.scrPos][1]).ljust(self.lcd.width)
                else:
                    self.lines[i+1] = (" %s" % self.options[i+self.scrPos][1]).ljust(self.lcd.width)

    def nextScreen(self):
        if Hardware.buttons["back"]:
            return self.previousId
        elif Hardware.buttons["enter"]:
            return self.options[self.curPos][0]
        else:
            return self.screenId
class GpioScreen(ListScreen):
    'List Gpio Operations'
    
    def update(self):
        ListScreen.update(self)
        if Hardware.buttons["enter"]:
            Hardware.outputs[self.options[self.curPos][0][0]] = self.options[self.curPos][0][1]

    def nextScreen(self):
        if Hardware.buttons["back"]:
            return self.previousId
        else:
            return self.screenId
    
        
class FuncScreen(ListScreen):
    'List network opertations'
    
    def update(self):
        ListScreen.update(self)
        if Hardware.buttons["enter"]:
            self.options[self.curPos][0]()

    def nextScreen(self):
        if Hardware.buttons["back"]:
            return self.previousId
        else:
            return self.screenId
        

class TempScreen(Screen):
    'Show temperatures'

    tools = []
    tool = 0

    def update(self):
        self.lines[0] = list(self.title.center(self.lcd.width))
        
        self.tools = []

        for t in Printer.temperatures:
            self.tools.append(t)

        self.tools.sort()

        ptool = ""
        for t in self.tools:
            i = self.tools.index(t)
            if i % 2 == 0:
                ptool = t
            else:
                s1 = ' '
                s2 = ' '

                if self.tool == i-1:
                    s1 = '>'
                if self.tool == i:
                    s2 = '>'

                a1 = int(Printer.temperatures[ptool]["actual"])
                t1 = int(Printer.temperatures[ptool]["target"])
                l1 = "{}{}{}{: >3d}/{: <3d}".format(s1, ptool[0].upper(), ptool[-1].upper(), a1, t1)
                
                a2 = int(Printer.temperatures[t]["actual"])
                t2 = int(Printer.temperatures[t]["target"])
                l2 = "{}{}{}{: >3d}/{: <3d}".format(s2, t[0].upper(), t[-1].upper(), a2, t2)

                self.lines[1+int(math.floor(self.tools.index(t)/2))] = list("%s%s" % (l1,  l2))
        
        if Hardware.buttons["up"] and self.tool > 1:
            self.tool = self.tool - 2
        if Hardware.buttons["down"] and self.tool < len(self.tools)-2:
            self.tool = self.tool + 2
        if Hardware.buttons["left"] and self.tool > 0:
            self.tool = self.tool - 1
        if Hardware.buttons["right"] and self.tool < len(self.tools)-1:
            self.tool = self.tool + 1

        Printer.tmpTool = self.tools[self.tool]
            
        
    def nextScreen(self):
        if Hardware.buttons["back"]:
            return self.previousId
        elif Hardware.buttons["enter"]:
            return "temp"
        else:
            return self.screenId
    
class TempChangeScreen(Screen):
    'Change a temperature'
    
    temp = 0

    def init(self):
        Screen.init(self)
        self.tool = Printer.tmpTool
        self.temp = int(Printer.temperatures[self.tool]["target"])

    def update(self):
        self.lines[0] = list(self.tool.center(self.lcd.width))
        self.lines[1] = list("+10".center(self.lcd.width))
        self.lines[2] = list("-1 {: =3d} +1".format(self.temp).center(self.lcd.width))
        self.lines[3] = list("-10".center(self.lcd.width))

        if Hardware.buttons["up"]:
            self.temp = self.temp + 10
        if Hardware.buttons["down"]:
            self.temp = self.temp - 10
        if Hardware.buttons["left"]:
            self.temp = self.temp - 1
        if Hardware.buttons["right"]:
            self.temp = self.temp + 1
        if Hardware.buttons["enter"]:
            Printer.setTemp(self.tool, self.temp)

    def nextScreen(self):
        if Hardware.buttons["back"] or Hardware.buttons["enter"]:
            return self.previousId
        else:
            return self.screenId

        
class FileScreen(ListScreen):
    'List the files on the printer'
    
    def update(self):
        i = 0
        
        self.options = []
        if "files" in Printer.files:
            for f in Printer.files["files"]:
                self.options.append(["file", f["name"]])
                i = i + 1
        
        ListScreen.update(self)
        Printer.tmpFile = self.curPos

class FileInfoScreen(Screen):
    'Display info about a file'
    
    pos = 0
    
    def update(self):
        f = Printer.files["files"][Printer.tmpFile]
        self.lines[0] = f["name"].center(20)
        
        time = []
        size = []
        date = []
        orig = []
        
        if "gcodeAnalysis" in f and not f["gcodeAnalysis"]["estimatedPrintTime"] == None:
            m, s = divmod(int(f["gcodeAnalysis"]["estimatedPrintTime"]), 60)
            h, m = divmod(m, 60)
            time = list(str("%02d:%02d:%02d" % (h, m, s)).center(self.lcd.width/2))
        else:
            time = list("".center(self.lcd.width/2))
        
        if not f["size"] == None:
            s = filesize.size(int(str(f["size"])))
            size = list(str(s).center(self.lcd.width/2))
        else:
            size = list("".center(self.lcd.width/2))
        
        if not f["date"] == None:
            d = datetime.datetime.fromtimestamp(int(f["date"])).strftime('%m/%d/%Y')
            date = list(d.center(self.lcd.width/2))
        else:
            date = list("".center(self.lcd.width/2))
        
        if not f["origin"] == None:
            orig = list(str(f["origin"]).center(self.lcd.width/2))
        else:
            orig = list("".center(self.lcd.width/2))

        self.lines[1] = time+date
        self.lines[2] = size+orig
        
        self.lines[3] = list(" Print  Load  Delete")
        
        if Hardware.buttons["right"] and self.pos < 3:
            self.pos = self.pos + 1
        if Hardware.buttons["left"] and self.pos > -1:
            self.pos = self.pos - 1
        
        if self.pos == 0:
            self.lines[3][0] = '>'

        
class FileScreen(ListScreen):
    'List the files on the printer'
    
    def update(self):
        i = 0
        
        self.options = []
        for f in Printer.files["files"]:
            self.options.append(["file", f["name"]])
            i = i + 1
        
        ListScreen.update(self)
        Printer.tmpFile = self.curPos

class FileInfoScreen(Screen):
    'Display info about a file'
    
    pos = 0
    
    def update(self):
        f = Printer.files["files"][Printer.tmpFile]
        self.lines[0] = f["name"].center(20)
        
        time = []
        size = []
        date = []
        orig = []
        
        if "gcodeAnalysis" in f and not f["gcodeAnalysis"]["estimatedPrintTime"] == None:
            m, s = divmod(int(f["gcodeAnalysis"]["estimatedPrintTime"]), 60)
            h, m = divmod(m, 60)
            time = list(str("%02d:%02d:%02d" % (h, m, s)).center(self.lcd.width/2))
        else:
            time = list("".center(self.lcd.width/2))
        
        if not f["size"] == None:
            s = filesize.size(int(str(f["size"])))
            size = list(str(s).center(self.lcd.width/2))
        else:
            size = list("".center(self.lcd.width/2))
        
        if not f["date"] == None:
            d = datetime.datetime.fromtimestamp(int(f["date"])).strftime('%m/%d/%Y')
            date = list(d.center(self.lcd.width/2))
        else:
            date = list("".center(self.lcd.width/2))
        
        if not f["origin"] == None:
            orig = list(str(f["origin"]).center(self.lcd.width/2))
        else:
            orig = list("".center(self.lcd.width/2))

        self.lines[1] = time+date
        self.lines[2] = size+orig
        
        self.lines[3] = list(" Print  Load  Delete")
        
        if Hardware.buttons["right"] and self.pos < 3:
            self.pos = self.pos + 1
        if Hardware.buttons["left"] and self.pos > -1:
            self.pos = self.pos - 1
        
        if self.pos == 0:
            self.lines[3][0] = '>'
        elif self.pos == 1:
            self.lines[3][7] = '>'
        elif self.pos == 2:
            self.lines[3][13] = '>'
        else:
            self.pos = 0
            self.lines[3][0] = '>'
        
        if Hardware.buttons["enter"]:
            if self.pos == 0:
                Printer.selectFile(f["name"], f["origin"], True)
            elif self.pos == 1:
                Printer.selectFile(f["name"], f["origin"], False)
            elif self.pos == 2:
                Printer.deleteFile(f["name"], f["origin"])
        
    def nextScreen(self):
        if Hardware.buttons["back"] or Hardware.buttons["enter"]:
            return self.previousId
        else:
            return self.screenId
    
