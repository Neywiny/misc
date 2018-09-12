import numpy as np
from Tkinter import *
import audioop,time,colorsys,pyaudio
#import threading

class Recorder():
    def __init__(self):
        self.p = None
        self.stream=None
        self.buff = None
        self.rms = None
        self.m = None
        self.running = True
        #print 'initiated'
        return
    def run(self,q=None):
        #print'running'
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
        if True:
        #while self.running:
            self.buff = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
            self.buff = np.append(self.buff,[0]*len(self.buff)*(2**PADDING-1))
            self.buff = np.fft.fft(self.buff)/CHUNK
            self.rms = audioop.rms(self.buff,2)
            self.buff = map(lambda y:(y.real**2+y.imag**2)**(0.5)/(1.516122797*self.rms),self.buff)[:len(self.buff)/2]
            self.m = float(max(self.buff))
    def get(self):
        #print 'getting'
        self.run()
        try:
            return ((list(self.buff),float(self.rms),float(self.m)))
        except (AttributeError,TypeError):
            print 'printing>>',self.buff,self.rms,self.m
    def end(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
class Drawer():
    def __init__(self,recorder):
        self.m = 0
        self.text = ''
        self.recorder = recorder
    def draw(self):
        data,rms,m = self.recorder.get()
        if rms == 0: return False
        if m == 0: return False
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
            canvas.delete("bar"+str(x))
            if GHEIGHT == tBarHeight:
                hexcode = "#%02x%02x%02x" % hsv2rgb(1-((y/self.m)*0.75),1,1)
                canvas.create_rectangle(x*(WIDTH/len(data)),HEIGHT,x*(WIDTH/len(data))+bWidth,HEIGHT-((y/self.m)*GHEIGHT),tag="bar"+str(x),fill=hexcode)
            else:
                drawBar(x,x*(WIDTH/len(data)),y,bWidth, self.m)
        canvas.delete('display')
        canvas.create_text(WIDTH/2, 20, text=self.text, tag = 'display')
        return True
    
def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def update():
    global times
    t1 = time.time()
    #recorder.get(q)
    if not drawer.draw():
        drawer.m = 0
    times.append(time.time()-t1)
    #drawer.text = ("%.03f"%(sum(times)/len(times)))[2:]
    drawer.text = str(PADDING)+' '+str(len(recorder.buff))
    window.after(1,update)
    
def drawBar(sid, x, y, w, m):
    yVal = int(y/m*nBars)
    yN = HEIGHT
    h = GHEIGHT/nBars
    for bar in xrange(yVal):
        Hue = 1-(float(bar)/nBars)-0.3*1.1
        if Hue < 0: Hue = 0
        gradColor = '#%02x%02x%02x' % hsv2rgb(Hue,1,1)
        canvas.create_rectangle( x , HEIGHT-(h*bar), x + w, yN - h, fill = gradColor ,outline = "#FFFFFF", tag="bar"+str(sid))
        yN -= h
        
def click(event):
    global GHEIGHT,PADDING
    if event.x <= WIDTH/2:
        GHEIGHT = window.winfo_screenheight()
    else:
        GHEIGHT = tBarHeight

def up(event):
    global PADDING
    PADDING += 1
def down(event):
    global PADDING
    PADDING -= 1
def exit(event):
    window.destroy()
global times,GHEIGHT,PADDING
PADDING = 0
times = list()
CHUNK = 2048
RATE = 192000
WIDTH, HEIGHT = 1920, 1080
divs = CHUNK
mSec = 5
tBarHeight = 120
nBars = 20
window = Tk()
GHEIGHT = window.winfo_screenheight()
#window.attributes("-fullscreen",True)
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#FFFFFF")
canvas.bind(sequence = "<Button-1>",func = click)
window.bind(sequence = "<Up>",func = up)
window.bind(sequence = "<Down>",func = down)
window.bind(sequence = "q",func = exit)
canvas.pack()
#########
recorder = Recorder()
drawer = Drawer(recorder)
#########
window.after(0,update)
window.mainloop()
recorder.end()
