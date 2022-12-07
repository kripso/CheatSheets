# with the Tkinter canvas, drawings can only be saved as .ps files 
# use PIL to draw simultaneuosly to memory and then save to file
# PIL allows .png .jpg .gif or .bmp file formats
import tkinter as tk
from PIL import Image, ImageDraw
root = tk.Tk()
root.title("drawing lines")
# # some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)
width = 450
height = 450
# # create the drawing canvas
cv = tk.Canvas(root, width=width, height=height, bg='white')
cv.pack()
# create empty PIL image and draw objects to draw on
# PIL draws in memory only, but the image can be saved
image = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)
# draw horizontal lines
x1 = 0
x2 = 450
for k in range(0, 500, 50):
    y1 = k
    y2 = k
    # Tkinter (visible)
    cv.create_line(x1, y1, x2, y2)
    # PIL (to memory for saving to file)
    draw.line((x1, y1, x2, y2), black)    
# draw vertical lines
y1 = 0
y2 = 450
for k in range(0, 500, 50):
    x1 = k
    x2 = k
    # Tkinter
    cv.create_line(x1, y1, x2, y2)
    # PIL
    draw.line((x1, y1, x2, y2), black)
# Tkinter canvas object can only be saved as a postscipt file
# which is actually a postscript printer language text file
cv.postscript(file="mylines.ps", colormode='color')
# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "mylines.jpg"
image.save(filename)
root.mainloop()

