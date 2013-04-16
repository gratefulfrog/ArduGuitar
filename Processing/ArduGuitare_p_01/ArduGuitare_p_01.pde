/*
Android Pickups_p_01 some improvements
*/
/*
import android.view.MotionEvent;
import ketai.ui.*;

KetaiGesture gesture;
KetaiVibrate vibe;
*/

PImage base;
PImage overlays[] = new PImage[4];

String baseFile = "Pickups1196x768.png",
       overlayFiles[] = {"neck1196x768.png",
                         "middle1196x768.png",
                         "bridgeNorth1196x768.png",
                         "bridgeBoth1196x768.png"};

boolean selected[]= {false,false,false,true};

int currentPreset = 0;
        
int nbOverlays = 4;

int vol = 11,
    tone = 11,
    xI = 0,
    yI = 0,
    pv=11,
    pt=11,
    xRange[] = new int[4],
    yRange[]= new int[4];

boolean down = false;

color colors[] = new color[5];

String names[] = { "Rock",
                   "Blues",
                   "Jazz",
                   "Comp",
                   "Lead"};

void loadImages(){
  base = loadImage(baseFile);
  for (int i=0; i<nbOverlays ;i++){
    overlays[i] = loadImage(overlayFiles[i]);
  }
}

void setup() {

  // Set the size of the screen (this is not really necessary 
  // in Android mode, but we'll do it anyway)
  size(1196,768);
  orientation(LANDSCAPE);
  /*
  gesture = new KetaiGesture(this);
  vibe = new KetaiVibrate(this);
  */
  colorMode(HSB, 360, 100, 100);
  colors[0] = color(0,100,100);  //red
  colors[1] = color(60,100,100); //yellow
  colors[2] = color(120,100,100);  // green
  colors[3] = color(240,100,100);  // blue
  colors[4] = color(300,100,100); // violet
            //color(0,100,100};  // turquoise

  smooth();
  fill(255);
  noStroke();
  loadImages();
  //textSize(32);
  ellipseMode(CENTER);
  noLoop();
}

void draw() {
  background(0,0,0,0);
  image(base,0,0);
  
  for (int i=0;i<nbOverlays;i++){
    if (selected[i])
      image(overlays[i],0,0);
  }
  int yEllipse = height/10, 
      yText = 0;
      
  textSize(32);
  for (int i =0;i<5;i++){
    stroke(colors[i]);
    strokeWeight(4);
    fill(0,0,0,0);
    if (currentPreset==i){
      fill(colors[i]);
    }
    ellipse(round(width*15/16),yEllipse,width/8,height/10);
    fill(color((hue(colors[i])+180)%360,100,100));
    textAlign(CENTER,CENTER);//,CENTER);
    text(names[i],round(width*15/16),yText+height/10);
    noStroke();
    yEllipse += round(height/5);
    yText += round(height/5);
    fill(0,0,0,0);
  }
  fill(0,0,100);
  //textAlign(RIGHT,TOP);
  textAlign(CENTER,TOP);
  textSize(64);
  text(vtString("vol: ",vol),width/2,2); //width*3/4,2);
  //textAlign(RIGHT,BOTTOM);
  textAlign(CENTER,BOTTOM);
  text(vtString("tone: ",tone),width/2,height-2);//width*3/4,height-2);
  fill(0,0,0,0);
}

String vtString(String vt, int val) {
  String res = vt;
  if (val<10){
    vt +=" ";
  }
  return vt + val;
}

void onTap(float x, float y){       
  if (x < width/4) {
    selected[0]= !selected[0];
  }
  else if (x < width/2) {   
    selected[1]= !selected[1];
  }
  else if (x < width*5/8) {
    selected[2]= !selected[2];
    if (selected[2]){
      selected[3] = false;
    }
  }
  else if (x < width*7/8){
    selected[3]= !selected[3];
    if (selected[3]){
      selected[2] = false;
    }
  }
  else {
    for (int i=0;i< 5;i++){
      if (y < height*(i+1)/5) {
        println("color selected: " + i);
        currentPreset = i;
        break;
      }
    }
  }
  
  redraw();
}

void onLongPress(float x, float y){
   //vibe.vibrate(1000);
  if (x < width*7/8) {
    println("  doAllOnOff!");
    doAllOnOff();
  }
  else {
    // do stuff
    onTap(x,y);
   //vibe.vibrate(1000);
    println("vibrate!");    
  }
  redraw();
}

void doAllOnOff(){
  boolean allOn = false;
  for (int i=0;i< nbOverlays;i++){
    allOn |= selected[i];
  }
  for (int i=0;i< nbOverlays;i++){
    selected[i] = !allOn;
  }
}

// only for Android version
/*  
void keyPressed() {
  if (key == CODED && keyCode == MENU) {
    println("menu press!");
    vibe.vibrate(1000);
  }
}
*/

void mousePressed() {
  if(!down){
    xI = mouseX;
    yI = mouseY;
    pv = vol;
    pt = tone;
    down = true;
  }
  onTap(xI,yI);
  println("pressed");
  redraw();
}


void mouseDragged(){
  checkDirection();
  vol = constrain(round(map(mouseX - xI,xRange[0],xRange[1],xRange[2],xRange[3])),0,11);
  tone = constrain(round(map(mouseY - yI, yRange[0],yRange[1],yRange[2],yRange[3])),0,11);
  redraw();
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
  redraw();
}

/*

public boolean surfaceTouchEvent(MotionEvent event) {

  //call to keep mouseX, mouseY, etc updated
  super.surfaceTouchEvent(event);

  //forward event to class for processing
  return gesture.surfaceTouchEvent(event);
}
*/
