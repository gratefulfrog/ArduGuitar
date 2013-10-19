
/// Global Variables
const int incomingMsgSize = 5,
          outgoingMsgSize = 6;

const char errorClearChar = 'z';

int currentCharCount = 0,   // how many chars we've read
    errorClearCount = incomingMsgSize;

char incomingBuffer[incomingMsgSize]= "";
char outgoingBuffer[outgoingMsgSize] = "";

boolean lastReplyStatus = false,
        errorMode = false;


void processIncomingAtom(){
  // read characters on the Serial object one by one,
  // if a full message has been read, process it and reset counter
  // otherwise continue reading
  //
  // If we have a full message and can process it
  if (currentCharCount == incomingMsgSize) {
    executeIncomingString();
    currentCharCount = 0;
  }
}

void readIntoAtom(){
  // if there's something to read, add it to the incoming buffer and update the
  // charcter count
  if (Serial.available() > 0) {
    // read one char and add it to the buffer if ok:
    char c  = Serial.read();
    if (c == errorClearChar){
      errorMode = true;
      errorClearCount--;
    }
    else {
      incomingBuffer[currentCharCount++] = c;
    }
  }
}

void executeIncomingString(){
  // after each atomic incoming msg, reply
  outgoingBuffer[0] = 'x';
  if (lastReplyStatus) { // then we want to make it error this time
    outgoingBuffer[0] = 'e';
    errorMode = true;
  }
  for (int i=0;i<incomingMsgSize;i++){
    outgoingBuffer[i+1]= incomingBuffer[i];
  }
  lastReplyStatus = ! lastReplyStatus;
  doComm();
}

void doComm(){
  for (int i=0;i<outgoingMsgSize;i++){
    Serial.write(outgoingBuffer[i]);
    //delay(1);  
  } 
} 

void  clearErrorMode(){
  if (errorClearCount == 0){ //all good
    errorClearCount = incomingMsgSize;
    errorMode = false;
    currentCharCount = 0;
    for (int i=0;i<outgoingMsgSize;i++){
      outgoingBuffer[i] = errorClearChar;
    }
    doComm();
  }
  else if (Serial.available()>0){
    if(errorClearChar == Serial.read()){
      errorClearCount--;
    }
  }
}

//////////////  std functions ////////////////

void setup(){
  Serial.begin(115200);
}

void loop(){
  if (!errorMode){
    processIncomingAtom();
    readIntoAtom();
  }
  else {
    clearErrorMode();
  } 
}
