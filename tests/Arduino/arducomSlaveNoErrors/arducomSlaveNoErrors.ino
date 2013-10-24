/* This is an example of how to use the ArduComSlave class.
 * First we have to define a function that will generate the response to incoming messages
 * 'prcoMsg' is just that: It prepends an 'x' to the incoming message
 * Then we declare a pointer to an ArduComSlave, 
 * we instatiate the ArduComSlave, then call its doInit method. Upon exit from that, it is ready to go.
 * Note that we have used 'Serial' as the serial object port.
 * in the loop(), we only have to call stepLoop() and the rest is magic.
 * test this by inputing at the Serial Monitor:
 * first type an 'A' to confirm init,
 * then type sequences of 5 chars and observing the responses.
 * NOTE: the librairy outQueue.h must be included for this to work, I do not know why...
 */

#include <outQueue.h>
#include <ArduCom.h>

boolean procMsg(char *buf,char*, int bufSize){
  // just for creating errors,
  // this is an 'ArduComResponseFunc'
    buf[0] =  'x';
  return true;
}
  
ArduComSlave *com;

//////////////  std functions ////////////////

void setup(){
  com = new ArduComSlave(&Serial,&procMsg,ARDUCOM_MSGSIZE);
  com->doInit();
}

void loop(){
  com->stepLoop();
}
