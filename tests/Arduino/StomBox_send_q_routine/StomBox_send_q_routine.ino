/* timeout is bad!
 * this version uses a boolean to prime the pump!
 */


#include <outQueue.h>

/// Global Variables

outQueue *q;

boolean atomAckedOnSerial1 = false,   // this is true when the last sent atom on Serial1 has been acked
        initialized = false;

const char initChar = 'A';        

const int incomingMsgSizeSerial1 = outQueue::eLen +1,
          outgoingMsgSizeSerial1 = outQueue::eLen,
          incomingMsgSizeSerial = outQueue::eLen,
          initDelay = 100;  // used to give the other Arduino a chance to send something at startup

int currentCharCountSerial = 0,   // how many chars we've read on Serial or Serial1
    currentCharCountSerial1 = 0;

char incomingBufferSerial1[incomingMsgSizeSerial1],
     outgoingBufferSerial1[outgoingMsgSizeSerial1];


///////////////////////////////////////////////////////////////////////////
///////////////////  Human Monitoring Stuff ///////////////////////////////
///////////////////////////////////////////////////////////////////////////
void msg(String s){
  // send stuff to the serial terminal for human observation
  Serial.println(s);
}

void   msg(String s, char *c, int len){
  // send stuff to the serial terminal for human observation
  // allows a string plus a un-terminated char array to be sent
  char buff[len+1];
  for (int i=0;i< len;i++){
    buff[i]=  c[i];
  }
  buff[len] = '\0';
  msg (s + buff);
}

///////////////////////////////////////////////////////////////////////////
/////////////  Terminal Input and equeueing       /////////////////////////
///////////////////////////////////////////////////////////////////////////

void enQueueCurrentOutgoingSerial1(){
  // take the current whole atom, enqueue it
  q->enQ(outgoingBufferSerial1);
  msg("Enqueued:" ,outgoingBufferSerial1,5);
}

void processSerialMonitorIncoming() {
  // If we have already read a whole atom, then enqueue it for sending, and reset char count
  // or, if we have something to read, add it to the current underwork atom
  if (currentCharCountSerial == incomingMsgSizeSerial){
    enQueueCurrentOutgoingSerial1();
    currentCharCountSerial = 0;
  }
  else if (Serial.available()>0){
    outgoingBufferSerial1[currentCharCountSerial++] = Serial.read();
  }
}

///////////////////////////////////////////////////////////////////////////
///////////////////  Serial1 Reading and writing  /////////////////////////
///////////////////////////////////////////////////////////////////////////

void sendAtomSerial1(char *m){
  // send the raw char array, and set atomAckedOnSerial1 to false, 
  // so that the Queue won't be popped until we get the ACK
  if (m != NULL){
    Serial1.write((byte*)m,outgoingMsgSizeSerial1);
    msg("Sent atom: ", m,outgoingMsgSizeSerial1);
    atomAckedOnSerial1 =false;
  }
}

boolean incomingSerial1Ok(){
  // if it starts with e, then not ok!
  // otherwise, if any of the chars do not match the last sent, i.e. the top of the queue, 
  // then not ok.
  if(incomingBufferSerial1[0] == 'e'){
    return false;
  }
  boolean ret = true;
  char *sent = q->pQ();
  for (int i=1; i< incomingMsgSizeSerial1;i++){
    if (sent[i-1] != incomingBufferSerial1[i]){
      ret = false;
      break;
    }
  }
  return ret;
}
  
void processCurrentIncomingSerial1(){
  // We have received an incoming atom from Serial1,
  // if it is ok, then we confirm ack and can pop the queue 
  // if it is not ok, then we do not pop the queue and do not set the ACK
  // in any event, we try to send the atom currently at the top of the queue, 
  if(incomingSerial1Ok()){
    char *c = q->deQ();
    msg("dq'd: ",c,5);
    atomAckedOnSerial1 = true;
  }
  // so it's ok and we moved on, or it's not ok and we are still at the same on
  sendAtomSerial1(q->pQ());  // try to send the next one, or the last one again 
}

void ProcessSerial1Incoming(){
  // do one of the following:
  // if the current incoming atom is complete, then process it,
  // or, if there is something to read on Serial1, add it to the current incoming atom,
  // or, if it is ok to send something, then send the atom at the head of the queue
  if (currentCharCountSerial1 == incomingMsgSizeSerial1){
    msg("Rec'd reply: ",incomingBufferSerial1,incomingMsgSizeSerial1);
    processCurrentIncomingSerial1();
    currentCharCountSerial1 = 0;
  }
  else if (Serial1.available()>0){
    char c = Serial1.read();
    if (c != initChar){
      incomingBufferSerial1[currentCharCountSerial1++] = c;
    }
    else{
      Serial1.write(initChar);  // to clear an init call!
    }
    msg("Rec'd a char : ",&c,1);
  }
  else if (atomAckedOnSerial1){
    // try to send the top of the queue, NOT only to prime the pump, 
    // because:
    // at init, there is nothing on Serial1,
    // but we consider that no atoms sent have been Acked, so atomAckedOnSerial1 is true,
    // when we send an Atom on Serial1, acked goes to false,
    // then if we have read an atom or if we are reading, we don't get here
    // and if we have read an atom, then acked may go to true and the queue is popped,
    // which would imply that the top sent, if there is one! 
    // But what if there is nothing in the queue? then, we return to the initial state and
    // this branch of the if will get called if an outgoing atom is enqueued.
    sendAtomSerial1(q->pQ());  
  }
}  

///////////////////////////////////////////////////////////////////////////
///////////////////   Establishment of Comm ///////////////////////////////
///////////////////////////////////////////////////////////////////////////

void checkInit(){
  // wait for the other Arduino to send a char, if it is the initChar, then we can start
  // so we are "initialized" and the last sent atom has been acked, since there are none
  // if not just ignore the char as garbage... and pause for a short while.
  if (Serial1.available()>0){
    char c = Serial1.read();
    if (c==initChar){
      atomAckedOnSerial1 = initialized= true;
      Serial1.write(initChar);
      delay(initDelay);
    }
  }
}

///////////////////////////////////////////////////////////////////////////
///////////////////       Std Functions     ///////////////////////////////
///////////////////////////////////////////////////////////////////////////
void setup(){
  q = new outQueue();
  Serial.begin(115200); // for input from Serial Monitor
  while(!Serial);
  Serial1.begin(115200); // for comm to other arduino
  while(!Serial1);
  delay(5000);           // to give the human time to start the Serial Monitor
  while (!initialized){
    checkInit();
  }
  Serial.println("Ready!");
}
    
void loop(){
  // read and process anything from the Serial Monitor; 
  processSerialMonitorIncoming(); 
  // read an process replies from other arduino; includes writing to serial montior and error handling
  // this includes sending to other arduino
  ProcessSerial1Incoming();   
}

