/* TimerThreadTest
 * Uses a Timer to change the display
 * while allowing mouse interaction
 */


Cycle c;

void setupCycle(){
  String names[] = {"1 sec", "2 sec", "3 sec", "4 sec"};
  int    delays[] = {1000,2000,3000,4000};
  
  c = new Cycle(names,delays);
  c.reset();
  c.startCycle(); 
}  

void setupDisplay(){
  size(200,200);
  background(255);
  fill(0);  
}

void setup() {
  setupDisplay();
  setupCycle();
}

void refreshDisplay(){
  background(255);
  text(c.currentName(),10,50);
}
void draw() {
  //System.out.println("in draw: ");
  if (c.cycleTimeUp()) {
    refreshDisplay();
    c.incCycle();
  }
}

void mouseClicked(){
  background(255);
  if(c.cycling()) {
    c.quit();
  }
  else{
    c.startCycle();
  }
  text("CLICK: cycle is active? " + c.cycling(),10,50);
}
