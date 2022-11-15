import numpy as np
import cv2

image = cv2.imread('frame1.jpg')
width = 1920
height = 1080

wantedWidth = 1312
wantedHeight = 738

y1 = int((height-wantedHeight)/2)
x1 = int((width-wantedWidth)/2)
y2 = int((height-wantedHeight)/2) + wantedHeight
x2 = int((width-wantedWidth)/2) + wantedWidth
print(x1, y1, x2, y2)
crop = image[y1:y2, x1:x2]
cv2.imshow('Image', crop)
cv2.imwrite("image.jpg", crop)
cv2.waitKey(0)
