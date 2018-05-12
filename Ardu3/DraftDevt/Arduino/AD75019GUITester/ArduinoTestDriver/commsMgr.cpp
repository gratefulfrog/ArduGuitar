#include "commsMgr.h"

//#define DEBUG

int char2bit(char c){
  return c == '1' ? 1 : 0;
}

String val2String(uint32_t val,int len){
  //Serial.println(String("val2String called with : ") + val + " , " + len);
  String res = "";
  for (int i=0; i< len;i++){
    int v = (val & (1<<(len-1-i)));
    res+=v ? '1':'0';
  }
  return res;
}

void CommsMgr::initSerial(long baudRate){
  Serial.begin(baudRate);
  while (!Serial);
}

void CommsMgr::establishContact() {
  const int loopPauseTime EST_CONTACT_LOOP_PAUSE;
  while (Serial.available() <= 0) {
    Serial.print(contactChar);   // send a char and wait for a response...
    delay(loopPauseTime);
  }
  Serial.read();
  currentState = contact;
}

 CommsMgr::CommsMgr(long baudRate){
  initSerial(baudRate);
  establishContact();
 }

boolean CommsMgr::processIncoming(){
  static int tempCount =0;
  boolean execFlag = false;
  if (Serial.available()>0){
    char incomingChar = Serial.read();  
    switch(currentState){
      case (contact):
      case (poll):
        // we got a poll, it's ok to send the current X,Y,and bitVec values
        if (incomingChar == pollChar){
          currentState = poll;
        }
        // we got a settings command, 16 Xbits + 256 conection bits
        // init to read the string values of the bits
        else if (incomingChar == executeChar){
          currentState = execute;
          incomingBitsAsString = "";
          #ifdef DEBUG
            Serial.println("got an x"); 
          tempCount =0;
          #endif
        }
        break;
      case (execute):
        // we are reading in bits, keep on reading until done, then when we got
        // all the bits we need, execute the result
        incomingBitsAsString += incomingChar;
        #ifdef DEBUG
          Serial.println(String("read a char for x :") + tempCount++);
        #endif
        if (incomingBitsAsString.length() == execIncomingLength){
          execFlag = true;
          currentState = poll;
          #ifdef DEBUG
            Serial.println("finished an x read");
          #endif
        }
    }
  }
  return execFlag;
}
/*
boolean CommsMgr::ready2Exec() const{
  Serial.println(String ("ready2Exec returning : ") + execFlag);
  return execFlag;
}
*/
void CommsMgr::getIncomingXValues(uint16_t &xVals)  const{
  xVals = 0;
  for (int i=0; i<16; i++){
    xVals |= char2bit(incomingBitsAsString[i]) << (16-1 -i);
  }
}


// the following is completely untested!!!
void CommsMgr::getIncomingBitVec(uint8_t  (&bitVec)[BITVEC_NB_BYTES]) const{
  int bitVecIndex = 0,
      strIndex    = XYVALUES_NBBITS;  // first setting value on incoming
 
  while (strIndex < INCOMING_LENGTH){
    bitVec[bitVecIndex] = 0;
    for (int i=0;i< NB_BITS_IN_BYTE;i++){
      // do 8 chars
      bitVec[bitVecIndex] |= char2bit(incomingBitsAsString[strIndex++]) << (NB_BITS_IN_BYTE-i-1);
    }
    bitVecIndex++;
  }
}

#ifdef DEBUG
void CommsMgr::sendReply(const uint16_t &xValues,
                         const uint16_t &yValues,
                         const uint8_t  (&bitVec)[BITVEC_NB_BYTES]){
  if (currentState == poll){
    Serial.println(String("x : ") + val2String(xValues,XYVALUES_NBBITS));
    Serial.println(String("y : ") + val2String(yValues,XYVALUES_NBBITS));
    for (int i=0; i<BITVEC_NB_BYTES; i++){
      Serial.println(String(i) + " : " + val2String(bitVec[i],NB_BITS_IN_BYTE));
    }
    currentState = contact;
  }
}

#else
void CommsMgr::sendReply(const uint16_t &xValues,
                         const uint16_t &yValues,
                         const uint8_t  (&bitVec)[BITVEC_NB_BYTES]){
  if (currentState == poll){
    Serial.print(val2String(xValues,XYVALUES_NBBITS));
    Serial.print(val2String(yValues,XYVALUES_NBBITS));
    for (int i=0; i<BITVEC_NB_BYTES; i++){
      Serial.print(val2String(bitVec[i],NB_BITS_IN_BYTE));
    }
    currentState = contact;
  }
}
#endif

