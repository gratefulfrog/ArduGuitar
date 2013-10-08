/* ArduStomp_01
 * code to command the ARduGuitar from an arduino based stomp box.
 */

#include <Arduino.h>
#include "confClass.h" 
#include "actuatorClass.h"

// minimum millis between button presses
#define MIN_TIME_BETWEEN_BUTTON_PRESSES 100

#define VUP_PIN 2
#define VDW_PIN 3
#define TUP_PIN 4
#define TDW_PIN 5
#define N_PIN   6
#define M_PIN   7
#define B_PN    8
#define P_PIN   9
#define A_PIN   10

const int pins[]= {VUP_PIN,
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

// for led shift register shifting
//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin = 13;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin = 12;
////Pin connected to Data in (DS) of 74HC595
const int dataPin = 11;

const int ledArraySize =24;        
boolean leds[ledArraySize];

// these pairs say the LED starting index and how many there are in the button control group
const int volLedIndex[2] = {1,5},   
          neckLedIndex[2] = {6,1},
          middleLedIndex[2] = {7,1},
          toneLedIndex[2] = {9,5},   
          bridgeLedIndex[2] = {14,2},   
          presetLedIndex[2] = {17,4},   
          autoLedIndex[2] = {21,1},   
          powerLedIndex[2] = {22,1},   
          connectLedIndex[2] = {23,1};

const int *indexLis[] = {  volLedIndex,
                           neckLedIndex,
                           middleLedIndex,
                           toneLedIndex,
                           bridgeLedIndex,  
                           presetLedIndex,
                           autoLedIndex,
                           powerLedIndex,  
                           connectLedIndex};
  
#define VOL     0
#define NECK    1
#define MIDDLE  2
#define TONE    3
#define BRIDGE  4
#define PRESET  5
#define AUTO    6
#define POWER   7
#define CONNECT 8

// return a point to the part of the array where the thing starts
boolean* getBools(int indicator){
  return &leds[indexLis[indicator][0]];
}


// This method sends bits to the shift registers:
void registerWrite() {
  // turn off the output so the leds don't light up
  // while you're shifting bits:
  digitalWrite(latchPin, LOW);

  byte outgoing[] = {0,0,0};
  for (int i =0;i<24;i++){
    if (leds[i]){
      outgoing[int(i/8)] |= 1 <<(7 - (i%8));
    }
  }

  Serial.println("outgoing[0] = " + String(outgoing[0]));
  Serial.println("outgoing[1] = " + String(outgoing[1]));  
  Serial.println("outgoing[2] = " + String(outgoing[2]));  
  
  for (int i = 2;i>-1 ;i--){
    shiftOut(dataPin, clockPin, LSBFIRST, outgoing[i]);
  }
  // turn on the output so the LEDs can light up:
  digitalWrite(latchPin, HIGH);
}

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
  /*
  for (int i=0;i<5;i++){
    s += String(volLed[i])  +" ";
  }
  */
  for (int i=0;i<indexLis[VOL][1];i++){
    s += String(getBools(VOL)[i])  +" ";
  }
  msg(s);
  showLeds();
}

void showNeckLed(){
  msg("Neck: " +String(*getBools(NECK)));
  showLeds();
}
void showMiddleLed(){
  msg("Middle: " +String(*getBools(MIDDLE)));
  showLeds();
}
void showBridgeLeds(){
  String s = "Bridge: ";
  for (int i=0;i<indexLis[BRIDGE][1];i++){
    s += String(getBools(BRIDGE)[i]) +" ";
  }
  msg(s);
  showLeds();
}  
void showToneLeds(){
  String  s = "Tone: ";
  for (int i=0;i<indexLis[TONE][1];i++){
    s += String(getBools(TONE)[i]) +" ";
  }
  msg(s);
  showLeds();
}
void showPresetLeds(){
String  s = "Preset: ";
  for (int i=0;i<indexLis[PRESET][1];i++){
    s += String(getBools(PRESET)[i]) +" ";
  }
  msg(s);
  showLeds();
}
void showAutoLed(){
  msg("Auto: " +String(*getBools(AUTO)));
  showLeds();
}

