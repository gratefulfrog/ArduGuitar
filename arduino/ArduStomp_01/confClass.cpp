/* confClass.cpp
 * all the confs since we don't have a sd card
 */
 
#include "confClass.h"

const String confClass::onOffString[] = {"000","255"},// off,on, i.e. 0,1
             confClass::pickupPinStrings[]   = {"02", //neck
                                                "03", // middlePin
       		                                "04", //bridgePin
                                                "05"},  // splitPin
             confClass::volPinStrings[] = {"09","10","12"},
             confClass::tonePinString    = "11",
             confClass::volSettingsStrings[][6] = {{"000","012","014","018","027","255"},  // volPWM[0]-> volPins[0]
    		                                   {"255","030","020","015","013","000"},  // volPWM[1]-> volPins[1]
		                                   {"000","000","000","000","000","255"}}, // 3rd vactrol for max volume: volPWM[2]-> volPins[2]
             confClass::toneSettingsStrings[] = {"255","090","046","027","017","000"};  // tone levels: [0,1,2,3,4,5]
  
const int confClass::presets[][5] =  //vol, tone, neck, middle, bridge
                                    {{0,   0,    0,    0,      0},  //{3,   5,    0,    1,      1},  // 0
                                     {5,   2,    1,    1,      1},  // 1
                                     {5,   1,    1,    0,      0},  // 2
                                     {4,   5,    0,    1,      1}}, // 3
          confClass::autoSetting[] = {2, 200, 3, 200},
          confClass::nbPresets =  4;  // presetID, delayMillis ...
  
biInc confClass::vtSettings[2] = {biInc(5), 
                                  biInc(5)};  // vol tone
cyclerClass confClass::pupSettings[3] = {cyclerClass(2),
                                         cyclerClass(2), 
                                         cyclerClass(3)}; // neck, middle, bridge


String confClass::setVT(int id, int val){
  String ret = "";
  if (val >= 0 &&
      val <= 5 && 
      vtSettings[id].getVal() !=val) { // then there's something to do
    vtSettings[id].setVal(val);
    ret += vtString(id);
  }
  return ret;
}
  
String confClass::setPreset(int pid) { // pid is a preset id
  String ret = "";
  // first vol and tone
  int i=0;
  for (; i<2;i++){
    ret += setVT(i, presets[pid][i]);
  }
  for(int j=0;i<5;j++,i++){
    ret+= setPup(j, presets[pid][i]);
  }
  return ret;
}
String confClass::vtString (int i){
  int val = vtSettings[i].getVal();
  //Serial.print ("calling vtString on: " + String(i) + " with val: " + String(val) + "\n");
  String ret = "";
  if (i == 1){  // tone to do
    ret += tonePinString + toneSettingsStrings[val];
  }
  else {
    for (int i=0;i < 3; i++){
      ret += volPinStrings[i] + volSettingsStrings[i][val];
    }
  }
  return ret;
}

String confClass::pupString(int i){
  int v = pupSettings[i].getVal();
  String ret = "";
  if (i < 2){    
    ret += pickupPinStrings[i]  + onOffString[v];
  }
  else {
    switch(v) {
      case 0:  // bridge off
        ret += pickupPinStrings[2] + onOffString[0] + pickupPinStrings[3] + onOffString[0];
        break;
      case 1:  // bridge both
        ret += pickupPinStrings[2] + onOffString[1] + pickupPinStrings[3] + onOffString[0];
        break;
      case 2:  // bridge split
        ret += pickupPinStrings[2] + onOffString[1] + pickupPinStrings[3] + onOffString[1];
        break;
    }
  }
  return ret;
}
    
String confClass::setPup(int i, int v) {
  String ret = "";
  if ((v <2 || (i==2 && v<3)) &&
      pupSettings[i].getVal() != v)  { // something to do
    pupSettings[i].setVal(v);
    ret += pupString(i);
  }
  return ret;
}
  
// public:
confClass::confClass(): currentPreset(4){
  setPreset(currentPreset.getVal());
  }

String confClass::incVT(int i, int sens){ // id =0 Vol, id = 1 tone
  String ret = "";
  int oldVal = vtSettings[i].getVal();
  vtSettings[i].inc(sens);
  int newVal = vtSettings[i].getVal();
  if (newVal != oldVal) { //something to do
    ret += vtString (i);
  }
  
  return ret;
}
  
String confClass::incPup(int i) {  // always something to do
  pupSettings[i].incState();
  return pupString(i);
}

String confClass::incPreset(){
  currentPreset.incState();
  return setPreset(currentPreset.getVal());
}  


