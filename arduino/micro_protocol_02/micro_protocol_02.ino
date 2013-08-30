/* micro_protocol 02:
 * clears incoming buffer on error...
 * implements a serial protocol for receiving 5 bytes and tranlating them into
 * commands for pin writes
 * this version accepts strings of the form char[5]
 'ppvvv'  where p & v are on [0,9]
 and where int('pp') is on 0,13 or is 99 in case of heartbeat request
 and where int ('vvv') is on 0,255 or is 999 in case of heartbeat request
 *
 * This has been tested with pySerialRfcomm01.py and works perfectly!
 * updated 2013 03 28 for heartbeat
 */

// change USB_SERIAL to 0 to use the tx and rx pins
#define USB_SERIAL 0  
#if (USB_SERIAL)
#define SERIAL_CLASS Serial
#define SERIAL_CLASS_STRING "Serial"
#else
#define SERIAL_CLASS Serial1
#define SERIAL_CLASS_STRING "Serial1"
#endif

//////////////////////////
// start of protocol_01 global Variables
// const String protocolName = "protocol_01"; 

// NOTE: this is the config for:
//    3 PWM output pins 9,10,11
//    12 digital output pins
//    Pins 0 & 1 are left out for use in Serial1 comms
//    also, we set phase-correct PWM on timers 0 & 1, for pwm pins 9,10, 3,11
const int incomingMsgSize = 5,
          pwmPins[] = {9,10,11},
          nbPWMPins = 3,
          allPins[] = {2,3,4,5,6,7,8,9,10,11,12,13},  // 0 & 1 are usef for RX and TX
          nbOutputPins = 12;

const String badPin = String("e00001"),
             badVal =  String("e00002");
          
int currentCharCount = 0;

char incomingBuffer[5] = "";

// end of Global Variables
////////////////////////////  

void setup(){
  pwmSetup();
  serialSetup();
  protocolSetup();
  pinSetup();
}

void pwmSetup(){
  // set up the hardware timers for phase-correct, maximum speed PWM
  // timer 1: pin 9 & 10
  TCCR1B = _BV(CS10); // change the PWM frequencey to 31.25kHz   - pins 9 & 10 
  // or is it _BV(CS00) ???
  TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM10);  // phase-correct PWM on timer 1

  // timer 0 : pin 3 & 11
  TCCR0B = _BV(CS00); // change the PWM frequencey to 31.25 kHz  - pin 3 & 11
  TCCR0A = _BV(COM0A1) | _BV(COM0B1) | _BV(WGM00); // phase-correct pwm on timer 0  
}

void serialSetup(){
  // configure the Serial Object, then wait for the port to be ready
  SERIAL_CLASS.begin(9600);
  //SERIAL_CLASS.begin(115200);  // seems to add clicking?
  //SERIAL_CLASS.begin(1200);  // way too slow!

  
  while(!SERIAL_CLASS);
  //msg("initialized.");
}

void protocolSetup(){
  // currently there is nothing to setup here.
  //msg(protocolName + String(" initialized."));
}

void pinSetup(){
  // set all the pins to output mode
  // set all digital pins to LOW
  // set all analogPins to 0
  for (int i=0; i< nbOutputPins;i++){
    pinMode(allPins[i],OUTPUT);
    digitalWrite(allPins[i],LOW);
  }
  for (int i=0; i< nbPWMPins;i++){
    analogWrite(pwmPins[i],0);
  }
  //msg(String("Pins initialized."));
}

void msg(const String s){
  // output the string to the serial device; NOTE: '\n' is NOT added, 
  // flush the output to be sure it is sent
  //SERIAL_CLASS.print(String("Arduino ") + String(SERIAL_CLASS_STRING));
  //SERIAL_CLASS.println(": " + s);
  SERIAL_CLASS.print(s);
  SERIAL_CLASS.flush();
}

int dChar2D(const char c){
  // takes a charcter as input and return the corresponding digit as int
  // no error checking
  return int(map(c,'0','9',0,9));
}

