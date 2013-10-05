/* 
 Debounce and Actuators
 */

#include "deBounceButton.h"
#include "actuatorClass.h"

// constants won't change. They're used here to 
// set pin numbers:
const int onButtonPin = 2,
          offButtonPin = 3;    // the number of the pushbutton pin
const int ledPin = 13;      // the number of the LED pin

// Variables will change:
int ledState = LOW;         // the current state of the output pin
/*
deBounceButton on(onButtonPin),
               off(offButtonPin);
*/

String offAction(){
  if(ledState != LOW){
    ledState= LOW;
    digitalWrite(ledPin, ledState);
  }
  return "Off Pressed!\n";
}
String onAction(){
  if(ledState != HIGH){
    ledState= HIGH;
    digitalWrite(ledPin, ledState);
  }
  return "On Pressed!\n";
}

actuatorClass turnOn(onButtonPin,onAction),     
              turnOff(offButtonPin,offAction);

void setup() {  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, ledState);
}

void loop() {
  turnOn.update();
  turnOff.update();
}

