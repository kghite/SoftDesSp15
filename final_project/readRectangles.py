"""
Kathryn Hite
3/27/15
Input a drawing and find and classify the rectangles within it.
"""

import cv2
import numpy as np

# Get image
def get_binary(file_path):
	image = cv2.imread(file_path)

# Convert the image to grayscale
# Convert the grayscale image to binary
	cv2.imshow("image", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return image

# Find all rectangles within the image
def find_rectangles(image):
	pass

# Classify the rectangles as sides of a 3D Cube

# Perform matrix transforms to create a list of vertices representing the 3D object
def create_cube(rectangles):
	pass

get_binary("cube_labeled.jpeg")