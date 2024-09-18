import cv2
import sys
import time
from grblComm import GRBLComms
from yoloDet import Detection
from zaxis import ZAxisComms
from datetime import datetime


zAxisPort = "COM3"
PORT = "COM4"
BAUD_RATE = 115200
zAxisBaudRate = 9600
CROP_COORDINATES = (0, 285, 480, 640)
TROLLEY = [423, 480]
MODEL_PATH = "finalstrolley.pt"
CAPTURE_PATH = "./imgs/captured_image.jpg"
CROPPED_PATH = "./imgs/cropped_img.jpg"
outfile = './imgs/%s.jpg' % ('image' + str(datetime.now()))

OFFSET_THRESHOLD = 20  # Define your own offset value based on your requirements

camera = cv2.VideoCapture(0)
detection = Detection(MODEL_PATH)

prev_x, prev_y = None, None  # Initializing previous x and y to None
#use_secondary_detection = False  # Added this line
flag = False

#near corner coordinates x = 0 y =50
#opposite corner coordinates 
if __name__ == "__main__":
    grbl = GRBLComms(PORT, BAUD_RATE)
    zAxis = ZAxisComms(zAxisPort, zAxisBaudRate)
    grbl.connect() 
    time.sleep(2)
    zAxis.connect()
    time.sleep(2)
    print("ZAxis connected")
    grbl.enableHardLimit()
    grbl.homeMachine()
    grbl.disableHardLimit()


    dontStop = True
    while(dontStop):

        _, frame = camera.read()
        _, frame = camera.read()

        cv2.imwrite(CAPTURE_PATH, frame)
        cv2.imwrite(outfile, frame)
        print(f"Picture captured: {CAPTURE_PATH}")

        cropped_image_path = detection.crop_input_image(CAPTURE_PATH, CROPPED_PATH, CROP_COORDINATES)
        results = detection.predict(source=cropped_image_path, device="cpu")
        print(results)
        # Use the primary detection results[0] by default
        try:
            x, y = results[0]
        except:
            continue

        #detection.show_output_image((x, y))

        #time.sleep(1000000)
        # If using the secondary detection is preferred or the primary detection is too close to the previous one
        #if ((((prev_x is not None) and (prev_y is not None)) and ((abs(x - prev_x) < OFFSET_THRESHOLD) and (abs(y - prev_y) < OFFSET_THRESHOLD)))):
        if (flag == True):

            print("Using secondary detection")
            # Check if results[1] exists to avoid index out of range errors
            if len(results) > 1:
                x, y = results[1]
                #use_secondary_detection = False  # Reset it for the next round
            else:
                print("Secondary detection not found. Using primary detection.")

        #prev_x, prev_y = x, y  # Update the previous x and y after using them for comparison
        if (flag == True):
            flag = False
        else:
            flag = True
            
        x = x * 480
        y = y * (CROP_COORDINATES[3]- CROP_COORDINATES[1])
        #u = y * 382
        x = min(515, x)
        y = min(302, y)
        print("X: ", x, ", Y: ", y)
        detection.show_output_image((x, y))

        detection.cleanup()

        print("Picking up box ", x)

        grbl.moveMachine(x, y + 273)
        
        zAxis.pickup()
        """
        for remaining in range(8, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining. Attempting Pickup".format(remaining))
            sys.stdout.flush()
            time.sleep(1)   
        """
        print("\nGoing to DROPOFF")
        #grbl.homeMachine()
        grbl.moveMachine(400, 0)
        zAxis.drop()
    
    grbl.disconnect()
