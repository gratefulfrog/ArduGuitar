
R= 500
y=0
x= 0
h= min(2*R,800)

def verticalLines(s):
    xMax =0
    for i in range(s, 190,10):
        d = R*(1-cos(radians(i)))
        line (x+d,y,x+d, y+h)
        xMax=max(xMax,x+d)
    print('xMAx:\t' +str(xMax))
    stroke('#FF0000')
    for a in [0,45,90,135,180]:
        d = R*(1-cos(radians(a)))
        line (x+d,y,x+d, y+h)
    
    
def horizontalLines(s):
    for i in range(0, 180,10):
        d = R*(1-cos(radians(i)))
        line (x,y+d,x+h, y+d)


def setup():
    size(1001,801)
    background(0)
    stroke(255)
    verticalLines(0)
    #horizontalLines(0)
    stroke('#FF0000')

INC = True
i=0
lastX = 0
def inc():
    global i
    global INC
    global lastX
    if mousePressed:
        if mouseX > lastX:
            i = (i+1)%10
            lastX=mouseX
            

mouseStartX = 0
mouseEndX = 0

def draw():
    global i
    #background(0)
    #inc()
     
    #stroke(255)
    #verticalLines(0)
    #horizontalLines(0)
    stroke('#FF0000')
    #verticalLines(i)
    #horizontalLines(i)

def mousePressed():
    global mouseStartX 
    mouseStartX = mouseX
    
def mouseReleased():
    global mouseEndX
    mouseEndX=mouseX
    print('dX:\t' + str(mouseEndX - mouseStartX))
    print('dA:\t' + str(degrees(acos(mouseEndX/R) - acos(mouseStartX/R)))) ## ???


"""    
lastPressTime = millis()
pressdelay = 200    

def mouseClicked():
    global INC 
    global lastPressTime
    if (millis() > lastPressTime + pressdelay):
        inc()
        lastPressTime = millis()
"""