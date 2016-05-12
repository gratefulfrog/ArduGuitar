## HMI mockup python version

import Classes, oClasses, stubs, TrackBall

widthReal =  300  # millimeters
heightReal = 220;
bg = 40

def settings():
  size(int(round(widthReal*Classes.Positionable.scaleFactor)),
       int(round(heightReal*Classes.Positionable.scaleFactor)))

ld = None 
lcdPbs = None
ledPbs = None 

lcdMgr = None

sh = None
sv = None
tb = None

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
    ld = Classes.LedDisplay(70,40)
    [ld.setT(i,0) for i in range(5)]
    [ld.setV(i,0) for i in range(5)]
    ld.TR.set(0)
    ld.display()
    
def drawLCDPbs():
    [p.display() for p in lcdPbs ]

def setup():
    global lcdMgr
    global tb
    global lcdPbs
    global ledPbs
    global sv
    global sh
    background(bg)
    doLeds()
    lcdPbs = [Classes.PushButton(167 + i*14,30, None) for i in range (2)]
    ledPbs = [0,1,2,3]
    lcdMgr = oClasses.LCDMgr(stubs.configDict[(2,0)]['S'],Classes.LCD(140,0),lcdPbs)
    setupLEDPbs()
    sh = Classes.Selector(185, 52,Classes.Selector.white,True,stubs.hSelect)
    sv = Classes.Selector(220, 41,Classes.Selector.black,False,stubs.vSelect)
    tb = TrackBall.TrackBall(185,100, stubs.hTBFunc,stubs.vTBFunc)

lastSIter = 0
iterDelay = 1000
def iterSelect():
    global lastSIter
    if(millis() > lastSIter + iterDelay):
        sv.setPos((sv.pos + 1) %5)
        sh.setPos((sh.pos + 1) %5)
        lastSIter = millis()

lastLIter = -5000
vtrVal = 0
def iterLeds():
    global lastLIter
    global ld
    global vtrVal
    
    if(millis() > lastLIter + iterDelay):
        for i in range(5):
            ld.setT(i,vtrVal)
            ld.setV(i,vtrVal)
            None
        ld.setTR(vtrVal)
        lastLIter = millis()
    vtrVal = (vtrVal  + 1) %6   
    
    
def draw():
    global lcdMgr
    background(bg)
    drawLCDPbs()
    ld.display()
    displayLEDPbs()
    lcdMgr.display()
    sh.display()
    sv.display()
    tb.display()
    #iterSelect()
    #iterLeds()