boolean isIn(const int v, const int lis[], const int lisLen){
  // responds true id v is in lis up to lislen,
  // responds false otherwise.
  boolean res = false;
  for (int i=0;i<lisLen;i++){
    if (v==lis[i]){
      res=true;
      break;
    }
  }
  return res;
}

int io2Pin(const char* cp){
  // takes a pointer to a char[2], expecting only digits 
  // converts to a int
  // checks to be sure the resulting int is a member of allPins
  // returns a valid pin or -1 to indicate error
  int v0 = dChar2D(cp[0]),
      v1 = dChar2D(cp[1]);
  int res = int(v0*10+v1);
  if ((res != 99) && (!isIn(res,allPins,nbOutputPins))) { //(!isIn(res,allPins,nbOutputPins)) { 
    res = -1;
  }
  return(res);
}

int io2Val(const char* cv){
  // takes a pointer to a char[3], expecting only digits 
  // converts to a int
  // checks to be sure the resulting int is on [0,255]
  // returns a valid int or -1 to indicate error
  int v0 = dChar2D(cv[0]),
      v1 = dChar2D(cv[1]),
      v2 = dChar2D(cv[2]);
  int res = int(v0*100+v1*10+v2);
  if ((res != 999) && (res > 255)) { //(res>255) { 
    res = -1;
  }
  return(res);
}

boolean isPWM(const int p){
  // returns true if p is a member of pwmPins
  return isIn(p,pwmPins,nbPWMPins);
}

void  clearIncoming(){
  // somthing has gone wrong, clear the incoming serial stream.
  while (SERIAL_CLASS.read() != -1);
}

void executeIncomingString(){
  // uses global variable incomingBuffer to extract
  // char[2] + char[5] and convert them to pin and value,
  // in case of error the type of error is determined
  // if no error, exectues the pin setting to value
  // calls 'msg' with a reply saying
  //  aPPVVV : analogWrite, PP = pin, VVV = value
  //  dPPVVV : digitalWrite, PP = pin, VVV = value
  //  eCCCCC : error, CCCCC = error code value
  const int pin = io2Pin(incomingBuffer),
            val = io2Val(incomingBuffer+2);
  String reply = "",
         analog = "a",
         digital = "d", //;
         heartbeat = "x";
         
  if (pin<0) {
    reply = badPin;
    clearIncoming();
  }
  else if (val < 0){
    reply = badVal;
    clearIncoming();
  }    
  // add the heartbeat
  else if (pin == 99 && val == 999) {
    // don't change anything, just echo back that we are alive
    reply = heartbeat;
  }
  else if (isPWM(pin)){
    analogWrite(pin,val);
    reply = analog;
  }
  else if (val == 0) {
    digitalWrite(pin,LOW);
    reply = digital;
  }
  else {
    digitalWrite(pin,HIGH);
    reply = digital;
  }
  if (reply == digital || reply == analog || reply == heartbeat){ //(reply == digital || reply == analog){ 
      reply += pad(pin,2) + pad(val,3);
    }
  msg(reply);
}

String pad(int val,int places){
  // returns a String containgingc an int 'val' zero-padded to  length 'places'
  // no error checking
  String reply = String(val);
  const int missingZeros = places - reply.length();
  for (int i=0;i< missingZeros;i++){
    reply = String("0") + reply;
  }
  return (reply);
}

void loop(){
  // read characters on the Serial object one by one,
  // if a full message has been read, process it and reset counter
  // otherwise continue reading
  //
  // If we have a full message and can process it
  if (currentCharCount == incomingMsgSize) {
    executeIncomingString();
    currentCharCount = 0;
  }
  // if there's something to read, add it to the incoming buffer and update the
  // charcter count
  if (SERIAL_CLASS.available() > 0) {
    // read one char and add it to the buffer
    incomingBuffer[currentCharCount++] = SERIAL_CLASS.read();
  }
}

