/*  Gratefulfrog
 *  2018 05 11


#include "app.h"
#define BAUD_RATE (115200)

const long baudRate = BAUD_RATE;


const int loopPauseTime =  200; // milli seconds

const char contactChar = '|',
           pollChar    = 'p',
           executeChar = 'x'; 

enum state  {contact, poll, execute};
state currentState = contact;

String incomingBitsAsString = "";
const int execIncomingLength = 16;// + 256;

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
  currentState = contact;
}

void initBitVec(){
  for (int i=0; i<bitVecNBBytes; i++){
    bitVec[i]=0;
  }
}

void initSerial(){
  Serial.begin(baudRate);
  while (!Serial);
}

void setup() {
  initSerial();
  initBitVec();
  establishContact();
}

int char2bit(char c){
  return c == '1' ? 1 : 0;
}

void setXValues(){
  // placeholder!
  // real code would set all the X output pins
  return;
}
void updateDevice(){
  // placeholder!
  return;
}
void readYValues(){
  // XXXX only for testing GUI XXX
  // real code woul read all the Y input pins
  yValues = xValues;
}

void execIncoming(){
  // take the string read and convert it to bit values,
  // assign the values
  // then update the device
  //Serial.println("execIncoming called");
  xValues = 0;
  for (int i=0; i<16; i++){
    xValues |= char2bit(incomingBitsAsString[i]) << (16-1 -i);
  }
  setXValues();
  // XXXX only for testing GUI XXX
  for (int i=0; i<bitVecNBBytes; i+=2){
    uint8_t l = (uint8_t)(((xValues & (255<<8))>>8) & 255),
            r = (uint8_t)(xValues & (255));
    bitVec[i]   = l;
    bitVec[i+1] = r;
  }
  updateDevice();
  readYValues();
  replyReady=true;
  currentState = contact;
}

void processIncoming(){
  char incomingChar = Serial.read();  
  switch(currentState){
    case (contact):
    case (poll):
      // we got a poll, it's ok to send the current X,Y,and bitVec values
      if (incomingChar == pollChar){
        replyReady = true;
      }
      // we got a settings command, 16 Xbits + 256 conection bits
      // init to read the string values of the bits
      else if (incomingChar == executeChar){
        currentState = execute;
        incomingBitsAsString = "";
      }
      break;
    case (execute):
      // we are reading in bits, keep on reading until done, then when we got
      // all the bits we need, execute the result
      incomingBitsAsString += incomingChar;
      if (incomingBitsAsString.length() == execIncomingLength){
        execIncoming();
      }
  }
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
  replyReady=false;
}
void loop() {
  if (Serial.available()>0){
    processIncoming();
  }
  if (replyReady){
    sendReply();
  }
}

*/
