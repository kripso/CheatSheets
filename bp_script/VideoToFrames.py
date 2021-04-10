import cv2
from PIL import Image, ImageDraw

width = 1280
height = 720

x = 0.44
y = 1-0.32

image = Image.open("exports\\001Extracted\\frame1.jpg")
draw = ImageDraw.Draw(image)
draw.ellipse((width*x-7, height*y-7, width*x+7, height*y+7), fill="red")
image.save("exports\\001Extracted\\frame.jpg", quality=95)

# vidcap = cv2.VideoCapture('exports\\001\\world.mp4')
# success, image = vidcap.read()
# count = 0
# while success:
#     if count == 2:
#         cv2.imwrite("exports\\001Extracted\\frame%d.jpg" % count, image)     # save frame as JPEG file
#     success, image = vidcap.read()
#     # print('Read a new frame: ', success)
#     count += 1

# print(count)

# TODO: calculate Random Frames 10%
# TODO: Read CSV "world_index" == frame and take gaze data with "confidence" of 85 and more and take median cordinate
# TODO: take image and export to procesed folder
