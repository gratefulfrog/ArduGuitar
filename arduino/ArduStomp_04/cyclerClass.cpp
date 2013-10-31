#include "cyclerClass.h" 


cyclerClass::cyclerClass(byte nbStates): biInc(nbStates-1){}

byte cyclerClass::getState() const {
  biInc::getVal();
}
  
byte cyclerClass::incState(){
  return _val = _val == _maxVal ? 0 : _val+1;
}

