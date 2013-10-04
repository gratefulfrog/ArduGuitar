/* ArduStomp_01
 * code to command the ARduGuitar from an arduino based stomp box.
 */

#define DEBUG
#include <Arduino.h>
#include "biInc.h" 
#include "cyclerClass.h" 
#include "confClass.h" 

#define VUP_PIN 1
#define VDW_PIN 2
#define TUP_PIN 3
#define TDW_PIN 4
#define N_PIN   5
#define M_PIN   6
#define B_PN    7
#define P_PIN   8
#define A_PIN   9

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

const String buttonNames[] = {"Vol Up",
                              "Vol Down",
                              "Tone Up",
                              "Tone Down",
                              "Neck",
                              "Middle",
                              "Bridge",
                              "Preset",
                              "Auto"};

confClass conf;

boolean neckLed = false,
        middleLed = false,
        bridgeLed[] = {false,false},
        volLed[] = {false,false,false,false,false},
        toneLed[] = {false,false,false,false,false},        
        presetsLed[] = {false,false,false,false},
        autoLed = false,
        powerLed = true,
        connectLed = false;

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
String volUp(){
  String ret = conf.incVT(0,1);
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  //msg("called VolUp, returning: " + ret);
  return ret;
}

String volDown(){
  String ret = conf.incVT(0,-1);
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  //msg("called VolDown, returning: " + ret);
  return ret;
}

String toneUp(){
  String ret = conf.incVT(1,1);
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  //msg("called toneUp, returning: " + ret);
  return ret;
}
String toneDown(){
  String ret = conf.incVT(1,-1);
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());  
  //msg("called toneDown, returning: " + ret);
  return ret;
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

String neck(){
  String ret = conf.incPup(0);
  setNeckLed();
  return ret;
}
String middle(){
  String ret = conf.incPup(1);
  setMiddleLed();
  return ret;
}
String bridge(){
  String ret = conf.incPup(2);
  setBridgeLed();
  return ret;
}

void setPresetLed(){
  for(int i = 0; i<conf.nbPresets;i++){
    presetsLed[i] = false;
  }
  presetsLed[conf.currentPreset.getState()] = true;  
}

String preset() {
  String ret =  conf.incPreset();  
  setPresetLed();
  return ret;
}

String autoL(){;}


typedef String (*buttonFuncPtr)();

buttonFuncPtr buttonFuncs[]= { &volUp,     
                               &volDown,
                               &toneUp,
                               &toneDown,
                               &neck,
                               &middle,
                               &bridge,
                               &preset,
                               &autoL};



void msg(String s){
  #ifdef DEBUG
  Serial.print(s + '\n');
  #endif
}

void setupPins(){
   for (int i=0;i<nbButtons;i++){
     pinMode(pins[i],INPUT);
   }
   msg("Pins setup!");
}

void setupData(){
  msg("Setup Data!");
  commBT(conf.incPreset());
  vtLeds(volLed,5,conf.vtSettings[0].getVal());
  vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  setNeckLed();
  setMiddleLed();
  setBridgeLed();
  setPresetLed();
}

void commBT(String s){
  msg("BT Send: " + s);
}

boolean buttonPressedNow(int i){
 // just for tests
 int pressed[] =  {0,0,0,0,0,
                   1,1,1,1,1,
                   2,2,2,2,2,
                   3,3,3,3,3,
                   4,4,
                   5,5,
                   6,6,6,
                   7,7,7,7};
 static int current = 0;
 boolean result =  i== pressed[current];
 if (result){
   current = (current + 1)% 31;
   msg("pressed: "+ String(i) + ": " + buttonNames[i]);
   
 }
 return  result;
}

void checkButtons(){
  for (int i=0;i<nbButtons;i++){
    if(buttonPressedNow(i)){
      commBT((*buttonFuncs[i])());
      break;
    }    
  }
}


void setLeds(){
  showLeds();
}

void showLeds(){
  msg("Power: " +String(powerLed));
  msg("Connected: " +String(connectLed));
  msg("Neck: " +String(neckLed));
  msg("Middle: " +String(middleLed));
  String s = "Bridge: ";
  for (int i=0;i<2;i++){
    s += String(bridgeLed[i]) +" ";
  }
  msg(s);
  s = "Vol: ";
  for (int i=0;i<5;i++){
    s += String(volLed[i])  +" ";
  }
  msg(s);
  s = "Tone: ";
  for (int i=0;i<5;i++){
    s += String(toneLed[i]) +" ";
  }
  msg(s);
  s = "Preset: ";
  for (int i=0;i<4;i++){
    s += String(presetsLed[i]) +" ";
  }
  msg(s);
}

void setup(){
   Serial.begin(9600);
   msg("Starting...");
   setupPins();
   setupData();
   setLeds();
   msg("5 seconds delay...");
   delay (5000);
 }

void loop(){
  msg("\n\n=======");
  checkButtons();
  //msg("vol val: " + String(conf.vtSettings[0].getVal()));
  setLeds();
  delay(2000);
}

