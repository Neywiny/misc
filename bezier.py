import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
class nCi:
    data = {0:{0:1}}
    def genrow(self,row):
        if row in self.data:
            return self.data[row]
        else:
            if row - 1 in self.data:
                inputRow = self.data[row-1]
            else:
                inputRow = self.genrow(row - 1)
            length = len(self.data[row - 1]) + 1
            outputRow = list([1]*length)
            for i in range(1, len(self.data[row - 1])):
                outputRow[i] = inputRow[i-1] + inputRow[i]
            self.data[row] = outputRow
            return outputRow
            
    def __getitem__(self,val):
        if type(val) == slice:
            val = (val.start,val.stop)
        if len(val) != 2:
            raise IndexError
        if not (val[0] in self.data and val[1] in self.data[0]):
            self.genrow(val[0])
        return self.data[val[0]][val[1]]
    def __call__(self,row,position):
        return self[(row,position)]
class Bezier:
    class Point:
        def __init__(self,point):
            self.value = list(point)
        def __mul__(self,factor):
            return self.__class__((self.value[0]*factor,self.value[1]*factor))
        def __str__(self):
            return '('+str(self.value[0])+','+str(self.value[1])+')'
        def __repr__(self):
            return str(self)
        def __add__(self,other):
            return self.__class__((self.value[0]+other.value[0],self.value[1]+other.value[1]))
        def val(self):
            return self.value
    nci = nCi()
    points = list()
    step = 0.1
    def __init__(self,*points):
        if type(points[0]) == list or type(points[0]) == tuple:
            points = points[0]
        for point in points:
            self.points.append(self.Point(point))
        self.n = len(points) - 1
    def bin(self,i,n,t):
        return float(self.nci(n,i))*(t**i)*((1-t)**(n-i))
    def __call__(self,t):
        l = [self.points[i] * self.bin(i,self.n,t) for i in range(self.n + 1)]
        total = self.Point((0,0))
        for point in l:
            total += point
        return total
    def genPoints(self,step=None):
        if step == None:
            step = self.step
        output = list()
        for i in range((int(1/step)) + 1):
            output.append(self(i*step))
        return output
    def getPoints(self):
        return self.points
    def setPoints(self,points):
        self.points = [self.Point(point) for point in points]
        self.n = len(points) - 1
    def newPoint(self,n,x,y):
        self.points.insert(n,self.Point((x,y)))
        self.n += 1
    def setPoint(self,n,x,y):
        self.points[n] = self.Point((x,y))
    def delPoint(self,n=None,x=None,y=None):
        if n != None:
            self.points.pop(n)
            self.n -= 1
        elif x != None and y != None:
            for point in self.points:
                if point.val() == [x,y]:
                    self.points.remove(point)
                    self.n -= 1
                    break
def redraw():
    ax.clear()
    if selectedControl:
        ax.annotate(xy=(selectedControl.center[0],selectedControl.center[1]),s='%(x)5f,%(y)5f'%{'x':selectedControl.center[0],'y':selectedControl.center[1]})
    points = B.genPoints()
    pX = [point.value[0] for point in points]
    pY = [point.value[1] for point in points]
    ax.scatter(pX,pY)

    minX,minY = maxX,maxY = patches[0].center
    mini,maxi = min(minX,minY),max(maxX,maxY)
    for x,y in [patch.center for patch in patches]:
        maxi = max(maxi,x,y)
        mini = min(mini,x,y)
    #ax.set_xlim([mini*0.91,maxi*1.1])
    #ax.set_ylim([mini*0.91,maxi*1.1])
    print(ax.set_ylim(bottom = mini*0.91, top=maxi*1.1),ax.set_xlim(left=mini*0.91, right=maxi*1.1),maxi,mini)
    ax.axis('equal')
    p = PatchCollection(patches,alpha=0.4)
    ax.add_collection(p)
    
    fig.canvas.draw_idle()
def update(nPoints):
    B.step = 1.0/nPoints
    redraw()
