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

uint16_t xValues = 0,
         yValues = 0;

const int bitVecNBBytes = 32;
uint8_t  bitVec[bitVecNBBytes];
         

// We need this function to establish contact with the Processing sketch
void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print(contactChar);   // send a char and wait for a response...
    delay(loopPauseTime);
  }
  Serial.read();
}

void initBitVec(){
  for (int i=0; i<bitVecNBBytes; i++){
    bitVec[i]=0;
  }
}

void setup() {
  Serial.begin(baudRate);
  while (!Serial);

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
  Serial.print(val2String(xValues,16));
  Serial.print(val2String(yValues,16));
  for (int i=0; i<bitVecNBBytes; i++){
    Serial.print(val2String(bitVec[i],8));
  }
}

int char2bit(char c){
  int res = c == '1' ? 1 : 0;
  //Serial.println(String("(") + c + "," + res + ")");
  return res ;
}

void readYValues(){
  // XXXX only for testing GUI XXX
  yValues = xValues;
  // to be completed on real board i.e. yValues[i] |= digitalRead(pin[i]) << i;
}
void setXValues(){
  xValues = 0;
  for (int i=0; i<16; i++){
    xValues |= char2bit(incomingBits[i]) << (16-1 -i);
  }
  // to be completed on real board i.e. digitalWrite(pin[i[,(xValues & 1<<i) ? 1 : 0);
}
void setConnections(){
  int strIndex=16;  // first of 256 bit characters
  for (int vecIndex = 0; vecIndex<bitVecNBBytes; vecIndex++){
    bitVec[vecIndex] = 0;
    for (int bitPos = 0; bitPos < 8; bitPos++){ 
      bitVec[vecIndex] |= char2bit(incomingBits[strIndex++]) <<(8-1-bitPos);
    }
  }
}

void execIncoming(){
  setXValues();
  setConnections();  
  readYValues();
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

