#include "biInc.h"

biInc::biInc(int mx): _maxVal(mx), _incVal(1) {
  _val = _minVal;  
}
    
int biInc::getVal() const {
  return _val;
}

void biInc::inc(int i){
  int increment = i > 0 ? _incVal : -_incVal;
  _val = min(max(_val + increment,_minVal),_maxVal);
}   

