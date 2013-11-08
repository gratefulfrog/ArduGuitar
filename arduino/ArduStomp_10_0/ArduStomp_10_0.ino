//  -*-C++-*-
/* ArduStomp_10_0
 * rething after SRAM and PROGMEM issues:
 ** make it simpler
 ** make it more efficient in mem usage
 ** try to do everything static or at least without dynamic DE-allocations,
 ** use binary display for Bol and tone values! only 3 LEDS each!
 ** no: save this for the future ..allow for 2 LEDS on EACH Pup,
 * code to command the ARduGuitar from an arduino based stomp box.
 * integrating coms and BT
 */

#include <Arduino.h>
#include <SPI.h>
#include <ArduConf00.h>
#include <State.h>
#include <DebounceButton.h>
#include <outQueueStatic.h>
#include <ArduComOptStatic.h>
#include <RN42autoConnectOpt.h>
#include <SD.h>
#include <SDReader.h>
#include <LEDManager.h>
#include <Actuator.h>
#include <ArduStomp.h>

int freeRam (){
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

///////////////////////////////////////////////////////
void setup(){
  Serial.begin(115200);
  while(!Serial);
  delay(5000);
  Serial.println("Starting...");
  Serial.print("Free Ram: ");
  Serial.println(freeRam());

  ArduStomp::init();
  Serial.println("return from ArduStomp::init()...");
  Serial.print("Free Ram: ");
  Serial.println(freeRam());
  
  Actuator::init(ArduStomp::as);
  Serial.println("return from Actuator::init(ArduStomp::as)...");
  Serial.print("Free Ram: ");
  Serial.println(freeRam());
  LEDManager::set(ArduConf00::powerID,1);     // set the power led
  LEDManager::set(ArduConf00::connectID,1);     // set the connect led

}
/*
void loop(){
  ArduStomp::as->stepAlarm();
  //delay(5000);
  Serial.print("Free Ram: ");
  Serial.println(freeRam());
}
/*
void loop(){
  ArduStomp::as->stepAlarm();
}
*/
void loop(){}
/*
void loop(){
  if(Actuator::allOK){
    for (byte b = 0;b<NB_ACTUATORS;b++){
      if (Actuator::actuators[b] && 
          Actuator::actuators[b]->update()){
	break;
      }
    }
  }
}
*/
/*
void loop(){
  if(Actuator::allOK){
    for (byte b = 0;b<NB_ACTUATORS;b++){
      if (Actuator::actuators[b] && 
          Actuator::actuators[b]->update()){
	break;
      }
    }
  }
  if(Actuator::allOK){
    ArduStomp::as->checkAuto();
    ArduStomp::as->com->stepLoop();
  }
  else{ // it's broken, tell the world!
    ArduStomp::as->stepAlarm();
  }
}

*/
