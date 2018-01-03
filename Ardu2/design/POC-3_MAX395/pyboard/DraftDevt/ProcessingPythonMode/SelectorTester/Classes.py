class Positionable:
  scaleFactor =  4
  def __init__(self, xx, yy):
    self.x = xx
    self.y = yy
  
  def  copy(self):
    return Positionable(self.x, self.y)

class Selector(Positionable):
    sW = 25*Positionable.scaleFactor
    sH = 3*Positionable.scaleFactor
    sR = 2*sH  # radius
    bgC = '#646464'
    black = '#000000'
    white = '#FFFFFF'
    selectedColor = '#FC6608'
    clickPrecision = 5

    def __init__(self,x,y,cc,isHorizontal, func, nbStops=5, initPos=0):
        Positionable.__init__(self,x,y)
        self.c = cc
        self.isHorizontal = isHorizontal
        self.posFunc = func
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
        self.pos = pIndex
        self.posFunc(self.pos)                    
            
            
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
        elif self.sliding and mousePressed:
            None
        elif self.sliding and not mousePressed:
            self.sliding  = False
            self.setPos(self.getClosestPos())
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
        return res