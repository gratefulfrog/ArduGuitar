#include "spiMgr.h"

#define DEBUG

boolean SPIMgr::spiInit = false;

SPIMgr::SPIMgr(){
  if (!spiInit){
    SPI.begin(); 
    spiInit=true;
  }
  clear();
}

void SPIMgr::update() {
  #ifdef DEBUG
  for (int i = 0; i< nbBytes;i++){
    Serial.print(bitVec[i]);
    Serial.print(" ");
  }
  Serial.println();
  #endif
  byte tempVec[32];
  for (int i=0;i<nbBytes;i++){
    tempVec[i]=bitVec[i];
  }
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
  for (int i=0;i<nbBytes;i++){
    SPI.transfer(tempVec[i]);
  }
  //SPI.transfer(tempVec,nbBytes);
  digitalWrite(pclk,LOW);
  delayMicroseconds(1);
  digitalWrite(pclk,HIGH);
  SPI.endTransaction();
}

void SPIMgr::connect(int x, int y,boolean set){
  // first get the positon of the 2 x bytes
  int x15pos = (15-y)*2;
  // then set the correct bit for the x bit
  unsigned int v  = 1 << x;
  // pair contains a bit corresponding to the x pin
  byte pair[2] = {((v>>8) & 255), (v & 255)};
    
  for (int i=0;i<2;i++){
    if (set){
      //to set we just or the x bit 
      bitVec[x15pos+i] |= pair[i];
    }
    else{
      // to unset we and all the bits except the x bit
      bitVec[x15pos+i] &= (255 ^ pair[i]);
    }
  }
}

void SPIMgr::clear(){
  setAll(0);
}

void SPIMgr::setAll(byte v){
  for (int i=0;i<nbBytes;i++){
    bitVec[i]=v;
  }
}

