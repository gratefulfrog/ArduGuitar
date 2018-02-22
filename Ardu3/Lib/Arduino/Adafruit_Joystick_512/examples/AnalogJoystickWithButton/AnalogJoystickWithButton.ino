#include "Adafruit_Joystick_512.h"

/* Simple example of reading Joystick x,y values and handling the pushbutton.
 * The x,y values are read and displayed.
 * the pushbutton toggles on/off the Arduino on-board LED.
 * 
 * Wiring and Configuration:
 * wire the device to +5V, GND, and then select analog pins for X,Y, and an interrupt enebled pin for SEL
 * change the #defines to the values you use.
 *
 * Usage:
 *  start Serial Monitor with correct Baud Rate
 */

#define XOUT     (A0)
#define YOUT     (A1)
#define SEL      (2)
#define LED_PIN  (13)
#define BAUD     (115200)

JoyStick *js;

const int XPin   = XOUT,
          YPin   = YOUT,
          pbPin  = SEL,
          ledPin = LED_PIN,
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
  Serial.begin(BAUD);
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

