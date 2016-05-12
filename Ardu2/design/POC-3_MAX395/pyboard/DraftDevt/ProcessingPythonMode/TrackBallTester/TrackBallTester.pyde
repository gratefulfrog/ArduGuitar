 
redLines = True

def verticalLines(s):
    stroke(255)
    h=height-1
    R=(width-1)/2
    oX = (width-1)/2
    oY = (height-1)/2
    minL=3
    for i in range(s, 190,10):
        d = R*(1-cos(radians(i)))
        line (d,oY-max(minL,sqrt(d*(2*R-d))),d,oY+max(minL,sqrt(d*(2*R-d))))
    if redLines:
        stroke('#FF0000')
        for a in [0,45,90,135,180]:
            d = R*(1-cos(radians(a)))
            line (d,oY-max(minL,sqrt(d*(2*R-d))),d,oY+max(minL,sqrt(d*(2*R-d))))
    
def horizontalLines(s):
    stroke(255)
    h= width-1
    R = (height-1)/2
    oX = (width-1)/2
    oY = (height-1)/2
    minL=3
    for i in range(s, 190,10):
        d = R*(1-cos(radians(i)))
        line (oX-max(minL,sqrt(d*(2*R-d))),d,oX+max(minL,sqrt(d*(2*R-d))), d)
    if redLines:
        stroke('#FF0000')
        for a in [0,45,90,135,180]:
            d = R*(1-cos(radians(a)))
            line (oX-max(minL,sqrt(d*(2*R-d))),d,oX+max(minL,sqrt(d*(2*R-d))), d)
     
def setup():
    size(301,301)
    background(0)
    verticalLines(0)
    horizontalLines(0)
    #mSleep(1000)
    #print(str(steps))
    print('Starting!')
    #shiftRight(50)
    
def mSleep(msecs):
    now = millis()
    while millis()-now < msecs:
        None

hSteps = 0 # for stepping the display 
hI=0
def incH():
    global hI
    global hSteps
    global mouseStartX
    if mousePressed:
        if mouseOffTarget():
            return
        if mouseX-mouseStartX <0:
            incHNeg()
        else:
            hSteps = map(mouseX-mouseStartX,0,width-1,0,18)
            mouseStartX = mouseX
            if hSteps>0:
                hI = (hI+1)%10
                hSteps -=1

def incHNeg():
    global hI
    global hSteps
    global mouseStartX
    if mousePressed:
        if mouseOffTarget():
            return
        if mouseX-mouseStartX >0:
            incH()
        else:
            hSteps = map(mouseStartX-mouseX,0,width-1,0,18)
            mouseStartX = mouseX
            if hSteps>0:
                hI = 9 if hI==0 else hI-1
                hSteps -=1

vSteps = 0 # for stepping the display 
vI=0
def incV():
    global vI
    global vSteps
    global mouseStartY
    if mousePressed:
        if mouseOffTarget():
            return
        if mouseY-mouseStartY <0:
            incVNeg()
        else:
            vSteps = map(mouseY-mouseStartY,0,height-1,0,18)
            mouseStartY = mouseY
            if vSteps>0:
                vI = (vI+1)%10
                vSteps -=1

def incVNeg():
    global vI
    global vSteps
    global mouseStartY
    if mousePressed:
        if mouseOffTarget():
            return
        if mouseX-mouseStartX >0:
            incH()
        else:
            vSteps = map(mouseStartY-mouseY,0,height-1,0,18)
            mouseStartY = mouseY
            if vSteps>0:
                vI = 9 if vI==0 else vI-1
                vSteps -=1


mouseStartX = 0
mouseEndX = 0
startPointX = 0

mouseStartY = 0
mouseEndY = 0
startPointY = 0

def mouseOffTarget():
    oX = (width-1)/2
    oY = (height-1)/2
    return sq(mouseX-oX) + sq(mouseY-oY) > sq((width-1)/2)

def draw():
    background(0)
    incH()
    incV()
    verticalLines(hI)
    horizontalLines(vI)
    #horizontalLines(0)
    mSleep(50)


def mousePressed():
    global mouseStartX
    global startPointX
    global mouseStartY
    global startPointY
    mouseStartX = mouseX
    startPointX = mouseX
    mouseStartY = mouseY
    startPointY = mouseY
   
def mouseReleased():
    global mouseEndX
    global mouseEndY
    mouseEndX = mouseX
    mouseEndY = mouseY
    dX = mouseEndX - startPointX
    dY = mouseEndY - startPointY
    dV = round(map(dX,1-width,width-1,-5,5))
    dT = round(map(dY,1-height,height-1,-5,5))
    print('dX,dY:\t' + str(dX) +','+str(dY))
    print('dV,dT:\t' + str(dV) +','+str(dT))