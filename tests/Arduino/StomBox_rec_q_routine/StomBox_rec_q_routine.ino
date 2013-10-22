
// just for creating errors

boolean lastReplyStatus = true,
        initialized = false;

const char initChar = 'A';

/// Global Variables
const int incomingMsgSize = 5,
          outgoingMsgSize = 6;

int currentCharCount = 0;   // how many chars we've read

char incomingBuffer[incomingMsgSize]= "";
char outgoingBuffer[outgoingMsgSize] = "";


void doComm(){
  //Serial.write((byte*)outgoingBuffer,outgoingMsgSize);
  for (int i=0;i<outgoingMsgSize;i++){
    Serial.write(outgoingBuffer[i]);
  } 
} 

void executeIncomingString(){
  // after each atomic incoming msg, reply
  outgoingBuffer[0] = 'x';
  if (lastReplyStatus) { // then we want to make it error this time
    outgoingBuffer[0] = 'e';
  }
  for (int i=0;i<incomingMsgSize;i++){
    outgoingBuffer[i+1]= incomingBuffer[i];
  }
  lastReplyStatus = ! lastReplyStatus;
  doComm();
}

void processIncomingAtom(){
  // if a full message has been read, process it and reset counter
  // otherwise do nothing
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
    char c = Serial.read();
    if (c !=initChar){
      incomingBuffer[currentCharCount++] = c;
    }
  }
}

void doInit(){
  Serial.write(initChar);
  delay(100);
  if(Serial.available()>0){
    char c = Serial.read();
    if (c !=initChar){
      incomingBuffer[currentCharCount++] = c;
    }      
    initialized = true;
  }
}

//////////////  std functions ////////////////

void setup(){
  Serial.begin(115200);
  while (!initialized){
    doInit();
  }
}

void loop(){
  processIncomingAtom();
  readIntoAtom();
}
