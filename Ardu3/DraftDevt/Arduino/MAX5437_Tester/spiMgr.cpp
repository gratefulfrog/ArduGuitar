#include "spiMgr.h"

uint8_t char2bit(char c){
  //int res = c == '1' ? 1 : 0;
  //Serial.println(String("(") + c + "," + res + ")");
  return c == '1' ? 1 : 0; //res ;
}

// static class variable
boolean SPIMgr::hasBegun = false;

void SPIMgr::beginTransaction() const {
  SPI.beginTransaction (settings); 
  digitalWrite (ssPin, select);
}

void SPIMgr::endTransaction() const {
  digitalWrite (10, !digitalRead(ssPin));
  if (pulse){
    digitalWrite (10, !digitalRead(ssPin));
  }
  SPI.endTransaction ();
}

SPIMgr::SPIMgr(int ss,  // slave select pin 
               int slect, // when is the chip selected for reading bits LOW or HIGH
               boolean pAfterInput,  // should the slect pin be pulsed after input? the AD75019 requies it
               int bOrder, 
               int sMode, 
               int cRate) :
               ssPin(ss),
               select(slect),
               pulse(pAfterInput),
               settings(SPISettings(cRate,bOrder,sMode)){
            
  if (!hasBegun){
    SPI.begin();
    hasBegun = true;
  }
  digitalWrite(ssPin, (pulse ? select : !select));
}
// none of the send methods returns a reply
void SPIMgr::send(uint8_t b) const{ // a single byte
  beginTransaction();
  SPI.transfer(b);
  endTransaction();
}
void SPIMgr::send(const uint8_t vec[], int size) const{ // a vector of bytes, the vector is not overwritten by the reply
  uint8_t newVec[size];
  for (int i=0;i<size;i++){
    newVec[i] = vec[i];
  }
  beginTransaction();
  SPI.transfer(newVec,size);
  endTransaction();
}

void SPIMgr::send(const String s) const{  // a string of '0' and/or '1'
  const int len    = s.length(),
            vecLen = len/8;
  uint8_t bitVec[vecLen];

  int strIndex =0;
  for (int i = 0; vecLen; i++){
    bitVec[i] = 0;
    for (int bitPos = 0; bitPos < 8; bitPos++){ 
      bitVec[i] |= char2bit(s[strIndex++]) <<(8-1-bitPos);
    }
  }
  send(bitVec,vecLen);
}

