from ultralytics import YOLO
from PIL import Image
import shutil
import cv2

class Detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, source, device="cpu"):
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

camera = cv2.VideoCapture(1)
# Usage:
if __name__ == "__main__":
    detection = Detection("best_top.pt")
    
    trolley = [600,430]
    # Define the coordinates to crop the input image (x1, y1, x2, y2)
    crop_coordinates = (150, 0, 500, 481)

    file_name = f"img9.jpg"
    _, frame = camera.read()
    cv2.imwrite(file_name, frame)
    print(f"Picture captured: {file_name}")

    cropped_image_path = detection.crop_input_image(file_name, "./imgs/cropped_img.jpg", crop_coordinates)
    results = detection.predict(source=cropped_image_path, device="cpu")
    results = detection.predict(source="img9.jpg", device="cpu")
    print(results)
    x, y = results[0]
    print(x*430, y*600)
    
    # Show the YOLO output image
    detection.show_output_image()

    # Cleanup temporary files
    detection.cleanup()
