import cv2
import numpy as np

# Load the image
image = cv2.imread('image.png')
# image = cv2.imread('birg.jpg')

# Initialize the ORB detector
orb = cv2.ORB_create()

# Detect keypoints and compute descriptors
keypoints, descriptors = orb.detectAndCompute(image, None)

print("Number of keypoints detected: ", len(keypoints))

print("Keypoints : ", keypoints)

# Draw keypoints on the image
image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))

cv2.imshow('ORB Keypoints', image_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()