// model

float currentVolume = 5.0,
      currentTone   = 5.0;
int   currentPickup = 0,
      currentSplit = 0,
      currentPreset = -1;


void tone(float theSliderVlaue) {
  if (slidersInit && currentTone != theSliderVlaue){
    currentTone = theSliderVlaue;
    println("tone event: " + theSliderVlaue);
    arduinoSetTone((int)currentTone);
  }
}

void volume(float theSliderVlaue) {
  if (slidersInit && currentVolume != theSliderVlaue){
    currentVolume = theSliderVlaue;
    println("volume event: "+ theSliderVlaue);
    arduinoSetVolume((int)currentVolume);
  }
}

void controlEvent(ControlEvent theEvent) {
  if (allInit){    
    String msg = theEvent.getName() +" event: ";  
    if(theEvent.isFrom(r)){
      setPickup(msg,int(theEvent.getValue()));
    }
    else if(theEvent.isFrom(s))  {
      setSplit(msg, int(theEvent.getValue()));
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

void setPickup(String msg, int eventId) {
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

void setSplit(String msg, int eventId) {
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

void setPreset (String msg, int eventVal){
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

void arduinoSetPickup(int pickup) {
  println("arduinoSetPickup: " + pickup);
}
void arduinoSetSplit(int split) {
  println("arduinoSetSplit: " + split);
}
void arduinoSetVolume(int vol) {
  println("arduinoSetVolume: " + vol);
}
void arduinoSetTone(int tone) {
  println("arduinoSetTone: " + tone);
 }


void inputFileSelected(File selection) {
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

void doWritePresets(){
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
    
void outputFileSelected(File selection) {
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

void doWriteCurrentPreset() {
  String s = l.getItem(currentPreset).getName();
  println("Writing current preset to presetsA " + s);
  String currentSettings[] = { s,
                              str(int(currentVolume)),
                              str(int(currentTone)),
                              str(currentPickup),
                              str(currentSplit) };
  presetsA.set(currentPreset, currentSettings);
  println("This is the preset that was written:");
  println(presetsA.get(currentPreset));
}

void doDeleteCurrentPreset() {
  println("Deleting current preset, and there is no current one anymore...");
  presetsA.remove(currentPreset);
  l.setLabel("");
  l.clear();
  loadData(l);
  currentPreset=-1;
}

void doRenameCurrent(String newName){
  println("doRenameCurrent with newName: " + newName);
  String currentSettings[] = { newName,
                              str(int(currentVolume)),
                              str(int(currentTone)),
                              str(currentPickup),
                              str(currentSplit) };
  presetsA.set(currentPreset, currentSettings);
  t.setVisible(false);
  l.clear();
  l.setVisible(true);
  loadData(l);
  l.captionLabel().set(l.getItem(currentPreset).getName());
}

void  doNewName(String nm) {
  println("doNewName calles with : " + nm);
  String currentSettings[] = { nm,
                              str(int(currentVolume)),
                              str(int(currentTone)),
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

