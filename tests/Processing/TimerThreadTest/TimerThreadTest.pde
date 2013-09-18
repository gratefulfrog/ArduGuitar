/* TimerThreadTest
 * Uses a Timer to change the display
 * while allowing mouse interaction
 */


import ketai.ui.*;
import android.view.MotionEvent;
KetaiGesture ges;
boolean androidVersion = true;

//set to false to run on PC
//boolean androidVersion = false;

int bColor = 0,
    fColor = 255,
    tSize  = 50;

Cycle c;

void setupCycle(){
  // this routine instatiates the Cylce object and starts it cycling
  //String names[] = {"1 sec", "2 sec", "3 sec", "4 sec"};
  String cycleFileName;
  if (androidVersion){ 
    cycleFileName = "//sdcard/ArduGuitar/cycle.tsv";
  }
  else {
    cycleFileName =  "/home/bob/ArduGuitar/android/cycle.tsv" ;
  }

  c = new Cycle(cycleFileName);  
  println("waiting 5 seconds...");  
  delay(5000);
  c.reset();
  c.startCycle(); 
}  

void setupDisplay(){
  if(!androidVersion){
    size(800,600);
  }
  textSize(tSize);  
  background(bColor);
  fill(fColor);  
  textAlign(CENTER,CENTER);
}

void setup() {
  // androidVersion
  ges = new KetaiGesture(this);
  setupDisplay();
  setupCycle();
}

void refreshDisplay(){
  if(c.cycling()) {
    background(bColor);
    text(c.currentName(),width/2,height/2);
  }
}
void draw() {
  //System.out.println("in draw: ");
  refreshDisplay();
  if (c.cycleTimeUp()) {
    c.incCycle();
  }
}

// from Ketai
void onTap(float x, float y){
  mouseClicked();
}

void mouseClicked(){
  background(bColor);
  if(c.cycling()) {
    c.quit();
  }
  else{
    c.startCycle();
  }
  text("CLICK: cycle is active? " + c.cycling(),width/2,height/2);
}

// from Ketai and Android
// androidVersion

public boolean surfaceTouchEvent(MotionEvent event) {
    //call to keep mouseX, mouseY, etc updated
    super.surfaceTouchEvent(event);
    //forward event to class for processing
    return ges.surfaceTouchEvent(event);
}

