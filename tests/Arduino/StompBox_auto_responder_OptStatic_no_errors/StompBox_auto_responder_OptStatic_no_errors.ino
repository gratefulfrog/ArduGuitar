// -*-c++-*-
/* This is an example of how to use the ArduComOptSlave class.
 * It simply ACK's anything it gets!
 * NOTE: It only works with the UNO Board!
 * This has been tested and works!
 */

#include <State.h>
#include <outQueueStatic.h>
#include <ArduComOptStatic.h>

boolean procMsg(char *buf, char*, byte){
  // just for ACKing anything received,
  // this is an 'ArduComOptResponseFunc'
  buf[0] =  'x';
  return true;
}
  
ArduComOptStaticSlave *com;

//////////////  std functions ////////////////

void setup(){
  com = new ArduComOptStaticSlave(&Serial,&procMsg,ARDUCOMOPTSTATIC_MSGSIZE);
  com->doInit();
}

void loop(){
  com->stepLoop();
}
