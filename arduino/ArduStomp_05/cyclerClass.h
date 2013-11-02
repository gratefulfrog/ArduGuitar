// biInc and cyclerClass

/* biInc: a general purpose value holder class
 * such that Zero is the min
 * max is assgined const at instatiation
 * inc can take positive and negative values but always incs by the step of One
 */
/* cyclerClass a general purpose value cylcer class
 * such that Zero is the min
 * nb of states is assgined const at instatiation
 * inc cycles from Zero to nbStates-1 and then from Zero again...
 */

#ifndef CYCLERCLASS_H
#define CYCLERCLASS_H

#include <Arduino.h>

class biInc {
  protected:  
    static const byte _minVal = 0;
    const byte _maxVal,
               _incVal;
    byte _val;
    
  public:
    biInc(byte mx); // min is zero and start is zero
    byte getVal() const;
    void setVal(byte v);
    byte inc(char i);
};

class cyclerClass: public biInc {
  public:
    cyclerClass(byte nbStates);
    //byte getState() const;
    //byte incState();
    byte inc();
};
#endif


