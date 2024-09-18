import cv2
import numpy as np

def barrel_distortion(image_path, output_path, k1=-0.1, k2=0.0001):
    img = cv2.imread(image_path)

    height, width = img.shape[:2]

    # Generate a new camera matrix from the intrinsic camera matrix.
    # fx, fy: focal lengths, cx, cy: optical centers
    fx, fy, cx, cy = width, height, width / 2, height / 2
    camera_matrix = np.array([[fx, 0, cx],
                              [0, fy, cy],
                              [0, 0, 1]], dtype="double")

    # Distortion coefficients - only k1 and k2
    dist_coeffs = np.array([k1, k2, 0, 0, 0])

    # Applying barrel distortion
    distorted_img = cv2.undistort(img, camera_matrix, dist_coeffs)

    cv2.imwrite(output_path, distorted_img)

# Use the function
barrel_distortion("img_.jpg", "distorted_image.jpg")
