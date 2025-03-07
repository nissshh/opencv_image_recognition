import cv2
import numpy as np

# Load the image
# image = cv2.imread('image.png')
image = cv2.imread('birg.jpg')
# image = cv2.imread('aws.png')

# Apply a Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

# Convert the image to grayscale and apply edge detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)


# Show the original and blurred images
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()