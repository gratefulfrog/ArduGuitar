#ifndef AUTOCLASS_H 
#define AUTOCLASS_H 

#include <Arduino.h>
#include "cyclerClass.h"

// until we have an SD card to read from
static int nbAutoPresets = 2,
           autoPresetLis[][2] = {{0,1000},
                                 {1,2000}};

class autoClass {
  private:
    cyclerClass state,
                *currentIndex;
    int **presetDelayLis; //[][2];
    long lastAutoTime;
    
    void load();
    
  public:
    autoClass();
    boolean running() const;
    int inc();
    int check();
  
  
};

#endif









