/*  Gratefulfrog
 *  2018 05 11
*/
const long baudRate = 115200;

const int loopPauseTime =  200; // milli seconds

const char contactChar = '|',
           pollChar    = 'p',
           executeChar = 'x'; 

enum state  {contact, poll, execute};
state currentState = contact;

int incompingCharCount = 0;
String incomingBits = "";
const int execIncomingLength = 16 + 256;

boolean replyReady = false;

const int bitVecNBBytes = 32;
uint8_t  bitVec[bitVecNBBytes];

// lower left side, these are output pins
int xPinVec[] = { 28, 39, 14, 30,
                  32, 34, 36, 40,
                  38, 29, 15, 31,
                  33, 35, 37, 41};

// vertical right side these are input pins
int yPinVec[] = { 2, 3, 4, 5,
                  6, 7, 8, 9,
                 10,11,12,18,
                 19,22,23,24};


// We need this function to establish contact with the Processing sketch
void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print(contactChar);   // send a char and wait for a response...
    delay(loopPauseTime);
  }
  Serial.read();
}

void initPins(){
  for (int i=0;i<16;i++){
    pinMode(xPinVec[i],OUTPUT);
    pinMode(yPinVec[i],INPUT);
  }
}

void initBitVec(){
  for (int i=0; i<bitVecNBBytes; i++){
    bitVec[i]=0;
  }
}

void setup() {
  Serial.begin(baudRate);
  while (!Serial);
  initPins();
  initBitVec();
  
  // wait for handshake
  establishContact();
  currentState = contact;
}

String val2String(uint32_t val,int len){
  String res = "";
  for (int i=0; i< len;i++){
    int v = (val & (1<<(len-1-i)));
    res+=v ? '1':'0';
  }
  return res;
}

void sendReply(){
  // x pins
  for (int i=0;i<16;i++){
    Serial.print(digitalRead(xPinVec[i]));
  }
  // y pins
  for (int i=0;i<16;i++){
    Serial.print(digitalRead(yPinVec[i]));
  }
  // spi bits received
  for (int i=0; i<bitVecNBBytes; i++){
    Serial.print(val2String(bitVec[i],8));
  }
}

int char2bit(char c){
  //int res = c == '1' ? 1 : 0;
  //Serial.println(String("(") + c + "," + res + ")");
  return c == '1' ? 1 : 0; //res ;
}

void setXValues(){
  for (int i=0; i<16; i++){
    digitalWrite(xPinVec[i],char2bit(incomingBits[i]));
  }
}

void setConnections(){
  int strIndex=16;  // first of 256 bit characters
  for (int vecIndex = 0; vecIndex<bitVecNBBytes; vecIndex++){
    bitVec[vecIndex] = 0;
    for (int bitPos = 0; bitPos < 8; bitPos++){ 
      bitVec[vecIndex] |= char2bit(incomingBits[strIndex++]) <<(8-1-bitPos);
    }
  }
  // send bits to chip here!
}

void execIncoming(){
  setXValues();
  setConnections();  
 }
 
void processIncoming(){
  char incomingChar = Serial.read();  
  switch(currentState){
    case (contact):
    case (poll):
      if (incomingChar == pollChar){
        replyReady = true;
      }
      else if (incomingChar == executeChar){
        currentState = execute;
        incomingBits = "";
      }
      break;
    case (execute):
      incomingBits += incomingChar;
      if (incomingBits.length() == execIncomingLength){
        execIncoming();
        replyReady=true;
        currentState = contact;
      }
  }
}

void loop() {
  if (Serial.available()>0){
    processIncoming();
  }
  if (replyReady){
    sendReply();
    replyReady=false;
  }
}

