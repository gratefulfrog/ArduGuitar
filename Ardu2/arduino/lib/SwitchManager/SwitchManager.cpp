// -*- c++ -*-
/* SwitchManager.cpp
 */

#include <SwitchManager.h>

void SwitchManager::init(){
  pinMode(LATCH_PIN, OUTPUT);
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
}

void SwitchManager::setSwitchVal(byte switchId, byte val){
  // this will update the onVec and OffVec as per args
  /* it's not so straightforward.
   * this is what happens:
   * the switchId is used as an index in the Ardu2Conf::startIndex[]
   * from this we get the starting point SP.
   * doing integer division, SP/8 -> byteIndex for the vectors
   * and  SP % 8 -> offset within the byte, i.e. the amount that 
   * the val has to be left shifted before ORing it onto that byte.
   * thus onVec[byteIndex] |= (val << offset);
   * then we need the not of val for the offVec to XOR it in to the offVec
   * offVec[byteIndex]  ^= ((~val) << offset);  GOOD
   * then we have to see if the val is bigger than what was OR'd and XOR'd in.
   * so if (val >> offset >0  then there's more to do
   * so take the next byte -> byteIndex+1
   * and take the unprocessed part val >> (8-offset)
   * and OR it into the onVec
   * onVec[byteIndex+1] |= (val >> (8-offset))
   * and then XOR the not of it onto the offVec
   * offVec[byteIndex+1] ^= ((~val) >> (8-offset))
   */

  byte startingPoint =  Ardu2Conf::startIndex[switchId];
  byte byteIndex = startingPoint/8,
    offset = startingPoint % 8;
  Ardu2Conf::onVec[byteIndex] |= (val << offset);
  Ardu2Conf::offVec[byteIndex]  ^= ((~val) << offset);
  
  if (val >> offset >0){ 
    Ardu2Conf::onVec[byteIndex+1] |= (val >> (8-offset));
    Ardu2Conf::offVec[byteIndex+1] ^= ((~val) >> (8-offset));
  }
}

void SwitchManager::executeSwitching(){
  //Serial.print("Called SwitchManager::executeSwitching:\t" );

  // turn off the output so the leds don't light up
  // while you're shifting bits:
  digitalWrite(LATCH_PIN, LOW);
  delay(5);

  for (byte i=0;i<NB_SHIFT_REGS;i++){
    Ardu2Conf::curVec[i] |= Ardu2Conf::onVec[i];  
    SPI.transfer(Ardu2Conf::curVec[i]);
  }
  // 'make before' now ready
  // turn on the output so the switches can "Make":
  digitalWrite(LATCH_PIN, HIGH);
  delay(5);

  // now do the "Break"
  digitalWrite(LATCH_PIN, LOW);
  delay(5);
  for (byte i = 0;i<NB_SHIFT_REGS;i++){
    Ardu2Conf::curVec[i] &= Ardu2Conf::offVec[i];  
    SPI.transfer(Ardu2Conf::curVec[i]);
  }
  // 'break' now ready
  digitalWrite(LATCH_PIN, HIGH);
  delay(5);
}



