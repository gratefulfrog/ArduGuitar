// gui_00 using ControlP5 some trials...

import controlP5.*;
import processing.serial.*; 

ControlP5 cp5;

int winBackgroundColor = color(100),
    itemActiveColor = color(155),
    labelColor = color(255),
    itemForegroundColor = color(120),
    itemBackgroundColor = color(80);
    
boolean slidersInit   = false,
        selectorsInit = false,
        listBoxInit   = false,
        presetsInit   = false,
        initButtons   = false,
        initGP4s      = false,
        allInit       = false;

int x=0, y=1, dX=2, dY=3;

Serial arduinoPort;

int rectP[] = {16,126,386,122},
    rectS[] = {136,258,148,24},
    win[]   = {550,300};    

boolean initArduino(){
 boolean result = false;
 if (Serial.list().length>0){  
    String portName =Serial.list()[0];
    arduinoPort = new Serial(this, portName, 9600);
    println("Connected to arduino on " + portName);
    arduinoPort.bufferUntil('\n');
    result = true;
  } 
  else {
    println("No serial ports available.");
  }
  return result;
}

void doGuiInit() {
  slidersInit = initSliders(cp5);
  selectorsInit = initSelectors(cp5);
  presetsInit = initPresets();
  listBoxInit = initListBox(cp5);
  initButtons = initButtons(cp5);
  initGP4s = initG4PStuff();
  allInit = slidersInit && selectorsInit && listBoxInit && presetsInit && initButtons && initGP4s;
  println("allInit = " + allInit);
  loadPreset(0);
}

void setup() {
  size(win[x],win[y]);
  frame.setTitle("ArduGuitar");
  noStroke();
  cp5 = new ControlP5(this);
  /* no serial
  if (!initArduino()) { 
    exit();
  }
  else {
    doGuiInit();
    println("setup complete!");
  }
  */
  doGuiInit();
  println("setup complete!");
}  
  
void draw() {
  background(winBackgroundColor);
  stroke(60);
  fill(winBackgroundColor);
  rect(rectP[x],rectP[y],rectP[dX],rectP[dY]);
  rect(rectS[x],rectS[y],rectS[dX],rectS[dY]);
}

void serialEvent(Serial aPort){
  //println("Serial event!");
 
  // read the buffer
  String inputString = "Received from Arduino: \"" + aPort.readStringUntil('\n');
  print(inputString);
}
