#ifndef DEBOUNCEBUTTON_H
#define DEBOUNCEBUTTON_H

#include <Arduino.h>

class deBounceButton {
  private:
    int buttonPin,
        buttonState,     // = LOW,   // the current reading from the input pin
        lastButtonState; // = LOW;   // the previous reading from the input pin

    // the following variables are long's because the time, measured in miliseconds,
    // will quickly become a bigger number than can be stored in an int.
    long lastDebounceTime;            //  = 0;  // the last time the output pin was toggled
    static const long debounceDelay = 50;    // the debounce time; increase if the output flickers
    
  public:
    deBounceButton(int pin);
    boolean pressed();  
};

#endif
