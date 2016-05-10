def verticalLines(s):
    R= 200
    y=20
    x= 20
    h= 2*R
    for i in range(s, 100,10):
        d = R*(1-cos(radians(i)))
        line (x+d,y,x+d, y+h)

def horizontalLines(s):
    R= 200
    y=20
    x= 20
    h= 2*R
    for i in range(s, 100,10):
        d = R*(1-cos(radians(i)))
        line (x,y+d,x+h, y+d)


def setup():
    size(1000,800)
    background(0)
    stroke(255)
    #verticalLines(0)
    horizontalLines(0)
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
            

def draw():
    global i
    background(0)
    inc()
     
    stroke(255)
    #verticalLines(0)
    horizontalLines(0)
    stroke('#FF0000')
    #verticalLines(i)
    horizontalLines(i)

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