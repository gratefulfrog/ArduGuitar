
class SliderWithStops:
    normalColor = 40
    selectedColor = 0
    precision = 5
    bD = 20
    delta = 60
    def closestValue(unused,v, Vect):
        res = Vect[0]
        if v <= Vect[0]:
            None
        elif v >= Vect[-1:][0]:
            res = Vect[-1:][0]
        else:
            d = abs(Vect[0]-v)
            for vp in Vect[1:]:
                if abs(vp-v) < d:
                    res = vp
                    d = abs(vp-v)
        return res
    
    def __init__(self,x,y,nbStops,initPos,vORh):
        self.vORh = vORh
        self.pos = initPos # an id <nbStops
        self.sliding = False
        self.targetPosVect = []
        self.x = x + (self.pos*SliderWithStops.delta if self.vORh == 'h' else 0)
        self.y = y  + (self.pos*SliderWithStops.delta if self.vORh == 'v' else 0)
        for i in range(nbStops):
            if vORh == 'v':
                self.targetPosVect += [(x,y+i*SliderWithStops.delta)]
            else:
                self.targetPosVect += [(x+i*SliderWithStops.delta,y)]
    
    def draw(self):
        if mousePressed and self.overB():
            self.sliding =  True
            print('sliding')
        if self.sliding and not mousePressed:
            self.sliding = False
            self.setPos()
            print('not sliding')
            
        #draw slider then targets
        rectMode(CENTER)
        ellipseMode(CENTER)
        if self.sliding:
            fill(SliderWithStops.selectedColor)
            stroke(SliderWithStops.selectedColor)
            self.setPos()
            rect(self.x,self.y,SliderWithStops.bD,SliderWithStops.bD)
        else:
            fill(SliderWithStops.normalColor)
            stroke(SliderWithStops.normalColor)
            rect(self.x, #+ (self.pos*SliderWithStops.delta if self.vORh == 'h' else 0),
                 self.y, # + (self.pos*SliderWithStops.delta if self.vORh == 'v' else 0),
                 SliderWithStops.bD,SliderWithStops.bD)
        fill(255)
        stroke(0)
        for pxy in self.targetPosVect:
            ellipse(pxy[0],pxy[1],SliderWithStops.bD,SliderWithStops.bD)
    
    def overB(self):
        xB = self.x 
        yB = self.y 
        res = (mouseX>=xB-SliderWithStops.bD-SliderWithStops.precision 
            and mouseX <= xB+SliderWithStops.bD+SliderWithStops.precision 
            and mouseY >= yB-SliderWithStops.bD-SliderWithStops.precision 
            and mouseY <= yB+SliderWithStops.bD+SliderWithStops.precision)
        print (res)
        return res
    
    def setPos(self):
        if self.vORh == 'v':
            self.x = self.targetPosVect[0][0]
            self.y = self.closestValue(mouseY, [p[1] for p in self.targetPosVect])
        else:
            self.x = self.closestValue(mouseX, [p[0] for p in self.targetPosVect]) 
            self.y = self.targetPosVect[0][1]
    



swp = SliderWithStops(100,100,5,2,'v')
swpH = SliderWithStops(150,100,5,2,'vh')
def setup():
    size(1000, 700)
    background(80)
    stroke(0)
    fill(255)
    
def draw():
    background(80)
    swp.draw()
    swpH.draw()

