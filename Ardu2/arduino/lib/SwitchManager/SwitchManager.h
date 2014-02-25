// -*- c++ -*-
/* SwitchManager.h
 *to manage analog switch inputs/outputs
 * What is a switch?
 * - an id that links to an address on the SPI chaine
 * - a description of what it does?
 * How will commands be communicated?
 * - protocol: xxV: xx an int represent the ID, and V either 0 or 1 ?
 * - protocol: *1xxyyzz...0mmnnpp...# where all ids following 1 are turned on, 
 *             and those following 0 are turned off? with * and # as message 
 *             delimiters? This is nicer since it lets the UI define the block
 *             size at each call!
 * How will the values be passed to the on/off controller?
 * - for ex, controller.do(); //onVect[],offVect[] ?globals?
 *    where the vectors are:
 *    - onVec: values are 1 if turned on and 0 if unchanged, such that
 *      curVec OR onVec -> updated On state for 'make before' part of operation,
 *    - offVec: values are 1 if unchanged, 0 if turned off, such that
 *      curVec AND offVec -> updated final state for 'break' part of operation.
 *   where controller::do looks somethinglike
 *   static unsigned byte curVec[NbBytes]; // has current values for all the 
 *                                         // switch controls
 *   for (byte i = 0;i<NbBytes;i++){
 *     curVec[i] |= onVec[i];  
 *   }
 *   // 'make before' now ready
 *   spiManger.update(curVec); // spi manager returns only after the 2ms 
 *                             // delay after update
 *   for (byte i = 0;i<NbBytes;i++){
 *     curVec[i] &= offVec[i];  
 *   }
 *   // 'break' now ready
 *   spiManger.update(curVec); 
 *  
 *  That looks pretty good!
 *  ---
 * So what is needed?
 * a conf class that has all the parameters as public static so no need to pass
 * them on the stack, 
 * public: static const byte nbSwitchRegs =  11;
 * public: static byte curVec[nbSwitchRegs], 
 *                     onVec[nbSwitchRegs], 
 *                     offVec[nbSwitchRegs];
 */


#ifndef SWITCHMANAGER_H
#define SWITCHMANAGER_H

#include <Arduino.h>
#include <SPI.h>
#include <Ardu2Conf.h>

class SwitchManager {
private:
  static byte mask(byte size);

public:
  static void init();
  static void setSwitch(byte switchId, boolean val);
  static void setComponent(byte componentId, byte val);
  static void executeSwitching();
};

#endif
