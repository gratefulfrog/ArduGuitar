import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import controlP5.*; 
import processing.serial.*; 
import java.awt.Rectangle; 
import java.util.ArrayList; 
import g4p_controls.*; 
import controlP5.*; 
import controlP5.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class gui_00_no_serial extends PApplet {

// gui_00 using ControlP5 some trials...


 

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

public boolean initArduino(){
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

public void doGuiInit() {
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

public void setup() {
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
  
public void draw() {
  background(winBackgroundColor);
  stroke(60);
  fill(winBackgroundColor);
  rect(rectP[x],rectP[y],rectP[dX],rectP[dY]);
  rect(rectS[x],rectS[y],rectS[dX],rectS[dY]);
}

public void serialEvent(Serial aPort){
  //println("Serial event!");
 
  // read the buffer
  String inputString = "Received from Arduino: \"" + aPort.readStringUntil('\n');
  print(inputString);
}
// dialogs tab

boolean bigG = false,
        isRename = false;

String small = "16x16",
       big   = "22x22",
       imageName[] = { "go-jump-3-",
                       "format-text-strikethrough-2-",
                       "list-add-3-", 
                       "list-remove-3-",
                       "document-save-3-",
                       "document-open-5-"},
       imageExt  = ".png";

public String getImage(int i) {
  if (bigG){
  return imageName[i] + big + imageExt;
  }
  else{
  return imageName[i] + small + imageExt;
  }
}

public boolean initButtons(ControlP5 cp5) {
  //String image = getImage();  
  int x1 = rectLb[x],
      y1 = rectV[y];
      
  Button b0 =  cp5.addButton("writeCurrentButton")
                 .setValue(0)
                 .setPosition(x1,y1)
                 .registerTooltip("Write Current Preset")
                 .setImage(loadImage(getImage(0)))
                 .updateSize()
                 ;
 
  x1 += b0.getWidth();
  Button b1 = cp5.addButton("renameCurrentButton")
                 .setValue(1)
                 .setPosition(x1,y1)
                 .registerTooltip("Rename Current Preset")
                 .setImage(loadImage(getImage(1)))
                 .updateSize()
                 ;
  x1 += b1.getWidth();                 ;
  Button b2 = cp5.addButton("writeNewButton")
                 .setValue(2)
                 .setPosition(x1,y1)
                 .registerTooltip("Create New Preset")
                 .setImage(loadImage(getImage(2)))
                 .updateSize()
                 ;
  x1 += b2.getWidth();                 ;
  Button b3 = cp5.addButton("deleteCurrentButton")
                 .setValue(3)
                 .setPosition(x1,y1)
                 .registerTooltip("Delete Current Preset")
                 .setImage(loadImage(getImage(3)))
                 .updateSize()
                 ;
  x1 += b3.getWidth();                 ;
  Button b4 = cp5.addButton("saveButton")
                 .setValue(4)
                 .setPosition(x1,y1)
                 .registerTooltip("Save Preset File")
                 .setImage(loadImage(getImage(4)))
                 .updateSize()
                 ;
  x1 += b4.getWidth();                 ;
  Button b5 = cp5.addButton("openButton")
                 .setValue(5)
                 .setPosition(x1,y1)
                 .registerTooltip("Open Preset File")
                 .setImage(loadImage(getImage(5)))
                 .updateSize()
                 ;
  cp5.getTooltip().getLabel().toUpperCase(false);
  println("Buttons initialized.");   
  return true;
}  

/*
void writeCurrentButton(int val){
  println("writeCurrentButton received " + val);
}
*/

public void renameCurrentButton(int val){
  if (allInit){
    isRename = true;
    println("renameCurrentButton received " + val);
    l.setVisible(false);
    t.setText(l.captionLabel().getText());  
    t.setVisible(true);
    t.setFocus(true);
    t.keepFocus(true);
  }
}

public void writeNewButton(int val){
  if (allInit){
    println("writeNewButton received " + val);
    l.setVisible(false);
    t.setText(newPresetDefaultName);  
    t.setVisible(true);
    t.setFocus(true);
    t.keepFocus(true);
  }
}

/*

void deleteCurrentButton(int val){
  println("deleteCurrentButton received " + val);
}

void saveButton(int val){
  println("saveButton received " + val);
}


void openButton(int val){
  println("openButton received " + val);
 
}

*/


// file_ops
// read/write presets file

String defaultPresetsFile = "presets.csv" ; //"/home/bob/.presets.csv";
String currentPresetsFile = defaultPresetsFile; 

ArrayList presetsA = new ArrayList();  // this is where the presets are stored

public int getPresetVolume(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[1]);
}
public int getPresetTone(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[2]);
}

public int getPresetPickup(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[3]);
}
public int getPresetSplit(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[4]);
}
String headerLine = "n,v,t,s,l";

