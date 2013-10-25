#include "biInc.h"

biInc::biInc(int mx): _maxVal(mx), _incVal(1) {
  _val = _minVal-1;  // to provoke update at presets  
}
    
int biInc::getVal() const {
  return _val;
}

void biInc::setVal(int v)  {
  if (v <= _maxVal && v >= _minVal){
    _val = v;
  }
}

int biInc::inc(int i){
  int increment = i > 0 ? _incVal : -_incVal;
  return _val = min(max(_val + increment,_minVal),_maxVal);
}   

