#include "cyclerClass.h" 

biInc::biInc(byte mx): _maxVal(mx), _incVal(1) {
  _val = _minVal;  // to provoke update at presets  
}
    
byte biInc::getVal() const {
  return _val;
}

void biInc::setVal(byte v)  {
  if (v <= _maxVal && v >= _minVal){
    _val = v;
  }
}

byte biInc::inc(char i){
  int increment = i > 0 ? _incVal : -_incVal;
  return _val = min(max(_val + increment,_minVal),_maxVal);
}   

cyclerClass::cyclerClass(byte nbStates): biInc(nbStates-1){}

byte cyclerClass::inc(){
  return _val = _val == _maxVal ? 0 : _val+1;
}


/*
byte cyclerClass::getState() const {
  biInc::getVal();
}
  
byte cyclerClass::incState(){
  return _val = _val == _maxVal ? 0 : _val+1;
}
*/
