/* TimerThreadTest
 * Uses a Timer to change the display
 * while allowing mouse interaction
 * Now integrated into main devt.
 */

// start specifics for android version
///*
import ketai.ui.*;
import android.view.MotionEvent;
KetaiGesture ges;
boolean androidVersion = true;
//*/
// end android specifics

// start non-android specifcs
///*
//boolean androidVersion = false;
//*/
// end non android specifics

int bColor = 0,
    fColor = 255,
    tSize  = 50,
    cStartDelay = 1000;

Cycle c;

String getCycleFileName() {
  if (androidVersion){ 
    return "//sdcard/ArduGuitar/cycle.tsv";
  }
  else {
    return "/home/bob/ArduGuitar/android/cycle.tsv" ;
  }
} 

void setupCycle(){
  // this routine instatiates the Cylce object and starts it cycling
  String cycleFileName = getCycleFileName();
  c = new Cycle(cycleFileName);  
  println("waiting 5 seconds...");  
  delay(cStartDelay);
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
  // specifcs for android
  ///*
  ges = new KetaiGesture(this);
  //*/
  // end android specifics
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

// start android specifics
// from Ketai and Android
// 
///*
public boolean surfaceTouchEvent(MotionEvent event) {
    //call to keep mouseX, mouseY, etc updated
    super.surfaceTouchEvent(event);
    //forward event to class for processing
    return ges.surfaceTouchEvent(event);
}
// 
//*/
// end android specifics