void showPowConLeds(){
  msg("Power: " +String(*getBools(POWER)));
  msg("Connected: " +String(*getBools(CONNECT)));
  showLeds();
}  
void showLeds(){
  registerWrite();
  msg("LEDs updated!");
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
const long minActionDelay = MIN_TIME_BETWEEN_BUTTON_PRESSES;

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
  if (!s.equals("") || f == &showAutoLed){
    (*f)();
    commBT(s);
  }
} 
void volUp(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incVT(0,1);
  //vtLeds(volLed,5,conf.vtSettings[0].getVal());
  vtLeds(getBools(VOL),indexLis[VOL][1],conf.vtSettings[0].getVal());
  
  testAndSend(ret,&showVolLeds);
}
void volDown(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incVT(0,-1);
  //vtLeds(volLed,5,conf.vtSettings[0].getVal());
  vtLeds(getBools(VOL),indexLis[VOL][1],conf.vtSettings[0].getVal());
  testAndSend(ret,&showVolLeds);
}
void toneUp(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incVT(1,1);
  //vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  vtLeds(getBools(TONE),indexLis[TONE][1],conf.vtSettings[1].getVal());
  testAndSend(ret,&showToneLeds);
}
void toneDown(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incVT(1,-1);
  //vtLeds(toneLed,5,conf.vtSettings[1].getVal());  
  vtLeds(getBools(TONE),indexLis[TONE][1],conf.vtSettings[1].getVal());
  testAndSend(ret,&showToneLeds);
}
void setNeckLed(){
  // neckLed = conf.pupSettings[0].getState() >0;
  *getBools(NECK)  = conf.pupSettings[0].getState() >0;
}
void setMiddleLed(){
  //middleLed = conf.pupSettings[1].getState() >0;
  *getBools(MIDDLE) = conf.pupSettings[1].getState() >0;
}
void setBridgeLed(){
  getBools(BRIDGE)[0] = getBools(BRIDGE)[1] = false;
  switch(conf.pupSettings[2].getState()){
    case 1:
      getBools(BRIDGE)[1] = true;
    case 2:
      getBools(BRIDGE)[0] = true;
  }
} 
void neck(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incPup(0);
  setNeckLed();
  testAndSend(ret,&showNeckLed);
}
void middle(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incPup(1);
  setMiddleLed();
  testAndSend(ret,&showMiddleLed);
}
void bridge(){
  if (!actionDelayOK()){
    return;
  }
  autoOff();
  String ret = conf.incPup(2);
  setBridgeLed();
  testAndSend(ret,&showBridgeLeds);
}
void setPresetLed(){
  for(int i = 0; i<conf.nbPresets;i++){
    getBools(PRESET)[i] = false;
  }
  getBools(PRESET)[conf.currentPreset.getState()] = true;
  vtLeds(getBools(VOL),indexLis[VOL][1],conf.vtSettings[0].getVal());  
  vtLeds(getBools(TONE),indexLis[TONE][1],conf.vtSettings[1].getVal());
  setNeckLed();
  setMiddleLed();
  setBridgeLed();
}
void preset() {
  if (!actionDelayOK()){
    return;
  }
  autoOff();  
  String ret =  conf.incPreset(false);  
  setPresetLed();
  //testAndSend(ret,&showPresetLeds);
  testAndSend(ret,&showLeds);
}

void setAutoLed(){
  *getBools(AUTO)  = conf.autoRunning(); //conf.autoSettings.getState() >0;
}

// needs a true function here!
void autoIt(){
  if (!actionDelayOK()){
    return;
  }
  String ret = conf.incAuto();
  setAutoLed();
  setPresetLed();
  testAndSend(ret,&showLeds);
}

void autoOff(){
  if (conf.autoRunning()){
    conf.incAuto();
    setAutoLed();
  }
}

doerFunPtr buttonFuncs[]= { &volUp,     
                            &volDown,
                            &toneUp,
                            &toneDown,
                            &neck,
                            &middle,
                            &bridge,
                            &preset,
                            &autoIt};

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
  //vtLeds(volLed,5,conf.vtSettings[0].getVal());
  vtLeds(getBools(VOL),indexLis[VOL][1],conf.vtSettings[0].getVal());
  //vtLeds(toneLed,5,conf.vtSettings[1].getVal());
  vtLeds(getBools(TONE),indexLis[TONE][1],conf.vtSettings[1].getVal());
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
  *getBools(CONNECT) =  true;
  //connectLed = true;
  msg("Connected!");
}

void powerOn(){
  *getBools(POWER) =  true;
  msg("Power On!");
}

void checkAuto(){
  //String ret =  conf.incPreset(false);  
  String ret = conf.checkAuto();
  setPresetLed();
  testAndSend(ret,&showLeds);
}

void setup(){
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  for (int i=0;i<ledArraySize;i++){
    leds[i] = false;
  }
  delay (5000);
  Serial.begin(9600);
  msg("Starting..."); // ok
  powerOn();          // ok
  connectBT();        // ok
  setupActuators();   // ok
  setupData();        // ok
  msg("5 seconds delay...");
  delay (5000);
  msg("looping...");
  showLeds();         // ok  leds are set to show that we are ready for action!
 }

void loop(){
  for (int i = 0;i<nbButtons;i++){
    actuators[i]->update();
  }
  if (conf.autoRunning()){
    checkAuto();
  }
}