public void readConfig(String fileName) {
  // read all the presets from the fileName
  println("Reading file: " + fileName);
  presetsA = new ArrayList(); 
  String lines[] = loadStrings(fileName);
  for (int i=1;i<lines.length;i++){
    addConfig(lines[i]);
  }
}

public void readDefaultConfig(){
  String def =  new String("Default,5,5,0,0");
  addConfig("Default,5,5,0,0");
}

public void addConfig(String str){
  presetsA.add(split(str,','));
  println("Adding config: " + str);
}

public void writeConfig(String fileName) {
  PrintWriter output = createWriter(fileName);
  println("Writing file: " + fileName);
  println("Writing Header Line : " + headerLine);
  output.println(headerLine); 
  for (int i = 0 ; i < presetsA.size(); i++) {
    String line = join((String[])presetsA.get(i),",");
    println("Writing Config Line : " + line);
    output.println(line);
  }   
  output.flush();
  output.close();
}

public boolean initPresets(){
  File f = new File(dataPath(currentPresetsFile));
  if (!f.exists()) {
    println("Default Presets File does not exist");
    readDefaultConfig();
  }
  else {
   readConfig(currentPresetsFile);
   println("Presets initialized.");
  }
 return true;
}

// g4p stuff that is missing in ControlP5






public boolean initG4PStuff() {
  return true;
}

// listBox tests



ListBox l;
Textfield t;

String newName = "",
       newPresetDefaultName = "New";

int itemH = 21,
    nbItems = 11;
int rectLb[] = {3*rectP[0]+rectP[2], 
                3*itemH, 
                win[x]-rectP[x]-3*rectP[0]-rectP[2], 
                nbItems*itemH}; 

public boolean initListBox(ControlP5 cp5) {  
  //ControlP5.printPublicMethodsFor(ListBoxItem.class);
  t = cp5.addTextfield("newName")
     .setPosition(rectLb[x], rectLb[y] - itemH )
     .setSize(rectLb[dX], itemH )
     .setFont(createFont("Free Sans",12))
     .setFocus(false)
     .setColor(labelColor)
     .setLabel("")
     ;
  t.setVisible(false);
  
  l = cp5.addListBox("presets")
         .setPosition(rectLb[x], rectLb[y])
         .setSize(rectLb[dX], rectLb[dY])           
         .setItemHeight(itemH)
         .setBarHeight(itemH)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         ;
  l.toUpperCase(false);
  l.captionLabel().toUpperCase(false);
  l.captionLabel().set("Presets");
  l.captionLabel().setColor(labelColor);
  l.captionLabel().style().marginTop = 3;
  l.valueLabel().style().marginTop = 3;
  l.captionLabel().setFont(createFont("Free Sans",12));
  l.valueLabel().setFont(createFont("Free Sans",12));
  l.valueLabel().toUpperCase(false);

  loadData(l);  
  l.captionLabel().set(l.getItem(0).getName());
  l.disableCollapse();
  println ("listBox initialized.");
  return true;
}

public void loadData(ListBox l){
  for (int i = 0 ; i < presetsA.size(); i++) {
    String []line = (String[])presetsA.get(i);
    println("Loading listBox item: " + line[0]);
    ListBoxItem lbi = l.addItem(line[0], i);
    lbi.setColorBackground(itemBackgroundColor);
  }
}

public void loadPreset(int n){
  l.setValue(0);
}


// model

float currentVolume = 5.0f,
      currentTone   = 5.0f;
int   currentPickup = 0,
      currentSplit = 0,
      currentPreset = -1;


public void tone(float theSliderVlaue) {
  if (slidersInit && currentTone != theSliderVlaue){
    currentTone = theSliderVlaue;
    println("tone event: " + theSliderVlaue);
    arduinoSetTone((int)currentTone);
  }
}

public void volume(float theSliderVlaue) {
  if (slidersInit && currentVolume != theSliderVlaue){
    currentVolume = theSliderVlaue;
    println("volume event: "+ theSliderVlaue);
    arduinoSetVolume((int)currentVolume);
  }
}

