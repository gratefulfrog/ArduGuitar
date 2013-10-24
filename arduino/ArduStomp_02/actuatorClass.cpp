#include "actuatorClass.h"

actuatorClass::actuatorClass(int pin, doerFunPtr f): fPtr(f), b(pin){
  ;
}
void actuatorClass::update() {
  if(b.pressed()){
    (*fPtr)() ;
  }
}