def onclick(event):
    global selectedControl
    if event.inaxes == ax:
        if event.button == 3:
            for i,circle in enumerate(patches):
                if circle.contains_point((event.xdata,event.ydata)):
                    patches.remove(circle)
                    B.delPoint(i)
                    redraw()
                    return
        if event.dblclick:
            for i,circle in enumerate(patches):
                if circle.contains_point((event.xdata,event.ydata)):
                    selectedControl = circle
                    redraw()
                    break
        elif selectedControl:
            B.setPoints(list(circle.center for circle in patches))
            selectedControl = None
            redraw()
        else:
            if not any(circle.contains_point((event.xdata,event.ydata)) for circle in patches):
                patches.insert(int(len(patches)/2),Circle((event.xdata,event.ydata),0.1))
                B.setPoints(list(circle.center for circle in patches))
                redraw()
def onmove(event):
    if selectedControl and event.xdata and event.ydata:
        selectedControl.center = event.xdata,event.ydata
        B.setPoints(list(circle.center for circle in patches))
        redraw()
def newPoint(event):
    global text_boxN,text_boxX,text_boxY
    B.newPoint(int(text_boxN.text[0]),float(text_boxX.text[0]),float(text_boxY.text[0]))
    patches.insert(int(text_boxN.text[0]),Circle((float(text_boxX.text[0]),float(text_boxY.text[0])),0.1))
    redraw()
def setPoint(event):
    global text_boxN,text_boxX,text_boxY
    B.setPoint(int(text_boxN.text[0]),float(text_boxX.text[0]),float(text_boxY.text[0]))
    patches[int(text_boxN.text[0])] = Circle((float(text_boxX.text[0]),float(text_boxY.text[0])),0.1)
    redraw()
plt.close('all')
fig = plt.figure()#figsize=(10,8))
fig.canvas.set_window_title('Bezier')

cid = fig.canvas.mpl_connect('button_press_event', onclick)
mpt = fig.canvas.mpl_connect('motion_notify_event', onmove)

ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')

axStep = plt.axes([0.15, 0.025, 0.5, 0.05])
sStep = Slider(axStep,"intervals",1,999,valinit=2,valfmt="%.3d")
sStep.on_changed(update)

def textNVerify(text):
    text = str(text)
    if text.count('.') > 1:
        text.replace('.','',1)
    text_boxN.text = ''.join(filter(lambda x: x in '1234567890.',text))[:13]
def textXVerify(text):
    text = str(text)
    if text.count('.') > 1:
        text.replace('.','',1)
    text_boxX.text = ''.join(filter(lambda x: x in '1234567890.',text))[:13]
def textYVerify(text):
    text = str(text)
    if text.count('.') > 1:
        text.replace('.','',1)
    text_boxY.text = ''.join(filter(lambda x: x in '1234567890.',text))[:13]
WIDTH = 0.2
axboxN = plt.axes([0.15, 0.075, WIDTH, 0.035])
text_boxN = TextBox(axboxN, 'Point #')
axboxX = plt.axes([0.15+0.1+WIDTH, 0.075, WIDTH, 0.035])
text_boxX = TextBox(axboxX, 'Point X')
axboxY = plt.axes([0.15+(0.1+WIDTH)*2, 0.075, WIDTH, 0.035])
text_boxY = TextBox(axboxY, 'Point Y')

text_boxN.on_text_change(textNVerify)
text_boxX.on_text_change(textXVerify)
text_boxY.on_text_change(textYVerify)


addax = plt.axes([0.85, 0.025, 0.1, 0.04])
button = Button(addax, 'Add')
button.on_clicked(newPoint)
moveax = plt.axes([0.75, 0.025, 0.1, 0.04])
buttonMove = Button(moveax, 'Set')
buttonMove.on_clicked(setPoint)

patches = []
selectedControl = None
controlPoints = [(1,1),(2,3),(4,3),(3,1)]
minX,minY = maxX,maxY = controlPoints[0]
for x,y in controlPoints:
    if maxX < x:
        maxX = x
    if maxY < y:
        maxY = y
    if minX > x:
        maxX = x
    if minY > y:
        maxY = y
    temp = Circle((x,y),0.1)
    patches.append(temp)
    
B = Bezier(list(circle.center for circle in patches))
points = B.genPoints()

pX = [point.value[0] for point in points]
pY = [point.value[1] for point in points]
ax.scatter(pX,pY)
ax.set_xlim([minX*0.91,maxX*1.1])
ax.set_ylim([minY*0.91,maxY*1.1])
p = PatchCollection(patches,alpha=0.4)
ax.add_collection(p)
fig.set_figheight
plt.show()
