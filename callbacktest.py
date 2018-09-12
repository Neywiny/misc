import numpy as np
from Tkinter import *
import audioop,time,colorsys,pyaudio
def callback(in_data, frame_count, time_info, status):
    rms = audioop.rms(in_data,2)
    data = map(lambda x: ord(x), in_data)
    m = float(max(data))
    data = np.fft.fft(data)
    data = map(lambda y:(y.real**2+y.imag**2)**(0.5)/(1.516122797*rms),data)[:len(data)/2]
    if rms == 0: return False
    if m == 0: return False
    if Log:
        nData = list()
        i = 1
        while i*2 < len(data):
            nData.append(sum(data[i:i*2])/(i*2-1))
            i *= 2
        data = nData
    bWidth = WIDTH/len(data)
    for x,y in enumerate(data):    
        if GHEIGHT == tBarHeight or (not Log):
            canvas.delete("bar"+str(x))
            hexcode = "#%02x%02x%02x" % hsv2rgb(1-((y/m)*0.75),1,1)
            canvas.create_rectangle(x*(WIDTH/len(data)),HEIGHT,x*(WIDTH/len(data))+bWidth,HEIGHT-((y/m)*GHEIGHT),tag=("bar","bar"+str(x)),fill=hexcode)
        else:
            drawBar(x,x*(WIDTH/len(data)),y,bWidth, m)
    canvas.delete('display')
    return tuple((in_data, pyaudio.paContinue))
def drawBar(sid, x, y, w, m):
    yVal = int(y/m*nBars)
    yN = HEIGHT
    h = GHEIGHT/nBars
    if yVal < (0.5*nBars):
        canvas.delete("bar"+str(sid))
    else:
        canvas.delete("up"+str(sid))
    for bar in xrange(yVal):
        Hue = 1-(float(bar)/nBars)-0.3*1.1
        if Hue < 0: Hue = 0
        gradColor = '#%02x%02x%02x' % hsv2rgb(Hue,1,1)
        canvas.create_rectangle( x , HEIGHT-(h*bar), x + w, yN - h, fill = gradColor ,outline = "#FFFFFF", tags=("bar","bar"+str(sid),"up"+str(sid)))
        yN -= h
def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
def click(event):
    global GHEIGHT,Log
    canvas.delete("bar")
    Log = bool(round(event.y/float(HEIGHT)))
    if event.x <= WIDTH/2:
        GHEIGHT = window.winfo_screenheight()
    else:
        GHEIGHT = tBarHeight
CHUNK = 1024
RATE = 44100
WIDTH, HEIGHT = 1920, 1080
divs = CHUNK
Log = True
mSec = 5
tBarHeight = 30
nBars = 20
window = Tk()
global GHEIGHT
GHEIGHT = window.winfo_screenheight()
window.attributes("-fullscreen",True)
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#FFFFFF")
canvas.bind(sequence = "<Button-1>",func = click)
canvas.pack()
#########
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK,stream_callback = callback)
#########
#window.after(0,update)
window.mainloop()
