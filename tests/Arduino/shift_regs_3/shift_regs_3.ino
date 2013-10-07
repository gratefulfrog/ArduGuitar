/*
  Shift Register Example
 for three 74HC595 shift registers

 This will cylce throug 7 leds on 3 shift regs, from pins 1-7 on each, in the proper order!

 Or it will read 2 digits from montior and light appropriate led
 knowing that the leds are on the following shift reg pins, and those are index valuess sued
 01 02 03 04 05 06 07   vol1 vol2 vol3 vol4 vol5  neck  middle
 09 10 11 12 13 14 15   ton1 ton2 ton3 ton4 ton5  bridgeNorth BridgeSouth
 17 18 19 20 21 22 23   pre1 pre2 pre3 pre4 auto  power connect

 Hardware:
 * 3 74HC595 shift register attached to pins 2, 3, and 4 of the Arduino,
 as detailed below.
 * LEDs attached to  outputs 1 through 7 of the shift register

 */

//Pin connected to latch pin (ST_CP) of 74HC595
const int latchPin = 13;
//Pin connected to clock pin (SH_CP) of 74HC595
const int clockPin = 12;
////Pin connected to Data in (DS) of 74HC595
const int dataPin = 11;

const int ledArraySize =24;
bool leds[ledArraySize];

void setup() {
  //set pins to output because they are addressed in the main loop
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  for (int i=0;i<ledArraySize;i++){
    leds[i] = false;
  }
  Serial.begin(9600);
  registerWrite();
  Serial.println("reset");
}

void loop(){
  iterateLeds();
}

void loopOld() {
//read 2 digits and set that led
  int r =read2Digits();
  if ((r > 0) && (r % 8 !=0) && (r < 24)){
    Serial.println("Read: " + String(r));
    leds[r] = !leds[r];
    for (int i=0;i<ledArraySize;i++){
      Serial.print(leds[i]);
    }
    Serial.print('\n');
    registerWrite();
    delay(50);
  }
}

void iterateLeds(){
  static int lastLedOn = 0;
  
  int nextLed = (lastLedOn + 1) % 24;
  
  if (nextLed %8== 0) {
    nextLed++;
  }
  
  leds[lastLedOn] = false;
  leds[nextLed] = true;
  lastLedOn = nextLed;
  registerWrite();
  delay(500);
} 

// This method sends bits to the shift registers:
void registerWrite() {
  // turn off the output so the leds don't light up
  // while you're shifting bits:
  digitalWrite(latchPin, LOW);

  byte outgoing[] = {0,0,0};
  for (int i =0;i<24;i++){
    if (leds[i]){
      outgoing[int(i/8)] |= 1 <<(7 - (i%8));
    }
  }

  Serial.println("outgoing[0] = " + String(outgoing[0]));
  Serial.println("outgoing[1] = " + String(outgoing[1]));  
  Serial.println("outgoing[2] = " + String(outgoing[2]));  
  
  for (int i = 2;i>-1 ;i--){
    shiftOut(dataPin, clockPin, LSBFIRST, outgoing[i]);
  }
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

