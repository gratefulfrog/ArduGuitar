#ifndef ACTUATOR_CLASS_H
#define ACTUATOR_CLASS_H

#include <Arduino.h>

class deBounceButton {
  private:
    byte buttonPin,
         buttonState,     // = LOW,   // the current reading from the input pin
         lastButtonState; // = LOW;   // the previous reading from the input pin

    // the following variables are long's because the time, measured in miliseconds,
    // will quickly become a bigger number than can be stored in an int.
    long lastDebounceTime;  //  = 0;  // the last time the output pin was toggled
    static const byte debounceDelay = 30;    // the debounce time; increase if the output flickers
    
  public:
    deBounceButton(byte pin);
    boolean pressed();  
};

typedef void (*doerFunPtr)();

class actuatorClass {
  private:
    const doerFunPtr fPtr;
    deBounceButton   b;
    
  public:
    actuatorClass(byte pin, doerFunPtr f);
    void update();  
};

#endif
