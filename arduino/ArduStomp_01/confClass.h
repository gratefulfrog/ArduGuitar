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
#include "cyclerClass.h"

class confClass {
 private:
  const static String onOffString[2], //{"000","255"};// off, on, i.e. 0,1
                      pickupPinStrings[4],
                      volPinStrings[3],
                      tonePinString,  
                      volSettingsStrings[3][6], 
                      toneSettingsStrings[6];
  
  const static int presets[][5],
                    autoSetting[],
                    nbPresets;
  
  static biInc vtSettings[2]; 
  static cyclerClass pupSettings[3];
  
  String setVT(int id, int val);
  String setPup(int id, int val);
  
  String setPreset(int id);  
  
  String vtString (int i);
  String pupString(int i);
  
  cyclerClass currentPreset;
  
 public:
  confClass();
  String incVT(int id, int sens); // id =0 Vol, id = 1 tone
  String incPup(int id);  
  String incPreset();
};


#endif
