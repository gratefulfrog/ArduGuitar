## HMI mockup python version

import Classes, oClasses, stubs

widthReal =  300  # millimeters
heightReal = 220;
bg = 40

def settings():
  size(int(round(widthReal*Classes.Positionable.scaleFactor)),int(round(heightReal*Classes.Positionable.scaleFactor)))

ld = Classes.LedDisplay(70,40)
lcdPbs = [Classes.PushButton(167 + i*14,30, None) for i in range (2)]
ledPbs = [0,1,2,3]

lcdMgr = None

sh = Classes.Selector(185, 52,Classes.Selector.white,True,stubs.hSelect)
sv = Classes.Selector(220, 41,Classes.Selector.black,False,stubs.vSelect)

def setupLEDPbs():
    global ledPbs
    ind = 0
    colInd = [4,5,2,1]
    for i in range(2):
        for j in range(2):
            ledPbs[ind] = Classes.LedPB(140+j*Classes.LedPB.hSpacing, 51+i*Classes.LedPB.vSpacing, Classes.LED.LEDColors[colInd[ind]],stubs.lpbFuncs[ind])
            ledPbs[ind].display()
            ind+=1

def displayLEDPbs():
    [p.display() for p in ledPbs]
        
def doLeds():
    global ld
    [(ld.setV(i,i+3), ld.setT(i,i+2)) for i in range(5)]
    ld.TR.set(7)
    ld.display()
    
def drawLCDPbs():
    [p.display() for p in lcdPbs ]

def setup():
    global lcdMgr
    background(bg)
    doLeds()
    lcdMgr = oClasses.LCDMgr('(A|B)',Classes.LCD(140,0),lcdPbs)
    setupLEDPbs()
    

lastIter = millis()
iterDelay = 1000
def iterSelect():
    global lastIter
    if(millis() > lastIter + iterDelay):
        sv.setPos((sv.pos + 1) %5)
        sh.setPos((sh.pos + 1) %5)
        lastIter = millis()
    
def draw():
    global lcdMgr
    background(bg)
    drawLCDPbs()
    ld.display()
    displayLEDPbs()
    lcdMgr.display()
    sh.display()
    sv.display()
    iterSelect()