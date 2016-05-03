class Positionable{
  final static int scaleFactor =  4;
  int x,
      y;
  Positionable(int xx, int yy){
    x = xx;
    y = yy;
  }
  Positionable(Positionable p){
    x = p.x;
    y = p.y;
  }
}
// used for LED class, sorry for the gloval variables
color[] LEDColors = new color[6];
boolean cInit = false;

class LED extends Positionable {
  final static int ledLedSpacing    = 10, //millimetes center/center
                   ledButtonSpacing = 8,
                   nbColors = 4;
  final static color blue      = #0000FF,
                     green     = #00FF00,
                     blueGreen = #00FFFF,
                     offColor  = 0,
                     red       = #FF0000,
                     yellow    = #FFFF00;
  
  final static int off = 0,
                   on  = 1;
                   
  final static int r = 8 * Positionable.scaleFactor; 
  color[] c;
  int state;
  LED(int x, int y, color cc){
    super(x,y);
    if (!cInit){
        color[] cTemp = {LED.offColor,LED.blue,LED.green,LED.blueGreen,LED.red,LED.yellow};
        for (int i = 0; i<LEDColors.length;i++){
          LEDColors[i] = cTemp[i];
        }
        cInit = true;
    }
    int nb = 2;
    if (cc== LED.blueGreen){
      nb=4;
    }
    c = new color[nb];
    
    c[LED.off] = offColor;
    if (nb==2){
      c[1]  = cc;
    }
    else {
      for (int i=0;i< nbColors;i++){
        c[i]= LEDColors[i];
      }
    state = 0;
    }
  }
  void toggle(){
    int nb = c.length;
    switch(state){
      case 0:
        state = nb==4 ? 3 : 1;
        break;
      case 1:
        state = nb == 4 ? 2 : 0;
        break;
      case 2:
        state = 1;
        break;
      case 3:
        state = 0;
        break;
    }
  }
        
  LED set(int v){
    state= v;
    return this;
  }
  LED setMulti(int v,color cs){
    int ns = cs==LED.blue ? v : v<<1;
    state = state == 0 ? ns : ns | state;        
    return this;
  }
  void display(){
    stroke(c[state]);
    fill(c[state]);
    ellipse(x,y,r,r);
  }
}

class LedLine extends  Positionable {
  // vertical line of blue leds, only for Tone Range
  final static int nbLeds =3;
  LED [] leds= new LED[nbLeds];
  LedLine(int x, int y){
    super(x,y);
    // led positions are relative to x,y of middle led
    for (int i=0; i<nbLeds;i++){
      int vOffset = (1-i)*Positionable.scaleFactor*LED.ledLedSpacing;
      leds[i] = new LED(0,vOffset,LED.blue);
    }
  }
  void display(){
    pushMatrix();
    translate(x*Positionable.scaleFactor,y*Positionable.scaleFactor);
    for (int i=0; i<nbLeds;i++){
      leds[i].display();
    }
    popMatrix();
  }
  LedLine set(int v){
    int vals[]  = {v&1,(v&2)>>1,(v&4)>>2};
    for (int i=0;i<nbLeds;i++){
      leds[i].set(vals[i]);
    }
    return this;
  }
  LedLine toggle(int i){
    leds[i].toggle();
    return this;
  }
}

class LedCross extends  Positionable {
  // cross of horizontal gree, vertical blue, central bluegreen leds
  
  final static int nbHorizontalLeds =2;
  LED [] horizontalLeds;
  LED [] verticalLeds;
  LED centerLed;
  
  LedCross(int x, int y){
    super(x,y);
    centerLed      = new LED(0,0,LED.blueGreen);
    verticalLeds   = new LED[2];
    horizontalLeds = new LED[2];
    // led positions are relative to x,y of middle led
    int pos = 1;
    for (int i=0; i<2;i++){
      int offset = pos*Positionable.scaleFactor*LED.ledLedSpacing;
      horizontalLeds[i] = new LED(offset,0,LED.green);
      verticalLeds[i]   = new LED(0,offset,LED.blue);
      pos-=2;
    }
  }
  void display(){
    pushMatrix();
    translate(x*Positionable.scaleFactor,y*Positionable.scaleFactor);
    for (int i=0; i<2;i++){
      horizontalLeds[i].display();
      verticalLeds[i].display();
    }
    centerLed.display();
    popMatrix();
  }
  LedCross set(int v, color c){
    // set binary value for vol [0,5]
    int vals[] = {v&1,(v&4)>>2,(v&2)>>1}; // note bit order 0,2,1 
    for (int i=0;i<2;i++){
       if(c == LED.green){
         horizontalLeds[i].set(vals[i]);
       }
       else{
         verticalLeds[i].set(vals[i]);
       }
    }
    centerLed.setMulti(vals[2],c);
    return this;
  }
    
  LedCross setV(int v){
    return set(v, LED.green);
  }
  LedCross setT(int v){
    return set(v, LED.blue);
  } 
}
class LedDisplay extends Positionable {
  final static int stdSpacing = 40,  // mostly
                   shortSpacing = 30, // ends x spacing
                   nbVTs = 5;
  LedCross MVT,
           AVT,
           BVT,
           CVT,
           DVT;
  LedLine  TR;
  LedCross[] allVTs = new LedCross[5];
  LedDisplay(int x, int y){
    super(x,y);
    allVTs[0] = MVT = new LedCross(-(shortSpacing +stdSpacing/2),0);
    allVTs[1] = AVT = new LedCross(-stdSpacing/2,-stdSpacing/2);
    allVTs[2] = BVT = new LedCross(-stdSpacing/2,stdSpacing/2);
    allVTs[3] = CVT = new LedCross(stdSpacing/2,-stdSpacing/2);
    allVTs[4] = DVT = new LedCross(stdSpacing/2,stdSpacing/2);
    TR =  new LedLine(shortSpacing +stdSpacing/2,0);  
  }
  LedDisplay setV(int index, int v){
    allVTs[index].setV(v);
    return this;
  }
  LedDisplay setT(int index, int v){
    allVTs[index].setT(v);
    return this;
  }
  LedDisplay setTR(int v){
    TR.set(v);
    return this;
  }
  
  void display() {
    pushMatrix();
    translate(x*Positionable.scaleFactor,y*Positionable.scaleFactor);
    for (int i=0;i<nbVTs;i++){
      allVTs[i].display();
    }
    TR.display();
    popMatrix();
  }
}

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
    