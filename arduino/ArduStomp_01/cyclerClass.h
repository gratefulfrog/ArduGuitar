/* a general purpose value cylcer class
 * such that Zero is the min
 * nb of states is assgined const at instatiation
 * inc cycles from Zero to nbStates-1 and then from Zero again...
 */

#ifndef CYCLERCLASS_H
#define CYCLERCLASS_H

#include "biInc.h"
#include "misc.h"

class cyclerClass: private biInc {
  public:
    cyclerClass(int nbStates);
    int getState() const;
    void incState();
};
#endif


