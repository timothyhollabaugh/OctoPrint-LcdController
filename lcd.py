import serial

port = "/dev/ttyAMA0"

ser = serial.Serial("/dev/ttyAMA0")

class Lcd():
    
    width = 20
    height = 4
    
    def write(self, data):
        ser.write(data.encode())
    def clear(self):
        ser.write("?f")
    def setCur(self, x, y):
        if(x <= self.width and x >= 0):
            ser.write("?x"+"{:0>2d}".format(x))
        if(y <= self.height and y >= 0):
            ser.write("?y"+"{:0>1d}".format(y))
    
