#ifndef JOYSTICK_H
#define JOYSTICK_H

#include <Arduino.h>

class JoyStick{
  protected:
    const int XPin,
              YPin,
              pbPin,   // must be a pin capable of generating interrupts!!!
              maxAnalog = 1023,
              minAnalog = 0,
              maxOutput = 100,
              minOutput = -100,
              pinExpo = 5;

    void (*interruptHandler)();  // a pointer to the function that will be called when the pushbutton goes LOW

    int X0   = 0,
        Y0   = 0;
    
    void calibrateXY();
  public:
    JoyStick(int xp,int yp, int pbp, void (*pbISR)());  // last arg is a pointer to the interrupt handler
    int readX() const;
    int readY() const;
  
};

#endif
