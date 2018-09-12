import numpy as np
from Tkinter import *
import audioop,time,colorsys,pyaudio

class Recorder():
    def __init__(self):
        self.p=pyaudio.PyAudio()
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
        self.buff = None
        self.running = True
        return
    def run(self):
        self.buff = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
    def get(self):
        return self.buff
    def end(self):
        self.runing = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
class Drawer():
    def __init__(self):
        self.m = 0
        self.text = ''
    def draw(self):
        data = recorder.get()
        m = float(max(data))
        rms = audioop.rms(data,2)
        if rms == 0: return False
        data = np.fft.fft(data)
        data = map(lambda y:(y.real**2+y.imag**2)**(0.5)/(1.516122797*rms),data)[:len(data)/2]
        if m == 0: return False
        if Log:
            nData = list()
            i = 1
            while i*2 < len(data):
                nData.append(sum(data[i:i*2])/(i*2-1))
                i *= 2
            data = nData
        maxi = float(max(data))
        if maxi > self.m:
            self.m = maxi
        elif maxi <= 0.5*self.m:
            self.m *= 0.75
        bWidth = WIDTH/len(data)
        for x,y in enumerate(data):    
            if GHEIGHT == tBarHeight or (not Log):
                canvas.delete("bar"+str(x))
                hexcode = "#%02x%02x%02x" % hsv2rgb(0.75-((y/self.m)*0.75),1,1)
                canvas.create_rectangle(x*(WIDTH/len(data)),HEIGHT,x*(WIDTH/len(data))+bWidth,HEIGHT-((y/self.m)*GHEIGHT),tag=("bar","bar"+str(x)),fill=hexcode)
            else:
                drawBar(x,x*(WIDTH/len(data)),y,bWidth, self.m)
        canvas.delete('display')
        canvas.create_text(WIDTH/2, 20, text=str(rms)+' '+str(m), tag = 'display')
        return True
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
def update():
    t1 = time.time()
    recorder.run()
    if not drawer.draw():
        drawer.m = 0
    t2 = time.time()
    canvas.delete("time")
    canvas.create_rectangle(0,0,(t2-t1)*1000,25,fill = '#%02x%02x%02x' % hsv2rgb(1-(t2-t1)*0.75,1,1),tag = "time")
    drawer.text = str(Log)
    delay = (16-((t2-t1)*1000))
    if delay <=0: delay = 16
    window.after(int(delay),update)
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
recorder = Recorder()
drawer = Drawer()
#########
window.after(0,update)
window.mainloop()
recorder.end()
