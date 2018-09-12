##from matplotlib import pyplot as plt
##from matplotlib import colors
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk
import colorsys
def hsv2rgb(h,s=1,v=1):
    return tuple(i for i in tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h/MAX,s,v)))
def mandelbrot(c,maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0

def mandelbrot_set(r1,r2,width,height,maxiter):
    n3 = np.empty((width,height))
    for i in range(width):
        for y in range(height):
            n3[i,y] = mandelbrot(r1[i] + 1j*r2[y],maxiter)
    #np.savetxt('mandel.txt', n3, fmt='%.1d', delimiter=',', newline='\n')
    return n3

def mandelbrot_image(x,y,width=10,height=10,maxiter=256):
    dpi = 72
    img_width = dpi * width
    img_height = dpi * height
    z = mandelbrot_set(x,y,img_width,img_height,maxiter)
    return z
print 'starting'
window = Tk()
WIDTH = 720
HEIGHT = 720
##canvas = Canvas(window, width=WIDTH,height=HEIGHT,bg = "#000000")
##canvas.pack()
x = np.linspace(-2.0, 0.5, 720)
y = np.linspace(-1.25, 1.25, 720)
data = np.empty((720,720))
data.fill(0)
hue = 0
MAX = 128.0
#data = mandelbrot_set(x,y,720,720,256)
data = np.load('mandel.npy')
##output = np.empty((WIDTH,HEIGHT),dtype=np.dtype((np.int,3)))
##for i in range(WIDTH):
##    output[i] = map(hsv2rgb,data[i])
img = Image.fromarray(data, 'I')
img.show()
photo = ImageTk.PhotoImage(img)
label = Label(image=photo)
label.image = photo
label.pack()
#window.mainloop()
