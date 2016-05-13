import Classes 
import stubs

class TrackBall(Classes.Positionable):
    radius = 22*Classes.Positionable.scaleFactor
    lineColor = '#FFFFFF'
    markColor = '#FF0000' 
    delayMS = 50  # time to wait between line draws
    minL = 3 # min line length
    redLines=True
    
    def __init__(self,(x,y), xFunc, yFunc,bg):
        # x,y func should take a delta distance as argume
        Classes.Positionable.__init__(self,x,y)
        self.xFunc = xFunc
        self.yFunc = yFunc
        self.bg = bg
        self.mouseStartX = 0
        self.mouseEndX = 0
        self.startPointX = 0 
        self.mouseStartY = 0
        self.mouseEndY = 0
        self.startPointY = 0
        self.hI=0
        self.vI=0
        self.hSteps=0
        self.vSteps=0
        self.oX = TrackBall.radius
        self.oY = TrackBall.radius
        self.sliding=False
        self.lastLineDraw = millis()
        
    def display(self):
        pushMatrix()
        translate(self.x*Classes.Positionable.scaleFactor,self.y*Classes.Positionable.scaleFactor)
        self.incH(True)
        self.incH(False)
        self.outline()
        self.lines(True)
        self.lines(False)
        #stubs.mSleep(TrackBall.delayMS)
        popMatrix()
    
    def outline(self):
        stroke(self.markColor)
        #stroke(255)
        fill(self.bg)
        ellipseMode(CENTER)
        R=self.oX  # can use either since it's a circle
        H = 2*TrackBall.radius
        ellipse(R,R,H,H)
    
    def lines(self,isVertical):
        stroke(TrackBall.lineColor)
        R = TrackBall.radius
        for i in range(self.vI if isVertical else self.hI, 190,10):
            d = R*(1-cos(radians(i)))
            if isVertical:
                line (d,self.oY-max(3,sqrt(d*(2*R-d))),d,self.oY+max(3,sqrt(d*(2*R-d))))
            else:
                line (self.oX-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oX+max(TrackBall.minL,sqrt(d*(2*R-d))), d)
        if TrackBall.redLines:
            stroke(TrackBall.markColor)
            for a in [0,45,90,135,180]:
                d = R*(1-cos(radians(a)))
                if isVertical:
                    line (d,self.oY-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oY+max(TrackBall.minL,sqrt(d*(2*R-d))))
                else:
                    line (self.oX-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oX+max(TrackBall.minL,sqrt(d*(2*R-d))), d)
                    
    def setSliding(self, start):
        if start:
            self.sliding=True
            self.mouseStartX = mouseX
            self.startPointX = mouseX
            self.mouseStartY = mouseY
            self.startPointY = mouseY
        else:
            self.sliding=False
            self.mouseEndX = mouseX
            self.mouseEndY = mouseY
            dX = self.mouseEndX - self.startPointX
            dY = self.mouseEndY - self.startPointY
            w= TrackBall.radius*2
            dV = round(map(dX,-w,w,-5,5))
            dT = round(map(dY,-w,w,-5,5))
            if dV!=0:
                self.xFunc(dV)
            if dT!=0:
                self.yFunc(dT)
            
            #print('dX,dY:\t' + str(dX) +','+str(dY))
            #print('dV,dT:\t' + str(dV) +','+str(dT))
            
    def getSet(unused,isHorizontal):
        if isHorizontal:
            return (mouseY, 'self.mouseStartY','self.hSteps','self.hI')
        else:
            return  (mouseX, 'self.mouseStartX','self.vSteps','self.vI')
        
    def incH(self,isHorizontal=False):
        if self.mouseOffTarget():
            return
        if mousePressed:
            if not self.sliding:
                self.setSliding(True)
            (mouse,mouseStartS,StepS,IS) = self.getSet(isHorizontal)
            positiveMovement= eval(mouseStartS)<= mouse
            exec(StepS + '= map(abs(mouse-eval(mouseStartS)),0,2*TrackBall.radius,0,18)')
            #self.hSteps = map(abs(mouse-eval(mouseStartS)),0,2*TrackBall.radius,0,18)
            exec(mouseStartS + ' = mouse')
            if eval(StepS)>0:
            #if self.hSteps>0:
                if positiveMovement:
                    exec(IS + '= (' + IS + '+1)%10')
                    #self.hI = (self.hI+1)%10  
                else: 
                    exec(IS + '= (9 if ' + IS + '==0 else ' + IS +' -1)')
                    #self.hI= (9 if self.hI==0 else self.hI-1)
                exec(StepS  +'-=1')
                #self.hSteps -=1
        elif self.sliding:
            self.setSliding(False)

    def mouseOffTarget(self):
        oX = TrackBall.radius+self.x*Classes.Positionable.scaleFactor
        oY = TrackBall.radius+self.y*Classes.Positionable.scaleFactor
        res= sq(mouseX-oX) + sq(mouseY-oY) > sq(TrackBall.radius)
        #print('mouse off target:\t' +str(res))
        #print('mouseX:\t' + str(mouseX))
        #print('oX:\t' + str(oX))
        return res