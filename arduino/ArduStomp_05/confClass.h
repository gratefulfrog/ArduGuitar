/* confClass.h
 * a general purpose value holder class
 * such that Zero is the min
 * max is assgined const at instatiation
 * inc can take positive and negative values but always incs by the step of One
 */
 
/* from data.tsv
 * name	  vol	tone	neck	middle	bNorth	bBoth
 * Rock	  6	11	0	1	0	1
 * Woman  10	4	1	0	0	1
 * Jazz	  11	1	1	0	0	0
 * Comp	  8	11	0	1	0	1
 * Auto	  0	0	0	0	0	0
 *
 * from conf.pde
 * volPins[] = {"09","10","12"},
 * tonePin   = "11",
 * selectorPins[]   = {"02", //neck
                       "03", // middlePin
		       "05",  // splitPin
	               "04"}, //bridgePin
 * onOff[] = {"000", "255"}, // 0, 1
 * // vol levels: [0,1,2,3,4,5]
   volPWM[][]  = {{"000","012","014","018","027","255"},
                   // volPWM[0]-> volPins[0]
		  {"255","030","020","015","013","000"},
	           // volPWM[1]-> volPins[1]
		  {"000","000","000","000","000","255"}},  
	           // 3rd vactrol for max volume: volPWM[2]-> volPins[2]
 * tonePWM[] = {"255","090","046","027","017","000"};
                // tone levels: [0,1,2,3,4,5]
 */
 

#ifndef CONF_H
#define CONF_H

#include <Arduino.h>
#include <SDReader.h>
#include "cyclerClass.h"

class confClass {
 private:
   const byte offOn[] = {0,255},
              pickupPins[] = {2,3,4,5},
              volPins[]    = {9,10,12},
              tonePin      = 11,
              volSettings[][6] = {{0,  12,14,18,27,255},  // volPWM[0]-> volPins[0]
    		                  {255,30,20,15,13,  0},  // volPWM[1]-> volPins[1]
                                  {0,   0, 0, 0, 0,255}}, // 3rd vactrol for max volume: volPWM[2]-> volPins[2]
              toneSettings[4]  =  {255,90,46,27,17,  0};
              
  void pickupMsg(char *b, byte pickupID){
     b2a(b,pickupPins[pickupId]); // the pin
     b2a(b+2,offOn[pickupSettings(pickupId)]);  // the value
  }
  void toneMsg(char *b){
     b2a(b,tonePin); // the pin
     b2a(b+2,toneSettings[toneVal()]); // the value
  }
  void volMsg(char *b){
    for (byte i =0;i<3,i++){
      b2a(b[i*5],volPins[i]);  // the pin
      b2a(b[i*5)+2],volSettings[i][volVal()]);
    }
  }  
  void b2a(char *buf, byte b){
    if(b<100){
      buf[0] = b/10;
      buf[1] = b%10;
    }
    else{
      buf[0] = b/100;
      buf[1] = (b%100)/10;
      buf[2] = b%10;
    }
  }
  /*
  vol:3
  tone:3
  neck:1
  middle:1
  bridgeN:1
  BridgeB:1
  */
  unsigned int currentSettings = 0;  
                
  const static char onOffString[][4], //{"000","255"};// off, on, i.e. 0,1
                      pickupPinStrings[][3],
                      volPinStrings[][3],
                      tonePinString[],  
                      volSettingsStrings[][6][4], 
                      toneSettingsStrings[][4];
  
  String setVT(byte id, byte val,boolean force);
  String setPup(byte id, byte val,boolean force);
  
  String setPreset(byte id,boolean force);  
  
  String vtString (byte i);
  String pupString(byte i);
  PresetClass *pre;
  AutoClass *aut;

 public:
  static biInc vtSettings[2]; 
  static cyclerClass pupSettings[3];
  //cyclerClass currentPreset;

  confClass(PresetClass *p, AutoClass *a);
  String getPresetString(byte presetIndex);
  String incVT(byte id, int sens); // id =0 Vol, id = 1 tone
  String incPup(byte id);  
  String incPreset(boolean force);
};

#endif
