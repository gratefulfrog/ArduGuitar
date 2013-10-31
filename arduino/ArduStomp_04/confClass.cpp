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
          
biInc confClass::vtSettings[2] = {biInc(5), 
                                  biInc(5)};  // vol tone
      
cyclerClass confClass::pupSettings[3] = {cyclerClass(2),
                                         cyclerClass(2), 
                                         cyclerClass(3)}; // neck, middle, bridge

String confClass::setVT(byte id, byte val, boolean force){
  String ret = "";
  //Serial.print("at call  vtSettings[id].getVal() = " + String(vtSettings[id].getVal()));
  if (force || 
      (val >= 0 &&
       val <= 5 && 
       vtSettings[id].getVal() !=val)) { // then there's something to do
    vtSettings[id].setVal(val);
    ret += vtString(id);
  }
  //Serial.print("called confconfClass::setVT(" + String(id) +", " + String(val));

  //Serial.print("...returning: " + ret + ".\n");
  return ret;
}
// FIX
String confClass::setPreset(byte pid, boolean force) { // pid is a preset id
  String ret = "";
  /*
  // first vol and tone
  int i=0;
  for (; i<2;i++){
    ret += setVT(i, presets[pid][i],force);
  }
  for(int j=0;i<5;j++,i++){
    ret+= setPup(j, presets[pid][i], force);
  }
  */
  return ret;
}

String confClass::vtString (byte i){
  int val = vtSettings[i].getVal();
  //Serial.print ("calling vtString on: " + String(i) + " with val: " + String(val) + ".\n");
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

String confClass::pupString(byte i){
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
    
String confClass::setPup(byte i, byte v,boolean force) {
  String ret = "";
  if ((force ||(v <2 || (i==2 && v<3)) &&
                pupSettings[i].getVal() != v))  { // something to do
    pupSettings[i].setVal(v);
    ret += pupString(i);
  }
  return ret;
}
  
// public:
confClass::confClass(PresetClass *p, AutoClass *a): pre(p), aut(a){ //currentAutoIndex(0), lastAutoTime(0){
  setPreset(0,false);
  }

String confClass::getPresetString(byte presetIndex){
  String ret = "";
  // FIX
  return ret;
} 
String confClass::incVT(byte i, int sens){ // id =0 Vol, id = 1 tone
  String ret = "";
  int oldVal = vtSettings[i].getVal();
  //vtSettings[i].inc(sens);
  //int newVal = vtSettings[i].getVal();
  //if (newVal != oldVal) { //something to do
  if(vtSettings[i].inc(sens) != oldVal){
    ret += vtString (i);
  }
  
  return ret;
}
  
String confClass::incPup(byte i) {  // always something to do
  pupSettings[i].incState();
  return pupString(i);
}
// FIX
String confClass::incPreset(boolean force) {
  //currentPreset.incState();
  //return setPreset(currentPreset.getVal(),force);
  //return setPreset(currentPreset.incState(),force);
  return "";
}  


