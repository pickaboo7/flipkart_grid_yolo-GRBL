import cv2
import sys
import time
from grblComm import GRBLComms
from yoloDet import Detection
from PIL import Image, ImageDraw
import os

PORT = "COM4"
BAUD_RATE = 115200
CROP_COORDINATES = (0, 25, 480, 411)

TROLLEY = [480, 480]
MODEL_PATH = "best_top.pt"
CAPTURE_PATH = "./imgs/captured_image.jpg"
CROPPED_PATH = "./imgs/cropped_img.jpg"
OFFSET_THRESHOLD = 20  # Define your own offset value based on your requirements

#image top left corner, x = 0, y = 50
#image bottom right corner x = 
camera = cv2.VideoCapture(0)

def crop_input_image(input_image_path, output_image_path, crop_coordinates):
    input_img = Image.open(input_image_path)
    x1, y1, x2, y2 = crop_coordinates
    cropped_img = input_img.transpose(method=Image.Transpose.ROTATE_90)
    cropped_img = cropped_img.crop((x1, y1, x2, y2))

    cropped_img.save(output_image_path)

    return output_image_path

def show_output_image(result, CROPPED_PATH):    
    output_img = Image.open(CROPPED_PATH)
    #utput_img = output_img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    #output_img = output_img.transpose(method=Image.Transpose.ROTATE_90)
    draw = ImageDraw.Draw(output_img)
    print("Result: ", result)
    x, y = result
    draw.ellipse([x-5, y-5, x+5, y+5], fill='blue')
    output_img.show()


def cleanup():
    #shutil.rmtree("./runs")
    os.remove("./imgs/captured_image.jpg")
    os.remove("./imgs/cropped_img.jpg")

def goto(x, y):
    y = y * 406
    x = x * 480


    x = min(515, x)
    y = min(420, y)

    print("X: ", x, ", Y: ",y)
    show_output_image((x, y), CROPPED_PATH)


    print("Picking up box ", x)
    grbl.moveMachine(x, y + 50)
    cleanup()

    for remaining in range(8, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining. Attempting Pickup".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    print("\nGoing to DROPOFF")
    grbl.moveMachine(275, 20)

#near corner coordinates x = 0 y =50
#opposite corner coordinates 
if __name__ == "__main__":
    grbl = GRBLComms(PORT, BAUD_RATE)
    grbl.connect()  
    # grbl.enableHardLimit()
    grbl.homeMachine()
    # grbl.disableHardLimit()

    dontStop = True
    i = 0
    coordinates = [(0, 0), (0.25, 0), (0.5,0.5), (0, 0.25), (1,1)]
    while(dontStop):

        

        _, frame = camera.read()
        cv2.imwrite(CAPTURE_PATH, frame)
        print(f"Picture captured: {CAPTURE_PATH}")

        cropped_image_path = crop_input_image(CAPTURE_PATH, CROPPED_PATH, CROP_COORDINATES)
        x, y = coordinates[i]

        goto(x, y)

        i = (i + 1) % len(coordinates)
    grbl.disconnect()
