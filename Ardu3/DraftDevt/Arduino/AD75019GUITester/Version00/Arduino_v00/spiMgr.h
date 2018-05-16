#ifndef SPIMGR_H
#define SPIMGR_H

#include <Arduino.h>
#include <SPI.h>

#define SPI_BIT_ORDER (MSBFIRST)
#define SPI_MODE      (SPI_MODE0)
#define SPI_CLK_RATE  (500000)   // 500KHZ //5 MHz


/* usage:
 *  instanciate obj 
 *  ad75019SPIMgr *spi = new ad75019SPIMgr();
 *  send stuff
 *  spi>send(stuff)
 */

extern uint8_t char2bit(char c);

class ad75019SPIMgr{
  protected:
    const int ssPin;
    
    void beginTransaction() const;
    void endTransaction() const;

  public:
    ad75019SPIMgr(int ssPin);
    // none of the send methods returns a reply
    void send(uint8_t b) const; // a single byte
    void send(const uint8_t vec[], int size) const; // a vector of bytes, the vector is not overwritten by the reply
    void send(const String s) const;  // a string of '0' and/or '1'
};

#endif
