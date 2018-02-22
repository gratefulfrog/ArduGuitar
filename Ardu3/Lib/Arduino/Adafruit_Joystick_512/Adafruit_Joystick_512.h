#ifndef JOYSTICK_512_H
#define JOYSTICK_512_H

/* Library to drive the Anafruit 2-axis analog joystick product ID 512
 * Wiring the joystick:
 * Vcc -> Ardunio 5V
 * Xout -> X-axis input pin, any analog pin
 * Yout -> Y-axis input pin, any analog pin
 * Sel  -> pushbutton interrupt pin, any interrupt enabled pin, on Uno: pins 2 or 3
 * GND  -> Arduino GND
 *
 * Usage:
 * 0. Check the #define's below to see if they suite your needs, change as desired.
 * 1. create your interrupt handler function, a.k.a Interrupt Service Routine ISR
 *  void pbISR(){  // this will be called every time the pb is pushed  
 * 2. decide on your pins: xPin, Ypin, pbPin, for example:
 *  const int xPin  = A0, 
 *            yPin  = A1,
 *            pbPin = 2;
 * 3. Declare a global pointer to a JoyStick object
 *  JoyStick *js
 * 4. in setup, instantiate a JoyStick:
 *    void setup(){
 *      js = new JoyStick(xPin,yPin,pbPin,pbISR);
 * 5. read the x and y values in the loop and do stuff with them.
 * void loop(){
 *  int currentX = js->readX(),
 *      currentY = js->readY();
 * 6. that's all there is to it!
 */

#include <Arduino.h>

// The following values may need to be adjusted depending on user needs
#define MAX_ANALOG  (1023)
#define MIN_ANALOG  (0)
#define MAX_OUTPUT  (100)
#define MIN_OUTPUT  (-100)
#define ZERO_DELTA  (10)       // minimum stick reading change before detecting movement 

class JoyStick{
  protected:
    const int XPin,
              YPin,     
              pbPin,   // pushbutton pin must be a pin capable of generating interrupts!!!
              maxAnalog = MAX_ANALOG,
              minAnalog = MIN_ANALOG,
              maxOutput = MAX_OUTPUT,
              minOutput = MIN_OUTPUT,
              pinExpo   = ZERO_DELTA;

    void (*interruptHandler)();  // a pointer to the function that will be called when the pushbutton goes LOW

    int X0   = 0,
        Y0   = 0;
    
    void calibrateXY();
    int read(boolean isX) const;
  public:
    JoyStick(int xp,int yp, int pbp, void (*pbISR)());  // last arg is a pointer to the interrupt handler
    int readX() const;
    int readY() const;
  
};

#endif
