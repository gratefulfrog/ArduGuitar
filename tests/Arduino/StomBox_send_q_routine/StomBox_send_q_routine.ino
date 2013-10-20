/* timeout is bad!
 * this version uses a boolean to prime the pump!
 */


#include <outQueue.h>

/// Global Variables

outQueue *q;

boolean ok2Send = false,
        initialized = false;

const char initChar = 'A';        

const int incomingMsgSizeSerial1 = outQueue::eLen +1,
          outgoingMsgSizeSerial1 = outQueue::eLen,
          incomingMsgSizeSerial = outQueue::eLen;

int currentCharCountSerial = 0,   // how many chars we've read on Serial or Serial1
    currentCharCountSerial1 = 0;

char incomingBufferSerial1[incomingMsgSizeSerial1],
     outgoingBufferSerial1[outgoingMsgSizeSerial1];


void msg(String s){
  Serial.println(s);
}

void   msg(String s, char *c, int len){
  char buff[len+1];
  for (int i=0;i< len;i++){
    buff[i]=  c[i];
  }
  buff[len] = '\0';
  msg (s + buff);
}

void sendAtomSerial1(char *m){
  if (m != NULL){
    Serial1.write((byte*)m,outgoingMsgSizeSerial1);
    msg("Sent atom: ", m,outgoingMsgSizeSerial1);
    ok2Send =false;
  }
}

void enQueueCurrentOutgoingSerial1(){
  q->enQ(outgoingBufferSerial1);
  msg("Enqueued:" ,outgoingBufferSerial1,5);
}

void processSerialMonitorIncoming() {
 if (currentCharCountSerial == incomingMsgSizeSerial){
   enQueueCurrentOutgoingSerial1();
   currentCharCountSerial = 0;
 }
 else if (Serial.available()>0){
   outgoingBufferSerial1[currentCharCountSerial++] = Serial.read();
 }
}

boolean incomingSerial1Ok(){
  // if it starts with e, then not ok!
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
  if(incomingSerial1Ok()){
    char *c = q->deQ();
    msg("dq'd: ",c,5);
    ok2Send = true;
  }
  // so it's ok and we moved on, or it's not ok and we are still at the same on
  sendAtomSerial1(q->pQ());  // try to send the next one
}

void ProcessSerial1Incoming(){
if (currentCharCountSerial1 >= incomingMsgSizeSerial1){
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
 else if (ok2Send){
   sendAtomSerial1(q->pQ());  // try to send the top of the queue
 }
}  

void checkInit(){
  if (Serial1.available()>0){
    char c = Serial1.read();
    if (c==initChar){
      ok2Send = initialized= true;
      Serial1.write(initChar);
      delay(100);
    }
  }
}

//////  Std Functions //////

void setup(){
  q = new outQueue();
  Serial.begin(115200); // for input from Serial Monitor
  while(!Serial);
  Serial1.begin(115200); // for comm to toher arduino
  while(!Serial1);
  delay(5000);
  while (!initialized){
    checkInit();
  }
  Serial.println("Ready!");
}
    
void loop(){
  // read and process anything from the Serial Monitor; this includes sending to other arduino
  processSerialMonitorIncoming(); 
  // read an process replies from other arduino; includes writing to serial montior and error handling
  ProcessSerial1Incoming();   
}

