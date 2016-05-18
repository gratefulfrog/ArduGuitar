import stubs

class Positionable:
  scaleFactor =  4
  def __init__(self, xx, yy):
    self.x = xx
    self.y = yy
   
  def  copy(self):
    return Positionable(self.x, self.y)

class MouseLockable:
    hasMouse = None
    
    def __init__(self):
        self.id = stubs.IDs.next()
        
    def lock(self):
        # return True if lock was obtaine False otherwise
        if not (MouseLockable.hasMouse == None or MouseLockable.hasMouse == self.id):
            return False
        else:
            MouseLockable.hasMouse = self.id
            return True
        
    def unlock(self):
        if MouseLockable.hasMouse == self.id:
            MouseLockable.hasMouse = None
            
class LED (Positionable): 
    ledLedSpacing    = 10 ## millimetes center/center
    ledButtonSpacing = 8
    #nbMultiColors    = 4 
    blue      = '#0000FF'
    green     = '#00FF00'
    blueGreen = '#00FFFF'
    offColor  = '#000000'
    red       = '#FF0000'
    yellow    = '#FFFF00'

    LEDColors = [i for i in [offColor, blue, green, blueGreen, red, yellow]]

    r = 8 * Positionable.scaleFactor

    def __init__(self,x, y, colorC):
      Positionable.__init__(self,x,y);
      self.state = 0
      if colorC== LED.blueGreen:
        self.c = [col for col in LED.LEDColors[:4]] 
      else:
        self.c = [LED.offColor, colorC]

    def toggle(self):
      nb = len(self.c)
      if self.state == 0:
        self.state = 3 if nb==4 else 1
      elif self.state == 1:
        self.state = 2 if nb == 4 else 0
      elif self.state == 2:
        self.state = 1
      elif self.state == 3:
        self.state = 0

    def set(self,v):
      self.state = v
      return self
    
    def setMulti(self,v,colorC):
        # there are 2 cases, blue or green
        if colorC == LED.blue:
            self.state = (self.state & 2 )| v 
        else: # it's green
             self.state =  (self.state & 1) | (v<<1 )
        return self
 
    def display(self):
      stroke(self.c[self.state])
      fill(self.c[self.state])
      ellipse(self.x,self.y,LED.r,LED.r)
          
class LedLine(Positionable):
    nbLeds = 3
    # vertical line of blue leds, only for Tone Range
    def __init__(self,x, y):
        Positionable.__init__(self,x,y)
        # led positions are relative to x,y of middle led
        self.leds = [LED(0,(1-i)*Positionable.scaleFactor*LED.ledLedSpacing,LED.blue) for i in range(LedLine.nbLeds)]
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor)
        for i in range(LedLine.nbLeds):
            self.leds[i].display()
        popMatrix()
        
    def setT(self, v):
        print(v)
        for res  in map (lambda i,v:(i,v), range(3),[v&1,(v&2)>>1,(v&4)>>2]):
            self.leds[res[0]].set(res[1])
        return self

    def toggle(self, i):
        self.leds[i].toggle()
        return self

class LedCross (Positionable):
    # cross of horizontal green, vertical blue, central bluegreen leds
  
    nbHorizontalLeds =2

    def __init__(self, x, y):
        Positionable.__init__(self,x,y)
        self.centerLed      = LED(0,0,LED.blueGreen)
        self.verticalLeds   = [1,2]
        self.horizontalLeds = [1,2]
        #led positions are relative to x,y of middle led
        pos = 1;
        for  i in range(LedCross.nbHorizontalLeds):
            offset = pos*Positionable.scaleFactor*LED.ledLedSpacing;
            self.horizontalLeds[i] = LED(offset,0,LED.green)
            self.verticalLeds[i]   = LED(0,offset,LED.blue)
            pos-=2
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor);
        for  i in range(LedCross.nbHorizontalLeds):
            self.horizontalLeds[i].display()
            self.verticalLeds[i].display()
        self.centerLed.display();
        popMatrix()

    def set(self, v, c):
        # set binary value for vol [0,5]
        vals = [v&1,(v&4)>>2,(v&2)>>1] #note bit order 0,2,1 
        for i in range(2):
            if(c == LED.green):
                self.horizontalLeds[i].set(vals[i])
            else:
                self.verticalLeds[i].set(vals[i])
        self.centerLed.setMulti((v&2)>>1,c)
        return self

    def setV(self, v):
        return self.set(v, LED.green)
  
    def setT(self, v):
        return self.set(v, LED.blue)
  