public void controlEvent(ControlEvent theEvent) {
  if (allInit){    
    String msg = theEvent.getName() +" event: ";  
    if(theEvent.isFrom(r)){
      setPickup(msg,PApplet.parseInt(theEvent.getValue()));
    }
    else if(theEvent.isFrom(s))  {
      setSplit(msg, PApplet.parseInt(theEvent.getValue()));
    }
    else if (theEvent.isGroup() && theEvent.name().equals("presets")){
      setPreset(msg, (int)theEvent.group().value());
    }
    else if (theEvent.name().equals("openButton")){
      selectInput("Open a Presets file", "inputFileSelected");
    }
    else if (theEvent.name().equals("saveButton")){
     doWritePresets();
    }
    else if (theEvent.name().equals("writeCurrentButton")){
      doWriteCurrentPreset();
    }
    else if (theEvent.name().equals("deleteCurrentButton")){
      doDeleteCurrentPreset();
    }    
    else if(theEvent.isAssignableFrom(Textfield.class)) {
      if (isRename){
        doRenameCurrent(theEvent.getStringValue());
        isRename = false;
      }
      else { 
        doNewName(theEvent.getStringValue());
      } 
    }
  }
}

public void setPickup(String msg, int eventId) {
  switch(eventId){
    case(-1):
      r.activate(pickupActivationMap[currentPickup]); 
      break;
    case(0): msg += "neck"; break;
    case(1): msg += "neck middle"; break;
    case(2): msg += "middle"; break;
    case(3): msg += "middle bridge"; break;
    case(4): msg += "bridge"; break;
    case(5): msg += "neck brdige"; break;
    case(6): msg += "neck middle bridge"; break;
  }
  if(eventId>-1 && currentPickup != eventId) {
    currentPickup = eventId;
    println(msg);
    arduinoSetPickup(currentPickup);
  }
}

public void setSplit(String msg, int eventId) {
  switch(eventId){
    case(-1): 
      s.activate(splitActivationMap[currentSplit]); 
      break;
    case(0): msg += "both"; break;
    case(1): msg += "split"; break;
  }
  if(eventId>-1 && currentSplit != eventId) {
    currentSplit = eventId;
    println(msg);
    arduinoSetSplit(currentSplit);
  }
}

public void setPreset (String msg, int eventVal){
  println(msg + " event: " + eventVal);  
  if (eventVal != currentPreset){
    currentPreset = eventVal;
    Slider vSlider = cp5.get(Slider.class,"volume");
    vSlider.setValue(getPresetVolume(eventVal));
    Slider tSlider = cp5.get(Slider.class,"tone");
    tSlider.setValue(getPresetTone(eventVal));
    r.activate(pickupActivationMap[getPresetPickup(eventVal)]);
    s.activate(splitActivationMap[getPresetSplit(eventVal)]);

    ListBox l = cp5.get(ListBox.class,"presets");
    l.captionLabel().set(l.getItem(eventVal).getName());
  }  
}

/* no serial
void arduinoSetPickup(int pickup) {
  println("arduinoSetPickup: " + pickup);
  arduinoPort.write('s');
  arduinoPort.write(48 + pickup);
}
void arduinoSetSplit(int split) {
  println("arduinoSetSplit: " + split);
  arduinoPort.write('l');
  arduinoPort.write(48 + split);
}
void arduinoSetVolume(int vol) {
  println("arduinoSetVolume: " + vol);
  arduinoPort.write('v');
  arduinoPort.write(48 + vol);
}
void arduinoSetTone(int tone) {
  println("arduinoSetTone: " + tone);
  arduinoPort.write('t');
  arduinoPort.write(48 + tone);
}
*/

public void arduinoSetPickup(int pickup) {
  println("arduinoSetPickup: " + pickup);
}
public void arduinoSetSplit(int split) {
  println("arduinoSetSplit: " + split);
}
public void arduinoSetVolume(int vol) {
  println("arduinoSetVolume: " + vol);
}
public void arduinoSetTone(int tone) {
  println("arduinoSetTone: " + tone);
 }


public void inputFileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
  } else {
    currentPresetsFile = selection.getAbsolutePath();
    println("User selected " + currentPresetsFile);
    readConfig(currentPresetsFile);
    l.clear();
    loadData(l);
    currentPreset = -1;
    loadPreset(0); //currentPreset);
  }
}

