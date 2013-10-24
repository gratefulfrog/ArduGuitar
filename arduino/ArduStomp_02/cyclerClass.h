/* a general purpose value cylcer class
 * such that Zero is the min
 * nb of states is assgined const at instatiation
 * inc cycles from Zero to nbStates-1 and then from Zero again...
 */

#ifndef CYCLERCLASS_H
#define CYCLERCLASS_H

#include "biInc.h"

class cyclerClass: public biInc {
  public:
    cyclerClass(int nbStates);
    int getState() const;
    int incState();
};
#endif