class LedDisplay(Positionable):
    stdSpacing = 40     # mostly
    shortSpacing = 30  # ends x spacing
    nbVTs = 5

    def __init__(self, (x, y)):
        Positionable.__init__(self,x,y)
        self.MVT =  LedCross(-(LedDisplay.shortSpacing + LedDisplay.stdSpacing/2),0);
        self.AVT =  LedCross(-LedDisplay.stdSpacing/2,-LedDisplay.stdSpacing/2);
        self.BVT =  LedCross(-LedDisplay.stdSpacing/2,LedDisplay.stdSpacing/2);
        self.CVT =  LedCross(LedDisplay.stdSpacing/2,-LedDisplay.stdSpacing/2);
        self.DVT =  LedCross(LedDisplay.stdSpacing/2,LedDisplay.stdSpacing/2);
        self.TR =   LedLine(LedDisplay.shortSpacing +LedDisplay.stdSpacing/2,0);  
        self.allVTs =[self.MVT,self.AVT,self.BVT,self.CVT,self.DVT,self.TR]
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor);
        for v in  self.allVTs:
            v.display()
        self.TR.display()
        popMatrix()

    def setV(self, index, v):
        if index < len(self.allVTs)-1:
            self.allVTs[index].setV(v)
        return self
  
    def setT(self, index,  v):
        self.allVTs[index].setT(v)
        return self
  
    def setTR(self, v):
        self.TR.set(v)
        return self

class LCD(Positionable):
    lcdW = 70*Positionable.scaleFactor
    lcdH = 25*Positionable.scaleFactor
    lcdBG = '#E3DE42'
    
    def __init__(self,(x,y)):
        Positionable.__init__(self,x,y)
        self.lcdFont = createFont('Courier', LCD.lcdH/3.5)
        textFont(self.lcdFont)
        self.lns =['0123456789ABCDEF','0123456789ABCDEF']
    
    def setLn(self, lineNb, val):
        self.lns[lineNb] = val
        return self
  
    def getLn(self, lineNb):
        return self.lns[lineNb]
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor)
        rectMode(CORNER)
        fill(LCD.lcdBG)
        stroke(LCD.lcdBG)
        rect(0,0,LCD.lcdW,LCD.lcdH);
        stroke(LED.blue)
        fill(LED.blue)
        textFont(self.lcdFont)
        textAlign(LEFT,BOTTOM)
        text(self.lns[0], 0,LCD.lcdH/3.5+10)        
        text(self.lns[1], 0,LCD.lcdH-20)
        popMatrix()
    

class PushButton (Positionable,MouseLockable):
    pbW = 6*Positionable.scaleFactor
    pbH = 6*Positionable.scaleFactor
    pushedColor = 0
    releasedColor = '#FFFFFF'
    overColor = '#646464'
    debounceDelay = 200

    def __init__(self, x, y, q, actuatorFuncLis):
        Positionable.__init__(self,x,y)
        MouseLockable.__init__(self)
        self.q = q
        self.clickFuncLis = [self.push] + actuatorFuncLis if actuatorFuncLis else [] 
        self.c = PushButton.releasedColor
        self.lastClickTime = millis()
        
    def display(self):
        if self.isOver():
            # we have the lock and we are over
            if mousePressed and self.lock():
                self.c = PushButton.pushedColor
                self.onClick()
            else:
                self.unlock()
                self.c = PushButton.overColor
        else:
            self.c = PushButton.releasedColor
            self.unlock()
        #self.mouseTest()
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor)
        rectMode(CORNER)
        fill(self.c)
        stroke(self.c)
        rect(0,0,PushButton.pbW,PushButton.pbH)
        popMatrix()
        
        
    def mouseTest(self):
        if not self.isOver():
            self.c=PushButton.releasedColor
            #self.unlock()
            return
            # we are over with a lock
        if mousePressed:
            #over with a lock and mouse is pressed
            self.c = PushButton.pushedColor
            self.onClick()
        else:
            self.c = PushButton.overColor
            # we were previously over, with lock but no longer over,
            # over with lock but not pressed
        self.c = PushButton.releasedColor
        self.unlock()

    def isOver(self):
        xx = self.x*Positionable.scaleFactor
        yy = self.y*Positionable.scaleFactor
        return(mouseX > xx and  mouseX < xx+PushButton.pbW and mouseY > yy and mouseY < yy+PushButton.pbH) #and self.lock())

    def onClick(self):
        if millis() > PushButton.debounceDelay + self.lastClickTime:
            for f in self.clickFuncLis:
                f()
            self.lastClickTime = millis()
    
    def push(self):
        self.q.push((0x40 | self.id)<<8)

class LCDPBArray:
    colInd = [4,5,2,1]
    oX = 167
    xOffSet = 14
    oY = 35
    def __init__(self,q):
        self.lcdPbs = [PushButton(LCDPBArray.oX + i*LCDPBArray.xOffSet,LCDPBArray.oY, q, None) for i in range (2)]
        
    def display(self):
        for pb in self.lcdPbs:
            pb.display()    
            
