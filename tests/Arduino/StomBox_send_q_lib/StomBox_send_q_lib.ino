/* This is an example of how to use the ArduComMaster class.
 * First we have to define a function that will generate stuff to send on the comm.
 * 'processSerialMonitorIncoming()': this is the routine that gets stuff from the serial monitor.
 * Then we declare a pointer to an ArduComMaster,
 * instantiate it in setup(),  then call its doInit method. Upon exit from that, it is ready to go.
 * Note that we have used 'Serial1' as the serial object port.
 * in the loop(), we only have to call stepLoop() and the rest is magic.
 * test this by inputing at the Serial Monitor:
 * type in blocks of 5 chars, but not 'A' since that will be discarded,
 * then observe the responses.
 * NOTE: the librairy outQueue.h must be included for this to work, I do not know why...
 */

#include <outQueue.h>
#include <ArduCom.h>

/// Global Variables
int incomingMsgSizeSerial = ARDUCOM_MSGSIZE, 
    currentCharCountSerial = 0;   // how many chars we've read on Serial Terminal

char outgoingBuffer[ARDUCOM_MSGSIZE];

ArduComMaster *c;

///////////////////////////////////////////////////////////////////////////
/////////////  Terminal Input and equeueing       /////////////////////////
///////////////////////////////////////////////////////////////////////////
void processSerialMonitorIncoming() {
  // this is a part of the test suite, not of the ArduCom class 
  // If we have already read a whole atom, then enqueue it for sending, and reset char count
  // or, if we have something to read, add it to the current underwork atom
  if (currentCharCountSerial == incomingMsgSizeSerial){
    c->enqueueMsg(outgoingBuffer);
    ArduCom::msg("Enqueued:" ,outgoingBuffer,c->msgSize);
    currentCharCountSerial = 0;
  }
  else if (Serial.available()>0){
    outgoingBuffer[currentCharCountSerial++] = Serial.read();
  }
}


///////////////////////////////////////////////////////////////////////////
///////////////////       Std Functions     ///////////////////////////////
///////////////////////////////////////////////////////////////////////////
void setup(){
  Serial.begin(115200); // for input from Serial Monitor
  while(!Serial);
  delay(5000);           // to give the human time to start the Serial Monitor
  c = new ArduComMaster(&Serial1,&procReply,ARDUCOM_MSGSIZE);
  c->doInit();
  Serial.println("Ready!");
}
    
void loop(){
  // read and process anything from the Serial Monitor; 
  processSerialMonitorIncoming();
  // step the comms loop
  c->stepLoop();
}

