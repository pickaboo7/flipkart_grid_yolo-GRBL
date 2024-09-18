from ultralytics import YOLO
from PIL import Image
import shutil
import os
import serial
import cv2
import time

# Set the correct serial port and baud rate
ser = serial.Serial('COM7', 9600)  # Use 'COM6' or the appropriate port on your laptop

# Initialize the camera
camera = cv2.VideoCapture(0)  # Adjust the camera index as needed

# Flag to track the switch state
switch_state = False

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cuda"):
        results = self.model.predict(source=source, save=True, device=device)
        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()
            confidence = (r.boxes.conf).tolist()

        centroids = [[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates]
        return centroids

    def crop_input_image(self, input_image_path, output_image_path, crop_coordinates):
        input_img = Image.open(input_image_path)
        x1, y1, x2, y2 = crop_coordinates
        cropped_img = input_img.crop((x1, y1, x2, y2))
        cropped_img.save(output_image_path)
        return output_image_path  # Return the path to the cropped image

    def show_output_image(self):
        output_img = Image.open("./runs/segment/predict/cropped_img.jpg")
        output_img.show()

    def cleanup(self):
        shutil.rmtree("./runs")


if __name__ == "__main__":
    detection = Detection("best.pt")

    # Define the coordinates to crop the input image (x1, y1, x2, y2)
    crop_coordinates = (150, 0 , 500, 481)

    while True:
        data = ser.readline().decode().strip()

        if data == "Switch Pressed" and not switch_state:
            switch_state = True  # Set the switch state to pressed

        if data == "Switch Released" and switch_state:
            # The switch is released, stop capturing
            switch_state = False  # Set the switch state to released

        if switch_state:
            # Capture a picture continuously
            file_name = f"./imgs/captured_image.jpg"
            _, frame = camera.read()
            cv2.imwrite(file_name, frame)
            print(f"Picture captured: {file_name}")

            # Crop the input image based on predefined coordinates and get the path to the cropped image
            cropped_image_path = detection.crop_input_image(file_name, "./imgs/cropped_img.jpg", crop_coordinates)

            # Perform YOLO detection on the cropped image
            results = detection.predict(source=cropped_image_path, device="cuda")
            print(results)

            # Show the YOLO output image
            detection.show_output_image()

            # Cleanup temporary files
            detection.cleanup()

        time.sleep(0.1)
