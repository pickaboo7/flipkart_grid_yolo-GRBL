import time

from GRBL import GRBLComms
from zaxis import ZAxisComms

grblBaudRate = 115200
zAxisBaudRate = 9600

grblPort = "COM3"
zAxisPort = "COM4"

grbl = GRBLComms(grblPort, grblBaudRate)
zAxis = ZAxisComms(zAxisPort, zAxisBaudRate)

# connecting to serial
grbl.connect()
time.sleep(2)
print("GRBL connected")

zAxis.connect()
time.sleep(2)
print("ZAxis connected")

grbl.homeMachine()

# go to pickup point
grbl.moveMachine(300, 400)

# pickup box
zAxis.pickup()

# go to drop location
grbl.goToDropOff()

# drop box
zAxis.drop()

time.sleep(3)
zAxis.disconnect()
grbl.disconnect()