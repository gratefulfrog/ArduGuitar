#include "app.h"

void  App::initBitVec(){
  for (int i=0; i<bitVecNBBytes; i++){
    bitVec[i]=0;
  }
}


void App::setXValues(){
  // placeholder!
  // real code would set all the X output pins
  return;
}
void App::updateDevice(){
  // XXXX only for testing GUI XXX
  for (int i=0; i<bitVecNBBytes; i+=2){
    uint8_t l = (uint8_t)(((xValues & (255<<NB_BITS_IN_BYTE))>>NB_BITS_IN_BYTE) & 255),
            r = (uint8_t)(xValues & (255));
    bitVec[i]   = l;
    bitVec[i+1] = r;
  }
}
void App::readYValues(){
  // XXXX only for testing GUI XXX
  // real code would read all the Y input pins
  yValues = xValues;
}

void App::execIncoming(){
  comms->getIncomingXValues(xValues);
  setXValues();
  //comms->getIncomingBitVec(bitVec);
  updateDevice();
  readYValues();
}

App::App(long baudRate){
  initBitVec();
  comms =  new CommsMgr(baudRate);
}

void App::loop(){
  if(comms->processIncoming()){
    execIncoming();
  }
  comms->sendReply(xValues,yValues,bitVec);
}
  