public void doWritePresets(){
  boolean askOverWrite = false;
  if (currentPresetsFile == defaultPresetsFile) { askOverWrite = true; }
  else {
    File f = new File(dataPath(currentPresetsFile));  
    if (f.exists()) { askOverWrite = true; }
  }
    
  if (askOverWrite) { // need to ask!
    println("File exists!");
    println("open msg dialog to confirm overwrite.");
    int reply = G4P.selectOption(this, 
                                 "Overwrite " + currentPresetsFile + " ?",
                                 "Warning", 
                                 G4P.WARNING,
                                 G4P.OK_CANCEL);
     if(reply == G4P.OK) { // just do it
       writeConfig(currentPresetsFile); 
     }
     else { // do not overwrite, means asking for new file
       selectInput("Save Presets to file", "outputFileSelected");
     }    
  }
  else { // don't need to ask ! 
    selectInput("Save Presets to file", "outputFileSelected");
  } 
}
    
public void outputFileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
  } else {
    String fName = selection.getAbsolutePath();
    println("User selected " + fName);
    File f = new File(dataPath(fName));
    boolean doWrite = false;
    if (!f.exists()) {
      println("File does not exist");
      doWrite = true;
    }
     else {
       println("open msg dialog to confirm overwrite.");
       int reply = G4P.selectOption(this, 
                                   "File exists! Overwrite?",
                                   "Warning", 
                                   G4P.WARNING,
                                   G4P.OK_CANCEL);
       if(reply == G4P.OK) { doWrite = true; }
     }
     if(doWrite){
       currentPresetsFile = selection.getAbsolutePath();
       writeConfig(currentPresetsFile);
     }
  }
}

public void doWriteCurrentPreset() {
  String s = l.getItem(currentPreset).getName();
  println("Writing current preset to presetsA " + s);
  String currentSettings[] = { s,
                              str(PApplet.parseInt(currentVolume)),
                              str(PApplet.parseInt(currentTone)),
                              str(currentPickup),
                              str(currentSplit) };
  presetsA.set(currentPreset, currentSettings);
  println("This is the preset that was written:");
  println(presetsA.get(currentPreset));
}

public void doDeleteCurrentPreset() {
  println("Deleting current preset, and there is no current one anymore...");
  presetsA.remove(currentPreset);
  l.setLabel("");
  l.clear();
  loadData(l);
  currentPreset=-1;
}

public void doRenameCurrent(String newName){
  println("doRenameCurrent with newName: " + newName);
  String currentSettings[] = { newName,
                              str(PApplet.parseInt(currentVolume)),
                              str(PApplet.parseInt(currentTone)),
                              str(currentPickup),
                              str(currentSplit) };
  presetsA.set(currentPreset, currentSettings);
  t.setVisible(false);
  l.clear();
  l.setVisible(true);
  loadData(l);
  l.captionLabel().set(l.getItem(currentPreset).getName());
}

public void  doNewName(String nm) {
  println("doNewName calles with : " + nm);
  String currentSettings[] = { nm,
                              str(PApplet.parseInt(currentVolume)),
                              str(PApplet.parseInt(currentTone)),
                              str(currentPickup),
                              str(currentSplit) };
  presetsA.add(currentSettings);
  t.setVisible(false);
  l.clear();
  l.setVisible(true);
  loadData(l);
  currentPreset = presetsA.size() -1;
  l.captionLabel().set(l.getItem(currentPreset).getName());
}

// radios



RadioButton r,s;

int pickupActivationMap[] ={5, 11, 7, 13, 9, 2, 17},
    splitActivationMap[] = {0,1};

