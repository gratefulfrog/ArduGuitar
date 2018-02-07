#include "joystick.h"

JoyStick *js;

const int XPin   = A0,
          YPin   = A1,
          pbPin  = 2,
          ledPin = 13,
          changeDelta = 50,   // millisecs          
          displayDelta = 200; // millisecs
          
volatile boolean flag = false;

void pbISR(){
  flag = true;
}

void allocateJS(){
  js = new JoyStick(XPin, YPin,pbPin, pbISR);
  if (!js){
    Serial.println("Joystick allocation failed...");
    while(1);
  }  
}

void setup(){
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  allocateJS();
  Serial.println("\nStarting up...");
}

void testFlag(){
  static unsigned long lastChangeTime = 0;
  noInterrupts();
  if (flag){
    if( millis()-lastChangeTime > changeDelta){
      digitalWrite(ledPin,!digitalRead(ledPin));
      lastChangeTime = millis();
      Serial.println("\nPush Button!\n");
    }
    flag = false;
  }  
  interrupts();       
}

void loop() {
  static unsigned long lastDisplayTime = 0;
  testFlag();
  if (millis()-lastDisplayTime < displayDelta){
    return;
  }
  lastDisplayTime = millis();
  String line = String("X: ") 
              + String(js->readX())
              + String("  Y: ") 
              + String(js->readY());
  Serial.println(line);
}

