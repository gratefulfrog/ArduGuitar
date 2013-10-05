/* ArduStomp_01
 * code to command the ARduGuitar from an arduino based stomp box.
 */

#include <Arduino.h>
#include "confClass.h" 
#include "actuatorClass.h"

#define VUP_PIN 2
#define VDW_PIN 3
#define TUP_PIN 4
#define TDW_PIN 5
#define N_PIN   6
#define M_PIN   7
#define B_PN    8
#define P_PIN   9
#define A_PIN   10

int pins[]= {VUP_PIN,
             VDW_PIN,
             TUP_PIN,
             TDW_PIN,
             N_PIN,
             M_PIN,
             B_PN,
             P_PIN,
             A_PIN };

const int nbButtons = 9;

confClass conf;

// LED status
boolean neckLed = false,
        middleLed = false,
        bridgeLed[] = {false,false},
        volLed[] = {false,false,false,false,false},
        toneLed[] = {false,false,false,false,false},        
        presetsLed[] = {false,false,false,false},
        autoLed = false,
        powerLed = true,
        connectLed = false;

////////////////////////////////////////////////////////////
////////////////////// for debugging  //////////////////////
////////////////////////////////////////////////////////////
/// these show*Led* fucntions need to be replaced with calls
/// that actuall control the leds!
/////
const String buttonNames[] = {"Vol Up",
                              "Vol Down",
                              "Tone Up",
                              "Tone Down",
                              "Neck",
                              "Middle",
                              "Bridge",
                              "Preset",
                              "Auto"};
void showVolLeds(){
  String   s = "Vol: ";
  for (int i=0;i<5;i++){
    s += String(volLed[i])  +" ";
  }
  msg(s);
}

void showNeckLed(){
  msg("Neck: " +String(neckLed));
}
void showMiddleLed(){
  msg("Middle: " +String(middleLed));
}
void showBridgeLeds(){
  String s = "Bridge: ";
  for (int i=0;i<2;i++){
    s += String(bridgeLed[i]) +" ";
  }
  msg(s);
}  
void showToneLeds(){
  String  s = "Tone: ";
  for (int i=0;i<5;i++){
    s += String(toneLed[i]) +" ";
  }
  msg(s);
}
void showPresetLeds(){
String  s = "Preset: ";
  for (int i=0;i<4;i++){
    s += String(presetsLed[i]) +" ";
  }
  msg(s);
}
void showPowConLeds(){
  msg("Power: " +String(powerLed));
  msg("Connected: " +String(connectLed));
}  
void showLeds(){
  showPowConLeds();
  showNeckLed();
  showMiddleLed();
  showBridgeLeds();
  showVolLeds();
  showToneLeds();
  showPresetLeds();
}

////////////////////////////////////////////////////////////
////////////////////// end debugging  //////////////////////
////////////////////////////////////////////////////////////

void vtLeds(boolean arr[],int nb,int level){
  // set leds for vol, tone, presets
  for(int i=0;i<nb;i++){
    if (i< level){
      arr[i] = true;
    }
    else {
      arr[i] =  false;
    }
  }
}

long lastActionTime = 0;
const long minActionDelay = 300;

boolean actionDelayOK(){
  // don't allow more than one button press per unit of minActionDelay!
  if(millis()-lastActionTime > minActionDelay){
    lastActionTime = millis();
    return true;
  }
  else{
    return false;
  }
}
void testAndSend(String s, void (*f)()){
  if (!s.equals("")){
    (*f)();
    commBT(s);
  }
} 
void volUp(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incVT(0,1);
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  testAndSend(ret,&showVolLeds);
}
void volDown(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incVT(0,-1);
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  testAndSend(ret,&showVolLeds);
}
void toneUp(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incVT(1,1);
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  testAndSend(ret,&showToneLeds);
}
void toneDown(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incVT(1,-1);
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());  
  testAndSend(ret,&showToneLeds);
}
void setNeckLed(){
  neckLed = conf.pupSettings[0].getState() >0;
}
void setMiddleLed(){
  middleLed = conf.pupSettings[1].getState() >0;
}
void setBridgeLed(){
  bridgeLed[0] = bridgeLed[1] = false;
  switch(conf.pupSettings[2].getState()){
    case 1:
      bridgeLed[1] = true;
    case 2:
      bridgeLed[0] = true;
  }
} 
void neck(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incPup(0);
  setNeckLed();
  testAndSend(ret,&showNeckLed);
}
void middle(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incPup(1);
  setMiddleLed();
  testAndSend(ret,&showMiddleLed);
}
void bridge(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incPup(2);
  setBridgeLed();
  testAndSend(ret,&showBridgeLeds);
}
void setPresetLed(){
  for(int i = 0; i<conf.nbPresets;i++){
    presetsLed[i] = false;
  }
  presetsLed[conf.currentPreset.getState()] = true;  
}
void preset() {
  if (!actionDelayOK()){
    return;
  }  
  String ret =  conf.incPreset(false);  
  setPresetLed();
  testAndSend(ret,&showPresetLeds);
}
// needs a true function here!
void autoL(){;}

doerFunPtr buttonFuncs[]= { &volUp,     
                            &volDown,
                            &toneUp,
                            &toneDown,
                            &neck,
                            &middle,
                            &bridge,
                            &preset,
                            &autoL};

void msg(String s){
  Serial.print(s + '\n');
}

actuatorClass *actuators[nbButtons];

void setupActuators(){
   for (int i=0;i<nbButtons;i++){
     actuators[i] = new actuatorClass(pins[i],buttonFuncs[i]);
   }
   msg("Actuators setup!");
}

void setupData(){
  commBT(conf.incPreset(true));
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  setNeckLed();
  setMiddleLed();
  setBridgeLed();
  setPresetLed();
  msg("Data setup!");
}

// needs to be updated for BT usage...
void commBT(String s){
  if(!s.equals(String(""))){
    msg("BT Send: " + s);
  }
}

/// needs to be updated to real version after debugging!
void  connectBT(){
  connectLed = true;
  msg("Connected!");
}

void setup(){
  delay (5000);
  Serial.begin(9600);
  msg("Starting...");
  setupActuators();
  setupData();
  connectBT();
  showLeds();
  msg("5 seconds delay...");
  delay (5000);
  msg("looping...");
 }

void loop(){
  for (int i = 0;i<nbButtons;i++){
    actuators[i]->update();
  }
}

