import cv2
import numpy as np
import math

def get_angle(width, height):
    # Calculate the angle using arctangent
    angle_rad = math.atan(height / width)
    
    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

def resize_window(image, scale_percent):
    # Get the screen resolution
    screen_width, screen_height = 1920, 1080  # Update with your screen resolution or use a method to get it dynamically

    # Calculate the new width and height for the window
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    # Resize the window
    cv2.namedWindow('Detected Rectangular Box', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detected Rectangular Box', width, height)

def detect_rectangular_box(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Resize the window to fit into a quarter of the screen
    scale_percent = 25
    resize_window(image, scale_percent)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has four vertices, it is likely a rectangular box
        if len(approx) == 4:
            # Draw the contour and bounding box
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(approx)
            
            # Get the angle of the box
            angle = get_angle(w, h)

            # Display the angle on the image
            cv2.putText(image, f"Angle: {angle:.2f} degrees", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow('Detected Rectangular Box', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Specify the path to your image
image_path = 'img69.jpg'

# Perform object detection on the image
detect_rectangular_box(image_path)