public boolean initSelectors(ControlP5 cp5){
  r = cp5.addRadioButton("pickupSelector")
         .setPosition(20,130)
         .setSize(120,25)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         .setItemsPerRow(5)
         .setSpacingColumn(-55)
         .setSpacingRow(5)    
         .addItem("null1",-1)
         .addItem("null2",-1)
         .addItem("Neck Bridge",5)
         .addItem("null4",-1)
         .addItem("null5",-1)
         .addItem("Neck",0)
         .addItem("null7",-1)
         .addItem("Middle",2)
         .addItem("null9",-1)
         .addItem("Bridge",4)
         .addItem("null11",-1)
         .addItem("Neck Middle",1)
         .addItem("null13",-1)
         .addItem("Middle Bridge",3)
         .addItem("null15",-1)
         .addItem("null16",-1)
         .addItem("null17",-1)
         .addItem("Neck Middle Bridge",6)
         .addItem("null19",-1)
         .addItem("null20",-1)
         ;
  r.activate(5);      

  for(Toggle t:r.getItems()) {
    if(t.captionLabel().getText().charAt(1) == 'u'){
      t.setVisible(false);
      t.setSize(0,0);
    }
    t.captionLabel().align(ControlP5.CENTER,ControlP5.CENTER);
    t.captionLabel().toUpperCase(false);
    t.captionLabel().setFont(createFont("Free Sans",12));
  }
  
  s = cp5.addRadioButton("splitSelector")
         .setPosition(140,260)
         .setSize(70,20)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         .setItemsPerRow(2)
         .setSpacingColumn(2)       
         .addItem("Both",0)
         .addItem("Split",1)
         ;
  s.activate(0);
  
  for(Toggle t:s.getItems()) {
    t.captionLabel().align(ControlP5.CENTER, ControlP5.CENTER);
    t.captionLabel().toUpperCase(false);
    t.captionLabel().setFont(createFont("Free Sans",12));
  }
  arduinoSetPickup(currentPickup);
  arduinoSetSplit(currentSplit);
  println("Radios initialized.");
  return true;
}
/*
void keyPressed() {
  switch(key) {
    case('n'): r.activate(5); break;  // n: Neck
    case('m'): r.activate(7); break;  // m: Middle
    case('b'): r.activate(9); break;  // b: Bridge
    case('a'): r.activate(17); break; // a: All pickups
    case('l'): r.activate(11); break; // l: Left mix = neck + middle
    case('r'): r.activate(13); break; // r: Right mix = middle + bridge
    case('t'): r.activate(2); break;  // t: Top mix = neck + bridge
    case('s'): s.activate(1); break;  // s: Split
    case('u'): s.activate(0); break;  // u: Unsplit
  }
}
*/
// sliders

int rectV[] = {111,20,200,20};
int rectT[] = {rectV[x],4*rectV[y],rectV[dX],rectV[dY]};

public boolean initSliders(ControlP5 cp5) {
  cp5.addSlider("volume")
     .setBroadcast(false) 
     .setPosition(rectV[x],rectV[y])
     .setSize(rectV[dX],rectV[dY])
     .setRange(0,5)
     .setValue(5)
     .setNumberOfTickMarks(6)
     //.setSliderMode(Slider.FLEXIBLE)
     .setSliderMode(Slider.FIX)
     .setColorActive(itemActiveColor)
     .setColorForeground(itemForegroundColor)
     .setBroadcast(true)
     ;
  // reposition the value and caption Labels for controller 'tone'
  cp5.getController("volume").getValueLabel().setVisible(false);
  cp5.getController("volume").getCaptionLabel().align(ControlP5.CENTER, ControlP5.BOTTOM_OUTSIDE).setPaddingX(0);
  cp5.getController("volume").captionLabel().toUpperCase(false);
  cp5.getController("volume").getCaptionLabel().setFont(createFont("Free Sans",14));
  
  // add a vol/tone slider
  cp5.addSlider("tone")
     .setBroadcast(false)
     .setPosition(rectT[x],rectT[y])
     .setSize(rectT[dX],rectT[dY])
     .setRange(0,5)
     .setValue(5)
     .setNumberOfTickMarks(6)
     //.showTickMarks(false)
     //.setSliderMode(Slider.FLEXIBLE)
     .setSliderMode(Slider.FIX)
     .setColorActive(itemActiveColor)
     .setColorForeground(itemForegroundColor)
     .setBroadcast(true)
     ;
  // reposition the value and caption Labels for controller 'tone'
  cp5.getController("tone").getValueLabel().setVisible(false); 
  cp5.getController("tone").getCaptionLabel().align(ControlP5.CENTER, ControlP5.BOTTOM_OUTSIDE).setPaddingX(0);
  cp5.getController("tone").captionLabel().toUpperCase(false);
  cp5.getController("tone").getCaptionLabel().setFont(createFont("Free Sans",14));
  
  arduinoSetVolume((int)currentVolume);
  arduinoSetTone((int)currentTone);
  println("Sliders initialized.");
  return true;
}

  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "gui_00_no_serial" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
