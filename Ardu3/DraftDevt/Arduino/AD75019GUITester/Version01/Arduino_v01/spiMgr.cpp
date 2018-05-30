#include "spiMgr.h"

uint8_t char2bit(char c){
  //int res = c == '1' ? 1 : 0;
  //Serial.println(String("(") + c + "," + res + ")");
  return c == '1' ? 1 : 0; //res ;
}


void ad75019SPIMgr::beginTransaction() const {
  SPI.beginTransaction (SPISettings (SPI_CLK_RATE, SPI_BIT_ORDER, SPI_MODE)); 
  digitalWrite (ssPin, HIGH);
}

void ad75019SPIMgr::endTransaction() const {
  digitalWrite (ssPin, LOW);
  digitalWrite (ssPin, HIGH);       
  SPI.endTransaction ();
}
  
ad75019SPIMgr::ad75019SPIMgr(int ssP): ssPin(ssP){
  pinMode(ssPin,OUTPUT);
  digitalWrite(ssPin,HIGH);
  SPI.begin();
}
// none of the send methods returns a reply
void ad75019SPIMgr::send(uint8_t b) const{ // a single byte
  beginTransaction();
  SPI.transfer(b);
  endTransaction();
}
void ad75019SPIMgr::send(const uint8_t vec[], int size) const{ // a vector of bytes, the vector is not overwritten by the reply
  uint8_t newVec[size];
  for (int i=0;i<size;i++){
    newVec[i] = vec[i];
  }
  beginTransaction();
  SPI.transfer(newVec,size);
  endTransaction();
}

void ad75019SPIMgr::send(const String s) const{  // a string of '0' and/or '1'
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


