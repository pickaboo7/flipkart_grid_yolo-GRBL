import cv2
import numpy as np

def find_rotation_angle(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img_copy = img.copy()

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (presumably the box)
    largest_contour = max(contours, key=cv2.contourArea)

    # Fit a bounding box to the contour
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Get the rotation angle from the rectangle
    angle = rect[-1]

    # Get the angles of the box sides
    side_angles = [np.arctan2(box[i][1] - box[i - 1][1], box[i][0] - box[i - 1][0]) for i in range(len(box))]

    # Find the angle corresponding to the longest side
    longest_side_index = np.argmax([np.linalg.norm(box[i] - box[i - 1]) for i in range(len(box))])
    angle_with_x_axis = side_angles[longest_side_index] * (180 / np.pi)

    # Draw the box on the image
    cv2.drawContours(img_copy, [box], 0, (0, 255, 0), 2)

    # Draw the longest side with a different color (e.g., blue)
    cv2.line(img_copy, tuple(box[longest_side_index]), tuple(box[longest_side_index - 1]), (0, 0, 255), 2)

    # Draw a horizontal line through the center of the image
    center_line_y = img_copy.shape[0] // 2
    cv2.line(img_copy, (0, center_line_y), (img_copy.shape[1], center_line_y), (255, 0, 0), 2)

    # Draw the angle arc on the image
    center = tuple(np.mean(box, axis=0).astype(int))
    radius = 50
    start_angle = int(angle_with_x_axis - 90)
    end_angle = int(angle_with_x_axis + 90)
    color = (255, 0, 0)  # Red color for the arc
    thickness = 2
    cv2.ellipse(img_copy, center, (radius, radius), 0, start_angle, end_angle, color, thickness)

    # Resize the output window to 1/3 of the original size
    scale_percent = 33.3
    width = int(img_copy.shape[1] * scale_percent / 100)
    height = int(img_copy.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img_copy, dim, interpolation=cv2.INTER_AREA)

    # Display the result
    cv2.imshow("Traced Box with Angle Arc", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return angle_with_x_axis

# Use 'box.jpg' as the image file
image_path = 'box.jpg'
angle_with_x_axis = find_rotation_angle(image_path)
print(f"Angle with x-axis of the longest side: {angle_with_x_axis} degrees")
