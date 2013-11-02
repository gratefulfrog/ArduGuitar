/* This is an example of how to use the ArduComOptMaster class.
 * First we have to define a function that will generate stuff to send on the comm.
 * 'processSerialMonitorIncoming()': this is the routine that gets stuff from the serial monitor.
 * Then we declare a pointer to an ArduComOptMaster,
 * instantiate it in setup(),  then call its doInit method. Upon exit from that, it is ready to go.
 * Note that we have used 'Serial1' as the serial object port.
 * in the loop(), we only have to call stepLoop() and the rest is magic.
 * test this by inputing at the Serial Monitor:
 * type in blocks of 5 chars, but not 'A' since that will be discarded,
 * then observe the responses.
 * NOTE: the librairy outQueue.h must be included for this to work, I do not know why...
 * NOTE:  ArduComOpt DEBUG must be enabled by removing commented lines indicated by DEBUG
 */

#include <outQueue.h>
#include <ArduComOpt.h>

/// Global Variables
int incomingMsgSizeSerial = ARDUCOMOPT_MSGSIZE, 
    currentCharCountSerial = 0;   // how many chars we've read on Serial Terminal

char outgoingBuffer[ARDUCOMOPT_MSGSIZE];

ArduComOptMaster *c;


int freeRam (){
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

///////////////////////////////////////////////////////////////////////////
/////////////  Terminal Input and equeueing       /////////////////////////
///////////////////////////////////////////////////////////////////////////
void processSerialMonitorIncoming() {
  // this is a part of the test suite, not of the ArduComOpt class 
  // If we have already read a whole atom, then enqueue it for sending, and reset char count
  // or, if we have something to read, add it to the current underwork atom
  if (currentCharCountSerial == incomingMsgSizeSerial){
    Serial.print("FreeRam: ");
    Serial.println(freeRam());
    c->enqueueMsg(outgoingBuffer);
    ArduComOpt::msg("Enqueued:" ,outgoingBuffer,c->msgSize);
    currentCharCountSerial = 0;
    Serial.print("FreeRam: ");
    Serial.println(freeRam());
  }
  else if (Serial.available()>0){
    outgoingBuffer[currentCharCountSerial++] = Serial.read();
  }
}
///////////////////////////////////////////////////////////////////////////
///////////////////       Std Functions     ///////////////////////////////
///////////////////////////////////////////////////////////////////////////
void setup(){
  Serial.begin(ARDUCOMOPT_BAUDRATE); // for input from Serial Monitor
  while(!Serial);
  delay(5000);           // to give the human time to start the Serial Monitor
  c = new ArduComOptMaster(&Serial1,ARDUCOMOPT_MSGSIZE);
  c->doInit();
  delay(5000);
  Serial.println("Ready!");
  Serial.print("FreeRam: ");
  Serial.println(freeRam());
}
    
void loop(){
  // read and process anything from the Serial Monitor; 
  processSerialMonitorIncoming();
  // step the comms loop
  c->stepLoop();
}

