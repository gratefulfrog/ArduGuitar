class Positionable:
  scaleFactor =  4
  def __init__(self, xx, yy):
    self.x = xx
    self.y = yy
  
  def  copy(self):
    return Positionable(self.x, self.y)

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
      ns = v if colorC==LED.blue else (v<<1)
      self.state = ns if self.state == 0 else ns | self.state;        
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
        
    def set(self, v):
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
        self.verticalLeds   = [1,2,3]
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

    def __init__(self, x, y):
        Positionable.__init__(self,x,y)
        self.MVT =  LedCross(-(LedDisplay.shortSpacing + LedDisplay.stdSpacing/2),0);
        self.AVT =  LedCross(-LedDisplay.stdSpacing/2,-LedDisplay.stdSpacing/2);
        self.BVT =  LedCross(-LedDisplay.stdSpacing/2,LedDisplay.stdSpacing/2);
        self.CVT =  LedCross(LedDisplay.stdSpacing/2,-LedDisplay.stdSpacing/2);
        self.DVT =  LedCross(LedDisplay.stdSpacing/2,LedDisplay.stdSpacing/2);
        self.TR =   LedLine(LedDisplay.shortSpacing +LedDisplay.stdSpacing/2,0);  
        self.allVTs =[self.MVT,self.AVT,self.BVT,self.CVT,self.DVT]
    
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor);
        for v in  self.allVTs:
            v.display()
        self.TR.display()
        popMatrix()

    def setV(self, index, v):
        self.allVTs[index].setV(v)
        return self
  
    def setT(self, index,  v):
        self.allVTs[index].setT(v)
        return self
  
    def setTR(self, v):
        self.TR.set(v)
        return self

  
"""

class LCD extends Positionable {
  final static int lcdW = 70*Positionable.scaleFactor,
                   lcdH = 25*Positionable.scaleFactor;
  final static color lcdBG = #E3DE42;
  String[] lns = new String[2];
    
  LCD(int x,int y){
    super(x,y);
    PFont myFont = createFont("Courier", lcdH/3.5);
    textFont(myFont);
    for (int i=0;i<2;i++){
      lns[i] = "0123456789ABCDEF";
    }
  }
  LCD setLn(int lineNb, String val){
    lns[lineNb] = val;
    return this;
  }
  String getLn(int lineNb){
    return lns[lineNb];
  }
  void display() {
    pushMatrix();
    translate(x*Positionable.scaleFactor,y*Positionable.scaleFactor);
    rectMode(CORNER);
    fill(lcdBG);
    rect(0,0,lcdW,lcdH);
    stroke(LED.blue);
    fill(LED.blue);
    text(lns[0], 0,lcdH/3.5+10);
    text(lns[1], 0,lcdH-20);
    popMatrix();
  }
}

class Actuator{
  final static int minDelay = 500;
  int lastX;
  
  Actuator(){
    lastX = millis();
  }
  void doX(){}
  
  void x(){
    if(millis()>minDelay+lastX){
      doX();
      lastX = millis();
    }
  }
}

class LedActuator extends Actuator{
  LED led;
  LedActuator(LED ld){
    super();
    led = ld;
  }
  void doX(){
    led.toggle();
  }
}

class PushButton extends Positionable {
  final static int pbW = 6*Positionable.scaleFactor,
                   pbH = 6*Positionable.scaleFactor;
  final static color pushedColor = 0,
                     releasedColor = #FFFFFF,
                     overColor = #646464;
  color c = releasedColor;
  Actuator ba;
  PushButton(int x, int y, Actuator bba){
    super(x,y);
    ba = bba;
  }
  void display(){
    if (overButton(mouseX,mouseY)){
      if (mousePressed){
        c = pushedColor;
        ba.x();
      }
      else{
        c = overColor;
      }
    }
    else {
      c = releasedColor;
    }
    pushMatrix();
    translate(x*Positionable.scaleFactor,y*Positionable.scaleFactor);
    rectMode(CORNER);
    fill(c);
    stroke(c);
    rect(0,0,pbW,pbH);
    popMatrix();
  }
  boolean overButton(int mx, int my){
    int xx = x*Positionable.scaleFactor,
        yy = y*Positionable.scaleFactor;
    boolean res = (mx >= xx     && 
                   mx <= xx+pbW && 
                   my >= yy     && 
                   my <= yy+pbH);
    return res;
  }
}

class LedPB{
  final static int ledVOffset = -6*Positionable.scaleFactor,
                   ledHOffset = 3*Positionable.scaleFactor,
                   hSpacing = 10,
                   vSpacing = 22;
  PushButton pb;
  LedActuator la;
  LED led;
  LedPB(int xx, int yy, color cc){
    led = new LED(ledHOffset,ledVOffset,cc);
    pb =new PushButton(xx,yy, new LedActuator(led));
  }
  void display(){
    pushMatrix();
    translate(pb.x*Positionable.scaleFactor,pb.y*Positionable.scaleFactor);
    led.display();
    popMatrix();
    pb.display();
  }
}
    
"""