class LedPB:
    ledVOffset = -6*Positionable.scaleFactor
    ledHOffset = 3*Positionable.scaleFactor
    hSpacing = 10
    vSpacing = 22

    def __init__(self,xx,yy,cc,q,func):
        self.led = LED(LedPB.ledHOffset,LedPB.ledVOffset,cc)
        self.pb = PushButton(xx,yy, q, [func, self.led.toggle])

    def display(self):
        pushMatrix()
        translate(self.pb.x*Positionable.scaleFactor,self.pb.y*Positionable.scaleFactor)
        self.led.display()
        popMatrix()
        self.pb.display()

class LedPBArray:
    colInd = [4,5,2,1]
    oX = 140
    oY = 51
    def __init__(self,(x,y),q):
        self.ledPbs = [None for i in range(4)]
        ind=0
        for i in range(2):
            for j in range(2):
                self.ledPbs[ind] = LedPB(x+j*LedPB.hSpacing, 
                                         y+i*LedPB.vSpacing, 
                                         LED.LEDColors[LedPBArray.colInd[ind]],
                                         q,
                                         stubs.lpbFuncs[ind])
                ind+=1
    def display(self):
        for lpb in self.ledPbs:
            lpb.display()
                
        
class Selector(Positionable,MouseLockable):
    sW = 25*Positionable.scaleFactor
    sH = 3*Positionable.scaleFactor
    sR = 2*sH  # radius
    bgC = '#646464'
    black = '#000000'
    white = '#FFFFFF'
    selectedColor = '#FC6608'
    clickPrecision = 5

    def __init__(self,(x,y),cc,isHorizontal, q, nbStops=5, initPos=0):
        Positionable.__init__(self,x,y)
        MouseLockable.__init__(self)
        self.c = cc
        self.isHorizontal = isHorizontal
        self.q = q
        self.nbStops = nbStops
        self.pos = initPos
        self.sliding = False
        if isHorizontal:
            self.w = Selector.sW
            self.h = Selector.sH
            self.origin = (0,self.h/2.0)  # centered at 0,0
            self.posV = [(i*self.w/(nbStops-1.0),self.h/2.0) for i in range(5)]
        else:
            self.w = Selector.sH
            self.h = Selector.sW
            self.origin = (self.w/2.0,0)
            self.posV = [(self.w/2.0,i*self.h/(nbStops-1.0)) for i in range(5)]
    
    def displayRect(self):
        rectMode(CORNER)
        fill(Selector.bgC)
        stroke(Selector.bgC)
        rect(0,0,self.w,self.h) 
     
    def getClosestPos(self):
        res = 0        
        m = mouseY
        vec = [r[1]+self.y*Positionable.scaleFactor for r in self.posV]
        if self.isHorizontal:
            m = mouseX
            vec = [r[0]+self.x*Positionable.scaleFactor for r in self.posV]
        if m <= vec[0]:
                None # done
        elif m >= vec[-1]:
            res = self.nbStops-1
        else:
            d = abs(m - vec[res])
            for i in range(1,self.nbStops):
                dd = abs(m-vec[i])
                if dd < d:
                    d = dd
                    res = i
        #print('m: ' + str(m) + 'vec: ' + str(vec))
        #print('Closest was: ' + str(res))
        return res
    
    def setPos(self, pIndex):
        if self.pos != pIndex:
            self.pos = pIndex
            self.q.push( (0X20<<8) | (((self.pos)<< 4 | 0xF) if self.isHorizontal else (0xF0 | self.pos)))                  
            
    def displaySlider(self):
        fill(self.c)
        stroke(self.c)
        ellipseMode(CENTER)
        ellipse(self.posV[self.pos][0],self.posV[self.pos][1],Selector.sR,Selector.sR)
        
    def displaySliding(self):
        fill(Selector.selectedColor)
        stroke(Selector.selectedColor)
        (x,y) = self.posV[self.getClosestPos()]
        ellipseMode(CENTER)
        ellipse(x,y,Selector.sR,Selector.sR)
            
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor)
        if mousePressed and self.isOverS():
            self.sliding = True
        if self.sliding:
            self.setPos(self.getClosestPos())
        if not mousePressed:
            self.sliding  = False
            self.unlock()
            
        self.displayRect()
        if self.sliding:
            self.displaySliding()
        else:
            self.displaySlider()
        
        popMatrix()
    
    def xy(self):
        return map(lambda a,b: a+b,
               (self.posV[self.pos][0],self.posV[self.pos][1]), 
               (self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor))
    
    def isOverS(self):
        (sX, sY) = self.xy()
        delta = Selector.sH + Selector.clickPrecision
        #print('mouseX: ' + str(mouseX) + ' sliderX: ' + str(sX))
        #print('mouseY: ' + str(mouseY) + ' sliderY: ' + str(sY))
        res = (mouseX >= (sX - delta) and 
               mouseX <= (sX + delta) and 
               mouseY >= (sY - delta) and 
               mouseY <= (sY + delta))
        
        #print('Over: ' + str(res))
        return res and self.lock()