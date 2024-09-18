import cv2 
import time

camera = cv2.VideoCapture(0)
i = 102
while(True):
    i += 1
    file_name = f"./data/imgCap_{i}.jpg"
    _, frame = camera.read()
    cv2.imwrite(file_name, frame)
    print(f"Picture captured: {file_name}")
    time.sleep(10)

