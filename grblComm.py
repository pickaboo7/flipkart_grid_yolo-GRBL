import serial
import time
import sys

class GRBLComms:
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        self.state = False # for Z-axis toggle
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudRate)
        self.wakeupMachine()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        
        print("Machine disconnected successfuly")

    def sendCommand(self, command):
        if not self.connection:
            raise Exception("GRBL is not connected!")
        
        self.connection.write(f"{command}\r\n".encode())
        #print("Command sent")
    
    def waitForMovementCompletion(self, message="Idle"):
    
        time.sleep(1)
        idleCounter = 0

        while True:
            self.connection.reset_input_buffer()
            
            self.sendCommand('?')
            response = self.connection.readline().strip().decode()
            #print(response)
            # when homing checks for "ok"
            if response == message:
                break

            # when moving to (x, y) checks for "Idle"
            if response != 'ok':
                # print(response)
                if 'Idle' in response:
                    # machine has reached desired location
                    idleCounter += 1

            if idleCounter >= 10:
                # count no of times machine reported to be idle
                break
        return
        """
        for remaining in range(25, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining. Attempting Pickup".format(remaining))
            sys.stdout.flush()
            time.sleep(1)   

        return
        """

    def homeMachine(self):
        print(f'Homing machine')
        self.sendCommand("$H")
        self.waitForMovementCompletion()

    def moveMachine(self, x, y):
        print(f'Moving machine to X:{x}, Y:{y}')

        self.sendCommand(f'G00 X{x} Y{y}')

        self.waitForMovementCompletion()
        
        print(f'reached X:{x} Y:{y}')
        return True

    def goToDropOff(self):
        self.moveMachine(270, 20)
            
    def wakeupMachine(self):
        self.connection.write(b"\r\n\r\n")
        time.sleep(2)
        self.connection.flushInput()

    def isIdle(self):
        response = self.sendCommand("?")
        if 'Idle' in response:
            return True
        return False
    
    def disableHardLimit(self):
        self.sendCommand('$21 = 0')

    def enableHardLimit(self):
        self.sendCommand('$21 = 1')
    
    def ZaxisRoutine(self):
        if self.state:
            self.sendCommand("M3 S0") # can also be changed to "M5"
        else:
            self.sendCommand("M3 S1000")
        self.state = not self.state
        time.sleep(1) # this will require some fine tuning

    def setZOff(self):
        self.state = False
        self.sendCommand("M3 S0")


if __name__ == "__main__":
    try:
        grbl = GRBLComms("COM4", 115200)
        grbl.connect()
        time.sleep(2)
        grbl.homeMachine()
        grbl.disableHardLimit()
        grbl.moveMachine(520, 520)
        # grbl.moveMachine(100, 300)
        # grbl.moveMachine(500, 200)


    except KeyboardInterrupt:
        grbl.disconnect()