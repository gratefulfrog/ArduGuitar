#include "cyclerClass.h" 


cyclerClass::cyclerClass(int nbStates): biInc(nbStates-1){}

int cyclerClass::getState() const {
  biInc::getVal();
}
  
int cyclerClass::incState(){
  return _val = _val == _maxVal ? 0 : _val+1;
}

