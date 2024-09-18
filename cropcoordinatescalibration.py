import cv2
import sys
import time
from grblComm import GRBLComms
from yoloDet import Detection
from PIL import Image, ImageDraw
import os

CROP_COORDINATES = (0, 285, 480, 640)
CAPTURE_PATH = "./imgs/captured_image.jpg"
CROPPED_PATH = "./imgs/cropped_img.jpg"

camera = cv2.VideoCapture(0)


def crop_input_image(input_image_path, output_image_path, crop_coordinates):
    input_img = Image.open(input_image_path)
    x1, y1, x2, y2 = crop_coordinates
    cropped_img = input_img.transpose(method=Image.Transpose.ROTATE_90)
    cropped_img = cropped_img.crop((x1, y1, x2, y2))

    cropped_img.save(output_image_path)

    return output_image_path

_, frame = camera.read()
cv2.imwrite(CAPTURE_PATH, frame)
print(f"Picture captured: {CAPTURE_PATH}")

cropped_image_path = crop_input_image(CAPTURE_PATH, CROPPED_PATH, CROP_COORDINATES)