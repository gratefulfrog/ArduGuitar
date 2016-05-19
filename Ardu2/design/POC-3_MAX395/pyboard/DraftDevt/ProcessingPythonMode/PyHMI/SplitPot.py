from Classes import Positionable,MouseLockable,EnQueueable
import stubs

class SplitPot(Positionable,MouseLockable):
    # name display
    volT='V'
    toneT='T'
    toneRangeT= 'TR'
    letterColor='#216249'
    nameColor= '#FFFFFF' #'#FFFF00'
    letterSize=12
    debounceDelay = 150
    
    # rect Display
    sc=0
    fc='#AFAFAF'
    w  = 22*Positionable.scaleFactor
    h  = 68*Positionable.scaleFactor
    lh = 3*Positionable.scaleFactor
    sepoY = h/2-lh/2

    def __init__(self,x,y,name,vtFuncIndex,q,isToneRange=False):
        Positionable.__init__(self,x,y)
        MouseLockable.__init__(self,MouseLockable.SPLITPOT)
        self.volEnQueueable = EnQueueable(EnQueueable.VOL,q)
        self.toneEnQueueable = EnQueueable(EnQueueable.TONE,q)
        self.nameT = name
        self.vtFuncIndex = vtFuncIndex
        #  = vtFuncTuple[0]
        #self.onNewToneFunc = vtFuncTuple[1]
        self.q = q
        if isToneRange:
            self.vT= ''
            self.tT = SplitPot.toneRangeT
        else:
            self.vT= SplitPot.volT
            self.tT = SplitPot.toneT
        self.oX = self.x*Positionable.scaleFactor
        self.oY = self.y*Positionable.scaleFactor
        self.oV = False
        self.oT = False
        self.contact=False
        self.fillC = SplitPot.fc
        self.strokeC = SplitPot.sc
        # name display position data
        self.xT = SplitPot.w/2
        self.yT = SplitPot.sepoY/2
        self.yV = SplitPot.h- self.yT
        self.yN = (self.yT+self.yV)/2
        self.lastClickTime = millis()
        # vol tone values
        #self.lastV=0
        #self.lastT=0
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor);
        fill(self.fillC)
        stroke(self.strokeC)
        rect(0,0,SplitPot.w,SplitPot.h)
        fill(self.strokeC)
        rect(0,SplitPot.sepoY,SplitPot.w,SplitPot.lh)
        self.displayLetters()
        popMatrix()
        self.mouseTest()
    
    def displayLetters(self):
        fill(SplitPot.letterColor)
        textAlign(CENTER, CENTER)
        textSize(SplitPot.letterSize)
        text(self.tT,self.xT,self.yT)
        text(self.vT,self.xT,self.yV)
        fill(SplitPot.nameColor)
        text(self.nameT,self.xT,self.yN)
    
    def mouseTest(self):
        if mousePressed:
            if not self.isOver():
                return
            # we are over
            if not self.contact:
                self.contact=True
                self.invertFill()
            self.doVT()
        elif self.contact:
            # we had begun a mouse press event, and released the mouse
            self.invertFill()
            self.contact=False
            self.unlock()
            #print('Clear!')
    
    def overVy(self):
        self.oV =   (mouseY >self.oY+SplitPot.sepoY+SplitPot.lh and mouseY < self.oY+SplitPot.h)
        
    def overTy(self):
        self.oT= (mouseY >self.oY and mouseY < self.oY+SplitPot.sepoY)
    
    def overX(self):
        return (mouseX >self.oX and mouseX <self.oX+SplitPot.w)
    
    def isOver(self):
        self.overVy()
        self.overTy()
        return (self.overX() and (self.oT or self.oV) and self.lock())

    def invertFill(self):
        temp = self.strokeC
        self.strokeC = self.fillC
        self.fillC = temp
    
    def doVT(self):
        if millis() < SplitPot.debounceDelay + self.lastClickTime:
            return
        if self.oV:
            val=round(map(mouseY,self.oY+SplitPot.h, self.oY+SplitPot.sepoY+SplitPot.lh, 0,5))
            self.volEnQueueable.push( self.vtFuncIndex,int(val))            
        if self.oT:
            val=round(map(mouseY,self.oY+SplitPot.sepoY,self.oY,0,5))
            self.toneEnQueueable.push( self.vtFuncIndex,int(val))
        self.lastClickTime = millis()
            
class SplitPotArray(Positionable):
    masterRangeSpace = 33
    potSpace = SplitPot.w/Positionable.scaleFactor
    #names            = ['M','A','B','C','D','TR']
    nbCoils          = 4
    
    def __init__(self,(x,y),names,q):
        Positionable.__init__(self,x,y)
        self.splitPots = [None for i in range(SplitPotArray.nbCoils+2)]
        
        px = SplitPotArray.masterRangeSpace
        funcArray = [stubs.makeVTFunc(name) for name in names[:SplitPotArray.nbCoils+1]]
        self.splitPots[0] = SplitPot(self.x,
                                     self.y,
                                     names[0],
                                     0, # id of 'M'
                                     q)
                                     #funcArray[0])
        
        for i in range(SplitPotArray.nbCoils):
            self.splitPots[i+1]= SplitPot(self.x+px+i*SplitPotArray.potSpace,
                                          self.y,
                                          names[i+1],
                                          i+1,
                                          q)
                                          #funcArray[i+1])
        
        self.splitPots[SplitPotArray.nbCoils+1] =  SplitPot(self.x+2*px+3*SplitPotArray.potSpace,
                                                            self.y,
                                                            names[SplitPotArray.nbCoils+1],
                                                            SplitPotArray.nbCoils+1, # tone range
                                                            q,
                                                            #stubs.makeVTFunc(names[SplitPotArray.nbCoils+1],False),
                                                            True)
        
    def display(self):
        for sp in  self.splitPots:
            sp.display()