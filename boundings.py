import cv2
import numpy as np
# Load the pre-trained model and image
model = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'weights.caffemodel')
image = cv2.imread('image.png')
# image = cv2.imread('birg.jpg')
# image = cv2.imread('aws.png')

# Preprocess the image and pass it through the model
blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
model.setInput(blob)
detections = model.forward()

# Loop over the detections and draw bounding boxes
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        box = detections[0, 0, i, 3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
        (startX, startY, endX, endY) = box.astype("int")
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# Show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)