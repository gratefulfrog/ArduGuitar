#ifndef COMMSMGR_H
#define COMMSMGR_H

#include <Arduino.h>

// config params
#define CONTACT_CHAR   '|'
#define POLL_CHAR      'p'
#define EXECUTE_CHAR   'x'

#define NB_BITS_IN_BYTE  (8)
#define AD75019_NB_BITS  (256)
#define BITVEC_NB_BYTES  (AD75019_NB_BITS/NB_BITS_IN_BYTE)
#define XYVALUES_NBBITS  (16)
#define INCOMING_LENGTH  (XYVALUES_NBBITS + AD75019_NB_BITS)

#define EST_CONTACT_LOOP_PAUSE  (200)  // milliseconds

extern int char2bit(char c);
extern String val2String(uint32_t val,int len);

class CommsMgr{
  protected:
    const int execIncomingLength = INCOMING_LENGTH;
    
    const char contactChar = CONTACT_CHAR,
               pollChar    = POLL_CHAR,
               executeChar = EXECUTE_CHAR; 
    enum state  {contact, poll, execute};
    state currentState = contact;

    String incomingBitsAsString = "";
         
    void initSerial(long baudRate);
    void establishContact();
    
  public:
    CommsMgr(long baudRate);
    boolean processIncoming();  // return true if there is something to execute
    //boolean ready2Exec() const;
    void getIncomingXValues(uint16_t &Xvals) const;
    void CommsMgr::getIncomingBitVec(uint8_t  (&bitVec)[BITVEC_NB_BYTES]) const;
    void sendReply(const uint16_t &xValues,
                   const uint16_t &yValues,
                   const uint8_t  (&bitVec)[BITVEC_NB_BYTES]);
};
#endif

