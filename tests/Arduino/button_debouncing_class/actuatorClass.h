#ifndef ACTUATOR_CLASS_H
#define ACTUATOR_CLASS_H

#include "deBounceButton.h"

typedef String (*doerFunPtr)();

class actuatorClass {
  private:
    const doerFunPtr fPtr;
    deBounceButton   b;
    
  public:
    actuatorClass(int pin, doerFunPtr f);
    void update();  
};

#endif
