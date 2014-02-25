// -*- c++ -*-
/* SwitchManager.cpp
 */

#include <SwitchManager.h>

void SwitchManager::init(){
  pinMode(LATCH_PIN, OUTPUT);
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
}

byte SwitchManager::mask(byte size){
  // return a byte with size number of 1s on the right 
  byte res=0;
  for (byte i=0;i<size;i++){
    res |= (1<<i);
  }
  return res;
}

void SwitchManager::setSwitch(byte switchId, boolean val){
  /* if val is true, turn on, else off
   * this is called on individual SPST switch IDs
   * switchId is on [0,81]
   */
  byte componentIndex = switchId/8,
    offset = switchId % 8;
  if (val){ // turn on a single switch
    Ardu2Conf::onVec[componentIndex] |= (1 << offset);
    //Serial.print("turning on: ");
    //Serial.println(switchId);
  }
  else{ // turn off a single switch
    byte msk = (254 << offset) | SwitchManager::mask(offset);
    Ardu2Conf::offVec[componentIndex] &= msk;
    //Serial.print("turning off: ");
    //Serial.println(switchId);
  }
}


void SwitchManager::setComponent(byte componentId, byte val){
  // this will update the onVec and OffVec as per args
  // componentId is a value on[0,18]
  /* it's not so straightforward.
   * this is what happens:
   * the componentId is used as an index in the Ardu2Conf::startIndex[]
   * from this we get the starting point SP.
   * doing integer division, SP/8 -> componentIndex for the vectors
   * and  SP % 8 -> offset within the byte, i.e. the amount that 
   * the val has to be left shifted before ORing it onto that byte.
   * thus onVec[componentIndex] |= (val << offset);
   * then we need the not of val for the offVec to XOR it in to the offVec
   * offVec[componentIndex]  ^= ((~val) << offset);  GOOD
   * then we have to see if the val is bigger than what was OR'd and XOR'd in.
   * so if (val >> offset >0  then there's more to do
   * so take the next byte -> componentIndex+1
   * and take the unprocessed part val >> (8-offset)
   * and OR it into the onVec
   * onVec[componentIndex+1] |= (val >> (8-offset))
   * and then XOR the not of it onto the offVec
   * offVec[componentIndex+1] ^= ((~val) >> (8-offset))
   */

  byte startingPoint =  Ardu2Conf::startIndex[componentId];
  byte componentIndex = startingPoint/8,
    offset = startingPoint % 8;
  Ardu2Conf::onVec[componentIndex] |= (val << offset);

  byte size = Ardu2Conf::startIndex[componentId+1] - startingPoint;
  byte msk = SwitchManager::mask(size);
  byte xOrTemp = msk ^ val;
  Ardu2Conf::offVec[componentIndex]  ^= (xOrTemp << offset);

  if ((val >> (8-offset)) >0){ 
    Ardu2Conf::onVec[componentIndex+1] |= (val >> (8-offset));
    Ardu2Conf::offVec[componentIndex]  ^= (xOrTemp >> (8-offset));
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
  Ardu2Conf::resetVecs();
}



