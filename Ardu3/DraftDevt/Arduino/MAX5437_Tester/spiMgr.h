#ifndef SPIMGR_H
#define SPIMGR_H

#include <Arduino.h>
#include <SPI.h>

#define SPIMGR_BIT_ORDER_MSB (MSBFIRST)
#define SPIMGR_MODE0         (SPI_MODE0)
#define SPIMGR_5MH_CLK_RATE  (5000000)  //5 MHz
#define SPIMGR_10MH_CLK_RATE  (10000000)  //10 MHz

/* usage:
 *  instanciate obj 
 *  ad75019SPIMgr *spi = new SPIMgr(pin,select, pulse);
 *  send stuff
 *  spi>send(stuff)
 */

extern uint8_t char2bit(char c);

class SPIMgr{
  protected:
    // maintained by the instances 
    static boolean hasBegun;
    
    const int ssPin,
              select;
              
    const SPISettings settings;

    const boolean pulse;
                      
    
    void beginTransaction() const;
    void endTransaction() const;

  public:

    SPIMgr( int ss,  // slave select pin 
            int slect, // when is the chip selected for reading bits LOW or HIGH
            boolean pAfterInput,  // should the slect pin be pulsed after input? the AD75019 requies it
            int bOrder, 
            int sMode, 
            int cRate);
           
    // none of the send methods returns a reply
    void send(uint8_t b) const; // a single byte
    void send(const uint8_t vec[], int size) const; // a vector of bytes, the vector is not overwritten by the reply
    void send(const String s) const;  // a string of '0' and/or '1'
};

#endif
