/*  Gratefulfrog
 *  2018 05 11
*/

#include "spiMgr.h"

#define UNO

#ifdef UNO
  #define SPI_SS (10)
#else // MEGA
  #define SPI_SS   (53)
#endif

// UNO SPI PINS
// CLK  13
// MISO 12
// MOSI 11
// SS   10

const long baudRate = 115200;

const int loopPauseTime =  200; // milli seconds

const char contactChar = '|',
           pollChar    = 'p',
           executeChar = 'x'; 

enum state  {contact, poll, execute};
state currentState = contact;

String g_incomingCharVec = "";

boolean g_replyReady = false;

const int g_ssPin  = SPI_SS,
          g_nbBits = 7,
          g_execIncomingLength = g_nbBits;

// We need this function to establish contact with the Processing sketch
void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print(contactChar);   // send a char and wait for a response...
    delay(loopPauseTime);
  }
  Serial.read();  
}

void initSerial(){
  Serial.begin(baudRate);
    while (!Serial);
}
void initPins(){
  pinMode(g_ssPin,OUTPUT);
}

// glogbal spi manager instance
SPIMgr *g_spi;

void initSPI(){
  g_spi =  new SPIMgr(g_ssPin,  // slave select pin 
                      LOW, // when is the chip selected for reading bits LOW or HIGH
                      false,  // should the slect pin be pulsed after input? the AD75019 requies it
                      SPIMGR_BIT_ORDER_MSB, 
                      SPIMGR_MODE0, 
                      SPIMGR_5MH_CLK_RATE); 
}

void setup() {
  initSerial();
  initPins();
  initSPI();
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


uint8_t g_outgoingBits = 0;

void execIncoming(){
  g_outgoingBits = 0;
  for (int i=0 ; i < g_nbBits;i++){
    g_outgoingBits |= (char2bit(g_incomingCharVec[i]) << (g_nbBits-1-i));
  }
  g_spi->send(g_outgoingBits);
 }

void sendReply(){
  Serial.println(String("Outgoing Bits : ") + val2String(g_outgoingBits,8));
}
 
void processIncoming(){
  char incomingChar = Serial.read();  
  switch(currentState){
    case (contact):
    case (poll):
      if (incomingChar == pollChar){
        g_replyReady = true;
      }
      else if (incomingChar == executeChar){
        currentState = execute;
        g_incomingCharVec = "";
      }
      break;
    case (execute):
      g_incomingCharVec += incomingChar;
      if (g_incomingCharVec.length() == g_execIncomingLength){
        execIncoming();
        g_replyReady=true;
        currentState = contact;
      }
  }
}
/*
void loop() {
  if (Serial.available()>0){
    processIncoming();
  }
  if (g_replyReady){
    sendReply();
    g_replyReady=false;
  }
}
*/
void loop(){
  static uint8_t b = 0;
  static int i = 0;
  g_spi->send(b);
  Serial.println(b,DEC);
  i= (b ==127 ? -1 : (b == 0) ? 1 : i);
  b = b+i;
  delay(500);
}

/*

const int bitVecNBBytes = 1,
          nbPins        = 1,
          nbBits        = 7,
          execIncomingLength = 7;
          
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


void initBitVec(){
  for (int i=0; i<bitVecNBBytes; i++){
    bitVec[i]=0;
  }
}

void sendReply(){
  // x pins
  for (int i=0;i<nbPins;i++){
    Serial.print(digitalRead(xPinVec[i]));
  }
  // y pins
  for (int i=0;i<nbPins;i++){
    Serial.print(digitalRead(yPinVec[i]));
  }
  // spi bits received
  for (int i=0; i<bitVecNBBytes; i++){
    Serial.print(val2String(bitVec[i],8));
  }
}

void setXValues(){
  for (int i=0; i<nbPins; i++){
    digitalWrite(xPinVec[i],char2bit(incomingBits[i]));
  }
}

void setConnections(){
  int strIndex=nbPins;  // first of 256 bit characters
  for (int vecIndex = 0; vecIndex<bitVecNBBytes; vecIndex++){
    bitVec[vecIndex] = 0;
    for (int bitPos = 0; bitPos < 8; bitPos++){ 
      bitVec[vecIndex] |= char2bit(incomingBits[strIndex++]) <<(8-1-bitPos);
    }
  }
  spi->send(bitVec,bitVecNBBytes);
  // send bits to chip here!
}


void execIncoming(){
  setXValues();
  setConnections();  
 }
*/
