import serial
import cv2
import time
from ultralytics import YOLO
from PIL import Image
import shutil
import * from comms.test

# GRBL Arduino Connection
ser_grbl = serial.Serial('COM8', 115200)  # Adjust COM port for GRBL Arduino

# Switch Arduino Connection
ser_switch = serial.Serial('COM7', 9600)  # Adjust COM port for Switch Arduino

# Initialize the camera
camera = cv2.VideoCapture(0)

# Flag to track the switch state
switch_state = False

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cuda"):
        results = self.model.predict(source=source, save=True, device=device)
        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()

        centroids = [[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates]
        return centroids

    def crop_input_image(self, input_image_path, output_image_path, crop_coordinates):
        input_img = Image.open(input_image_path)
        x1, y1, x2, y2 = crop_coordinates
        cropped_img = input_img.crop((x1, y1, x2, y2))
        cropped_img.save(output_image_path)
        return output_image_path

    def show_output_image(self):
        output_img = Image.open("./runs/segment/predict/cropped_img.jpg")
        output_img.show()

    def cleanup(self):
        shutil.rmtree("./runs")



if __name__ == "__main__":
    detection = Detection("best.pt")
    crop_coordinates = (150, 0, 500, 481)
    trolley = [600,430]

    while True:
        data = ser_switch.readline().decode().strip()

        if data == "Switch Pressed" and not switch_state:
            switch_state = True

        if data == "Switch Released" and switch_state:
            switch_state = False

        if switch_state:
            file_name = f"./imgs/captured_image.jpg"
            _, frame = camera.read()
            cv2.imwrite(file_name, frame)
            print(f"Picture captured: {file_name}")

            cropped_image_path = detection.crop_input_image(file_name, "./imgs/cropped_img.jpg", crop_coordinates)
            results = detection.predict(source=cropped_image_path, device="cuda")
            result = [a * b for a, b in zip(results[0], trolley)]
            print(result)
            detection.show_output_image()

            
            detection.cleanup()

        time.sleep(0.1)
