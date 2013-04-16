/*  simple code to use movement to increase/decrease values
 *  could be used for vol & tone controls...
 */


int pixDens = 2;
int xI = 0,
    yI = 0,
    v = 0,
    t = 0,
    pv=0,
    pt=0,
    xRange[] = new int[4],
    yRange[]= new int[4];

int cp = 0;

boolean down = false;

void setup(){
  //size(1196/pixDens,768/pixDens);
  orientation(LANDSCAPE);
  textSize(28);
  smooth();
}

void draw(){
  background(0);
  text("vol: " + v, 10, 60);
  text("tone: " + t, 10, 90);
}

void mousePressed() {
  if(!down){
    xI = mouseX;
    yI = mouseY;
    pv = v;
    pt = t;
    down = true;
  }
  println("pressed");
}

void mouseDragged(){
  checkDirection();
  v = constrain(round(map(mouseX - xI,xRange[0],xRange[1],xRange[2],xRange[3])),0,11);
  t = constrain(round(map(mouseY - yI, yRange[0],yRange[1],yRange[2],yRange[3])),0,11);
}

void checkDirection(){
  if (mouseX>=xI){
    xRange[0] = 0;
    xRange[1] = width-xI;
    xRange[2] = pv;
    xRange[3] = 11;
    
  }
  else{
    xRange[0] = -xI;
    xRange[1] = 0;
    xRange[2] = 0;
    xRange[3] = pv;
  }
  if (mouseY>=yI){
    yRange[0] = 0;
    yRange[1] = height-yI;
    yRange[2] = pt;
    yRange[3] = 0;
    
  }
  else{
    yRange[0] = 0;
    yRange[1] = -yI;
    yRange[2] = pt;
    yRange[3] = 11;
  }
  println(xRange);
  println(yRange);  
}

void mouseReleased() {
  down = false;
  println("released");
}

