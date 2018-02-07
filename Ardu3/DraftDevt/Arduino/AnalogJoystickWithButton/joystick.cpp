#include "joystick.h"

void JoyStick::calibrateXY(){
  long xSum = 0,
       ySum = 0;
  for(int i=0;i< 100; i++){
    xSum += analogRead(XPin);
    ySum += analogRead(YPin);
    delay(5);
  }
  X0 = round(xSum/100.0);
  Y0 = round(ySum/100.0);  
}

JoyStick::JoyStick(int xp,int yp, int pbp, void (*pbISR)()) : XPin(xp), 
                                                              YPin(yp), 
                                                              pbPin(pbp), 
                                                              interruptHandler(pbISR){
  pinMode(pbPin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pbPin), interruptHandler, LOW);
  calibrateXY();
}

int JoyStick::read(boolean isX) const{
  int pin = XPin,
      V0 = X0;
  if (!isX){
    pin = YPin;
    V0 = Y0;
  }
  int v = analogRead(pin);
  if (abs(v - V0) < pinExpo){
    return 0;
  }
  return v > V0 ? map(v,V0,maxAnalog,0,maxOutput) : map(v,minAnalog,V0,minOutput,0);
}

int JoyStick::readX() const{
  return read(true);
}

int JoyStick::readY() const{
  return read(false);
}


