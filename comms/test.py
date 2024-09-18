import serial
import time
from PIL import Image, ImageDraw
import cv2

PORT = "COM4"
BAUD_RATE = 115200

class GRBLComms:
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        self.state = False # for Z-axis toggle
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudRate, timeout=1)
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
    
    def waitForMovementCompletion(self, message="Idle"):
        time.sleep(1)
        idleCounter = 0

        while True:
            self.connection.reset_input_buffer()
            
            self.sendCommand('?')
            response = self.connection.readline().strip().decode()

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
            

    def homeMachine(self):
        print(f'Homing machine')
        self.sendCommand("$H")
        self.waitForMovementCompletion(message="ok")

    def moveMachine(self, x, y):
        print(f'Moving machine to X:{x}, Y:{y}')

        self.sendCommand(f'G00 X{x} Y{y}')

        self.waitForMovementCompletion()
        
        print(f'reached X:{x} Y:{y}')
        return True

    def goToDropOff(self):
        self.moveMachine(275, 20)
            
    def wakeupMachine(self):
        self.connection.write(b"\r\n\r\n")
        time.sleep(2)
        self.connection.flushInput()

    def isIdle(self):
        response = grbl.sendCommand("?")
        if 'Idle' in response:
            return True
        return False
    
    def ZaxisRoutine(self):
        if self.state:
            self.sendCommand("M3 S0") # can also be changed to "M5"
        else:
            self.sendCommand("M3 S1000")
        self.state = not self.state
        time.sleep(1) # this will require some fine tuning

    def disableHardLimit(self):
        self.sendCommand('$21 = 0')

    def enableHardLimit(self):
        self.sendCommand('$21 = 1')

    def setZOff(self):
        self.state = False
        self.sendCommand("M3 S0")

    def crop_input_image(self, input_image_path, output_image_path, crop_coordinates):
        input_img = Image.open(input_image_path)
        x1, y1, x2, y2 = crop_coordinates
        cropped_img = input_img.crop((x1, y1, x2, y2))
        cropped_img.save(output_image_path)
        return output_image_path

    def show_output_image(self,result):
        output_img = Image.open("./runs/segment/predict/cropped_img.jpg")
        draw = ImageDraw.Draw(output_img)
        print("Result: ", result)
        x, y = result
        draw.ellipse([x-5, y-5, x+5, y+5], fill='blue')

camera = cv2.VideoCapture(1)

if __name__ == "__main__":
    CAPTURE_PATH = "./imgs/captured_image.jpg"
    CROPPED_PATH = "./imgs/cropped_img.jpg"
    _, frame = camera.read()
    cv2.imwrite(CAPTURE_PATH, frame)
    print(f"Picture captured: {CAPTURE_PATH}")
    try:
        grbl = GRBLComms(PORT, BAUD_RATE)
        grbl.connect()

        grbl.homeMachine()
        grbl.moveMachine(200, 50)

        grbl.disconnect()

    except KeyboardInterrupt:
        grbl.disconnect()
