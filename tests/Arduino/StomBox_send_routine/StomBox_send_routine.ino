

/// Global Variables
const int incomingMsgSizeSerial1 = 6,
          outgoingMsgSizeSerial1 = 5,
          incomingMsgSizeSerial = 5,
          maxMsgs = 30;
const char errorClearChar = 'z';

int currentCharCountSerial = 0,   // how many chars we've read on Serial or Serial1
    currentCharCountSerial1 = 0,
    currentOutgoingIndexSerial1 = 0,
    currentIncomingIndexSerial1 = 0,
    errorClearCount = incomingMsgSizeSerial1;

char incomingBufferSerial1[incomingMsgSizeSerial1],
     outgoingBufferSerial1[maxMsgs][outgoingMsgSizeSerial1];

boolean errorMode = false;

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

void incMod(int *num, const int maxNum){
  *num = (*num + 1 ) % maxNum;
}

void sendAtomSerial1(char *m){
  Serial1.write((byte*)m,outgoingMsgSizeSerial1);
  //delay(5);
  msg("Sent atom: ", m,outgoingMsgSizeSerial1);
}

void sendCurrentOutgoingSerial1(){
  sendAtomSerial1(outgoingBufferSerial1[currentOutgoingIndexSerial1]);
  incMod(&currentOutgoingIndexSerial1,maxMsgs);
  currentCharCountSerial = 0;
}

void processSerialMonitorIncoming() {
 if (currentCharCountSerial == incomingMsgSizeSerial){
   sendCurrentOutgoingSerial1();
 }
 else if (Serial.available()>0){
   outgoingBufferSerial1[currentOutgoingIndexSerial1][currentCharCountSerial++] = Serial.read();
 }
}

void resendCurrentMsgsSerial1(){
  for (int i = currentIncomingIndexSerial1; i != currentOutgoingIndexSerial1; incMod(&i,maxMsgs)){
    sendAtomSerial1(outgoingBufferSerial1[i]);
  }
}

boolean areEqualTops() {
  boolean ret = true;
  for (int i=0;i<outgoingMsgSizeSerial1;i++){
    if (outgoingBufferSerial1[currentIncomingIndexSerial1][i] != incomingBufferSerial1[i+1]){
      ret = false;
      break;
    }
  }
  return ret;
}

// version checks for matching acks, does not work!
void processCurrentIncomingSerial1(){
  msg("Processing from Serial1: ",incomingBufferSerial1,incomingMsgSizeSerial1);
  // here we have a full reply from the other Arduino, at incomingBufferSerial1
  if (incomingBufferSerial1[0] =='e'){
    //error detected! must resend all the past
    msg("Error detected!");
    errorMode = true;
    //resendCurrentMsgsSerial1();
  }
  else if (areEqualTops()){
    //  then we are good to go on next element, effectively popping the outgoing head
    msg("ok detected! popping!!");
    incMod(&currentIncomingIndexSerial1,maxMsgs);
  }  
  else {
    // something is bad... set error mode
    msg("no error but no match, setting errorMode...");
    msg("current incoming Serial1: ",incomingBufferSerial1,incomingMsgSizeSerial1);
    errorMode = true;
  }
  currentCharCountSerial1 = 0;
}

/*
void processCurrentIncomingSerial1(){
  msg("Processing from Serial1: ",incomingBufferSerial1,incomingMsgSizeSerial1);
  // here we have a full reply from the other Arduino, at incomingBufferSerial1
  if (incomingBufferSerial1[0] =='e'){
    //error detected! must resend all the past
    msg("Error detected!");
    resendCurrentMsgsSerial1();
  }
  else{
    //  then we are good to go on next element, effectively popping the outgoing head
    msg("ok detected! popping!!");
    incMod(&currentIncomingIndexSerial1,maxMsgs);
  }  
  currentCharCountSerial1 = 0;
}
*/

void ProcessSerial1Incoming(){
if (currentCharCountSerial1 == incomingMsgSizeSerial1){
   msg("called processCurrentIncomingSerial1");
   processCurrentIncomingSerial1();
 }
 else if (Serial1.available()>0){
   incomingBufferSerial1[currentCharCountSerial1++] = Serial1.read();
   //msg("read a char on Serial1: ",&incomingBufferSerial1[currentCharCountSerial1-1],1);
 }
}  

void  clearErrorMode(){
  if (Serial1.available()>0){
    if(errorClearChar == Serial1.read()){
      errorClearCount--;
    }
  }
  else {
    Serial1.write(errorClearChar);
    delay(5);
  }
  if (errorClearCount == 0){ //all good
    errorClearCount = incomingMsgSizeSerial1;
    errorMode = false;
    currentCharCountSerial1 = 0;
    resendCurrentMsgsSerial1();
  }
}

//////  Std Functions //////

void setup(){
  Serial.begin(115200); // for input from Serial Monitor
  while(!Serial);
  Serial1.begin(115200); // for comm to toher arduino
  while(!Serial1);
}
    
void loop(){
  if (!errorMode){
    // read and process anything from the Serial Monitor; this includes sending to other arduino
    processSerialMonitorIncoming(); 
    // read an process replies from other arduino; includes writing to serial montior and error handling
    ProcessSerial1Incoming();   
  }
  else {
    clearErrorMode();
  }
}
/*
int tempCount = 0;
void loop(){
  if (Serial.available()>0){
    Serial1.write(Serial.read());
  }
  if (Serial1.available()>0){
    Serial.write(Serial1.read());
    ++tempCount ;
  }
  if (tempCount >10){
    tempCount=0;
    Serial.println();
  }
}
*/
