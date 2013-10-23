/* This is the same as StomBox_req_q_routine, but
 * using the embryonic ArduCom class.
 */

#include "ArduCom.h"

void procMsg(char *buf, int bufSize){
  // just for creating errors
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
  com = new ArduCom(&Serial,&procMsg,ARDUCOM_MSGSIZE);
  com->doInit();
}

void loop(){
  com->stepLoop();
}
