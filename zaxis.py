import serial
import time
import sys
class ZAxisComms:
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        self.connection = None
    
    def connect(self):
        self.connection = serial.Serial(self.port, self.baudRate)
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        
        print("Z axis arduino disconnected sucessfully")
    
    def pickup(self):
        self.sendCommand("pickup")

    def drop(self):
        self.sendCommand("drop")

    def sendCommand(self, command):
        if not self.connection:
            raise Exception("Z axis arduino not connected")
        self.connection.write(f"{command}\n".encode())
        response = self.connection.readline().decode()

        if response == "invalid":
            raise Exception("Invalid command sent")
        elif response == "done":
            return

if __name__ == "__main__":
    try:
        zAxis = ZAxisComms("COM3", 9600)
        zAxis.connect()
        time.sleep(2)

        zAxis.pickup()
        print("Dropoff")
        
        for remaining in range(10, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining. Attempting Pickup".format(remaining))
            sys.stdout.flush()
            time.sleep(1)   

        zAxis.drop()
    except KeyboardInterrupt:   
        zAxis.disconnect()
