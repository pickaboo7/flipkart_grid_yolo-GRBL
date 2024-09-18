import serial
import cv2
import time
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw
import shutil
import numpy as np

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cuda"):
        results = self.model.predict(source=source, save=True, device=device)
        for r in results:
            coordinates = (r.boxes.xyxyn).tolist()
            conf_values = (r.boxes.conf).tolist()
            box_xywhs = (r.boxes.xywh).tolist()

        area = [w * h for x, y, w, h in box_xywhs]
        print("Areas", area)

        for i in range(len(coordinates)):
            if(conf_values[i] < 0.8):
                coordinates = coordinates[:i]
                conf_values = conf_values[:i]
                area = area[:i]
                break

        
        #print("Coordinates before sort", coordinates)
        print("Area after clipping", area)
        print("Conf values ", conf_values)
        coordinates_new = [x for y, x in sorted(zip(area, coordinates), reverse=True)]
        conf_values_new = [x for y, x in sorted(zip(area, conf_values), reverse=True)]
        print("Conf values after sort ", conf_values_new)
        #print("Coordinates after sort", coordinates_new)
        centroids = [[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in coordinates_new]
        return centroids

    def crop_input_image(self, input_image_path, output_image_path, crop_coordinates):
        input_img = Image.open(input_image_path)
        x1, y1, x2, y2 = crop_coordinates
        cropped_img = input_img.transpose(method=Image.Transpose.ROTATE_90)
        cropped_img = cropped_img.crop((x1, y1, x2, y2))
        cropped_img.save(output_image_path)
        return output_image_path

    def show_output_image(self,result):
        output_img = Image.open("./runs/segment/predict/cropped_img.jpg")
        draw = ImageDraw.Draw(output_img)
        print("Result: ", result)
        x, y = result
        draw.ellipse([x-5, y-5, x+5, y+5], fill='blue')
        #output_img = np.asarray(output_img)
        #dot_radius = 5
        #dot_color = (0, 255, 0)  # Red color in BGR
        #thickness = -1  # This will fill the circle
        #output_img = cv2.circle(output_img, (int(result[0]), int(result[1])), dot_radius, dot_color, thickness)
        #output_img = Image.fromarray(output_img)

        output_img.show()

    def cleanup(self):
        shutil.rmtree("./runs")
        os.remove("./imgs/captured_image.jpg")
        os.remove("./imgs/cropped_img.jpg")