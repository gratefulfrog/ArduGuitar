oX = 0
oY = 0
w  = 100
h  = 360
lh = h/20
sepoY = h/2-lh/2

strokeC=0
fillC=255
oV = False
oT = False

contact=False

def setup():
    size(500,500)

def draw():
    background(40)
    fill(fillC)
    stroke(strokeC)
    rect(oX,oY,w,h)
    fill(strokeC)
    rect(oX,sepoY,w,lh)
    drawLetters()
    mouseTest()

letterColor='#216249'
toneT='T'
volT='V'
nameColor= '#FFFF00'
nameT = 'A'
xT= (w-oX)/2
yT = (sepoY-oY)/2
xV = xT
yV = ((oY+h)+(sepoY+lh))/2
xN = xT
yN = (yT+yV)/2

def drawLetters():
    fill(letterColor)
    textAlign(CENTER, CENTER)
    textSize(20)
    text(toneT,xT,yT)
    text(volT,xV,yV)
    fill(nameColor)
    text(nameT,xN,yN)
    

def overVy():
    global oV
    oV =   (mouseY >sepoY+lh and mouseY < oY+h)
    return oV

def overTy():
    global oT 
    oT= (mouseY >oY and mouseY < sepoY)
    return oT

def overX():
    return (mouseX >oX and mouseX <oX+w)

def isOver():
    overVy()
    overTy()
    return (overX() and (oT or oV))

def invertFill():
    global fillC
    global strokeC
    temp = strokeC
    strokeC = fillC
    fillC = temp

def show():
    if oV:
        doVT(newV=round(map(mouseY,oY+h, sepoY+lh, 0,5)))
    if oT:
        doVT(newT=round(map(mouseY,sepoY,oY,0,5)))

def mouseTest():
    if contact and isOver():
        show()

def mousePressed():
    global contact
    if isOver():
        contact=True
        invertFill()

def mouseReleased():
    global contact
    if contact:
        invertFill()
        contact=False
        print('Clear!')
        
lastV = 0
lastT = 0

def doVT(newV=None, newT=None):
    global lastV
    global lastT
    if newV!=None and (newV != lastV):
        lastV=newV
        print('Vol:\t' +str(lastV))
    if newT!=None and (newT != lastT):
        lastT=newT
        print('Tone:\t' +str(lastT))
