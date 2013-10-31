/* a general purpose value holder class
 * such that Zero is the min
 * max is assgined const at instatiation
 * inc can take positive and negative values but always incs by the step of One
 */

#ifndef BIINC_H
#define BIINC_H

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
    byte inc(int i);
};

#endif


