
#ifndef APP_H
#define APP_H

#include <Arduino.h>
#include "commsMgr.h"

class App{
  protected:

    uint16_t xValues = 0,
             yValues = 0;
    
    const static int bitVecNBBytes = 32; //BITVEC_NB_BYTES;
    uint8_t  bitVec[bitVecNBBytes];
         
    CommsMgr *comms;
    void  initBitVec();
    void setXValues();
    void updateDevice();
    void readYValues();
    void execIncoming();
    
  public:
    App(long baudRate);
    void loop();
};
#endif
