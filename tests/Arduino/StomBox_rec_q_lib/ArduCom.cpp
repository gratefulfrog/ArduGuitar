#include "ArduCom.h"

/*
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
*/
void ArduCom::respond(){
  //port->write((byte*)responseBuffer,responseSize);
  for (int i=0;i<responseSize;i++){
    port->write(msgBuffer[i]);
  } 
} 

void ArduCom::executeMsgString(){
  // after each atomic incoming msg, reply
  (*rFunc)(msgBuffer,msgSize);
  respond();
}
  

ArduCom::ArduCom(HardwareSerial *p,responseFunc f, int mSz): port(p), msgSize(mSz), responseSize(mSz+1){
  msgBuffer = new char[responseSize];
  initialized = false;
  currentCharCount = 1;
  rFunc = f;
}

void ArduCom::doInit() {
  // setup the port
  port->begin(baudRate);
  while(!*port);
  // send initChar and wait for response
  while(!initialized){
    port->write(initChar);
    delay(100);
    if(port->available()>0){
      char c = port->read();
      if (c !=initChar){
        msgBuffer[currentCharCount++] = c;
      }      
      initialized = true;
    }
  }
}

void ArduCom::stepLoop(){
  //processIncomingAtom();
  if (currentCharCount == responseSize) {
    executeMsgString();
    currentCharCount = 1;
  }

  //readIntoAtom();
  if (port->available() > 0) {
    // read one char and add it to the buffer if ok:
    char c = port->read();
    if (c !=initChar){
      msgBuffer[currentCharCount++] = c;
    }
  }
}

