/* ArduCom.h
 * ArduCom class,
 * responseLength = messageLength + 1
 * only one buffer used for both incoming and outgoing
 */


#ifndef ARDUCOM_H
#define ARDUCOM_H

#define INITCHAR 'A'
#define BAUDRATE 115200

#define ARDUCOM_MSGSIZE 5

#include <Arduino.h>

typedef void (*responseFunc)(char*,int);

class ArduCom {
  private:
    const static char initChar = INITCHAR;
    const static long baudRate = BAUDRATE;

    const int msgSize,
              responseSize;
  
    HardwareSerial *port;
    
    responseFunc rFunc;
    
    boolean initialized;
    int currentCharCount;   // how many chars we've read
    char *msgBuffer;
         //*responseBuffer;

    void respond();    
    void executeMsgString();
    void processMsgAtom();
    void readIntoMsgAtom();
  public:
    ArduCom(HardwareSerial *p,responseFunc f, int mSz);
    void doInit();
    void stepLoop();
};

#endif


