/* a general purpose value holder class
 * such that Zero is the min
 * max is assgined const at instatiation
 * inc can take positive and negative values but always incs by the step of One
 */

#ifndef BIINC_H
#define BIINC_H

#include "misc.h"

class biInc {
  protected:  
    static const int _minVal = 0;
    const int _maxVal,
              _incVal;
    int _val;
  
  public:
    biInc(int mx); // min is zero and start is zero
    int getVal() const;
    void inc(int i);
};


#endif


