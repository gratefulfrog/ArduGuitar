#ifndef SPIMGR_H 
#define SPIMGR_H

#include <Arduino.h>
#include <SPI.h>

/*
 * Pins:
 * MOSI: 11 or ICSP-4 
 * MISO: 12 or ICSP-1  
 * CLK:  13 or ICSP-3  
 * SS:   10
 */



class SPIMgr{
  protected:
    static const int nbBytes = 32;
    static boolean spiInit;
    
    const int pclk = 10;
    
    byte bitVec[nbBytes];

  public:
    SPIMgr();
    void update();
    void connect(int x, int y,boolean set);
    void clear();
    void setAll(byte v = 255);
};

#endif
