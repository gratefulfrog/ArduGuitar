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

int JoyStick::readX() const{
  int x = analogRead(XPin);
  if (abs(x - X0) < pinExpo){
    return 0;
  }
  return x > X0 ? map(x,X0,maxAnalog,0,maxOutput) : map(x,minAnalog,X0,minOutput,0);
}

int JoyStick::readY() const{
  int y = analogRead(YPin);
  if (abs(y - Y0) < pinExpo){
    return 0;
  }
  return y > Y0 ? map(y,Y0,maxAnalog,0,maxOutput) : map(y,minAnalog,Y0, minOutput,0);
}


