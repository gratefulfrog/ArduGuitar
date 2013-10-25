
#include "autoClass.h"

void autoClass::load() {
  // this is until we have an SD card to read
  currentIndex = new cyclerClass(2);
  presetDelayLis = new int*[nbAutoPresets]; 
  for (int i=0; i< nbAutoPresets; i++){
    presetDelayLis[i] = new int[2];
    presetDelayLis[i][0] = autoPresetLis[i][0];
    presetDelayLis[i][1] = autoPresetLis[i][1];
  } 
  lastAutoTime = 0;
}
     
autoClass::autoClass(): state(2){
  state.setVal(0);  // to get it up from -1 to 0 !!
  currentIndex->setVal(0);
  load();
}
boolean autoClass::running() const{
  return state.getState() > 0;
}
int autoClass::inc() {
  // return the index after inc
  state.incState();
  if (running()){
    lastAutoTime = millis();
    currentIndex->setVal(0);
  }
  return presetDelayLis[currentIndex->getState()][0];
}  

int autoClass::check(){
  long now = millis();
  if (now - lastAutoTime > presetDelayLis[currentIndex->getState()][1]) { //then next preset
    currentIndex->incState();
    lastAutoTime = now;
  }
  return presetDelayLis[currentIndex->getState()][0];
}
