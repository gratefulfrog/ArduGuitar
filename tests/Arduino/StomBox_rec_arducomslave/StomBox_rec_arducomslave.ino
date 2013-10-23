/* This is an example of how to use the ArduComSlave class.
 * First we have to define a function that will generate the response to incoming messages
 * 'prcoMsg' is just that: It prepends alternatively an 'e' or an 'x' to the incoming message
 * Then we declare a pointer to an ArduCom, the virtual class, since only later we decide
 * to instantiate a slave (in setup())
 * we instatiate the ArduComSlave, then call its doInit method. Upon exit from that, it is ready to go.
 * Note that we have used 'Serial' as the serial object port.
 * int the loop(), we only have to call stepLoop() and the rest is magic.
 * test this by inputing at the Serial Monitor:
 * first type an 'A' to confirm init,
 * then type sequences of 5 chars and observing the responses.
 */

#include <ArduCom.h>

void procMsg(char *buf, int bufSize){
  // just for creating errors,
  // this is an 'ArduComResponseFunc'
  static boolean lastResponseTrue = false;
  if (lastResponseTrue){
    buf[0] =  'e';
  }
  else{
    buf[0] =  'x';
  }
  lastResponseTrue = !lastResponseTrue;
}
  
ArduCom *com;

//////////////  std functions ////////////////

void setup(){
  com = new ArduComSlave(&Serial,&procMsg,ARDUCOM_MSGSIZE);
  com->doInit();
}

void loop(){
  com->stepLoop();
}
