// cycle_tester stuff testing

int winX = 300,
    winY = 200;

String defFile = "def.csv",
       defaultCycle = "N500B500";

void setup() {
  size(winX,winY);
  // read the cycle line from the presets file,
  // that gives the name of the cycle file
  // read the cycle file
  // conf for cycling with a button press,
  // need on/off buttons
  line(winX/2,0,winX/2,winY);
  textAlign(CENTER,CENTER);
  textSize(48);
  text("On",winX/4,winY/2);
  text("Off",3*winX/4,winY/2);
  println("leaving setup...");  
}

void cycleOn(){
  // read the cycle file 
  // start sending cycle commands
}

void cycleOff(){ 
  // stop sending cycle commands
}

void mousePressed(){
  if (mouseX > winX/2){
    doOff();
  }
  else {
    doOn();
  }
}

void doOn(){
  println ("clicked: ON");
  load();
}

void doOff(){ 
  println ("clicked: OFF");
  exit();
}

void load(){
  Table tv = null;
  String s = "";
  try {
      tv = loadTable(defFile, "csv");  
  } 
  catch (Exception e) {  
      println("Table load failed: " + e);
      tv = null;  
      println("failed to open, creating new default cycle...");
      s = defaultCycle;
  }
  if (tv != null) {
    int c = tv.getColumnCount();
    for (int i=0;i<c;i++){
      s += tv.getString(0,i);
    }
  }
  println(s);
}

void draw() {
}
