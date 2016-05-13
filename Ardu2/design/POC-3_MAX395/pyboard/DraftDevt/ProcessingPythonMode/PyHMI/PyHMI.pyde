## HMI mockup python version

import Classes, oClasses, stubs, TrackBall,SplitPot
from layout import layout

# DEBUGGING VARS
DOITER=False

######

def settings():
  size(int(round(layout.widthReal*Classes.Positionable.scaleFactor)),
       int(round(layout.heightReal*Classes.Positionable.scaleFactor)))

ld     = None 
ledPbA = None 
lcdMgr = None
sh     = None
sv     = None
tb     = None
spa    = None

def setup():
    global ld
    global ledPbA
    global lcdMgr
    global sv
    global sh
    global tb
    global spa
    global components
    ld     = Classes.LedDisplay(layout.oLD)
    ledPbA = Classes.LedPBArray(layout.oLPA)
    lcdMgr = oClasses.LCDMgr(stubs.configDict[(0,0)]['S'],Classes.LCD(layout.oLCD))
    sh     = Classes.Selector(layout.oSH,Classes.Selector.white,True,stubs.hSelect)
    sv     = Classes.Selector(layout.oSV,Classes.Selector.black,False,stubs.vSelect)
    tb     = TrackBall.TrackBall(layout.oTB, stubs.hTBFunc,stubs.vTBFunc,layout.bg)
    spa    = SplitPot.SplitPotArray(layout.oSPA)
    
    components = [ld,ledPbA,lcdMgr,sh,sv,tb,spa]
    
def draw():
    background(layout.bg)
    for c in components:
        c.display()
    if DOITER:
        iterSelect()
        iterLeds()

# iteration over leds and selectors
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
