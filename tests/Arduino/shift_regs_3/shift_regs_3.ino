/*
  Shift Register Example
 for three 74HC595 shift registers

 This will cylce throug 7 leds on 3 shift regs, from pins 1-7 on each, in the proper order!

 Or it will read 2 digits from montior and light appropriate led
 knowing that the leds are on the following shift reg pins, and those are index valuess sued
 01 02 03 04 05 06 07
 09 10 11 12 13 14 15 
 17 18 19 20 21 22 32

 Hardware:
 * 3 74HC595 shift register attached to pins 2, 3, and 4 of the Arduino,
 as detailed below.
 * LEDs attached to  outputs 1 through 7 of the shift register

 Created 22 May 2009
 Modified 23 Mar 2010
 by Tom Igoe

 */

//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin = 8;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin = 12;
////Pin connected to Data in (DS) of 74HC595
const int dataPin = 11;

const int pinArraySize =24;
bool pins[pinArraySize];

void setup() {
  //set pins to output because they are addressed in the main loop
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  for (int i=0;i<pinArraySize;i++){
    pins[i] = false;
  }
  Serial.begin(9600);
  registerWrite();
  Serial.println("reset");
}

void loop() {

//read 2 digits and set that led
  int r =read2Digits();
  if ((r > 0) && (r % 8 !=0) && (r < 24)){
    Serial.println("Read: " + String(r));
    pins[r] = !pins[r];
    for (int i=0;i<pinArraySize;i++){
      Serial.print(pins[i]);
    }
    Serial.print('\n');
    registerWrite();
    delay(50);
  }
}
/*
  // iterate over the 16 outputs of the two shift registers
  for (int thisLed = 1; thisLed < 24; thisLed++) {
    registerWrite(thisLed, HIGH);
    if ( thisLed% 8 !=0 ) {
      delay(500);
    }
  }
}
*/

// This method sends bits to the shift registers:
void registerWrite() {
  // turn off the output so the pins don't light up
  // while you're shifting bits:
  digitalWrite(latchPin, LOW);

  // break the bits into two bytes, one for 
  // the first register and one for the second:
  unsigned int bits2Send[2] = {0,0};
  for (int i=0;i<16;i++){
    if (pins[i]){
      bits2Send[0] |= (1 << (i));
    }
  }
  for (int i=16;i<24;i++){
    if (pins[i]){
      bits2Send[1] |= (1 << (i-16));
    }
  }
  Serial.println("bits2send[0] = " + String(bits2Send[0]));
  Serial.println("bits2send[1] = " + String(bits2Send[1]));  
  byte registerOne = highByte(bits2Send[0]);
  byte registerTwo = lowByte(bits2Send[0]);
  byte registerThree = highByte(bits2Send[1]);
  byte registerFour = lowByte(bits2Send[1]);
  

  // shift the bytes out:
  //shiftOut(dataPin, clockPin, MSBFIRST, registerThree);
  shiftOut(dataPin, clockPin, MSBFIRST, registerFour);  // second low bits reg 3
  shiftOut(dataPin, clockPin, MSBFIRST, registerOne);   // first high bits  reg 2
  shiftOut(dataPin, clockPin, MSBFIRST, registerTwo);   // first low bits   reg 1
  
  // turn on the output so the LEDs can light up:
  digitalWrite(latchPin, HIGH);
}

// This method sends bits to the shift registers:
void registerWrite(int whichPin, int whichState) {
  // the bits you want to send. Use an unsigned int,
  // so you can use all 16 bits:
  unsigned int bitsToSend1 = 0,
               bitsToSend2 = 0;    

  // turn off the output so the pins don't light up
  // while you're shifting bits:
  digitalWrite(latchPin, LOW);

  // turn on the next highest bit in bitsToSend:
  if (whichPin < 16){
    bitWrite(bitsToSend1, whichPin, whichState);
  }
  else {
    bitWrite(bitsToSend2, whichPin-16, whichState);
  }

  Serial.println(bitsToSend1);
  Serial.println(bitsToSend2);  
  

  // break the bits into two bytes, one for 
  // the first register and one for the second:
  byte registerOne = highByte(bitsToSend1);
  byte registerTwo = lowByte(bitsToSend1);
  byte registerThree = highByte(bitsToSend2);
  byte registerFour = lowByte(bitsToSend2);
  

  // shift the bytes out:
  //shiftOut(dataPin, clockPin, MSBFIRST, registerThree);
  shiftOut(dataPin, clockPin, MSBFIRST, registerFour);  // second low bits reg 3
  shiftOut(dataPin, clockPin, MSBFIRST, registerOne);   // first high bits  reg 2
  shiftOut(dataPin, clockPin, MSBFIRST, registerTwo);   // first low bits   reg 1
  
  // turn on the output so the LEDs can light up:
  digitalWrite(latchPin, HIGH);
}


int read2Digits(){
  static int count = 0;
  static char s[3] = {0,0,0};
  int ret = -1;
  
  while (Serial.available()>0){
    s[count++] = Serial.read();
    if (count ==2){
      ret = atoi(s);
      count = 0;
      s[0] = s[1] = 0;
    }  
  }
  return ret;
}

