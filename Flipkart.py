import serial
import cv2
import time
import os
import sys
from grblComm import GRBLComms
from yoloDet import Detection

PORT = "COM7"
BAUD_RATE = 115200
camera = cv2.VideoCapture(0)

if __name__ == "__main__":
    grbl = GRBLComms(PORT, BAUD_RATE)
    grbl.connect()
    grbl.enableHardLimit()
    grbl.homeMachine()
    grbl.disableHardLimit()
    grbl.moveMachine(275, 20)

    dontStop = True
    boxNo = 1
    while(dontStop):

        
    
        detection = Detection("best_top.pt")
        crop_coordinates = (150, 0, 500, 481)
        trolley = [600,430]

        file_name = f"./imgs/captured_image.jpg"
        _, frame = camera.read()
        cv2.imwrite(file_name, frame)
        print(f"Picture captured: {file_name}")

        cropped_image_path = detection.crop_input_image(file_name, "./imgs/cropped_img.jpg", crop_coordinates)
        results = detection.predict(source=cropped_image_path, device="cuda")
        x, y = results[0]
        x = x*430
        y = y*600
        if (x>350):
            x = 350
        if(y>520):
            y = 520
        print("X: ", y, ", Y: ", x)
        detection.show_output_image((x,y))

            
        detection.cleanup()

        print("Picking up box ", x)
        grbl.moveMachine(y+ 45, x + 170)
        #time.sleep(20)
        for remaining in range(12, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
        
        print("\nGoing to DROPOFF")
        x = x + 1
        grbl.moveMachine(275, 20)
    
    grbl.disconnect()

